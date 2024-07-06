from django.contrib import admin
from .models import ABODriverList_M, ABOToolList_M
# Register your models here.
@admin.register(ABOToolList_M)

class ABOToolList_MAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Phase0', 'Vendor', 'Version', 'ToolName', 'TestCase', 'editor', 'edit_time',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase0', 'Vendor', 'Version', 'ToolName', 'TestCase', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase0', 'Vendor', 'Version', 'ToolName', 'TestCase', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(ABODriverList_M)
class ABODriverList_MAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Phase0', 'Name', 'Function', 'Vendor', 'Version', 'Image', 'Driver', 'editor', 'edit_time', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase0', 'Name', 'Function', 'Vendor', 'Version', 'Image', 'Driver', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase0', 'Name', 'Function', 'Vendor', 'Version', 'Image', 'Driver', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选