from django.contrib import admin
from .models import CriticalIssue, CriticalIssueCrossResult, CriticalIssuefiles, CriticalIssueImgs, CriticalIssueTestProject

admin.site.register(CriticalIssueImgs)
admin.site.register(CriticalIssuefiles)
# Register your models here.
@admin.register(CriticalIssue)
class CriticalIssueAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
            'CG', 'Category', 'Object', 'Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution', 'Action',
            'Project', 'Status', 'Photo', 'video', 'editor', 'edit_time')
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )

    filter_horizontal = ('Photo', 'video',)
    list_display = (
            'IssueNum', 'CG', 'Category', 'Object', 'Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution', 'Action',
            'Project', 'Status', 'editor', 'edit_time')
    # 列表里显示想要显示的字段
    list_per_page = 200
    # 满50条数据就自动分页
    ordering = ('-edit_time',)
    # 后台数据列表排序方式
    list_display_links = (
            'IssueNum', 'CG', 'Category', 'Object', 'Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution', 'Action',
            'Project', 'Status', 'editor', 'edit_time')
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = ('IssueNum', 'CG', 'Category')  # 过滤器
    search_fields = (
    'IssueNum', 'CG', 'Category', 'Object', 'Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


@admin.register(CriticalIssueCrossResult)
class CriticalIssueCrossResultAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields' : ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')
    #     }),
    #     # ('Advanced options',{
    #     #     'classes': ('collapse',),
    #     #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
    #     # }),
    # )
    list_display = ('Projectinfo', 'CriticalIssue', 'result', 'Comment', 'editor', 'edit_time',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Projectinfo',)
    # 后台数据列表排序方式
    list_display_links = ('Projectinfo', 'CriticalIssue', 'result', 'Comment', 'editor', 'edit_time',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        "Projectinfo",
        "Projectinfo__Project",
        "CriticalIssue",
        "CriticalIssue__Category",
    )
    # 过滤器
    search_fields = ('Projectinfo__Project', 'CriticalIssue__Category', 'result', 'Comment', 'editor', 'edit_time',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选


@admin.register(CriticalIssueTestProject)
class CriticalIssueTestProjectAdmin(admin.ModelAdmin):
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
    list_display = ('Customer', 'Project',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Customer',)
    # 后台数据列表排序方式
    list_display_links = ('Customer', 'Project',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = ('Customer', 'Project',)  # 过滤器
    # list_filter = ('Customer','Phase', 'ItemNo_d', 'Item_d', 'TestItems')  # 过滤器
    search_fields = ('Customer', 'Project',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选