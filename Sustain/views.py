import json
import datetime
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Sum, Case, When, Value, IntegerField
from django.db.models.functions import Trim
from app01.models import UserInfo
from .models import SustainTask, SustainTestDetail


# ========== 辅助函数（保持不变）==========
def get_user_by_account(account):
    if not account:
        return None
    return UserInfo.objects.filter(account=account).first()


def get_user_role_by_account(account):
    user = get_user_by_account(account)
    if not user:
        return 'anonymous'
    if hasattr(user, 'is_superuser') and user.is_superuser:
        return 'admin'
    roles = user.role.all()
    for role in roles:
        if role.name in ['admin', 'DQA_C38_Sust_admin']:
            return 'admin'
    return 'normal'


def get_user_projects_by_account(account):
    user = get_user_by_account(account)
    if not user:
        return set()
    role = get_user_role_by_account(account)
    if role == 'admin':
        return None
    from CQM.models import CQMProject
    projects = CQMProject.objects.filter(owner=user).values_list('Project', flat=True)
    return set(projects)


def can_edit_task_by_account(account, task):
    role = get_user_role_by_account(account)
    if role == 'admin':
        return True
    user_projects = get_user_projects_by_account(account)
    if user_projects is None:
        return True
    return task.project_code in user_projects


# ========== 页面渲染 ==========
@csrf_exempt
def sustain_edit(request):
    account = request.session.get('account')
    user_role = get_user_role_by_account(account) if account else 'anonymous'
    user_projects = list(get_user_projects_by_account(account)) if account and get_user_projects_by_account(
        account) is not None else []
    return render(request, 'Sustain/edit.html', {
        'user_role': user_role,
        'user_projects': user_projects,
    })


@csrf_exempt
def sustain_summary(request):
    return render(request, 'Sustain/summary.html')


# ========== API 接口 ==========
@csrf_exempt
def get_customers(request):
    customers = SustainTask.objects.values_list('customer', flat=True).distinct().order_by('customer')
    return JsonResponse(list(customers), safe=False)


@csrf_exempt
def get_projects_by_customer(request):
    customer = request.GET.get('customer')
    if not customer:
        return JsonResponse([], safe=False)
    projects = SustainTask.objects.filter(customer=customer).values_list('project_code', flat=True).distinct().order_by(
        'project_code')
    return JsonResponse(list(projects), safe=False)


@csrf_exempt
def search_tasks(request):
    account = request.session.get('account')
    customer = request.GET.get('customer')
    project_code = request.GET.get('project_code')

    qs = SustainTask.objects.all()
    if customer:
        qs = qs.filter(customer=customer)
    if project_code:
        qs = qs.filter(project_code=project_code)

    role = get_user_role_by_account(account)
    if role != 'admin':
        my_projects = get_user_projects_by_account(account)
        if my_projects is not None:
            qs = qs.filter(project_code__in=my_projects)

    data = []
    for task in qs:
        details = list(task.test_details.all().values(
            'id', 'test_stage', 'test_status', 'test_category', 'category_info',
            'test_version', 'test_condition', 'driver_cut_in_format', 'issue_link',
            'test_resource', 'actual_workload', 'leverage_workload', 'test_team',
            'test_owner', 'test_start', 'test_end', 'working_day', 'change_list', 'remark'
        ))
        # 格式化日期字段
        for d in details:
            if d.get('test_start'):
                d['test_start'] = d['test_start'].strftime('%Y-%m-%d') if hasattr(d['test_start'], 'strftime') else d[
                    'test_start']
            if d.get('test_end'):
                d['test_end'] = d['test_end'].strftime('%Y-%m-%d') if hasattr(d['test_end'], 'strftime') else d[
                    'test_end']

        data.append({
            'id': task.id,
            'task_no': task.task_no,
            'year': task.year,
            'month': task.month,
            'customer': task.customer,
            'series': task.series,
            'project_code': task.project_code,
            'project_name': task.project_name,
            'mp_date': task.mp_date.strftime('%Y-%m-%d') if task.mp_date else '',
            'eop_or_not': task.eop_or_not,
            'eop_date': task.eop_date.strftime('%Y-%m-%d') if task.eop_date else '',
            'eos_date': task.eos_date.strftime('%Y-%m-%d') if task.eos_date else '',
            'project_status': task.project_status,
            'mp_year': task.mp_year,
            'eop_year': task.eop_year,
            'eos_year': task.eos_year,
            'leverage_project': task.leverage_project,
            'test_units_status': task.test_units_status,
            'unit_qty': task.unit_qty,
            'total_test_resource': str(task.total_test_resource),
            'total_actual_workload': str(task.total_actual_workload),
            'total_leverage_workload': str(task.total_leverage_workload),
            'final_test_status': task.final_test_status,
            'task_closure_date': task.task_closure_date.strftime('%Y-%m-%d') if task.task_closure_date else '',
            'task_leading_time': task.task_leading_time,
            'total_planning_workload': str(task.total_planning_workload),
            'total_waste_time': str(task.total_waste_time),
            'details': details,
        })
    return JsonResponse({'data': data})


