from django.contrib import admin
from .models import UserInfo, Role, Permission, Menu, lesson_learn, Imgs, files,ProjectinfoinDCT
from LessonProjectME.models import lessonlearn_Project, TestProjectLL
from CDM.models import CDM
from Bouncing.models import Bouncing_M,files_BM
from Package.models import Package_M,files_PM
from TestPlanME.models import TestItemME,TestProjectME,TestPlanME,KeypartAIO,KeypartC38NB
from TestPlanSW.models import TestItemSW,TestProjectSW,TestPlanSW,RetestItemSW, FFRTByRD, TestPlanSWAIO, TestProjectSWAIO
from DriverTool.models import DriverList_M,ToolList_M
from MQM.models import MQM
from CQM.models import CQM, CQMProject, CQM_history
from QIL.models import QIL_M, QIL_Project, files_QIL
from extraadminfilters.filters import UnionFieldListFilter
from INVGantt.models import INVGantt
# Register your models here.
admin.site.site_url = '/index/'

# admin.site.register(CDM)
# admin.site.register(MQM)
# admin.site.register(RetestItemSW)
# admin.site.register(TestPlanSW)
# admin.site.register(TestProjectSW)
# admin.site.register(TestItemSW)
# admin.site.register(TestPlanME)
# admin.site.register(TestProjectME)
# admin.site.register(TestItemME)
# admin.site.register(lessonlearn_Project)
admin.site.register(files_PM)
admin.site.register(files_BM)
admin.site.register(Imgs)
admin.site.register(files)
admin.site.register(files_QIL)
# admin.site.register(ProjectinfoinDCT)
# admin.site.register(DriverList_M)
# admin.site.register(ToolList_M)

@admin.register(INVGantt)
class INVGanttAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'INV_Number', 'INV_Model', 'Project_Name', "Year", "Unit_Qty", "TP_Kinds", "Qualify_Cycles", "Status", "TP_Cat", "Trial_Run_Type", "TP_Vendor",
                    "TP_Key_Parameter", "Lenovo_TP_PN", "Compal_TP_PN", "Issue_Link", "Remark", "Attend_Time", "ReTest_Attend_Time", "TestOwner", "Month", "Test_Start", "Test_End",
                    "Editor", "Edittime")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-INV_Model',)
    # 后台数据列表排序方式
    list_display_links = ('Customer', 'INV_Number', 'INV_Model', 'Project_Name', "Year", "Unit_Qty", "TP_Kinds", "Qualify_Cycles", "Status", "TP_Cat", "Trial_Run_Type", "TP_Vendor",
                    "TP_Key_Parameter", "Lenovo_TP_PN", "Compal_TP_PN", "Issue_Link", "Remark", "Attend_Time", "ReTest_Attend_Time", "TestOwner", "Month", "Test_Start", "Test_End",
                    "Editor", "Edittime")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ("Year", 'Customer', 'INV_Number', 'INV_Model', 'Project_Name',"TP_Cat", "Trial_Run_Type", "TP_Vendor",
                    "TP_Key_Parameter", "Lenovo_TP_PN", "Compal_TP_PN", "Status")  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ("Year", 'Customer', 'INV_Number', 'INV_Model', 'Project_Name',"TP_Cat", "Trial_Run_Type", "TP_Vendor",
                    "TP_Key_Parameter", "Lenovo_TP_PN", "Compal_TP_PN", "Status")  # 搜索字段
    date_hierarchy = 'Test_Start'  # 详细时间分层筛选

