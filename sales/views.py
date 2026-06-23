# ============================================================================
# 第一部分：导入模块
# ============================================================================
import json  # JSON 序列化/反序列化，用于 API 请求和响应
import uuid  # 生成通用唯一标识符，用于订单号、幂等键、支付流水号
import redis  # Redis 客户端，用于缓存、分布式锁、库存预扣减
import hashlib  # 哈希算法，用于微信支付签名
import logging  # 日志记录，用于调试和问题追踪
from decimal import Decimal  # 高精度小数，用于金额计算（避免浮点数精度问题）

from django.shortcuts import render, redirect  # 渲染模板和重定向
from django.http import JsonResponse, HttpResponse  # JSON响应和HTTP响应
from django.views.decorators.csrf import csrf_exempt  # 禁用CSRF验证（API接口和回调需要）
from django.db import transaction, IntegrityError  # 数据库事务和完整性错误处理
from django.db.models import F, Q, Avg, Sum, Count  # 数据库查询辅助（F表达式、Q查询、聚合函数）
from django.utils import timezone  # 时区感知的时间处理
from django.contrib.auth.decorators import login_required  # 登录验证装饰器
from django.conf import settings  # Django配置

from app01.models import UserInfo  # 自定义用户模型
from .models import (  # 本应用的所有模型
    Product,  # 产品模型
    ProductImage,  # 产品图片模型
    Warehouse,  # 仓库模型
    ProductWarehouse,  # 产品仓库关联（库存明细）
    Order,  # 订单模型
    OrderLogistics,  # 物流追踪模型
    PaymentRecord,  # 支付记录模型
    IdempotentKey,  # 幂等键模型（防止重复支付）
    ProductReview,  # 用户评价模型
    ReviewImage,  # 评价图片模型
    UserFeedback,  # 用户反馈模型
    Seller  # 卖家/商户模型
)
from .pay import get_payment_provider  # 支付提供者工厂函数

# 获取当前模块的日志记录器
logger = logging.getLogger(__name__)

# ============================================================================
# 第二部分：Redis 连接和 Lua 脚本
# ============================================================================

# Redis 连接池 - 复用连接，提高性能
redis_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,  # Redis 主机地址
    port=settings.REDIS_PORT,  # Redis 端口
    password=settings.REDIS_PASSWORD,  # Redis 密码
    db=settings.REDIS_DB_BUSINESS  # 使用独立的数据库（避免与Celery/Channels冲突）
)
redis_client = redis.Redis(connection_pool=redis_pool)

# Lua 脚本：原子预扣减库存
# 为什么要用 Lua 脚本？因为 Redis 是单线程的，Lua 脚本在 Redis 中执行是原子的，
# 可以在一次 Redis 调用中完成"读取-判断-扣减"三个操作，避免并发问题
DECR_STOCK_SCRIPT = """
local key = KEYS[1]          -- Redis 键名，格式为 "stock:{product_id}"
local qty = tonumber(ARGV[1]) -- 要扣减的数量
local current = tonumber(redis.call('get', key) or '0')  -- 获取当前库存
if current >= qty then       -- 如果库存充足
    redis.call('decrby', key, qty)  -- 原子扣减库存
    return 1                 -- 返回 1 表示成功
else
    return 0                 -- 返回 0 表示库存不足
end
"""
# 注册 Lua 脚本到 Redis，可以在 Python 中调用
decr_stock = redis_client.register_script(DECR_STOCK_SCRIPT)


# ============================================================================
# 第三部分：权限辅助函数
# ============================================================================

def get_user_role_by_account(account):
    """
    功能：根据用户账号获取用户角色
    作用：用于权限控制，判断用户是管理员还是普通用户
    工作流程：
    1. 如果账号为空，返回 'anonymous'（匿名用户）
    2. 查询 UserInfo 表获取用户对象
    3. 检查是否为超级用户（Django 自带的 is_superuser）
    4. 检查自定义角色表中是否有 'admin'、'sales_admin'、'DQA_SW_edit'
    5. 如果都没有，返回 'normal'（普通用户）
    """
    if not account:
        return 'anonymous'
    user = UserInfo.objects.filter(account=account).first()
    if not user:
        return 'anonymous'
    if hasattr(user, 'is_superuser') and user.is_superuser:
        return 'admin'
    roles = user.role.all()
    for role in roles:
        if role.name in ['admin', 'sales_admin', 'DQA_SW_edit']:
            return 'admin'
    return 'normal'


def can_edit_product(account):
    """
    功能：检查用户是否有编辑产品的权限
    作用：只有管理员才能新增、修改、删除产品
    """
    role = get_user_role_by_account(account)
    return role == 'admin'


def get_current_user(account):
    """
    功能：根据账号获取当前用户对象
    作用：在创建订单等操作中，需要关联当前登录用户
    """
    if not account:
        return None
    return UserInfo.objects.filter(account=account).first()


# ============================================================================
# 第四部分：支付回调处理函数（核心！）
# ============================================================================

def _process_payment_callback(payment_no, success=True, extra_data=None):
    """
    ════════════════════════════════════════════════════════════════════════════
    功能：处理支付回调的核心逻辑
    作用：当第三方支付平台（微信/支付宝）异步通知支付结果时调用
    ════════════════════════════════════════════════════════════════════════════

    什么是"回调"（Callback）？
    ────────────────────────────────────────────────────────────────────────────
    用户支付后，支付平台不会等待你的系统来查询结果，而是主动发送一个 HTTP 请求
    到你指定的 URL（即 notify_url），告诉你的系统"用户已经支付成功了"。
    这个主动通知的过程就叫"回调"。

    回调流程：
    ────────────────────────────────────────────────────────────────────────────
    1. 用户支付成功 → 支付平台生成交易号
    2. 支付平台立即向你的 notify_url 发送 POST 请求
    3. 你的系统收到通知后，验证签名、更新订单状态、扣减库存
    4. 返回 'success' 告诉支付平台"已处理完成"，支付平台停止重试

    什么是"幂等性"（Idempotent）？
    ────────────────────────────────────────────────────────────────────────────
    幂等性是指：同样的操作执行多次，结果和执行一次完全相同。
    在支付系统中，幂等性极其重要，因为：
    - 网络抖动可能导致支付平台重复发送回调
    - 你的系统处理回调时可能超时，支付平台会重试
    - 如果不做幂等，重复回调会导致：重复发货、重复扣库存、资金损失

    本系统的幂等实现（三层防护）：
    ────────────────────────────────────────────────────────────────────────────
    第一层：Redis 缓存 - key: "idempotent:{idempotent_key}"，快速返回结果
    第二层：数据库唯一约束 - IdempotentKey.idempotent_key UNIQUE
    第三层：状态机乐观锁 - WHERE id=xxx AND status='期望值'
    """
    try:
        # ──────────────────────────────────────────────────────────────────────
        # 步骤 1：根据支付流水号查询支付记录
        # ──────────────────────────────────────────────────────────────────────
        payment = PaymentRecord.objects.get(payment_no=payment_no)

        # ──────────────────────────────────────────────────────────────────────
        # 步骤 2：如果已经成功，直接返回（幂等性保证）
        # ──────────────────────────────────────────────────────────────────────
        if payment.status == 'SUCCESS':
            return

        # ──────────────────────────────────────────────────────────────────────
        # 步骤 3：开启数据库事务（保证原子性，要么全部成功，要么全部失败）
        # ──────────────────────────────────────────────────────────────────────
        with transaction.atomic():
            if success:
                # ============================================================
                # 分支 A：支付成功
                # ============================================================

                # 3a. 更新支付记录状态为 SUCCESS
                payment.status = 'SUCCESS'
                payment.callback_data = json.dumps(extra_data or {})
                payment.save(update_fields=['status', 'callback_data', 'updated_at'])

                # 3b. 获取关联的订单
                order = payment.order

                # 3c. 更新订单状态为 PAID（使用乐观锁）
                #     为什么要加 status='PAYING' 条件？
                #     防止并发：如果订单状态已经被其他回调更新，则跳过
                #     只有状态为 PAYING 的订单才能被更新为 PAID
                affected = Order.objects.filter(
                    id=order.id,
                    status='PAYING'
                ).update(
                    status='PAID',
                    paid_at=timezone.now(),
                    updated_at=timezone.now()
                )
                # 如果 affected == 0，说明订单状态已不是 PAYING，可能已支付

                # 3d. 更新幂等表状态为 SUCCESS
                idem = IdempotentKey.objects.filter(order=order).first()
                if idem and idem.status != 'SUCCESS':
                    idem.status = 'SUCCESS'
                    idem.save(update_fields=['status'])

            else:
                # ============================================================
                # 分支 B：支付失败
                # ============================================================

                # 3e. 更新支付记录状态为 FAILED
                payment.status = 'FAILED'
                payment.callback_data = json.dumps(extra_data or {})
                payment.save(update_fields=['status', 'callback_data', 'updated_at'])

                # 3f. 幂等表设为 FAILED，允许用户重试
                order = payment.order
                idem = IdempotentKey.objects.filter(order=order).first()
                if idem:
                    idem.status = 'FAILED'
                    idem.save(update_fields=['status'])

                # 3g. 恢复 Redis 预扣库存（因为支付失败，库存要还回去）
                redis_client.incrby(f"stock:{order.product.id}", order.quantity)

                # 3h. 恢复数据库库存（使用乐观锁，直接更新）
                Product.objects.filter(id=order.product.id).update(
                    stock=F('stock') + order.quantity
                )

    except PaymentRecord.DoesNotExist:
        # 支付记录不存在，忽略（可能是支付记录还未创建）
        pass


