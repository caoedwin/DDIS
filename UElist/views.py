# UElist/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import json, datetime, traceback
import pandas as pd
from io import BytesIO
import xlsxwriter
from django.db import transaction
from django.db.models import Q
from django.forms.models import model_to_dict
from django.db.models.functions import Length

# 导入模型
from .models import UEInspectionItem, UEBatch, UEScoreRecord
from CQM.models import CQMProject
from app01.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Value, CharField
from django.db.models.functions import Trim, Upper

@csrf_exempt
def UEItems_edit(request):
    """UE检查项目管理页面"""
    # 检查登录状态
    if not request.session.get('is_login', None):
        return redirect('/login/')

    # 获取皮肤设置
    Skin = request.COOKIES.get('Skin_raw')
    if not Skin:
        Skin = "/static/src/blue.jpg"

    weizhi = "DDIS/UE检查项目管理"

    canEdit = 0
    onlineuser = request.session.get('account')
    if onlineuser:
        user_obj = UserInfo.objects.filter(account=onlineuser).first()
        if user_obj:
            roles = [role.name for role in user_obj.role.all()]
            for role in roles:
                if role == 'admin' or 'DQA_SW_edit' in role:
                    canEdit = 1
                    break

    # 初始化变量
    content = []
    addselect = []
    errMsg = ''

    # 获取当前用户
    onlineuser = request.session.get('account', '')
    # 1. Function 选项
    function_choices = [{'value': k, 'label': v} for k, v in UEInspectionItem.CATEGORY_CHOICES]

    # 2. Category 选项 —— 手动去重（标准化 + 保留第一个出现的原始值）
    categories_qs = UEInspectionItem.objects.exclude(
        Category__isnull=True
    ).exclude(
        Category__exact=''
    ).values_list('Category', flat=True)

    category_dict = {}
    for cat in categories_qs:
        # 标准化：去除首尾空格 + 将连续空白压缩为单个空格（避免换行符差异）
        normalized = ' '.join(cat.strip().split())
        if normalized not in category_dict:
            # 保留首次出现的原始值（或可选择标准化后的值）
            category_dict[normalized] = cat  # 这里用 cat 保留原始格式，也可用 normalized

    category_list = [
        {'value': value, 'label': value}
        for value in category_dict.values()
    ]

    # 3. Item 选项 —— 同样手动去重（去除首尾空格后去重）
    items_qs = UEInspectionItem.objects.exclude(
        Item__isnull=True
    ).exclude(
        Item__exact=''
    ).values_list('Item', flat=True)

    item_dict = {}
    for item in items_qs:
        cleaned = item.strip()
        if cleaned not in item_dict:
            item_dict[cleaned] = cleaned  # 直接用清洗后的值

    item_list = [
        {'value': value, 'label': value}
        for value in item_dict.values()
    ]

    # POST请求处理
    if request.method == "POST":
        try:
            isGetData = request.POST.get('isGetData', '')

            if isGetData == 'first':


                return JsonResponse({
                    'function_choices': function_choices,
                    'category_options': category_list,
                    'item_options': item_list
                })

            elif isGetData == 'Search':
                # 搜索功能
                search_item = request.POST.get('Item', '').strip()
                search_function = request.POST.get('Function', '').strip()
                search_category = request.POST.get('Category', '').strip()

                query = Q()
                if search_item:
                    query &= Q(Item__icontains=search_item)
                if search_function:
                    query &= Q(Function=search_function)
                if search_category:
                    query &= Q(Category__icontains=search_category)

                items = UEInspectionItem.objects.filter(query) \
                    .order_by(
                    Length('Item').asc(),  # 先按字符长度
                    'Item'  # 再按字母顺序
                )

                items_list = []
                for item in items:
                    items_list.append({
                        'id': item.id,
                        'Item': item.Item,
                        'Function': item.Function,
                        'Category': item.Category,
                        'characteristic': item.characteristic,
                        'detailed_description': item.detailed_description,
                        'inspect_method': item.inspect_method,
                        'status': item.status,
                    })

                data = {
                    'content': items_list,
                    'errMsg': errMsg,
                    'function_choices': function_choices,
                    'category_options': category_list,
                    'item_options': item_list
                }
                return JsonResponse(data)

            if canEdit != 1:
                return JsonResponse({'errMsg': '您没有权限执行此操作'})


            elif isGetData == 'submit':
                if canEdit != 1:
                    return JsonResponse({'errMsg': '您没有权限执行此操作'})
                # 新增或编辑检查项
                item_id = request.POST.get('id', '')
                item_code = request.POST.get('Item', '').strip()
                function = request.POST.get('Function', '').strip()
                category = request.POST.get('Category', '').strip()
                characteristic = request.POST.get('characteristic', '').strip()
                detailed_description = request.POST.get('detailed_description', '').strip()
                inspect_method = request.POST.get('inspect_method', '').strip()
                status = request.POST.get('status', 'active')  # 默认 active

                # 验证必填字段
                if not all([item_code, function, category, characteristic]):
                    return JsonResponse({'errMsg': '必填字段不能为空'})

                if item_id:  # 编辑
                    try:
                        item_obj = UEInspectionItem.objects.get(id=item_id)
                        item_obj.Item = item_code
                        item_obj.Function = function
                        item_obj.Category = category
                        item_obj.characteristic = characteristic
                        item_obj.detailed_description = detailed_description
                        item_obj.inspect_method = inspect_method
                        item_obj.status = status
                        item_obj.save()

                        return JsonResponse({'success': True})
                    except UEInspectionItem.DoesNotExist:
                        return JsonResponse({'errMsg': '项目不存在'})
                    except Exception as e:
                        return JsonResponse({'errMsg': f'更新失败: {str(e)}'})
                else:  # 新增
                    # 检查是否已存在相同Item
                    if UEInspectionItem.objects.filter(Item=item_code).exists():
                        return JsonResponse({'errMsg': f'Item {item_code} 已存在'})

                    try:
                        UEInspectionItem.objects.create(
                            Item=item_code,
                            Function=function,
                            Category=category,
                            characteristic=characteristic,
                            detailed_description=detailed_description,
                            inspect_method=inspect_method,
                            status=status,
                        )
                        return JsonResponse({'success': True})
                    except Exception as e:
                        return JsonResponse({'errMsg': f'创建失败: {str(e)}'})


            elif isGetData == 'delete':

                if canEdit != 1:
                    return JsonResponse({'errMsg': '您没有权限执行此操作'})

                item_id = request.POST.get('id', '')

                try:

                    item = UEInspectionItem.objects.get(id=item_id)

                    # 检查是否已被评分记录引用

                    if UEScoreRecord.objects.filter(inspection_item=item).exists():
                        return JsonResponse({'errMsg': '该检查项已被评分记录引用，无法删除'})

                    item.delete()

                    return JsonResponse({'success': True})

                except UEInspectionItem.DoesNotExist:

                    return JsonResponse({'errMsg': '项目不存在'})

                except Exception as e:

                    return JsonResponse({'errMsg': f'删除失败: {str(e)}'})

            elif isGetData == 'upload_excel':
                if canEdit != 1:
                    return JsonResponse({'errMsg': '您没有权限执行此操作'})

                # ========== 高性能批量导入，带字段保护 ==========

                excel_file = request.FILES.get('excel_file')

                if not excel_file:
                    return JsonResponse({'errMsg': '请选择Excel文件'})

                try:

                    # ----- 1. 动态定位表头 -----

                    xl = pd.ExcelFile(excel_file)

                    sheet_names = xl.sheet_names

                    target_sheet = next((s for s in ['Check list', '工作表1'] if s in sheet_names), sheet_names[0])

                    df = pd.read_excel(excel_file, sheet_name=target_sheet, header=None)

                    header_row_idx = None

                    for i in range(min(10, len(df))):

                        row_str = ' '.join(df.iloc[i].astype(str).str.lower().str.strip())

                        if all(k in row_str for k in ['item', 'function', 'category', 'characteristic']):
                            header_row_idx = i

                            break

                    if header_row_idx is None:
                        return JsonResponse({'errMsg': '未找到包含Item,Function,Category,Characteristic的表头行'})

                    df.columns = df.iloc[header_row_idx].astype(str).str.strip()

                    df = df.iloc[header_row_idx + 1:].reset_index(drop=True)

                    # ----- 2. 列名映射 -----

                    required_cols = ['Item', 'Function', 'Category', 'Characteristic']

                    if not all(col in df.columns for col in required_cols):
                        return JsonResponse({'errMsg': f'Sheet缺少必要列: {required_cols}'})

                    desc_col = next(

                        (c for c in ['詳細說明（Detailed Description）', 'Detailed Description'] if c in df.columns),

                        None)

                    method_col = next((c for c in ['Inspect Methord', 'Inspect Method'] if c in df.columns), None)

                    # ----- 3. 受保护字段定义（已有非空值禁止被空覆盖）-----

                    PROTECTED_FIELDS = [

                        'Function',

                        'Category',

                        'characteristic',

                        'detailed_description',

                        'inspect_method'

                    ]  # 您可按需增删，例如允许清空“详细说明”则可移出此列表

                    # ----- 4. 解析数据，按Item去重（保留最后出现行）-----

                    data_dict = {}

                    for idx, row in df.iterrows():

                        item = str(row['Item']).strip()

                        if pd.isna(item) or item == '' or item.lower() == 'nan':
                            continue

                        data_dict[item] = {

                            'Function': str(row['Function']).strip(),

                            'Category': str(row['Category']).strip(),

                            'characteristic': str(row['Characteristic']).strip(),

                            'detailed_description': str(row[desc_col]).strip() if desc_col else '',

                            'inspect_method': str(row[method_col]).strip() if method_col else '',

                        }

                    if not data_dict:
                        return JsonResponse({'errMsg': 'Excel中没有有效数据'})

                    # ----- 5. 分离已存在和新增的Item -----

                    existing_items = set(

                        UEInspectionItem.objects.filter(Item__in=data_dict.keys()).values_list('Item', flat=True)

                    )

                    to_create = []

                    to_update_objs = []  # 存储实际需要更新的对象

                    skipped_no_change = 0  # 统计无任何字段更新的记录

                    for item, fields in data_dict.items():

                        if item not in existing_items:

                            # 新增：直接使用Excel值（空就是空）

                            to_create.append(UEInspectionItem(Item=item, status='active', **fields))

                        else:

                            # 更新：应用字段保护规则

                            try:

                                obj = UEInspectionItem.objects.get(Item=item)  # 可改用filter一次性取出，此处简化

                            except UEInspectionItem.DoesNotExist:

                                continue

                            need_update = False

                            for field in PROTECTED_FIELDS:

                                new_val = fields.get(field, '')

                                current_val = getattr(obj, field, '')

                                # 保护规则：新值为空 且 当前值非空 → 跳过

                                if new_val == '' and current_val != '':
                                    continue

                                # 其他情况（新值非空 / 新值为空但当前值也为空 / 字段不在保护列表）均执行赋值

                                setattr(obj, field, new_val)

                                need_update = True

                            if need_update:

                                to_update_objs.append(obj)

                            else:

                                skipped_no_change += 1

                    # ----- 6. 执行数据库操作（事务）-----

                    created_count = 0

                    updated_count = 0

                    with transaction.atomic():

                        if to_create:
                            created_objs = UEInspectionItem.objects.bulk_create(to_create, batch_size=500)

                            created_count = len(created_objs)

                        if to_update_objs:

                            # === 如果您使用 Django ≥ 2.2，推荐 bulk_update ===

                            try:

                                UEInspectionItem.objects.bulk_update(

                                    to_update_objs,

                                    fields=PROTECTED_FIELDS,  # 仅更新这5个字段

                                    batch_size=500

                                )

                            except AttributeError:

                                # === 兼容低版本 Django：逐条 save ===

                                for obj in to_update_objs:
                                    obj.save()

                            updated_count = len(to_update_objs)

                    # ----- 7. 返回结果 -----

                    message = f'成功处理 {len(data_dict)} 条记录'

                    if created_count:
                        message += f'，新增 {created_count} 条'

                    if updated_count:
                        message += f'，更新 {updated_count} 条'

                    if skipped_no_change:
                        message += f'，{skipped_no_change} 条记录无变化（已有数据未被空值覆盖）'

                    return JsonResponse({

                        'success': True,

                        'message': message,

                        'errors': []

                    })


                except Exception as e:

                    traceback.print_exc()

                    return JsonResponse({'errMsg': f'Excel处理失败: {str(e)}'})


        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'errMsg': f'服务器错误: {str(e)}'})

    # GET请求 - 渲染页面
    # 获取类别用于下拉框
    categories = UEInspectionItem.objects.values('Category').distinct()
    category_list = [{'Category': cat['Category']} for cat in categories]

    return render(request, 'UElist/UEItems_edit.html', {
        'Skin': Skin,
        'weizhi': weizhi,
        'addselect': category_list,
        'canEdit': canEdit,
    })