@csrf_exempt
def save_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    data = json.loads(request.body)
    task_id = data.get('id')
    if task_id:
        old_task = SustainTask.objects.filter(id=task_id).first()
        if old_task and not can_edit_task_by_account(account, old_task):
            return JsonResponse({'error': '无权限编辑此任务'}, status=403)

    # 处理日期字段
    def parse_date(val):
        if not val:
            return None
        if isinstance(val, str):
            return val if val else None
        return val

    task, created = SustainTask.objects.update_or_create(
        id=task_id,
        defaults={
            'task_no': data['task_no'],
            'year': data['year'],
            'month': data['month'],
            'customer': data['customer'],
            'series': data.get('series', ''),
            'project_code': data['project_code'],
            'project_name': data.get('project_name', ''),
            'mp_date': parse_date(data.get('mp_date')),
            'eop_or_not': data.get('eop_or_not', ''),
            'eop_date': parse_date(data.get('eop_date')),
            'eos_date': parse_date(data.get('eos_date')),
            'project_status': data.get('project_status', ''),
            'mp_year': data.get('mp_year', ''),
            'eop_year': data.get('eop_year', ''),
            'eos_year': data.get('eos_year', ''),
            'leverage_project': data.get('leverage_project', ''),
            'test_units_status': data.get('test_units_status', ''),
            'unit_qty': int(data.get('unit_qty', 0)),
            'total_test_resource': float(data.get('total_test_resource', 0)),
            'total_actual_workload': float(data.get('total_actual_workload', 0)),
            'total_leverage_workload': float(data.get('total_leverage_workload', 0)),
            'final_test_status': data.get('final_test_status', ''),
            'task_closure_date': parse_date(data.get('task_closure_date')),
            'task_leading_time': int(data.get('task_leading_time', 0)),
            'total_planning_workload': float(data.get('total_planning_workload', 0)),
            'total_waste_time': float(data.get('total_waste_time', 0)),
        }
    )

    if not created:
        task.test_details.all().delete()

    for detail in data.get('details', []):
        SustainTestDetail.objects.create(
            task=task,
            test_stage=detail.get('test_stage', ''),
            test_status=detail.get('test_status', ''),
            test_category=detail.get('test_category', ''),
            category_info=detail.get('category_info', ''),
            test_version=detail.get('test_version', ''),
            test_condition=detail.get('test_condition', ''),
            driver_cut_in_format=detail.get('driver_cut_in_format', ''),
            issue_link=detail.get('issue_link', ''),
            test_resource=float(detail.get('test_resource', 0)),
            actual_workload=float(detail.get('actual_workload', 0)),
            leverage_workload=float(detail.get('leverage_workload', 0)),
            test_team=detail.get('test_team', ''),
            test_owner=detail.get('test_owner', ''),
            test_start=parse_date(detail.get('test_start')),
            test_end=parse_date(detail.get('test_end')),
            working_day=int(detail.get('working_day', 0)),
            change_list=detail.get('change_list', ''),
            remark=detail.get('remark', ''),
        )
    return JsonResponse({'success': True, 'id': task.id})


