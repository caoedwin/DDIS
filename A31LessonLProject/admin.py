from django.contrib import admin
from .models import A31lesson_learn, A31lessonlearn_Project, A31TestProjectLL

# Register your models here.
@admin.register(A31lesson_learn)
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
    list_display = ('Category','Object','Symptom', 'Reproduce_Steps', 'Root_Cause', 'Solution','Action','editor', 'edit_time')
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

@admin.register(A31lessonlearn_Project)
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

@admin.register(A31TestProjectLL)
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