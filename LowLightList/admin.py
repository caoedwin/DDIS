from django.contrib import admin

# Register your models here.
from .models import LowLightList

@admin.register(LowLightList)
class LowLightListAdmin(admin.ModelAdmin):

    list_display = ('Customer', 'ProjectCompal', 'Lowlight_item', 'Root_Cause', 'LD', 'Owner', 'Mitigation_plan', 'editor', 'edit_time', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-ProjectCompal',)
    #后台数据列表排序方式
    list_display_links = ('Customer', 'ProjectCompal', 'Lowlight_item', 'Root_Cause', 'LD', 'Owner', 'Mitigation_plan', 'editor', 'edit_time', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Customer',
        'ProjectCompal',
        'editor',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Customer', 'ProjectCompal', 'editor',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选