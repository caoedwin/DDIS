# PCRList/views.py
import json
import base64
import openpyxl
from datetime import datetime, date

from django.db.models import Q, Sum
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.core.files.base import ContentFile

from .models import PCR
from CQM.models import CQMProject
from app01.models import UserInfo

def parse_request_data(request):
    """
    解析 JSON 或 FormData 请求，返回统一字典。
    支持字段：
        - 普通字符串
        - 数字（自动转 float）
        - 布尔（字符串 true/false 转 bool）
        - 日期（空字符串转为 None）
        - 文件（仅 FormData 时，存储在 data['attachment_file']）
    """
    content_type = request.content_type or ''
    if 'application/json' in content_type:
        data = json.loads(request.body)
    else:
        data = request.POST.dict()
        # 文件处理
        if 'attachment_file' in request.FILES:
            data['attachment_file'] = request.FILES['attachment_file']
        # 布尔字段转换
        for bool_field in ['pm_send_nre_to_sales', 'whether_in_budget', 'in_budget_but_cost_add']:
            if bool_field in data:
                val = data[bool_field]
                if isinstance(val, str):
                    data[bool_field] = val.lower() in ('true', '1', 'yes')
                else:
                    data[bool_field] = bool(val)
        # 数字字段转换
        for num_field in ['sample_qty', 'hc_qty', 'hc_days', 'device_fee_usd']:
            if num_field in data:
                try:
                    data[num_field] = float(data[num_field])
                except (ValueError, TypeError):
                    data[num_field] = 0.0
        # 日期字段空值处理
        for date_field in ['receive_date', 'execution_start', 'execution_end']:
            if date_field in data and not data[date_field]:
                data[date_field] = None
    return data


# ---------- 页面渲染 ----------
def pcr_list_page(request):
    """返回 PCR 管理页面"""
    return render(request, 'PCRList/pcr_list.html')


# ---------- 权限检查辅助函数（增强版，支持字符串用户名） ----------
def check_permission(user, compalproject):
    """
    检查用户是否有操作权限（管理员或项目 Owner）
    :param user: UserInfo 实例 或 用户名字符串
    :param compalproject: 项目名
    """
    # 如果传入的是字符串，则根据用户名获取 UserInfo 对象
    if isinstance(user, str):
        try:
            user = UserInfo.objects.get(account=user)   # 假设 account 字段存储用户名
        except UserInfo.DoesNotExist:
            return False

    # 超级管理员或 SVP 用户拥有所有权限
    if getattr(user, 'is_staff', False) or getattr(user, 'is_SVPuser', False):
        return True
    if user:
        roles = [role.name for role in user.role.all()]
        for role in roles:
            if role == 'admin' or 'DQA_C38_PCR_admin' in role:
                return True

    # 检查是否是项目的 Owner
    try:
        cqm_project = CQMProject.objects.get(Project=compalproject)
        return cqm_project.Owner.filter(id=user.id).exists()
    except CQMProject.DoesNotExist:
        return False


