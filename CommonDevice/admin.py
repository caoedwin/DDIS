from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(CommonDevice)
class CommonDeviceAdmin(admin.ModelAdmin):

    list_display = (
        'Category', 'Product_Type', 'Name', 'Num', 'Manufacturer', 'Cost', 'Account', 'PW',
        'Purchasing_Date', 'Department', 'Location', 'Asset_Num', 'Owner_Num', 'Owner', 'Mail', 'Contact_info', 'Comments', 'Editor', 'Edit_data',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Edit_data',)
    #后台数据列表排序方式
    list_display_links = ('Category', 'Product_Type', 'Name', 'Num', 'Manufacturer', 'Cost', 'Account', 'PW',
        'Purchasing_Date', 'Department', 'Location', 'Asset_Num', 'Owner_Num', 'Owner', 'Mail', 'Contact_info',  'Comments' )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Owner_Num',
        'Owner',
        'Category',
        'Product_Type',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Owner_Num', 'Owner', 'Category', 'Product_Type',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选