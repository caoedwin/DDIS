from django.contrib import admin

# Register your models here.
# from TestPlanSW.models import TestItemSW,TestProjectSW,TestPlanSW,RetestItemSW, FFRTByRD
# from extraadminfilters.filters import UnionFieldListFilter
# @admin.register(TestPlanSW)
# class TestPlanSWAdmin(admin.ModelAdmin):
#     # fieldsets = (
#     #     (None, {
#     #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
#     #     }),
#     #     # ('Advanced options',{
#     #     #     'classes': ('collapse',),
#     #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
#     #     # }),
#     # )
#     list_display = ( 'Projectinfo', 'Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',
#                      'Version','ReleaseDate','Owner','Priority','TDMSTotalTime','BaseTime','TDMSUnattendedTime',
#                      'BaseAotomationTime1SKU','Chramshell','ConvertibaleNBMode','ConvertibaleYogaPadMode',
#                      'DetachablePadMode','DetachableWDockmode','PhaseFVT','PhaseSIT','PhaseFFRT','Coverage', 'Items','editor', 'edit_time')
#     # 列表里显示想要显示的字段
#     list_per_page = 500
#     # 满50条数据就自动分页
#     ordering = ('-edit_time',)
#     #后台数据列表排序方式
#     list_display_links = ('Items', 'Projectinfo', 'editor', 'edit_time')
#     # 设置哪些字段可以点击进入编辑界面
#     # list_editable = ('Object',)
#     # 筛选器
#     list_filter = ('Projectinfo', 'Customer','Phase', ('Category2',UnionFieldListFilter))  # 过滤器
#     # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
#     search_fields = ('Projectinfo__Project', 'Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',
#                      'Version','ReleaseDate','Owner','Priority','TDMSTotalTime','BaseTime','TDMSUnattendedTime',
#                      'BaseAotomationTime1SKU','Chramshell','ConvertibaleNBMode','ConvertibaleYogaPadMode',
#                      'DetachablePadMode','DetachableWDockmode','PhaseFVT','PhaseSIT','PhaseFFRT','Coverage', 'editor', 'edit_time')  # 搜索字段
#     # date_hierarchy = 'Start_time'  # 详细时间分层筛选