# ---------- API 视图 ----------
@csrf_exempt
@require_http_methods(["POST"])
def pcr_list_api(request):
    """获取 PCR 列表（支持时间段筛选，仅包含 execution_start 和 execution_end 均非空的记录）"""
    # 获取当前用户
    onlineuser = request.session.get('account')
    user_info = None
    if onlineuser:
        try:
            user_info = UserInfo.objects.get(account=onlineuser)
        except UserInfo.DoesNotExist:
            pass
    """获取 PCR 列表（支持时间段筛选，仅包含 execution_start 和 execution_end 均非空的记录）"""
    data = json.loads(request.body)
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    page = int(data.get('page', 1))
    page_size = int(data.get('page_size', 20))

    queryset = PCR.objects.all()

    # 日期筛选：要求两个日期都不为空，并且时间段有重叠
    if start_date and end_date:
        queryset = queryset.filter(
            execution_start__isnull=False,
            execution_end__isnull=False,
            execution_start__lte=end_date,
            execution_end__gte=start_date
        )
    elif start_date:
        queryset = queryset.filter(
            execution_start__isnull=False,
            execution_end__isnull=False,
            execution_end__gte=start_date
        )
    elif end_date:
        queryset = queryset.filter(
            execution_start__isnull=False,
            execution_end__isnull=False,
            execution_start__lte=end_date
        )

    paginator = Paginator(queryset, page_size)
    page_obj = paginator.get_page(page)

    data_list = []
    for pcr in page_obj:
        can_delete = False
        if user_info:
            can_delete = check_permission(user_info, pcr.Compalproject)
        data_list.append({
            'id': pcr.id,
            'pcr_no': pcr.pcr_no,
            'pcr_title': pcr.pcr_title,
            'Customer': pcr.Customer,
            'Project': pcr.Project,
            'Compalproject': pcr.Compalproject,
            'phase': pcr.phase,
            'category': pcr.category,
            'receive_date': pcr.receive_date.strftime('%Y-%m-%d') if pcr.receive_date else '',
            'status': pcr.status,
            'sample_qty': float(pcr.sample_qty),
            'hc_qty': float(pcr.hc_qty),
            'hc_days': float(pcr.hc_days),
            'pd': float(pcr.pd),
            'device_fee_usd': float(pcr.device_fee_usd),
            'pm_send_nre_to_sales': pcr.pm_send_nre_to_sales,
            'execution_start': pcr.execution_start.strftime('%Y-%m-%d') if pcr.execution_start else '',
            'execution_end': pcr.execution_end.strftime('%Y-%m-%d') if pcr.execution_end else '',
            'whether_in_budget': pcr.whether_in_budget,
            'in_budget_but_cost_add': pcr.in_budget_but_cost_add,
            'remark': pcr.remark,
            'attachment': "/media/" + pcr.attachment.url if pcr.attachment else '',
            'created_by': pcr.created_by.username if pcr.created_by else '',
            'can_delete': can_delete,
        })

    return JsonResponse({
        'data': data_list,
        'total': paginator.count,
        'page': page,
        'page_size': page_size,
    })

@csrf_exempt
@require_http_methods(["POST"])
def pcr_statistics_api(request):
    """统计数据（仅统计 execution_start 和 execution_end 均非空的记录）"""
    data = json.loads(request.body)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    # 基础筛选：只包含两个日期都不为空的记录
    base_queryset = PCR.objects.filter(
        execution_start__isnull=False,
        execution_end__isnull=False
    )

    # 再根据传入的时间范围进行重叠筛选
    if start_date and end_date:
        base_queryset = base_queryset.filter(
            execution_start__lte=end_date,
            execution_end__gte=start_date
        )
    elif start_date:
        base_queryset = base_queryset.filter(execution_end__gte=start_date)
    elif end_date:
        base_queryset = base_queryset.filter(execution_start__lte=end_date)

    def stats(qs, customer=None, phase=None):
        """聚合统计函数，返回 Perform 和 Plan 的五项指标"""
        q = qs
        if customer:
            q = q.filter(Customer=customer)
        if phase:
            q = q.filter(phase=phase)

        perform = q.filter(status='Perform').aggregate(
            sample=Coalesce(Sum('sample_qty'), 0),
            hc_qty=Coalesce(Sum('hc_qty'), 0),
            hc_days=Coalesce(Sum('hc_days'), 0),
            pd=Coalesce(Sum('pd'), 0),
            dev=Coalesce(Sum('device_fee_usd'), 0)
        )
        plan = q.filter(status='Plan').aggregate(
            sample=Coalesce(Sum('sample_qty'), 0),
            hc_qty=Coalesce(Sum('hc_qty'), 0),
            hc_days=Coalesce(Sum('hc_days'), 0),
            pd=Coalesce(Sum('pd'), 0),
            dev=Coalesce(Sum('device_fee_usd'), 0)
        )
        total = {
            'sample_qty': float(perform['sample'] + plan['sample']),
            'hc_qty': float(perform['hc_qty'] + plan['hc_qty']),
            'hc_days': float(perform['hc_days'] + plan['hc_days']),
            'pd': float(perform['pd'] + plan['pd']),
            'device_fee_usd': float(perform['dev'] + plan['dev'])
        }
        return {
            'perform': {
                'sample_qty': float(perform['sample']),
                'hc_qty': float(perform['hc_qty']),
                'hc_days': float(perform['hc_days']),
                'pd': float(perform['pd']),
                'device_fee_usd': float(perform['dev'])
            },
            'plan': {
                'sample_qty': float(plan['sample']),
                'hc_qty': float(plan['hc_qty']),
                'hc_days': float(plan['hc_days']),
                'pd': float(plan['pd']),
                'device_fee_usd': float(plan['dev'])
            },
            'total': total
        }

    result = {
        'total': stats(base_queryset),
        'NB': stats(base_queryset, customer='NB'),
        'AIO': stats(base_queryset, customer='AIO'),
        'NB_NPI': stats(base_queryset, customer='NB', phase='NPI'),
        'NB_INV': stats(base_queryset, customer='NB', phase='INV'),
        'AIO_NPI': stats(base_queryset, customer='AIO', phase='NPI'),
        'AIO_INV': stats(base_queryset, customer='AIO', phase='INV'),
    }
    return JsonResponse(result)

