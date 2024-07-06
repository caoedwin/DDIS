from django.contrib import admin
from .models import ABOQIL_M, ABOQIL_Project, files_ABOQIL
admin.site.register(files_ABOQIL)
# Register your models here.
@admin.register(ABOQIL_M)
class ABOQIL_MAdmin(admin.ModelAdmin):
    list_display = ('Product', 'Customer', 'ABOQIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "edit_time",)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-ABOQIL_No',)
    # 后台数据列表排序方式
    list_display_links = ('Product', 'Customer', 'ABOQIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "editor", "edit_time",)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
                    'Product',
                    # ('Product', UnionFieldListFilter),
                   'Customer',
                   'ABOQIL_No',)  # 过滤器
    search_fields = ('Product', 'Customer', 'ABOQIL_No', 'Issue_Description', "Root_Cause", "Status", "editor", "Creator", "Created_On", "editor", "edit_time",)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
    filter_horizontal = ('files_ABOQIL',)

@admin.register(ABOQIL_Project)
class ABOQIL_ProjectAdmin(admin.ModelAdmin):
    list_display = ('Projectinfo', 'ABOQIL', 'result', 'Comment', "editor", "edit_time")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    # 后台数据列表排序方式
    list_display_links = ('Projectinfo', 'ABOQIL', 'result', 'Comment', "editor", "edit_time")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    list_filter = (
        "Projectinfo",
        "Projectinfo__Project",
        "ABOQIL",
        "ABOQIL__ABOQIL_No",
    )# 过滤器
    search_fields = ('Projectinfo__Project', 'ABOQIL__ABOQIL_No', 'result', 'Comment', "editor", "edit_time")  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选