@csrf_exempt
def delete_task(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    # 从 JSON body 中获取 id
    try:
        data = json.loads(request.body)
        task_id = data.get('id')
    except Exception:
        return JsonResponse({'error': '无效的请求数据'}, status=400)

    task = SustainTask.objects.filter(id=task_id).first()
    if not task:
        return JsonResponse({'error': '任务不存在'}, status=404)
    if not can_edit_task_by_account(account, task):
        return JsonResponse({'error': '无权限删除'}, status=403)
    task.delete()
    return JsonResponse({'success': True})

@csrf_exempt
def batch_delete_tasks(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)

    data = json.loads(request.body)
    task_ids = data.get('ids', [])
    if not task_ids:
        return JsonResponse({'error': '未选择任何任务'}, status=400)

    tasks = SustainTask.objects.filter(id__in=task_ids)
    deleted_count = 0
    errors = []
    for task in tasks:
        if can_edit_task_by_account(account, task):
            task.delete()
            deleted_count += 1
        else:
            errors.append(f'无权限删除任务 {task.task_no}')

    return JsonResponse({
        'success': True,
        'deleted_count': deleted_count,
        'errors': errors
    })

# Excel 上传并保存
@csrf_exempt
def upload_excel(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    account = request.session.get('account')
    if not account:
        return JsonResponse({'error': '请先登录'}, status=401)
    if get_user_role_by_account(account) != 'admin':
        return JsonResponse({'error': '仅管理员可上传Excel'}, status=403)

    excel_file = request.FILES.get('file')
    if not excel_file:
        return JsonResponse({'error': '未选择文件'}, status=400)

    try:
        xl = pd.ExcelFile(excel_file)
        if 'SW Sustain Tracking' not in xl.sheet_names:
            return JsonResponse({'error': 'Excel 中未找到名为 "SW Sustain Tracking" 的工作表'}, status=400)
        df_raw = pd.read_excel(excel_file, sheet_name='SW Sustain Tracking', header=None)
    except Exception as e:
        return JsonResponse({'error': f'读取Excel失败: {str(e)}'}, status=400)

    if df_raw.empty:
        return JsonResponse({'error': 'Excel 工作表为空'}, status=400)

    rows = df_raw.fillna('').values.tolist()

    # 必需列名（用于定位表头行，使用包含关系）
    required_headers = [
        'Task No', 'Year', 'Month', 'Customer', 'Series', 'Project Code', 'Project Name',
        'MP Date', 'EOP Or Not', 'EOP Date', 'EOS Date', 'Project Status', 'MP Year',
        'EOP Year', 'EOS Year', 'Leverage Project', 'Test Units status', 'Unit_Qty',
        'Total Test Resource'
    ]

    header_row_idx = None
    header_cells = None
    for i, row in enumerate(rows):
        row_str = [str(cell).strip() for cell in row if cell]
        # 只要该行包含所有必需的列名（部分匹配）就认为是表头行
        if all(any(h in cell for cell in row_str) for h in required_headers):
            header_row_idx = i
            header_cells = [str(cell).strip() for cell in row]
            break

    if header_row_idx is None:
        return JsonResponse({'error': '未找到包含必需列名的表头行，请检查 Excel 文件格式'}, status=400)

    # 基础列映射
    base_field_map = {
        'Task No': 'task_no', 'Year': 'year', 'Month': 'month', 'Customer': 'customer',
        'Series': 'series', 'Project Code': 'project_code', 'Project Name': 'project_name',
        'MP Date': 'mp_date', 'EOP Or Not': 'eop_or_not', 'EOP Date': 'eop_date',
        'EOS Date': 'eos_date', 'Project Status': 'project_status', 'MP Year': 'mp_year',
        'EOP Year': 'eop_year', 'EOS Year': 'eos_year', 'Leverage Project': 'leverage_project',
        'Test Units status': 'test_units_status', 'Unit_Qty': 'unit_qty',
        'Total Test Resource': 'total_test_resource',
        'Total Actual Workload(Hrs)': 'total_actual_workload',
        'Total Leverage Workload(Hrs)': 'total_leverage_workload',
        'Final Test Status': 'final_test_status', 'Task Closure Date': 'task_closure_date',
        'Task Leading Time (Days)': 'task_leading_time',
        'Total Planning Workload(Hrs)': 'total_planning_workload',
        'Total waste time (Hrs)': 'total_waste_time',
    }

    # 建立列名到索引的映射（使用包含匹配）
    col_positions = {}
    for idx, cell in enumerate(header_cells):
        for col_name in base_field_map.keys():
            if col_name in cell:   # 关键修改：包含匹配，例如 "Test Units status" 能匹配到包含该字符串的单元格
                col_positions[col_name] = idx
                break

    # 检查必需的几个关键列是否存在
    required_present = ['Task No', 'Year', 'Month', 'Customer', 'Project Code']
    missing = [c for c in required_present if c not in col_positions]
    if missing:
        return JsonResponse({'error': f'表头行缺少必需列: {", ".join(missing)}'}, status=400)

    # 测试详情字段映射
    detail_field_map = {
        'Test Stage': 'test_stage',
        'Test Status': 'test_status',
        'Test Category': 'test_category',
        'Category Info': 'category_info',
        'Test Version': 'test_version',
        'Test Condition': 'test_condition',
        'Driver cut in format': 'driver_cut_in_format',
        'Issue Link': 'issue_link',
        'Test Resource': 'test_resource',
        'Actual Workload(Hrs)': 'actual_workload',
        'Leverage Workload(Hrs)': 'leverage_workload',
        'Test Team': 'test_team',
        'Test_Owner': 'test_owner',
        'Test_Start': 'test_start',
        'Test_End': 'test_end',
        'Working Day': 'working_day',
        'Change list': 'change_list',
        'Remark': 'remark',
    }

    # 查找所有包含 'Test Stage' 的列（用于分组）
    test_stage_indices = [idx for idx, cell in enumerate(header_cells) if 'Test Stage' in cell]
    if not test_stage_indices:
        return JsonResponse({'error': '未找到包含 "Test Stage" 的列，无法解析测试详情'}, status=400)

    # 构建测试阶段组（每个组包含阶段名、起始列和结束列）
    groups = []
    prev_row_cells = rows[header_row_idx - 1] if header_row_idx > 0 else []
    for i, start_idx in enumerate(test_stage_indices):
        end_idx = test_stage_indices[i+1] - 1 if i+1 < len(test_stage_indices) else len(header_cells) - 1
        group_name = f'Stage_{i+1}'
        if start_idx < len(prev_row_cells):
            raw_name = str(prev_row_cells[start_idx]).strip()
            if 'New Test' in raw_name:
                group_name = 'New Test'
            elif 'Regression1' in raw_name:
                group_name = 'Regression1'
            elif 'Regression2' in raw_name:
                group_name = 'Regression2'
            elif 'Regression3' in raw_name:
                group_name = 'Regression3'
            elif 'Regression4' in raw_name:
                group_name = 'Regression4'
            elif 'Regression5' in raw_name:
                group_name = 'Regression5'
            else:
                group_name = raw_name if raw_name else group_name
        groups.append({'name': group_name, 'start': start_idx, 'end': end_idx})

    # 数据行从表头下一行开始
    data_rows = rows[header_row_idx + 1:]

    # ---------- 辅助函数 ----------
    def clean_cell(val):
        if val == '' or pd.isna(val):
            return ''
        s = str(val).strip()
        if any(kw in s for kw in ['公式', '需編輯', '下拉菜单选择', '需編輯，下拉菜單選擇', '无需编辑', '無需編輯']):
            return ''
        return s

    def parse_date(val):
        s = clean_cell(val)
        if not s:
            return None
        if ' ' in s:
            s = s.split(' ')[0]
        for fmt in ('%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y'):
            try:
                dt = datetime.datetime.strptime(s, fmt)
                return dt.strftime('%Y-%m-%d')
            except:
                continue
        if isinstance(val, (pd.Timestamp, datetime.datetime)):
            return val.strftime('%Y-%m-%d')
        return None

    def to_int(val, default=0):
        s = clean_cell(val)
        if s == '':
            return default
        try:
            return int(float(s))
        except:
            return default

    def to_float(val, default=0.0):
        s = clean_cell(val)
        if s == '':
            return default
        try:
            return float(s)
        except:
            return default

    def to_str(val, default='', max_len=None):
        s = clean_cell(val)
        if s == '':
            return default
        if max_len and len(s) > max_len:
            s = s[:max_len]
        return s

    def extract_year(task_no):
        import re
        match = re.search(r'(\d{6})', task_no)
        if match:
            return int(match.group(1)[:4])
        match = re.search(r'(\d{4})', task_no)
        if match:
            return int(match.group(1))
        return None

    valid_months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    errors = []
    success_count = 0

    for row_idx, row in enumerate(data_rows):
        # 跳过全空行
        if all(cell == '' or pd.isna(cell) for cell in row):
            continue

        task_no_col = col_positions.get('Task No')
        if task_no_col is None or task_no_col >= len(row):
            continue
        task_no_raw = row[task_no_col]
        task_no_clean = to_str(task_no_raw)
        if not task_no_clean:
            continue

        try:
            task_data = {}
            for col_name, model_field in base_field_map.items():
                if col_name not in col_positions:
                    continue
                col_idx = col_positions[col_name]
                raw_val = row[col_idx] if col_idx < len(row) else ''
                if model_field == 'year':
                    task_data[model_field] = to_int(raw_val, 0)
                elif model_field in ('unit_qty', 'task_leading_time'):
                    task_data[model_field] = to_int(raw_val, 0)
                elif model_field in ('total_test_resource', 'total_actual_workload',
                                     'total_leverage_workload', 'total_planning_workload',
                                     'total_waste_time'):
                    task_data[model_field] = to_float(raw_val, 0.0)
                elif model_field in ('mp_date', 'eop_date', 'eos_date', 'task_closure_date'):
                    task_data[model_field] = parse_date(raw_val)
                elif model_field == 'leverage_project':
                    task_data[model_field] = to_str(raw_val, '', max_len=10)
                else:
                    task_data[model_field] = to_str(raw_val, '')

            task_no = task_data.get('task_no')
            if not task_no:
                errors.append(f'第{row_idx+header_row_idx+2}行: Task No 为空')
                continue

            year_val = task_data.get('year')
            if not year_val:
                extracted = extract_year(task_no)
                if extracted:
                    task_data['year'] = extracted
                else:
                    errors.append(f'第{row_idx+header_row_idx+2}行: Year 不能为空，且无法从 Task No 提取年份')
                    continue

            month_val = task_data.get('month')
            if not month_val or month_val not in valid_months:
                errors.append(f'第{row_idx+header_row_idx+2}行: Month 无效或为空')
                continue

            if not task_data.get('customer'):
                errors.append(f'第{row_idx+header_row_idx+2}行: Customer 不能为空')
                continue
            if not task_data.get('project_code'):
                errors.append(f'第{row_idx+header_row_idx+2}行: Project Code 不能为空')
                continue

            task_obj, _ = SustainTask.objects.update_or_create(
                task_no=task_no,
                defaults=task_data
            )
            task_obj.test_details.all().delete()

            for group in groups:
                detail = {'test_stage': group['name']}
                for col in range(group['start'], min(group['end']+1, len(row))):
                    sub_name = header_cells[col] if col < len(header_cells) else ''
                    if not sub_name:
                        continue
                    # 查找对应的模型字段（因为 sub_name 可能包含换行，所以也要用包含匹配）
                    model_field = None
                    for key in detail_field_map.keys():
                        if key in sub_name:
                            model_field = detail_field_map[key]
                            break
                    if not model_field:
                        continue
                    raw_val = row[col] if col < len(row) else ''
                    if model_field in ('test_resource', 'actual_workload', 'leverage_workload'):
                        val = to_float(raw_val, 0.0)
                    elif model_field == 'working_day':
                        val = to_int(raw_val, 0)
                    elif model_field in ('test_start', 'test_end'):
                        val = parse_date(raw_val)
                    elif model_field == 'test_version':
                        val = to_str(raw_val, '', max_len=100)
                    else:
                        val = to_str(raw_val, '')
                    detail[model_field] = val

                if len(detail) <= 1:
                    continue
                if not detail.get('test_status') and not detail.get('test_category') and not detail.get('test_version'):
                    continue

                SustainTestDetail.objects.create(
                    task=task_obj,
                    test_stage=detail.get('test_stage', ''),
                    test_status=detail.get('test_status', ''),
                    test_category=detail.get('test_category', ''),
                    category_info=detail.get('category_info', ''),
                    test_version=detail.get('test_version', ''),
                    test_condition=detail.get('test_condition', ''),
                    driver_cut_in_format=detail.get('driver_cut_in_format', ''),
                    issue_link=detail.get('issue_link', ''),
                    test_resource=detail.get('test_resource', 0.0),
                    actual_workload=detail.get('actual_workload', 0.0),
                    leverage_workload=detail.get('leverage_workload', 0.0),
                    test_team=detail.get('test_team', ''),
                    test_owner=detail.get('test_owner', ''),
                    test_start=detail.get('test_start'),
                    test_end=detail.get('test_end'),
                    working_day=detail.get('working_day', 0),
                    change_list=detail.get('change_list', ''),
                    remark=detail.get('remark', ''),
                )

            success_count += 1

        except Exception as e:
            import traceback
            traceback.print_exc()
            errors.append(f'第{row_idx+header_row_idx+2}行处理出错: {str(e)}')

    return JsonResponse({'success_count': success_count, 'errors': errors})
@csrf_exempt
def dashboard_data(request):
    year = request.GET.get('year')
    customer = request.GET.get('customer')
    qs = SustainTask.objects.all()
    if year:
        qs = qs.filter(year=year)
    if customer:
        qs = qs.filter(customer=customer)

    customer_stats = qs.values('customer').annotate(
        pass_count=Count(Case(When(final_test_status='Pass', then=1), output_field=IntegerField())),
        conditional_pass_count=Count(Case(When(final_test_status='Conditional Pass', then=1), output_field=IntegerField())),
        fail_count=Count(Case(When(final_test_status='Fail', then=1), output_field=IntegerField())),
        ongoing_count=Count(Case(When(final_test_status__in=['Testing','Pending'], then=1), output_field=IntegerField())),
        planning_count=Count(Case(When(final_test_status='Planning', then=1), output_field=IntegerField())),
    ).order_by('customer')

    customer_table = []
    for item in customer_stats:
        total = item['pass_count'] + item['conditional_pass_count'] + item['fail_count'] + item['ongoing_count'] + item['planning_count']
        customer_table.append({
            'Customer': item['customer'],
            'Pass': item['pass_count'] + item['conditional_pass_count'],
            'Fail': item['fail_count'],
            'Ongoing': item['ongoing_count'],
            'Planning': item['planning_count'],
            'Total': total,
        })

    from django.db.models.functions import ExtractMonth
    month_stats = qs.values('year', 'month').annotate(
        total=Count('id'),
        pass_total=Count(Case(When(final_test_status__in=['Pass','Conditional Pass'], then=1), output_field=IntegerField()))
    ).order_by('year', 'month')
    months = [f"{item['year']}-{item['month']}" for item in month_stats]
    pass_data = [item['pass_total'] for item in month_stats]
    total_data = [item['total'] for item in month_stats]

    project_stats = qs.values('project_code').annotate(
        total=Count('id')
    ).order_by('-total')[:10]

    return JsonResponse({
        'customer_table': customer_table,
        'customer_series': [],
        'month_labels': months,
        'pass_series': {'name': 'Pass/Conditional Pass', 'data': pass_data},
        'total_series': {'name': 'Total Tasks', 'data': total_data},
        'project_top10': list(project_stats),
    })