from django.contrib import admin
from .models import KnowIssue_M
# Register your models here.
@admin.register(KnowIssue_M)
class KnowIssue_MAdmin(admin.ModelAdmin):
    list_display = ('Customer', 'Project_Code', 'Platform', "Issue_NO", "Issue_Title", "Issue_Component", "Detect_By_Case", "Root_Cause", "Issue_Status", "PL")
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Edittime',)
    # 后台数据列表排序方式
    list_display_links = ('Customer', 'Project_Code', 'Platform', "Issue_NO", "Issue_Title", "Issue_Component", "Detect_By_Case", "Root_Cause", "Issue_Status", "PL")
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    # list_filter = ('Customer','Project', 'Unit', 'Phase', 'Tester', 'Testitem','Result', 'Start_time', 'End_time', 'Result_time','Item_Des', 'Comments')  # 过滤器
    list_filter = (
                    'Customer',
                    # ('Product', UnionFieldListFilter),
                   'Project_Code',
                   'Platform',)  # 过滤器
    search_fields = ('Customer', 'Project_Code', 'Platform',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选