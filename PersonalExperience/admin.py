from django.contrib import admin
from .models import PerExperience, OSR_OSinfo

# Register your models here.

@admin.register(PerExperience)
class PerExperienceAdmin(admin.ModelAdmin):
    list_display = ('Proposer_Num', 'Proposer_Name', 'Dalei', 'Department_Code', 'Item', 'Positions_Name', 'Project', "SS_Date", "Year", "Time_Interval", "Phase", "Role", "Function", "SubFunction_Com", "KeypartNum",
                    "Comments", "Approved_Officer", "Status", "EditTime", )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Proposer_Num',)
    # 后台数据列表排序方式
    list_display_links = ('Proposer_Num', 'Proposer_Name', 'Dalei', 'Department_Code', 'Project', "SS_Date", "Year", "Time_Interval", "Phase", "Role", "Function", "SubFunction_Com", "KeypartNum",
                    "Comments", "Approved_Officer", "Status", "EditTime",)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ("Proposer_Num", 'Department_Code', 'Dalei', 'Project', 'Year', "Approved_Officer", "Status",)  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ("Proposer_Num", 'Department_Code', 'Project', 'Year', 'Project_Name',"Approved_Officer", "Status",)  # 搜索字段
    date_hierarchy = 'EditTime'  # 详细时间分层筛选

@admin.register(OSR_OSinfo)
class OSR_OSinfoAdmin(admin.ModelAdmin):
    list_display = ('OSinfo', 'Editer', 'EditTime',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-OSinfo',)
    # 后台数据列表排序方式
    list_display_links = ('OSinfo', 'Editer', 'EditTime',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ("OSinfo", )  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ("OSinfo",)  # 搜索字段