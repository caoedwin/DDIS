from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )

    list_display = (
        'name',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-name',)
    #后台数据列表排序方式
    list_display_links = ('name', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'name',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('name',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('category', 'name', )
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )

    list_display = (
         'category', 'name',
                    )

    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-name',)
    #后台数据列表排序方式
    list_display_links = ('name', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'name',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('name',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(CommonDevice)
class CommonDeviceAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('Category', 'Product_Type', 'Name', 'Num', 'Manufacturer', 'Cost', 'Account', 'PW',
        'Purchasing_Date', 'Department', 'Location', 'Asset_Num', 'Owner', 'Mail', 'Contact_info', 'Comments', 'Creator',)
        }),
        # ('Advanced options',{
        #     'classes': ('collapse',),
        #     'fields' : ('Start_time', 'End_time', 'Result_time','Result','Comments')
        # }),
    )

    list_display = (
        'Category', 'Product_Type', 'Name', 'Num', 'Manufacturer', 'Cost', 'Account', 'PW',
        'Purchasing_Date', 'Department', 'Location', 'Asset_Num', 'show_user', 'Mail', 'Contact_info', 'Comments', 'Creator', 'created_at', 'updated_at',
                    )
    def show_user(self, obj):
        user_list = []
        for user in obj.Owner.all():
            user_list.append(user.account+'-'+user.username)
        return '， '.join(user_list)

    show_user.short_description = 'owner'  # 设置表头
    filter_horizontal = ('Owner',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-created_at',)
    #后台数据列表排序方式
    list_display_links = ('Category', 'Product_Type', 'Name', 'Num', 'Manufacturer', 'Cost', 'Account', 'PW',
        'Purchasing_Date', 'Department', 'Location', 'Asset_Num', 'Mail', 'Contact_info',  'Comments' )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Owner',
        'Owner',
        'Category',
        'Product_Type',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Owner', 'Owner', 'Category', 'Product_Type', 'Owner__account',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选