from django.contrib import admin
from .models import SustainTask, SustainTestDetail


class SustainTestDetailInline(admin.TabularInline):
    model = SustainTestDetail
    extra = 1
    fields = (
        'test_stage', 'test_status', 'test_category', 'category_info',
        'test_version', 'test_condition', 'driver_cut_in_format', 'issue_link',
        'test_resource', 'actual_workload', 'leverage_workload',
        'test_team', 'test_owner', 'test_start', 'test_end',
        'working_day', 'change_list', 'remark'
    )
    raw_id_fields = ('task',)


@admin.register(SustainTask)
class SustainTaskAdmin(admin.ModelAdmin):
    list_display = (
        'task_no', 'year', 'month', 'customer', 'series', 'project_code',
        'final_test_status', 'task_closure_date'
    )
    list_filter = ('year', 'month', 'customer', 'series', 'final_test_status')
    search_fields = ('task_no', 'project_code', 'project_name')
    date_hierarchy = 'mp_date'
    inlines = [SustainTestDetailInline]

    fieldsets = (
        ('基本信息', {
            'fields': (
                'task_no', 'year', 'month', 'customer', 'series',
                'project_code', 'project_name'
            )
        }),
        ('项目里程碑', {
            'fields': (
                'mp_date', 'eop_or_not', 'eop_date', 'eos_date',
                'project_status', 'mp_year', 'eop_year', 'eos_year',
                'leverage_project'
            )
        }),
        ('测试资源', {
            'fields': (
                'test_units_status', 'unit_qty', 'total_test_resource',
                'total_actual_workload', 'total_leverage_workload',
                'final_test_status'
            )
        }),
        ('任务进度', {
            'fields': (
                'task_closure_date', 'task_leading_time',
                'total_planning_workload', 'total_waste_time'
            )
        }),
    )


@admin.register(SustainTestDetail)
class SustainTestDetailAdmin(admin.ModelAdmin):
    list_display = ('task', 'test_stage', 'test_status', 'test_owner', 'test_start', 'test_end')
    list_filter = ('test_stage', 'test_status', 'test_category')
    search_fields = ('task__task_no', 'test_owner', 'change_list')
    raw_id_fields = ('task',)