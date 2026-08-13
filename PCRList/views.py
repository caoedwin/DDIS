# PCRList/views.py
import json
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
    """
    content_type = request.content_type or ''
    if 'application/json' in content_type:
        data = json.loads(request.body)
    else:
        data = request.POST.dict()
        if 'attachment_file' in request.FILES:
            data['attachment_file'] = request.FILES['attachment_file']
        for bool_field in ['pm_send_nre_to_sales', 'whether_in_budget', 'in_budget_but_cost_add']:
            if bool_field in data:
                val = data[bool_field]
                if isinstance(val, str):
                    data[bool_field] = val.lower() in ('true', '1', 'yes')
                else:
                    data[bool_field] = bool(val)
        for num_field in ['sample_qty', 'hc_qty', 'hc_days', 'device_fee_usd']:
            if num_field in data:
                try:
                    data[num_field] = float(data[num_field])
                except (ValueError, TypeError):
                    data[num_field] = 0.0
        for date_field in ['receive_date', 'execution_start', 'execution_end']:
            if date_field in data and not data[date_field]:
                data[date_field] = None
    return data


def pcr_list_page(request):
    return render(request, 'PCRList/pcr_list.html')


def check_permission(user, compalproject):
    if isinstance(user, str):
        try:
            user = UserInfo.objects.get(account=user)
        except UserInfo.DoesNotExist:
            return False
    if getattr(user, 'is_staff', False) or getattr(user, 'is_SVPuser', False):
        return True
    if user:
        roles = [role.name for role in user.role.all()]
        for role in roles:
            if role == 'admin' or 'DQA_C38_PCR_admin' in role:
                return True
    try:
        cqm_project = CQMProject.objects.get(Project=compalproject)
        return cqm_project.Owner.filter(id=user.id).exists()
    except CQMProject.DoesNotExist:
        return False


@csrf_exempt
@require_http_methods(["POST"])
def pcr_list_api(request):
    onlineuser = request.session.get('account')
    user_info = None
    if onlineuser:
        try:
            user_info = UserInfo.objects.get(account=onlineuser)
        except UserInfo.DoesNotExist:
            pass

    data = json.loads(request.body)
    action = data.get('action', 'list')

    if action == 'options':
        customer_choices = [{'value': code, 'label': label} for code, label in PCR.Customer_CHOICES]
        phase_choices = [{'value': code, 'label': label} for code, label in PCR.PHASE_CHOICES]
        # 独立 Year 字段的去重选项
        year_field_choices = (
            PCR.objects.exclude(year='')
            .values_list('year', flat=True)
            .distinct()
            .order_by('year')
        )
        year_field_choices = [{'value': y, 'label': y} for y in year_field_choices]
        compalprojects = (PCR.objects.filter(Compalproject__isnull=False)
                          .exclude(Compalproject='')
                          .values_list('Compalproject', flat=True)
                          .distinct()
                          .order_by('Compalproject'))
        compalproject_choices = [{'value': proj, 'label': proj} for proj in compalprojects]

        return JsonResponse({
            'action': 'options',
            'customer_choices': customer_choices,
            'phase_choices': phase_choices,
            'year_field_choices': year_field_choices,   # 注意 key 改为 year_field_choices
            'compalproject_choices': compalproject_choices,
        })

    start_date = data.get('start_date')
    end_date = data.get('end_date')
    customer = data.get('customer', '').strip()
    phase = data.get('phase', '').strip()
    # 独立的 year 字段
    year = data.get('year', '').strip()
    compalproject = data.get('compalproject', '').strip()

    page = int(data.get('page', 1))
    page_size = int(data.get('page_size', 20))

    queryset = PCR.objects.all()

    # 日期重叠筛选（保持不变）
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

    # 其他筛选（使用独立的 year 字段）
    if customer:
        queryset = queryset.filter(Customer=customer)
    if phase:
        queryset = queryset.filter(phase=phase)
    if year:
        queryset = queryset.filter(year=year)   # 直接匹配字符串
    if compalproject:
        queryset = queryset.filter(Compalproject__icontains=compalproject)

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
            'year': pcr.year or '',
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
    data = json.loads(request.body)
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    if start_date or end_date:
        base_queryset = PCR.objects.filter(
            execution_start__isnull=False,
            execution_end__isnull=False
        )
        if start_date and end_date:
            base_queryset = base_queryset.filter(
                execution_start__lte=end_date,
                execution_end__gte=start_date
            )
        elif start_date:
            base_queryset = base_queryset.filter(execution_end__gte=start_date)
        elif end_date:
            base_queryset = base_queryset.filter(execution_start__lte=end_date)
    else:
        base_queryset = PCR.objects.all()

    customers = list(base_queryset.values_list('Customer', flat=True).distinct().order_by('Customer'))
    phases = ['NPI', 'INV']

    def aggregate_by_status(qs):
        perform = qs.filter(status='Perform').aggregate(
            sample_qty=Coalesce(Sum('sample_qty'), 0),
            hc_qty=Coalesce(Sum('hc_qty'), 0),
            hc_days=Coalesce(Sum('hc_days'), 0),
            pd=Coalesce(Sum('pd'), 0),
            device_fee_usd=Coalesce(Sum('device_fee_usd'), 0)
        )
        plan = qs.filter(status='Plan').aggregate(
            sample_qty=Coalesce(Sum('sample_qty'), 0),
            hc_qty=Coalesce(Sum('hc_qty'), 0),
            hc_days=Coalesce(Sum('hc_days'), 0),
            pd=Coalesce(Sum('pd'), 0),
            device_fee_usd=Coalesce(Sum('device_fee_usd'), 0)
        )
        ongoing = qs.filter(Q(status='Ongoing') | Q(status='On going')).aggregate(
            sample_qty=Coalesce(Sum('sample_qty'), 0),
            hc_qty=Coalesce(Sum('hc_qty'), 0),
            hc_days=Coalesce(Sum('hc_days'), 0),
            pd=Coalesce(Sum('pd'), 0),
            device_fee_usd=Coalesce(Sum('device_fee_usd'), 0)
        )
        total = {}
        for key in perform.keys():
            total[key] = perform[key] + plan[key] + ongoing[key]
        return {
            'Perform': perform,
            'Plan': plan,
            'Ongoing': ongoing,
            'Total': total
        }

    result = {
        'customers': customers,
        'phases': phases,
        'data': {}
    }

    result['data']['overall'] = aggregate_by_status(base_queryset)

    for cust in customers:
        qs_cust = base_queryset.filter(Customer=cust)
        result['data'][f'customer_{cust}'] = aggregate_by_status(qs_cust)

    for phase in phases:
        qs_phase = base_queryset.filter(phase=phase)
        result['data'][f'phase_{phase}'] = aggregate_by_status(qs_phase)

    for cust in customers:
        for phase in phases:
            qs_comb = base_queryset.filter(Customer=cust, phase=phase)
            result['data'][f'{cust}_{phase}'] = aggregate_by_status(qs_comb)

    return JsonResponse(result)


@csrf_exempt
@require_http_methods(["POST"])
def pcr_create_api(request):
    try:
        onlineuser = request.session.get('account')
        if not onlineuser:
            return JsonResponse({'success': False, 'message': '用户未登录'}, status=401)
        user_info = UserInfo.objects.get(account=onlineuser)

        data = parse_request_data(request)

        compalproject = data.get('Compalproject', data.get('Project'))
        if not check_permission(user_info, compalproject):
            return JsonResponse({'success': False, 'message': '无权限操作该项目'}, status=403)

        pcr_no = data.get('pcr_no')
        project = data.get('Project')
        pcr_title = data.get('pcr_title')
        if not pcr_no or not project or not pcr_title:
            return JsonResponse({'success': False, 'message': 'PCR No, Project, PCR Title 不能为空'})
        if PCR.objects.filter(pcr_no=pcr_no, Project=project, pcr_title=pcr_title).exists():
            return JsonResponse({'success': False, 'message': 'PCR No+Project+Title 已存在'})

        pcr = PCR.objects.create(
            pcr_no=pcr_no,
            pcr_title=pcr_title,
            Customer=data.get('Customer', 'NB'),
            year=data.get('year', ''),          # 新增
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
    try:
        onlineuser = request.session.get('account')
        if not onlineuser:
            return JsonResponse({'success': False, 'message': '用户未登录'}, status=401)
        user_info = UserInfo.objects.get(account=onlineuser)

        data = parse_request_data(request)

        record_id = data.get('id')
        if not record_id:
            return JsonResponse({'success': False, 'message': '缺少记录 ID'}, status=400)
        pcr = PCR.objects.get(id=record_id)

        if not check_permission(user_info, pcr.Compalproject):
            return JsonResponse({'success': False, 'message': '无权限操作该项目'}, status=403)

        new_pcr_no = data.get('pcr_no', pcr.pcr_no)
        new_project = data.get('Project', pcr.Project)
        new_pcr_title = data.get('pcr_title', pcr.pcr_title)
        if PCR.objects.filter(pcr_no=new_pcr_no, Project=new_project, pcr_title=new_pcr_title).exclude(id=record_id).exists():
            return JsonResponse({'success': False, 'message': 'PCR No+Project+Title 已存在'})

        for field in ['pcr_no', 'pcr_title', 'Customer', 'year', 'Project', 'Compalproject',
                      'phase', 'category', 'receive_date', 'status', 'sample_qty', 'hc_qty',
                      'hc_days', 'device_fee_usd', 'pm_send_nre_to_sales', 'execution_start',
                      'execution_end', 'whether_in_budget', 'in_budget_but_cost_add', 'remark']:
            if field in data:
                setattr(pcr, field, data[field])

        if data.get('attachment_clear'):
            if pcr.attachment:
                pcr.attachment.delete(save=False)
            pcr.attachment = None
        elif 'attachment_file' in data:
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

    rows = []
    for row in ws.iter_rows(values_only=True):
        if any(cell is not None and str(cell).strip() != '' for cell in row):
            rows.append(row)

    if len(rows) < 2:
        return JsonResponse({'success': False, 'message': '数据行数不足'})

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

    main_headers = [str(cell).strip() if cell else '' for cell in rows[header_row_idx]]
    sub_headers = [str(cell).strip() if cell else '' for cell in rows[subheader_row_idx]] \
                  if subheader_row_idx is not None else [''] * len(main_headers)

    field_mapping = {
        'pcr_no': ['PCR No', 'PCR No.', 'PCR Number'],
        'pcr_title': ['PCR Title', 'Title', 'PCR标题'],
        'Customer': ['Customer', '客户'],
        'year': ['Year', '年份'],           # 新增 Year 映射
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
        sub_lower = sub.lower()
        if 'sample' in sub_lower and 'sample_qty' not in col_index_map:
            col_index_map['sample_qty'] = idx
        elif 'hc qty' in sub_lower and 'hc_qty' not in col_index_map:
            col_index_map['hc_qty'] = idx
        elif 'hc days' in sub_lower and 'hc_days' not in col_index_map:
            col_index_map['hc_days'] = idx
        elif 'device fee' in sub_lower and 'device_fee_usd' not in col_index_map:
            col_index_map['device_fee_usd'] = idx

    col_index_map = {k: int(v) for k, v in col_index_map.items()}

    required_db_fields = ['pcr_no', 'pcr_title', 'Compalproject', 'Project', 'Customer', 'phase', 'status']
    missing = [f for f in required_db_fields if f not in col_index_map]
    if missing:
        return JsonResponse({'success': False, 'message': f'缺少必要的列映射: {missing}，请检查表头'})

    start_row = (subheader_row_idx if subheader_row_idx is not None else header_row_idx) + 1
    while start_row < len(rows):
        row = rows[start_row]
        pcr_col = col_index_map.get('pcr_no')
        if pcr_col is not None and pcr_col < len(row) and row[pcr_col] and str(row[pcr_col]).strip():
            break
        start_row += 1

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

            if PCR.objects.filter(pcr_no=pcr_no, Project=project, pcr_title=pcr_title).exists():
                duplicates.append(f"第{idx+1}行: {pcr_no} - {project} - {pcr_title}")
                continue

            compal_col = col_index_map.get('Compalproject', -1)
            compalproject = ''
            if compal_col != -1 and compal_col < len(row):
                compalproject = truncate_str(row[compal_col], 50)
            else:
                compalproject = project

            if not check_permission(user_info, compalproject):
                errors.append(f"第{idx+1}行: 无权限操作机种 {compalproject}")
                continue

            category_val = ''
            if 'category' in col_index_map and col_index_map['category'] < len(row):
                category_val = truncate_str(row[col_index_map['category']], 50)

            remark_val = ''
            if 'remark' in col_index_map and col_index_map['remark'] < len(row):
                remark_val = truncate_str(row[col_index_map['remark']], 500)

            receive_date_val = None
            if 'receive_date' in col_index_map and col_index_map['receive_date'] < len(row):
                receive_date_val = parse_date(row[col_index_map['receive_date']])

            # 读取 Year 字段
            year_val = ''
            if 'year' in col_index_map and col_index_map['year'] < len(row):
                year_val = truncate_str(row[col_index_map['year']], 10)

            create_data = {
                'pcr_no': pcr_no,
                'pcr_title': pcr_title,
                'Customer': row[col_index_map['Customer']] if col_index_map['Customer'] < len(row) else 'NB',
                'year': year_val,   # 新增
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