# ============================================================================
# 第五部分：页面视图（渲染 HTML 页面）
# ============================================================================

def product_list(request):
    """
    功能：产品列表页面（前台商城首页）
    作用：渲染产品列表页面，供用户浏览和购买
    权限：需要登录
    """
    # 检查用户是否已登录（通过 session 中的 is_login 标志）
    if not request.session.get('is_login', None):
        return redirect('/login/')  # 未登录则跳转到登录页

    # 获取当前用户并检查是否有编辑权限（用于显示/隐藏管理按钮）
    account = request.session.get('account')
    can_edit = can_edit_product(account)

    # 渲染模板，传递 can_edit 变量给前端
    return render(request, 'sales/product_list.html', {
        'can_edit': can_edit,
    })

def product_detail(request, product_id):
    """产品详情页"""
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'sales/product_detail.html')


# ============================================================================
# 第六部分：商品管理 API
# ============================================================================

@csrf_exempt
def api_products(request):
    """
    功能：获取产品列表（支持搜索和分页）
    作用：为前端产品管理页面提供数据
    URL: GET /sales/api/products/
    参数：search (搜索关键词), page (页码), page_size (每页数量)
    返回：产品列表 JSON，包含封面图片和仓库库存
    """
    if request.method == 'GET':
        # ──────────────────────────────────────────────────────────────────────
        # 1. 获取查询参数
        # ──────────────────────────────────────────────────────────────────────
        search = request.GET.get('search', '').strip()
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        # ──────────────────────────────────────────────────────────────────────
        # 2. 构建查询集
        # ──────────────────────────────────────────────────────────────────────
        queryset = Product.objects.all()
        if search:
            # Q 对象实现 OR 查询：名称包含 或 描述包含
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(description__icontains=search)
            )

        # ──────────────────────────────────────────────────────────────────────
        # 3. 计算总数并分页
        # ──────────────────────────────────────────────────────────────────────
        total = queryset.count()
        products = queryset.order_by('-id')[(page - 1) * page_size:page * page_size]

        # ──────────────────────────────────────────────────────────────────────
        # 4. 构建返回数据（包含关联数据）
        # ──────────────────────────────────────────────────────────────────────
        product_list = []
        for p in products:
            # 4a. 获取封面图片（优先使用 is_cover=True 的图片）
            cover_image = None
            cover = p.images.filter(is_cover=True).first()
            if cover:
                cover_image = cover.image.url
            elif p.images.first():
                cover_image = p.images.first().image.url

            # 4b. 获取仓库库存信息
            warehouses = []
            for pw in p.warehouses.all():
                warehouses.append({
                    'warehouse_name': pw.warehouse.name,
                    'stock': pw.stock,
                })

            # 4c. 组装产品数据（包含所有前端需要的字段）
            product_list.append({
                'id': p.id,
                'product_code': p.product_code,
                'name': p.name,
                'price': str(p.price),
                'stock': p.stock,
                'version': p.version,  # 乐观锁版本号
                'description': p.description,
                'category': p.category,
                'brand': p.brand,
                'is_active': p.is_active,
                'cover_image': cover_image,
                'warehouses': warehouses,
                'created_at': p.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # ──────────────────────────────────────────────────────────────────────
        # 5. 返回 JSON 响应
        # ──────────────────────────────────────────────────────────────────────
        return JsonResponse({
            'products': product_list,
            'total': total,
            'page': page,
            'page_size': page_size
        })

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def api_product_detail(request, product_id):
    """
    功能：获取单个产品的详细信息
    作用：用于编辑产品时回填数据
    URL: GET /sales/api/product/<int:product_id>/
    """
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({
            'id': product.id,
            'name': product.name,
            'price': str(product.price),
            'stock': product.stock,
            'description': product.description,
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)


@csrf_exempt
def api_product_create(request):
    """
    功能：创建新产品
    作用：管理员新增产品
    权限：仅管理员
    URL: POST /sales/api/product/create/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. 权限检查
    # ──────────────────────────────────────────────────────────────────────────
    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        # ──────────────────────────────────────────────────────────────────────
        # 2. 解析请求数据
        # ──────────────────────────────────────────────────────────────────────
        data = json.loads(request.body)
        name = data.get('name', '').strip()
        price = data.get('price')
        stock = int(data.get('stock', 0))
        description = data.get('description', '').strip()

        # ──────────────────────────────────────────────────────────────────────
        # 3. 数据验证
        # ──────────────────────────────────────────────────────────────────────
        if not name:
            return JsonResponse({'error': '产品名称不能为空'}, status=400)
        if price is None or float(price) < 0:
            return JsonResponse({'error': '价格必须大于等于0'}, status=400)
        if stock < 0:
            return JsonResponse({'error': '库存不能为负数'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 4. 检查产品名称是否已存在
        # ──────────────────────────────────────────────────────────────────────
        if Product.objects.filter(name=name).exists():
            return JsonResponse({'error': '产品名称已存在'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 5. 创建产品
        # ──────────────────────────────────────────────────────────────────────
        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock,
            description=description
        )

        # ──────────────────────────────────────────────────────────────────────
        # 6. 同步库存到 Redis（用于后续的预扣减）
        #    键名格式：stock:{product_id}
        # ──────────────────────────────────────────────────────────────────────
        redis_client.set(f"stock:{product.id}", stock)

        # ──────────────────────────────────────────────────────────────────────
        # 7. 返回成功响应
        # ──────────────────────────────────────────────────────────────────────
        return JsonResponse({
            'success': True,
            'message': '产品创建成功',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'stock': product.stock,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_product_update(request, product_id):
    """
    功能：更新产品信息
    作用：管理员编辑产品
    权限：仅管理员
    URL: POST /sales/api/product/update/<int:product_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # 权限检查
    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        # 1. 获取要更新的产品
        product = Product.objects.get(id=product_id)
        data = json.loads(request.body)

        # 2. 提取并验证数据
        name = data.get('name', '').strip()
        price = data.get('price')
        stock = int(data.get('stock', 0))
        description = data.get('description', '').strip()

        if not name:
            return JsonResponse({'error': '产品名称不能为空'}, status=400)
        if price is None or float(price) < 0:
            return JsonResponse({'error': '价格必须大于等于0'}, status=400)
        if stock < 0:
            return JsonResponse({'error': '库存不能为负数'}, status=400)

        # 3. 检查名称是否已被其他产品使用
        if Product.objects.filter(name=name).exclude(id=product_id).exists():
            return JsonResponse({'error': '产品名称已存在'}, status=400)

        # 4. 更新产品
        product.name = name
        product.price = price
        product.stock = stock
        product.description = description
        product.save()

        # 5. 同步更新 Redis 库存
        redis_client.set(f"stock:{product.id}", stock)

        return JsonResponse({
            'success': True,
            'message': '产品更新成功',
            'product': {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'stock': product.stock,
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_product_delete(request, product_id):
    """
    功能：删除产品
    作用：管理员删除产品
    权限：仅管理员
    注意：如果产品已有订单记录，则不允许删除
    URL: POST /sales/api/product/delete/<int:product_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        product = Product.objects.get(id=product_id)

        # 检查是否有订单关联（防止删除有购买记录的产品）
        if Order.objects.filter(product=product).exists():
            return JsonResponse({'error': '该产品已有订单记录，无法删除'}, status=400)

        # 删除产品
        product.delete()

        # 清理 Redis 中的相关数据
        redis_client.delete(f"stock:{product_id}")
        redis_client.delete(f"lock:product:{product_id}")

        return JsonResponse({'success': True, 'message': '产品删除成功'})
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_sync_stock_to_redis(request):
    """
    功能：同步所有产品库存到 Redis
    作用：管理员工具，用于批量同步数据库库存到 Redis
    使用场景：Redis 数据丢失或初始化时
    URL: POST /sales/api/sync_stock/
    """
    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    # 遍历所有产品，将库存同步到 Redis
    products = Product.objects.all()
    for p in products:
        redis_client.set(f"stock:{p.id}", p.stock)

    return JsonResponse({
        'success': True,
        'message': f'已同步 {products.count()} 个产品库存到 Redis'
    })


@csrf_exempt
def api_products_for_purchase(request):
    """
    功能：获取可购买的产品列表
    作用：供前台商城使用，只返回有库存的产品
    URL: GET /sales/api/products/purchase/
    """
    # 只返回库存大于 0 的产品
    products = Product.objects.filter(stock__gt=0)

    result = []
    for p in products:
        # 获取封面图片
        cover_image = None
        cover = p.images.filter(is_cover=True).first()
        if cover:
            cover_image = cover.image.url
        elif p.images.first():
            cover_image = p.images.first().image.url

        result.append({
            'id': p.id,
            'name': p.name,
            'price': str(p.price),
            'stock': p.stock,
            'cover_image': cover_image,  # 添加封面图片
        })

    return JsonResponse(result, safe=False)


# ============================================================================
# 第七部分：订单 API（创建订单 + 支付）
# ============================================================================

@csrf_exempt
def api_create_order(request):
    """
    ════════════════════════════════════════════════════════════════════════════
    功能：创建订单并预扣库存
    作用：用户下单时，锁定库存并生成订单
    ════════════════════════════════════════════════════════════════════════════

    这是支付流程的第一步：
    1. 用户选择产品 → 发起下单请求
    2. 系统预扣库存（Redis）+ 扣减数据库库存（乐观锁）
    3. 生成订单（状态为 PENDING）
    4. 生成幂等键（用于后续支付时的幂等控制）
    5. 返回订单号和幂等键给前端

    为什么要预扣库存？
    ────────────────────────────────────────────────────────────────────────────
    - 防止超卖：用户下单后，库存被锁定，其他人无法购买
    - Redis 预扣是快速过滤，数据库乐观锁是最终保证

    分布式锁的作用：
    ────────────────────────────────────────────────────────────────────────────
    - 同一商品同时只能有一个订单在处理
    - 防止并发下单导致库存超卖
    - 使用 Redis 的 SETNX 实现
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        # ──────────────────────────────────────────────────────────────────────
        # 1. 解析请求数据
        # ──────────────────────────────────────────────────────────────────────
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        payment_method = data.get('payment_method')

        if not product_id or not payment_method:
            return JsonResponse({'error': '缺少必要参数'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 2. 获取当前用户
        # ──────────────────────────────────────────────────────────────────────
        account = request.session.get('account')
        user = get_current_user(account)
        if not user:
            return JsonResponse({'error': '用户未登录'}, status=401)

        # ──────────────────────────────────────────────────────────────────────
        # 3. 分布式锁（同一商品串行化处理）
        #    redis_client.lock 基于 SETNX 实现，确保同一商品同时只有一个订单在处理
        #    timeout=5：锁自动过期时间 5 秒，防止死锁
        #    blocking_timeout=3：等待锁的最长时间 3 秒
        # ──────────────────────────────────────────────────────────────────────
        lock_key = f"lock:product:{product_id}"
        with redis_client.lock(lock_key, timeout=5, blocking_timeout=3) as lock:
            if not lock.owned():
                return JsonResponse({'error': '系统繁忙，请稍后重试'}, status=429)

            # ──────────────────────────────────────────────────────────────────
            # 4. Redis 预扣库存（Lua 脚本原子操作）
            #    这是快速检查，如果 Redis 库存不足，直接返回
            #    不查询数据库，减少数据库压力
            # ──────────────────────────────────────────────────────────────────
            stock_key = f"stock:{product_id}"
            result = decr_stock(keys=[stock_key], args=[quantity])
            if result == 0:
                return JsonResponse({'error': '库存不足'}, status=400)

            # ──────────────────────────────────────────────────────────────────
            # 5. 数据库事务（真正扣减库存）
            #    使用 select_for_update() 加行锁，防止并发修改
            # ──────────────────────────────────────────────────────────────────
            with transaction.atomic():
                # 5a. 查询产品（加行锁）
                product = Product.objects.select_for_update().get(id=product_id)

                # 5b. 二次检查库存（数据库级别，确保一致性）
                if product.stock < quantity:
                    # 库存不足，回滚 Redis 预扣
                    redis_client.incrby(stock_key, quantity)
                    return JsonResponse({'error': '库存不足（并发）'}, status=400)

                # 5c. 乐观锁扣减库存
                #     使用 version 字段，WHERE 条件包含 version
                #     如果 version 不匹配，说明数据已被其他请求修改，更新失败
                affected = Product.objects.filter(
                    id=product_id,
                    version=product.version,  # 乐观锁版本号
                    stock__gte=quantity
                ).update(
                    stock=F('stock') - quantity,
                    version=F('version') + 1  # 版本号 +1
                )
                if affected == 0:
                    # 乐观锁失败，回滚 Redis
                    redis_client.incrby(stock_key, quantity)
                    return JsonResponse({'error': '库存变更冲突，请重试'}, status=409)

                # 5d. 计算订单金额并生成订单号
                #     格式：ORD + 年月日时分秒 + 8位随机字符串
                total = product.price * quantity
                order_no = f"ORD{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"

                # 5e. 创建订单（状态为 PENDING 待支付）
                # 关键修复：添加 seller=product.seller 确保外键不为空
                order = Order.objects.create(
                    order_no=order_no,
                    user=user,
                    product=product,
                    seller=product.seller,  # ⬅️ 从产品获取卖家，修复 seller_id 不能为空的问题
                    quantity=quantity,
                    total_amount=total,
                    payment_method=payment_method,
                    status='PENDING'
                )

                # 5f. 生成幂等键（用于支付时防止重复）
                #     格式：订单号_支付方式_随机字符串
                #     例如：ORD20260101120000_WECHAT_a1b2c3d4e5f6
                idempotent_key = f"{order_no}_{payment_method}_{uuid.uuid4().hex}"
                IdempotentKey.objects.create(
                    idempotent_key=idempotent_key,
                    order=order,
                    status='PROCESSING'  # 处理中
                )

            # ──────────────────────────────────────────────────────────────────
            # 6. 缓存幂等键响应（用于快速重复请求返回）
            #    如果用户重复点击支付，直接从 Redis 返回，不查询数据库
            # ──────────────────────────────────────────────────────────────────
            response_data = {
                'order_no': order_no,
                'idempotent_key': idempotent_key,
                'total_amount': str(total),
                'payment_method': payment_method,
            }
            cache_key = f"idempotent:{idempotent_key}"
            redis_client.setex(cache_key, 3600, json.dumps(response_data))  # 缓存1小时

            return JsonResponse(response_data)

    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)
    except Exception as e:
        # 异常时回滚 Redis 预扣库存
        if 'product_id' in locals():
            redis_client.incrby(f"stock:{product_id}", quantity)
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def api_pay(request):
    """
    ════════════════════════════════════════════════════════════════════════════
    功能：执行支付
    作用：用户确认支付，调用第三方支付平台
    ════════════════════════════════════════════════════════════════════════════

    支付流程：
    1. 前端携带 idempotent_key 请求支付
    2. 系统检查 Redis 缓存（快速幂等）
    3. 检查数据库幂等表（唯一索引保证）
    4. 更新订单状态为 PAYING
    5. 创建支付记录
    6. 调用第三方支付平台（微信/支付宝）
    7. 返回支付凭证给前端

    幂等性保证流程：
    ────────────────────────────────────────────────────────────────────────────
    第一次请求：
    1. Redis 缓存未命中
    2. 数据库幂等表未找到记录 → 创建记录（PROCESSING）
    3. 执行支付逻辑
    4. 成功后更新幂等表为 SUCCESS，并缓存

    重复请求（网络重试）：
    1. Redis 缓存命中 → 直接返回成功（无需查询数据库）

    重复请求（缓存过期）：
    1. Redis 缓存未命中
    2. 数据库幂等表找到记录，状态为 SUCCESS → 重新缓存并返回
    3. 不会重复执行业务逻辑
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        idempotent_key = data.get('idempotent_key')
        if not idempotent_key:
            return JsonResponse({'error': '缺少幂等键'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 第一层防护：Redis 幂等缓存
        # 如果缓存中有结果，直接返回，不查询数据库
        # 这是最快的幂等检查
        # ──────────────────────────────────────────────────────────────────────
        cache_key = f"idempotent:{idempotent_key}"
        cached = redis_client.get(cache_key)
        if cached:
            resp = json.loads(cached)
            return JsonResponse({
                'status': 'success',
                'order_no': resp.get('order_no'),
                'message': '订单已处理（缓存）',
                'paid': True
            })

        # ──────────────────────────────────────────────────────────────────────
        # 第二层防护：数据库幂等表
        # IdempotentKey.idempotent_key 字段有 unique=True（唯一索引）
        # 这是最终的幂等保证
        # ──────────────────────────────────────────────────────────────────────
        try:
            idem = IdempotentKey.objects.get(idempotent_key=idempotent_key)
        except IdempotentKey.DoesNotExist:
            return JsonResponse({'error': '无效的幂等键'}, status=404)

        # ──────────────────────────────────────────────────────────────────────
        # 如果已成功，缓存结果并返回
        # ──────────────────────────────────────────────────────────────────────
        if idem.status == 'SUCCESS':
            redis_client.setex(cache_key, 3600, json.dumps({
                'order_no': idem.order.order_no,
                'paid_at': idem.order.paid_at.strftime('%Y-%m-%d %H:%M:%S') if idem.order.paid_at else None
            }))
            return JsonResponse({
                'status': 'success',
                'order_no': idem.order.order_no,
                'paid': True,
                'paid_at': idem.order.paid_at.strftime('%Y-%m-%d %H:%M:%S') if idem.order.paid_at else None,
            })

        # ──────────────────────────────────────────────────────────────────────
        # 如果正在处理中，检查订单状态
        # ──────────────────────────────────────────────────────────────────────
        if idem.status == 'PROCESSING':
            if idem.order.status == 'PAID':
                # 订单已支付，但幂等表未更新 → 修复数据一致性
                idem.status = 'SUCCESS'
                idem.save(update_fields=['status'])
                redis_client.setex(cache_key, 3600, json.dumps({'order_no': idem.order.order_no}))
                return JsonResponse({'status': 'success', 'message': '订单已支付'})
            # 正在处理中，让前端稍后查询
            return JsonResponse({'status': 'processing', 'message': '支付处理中，请稍后查询'})

        # ──────────────────────────────────────────────────────────────────────
        # 如果状态为 FAILED，允许重试（重置为 PROCESSING）
        # ──────────────────────────────────────────────────────────────────────
        if idem.status == 'FAILED':
            idem.status = 'PROCESSING'
            idem.save(update_fields=['status'])

        # ──────────────────────────────────────────────────────────────────────
        # 第三层防护：状态机乐观锁
        # 只有 PENDING 或 PAYING 状态的订单才能支付
        # ──────────────────────────────────────────────────────────────────────
        order = idem.order
        if order.status not in ['PENDING', 'PAYING']:
            return JsonResponse({'error': '订单状态不允许支付'}, status=400)

        with transaction.atomic():
            # 乐观锁：更新订单状态为 PAYING
            # 仅当状态为 PENDING 或 PAYING 时才更新
            # 如果 affected == 0，说明状态已被其他请求改变
            affected = Order.objects.filter(
                id=order.id,
                status__in=['PENDING', 'PAYING']
            ).update(
                status='PAYING',
                updated_at=timezone.now()
            )
            if affected == 0:
                return JsonResponse({'error': '订单状态已变更，请刷新'}, status=409)

            # 创建支付记录
            payment_no = f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
            payment = PaymentRecord.objects.create(
                payment_no=payment_no,
                order=order,
                payment_method=order.payment_method,
                amount=order.total_amount,
                status='PROCESSING'
            )

        # ──────────────────────────────────────────────────────────────────────
        # 模拟异步回调成功（实际生产中，这里应该调用第三方支付接口）
        # 支付平台会异步回调 api_payment_callback
        # 这里为了演示，直接模拟成功回调
        # ──────────────────────────────────────────────────────────────────────
        _process_payment_callback(payment_no, success=True, extra_data={'simulate': True})

        # 缓存结果
        redis_client.setex(cache_key, 3600, json.dumps({'order_no': order.order_no}))

        return JsonResponse({
            'status': 'success',
            'payment_no': payment_no,
            'message': '支付成功',
            'order_no': order.order_no,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_callback(request):
    """
    功能：第三方支付异步回调接口（已废弃，保留用于兼容）
    实际使用 api_payment_callback
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    try:
        data = json.loads(request.body)
        payment_no = data.get('payment_no')
        success = data.get('success', False)
        extra = data.get('extra', {})
        if not payment_no:
            return JsonResponse({'error': '缺少支付单号'}, status=400)

        _process_payment_callback(payment_no, success, extra)
        return JsonResponse({'code': 'SUCCESS'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def api_order_status(request, order_no):
    """
    功能：查询订单状态
    作用：供前端轮询查询支付结果
    URL: GET /sales/api/order_status/<str:order_no>/
    """
    try:
        order = Order.objects.get(order_no=order_no)
        data = {
            'order_no': order.order_no,
            'status': order.status,
            'total_amount': str(order.total_amount),
            'paid_at': order.paid_at.strftime('%Y-%m-%d %H:%M:%S') if order.paid_at else None,
        }
        return JsonResponse(data)
    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)


# ============================================================================
# 第八部分：产品图片 API
# ============================================================================

@csrf_exempt
def api_product_images(request, product_id):
    """
    功能：获取产品图片列表
    作用：在图片管理弹窗中显示所有图片
    URL: GET /sales/api/product/<int:product_id>/images/
    """
    try:
        product = Product.objects.get(id=product_id)
        # 按封面优先、排序字段排序
        images = product.images.all().order_by('-is_cover', 'sort_order')

        result = []
        for img in images:
            result.append({
                'id': img.id,
                'image': img.image.url,  # 图片 URL，如 /media/product_images/xxx.png
                'is_cover': img.is_cover,
                'sort_order': img.sort_order,
                'description': img.description,
                'created_at': img.created_at.strftime('%Y-%m-%d %H:%M:%S') if img.created_at else None
            })
        return JsonResponse(result, safe=False)
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)


@csrf_exempt
def api_product_image_upload(request):
    """
    功能：上传产品图片
    作用：管理员为产品添加图片
    权限：仅管理员
    URL: POST /sales/api/product/image/upload/

    请求参数：
    - product_id: 产品ID
    - image: 图片文件
    - is_cover: 是否设为封面 (true/false)
    - description: 图片描述
    - sort_order: 排序
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        # ──────────────────────────────────────────────────────────────────────
        # 1. 获取参数
        # ──────────────────────────────────────────────────────────────────────
        product_id = request.POST.get('product_id')
        image_file = request.FILES.get('image')
        is_cover = request.POST.get('is_cover', 'false') == 'true'

        if not product_id:
            return JsonResponse({'error': '缺少 product_id 参数'}, status=400)

        if not image_file:
            return JsonResponse({'error': '请选择要上传的图片'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 2. 文件验证
        # ──────────────────────────────────────────────────────────────────────
        # 检查文件类型
        if not image_file.content_type.startswith('image/'):
            return JsonResponse({'error': '只支持图片文件'}, status=400)

        # 检查文件大小（限制 5MB）
        if image_file.size > 5 * 1024 * 1024:
            return JsonResponse({'error': '图片大小不能超过 5MB'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 3. 创建图片记录
        # ──────────────────────────────────────────────────────────────────────
        product = Product.objects.get(id=product_id)

        # 如果设为封面，取消其他封面
        if is_cover:
            ProductImage.objects.filter(product=product, is_cover=True).update(is_cover=False)

        # 创建图片记录（Django 会自动保存文件到 MEDIA_ROOT）
        image = ProductImage.objects.create(
            product=product,
            image=image_file,
            is_cover=is_cover,
            sort_order=int(request.POST.get('sort_order', 0)),
            description=request.POST.get('description', '')
        )

        # ──────────────────────────────────────────────────────────────────────
        # 4. 返回成功响应
        # ──────────────────────────────────────────────────────────────────────
        return JsonResponse({
            'success': True,
            'message': '图片上传成功',
            'image': {
                'id': image.id,
                'url': image.image.url,  # Django 会自动生成完整 URL
                'is_cover': image.is_cover,
                'sort_order': image.sort_order,
                'description': image.description,
            }
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)
    except Exception as e:
        logger.error(f"图片上传失败: {str(e)}", exc_info=True)
        return JsonResponse({'error': f'上传失败: {str(e)}'}, status=500)


@csrf_exempt
def api_product_image_delete(request, image_id):
    """
    功能：删除产品图片
    作用：管理员删除不需要的图片
    权限：仅管理员
    URL: POST /sales/api/product/image/delete/<int:image_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        image = ProductImage.objects.get(id=image_id)

        # 删除图片文件（从磁盘上删除）
        if image.image:
            image.image.delete(save=False)  # save=False 表示不保存模型

        # 删除数据库记录
        image.delete()

        return JsonResponse({'success': True, 'message': '图片删除成功'})
    except ProductImage.DoesNotExist:
        return JsonResponse({'error': '图片不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_product_image_set_cover(request, image_id):
    """
    功能：设置图片为封面
    作用：管理员将某张图片设为产品封面
    权限：仅管理员
    URL: POST /sales/api/product/image/set_cover/<int:image_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        image = ProductImage.objects.get(id=image_id)
        product = image.product

        # 取消所有封面
        ProductImage.objects.filter(product=product, is_cover=True).update(is_cover=False)

        # 设置当前图片为封面
        image.is_cover = True
        image.save()

        return JsonResponse({'success': True, 'message': '设置封面成功'})
    except ProductImage.DoesNotExist:
        return JsonResponse({'error': '图片不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# 第九部分：仓库 API
# ============================================================================

@csrf_exempt
def api_warehouses(request):
    """
    功能：获取仓库列表
    作用：返回所有启用的仓库，用于下拉选择
    URL: GET /sales/api/warehouses/
    """
    try:
        warehouses = Warehouse.objects.filter(is_active=True).values(
            'id', 'warehouse_code', 'name', 'address', 'region', 'is_active', 'contact_person', 'contact_phone'
        )
        warehouse_list = list(warehouses)
        return JsonResponse({
            'results': warehouse_list,
            'total': len(warehouse_list)
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            'results': [],
            'total': 0,
            'error': str(e)
        }, status=500)


@csrf_exempt
def api_warehouse_create(request):
    """
    功能：创建仓库
    作用：管理员新增仓库
    权限：仅管理员
    URL: POST /sales/api/warehouse/create/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        data = json.loads(request.body)
        warehouse = Warehouse.objects.create(
            warehouse_code=data.get('warehouse_code'),
            name=data.get('name'),
            address=data.get('address'),
            region=data.get('region'),
            contact_person=data.get('contact_person', ''),
            contact_phone=data.get('contact_phone', ''),
        )
        return JsonResponse({
            'success': True,
            'message': '仓库创建成功',
            'warehouse': {
                'id': warehouse.id,
                'warehouse_code': warehouse.warehouse_code,
                'name': warehouse.name,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_warehouse_update(request, warehouse_id):
    """
    功能：更新仓库信息
    作用：管理员编辑仓库
    权限：仅管理员
    URL: POST /sales/api/warehouse/update/<int:warehouse_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
        data = json.loads(request.body)

        warehouse.warehouse_code = data.get('warehouse_code', warehouse.warehouse_code)
        warehouse.name = data.get('name', warehouse.name)
        warehouse.address = data.get('address', warehouse.address)
        warehouse.region = data.get('region', warehouse.region)
        warehouse.contact_person = data.get('contact_person', warehouse.contact_person)
        warehouse.contact_phone = data.get('contact_phone', warehouse.contact_phone)
        warehouse.save()

        return JsonResponse({'success': True, 'message': '仓库更新成功'})
    except Warehouse.DoesNotExist:
        return JsonResponse({'error': '仓库不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_warehouse_delete(request, warehouse_id):
    """
    功能：删除仓库
    作用：管理员删除仓库
    权限：仅管理员
    注意：如果仓库下还有产品库存，不允许删除
    URL: POST /sales/api/warehouse/delete/<int:warehouse_id>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)

        # 检查是否有产品库存
        if ProductWarehouse.objects.filter(warehouse=warehouse).exists():
            return JsonResponse({'error': '该仓库下还有产品库存，无法删除'}, status=400)

        warehouse.delete()
        return JsonResponse({'success': True, 'message': '仓库删除成功'})
    except Warehouse.DoesNotExist:
        return JsonResponse({'error': '仓库不存在'}, status=404)


@csrf_exempt
def api_warehouse_products(request, warehouse_id):
    """
    功能：获取仓库下的产品库存
    作用：查看某个仓库中所有产品的库存情况
    URL: GET /sales/api/warehouse/<int:warehouse_id>/products/
    """
    try:
        warehouse = Warehouse.objects.get(id=warehouse_id)
        products = ProductWarehouse.objects.filter(warehouse=warehouse).select_related('product')
        data = [{
            'product_id': pw.product.id,
            'product_code': pw.product.product_code,
            'product_name': pw.product.name,
            'stock': pw.stock,
            'reserved_stock': pw.reserved_stock,
            'min_stock': pw.min_stock,
            'max_stock': pw.max_stock,
        } for pw in products]
        return JsonResponse(data, safe=False)
    except Warehouse.DoesNotExist:
        return JsonResponse({'error': '仓库不存在'}, status=404)


@csrf_exempt
def api_warehouse_product_update(request):
    """
    功能：更新仓库产品库存
    作用：管理员调整某个仓库中某个产品的库存
    权限：仅管理员
    URL: POST /sales/api/warehouse/product/update/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        warehouse_id = data.get('warehouse_id')
        stock = data.get('stock', 0)
        min_stock = data.get('min_stock', 0)
        max_stock = data.get('max_stock', 0)

        # get_or_create：如果不存在则创建，存在则更新
        pw, created = ProductWarehouse.objects.get_or_create(
            product_id=product_id,
            warehouse_id=warehouse_id,
            defaults={
                'stock': stock,
                'min_stock': min_stock,
                'max_stock': max_stock,
            }
        )
        if not created:
            pw.stock = stock
            pw.min_stock = min_stock
            pw.max_stock = max_stock
            pw.save()

        return JsonResponse({
            'success': True,
            'message': '库存更新成功',
            'stock': pw.stock,
            'reserved_stock': pw.reserved_stock,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# 第十部分：订单物流 API
# ============================================================================

@csrf_exempt
def api_order_logistics(request, order_no):
    """
    功能：获取订单物流追踪信息
    作用：查看订单的物流轨迹
    URL: GET /sales/api/order/<str:order_no>/logistics/
    """
    try:
        order = Order.objects.get(order_no=order_no)
        tracks = order.logistics_tracks.all().values(
            'logistics_company', 'logistics_no', 'status', 'content', 'location', 'track_time'
        )
        return JsonResponse({
            'order_no': order.order_no,
            'logistics_company': order.logistics_company,
            'logistics_no': order.logistics_no,
            'logistics_status': order.logistics_status,
            'tracks': list(tracks)
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)


@csrf_exempt
def api_update_logistics(request, order_no):
    """
    功能：更新物流信息
    作用：管理员发货时填写物流公司和物流单号
    权限：仅管理员
    URL: POST /sales/api/order/<str:order_no>/update_logistics/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        order = Order.objects.get(order_no=order_no)
        data = json.loads(request.body)

        logistics_company = data.get('logistics_company')
        logistics_no = data.get('logistics_no')

        if logistics_company and logistics_no:
            # 更新订单物流信息
            order.logistics_company = logistics_company
            order.logistics_no = logistics_no
            order.logistics_status = '已发货'
            order.shipped_at = timezone.now()
            order.status = 'SHIPPED'  # 状态变更为已发货
            order.save()

            # 创建物流追踪记录
            OrderLogistics.objects.create(
                order=order,
                logistics_company=logistics_company,
                logistics_no=logistics_no,
                status='已发货',
                content='商品已发货，等待物流揽收',
                track_time=timezone.now()
            )

            return JsonResponse({'success': True, 'message': '物流信息更新成功'})
        else:
            return JsonResponse({'error': '物流公司和物流单号不能为空'}, status=400)

    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_orders_list(request):
    """
    功能：获取订单列表（管理员）
    作用：管理员查看和管理所有订单
    权限：仅管理员
    URL: GET /sales/api/orders/
    参数：status (状态筛选), search (搜索), page, page_size
    """
    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    # 获取查询参数
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '').strip()
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 20))

    # 构建查询集
    queryset = Order.objects.all().select_related('user', 'product')

    if status_filter:
        queryset = queryset.filter(status=status_filter)

    if search:
        queryset = queryset.filter(
            Q(order_no__icontains=search) |
            Q(user__username__icontains=search) |
            Q(product__name__icontains=search) |
            Q(receiver_name__icontains=search) |
            Q(receiver_phone__icontains=search)
        )

    # 分页
    total = queryset.count()
    orders = queryset.order_by('-created_at')[(page - 1) * page_size:page * page_size]

    # 构建返回数据
    data = [{
        'id': o.id,
        'order_no': o.order_no,
        'user_name': o.user.username if o.user else '已删除',
        'product_name': o.product.name,
        'quantity': o.quantity,
        'total_amount': str(o.total_amount),
        'payment_method': o.get_payment_method_display(),
        'status': o.status,
        'status_display': o.get_status_display(),
        'receiver_name': o.receiver_name,
        'receiver_phone': o.receiver_phone,
        'receiver_address': o.receiver_address,
        'logistics_company': o.logistics_company,
        'logistics_no': o.logistics_no,
        'logistics_status': o.logistics_status,
        'created_at': o.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'paid_at': o.paid_at.strftime('%Y-%m-%d %H:%M:%S') if o.paid_at else None,
        'shipped_at': o.shipped_at.strftime('%Y-%m-%d %H:%M:%S') if o.shipped_at else None,
        'delivered_at': o.delivered_at.strftime('%Y-%m-%d %H:%M:%S') if o.delivered_at else None,
    } for o in orders]

    return JsonResponse({
        'orders': data,
        'total': total,
        'page': page,
        'page_size': page_size,
    })


@csrf_exempt
def api_order_update_status(request, order_no):
    """
    功能：更新订单状态（管理员）
    作用：管理员手动修改订单状态（如发货、完成等）
    权限：仅管理员
    URL: POST /sales/api/order/update_status/<str:order_no>/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        order = Order.objects.get(order_no=order_no)
        data = json.loads(request.body)
        new_status = data.get('status')

        # 验证状态是否合法
        if new_status not in dict(Order.STATUS_CHOICES):
            return JsonResponse({'error': '无效的状态'}, status=400)

        # 状态流转时自动记录时间
        if new_status == 'SHIPPED':
            order.shipped_at = timezone.now()
        elif new_status == 'DELIVERED':
            order.delivered_at = timezone.now()
        elif new_status == 'CANCELLED':
            order.cancelled_at = timezone.now()

        order.status = new_status
        order.save()

        return JsonResponse({
            'success': True,
            'message': '订单状态更新成功',
            'new_status': new_status,
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ============================================================================
# 第十一部分：评价 API
# ============================================================================

@csrf_exempt
def api_product_reviews(request, product_id):
    """
    功能：获取产品评价列表
    作用：展示产品的用户评价
    URL: GET /sales/api/product/<int:product_id>/reviews/
    参数：page, page_size
    返回：评价列表、总数、平均评分
    """
    try:
        product = Product.objects.get(id=product_id)
        # 只返回已审核的评价
        reviews = product.reviews.filter(is_approved=True).select_related('user')

        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))

        total = reviews.count()
        reviews_list = reviews.order_by('-created_at')[(page - 1) * page_size:page * page_size]

        data = [{
            'id': r.id,
            'user_name': '匿名用户' if r.is_anonymous else (r.user.username if r.user else '已删除'),
            'rating': r.rating,
            'title': r.title,
            'content': r.content,
            'advantages': r.advantages,
            'disadvantages': r.disadvantages,
            'is_recommend': r.is_recommend,
            'images': [{'id': img.id, 'image': img.image.url} for img in r.images.all()],
            'created_at': r.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        } for r in reviews_list]

        # 计算平均评分
        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

        return JsonResponse({
            'reviews': data,
            'total': total,
            'page': page,
            'page_size': page_size,
            'avg_rating': round(avg_rating, 1) if avg_rating else 0,
            'total_count': total,
        })
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)


@csrf_exempt
def api_review_create(request):
    """
    功能：创建用户评价
    作用：用户购买后对产品进行评价
    权限：需要登录
    URL: POST /sales/api/review/create/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    try:
        data = json.loads(request.body)
        order_no = data.get('order_no')
        product_id = data.get('product_id')
        rating = data.get('rating')
        content = data.get('content')

        if not all([order_no, product_id, rating, content]):
            return JsonResponse({'error': '缺少必要参数'}, status=400)

        # 验证订单是否属于当前用户
        order = Order.objects.get(order_no=order_no, user=user)
        product = Product.objects.get(id=product_id)

        # 检查是否已评价（防止重复评价）
        if ProductReview.objects.filter(order=order, product=product).exists():
            return JsonResponse({'error': '该订单已评价'}, status=400)

        # 创建评价
        review = ProductReview.objects.create(
            order=order,
            product=product,
            user=user,
            rating=rating,
            title=data.get('title', ''),
            content=content,
            advantages=data.get('advantages', ''),
            disadvantages=data.get('disadvantages', ''),
            is_anonymous=data.get('is_anonymous', False),
            is_approved=data.get('is_approved', True),  # 默认审核通过
        )

        return JsonResponse({
            'success': True,
            'message': '评价成功',
            'review_id': review.id
        })

    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在或不属于该用户'}, status=404)
    except Product.DoesNotExist:
        return JsonResponse({'error': '产品不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_review_like(request, review_id):
    """
    功能：点赞/取消点赞评价
    作用：用户对评价进行点赞（简化实现）
    URL: POST /sales/api/review/<int:review_id>/like/
    """
    # 简化实现，完整功能需要创建 Like 模型
    return JsonResponse({'success': True, 'message': '点赞成功'})


@csrf_exempt
def api_review_images(request, review_id):
    """
    功能：获取评价图片
    作用：查看评价中附带的图片
    URL: GET /sales/api/review/<int:review_id>/images/
    """
    try:
        review = ProductReview.objects.get(id=review_id)
        images = review.images.all().values('id', 'image', 'sort_order')
        return JsonResponse(list(images), safe=False)
    except ProductReview.DoesNotExist:
        return JsonResponse({'error': '评价不存在'}, status=404)


@csrf_exempt
def api_review_approve(request, review_id):
    """
    功能：审核评价（管理员）
    作用：管理员审核用户评价，通过后前台可见
    权限：仅管理员
    URL: POST /sales/api/review/<int:review_id>/approve/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        review = ProductReview.objects.get(id=review_id)
        data = json.loads(request.body)
        is_approved = data.get('is_approved', True)

        review.is_approved = is_approved
        review.save()

        return JsonResponse({
            'success': True,
            'message': f'评价已{"通过" if is_approved else "拒绝"}审核',
        })
    except ProductReview.DoesNotExist:
        return JsonResponse({'error': '评价不存在'}, status=404)


@csrf_exempt
def api_review_delete(request, review_id):
    """
    功能：删除评价（管理员）
    作用：管理员删除不当评价
    权限：仅管理员
    URL: POST /sales/api/review/<int:review_id>/delete/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        review = ProductReview.objects.get(id=review_id)
        review.delete()
        return JsonResponse({'success': True, 'message': '评价删除成功'})
    except ProductReview.DoesNotExist:
        return JsonResponse({'error': '评价不存在'}, status=404)


# ============================================================================
# 第十二部分：用户反馈 API
# ============================================================================

@csrf_exempt
def api_feedback_create(request):
    """
    功能：创建用户反馈
    作用：用户提交投诉、建议、咨询等
    权限：需要登录
    URL: POST /sales/api/feedback/create/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    try:
        data = json.loads(request.body)

        feedback = UserFeedback.objects.create(
            user=user,
            order_id=data.get('order_id'),
            product_id=data.get('product_id'),
            feedback_type=data.get('feedback_type', 'OTHER'),
            title=data.get('title'),
            content=data.get('content'),
            images=json.dumps(data.get('images', [])),  # 存储为 JSON 字符串
        )

        return JsonResponse({
            'success': True,
            'message': '反馈提交成功',
            'feedback_id': feedback.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_feedback_list(request):
    """
    功能：获取用户反馈列表
    作用：用户查看自己的反馈记录
    权限：需要登录
    URL: GET /sales/api/feedback/list/
    """
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    feedbacks = UserFeedback.objects.filter(user=user).order_by('-created_at')
    data = [{
        'id': f.id,
        'feedback_type': f.get_feedback_type_display(),
        'title': f.title,
        'content': f.content[:100],  # 只显示前100字符
        'status': f.get_status_display(),
        'created_at': f.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for f in feedbacks]

    return JsonResponse(data, safe=False)


@csrf_exempt
def api_feedback_detail(request, feedback_id):
    """
    功能：获取反馈详情
    作用：用户查看单个反馈的完整信息
    权限：需要登录，且只能查看自己的反馈
    URL: GET /sales/api/feedback/<int:feedback_id>/
    """
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    try:
        feedback = UserFeedback.objects.get(id=feedback_id, user=user)
        return JsonResponse({
            'id': feedback.id,
            'feedback_type': feedback.get_feedback_type_display(),
            'title': feedback.title,
            'content': feedback.content,
            'status': feedback.get_status_display(),
            'images': json.loads(feedback.images) if feedback.images else [],
            'handle_content': feedback.handle_content,
            'handled_at': feedback.handled_at.strftime('%Y-%m-%d %H:%M:%S') if feedback.handled_at else None,
            'created_at': feedback.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })
    except UserFeedback.DoesNotExist:
        return JsonResponse({'error': '反馈不存在'}, status=404)


@csrf_exempt
def api_feedback_handle(request, feedback_id):
    """
    功能：处理反馈（管理员）
    作用：管理员回复处理用户反馈
    权限：仅管理员
    URL: POST /sales/api/feedback/<int:feedback_id>/handle/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        feedback = UserFeedback.objects.get(id=feedback_id)
        data = json.loads(request.body)

        handler = get_current_user(account)
        feedback.handler = handler
        feedback.handle_content = data.get('handle_content', '')
        feedback.status = data.get('status', 'RESOLVED')
        feedback.handled_at = timezone.now()
        feedback.save()

        return JsonResponse({
            'success': True,
            'message': '反馈处理成功',
        })
    except UserFeedback.DoesNotExist:
        return JsonResponse({'error': '反馈不存在'}, status=404)


# ============================================================================
# 第十三部分：管理员页面视图（渲染后台管理页面）
# ============================================================================

def admin_dashboard(request):
    """
    功能：管理员后台首页
    作用：显示管理后台仪表板
    权限：仅管理员
    URL: GET /sales/admin/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_dashboard.html', {
        'can_edit': True,
    })


def admin_products(request):
    """
    功能：管理员产品管理页面
    作用：展示产品列表和管理界面
    权限：仅管理员
    URL: GET /sales/admin/products/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_products.html', {
        'can_edit': True,
    })


def admin_warehouses(request):
    """
    功能：管理员仓库管理页面
    作用：展示仓库列表和管理界面
    权限：仅管理员
    URL: GET /sales/admin/warehouses/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_warehouses.html', {
        'can_edit': True,
    })


def admin_orders(request):
    """
    功能：管理员订单管理页面
    作用：展示订单列表和管理界面
    权限：仅管理员
    URL: GET /sales/admin/orders/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_orders.html', {
        'can_edit': True,
    })


def admin_reviews(request):
    """
    功能：管理员评价管理页面
    作用：展示评价列表和审核界面
    权限：仅管理员
    URL: GET /sales/admin/reviews/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_reviews.html', {
        'can_edit': True,
    })


def admin_feedbacks(request):
    """
    功能：管理员反馈管理页面
    作用：展示反馈列表和处理界面
    权限：仅管理员
    URL: GET /sales/admin/feedbacks/
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    if not can_edit_product(account):
        return redirect('/sales/')

    return render(request, 'sales/admin_feedbacks.html', {
        'can_edit': True,
    })


# ============================================================================
# 第十四部分：支付相关视图（调用第三方支付）
# ============================================================================

@csrf_exempt
def api_create_payment(request):
    """
    功能：创建支付订单 - 调用第三方支付
    作用：用户发起支付请求，调用微信/支付宝的统一下单接口
    权限：需要登录
    URL: POST /sales/api/create_payment/

    工作流程：
    1. 用户选择支付方式（微信/支付宝/银行卡）
    2. 系统根据卖家的支付配置获取对应的支付提供者
    3. 调用支付平台的统一下单接口
    4. 获取支付凭证（支付链接、二维码等）
    5. 返回给前端，引导用户完成支付
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # ──────────────────────────────────────────────────────────────────────
        # 1. 解析请求参数
        # ──────────────────────────────────────────────────────────────────────
        data = json.loads(request.body)
        order_no = data.get('order_no')
        payment_method = data.get('payment_method', 'WECHAT')

        if not order_no:
            return JsonResponse({'error': '缺少订单号'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 2. 获取订单并验证
        # ──────────────────────────────────────────────────────────────────────
        order = Order.objects.get(order_no=order_no, user=get_current_user(request.session.get('account')))

        # 只有待支付的订单才能发起支付
        if order.status != 'PENDING':
            return JsonResponse({'error': f'订单状态不允许支付: {order.status}'}, status=400)

        # ──────────────────────────────────────────────────────────────────────
        # 3. 获取卖家的支付配置
        # ──────────────────────────────────────────────────────────────────────
        seller = order.seller
        if not seller:
            return JsonResponse({'error': '卖家不存在'}, status=404)

        # ──────────────────────────────────────────────────────────────────────
        # 4. 获取支付提供者（微信/支付宝/银行）
        #    get_payment_provider 根据 seller.payment_provider 返回对应的提供者
        # ──────────────────────────────────────────────────────────────────────
        provider = get_payment_provider(seller)

        # ──────────────────────────────────────────────────────────────────────
        # 5. 构建回调 URL
        #    支付平台支付成功后，会异步通知这个 URL
        # ──────────────────────────────────────────────────────────────────────
        notify_url = f"{request.build_absolute_uri('/')}sales/api/payment_callback/"
        return_url = f"{request.build_absolute_uri('/')}sales/payment_result/"

        # ──────────────────────────────────────────────────────────────────────
        # 6. 调用支付平台创建订单
        # ──────────────────────────────────────────────────────────────────────
        result = provider.create_order(
            order_no=order_no,
            amount=str(order.total_amount),
            subject=order.product.name,
            description=order.product.description or '商品支付',
            notify_url=notify_url,
            return_url=return_url
        )

        if not result.get('success'):
            return JsonResponse({'error': result.get('error', '支付创建失败')}, status=500)

        # ──────────────────────────────────────────────────────────────────────
        # 7. 创建支付记录
        # ──────────────────────────────────────────────────────────────────────
        payment_no = f"PAY{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:8].upper()}"
        payment = PaymentRecord.objects.create(
            payment_no=payment_no,
            order=order,
            seller=seller,
            payment_method=payment_method,
            amount=order.total_amount,
            status='PROCESSING',
            callback_data=json.dumps(result)
        )

        # ──────────────────────────────────────────────────────────────────────
        # 8. 更新订单状态为支付中
        # ──────────────────────────────────────────────────────────────────────
        order.status = 'PAYING'
        order.save(update_fields=['status', 'updated_at'])

        # ──────────────────────────────────────────────────────────────────────
        # 9. 根据支付方式返回不同的响应
        # ──────────────────────────────────────────────────────────────────────
        response_data = {
            'success': True,
            'payment_no': payment_no,
            'order_no': order_no,
            'total_amount': str(order.total_amount),
        }

        if payment_method == 'WECHAT':
            # 微信支付：返回二维码链接或 JSAPI 参数
            response_data['pay_url'] = result.get('pay_url')
            response_data['prepay_id'] = result.get('prepay_id')
            response_data['payment_type'] = 'wechat_qr'
        elif payment_method == 'ALIPAY':
            # 支付宝：返回跳转链接
            response_data['pay_url'] = result.get('pay_url')
            response_data['payment_type'] = 'alipay_redirect'
        elif payment_method == 'BANK':
            # 银行转账：返回银行账户信息
            response_data['bank_info'] = result.get('bank_info')
            response_data['payment_type'] = 'bank_transfer'

        return JsonResponse(response_data)

    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)
    except Exception as e:
        logger.error(f"创建支付失败: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_payment_callback(request):
    """
    ════════════════════════════════════════════════════════════════════════════
    功能：第三方支付异步回调 - 最重要的接口
    作用：接收支付平台的异步通知，验证并更新订单状态
    ════════════════════════════════════════════════════════════════════════════

    这是整个支付系统最关键的接口！

    为什么必须支持幂等？
    ────────────────────────────────────────────────────────────────────────────
    1. 支付平台可能因网络问题重复发送回调
    2. 你的系统可能处理超时，支付平台重试
    3. 重复回调会导致重复发货、重复扣库存

    本接口的幂等实现：
    ────────────────────────────────────────────────────────────────────────────
    1. 使用 transaction_id（支付平台交易号）作为幂等键
    2. IdempotentKey 表 unique=True 保证唯一
    3. 如果已处理，直接返回成功

    安全措施：
    ────────────────────────────────────────────────────────────────────────────
    1. 签名验证：确保请求来自支付平台（防止伪造）
    2. 金额验证：防止篡改订单金额
    3. 状态检查：防止重复处理
    """
    if request.method not in ['POST', 'GET']:
        return HttpResponse('Method not allowed', status=405)

    try:
        # ──────────────────────────────────────────────────────────────────────
        # 1. 获取原始请求数据
        #    微信使用 XML 格式，支付宝使用 JSON 格式
        # ──────────────────────────────────────────────────────────────────────
        if request.method == 'POST':
            raw_data = request.body
            try:
                data = json.loads(raw_data)  # 支付宝格式
            except:
                # 微信格式：XML
                import xml.etree.ElementTree as ET
                root = ET.fromstring(raw_data)
                data = {}
                for child in root:
                    data[child.tag] = child.text
        else:
            data = request.GET.dict()

        # ──────────────────────────────────────────────────────────────────────
        # 2. 提取关键参数
        # ──────────────────────────────────────────────────────────────────────
        order_no = data.get('out_trade_no') or data.get('order_no')
        transaction_id = data.get('transaction_id') or data.get('trade_no')
        total_amount = data.get('total_amount') or data.get('total_fee')

        if not order_no:
            logger.warning("回调缺少订单号")
            return HttpResponse('fail')

        # ──────────────────────────────────────────────────────────────────────
        # 3. 幂等性检查（第一层）
        #    使用 transaction_id 作为幂等键
        # ──────────────────────────────────────────────────────────────────────
        if transaction_id:
            idempotent_key = f"pay_callback_{transaction_id}"

            try:
                idem = IdempotentKey.objects.get(idempotent_key=idempotent_key)
                if idem.status == 'SUCCESS':
                    logger.info(f"支付回调已处理: {transaction_id}")
                    return HttpResponse('success')  # 已处理过，直接返回成功
            except IdempotentKey.DoesNotExist:
                pass  # 未处理，继续

        # ──────────────────────────────────────────────────────────────────────
        # 4. 获取订单
        # ──────────────────────────────────────────────────────────────────────
        try:
            order = Order.objects.get(order_no=order_no)
        except Order.DoesNotExist:
            logger.error(f"订单不存在: {order_no}")
            return HttpResponse('fail')

        # ──────────────────────────────────────────────────────────────────────
        # 5. 如果订单已支付，直接返回成功（幂等性）
        # ──────────────────────────────────────────────────────────────────────
        if order.status in ['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']:
            return HttpResponse('success')

        # ──────────────────────────────────────────────────────────────────────
        # 6. 签名验证（安全核心）
        #    验证请求是否真的来自支付平台
        # ──────────────────────────────────────────────────────────────────────
        seller = order.seller
        provider = get_payment_provider(seller)
        verify_result = provider.verify_callback(data)

        if not verify_result.get('success'):
            logger.error(f"签名验证失败: {verify_result.get('error')}")
            return HttpResponse('fail')

        # ──────────────────────────────────────────────────────────────────────
        # 7. 金额验证（防止篡改）
        # ──────────────────────────────────────────────────────────────────────
        callback_amount = Decimal(str(verify_result.get('total_amount', 0)))
        if abs(callback_amount - order.total_amount) > Decimal('0.01'):
            logger.error(f"金额不一致: 回调={callback_amount}, 订单={order.total_amount}")
            return HttpResponse('fail')

        # ──────────────────────────────────────────────────────────────────────
        # 8. 处理支付成功（数据库事务）
        # ──────────────────────────────────────────────────────────────────────
        with transaction.atomic():
            # 8a. 再次检查订单状态（双重检查，防止并发）
            order = Order.objects.select_for_update().get(order_no=order_no)
            if order.status in ['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']:
                return HttpResponse('success')

            # 8b. 更新订单状态
            order.status = 'PAID'
            order.paid_at = timezone.now()
            order.transaction_id = transaction_id  # 保存交易号
            order.save()

            # 8c. 扣减库存（乐观锁）
            #     正常情况下，下单时已扣减库存，这里再次确认
            product = order.product
            affected = Product.objects.filter(
                id=product.id,
                stock__gte=order.quantity,
                version=product.version
            ).update(
                stock=F('stock') - order.quantity,
                version=F('version') + 1
            )

            if affected == 0:
                # 库存不足（理论上不会发生）
                logger.warning(f"库存不足，需要退款: 订单{order_no}")
                order.status = 'REFUNDING'
                order.save()
                return HttpResponse('fail')

            # 8d. 更新支付记录
            PaymentRecord.objects.filter(order=order).update(
                status='SUCCESS',
                callback_data=json.dumps(verify_result.get('raw_data', {})),
                updated_at=timezone.now()
            )

            # 8e. 记录幂等键（防止重复处理）
            if transaction_id:
                try:
                    IdempotentKey.objects.create(
                        idempotent_key=f"pay_callback_{transaction_id}",
                        order=order,
                        status='SUCCESS'
                    )
                except IntegrityError:
                    # 幂等键已存在（并发插入时可能发生）
                    pass

        logger.info(f"支付成功: 订单{order_no}, 交易号{transaction_id}")
        return HttpResponse('success')

    except Exception as e:
        logger.error(f"支付回调处理失败: {str(e)}", exc_info=True)
        return HttpResponse('fail')


def api_payment_result(request):
    """
    功能：支付结果页面（同步跳转）
    作用：支付完成后，支付平台同步跳转到此页面
    URL: GET /sales/api/payment_result/
    """
    order_no = request.GET.get('out_trade_no') or request.GET.get('order_no')
    if order_no:
        try:
            order = Order.objects.get(order_no=order_no)
            return render(request, 'sales/payment_result.html', {
                'order': order,
                'success': order.status in ['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']
            })
        except Order.DoesNotExist:
            pass

    return render(request, 'sales/payment_result.html', {
        'success': False,
        'error': '订单不存在'
    })


@csrf_exempt
def api_query_payment_status(request, order_no):
    """
    功能：查询支付状态
    作用：前端轮询查询支付结果
    URL: GET /sales/api/payment_status/<str:order_no>/
    """
    try:
        order = Order.objects.get(order_no=order_no)
        return JsonResponse({
            'order_no': order.order_no,
            'status': order.status,
            'status_display': order.get_status_display(),
            'paid_at': order.paid_at.strftime('%Y-%m-%d %H:%M:%S') if order.paid_at else None,
            'transaction_id': order.transaction_id,
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': '订单不存在'}, status=404)

@csrf_exempt
def api_product_image_set_cover(request, image_id):
    """设置图片为封面（仅管理员）"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not can_edit_product(account):
        return JsonResponse({'error': '无权限操作'}, status=403)

    try:
        image = ProductImage.objects.get(id=image_id)
        product = image.product

        # 取消所有封面
        ProductImage.objects.filter(product=product, is_cover=True).update(is_cover=False)

        # 设置当前图片为封面
        image.is_cover = True
        image.save()

        return JsonResponse({'success': True, 'message': '设置封面成功'})
    except ProductImage.DoesNotExist:
        return JsonResponse({'error': '图片不存在'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ========== 商户配置视图 ==========
@csrf_exempt
def seller_config(request):
    """
    功能：商户支付配置页面
    作用：卖家配置自己的微信/支付宝/银行支付参数
    权限：需要登录，且必须是卖家身份
    URL: GET /sales/seller_config/  (显示配置页面)
         POST /sales/api/seller_config/save/  (保存配置)
    """
    if not request.session.get('is_login', None):
        return redirect('/login/')

    account = request.session.get('account')
    user = get_current_user(account)
    if not user:
        return redirect('/login/')

    # 获取或创建卖家记录
    seller, created = Seller.objects.get_or_create(
        user=user,
        defaults={
            'seller_name': user.username or '我的店铺',
            'seller_code': f"SELLER{user.id:06d}",
            'payment_provider': 'WECHAT',
            'is_active': True
        }
    )

    return render(request, 'sales/seller_config.html', {
        'seller': seller,
        'can_edit': True,
    })


@csrf_exempt
def api_seller_config_save(request):
    """
    功能：保存商户配置
    作用：AJAX 保存卖家的支付配置
    权限：需要登录
    URL: POST /sales/api/seller_config/save/
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    try:
        data = json.loads(request.body)

        seller, created = Seller.objects.get_or_create(
            user=user,
            defaults={
                'seller_name': data.get('seller_name', user.username),
                'seller_code': f"SELLER{user.id:06d}",
                'payment_provider': data.get('payment_provider', 'WECHAT'),
                'is_active': True
            }
        )

        # 更新基本信息
        seller.seller_name = data.get('seller_name', seller.seller_name)
        seller.payment_provider = data.get('payment_provider', seller.payment_provider)

        # 微信支付配置
        seller.wechat_appid = data.get('wechat_appid', '')
        seller.wechat_mchid = data.get('wechat_mchid', '')
        seller.wechat_api_key = data.get('wechat_api_key', '')
        seller.wechat_cert_path = data.get('wechat_cert_path', '')
        seller.wechat_key_path = data.get('wechat_key_path', '')

        # 支付宝配置
        seller.alipay_app_id = data.get('alipay_app_id', '')
        seller.alipay_private_key = data.get('alipay_private_key', '')
        seller.alipay_public_key = data.get('alipay_public_key', '')
        seller.alipay_gateway = data.get('alipay_gateway', 'https://openapi.alipay.com/gateway.do')

        # 银行转账配置
        seller.bank_name = data.get('bank_name', '')
        seller.bank_account_name = data.get('bank_account_name', '')
        seller.bank_account_number = data.get('bank_account_number', '')
        seller.bank_branch = data.get('bank_branch', '')

        seller.save()

        return JsonResponse({
            'success': True,
            'message': '配置保存成功',
            'seller': {
                'id': seller.id,
                'seller_name': seller.seller_name,
                'payment_provider': seller.payment_provider,
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_seller_config_get(request):
    """
    功能：获取商户配置
    作用：AJAX 获取卖家的支付配置
    权限：需要登录
    URL: GET /sales/api/seller_config/get/
    """
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    user = get_current_user(account)
    if not user:
        return JsonResponse({'error': '用户不存在'}, status=404)

    seller = Seller.objects.filter(user=user).first()
    if not seller:
        return JsonResponse({'error': '卖家不存在，请先创建'}, status=404)

    return JsonResponse({
        'id': seller.id,
        'seller_name': seller.seller_name,
        'seller_code': seller.seller_code,
        'payment_provider': seller.payment_provider,
        'wechat_appid': seller.wechat_appid or '',
        'wechat_mchid': seller.wechat_mchid or '',
        'wechat_api_key': seller.wechat_api_key or '',
        'wechat_cert_path': seller.wechat_cert_path or '',
        'wechat_key_path': seller.wechat_key_path or '',
        'alipay_app_id': seller.alipay_app_id or '',
        'alipay_private_key': seller.alipay_private_key or '',
        'alipay_public_key': seller.alipay_public_key or '',
        'alipay_gateway': seller.alipay_gateway or 'https://openapi.alipay.com/gateway.do',
        'bank_name': seller.bank_name or '',
        'bank_account_name': seller.bank_account_name or '',
        'bank_account_number': seller.bank_account_number or '',
        'bank_branch': seller.bank_branch or '',
        'is_active': seller.is_active,
    })