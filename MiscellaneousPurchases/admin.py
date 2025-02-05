from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(SubscriptionStatus)
class SubscriptionStatusAdmin(admin.ModelAdmin):

    list_display = ('Year',
                    'Ledger',
                    'Name', 'Status', 'ModelSpecifications', 'SubscribeDate', 'SubscribeForm', 'SubscribeUnitPrice', 'Number',
                    'AcceptanceForm', 'AcceptanceDate', 'ActUnitPrice', 'Customer', 'ProjectCode',
                    'Department', 'RequisitionerNum', 'Requisitioner',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year',
                    'Ledger',
                    'Name', 'Status', 'ModelSpecifications', 'SubscribeDate', 'SubscribeForm', 'SubscribeUnitPrice', 'Number',
                    'AcceptanceForm', 'AcceptanceDate', 'ActUnitPrice', 'Customer', 'ProjectCode',
                    'Department', 'RequisitionerNum', 'Requisitioner',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'Ledger',
        'Customer',
        'SubscribeForm',
        'AcceptanceForm',
        'RequisitionerNum',
        'Requisitioner',

        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year',
        'Ledger',
        'Customer',
        'SubscribeForm',
        'AcceptanceForm',
        'RequisitionerNum',
        'Requisitioner',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):

    list_display = ('Year',
                    'Ledger',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year',
                    'Ledger',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'Ledger',

        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year',
                    'Ledger',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(ReceiptAmount)
class ReceiptAmountAdmin(admin.ModelAdmin):

    list_display = ('Year',
                    'Ledger',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year',
                    'Ledger',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'Ledger',

        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year',
                    'Ledger',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选