@admin.register(QIL_M)
class QIL_MAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Customer', 'QIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "edit_time",)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-QIL_No',)
    # 后台数据列表排序方式
    list_display_links = ('Product', 'Customer', 'QIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "editor", "edit_time",)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
                    'Product',
                    # ('Product', UnionFieldListFilter),
                   'Customer',
                   'QIL_No',)  # 过滤器
    search_fields = ('Product', 'Customer', 'QIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "editor", "edit_time",)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
    filter_horizontal = ('files_QIL',)

@admin.register(QIL_Project)
class QIL_ProjectAdmin(admin.ModelAdmin):
    list_display = ('Projectinfo', 'QIL', 'result', 'Comment', "editor", "edit_time")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    # 后台数据列表排序方式
    list_display_links = ('Projectinfo', 'QIL', 'result', 'Comment', "editor", "edit_time")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    list_filter = (
        "Projectinfo",
        "Projectinfo__Project",
        "QIL",
        "QIL__QIL_No",
    )# 过滤器
    search_fields = ('Projectinfo__Project', 'QIL__QIL_No', 'result', 'Comment', "editor", "edit_time")  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(ProjectinfoinDCT)
class ProjectinfoinDCTAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Year', 'ComPrjCode', 'PrjEngCode1', 'PrjEngCode2', 'ProjectName', "Size", "CPU", "Platform", "VGA", "OSSupport", "SS", "LD", "DQAPL", "DQAPLNum",)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year', 'ComPrjCode', 'PrjEngCode1', 'PrjEngCode2', 'ProjectName', "CPU", "Size", "Platform", "VGA", "OSSupport", "SS", "LD", "DQAPL", "DQAPLNum",)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Year', 'ComPrjCode', 'PrjEngCode1', 'PrjEngCode2', 'ProjectName', "Size", "CPU", "Platform", "VGA", "OSSupport", "SS", "LD", "DQAPL",)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(CQM_history)
class CQM_historyAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Changeid', 'Changecontent', 'Changeto', 'Changeowner', "Change_time",)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Changeid',)
    #后台数据列表排序方式
    list_display_links = ('Changeid', 'Changecontent', 'Changeto', 'Changeowner', "Change_time",)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        "Changeid__Project",
        'Changeid',
        'Changeowner',
        # 'Phase',
    )
    # 过滤器
    search_fields = ('Changeid__Project', 'Changecontent', 'Changeto', 'Changeowner', "Change_time")  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(CQMProject)
class CQMProjectAdmin(admin.ModelAdmin):
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
    list_display = ('Customer', 'Project', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ('Customer','Project',)  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', )  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(CQM)
class CQMAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Projectinfo', 'Customer', 'Project', 'Phase', 'Material_Group', 'Keyparts', 'Character', 'PID', 'VID',
                     'HW',  'FW',  'Supplier',  'R1_PN_Description',  'Compal_R1_PN', 'Compal_R3_PN', 'R1S', 'Reliability', 'Compatibility',
                    'Testresult', 'ESD', 'EMI', 'RF', 'PMsummary', 'Controlrun', 'Comments', 'editor', 'edit_time', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    #后台数据列表排序方式
    list_display_links = ('Projectinfo', 'Customer', 'Project', 'Phase', 'Material_Group', 'Keyparts', 'Character', 'PID', 'VID',
                     'HW',  'FW',  'Supplier',  'R1_PN_Description',  'Compal_R1_PN', 'Compal_R3_PN', 'Reliability', 'Compatibility',
                    'Testresult', 'ESD', 'EMI', 'RF', 'PMsummary', 'Controlrun', 'Comments', 'editor', 'edit_time', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Projectinfo',
        'Customer',
        'Phase',
        'Material_Group',
        'Compal_R1_PN',
        'Compal_R3_PN',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Projectinfo__Project', 'Customer', 'Project', 'Phase', 'Material_Group', 'Keyparts', 'Character', 'PID', 'VID',
                     'HW',  'FW',  'Supplier',  'R1_PN_Description',  'Compal_R1_PN', 'Compal_R3_PN', 'R1S', 'Reliability', 'Compatibility',
                    'Testresult', 'ESD', 'EMI', 'RF', 'PMsummary', 'Controlrun', 'Comments', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(lessonlearn_Project)
class lessonlearn_ProjectAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Projectinfo', 'lesson', 'result', 'Comment', 'editor', 'edit_time', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    #后台数据列表排序方式
    list_display_links = ('Projectinfo', 'lesson', 'result', 'Comment', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        "Projectinfo",
        "Projectinfo__Project",
        "lesson",
        "lesson__Category",
    )
    # 过滤器
    search_fields = ('Projectinfo__Project', 'lesson__Category', 'result', 'Comment', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestProjectLL)
class TestProjectLLMEAdmin(admin.ModelAdmin):
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
    list_display = ('Customer', 'Project', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ('Customer', 'Project',)  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', )  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(MQM)
class MQMAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Category', 'Name', 'Vendor', 'SourcePriority', 'CompalPN', 'VendorPN', 'Status', 'Description', 'Qty',
                    'Location', 'editor', 'edit_time',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Category', 'Name', 'Vendor', 'SourcePriority', 'CompalPN', 'VendorPN', 'Status', 'Description', 'Qty',
                    'Location', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ('Customer', 'Project', 'Category', 'Name', 'Vendor', 'SourcePriority', 'CompalPN', 'VendorPN', 'Status',)  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'Category', 'Name', 'Vendor', 'SourcePriority', 'CompalPN', 'VendorPN', 'Status', 'Description', 'Qty',
                    'Location', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


@admin.register(ToolList_M)

class ToolList_MAdmin(admin.ModelAdmin):
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

@admin.register(DriverList_M)
class DriverList_MAdmin(admin.ModelAdmin):
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

@admin.register(KeypartAIO)
class KeypartAIOAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Stand', 'Cable', 'Connectorsource', 'SSDHHD', 'Camera', 'ODD', 'Package', 'RegularAttendTime', 'RegressiveAttendTime')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Stand', 'Cable', 'Connectorsource', 'SSDHHD', 'Camera', 'ODD', 'Package', 'RegularAttendTime', 'RegressiveAttendTime')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Stand', 'Cable', 'Connectorsource', 'SSDHHD', 'Camera', 'ODD', 'Package', 'RegularAttendTime', 'RegressiveAttendTime')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(KeypartC38NB)
class KeypartC38NBAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Hinge', 'Cable', 'Connectorsource', 'Keyboard', 'ClickPad', 'SSDHHD', 'Camera', 'Rubberfoot', 'ODD', 'TrapDoorRJ45', 'RegularAttendTime', 'RegressiveAttendTime')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Hinge', 'Cable', 'Connectorsource', 'Keyboard', 'ClickPad', 'SSDHHD', 'Camera', 'Rubberfoot', 'ODD', 'TrapDoorRJ45', 'RegularAttendTime', 'RegressiveAttendTime')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase', 'IDs', 'Type', 'SKU', 'Planar', 'Panel', 'Hinge', 'Cable', 'Connectorsource', 'Keyboard', 'ClickPad', 'SSDHHD', 'Camera', 'Rubberfoot', 'ODD', 'TrapDoorRJ45', 'RegularAttendTime', 'RegressiveAttendTime')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestPlanME)
class TestPlanMEAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Items', 'Projectinfo', 'editor', 'edit_time', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Items', 'Projectinfo', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Projectinfo',
        'Items',
        # 'Phase',
    )  # 过滤器
    search_fields = ('Items__ItemNo_d', 'Projectinfo__Project', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


@admin.register(TestProjectME)
class TestProjectMEAdmin(admin.ModelAdmin):
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
    list_display = ('Customer', 'Project', 'Phase', 'ScheduleBegin')
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Project', 'Phase', 'ScheduleBegin')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer', 'Project', 'Phase')  # 过滤器
    search_fields = ('Customer', 'Project', 'Phase', 'ScheduleBegin')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(TestItemME)
class TestItemMEAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Customer', 'Phase', 'ItemNo_d', 'Item_d', 'Facility_Name_d', 'Voltage_d', 'Sample_Size_d', 'TimePunits_Facility_d', 'TimePunits_Manual_d',
                    'TimePunits_Program_d', 'Formula',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'Phase', 'ItemNo_d', 'Item_d', 'Facility_Name_d', 'Voltage_d', 'Sample_Size_d', 'TimePunits_Facility_d', 'TimePunits_Manual_d',
                    'TimePunits_Program_d', 'Formula',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d',)  # 过滤器
    search_fields = ('Customer', 'Phase', 'ItemNo_d', 'Item_d', 'Facility_Name_d', 'Voltage_d', 'Sample_Size_d', 'TimePunits_Facility_d', 'TimePunits_Manual_d',
                    'TimePunits_Program_d', 'Formula',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

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

@admin.register(CDM)
class CDMAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('Customer','Project', 'SKU_NO', 'A_cover_Material', 'C_cover_Material', 'D_cover_Material', 'Point1',
                        'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Ave', 'Conclusion',
                        'editor', 'edit_time')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    list_display = ('Customer','Project', 'SKU_NO', 'A_cover_Material', 'C_cover_Material', 'D_cover_Material', 'Point1',
                        'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Ave', 'Conclusion',
                        'editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Point1',
                        'Point2', 'Point3', 'Point4', 'Point5', 'Point6', 'Point7', 'Ave', 'Conclusion')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer','Project')  # 过滤器
    search_fields = ('Customer','Project', 'SKU_NO', 'A_cover_Material', 'C_cover_Material', 'D_cover_Material')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
# admin.site.register(Bouncing_M)
@admin.register(Bouncing_M)
class Bouncing_MAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('Customer','Project', 'A_cover', 'C_cover', 'D_cover', 'HS',
                        'Torque', 'Push', 'PV_L', 'PV_R', 'D_L', 'D_R', 'Conclusion','files_B',
                        'editor', 'edit_time')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    list_display = ('Customer','Project', 'A_cover', 'C_cover', 'D_cover', 'HS',
                        'Torque', 'Push', 'PV_L', 'PV_R', 'D_L', 'D_R', 'Conclusion',
                        'editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('HS',
                        'Torque', 'Push', 'PV_L', 'PV_R', 'D_L', 'D_R', 'Conclusion')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer','Project')  # 过滤器
    search_fields = ('Customer','Project', 'A_cover', 'C_cover', 'D_cover', )  # 搜索字段
    filter_horizontal = ('files_B',)
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
# admin.site.register(Package_M)
@admin.register(Package_M)
class Package_MAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('Customer','Project', 'Phase', 'Degree', 'Duan', 'Zhong',
                        'Chang', 'Left', 'Right', 'Top', 'Bottom', 'Zheng', 'Fan', 'Pattern',
                        'Conclusion','files_P','editor', 'edit_time')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    list_display = ('Customer','Project', 'Phase', 'Degree', 'Duan', 'Zhong',
                        'Chang', 'Left', 'Right', 'Top', 'Bottom', 'Zheng', 'Fan', 'Pattern',
                        'Conclusion','editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Degree', 'Duan', 'Zhong',
                        'Chang', 'Left', 'Right', 'Top', 'Bottom', 'Zheng', 'Fan', 'Pattern')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Customer','Project')  # 过滤器
    search_fields = ('Customer','Project')  # 搜索字段
    filter_horizontal = ('files_P',)
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
# @admin.register(files)
# class filesAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields' : ('files', 'single')
#         }),
#         # ('Advanced options',{
#         #     'classes': ('collapse',),
#         #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
#         # }),
#     )
#     list_display = ('files', 'single')
#     # 列表里显示想要显示的字段
#     list_per_page = 200
#     # 满50条数据就自动分页
#     ordering = ('-single',)
#     #后台数据列表排序方式
#     list_display_links = ('files', 'single')
#
# @admin.register(Imgs)
# class ImgsAdmin(admin.ModelAdmin):
#     fieldsets = (
#         (None, {
#             'fields' : ('img', 'single')
#         }),
#         # ('Advanced options',{
#         #     'classes': ('collapse',),
#         #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
#         # }),
#     )
#     list_display = ('img', 'single')
#     # 列表里显示想要显示的字段
#     list_per_page = 200
#     # 满50条数据就自动分页
#     ordering = ('-single',)
#     #后台数据列表排序方式
#     list_display_links = ('img', 'single')


@admin.register(lesson_learn)
class lesson_learnAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('Category','Object','Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution','Action', 'Status', 'Photo', 'video', 'editor', 'edit_time')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )

    filter_horizontal = ('Photo', 'video',)
    list_display = ('Category','Object','Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution','Action', 'Status','editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    #后台数据列表排序方式
    list_display_links = ('Category','Object','Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution','Action', 'editor', 'edit_time')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Object','Symptom', 'Root_Cause', 'Status')  # 过滤器
    search_fields = ('Category','Object','Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution','Action', 'Status', 'editor', 'edit_time')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('title','parent',)
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    # raw_id_fields = ('parent',)
    list_display = ('title',)
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-title',)
    #后台数据列表排序方式
    list_display_links = ('title',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Tester',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('title',)  # 过滤器
    search_fields = ('title',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('Menu_title','url','menu',)
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    # filter_horizontal = ('perms',)
    # raw_id_fields = ('menu',)
    list_display = ('Menu_title','url',)
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-url',)
    #后台数据列表排序方式
    list_display_links = ('Menu_title','url',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Tester',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('Menu_title','url',)  # 过滤器
    search_fields = ('Menu_title','url',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('name', 'perms')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )
    list_display = ('name', 'show_pers', 'show_users')
    def show_users(self, obj):
        user_list = []
        for user in obj.userinfo_set.all():
            # print(user)
            user_list.append(user.username)
        return '， '.join(user_list)

    show_users.short_description = '成員'  # 设置表头
    def show_pers(self, obj):
        per_list = []
        for perm in obj.perms.all():
            print(perm,1)
            per_list.append(perm.url)
        return '， '.join(per_list)

    show_pers.short_description = '權限'  # 设置表头
    filter_horizontal = ('perms',)
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-name',)
    #后台数据列表排序方式
    list_display_links = ('name',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Tester',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('name',)  # 过滤器
    search_fields = ('name',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields' : ('account','password','username','email','role',)
        }),
        ('Advanced options',{
            'classes': ('collapse',),
            'fields' : ('department','is_active','is_staff','is_SVPuser')
        }),
    )
    filter_horizontal = ('role',)
    list_display = ('account','password','username','email','show_role')
    '''展示show_role'''

    def show_role(self, obj):
        role_list = []
        for role in obj.role.all():
            role_list.append(role.name)
        return '， '.join(role_list)

    show_role.short_description = '角色'  # 设置表头
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-account',)
    #后台数据列表排序方式
    list_display_links = ('account','password','username','email')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Tester',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('account','password','username','email', 'role')  # 过滤器
    search_fields = ('account','password','username','email', 'role__name')  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


