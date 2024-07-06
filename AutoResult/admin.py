from django.contrib import admin
from .models import AutoItems, AutoProject, AutoResult
# Register your models here.
# admin.site.register(SeriesInfo)
# admin.site.register(CategoryInfo)
@admin.register(AutoItems)
class AutoItemsAdmin(admin.ModelAdmin):
    list_display = ('Number', 'Customer', 'ValueIf', "BaseIncome", "CaseID", "CaseName", "Item", "Owner", "Status",
                    "FunDescription", "Comment")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Number',)
    # 后台数据列表排序方式
    list_display_links = (
    'Number', 'Customer', 'ValueIf', "BaseIncome", "CaseID", "CaseName", "Item", "Owner", "Status",
                    "FunDescription", "Comment")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
        'Customer',
        # ('Product', UnionFieldListFilter),
        )  # 过滤器
    search_fields = ('Customer',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(AutoProject)
class AutoProjectAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Project', 'Year',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Project',)
    # 后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Year',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
        'Project',
        # ('Product', UnionFieldListFilter),
        )  # 过滤器
    search_fields = ('Project',)  # 搜索字段
    filter_horizontal = ('Owner',)
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(AutoResult)
class AutoResultAdmin(admin.ModelAdmin):
    list_display = ('Number', 'Customer', 'ValueIf', "BaseIncome", "CaseID", "CaseName", "Item", "Owner",
                    "FunDescription", "Comment", "AutoItem", "Projectinfo", "ProjectinfoCQM", "ProjectName", "Year", "Cycles", "Comments",
                    "editor", "edit_time")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    # 后台数据列表排序方式
    list_display_links = ('Number', 'Customer', 'ValueIf', "BaseIncome", "CaseID", "CaseName", "Item", "Owner",
                    "FunDescription", "Comment", "AutoItem", "Projectinfo",  "ProjectName", "Year", "Cycles", "Comments",
                    "editor", "edit_time")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
        'Number',
        'Projectinfo',
        'ProjectinfoCQM',
        # ('Product', UnionFieldListFilter),
        )  # 过滤器
    search_fields = ('Customer',)  # 搜索字段
    # raw_id_fields = ('Projectinfo',)
    # date_hierarchy = "Year" #The value of 'date_hierarchy' must be a DateField or DateTimeField.
    # filter_horizontal = ('role',)
    # date_hierarchy = 'edit_time'  # 详细时间分层筛选