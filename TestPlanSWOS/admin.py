
from django.contrib import admin
from TestPlanSWOS.models import TestItemSW,TestProjectSW,TestPlanSW,RetestItemSW, FFRTByRD, TestPlanSWAIO, TestProjectSWAIO
from extraadminfilters.filters import UnionFieldListFilter


@admin.register(TestPlanSWAIO)
class TestPlanSWAIOAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ( 'Projectinfo', 'Customer','Phase', 'Category', 'TestTitle', 'Subtesttitle','TestItem','Priority',
                     'ReleaseDate','Owner','AT_Totaltime','AT_AttendTime','AT_UnattendTime',
                     'AT_Automation','DQMS_AttendTime','DQMS_UnattendTime','TestUnitsConfig',
                     'SmartItem','Cusumer','Commercial','SDV','SIT','Coverage', 'editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Projectinfo', 'Customer','Phase', 'Category', 'TestTitle', 'Subtesttitle','TestItem', 'editor', 'edit_time')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Projectinfo',
        # 'Customer',
        # 'Phase',
        ('Customer', UnionFieldListFilter),
        ('Phase', UnionFieldListFilter),
        'Category',
        'TestTitle',
        'Subtesttitle',
        'TestItem',
    )  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Projectinfo__Project', 'Customer','Phase', 'Category', 'TestTitle', 'Subtesttitle','TestItem','Priority','editor', 'edit_time')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestProjectSWAIO)
class TestProjectSWAIOAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    filter_horizontal = ('Owner',)
    list_display = ('Customer', 'Project', 'Phase',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer', 'Project', 'Phase',)  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(FFRTByRD)
class FFRTByRDAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'EC', 'RF', 'EMI', 'ESD', 'HW', 'SW', 'SA', 'SIT', 'Thermal', 'Power', 'SED')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'EC', 'RF', 'EMI', 'ESD', 'HW', 'SW', 'SA', 'SIT', 'Thermal', 'Power', 'SED')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'EC', 'RF', 'EMI', 'ESD', 'HW', 'SW', 'SA', 'SIT', 'Thermal', 'Power', 'SED')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(RetestItemSW)
class RetestItemSWAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Phase', 'ItemNo_d', 'Item_d', 'TestItems', 'Category', 'Category2', 'Projectinfo', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase', 'ItemNo_d', 'Item_d', 'TestItems', 'Category', 'Category2', 'Projectinfo', 'edit_time')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Projectinfo',
        # 'Customer',
        # 'Phase',
        ('Customer', UnionFieldListFilter),
        ('Phase', UnionFieldListFilter),
        'Category2',
    )  # 过滤器 # 过滤器
    search_fields = ('Customer', 'Projectinfo__Project', 'Phase', 'ItemNo_d', 'Item_d', 'TestItems', 'Category', 'Category2', 'edit_time')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestPlanSW)
class TestPlanSWAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ( 'Projectinfo', 'Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',
                     'Version','ReleaseDate','Owner','Priority','TDMSTotalTime','BaseTime','TDMSUnattendedTime',
                     'BaseAotomationTime1SKU','Chramshell','ConvertibaleNBMode','ConvertibaleYogaPadMode',
                     'DetachablePadMode','DetachableWDockmode','PhaseFVT','PhaseSIT','PhaseFFRT','Coverage', 'Items','editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Items', 'Projectinfo', 'editor', 'edit_time')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Projectinfo',
        # 'Customer',
        # 'Phase',
        ('Customer', UnionFieldListFilter),
        ('Phase', UnionFieldListFilter),
        'Category2',
    )  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Projectinfo__Project', 'Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',
                     'Version','ReleaseDate','Owner','Priority','TDMSTotalTime','BaseTime','TDMSUnattendedTime',
                     'BaseAotomationTime1SKU','Chramshell','ConvertibaleNBMode','ConvertibaleYogaPadMode',
                     'DetachablePadMode','DetachableWDockmode','PhaseFVT','PhaseSIT','PhaseFFRT','Coverage', 'editor', 'edit_time')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestProjectSW)
class TestProjectSWAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    filter_horizontal = ('Owner',)
    list_display = ('Customer', 'Project', 'Phase',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer', 'Project', 'Phase',)  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestItemSW)
class TestItemSWAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems', 'Category', 'Category2', 'Version', 'ReleaseDate')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems', 'Category', 'Category2', 'Version', 'ReleaseDate')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',)  # 过滤器
    search_fields = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems','Category','Category2',
                     'Version','ReleaseDate','Owner','Priority','TDMSTotalTime','BaseTime','TDMSUnattendedTime',
                     'BaseAotomationTime1SKU','Chramshell','ConvertibaleNBMode','ConvertibaleYogaPadMode',
                     'DetachablePadMode','DetachableWDockmode','PhaseFVT','PhaseSIT','PhaseFFRT','Coverage')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
