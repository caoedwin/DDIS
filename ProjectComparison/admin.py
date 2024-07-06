from django.contrib import admin

# Register your models here.
from .models import ProjectPlan

@admin.register(ProjectPlan)
class ProjectPlanAdmin(admin.ModelAdmin):

    list_display = (
        'RD_Project_Plan', 'Year', 'DataType', 'CG', 'Compal_Model', 'Customer_Model', 'Marketing_type',
        'Status', 'Customer', 'Product_Type', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = (
         'RD_Project_Plan', 'Year', 'DataType', 'CG', 'Compal_Model', 'Customer_Model', 'Marketing_type',
        'Status', 'Customer', 'Product_Type',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'DataType',
        'Customer',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year', 'DataType', 'Customer',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选