@csrf_exempt
@require_http_methods(["POST"])
def pcr_create_api(request):
    """单条新增（支持 JSON 和 FormData）"""
    try:
        onlineuser = request.session.get('account')
        if not onlineuser:
            return JsonResponse({'success': False, 'message': '用户未登录'}, status=401)
        user_info = UserInfo.objects.get(account=onlineuser)

        data = parse_request_data(request)

        # 权限检查
        compalproject = data.get('Compalproject', data.get('Project'))
        if not check_permission(user_info, compalproject):
            return JsonResponse({'success': False, 'message': '无权限操作该项目'}, status=403)

        # 唯一性检查
        pcr_no = data.get('pcr_no')
        project = data.get('Project')
        pcr_title = data.get('pcr_title')
        if not pcr_no or not project or not pcr_title:
            return JsonResponse({'success': False, 'message': 'PCR No, Project, PCR Title 不能为空'})
        if PCR.objects.filter(pcr_no=pcr_no, Project=project, pcr_title=pcr_title).exists():
            return JsonResponse({'success': False, 'message': 'PCR No+Project+Title 已存在'})

        # 创建记录
        pcr = PCR.objects.create(
            pcr_no=pcr_no,
            pcr_title=pcr_title,
            Customer=data.get('Customer', 'NB'),
            Project=project,
            Compalproject=compalproject,
            phase=data.get('phase', 'NPI'),
            category=data.get('category', ''),
            receive_date=data.get('receive_date'),
            status=data.get('status', 'Plan'),
            sample_qty=data.get('sample_qty', 0),
            hc_qty=data.get('hc_qty', 0),
            hc_days=data.get('hc_days', 0),
            device_fee_usd=data.get('device_fee_usd', 0),
            pm_send_nre_to_sales=data.get('pm_send_nre_to_sales', False),
            execution_start=data.get('execution_start'),
            execution_end=data.get('execution_end'),
            whether_in_budget=data.get('whether_in_budget', True),
            in_budget_but_cost_add=data.get('in_budget_but_cost_add', False),
            remark=data.get('remark', ''),
            created_by=user_info,
        )

        # 处理附件（若有）
        if 'attachment_file' in data:
            pcr.attachment = data['attachment_file']
            pcr.save()

        return JsonResponse({'success': True, 'id': pcr.id})
    except UserInfo.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户信息不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def pcr_update_api(request):
    """编辑记录（支持 JSON 和 FormData，可更新附件）"""
    try:
        onlineuser = request.session.get('account')
        if not onlineuser:
            return JsonResponse({'success': False, 'message': '用户未登录'}, status=401)
        user_info = UserInfo.objects.get(account=onlineuser)

        data = parse_request_data(request)

        # 获取原记录
        record_id = data.get('id')
        if not record_id:
            return JsonResponse({'success': False, 'message': '缺少记录 ID'}, status=400)
        pcr = PCR.objects.get(id=record_id)

        # 权限检查
        if not check_permission(user_info, pcr.Compalproject):
            return JsonResponse({'success': False, 'message': '无权限操作该项目'}, status=403)

        # 唯一性检查（排除自身）
        new_pcr_no = data.get('pcr_no', pcr.pcr_no)
        new_project = data.get('Project', pcr.Project)
        new_pcr_title = data.get('pcr_title', pcr.pcr_title)
        if PCR.objects.filter(pcr_no=new_pcr_no, Project=new_project, pcr_title=new_pcr_title).exclude(id=record_id).exists():
            return JsonResponse({'success': False, 'message': 'PCR No+Project+Title 已存在'})

        # 更新普通字段
        for field in ['pcr_no', 'pcr_title', 'Customer', 'Project', 'Compalproject', 'phase', 'category',
                      'receive_date', 'status', 'sample_qty', 'hc_qty', 'hc_days', 'device_fee_usd',
                      'pm_send_nre_to_sales', 'execution_start', 'execution_end', 'whether_in_budget',
                      'in_budget_but_cost_add', 'remark']:
            if field in data:
                setattr(pcr, field, data[field])

        # 处理附件
        if data.get('attachment_clear'):
            # 清除附件
            if pcr.attachment:
                pcr.attachment.delete(save=False)
            pcr.attachment = None
        elif 'attachment_file' in data:
            # 替换附件
            if pcr.attachment:
                pcr.attachment.delete(save=False)
            pcr.attachment = data['attachment_file']

        pcr.save()
        return JsonResponse({'success': True})
    except PCR.DoesNotExist:
        return JsonResponse({'success': False, 'message': '记录不存在'}, status=404)
    except UserInfo.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户信息不存在'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def pcr_delete_api(request):
    """删除"""
    try:
        onlineuser = request.session.get('account')
        user_info = UserInfo.objects.get(account=onlineuser)
        data = json.loads(request.body)
        pcr = PCR.objects.get(id=data['id'])

        if not check_permission(user_info, pcr.Compalproject):
            return JsonResponse({'success': False, 'message': '无权限'}, status=403)

        pcr.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def pcr_batch_delete_api(request):
    """批量删除 PCR 记录（仅允许有权限的用户删除其有权操作的项目）"""
    try:
        onlineuser = request.session.get('account')
        if not onlineuser:
            return JsonResponse({'success': False, 'message': '用户未登录'}, status=401)
        user_info = UserInfo.objects.get(account=onlineuser)

        data = json.loads(request.body)
        ids = data.get('ids', [])
        if not ids:
            return JsonResponse({'success': False, 'message': '未提供ID列表'})

        deleted_count = 0
        errors = []

        for pk in ids:
            try:
                pcr = PCR.objects.get(id=pk)
                # 权限检查
                if not check_permission(user_info, pcr.Compalproject):
                    errors.append(f'ID {pk} 无权限删除')
                    continue
                pcr.delete()
                deleted_count += 1
            except PCR.DoesNotExist:
                errors.append(f'ID {pk} 不存在')
            except Exception as e:
                errors.append(f'ID {pk} 删除失败: {str(e)}')

        return JsonResponse({
            'success': True,
            'deleted_count': deleted_count,
            'errors': errors
        })
    except UserInfo.DoesNotExist:
        return JsonResponse({'success': False, 'message': '用户信息不存在'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': '请求数据格式错误'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

# ---------- 安全转换函数 ----------
def safe_float(value):
    if value is None or str(value).strip() == '':
        return 0.0
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0


@csrf_exempt
@require_http_methods(["POST"])
def pcr_upload_excel_api(request):
    """批量上传 Excel（支持自动定位表头）"""
    # 获取当前登录用户信息
    onlineuser = request.session.get('account')
    if not onlineuser:
        return JsonResponse({'success': False, 'message': '用户未登录'})
    try:
        user_info = UserInfo.objects.get(account=onlineuser)
    except UserInfo.DoesNotExist:
        return JsonResponse({'success': False, 'message': f'用户 {onlineuser} 没有对应的 UserInfo 记录，请联系管理员'})

    if 'excel_file' not in request.FILES:
        return JsonResponse({'success': False, 'message': '未提供文件'})
    excel_file = request.FILES['excel_file']
    try:
        wb = openpyxl.load_workbook(excel_file, data_only=True)
        ws = wb.active
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'Excel解析失败: {str(e)}'})

    # 读取所有非空行
    rows = []
    for row in ws.iter_rows(values_only=True):
        if any(cell is not None and str(cell).strip() != '' for cell in row):
            rows.append(row)

    if len(rows) < 2:
        return JsonResponse({'success': False, 'message': '数据行数不足'})

    # ---------- 1. 定位主表头行 ----------
    header_row_idx = None
    subheader_row_idx = None
    required_keywords = ['pcr no', 'project', 'customer', 'status']

    for i in range(len(rows)):
        row = rows[i]
        if not row:
            continue
        row_lower = [str(cell).strip().lower() if cell else '' for cell in row]
        if all(any(keyword in cell for cell in row_lower) for keyword in required_keywords):
            header_row_idx = i
            if i + 1 < len(rows):
                next_row_lower = [str(cell).strip().lower() if cell else '' for cell in rows[i+1]]
                if any('sample' in cell or 'hc' in cell or 'device' in cell for cell in next_row_lower):
                    subheader_row_idx = i + 1
            break

    if header_row_idx is None:
        return JsonResponse({
            'success': False,
            'message': '未找到包含 "PCR No", "Project", "Customer", "Status" 的表头行，请检查Excel格式'
        })

    # 获取主表头和子表头
    main_headers = [str(cell).strip() if cell else '' for cell in rows[header_row_idx]]
    sub_headers = [str(cell).strip() if cell else '' for cell in rows[subheader_row_idx]] \
                  if subheader_row_idx is not None else [''] * len(main_headers)

    # ---------- 2. 字段映射 ----------
    field_mapping = {
        'pcr_no': ['PCR No', 'PCR No.', 'PCR Number'],
        'pcr_title': ['PCR Title', 'Title', 'PCR标题'],
        'Customer': ['Customer', '客户'],
        'Project': ['Project', '项目'],
        'Compalproject': ['Compal Project', 'Compalproject', 'Compal项目'],
        'phase': ['Phase', 'NPI or INV', '阶段'],
        'category': ['Category', '类别'],
        'receive_date': ['Receive Date', '接收日期'],
        'status': ['Status', '状态'],
        'sample_qty': ['Sample Qty', 'Sample Q\'ty', '样品数量'],
        'hc_qty': ['HC Qty', 'HC Q\'ty', 'HC数量'],
        'hc_days': ['HC Days', 'HC Days', 'HC天数'],
        'device_fee_usd': ['Device fee (USD)', 'Device Fee', '设备费'],
        'pm_send_nre_to_sales': ['PM send NRE to Sales', 'PM发送NRE给Sales'],
        'execution_start': ['Execution Start', '执行开始'],
        'execution_end': ['Execution End', '执行结束'],
        'whether_in_budget': ['Whether In Budget', '是否在预算内'],
        'in_budget_but_cost_add': ['In budget but cost add', '预算内但成本增加'],
        'remark': ['Remark', '备注'],
    }

    col_index_map = {}
    for idx, (main, sub) in enumerate(zip(main_headers, sub_headers)):
        combined = f"{main} {sub}".strip() if sub else main
        if not combined:
            continue
        combined_lower = combined.lower()
        for db_field, aliases in field_mapping.items():
            if any(alias.lower() == combined_lower or alias.lower() == main.lower() or
                   (sub and alias.lower() == sub.lower()) for alias in aliases):
                col_index_map[db_field] = idx
                break
        # 特殊匹配子表头关键词
        sub_lower = sub.lower()
        if 'sample' in sub_lower and 'sample_qty' not in col_index_map:
            col_index_map['sample_qty'] = idx
        elif 'hc qty' in sub_lower and 'hc_qty' not in col_index_map:
            col_index_map['hc_qty'] = idx
        elif 'hc days' in sub_lower and 'hc_days' not in col_index_map:
            col_index_map['hc_days'] = idx
        elif 'device fee' in sub_lower and 'device_fee_usd' not in col_index_map:
            col_index_map['device_fee_usd'] = idx

    # ✅ 关键修复1：将列索引转换为整数（必须在循环外部，只执行一次）
    col_index_map = {k: int(v) for k, v in col_index_map.items()}

    # 检查必要字段
    required_db_fields = ['pcr_no', 'pcr_title', 'Project', 'Customer', 'phase', 'status']
    missing = [f for f in required_db_fields if f not in col_index_map]
    if missing:
        return JsonResponse({'success': False, 'message': f'缺少必要的列映射: {missing}，请检查表头'})

    # ---------- 3. 定位数据起始行 ----------
    start_row = (subheader_row_idx if subheader_row_idx is not None else header_row_idx) + 1
    while start_row < len(rows):
        row = rows[start_row]
        pcr_col = col_index_map.get('pcr_no')
        if pcr_col is not None and pcr_col < len(row) and row[pcr_col] and str(row[pcr_col]).strip():
            break
        start_row += 1

    # ---------- 辅助函数 ----------
    def parse_date(value):
        if not value:
            return None
        if isinstance(value, (datetime, date)):
            return value.date() if hasattr(value, 'date') else value
        if isinstance(value, str):
            for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d/%m/%Y', '%m/%d/%Y'):
                try:
                    return datetime.strptime(value.strip(), fmt).date()
                except:
                    continue
        return None

    def parse_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('yes', 'y', 'true', '1', '是')
        return bool(value)

    def truncate_str(value, max_len):
        """安全截断字符串"""
        if value is None:
            return ''
        s = str(value).strip()
        return s[:max_len] if len(s) > max_len else s

    success_count = 0
    duplicates = []
    errors = []

    for idx in range(start_row, len(rows)):
        row = rows[idx]
        pcr_col = col_index_map.get('pcr_no')
        if pcr_col is None or pcr_col >= len(row) or not row[pcr_col]:
            continue

        try:
            pcr_no = truncate_str(row[pcr_col], 50)
            project_col = col_index_map['Project']
            project = truncate_str(row[project_col], 50) if project_col < len(row) else ''
            pcr_title_col = col_index_map['pcr_title']
            pcr_title = truncate_str(row[pcr_title_col], 200) if pcr_title_col < len(row) else ''

            # 重复检查
            if PCR.objects.filter(pcr_no=pcr_no, Project=project, pcr_title=pcr_title).exists():
                duplicates.append(f"第{idx+1}行: {pcr_no} - {project} - {pcr_title}")
                continue

            # ✅ 关键修复2：Compalproject 默认使用 -1 而不是空字符串，避免字符串比较
            compal_col = col_index_map.get('Compalproject', -1)
            compalproject = ''
            if compal_col != -1 and compal_col < len(row):
                compalproject = truncate_str(row[compal_col], 50)
            else:
                # 如果没有找到 Compalproject 列，则使用 Project 列的值
                compalproject = project

            if not check_permission(user_info, compalproject):
                errors.append(f"第{idx+1}行: 无权限操作机种 {compalproject}")
                continue

            # 其他字段
            category_val = ''
            if 'category' in col_index_map and col_index_map['category'] < len(row):
                category_val = truncate_str(row[col_index_map['category']], 50)

            remark_val = ''
            if 'remark' in col_index_map and col_index_map['remark'] < len(row):
                remark_val = truncate_str(row[col_index_map['remark']], 500)

            # 日期处理：若缺失则使用今天（或 None，根据模型）
            receive_date_val = None
            if 'receive_date' in col_index_map and col_index_map['receive_date'] < len(row):
                receive_date_val = parse_date(row[col_index_map['receive_date']])
            if receive_date_val is None:
                receive_date_val = date.today()   # 避免 NOT NULL 约束错误

            create_data = {
                'pcr_no': pcr_no,
                'pcr_title': pcr_title,
                'Customer': row[col_index_map['Customer']] if col_index_map['Customer'] < len(row) else 'NB',
                'Project': project,
                'Compalproject': compalproject,
                'phase': row[col_index_map['phase']] if col_index_map['phase'] < len(row) else 'NPI',
                'category': category_val,
                'receive_date': receive_date_val,
                'status': row[col_index_map['status']] if col_index_map['status'] < len(row) else 'Plan',
                'sample_qty': safe_float(row[col_index_map.get('sample_qty', -1)]),
                'hc_qty': safe_float(row[col_index_map.get('hc_qty', -1)]),
                'hc_days': safe_float(row[col_index_map.get('hc_days', -1)]),
                'device_fee_usd': safe_float(row[col_index_map.get('device_fee_usd', -1)]),
                'pm_send_nre_to_sales': parse_bool(row[col_index_map['pm_send_nre_to_sales']]) if 'pm_send_nre_to_sales' in col_index_map else False,
                'execution_start': parse_date(row[col_index_map['execution_start']]) if 'execution_start' in col_index_map else None,
                'execution_end': parse_date(row[col_index_map['execution_end']]) if 'execution_end' in col_index_map else None,
                'whether_in_budget': parse_bool(row[col_index_map['whether_in_budget']]) if 'whether_in_budget' in col_index_map else True,
                'in_budget_but_cost_add': parse_bool(row[col_index_map['in_budget_but_cost_add']]) if 'in_budget_but_cost_add' in col_index_map else False,
                'remark': remark_val,
                'created_by': user_info,
            }

            PCR.objects.create(**create_data)
            success_count += 1

        except Exception as e:
            errors.append(f"第{idx+1}行: {str(e)}")

    return JsonResponse({
        'success': True,
        'success_count': success_count,
        'duplicates': duplicates,
        'errors': errors
    })