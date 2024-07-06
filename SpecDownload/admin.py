from django.contrib import admin
from .models import SpecDownload, files_SpecD
# Register your models here.
# admin.site.register(files_SpecD)
@admin.register(files_SpecD)
class files_SpecDAdmin(admin.ModelAdmin):
    list_display = ('single', 'files',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-single',)
    # 后台数据列表排序方式
    list_display_links = ('single', 'files',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
                    'single',
                    # ('Product', UnionFieldListFilter),
                  )  # 过滤器
    search_fields = ('single',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
@admin.register(SpecDownload)
class SpecDownloadAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Category', 'Functionn', "Case_name", "Version", "editor", "edit_time")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    # 后台数据列表排序方式
    list_display_links = ('Customer', 'Category', 'Functionn', "Case_name", "Version", "editor", "edit_time")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
                    'Customer',
                    # ('Product', UnionFieldListFilter),
                   'Category',
                   'Functionn',)  # 过滤器
    search_fields = ('Customer', 'Category', 'Functionn',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
    filter_horizontal = ('files_Spec',)