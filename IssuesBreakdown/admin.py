from django.contrib import admin

# Register your models here.
from .models import IssuesBreakdown

@admin.register(IssuesBreakdown)
class IssuesBreakdownAdmin(admin.ModelAdmin):

    list_display = (
        'Customer', 'Project', 'FFRT_Entry_unclose_issue', 'SIT_Exit_unclose_issue', 'first_FFRT', 'second_FFRT', 'third_FFRT', 'fourth_FFRT', 'fifth_FFRT',
        'sixth_FFRT', 'issue_def', 'Remark', 'FFRT', 'Defect_ID', 'Title', 'Create_date', 'Update_date', 'Status',
        'Severity', 'Category', 'Component', 'BIOS_KBC', 'Comments', 'Author', 'Assign_to', 'Description', 'Reproduce_steps', 'Age',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Project',)
    #后台数据列表排序方式
    list_display_links = (
        'Customer', 'Project', 'FFRT_Entry_unclose_issue', 'SIT_Exit_unclose_issue', 'first_FFRT', 'second_FFRT', 'third_FFRT', 'fourth_FFRT', 'fifth_FFRT',
        'sixth_FFRT', 'issue_def', 'Remark', 'FFRT', 'Defect_ID', 'Title', 'Create_date', 'Update_date', 'Status',
        'Severity', 'Category', 'Component', 'BIOS_KBC', 'Comments', 'Author', 'Assign_to', 'Description', 'Reproduce_steps', 'Age',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Customer',
        'Project',
        'FFRT',
        'issue_def',
        'Defect_ID',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Customer', 'Project', 'FFRT', 'issue_def', 'Defect_ID',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选