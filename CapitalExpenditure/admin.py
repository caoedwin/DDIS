from django.contrib import admin

# Register your models here.
from .models import CapitalExpenditure, C38CustomerT88AIODepartmentCode

@admin.register(CapitalExpenditure)
class CapitalExpenditureAdmin(admin.ModelAdmin):

    list_display = (
        'PlanYear', 'Customer', 'BudgetCode', 'Investment_Nature', 'Attribute_Code', 'Application_Department', 'Device_Name', 'Usage_Description',
        'Specifications', 'Acceptance_Month', 'Budget_Quantity', 'Estimated_Original_Currency', 'Estimated_Original_Price', 'Equivalent_To_RMB', 'Payment_Terms', 'Depreciation_Months', 'Accounting_Subjects',
        'Automated_Or_Not', 'Project_Code', 'Current_Situation', 'Applicable_Scope', 'Investment_Purpose', 'Investment_Purpose_Des',
        'Potential_Issues', 'Potential_Issues_Des', 'Tighten_Expenses', 'Annual_Increase_PerYear', 'Investment_Benefits_PerYear', 'Cash_Inflows_PerYear',
        'Payback_Period', 'Subscription_Status', 'Subscription_Quantity', 'Subscription_Amount', 'Entry_Amount',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-PlanYear',)
    #后台数据列表排序方式
    list_display_links = (
         'PlanYear', 'Customer', 'BudgetCode', 'Investment_Nature', 'Attribute_Code', 'Application_Department', 'Device_Name', 'Usage_Description',
        'Specifications', 'Acceptance_Month', 'Budget_Quantity', 'Estimated_Original_Currency', 'Estimated_Original_Price', 'Equivalent_To_RMB', 'Payment_Terms', 'Depreciation_Months', 'Accounting_Subjects',
        'Automated_Or_Not', 'Project_Code', 'Current_Situation', 'Applicable_Scope', 'Investment_Purpose', 'Investment_Purpose_Des',
        'Potential_Issues', 'Potential_Issues_Des', 'Tighten_Expenses', 'Annual_Increase_PerYear', 'Investment_Benefits_PerYear', 'Cash_Inflows_PerYear',
        'Payback_Period', 'Subscription_Status', 'Subscription_Quantity', 'Subscription_Amount', 'Entry_Amount',
                    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'PlanYear',
        'Customer',
        'BudgetCode',
        'Application_Department',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('PlanYear', 'Customer', 'BudgetCode', 'Application_Department',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(C38CustomerT88AIODepartmentCode)
class C38CustomerT88AIODepartmentCodeAdmin(admin.ModelAdmin):

    list_display = (
        'Year', 'Department_Code',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = (
        'Year', 'Department_Code',
    )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'Department_Code',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year', 'Department_Code',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选