@csrf_exempt
def UE_ProjectResult(request):
    """UE专案打分页面"""
    # 检查登录状态
    if not request.session.get('is_login', None):
        return redirect('/login/')

    # 获取皮肤设置
    Skin = request.COOKIES.get('Skin_raw')
    if not Skin:
        Skin = "/static/src/blue.jpg"

    weizhi = "DDIS/UE专案打分"

    # 获取当前用户
    onlineuser = request.session.get('account', '')

    # POST请求处理
    if request.method == "POST":
        try:
            action = request.POST.get('action', '')

            if action == 'get_projects':
                projects = CQMProject.objects.all().order_by('Project')
                project_list = []
                for project in projects:
                    owner_names = [user.account for user in project.Owner.all()]
                    project_list.append({
                        'id': project.id,
                        'Project': project.Project,
                        'Customer': getattr(project, 'Customer', ''),
                        'owners': owner_names,
                        'owner_flag': onlineuser in owner_names
                    })
                return JsonResponse({'projects': project_list})

                # -------------------- 2. 获取用户列表（新增）--------------------
            elif action == 'get_users':
                users = UserInfo.objects.all().order_by('username')
                user_list = []
                for user in users:
                    # 工号优先取 employee_id，若无则用 account
                    emp_id = getattr(user, 'employee_id', user.account)
                    user_list.append({
                        'user_id': user.id,
                        'name': user.username,  # 显示名称
                        'employee_id': emp_id  # 工号
                    })
                return JsonResponse({'users': user_list})

                # -------------------- 3. 获取批次列表（增强）--------------------
            elif action == 'get_batches':
                project_id = request.POST.get('project_id', '')
                if not project_id:
                    return JsonResponse({'batches': []})

                batches = UEBatch.objects.filter(project_id=project_id).order_by('-test_date')
                batch_list = []
                for batch in batches:
                    # 获取该批次所有测试人员信息
                    testers = batch.testers.all()  # 多对多
                    tester_ids = [t.id for t in testers]
                    tester_names = [t.username for t in testers]

                    # 判断当前用户是否为测试人员
                    current_user_is_tester = testers.filter(account=onlineuser).exists()

                    batch_list.append({
                        'batch_id': batch.batch_id,
                        'batch_name': batch.batch_name,
                        'test_date': batch.test_date.strftime('%Y-%m-%d'),
                        'tester_ids': tester_ids,  # 数组
                        'tester_names': tester_names,  # 数组
                        'created_by': batch.created_by.username if batch.created_by else '',
                        'current_user_is_tester': current_user_is_tester,  # 布尔值
                    })
                return JsonResponse({'batches': batch_list})

                # -------------------- 4. 获取单个批次详情（新增）--------------------
            elif action == 'get_batch_detail':
                batch_id = request.POST.get('batch_id', '')
                try:
                    batch = UEBatch.objects.get(batch_id=batch_id)
                    testers = batch.testers.all()
                    tester_ids = [t.id for t in testers]
                    tester_names = [t.username for t in testers]
                    current_user_is_tester = testers.filter(account=onlineuser).exists()

                    batch_detail = {
                        'batch_id': batch.batch_id,
                        'batch_name': batch.batch_name,
                        'test_date': batch.test_date.strftime('%Y-%m-%d'),
                        'tester_ids': tester_ids,
                        'tester_names': tester_names,
                        'created_by': batch.created_by.username if batch.created_by else '',
                        'current_user_is_tester': current_user_is_tester,
                        'project_id': batch.project.id,
                        'project_name': batch.project.Project,
                    }
                    return JsonResponse({'batch': batch_detail})
                except UEBatch.DoesNotExist:
                    return JsonResponse({'batch': None, 'message': '批次不存在'})

                # -------------------- 5. 创建批次（支持多测试人员）--------------------
            elif action == 'create_batch':
                project_id = request.POST.get('project_id', '')
                batch_name = request.POST.get('batch_name', '').strip()
                test_date = request.POST.get('test_date', '')
                tester_ids_str = request.POST.get('tester_ids', '')  # 逗号分隔的字符串

                if not all([project_id, batch_name, test_date, tester_ids_str]):
                    return JsonResponse({'success': False, 'message': '所有字段都必须填写'})

                try:
                    project = CQMProject.objects.get(id=project_id)
                    if UEBatch.objects.filter(project=project, batch_name=batch_name).exists():
                        return JsonResponse({'success': False, 'message': '批次名称已存在'})

                    # 获取当前用户作为创建人
                    try:
                        creator = UserInfo.objects.get(account=onlineuser)
                    except UserInfo.DoesNotExist:
                        return JsonResponse({'success': False, 'message': '用户不存在'})

                    # 解析测试人员ID列表
                    tester_id_list = [int(x) for x in tester_ids_str.split(',') if x.strip()]
                    testers = UserInfo.objects.filter(id__in=tester_id_list)

                    # 创建批次（此时暂不设testers，需先保存才能添加多对多）
                    batch = UEBatch.objects.create(
                        project=project,
                        batch_name=batch_name,
                        test_date=test_date,
                        created_by=creator,
                    )
                    # 添加测试人员（多对多）
                    batch.testers.set(testers)

                    # 为该批次创建所有检查项的空评分记录
                    inspection_items = UEInspectionItem.objects.filter(status='active')
                    for item in inspection_items:
                        UEScoreRecord.objects.create(
                            batch=batch,
                            inspection_item=item,
                            scorer=creator  # 初始评分人设为创建人（可选）
                        )

                    return JsonResponse({
                        'success': True,
                        'message': '批次创建成功',
                        'batch_id': batch.batch_id
                    })

                except CQMProject.DoesNotExist:
                    return JsonResponse({'success': False, 'message': '机种不存在'})
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'创建失败: {str(e)}'})

                # -------------------- 6. 获取评分数据（不变）--------------------
            elif action == 'get_scores':
                batch_id = request.POST.get('batch_id', '')
                if not batch_id:
                    return JsonResponse({'scores': []})
                try:
                    batch = UEBatch.objects.get(batch_id=batch_id)
                    score_records = UEScoreRecord.objects.filter(batch=batch) \
                        .select_related('inspection_item') \
                        .order_by(
                        Length('inspection_item__Item').asc(),  # 先按字符长度升序
                        'inspection_item__Item'  # 再按字母顺序
                    )
                    score_list = []
                    for record in score_records:
                        score_list.append({
                            'record_id': record.record_id,
                            'item_id': record.inspection_item.id,
                            'Item': record.inspection_item.Item,
                            'Function': record.inspection_item.Function,
                            'Category': record.inspection_item.Category,
                            'characteristic': record.inspection_item.characteristic,
                            'OneStar': record.OneStar,
                            'TwoStar': record.TwoStar,
                            'ThreeStar': record.ThreeStar,
                            'NotSup': record.NotSup,
                            'remark': record.remark,
                            'scorer': record.scorer.username if record.scorer else '',
                            'scored_date': record.scored_date.strftime('%Y-%m-%d %H:%M:%S')
                        })
                    return JsonResponse({
                        'scores': score_list,
                        'batch_name': batch.batch_name,
                        'project_name': batch.project.Project
                    })
                except UEBatch.DoesNotExist:
                    return JsonResponse({'scores': []})

                # -------------------- 7. 更新单条评分（增强返回）--------------------
            elif action == 'update_score':
                record_id = request.POST.get('record_id', '')
                one_star = request.POST.get('OneStar', '')
                two_star = request.POST.get('TwoStar', '')
                three_star = request.POST.get('ThreeStar', '')
                not_sup = request.POST.get('NotSup', '')
                remark = request.POST.get('remark', '')

                if not record_id:
                    return JsonResponse({'success': False, 'message': '记录ID不能为空'})

                try:
                    record = UEScoreRecord.objects.get(record_id=record_id)

                    # 权限验证：只有该批次的测试人员才能修改
                    batch = record.batch
                    if not batch.testers.filter(account=onlineuser).exists():
                        return JsonResponse({'success': False, 'message': '您不是该批次的测试人员，无权修改'})

                    user_info = UserInfo.objects.get(account=onlineuser)

                    record.OneStar = one_star
                    record.TwoStar = two_star
                    record.ThreeStar = three_star
                    record.NotSup = not_sup
                    record.remark = remark
                    record.scorer = user_info
                    record.save()

                    # 返回更新后的评分人及时间，供前端刷新
                    return JsonResponse({
                        'success': True,
                        'message': '更新成功',
                        'record': {
                            'scorer': record.scorer.username if record.scorer else '',
                            'scored_date': record.scored_date.strftime('%Y-%m-%d %H:%M:%S')
                        }
                    })

                except UEScoreRecord.DoesNotExist:
                    return JsonResponse({'success': False, 'message': '记录不存在'})
                except UserInfo.DoesNotExist:
                    return JsonResponse({'success': False, 'message': '用户不存在'})


            # ========== 高性能批量导入评分 ==========

            elif action == 'upload_excel_score':

                batch_id = request.POST.get('batch_id', '')

                excel_file = request.FILES.get('excel_file')

                if not batch_id:
                    return JsonResponse({'success': False, 'message': '请先选择批次'})

                if not excel_file:
                    return JsonResponse({'success': False, 'message': '请选择Excel文件'})

                try:

                    batch = UEBatch.objects.get(batch_id=batch_id)

                    # 权限验证：仅批次测试人员可上传

                    if not batch.testers.filter(account=onlineuser).exists():
                        return JsonResponse({'success': False, 'message': '您不是该批次的测试人员，无权上传'})

                    try:

                        user_info = UserInfo.objects.get(account=onlineuser)

                    except UserInfo.DoesNotExist:

                        return JsonResponse({'success': False, 'message': '用户不存在'})

                    # ---------- 1. 动态定位表头 ----------

                    xl = pd.ExcelFile(excel_file)

                    sheet_names = xl.sheet_names

                    target_sheet = next((s for s in ['Check list', '工作表1'] if s in sheet_names), sheet_names[0])

                    df = pd.read_excel(excel_file, sheet_name=target_sheet, header=None)

                    header_row_idx = None

                    for i in range(min(10, len(df))):

                        row_str = ' '.join(df.iloc[i].astype(str).str.lower().str.strip())

                        if all(k in row_str for k in ['item', 'function', 'category', 'characteristic']):
                            header_row_idx = i

                            break

                    if header_row_idx is None:
                        return JsonResponse(

                            {'success': False, 'message': '未找到包含Item,Function,Category,Characteristic的表头行'})

                    df.columns = df.iloc[header_row_idx].astype(str).str.strip()

                    df = df.iloc[header_row_idx + 1:].reset_index(drop=True)

                    # ---------- 2. 评分字段映射 ----------

                    SCORE_FIELD_MAP = {

                        '★': 'OneStar', '★★': 'TwoStar', '★★★': 'ThreeStar',

                        'not support': 'NotSup', 'remark': 'remark',

                        'ones': 'OneStar', 'twos': 'TwoStar', 'threes': 'ThreeStar',

                        'notsup': 'NotSup', '备注': 'remark',

                    }

                    if 'Item' not in df.columns:
                        return JsonResponse({'success': False, 'message': 'Excel缺少必要的"Item"列'})

                    actual_score_columns = {}

                    for col in df.columns:

                        col_lower = col.lower().strip()

                        if col_lower in SCORE_FIELD_MAP:
                            actual_score_columns[col] = SCORE_FIELD_MAP[col_lower]

                    if not actual_score_columns:
                        return JsonResponse(

                            {'success': False, 'message': 'Excel中未找到任何评分列（★, ★★, ★★★, Not Support, Remark等）'})

                    # ---------- 3. 解析数据，按Item去重（后出现覆盖前）----------

                    data_dict = {}

                    for idx, row in df.iterrows():

                        item_code = str(row['Item']).strip()

                        if pd.isna(item_code) or item_code == '' or item_code.lower() == 'nan':
                            continue

                        score_values = {}

                        for excel_col, db_field in actual_score_columns.items():

                            val = row.get(excel_col)

                            if pd.isna(val):

                                val = ''

                            else:

                                val = str(val).strip()

                            score_values[db_field] = val

                        data_dict[item_code] = score_values

                    if not data_dict:
                        return JsonResponse({'success': False, 'message': 'Excel中没有有效的Item数据'})

                    # ========== 互斥校验（新增） ==========

                    conflict_items = []

                    for item_code, sv in data_dict.items():

                        one = sv.get('OneStar', '')

                        two = sv.get('TwoStar', '')

                        three = sv.get('ThreeStar', '')

                        notsup = sv.get('NotSup', '')

                        star_count = sum([1 for v in [one, two, three] if v == 'V'])

                        notsup_flag = (notsup == 'N/S')

                        if star_count > 1 or (star_count >= 1 and notsup_flag):
                            conflict_items.append(item_code)

                    if conflict_items:

                        error_msg = f'Excel中存在互斥冲突的行，请修改后重新上传。冲突的Item: {", ".join(conflict_items[:10])}'

                        if len(conflict_items) > 10:
                            error_msg += f' 等共{len(conflict_items)}条'

                        return JsonResponse({'success': False, 'message': error_msg})

                    # ---------- 4. 查询系统中存在的检查项 ----------

                    items_in_excel = list(data_dict.keys())

                    existing_items = UEInspectionItem.objects.filter(Item__in=items_in_excel).only('id', 'Item')

                    item_map = {item.Item: item for item in existing_items}

                    missing_items = [item for item in items_in_excel if item not in item_map]

                    for missing in missing_items:
                        data_dict.pop(missing, None)

                    if not data_dict:
                        return JsonResponse({'success': False, 'message': 'Excel中的所有Item在系统中均不存在'})

                    # ---------- 5. 获取该批次下现有评分记录 ----------

                    existing_records = UEScoreRecord.objects.filter(

                        batch=batch,

                        inspection_item__in=item_map.values()

                    ).select_related('inspection_item')

                    record_map = {record.inspection_item.Item: record for record in existing_records}

                    # ---------- 6. 准备新增/更新（完全覆盖）----------

                    to_create = []

                    to_update = []

                    for item_code, sv in data_dict.items():

                        inspection_item = item_map.get(item_code)

                        if not inspection_item:
                            continue

                        if item_code in record_map:

                            record = record_map[item_code]

                            for db_field, new_val in sv.items():
                                setattr(record, db_field, new_val)  # 直接覆盖

                            record.scorer = user_info

                            to_update.append(record)

                        else:

                            to_create.append(

                                UEScoreRecord(

                                    batch=batch,

                                    inspection_item=inspection_item,

                                    scorer=user_info,

                                    **sv

                                )

                            )

                    # ---------- 7. 执行数据库操作 ----------

                    created_count = 0

                    updated_count = 0

                    with transaction.atomic():

                        if to_create:
                            created_objs = UEScoreRecord.objects.bulk_create(to_create, batch_size=500)

                            created_count = len(created_objs)

                        if to_update:

                            for record in to_update:
                                record.save()

                            updated_count = len(to_update)

                    # ---------- 8. 返回结果 ----------

                    message = f'成功处理 {len(data_dict)} 条记录'

                    if created_count:
                        message += f'，新增 {created_count} 条'

                    if updated_count:
                        message += f'，更新 {updated_count} 条'

                    if missing_items:
                        message += f'，忽略不存在的Item: {len(missing_items)} 个'

                    errors = []

                    if missing_items:
                        errors.append(
                            f'Item不存在: {", ".join(missing_items[:5])}' + ('...' if len(missing_items) > 5 else ''))

                    return JsonResponse({

                        'success': True,

                        'message': message,

                        'errors': errors

                    })


                except UEBatch.DoesNotExist:

                    return JsonResponse({'success': False, 'message': '批次不存在'})

                except Exception as e:

                    traceback.print_exc()

                    return JsonResponse({'success': False, 'message': f'Excel处理失败: {str(e)}'})

        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': f'服务器错误: {str(e)}'})

    # GET请求 - 渲染页面
    # 获取Function选项
    function_choices = UEInspectionItem.CATEGORY_CHOICES

    return render(request, 'UElist/UE_ProjectResult.html', {
        'Skin': Skin,
        'weizhi': weizhi,
        'function_choices': function_choices,
    })