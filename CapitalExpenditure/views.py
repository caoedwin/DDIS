from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime, os
from django.http import HttpResponse
import datetime, json, simplejson, pprint
from .models import CapitalExpenditure, C38CustomerT88AIODepartmentCode
from app01.models import UserInfo, ProjectinfoinDCT, Role
from PersonalInfo.models import Departments
from django.db import transaction
from django.db.models import F, Sum
from django.db.models.functions import Lower, Upper, Substr
from django.forms.models import model_to_dict

# Create your views here.
headermodel_CapitalExpenditure = {
    'PlanYear': 'PlanYear', '客戶別': 'Customer',
    '預算編號': 'BudgetCode', '投資性質': 'Investment_Nature', '屬性代碼': 'Attribute_Code', '申請部門': 'Application_Department',
    '設備或工程名稱': 'Device_Name', '用途說明': 'Usage_Description', '廠牌規格': 'Specifications', '驗收月份': 'Acceptance_Month',
    '預算數量': 'Budget_Quantity', '預估總價': 'Estimated_Original_Currency', '__EMPTY': 'Estimated_Original_Price',
    '折合人民幣': 'Equivalent_To_RMB', '付款條件': 'Payment_Terms', '折舊月數': 'Depreciation_Months', '會計科目': 'Accounting_Subjects',
    '是否自動化': 'Automated_Or_Not', 'Project Code': 'Project_Code', '現狀說明': 'Current_Situation',
    '適用範圍': 'Applicable_Scope',
    '投資動機與目的': 'Investment_Purpose', '投資動機與目的其他說明': 'Investment_Purpose_Des',
    '潛在問題': 'Potential_Issues', '潛在問題的其他說明': 'Potential_Issues_Des',
    '年節省支出': 'Tighten_Expenses', '年增加收益': 'Annual_Increase_PerYear', '年投資效益': 'Investment_Benefits_PerYear',
    '年淨現金流入': 'Cash_Inflows_PerYear', '回收年限(月數)': 'Payback_Period', '申購狀況': 'Subscription_Status',
    '申購數量': 'Subscription_Quantity', '申購金額\r\n(CNY)': 'Subscription_Amount', '入賬金額\r\n(CNY)': 'Entry_Amount',
}


@csrf_exempt
def CapitalExpenditure_Summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DDIS/CapitalExpenditure_Summary"

    yearOptions = [
        # "2020", "2021", "2023"
    ]
    for i in CapitalExpenditure.objects.all().values('PlanYear').distinct().order_by('PlanYear'):
        yearOptions.append(i["PlanYear"])
    CustomerOption = [

    ]
    YearNow = str(datetime.datetime.now().year)
    for i in Departments.objects.all().values("Customer").distinct().order_by("Customer"):
        CustomerOption.append(i['Customer'])

    CustomerToDepartmentSeven = [

    ]

    mock_data = [
        # {"id": "1", "PlanYear": "2024", "BudgetCode": "HKMKBAQAA0047789", "Investment_Nature": "A", "Attribute_Code": "1212", "Application_Department": "KMKBAQAA00",
        #  "Device_Name": "隔音室(屏蔽室)", "Usage_Description": "C38NB專案支援Wi-Fi 7, 目前無Wi-Fi 7 AP 可用於測試,需申購用於Wi-Fi 7的頻寬相關測試.",
        #  "Specifications": "TP-Link Archer BE900 BE24000四頻網狀WiFi7路由器或等同規格的其他品牌或型號", "Acceptance_Month": "6", "Budget_Quantity": "1", "Estimated_Original_Currency": "CNY",
        #  "Estimated_Original_Price": "15000", "Equivalent_To_RMB": "15000", "Payment_Terms": "驗收后月結150天付款", "Depreciation_Months": "72", "Accounting_Subjects": "6201E",
        #  "Automated_Or_Not": "N", "Project_Code": "INRG000000", "Current_Situation": "D", "Applicable_Scope": 1, "Investment_Purpose": "提高品質水准",
        #  "Investment_Purpose_Des": "", "Potential_Issues": "售後服務不易", "Potential_Issues_Des": "", "Tighten_Expenses": 1, "Annual_Increase_PerYear": 2500, "Investment_Benefits_PerYear": 1,
        #  "Cash_Inflows_PerYear": 2501, "Payback_Period": 72, "Subscription_Status": "未申購", "Subscription_Quantity": "", "Subscription_Amount": "", "Entry_Amount": ""},
        # {"id": "2", "PlanYear": "2025", "BudgetCode": "HKMKBAQAA0047789", "Investment_Nature": "A", "Attribute_Code": "1212", "Application_Department": "KMKBAQAA00",
        #  "Device_Name": "隔音室(屏蔽室)", "Usage_Description": "C38NB專案支援Wi-Fi 7, 目前無Wi-Fi 7 AP 可用於測試,需申購用於Wi-Fi 7的頻寬相關測試.",
        #  "Specifications": "TP-Link Archer BE900 BE24000四頻網狀WiFi7路由器或等同規格的其他品牌或型號", "Acceptance_Month": "6", "Budget_Quantity": "1", "Estimated_Original_Currency": "CNY",
        #  "Estimated_Original_Price": "15000", "Equivalent_To_RMB": "15000", "Payment_Terms": "驗收后月結150天付款", "Depreciation_Months": "72", "Accounting_Subjects": "6201E",
        #  "Automated_Or_Not": "N", "Project_Code": "INRG000000", "Current_Situation": "D", "Applicable_Scope": 1, "Investment_Purpose": "提高品質水准",
        #  "Investment_Purpose_Des": "", "Potential_Issues": "售後服務不易", "Potential_Issues_Des": "", "Tighten_Expenses": 1, "Annual_Increase_PerYear": 2500, "Investment_Benefits_PerYear": 1,
        #  "Cash_Inflows_PerYear": 2501, "Payback_Period": 72, "Subscription_Status": "未申購", "Subscription_Quantity": "", "Subscription_Amount": "", "Entry_Amount": ""},
        # {"id": "3", "PlanYear": "2024", "BudgetCode": "HKMKBAQAA0047789", "Investment_Nature": "A",
        #  "Attribute_Code": "1212", "Application_Department": "KMKBAQAA00",
        #  "Device_Name": "隔音室(屏蔽室)", "Usage_Description": "C38NB專案支援Wi-Fi 7, 目前無Wi-Fi 7 AP 可用於測試,需申購用於Wi-Fi 7的頻寬相關測試.",
        #  "Specifications": "TP-Link Archer BE900 BE24000四頻網狀WiFi7路由器或等同規格的其他品牌或型號", "Acceptance_Month": "6",
        #  "Budget_Quantity": "1", "Estimated_Original_Currency": "CNY",
        #  "Estimated_Original_Price": "15000", "Equivalent_To_RMB": "15000", "Payment_Terms": "驗收后月結150天付款",
        #  "Depreciation_Months": "72", "Accounting_Subjects": "6201E",
        #  "Automated_Or_Not": "N", "Project_Code": "INRG000000", "Current_Situation": "D", "Applicable_Scope": 1,
        #  "Investment_Purpose": "提高品質水准",
        #  "Investment_Purpose_Des": "", "Potential_Issues": "售後服務不易", "Potential_Issues_Des": "", "Tighten_Expenses": 1,
        #  "Annual_Increase_PerYear": 2500, "Investment_Benefits_PerYear": 1,
        #  "Cash_Inflows_PerYear": 2501, "Payback_Period": 72, "Subscription_Status": "未申購", "Subscription_Quantity": "",
        #  "Subscription_Amount": "", "Entry_Amount": ""},
    ]

    tables = [
        # {
        #     "data": [
        #         {"C38_T89": "數量", "Annual_Budget": "13", "Unsubscribed": '13', "Subscription_In_Progress": '0',
        #          "During_Acceptance": '0', "Acceptance_Completed": '0'},
        #         {"C38_T89": "金額(CNY)", "Annual_Budget": "423326", "Unsubscribed": '423326',
        #          "Subscription_In_Progress": '0',
        #          "During_Acceptance": '0', "Acceptance_Completed": '0'},
        #     ],
        #     "columns": [
        #         {"prop": "C38_T89", "label": "C38 & T89"},
        #         {"prop": "Annual_Budget", "label": "年度預算"},
        #         {"prop": "Unsubscribed", "label": "未申購"},
        #         {"prop": "Subscription_In_Progress", "label": "申購中"},
        #         {"prop": "During_Acceptance", "label": "驗收中"},
        #         {"prop": "Acceptance_Completed", "label": "驗收完成"},
        #     ]
        # },
        # {
        #     "data": [
        #         {"T88_AIO": "數量", "Annual_Budget": "13", "Unsubscribed": '13', "Subscription_In_Progress": '0',
        #          "During_Acceptance": '0', "Acceptance_Completed": '0'},
        #         {"T88_AIO": "金額(CNY)", "Annual_Budget": "423326", "Unsubscribed": '423326',
        #          "Subscription_In_Progress": '0',
        #          "During_Acceptance": '0', "Acceptance_Completed": '0'},
        #     ],
        #     "columns": [
        #         {"prop": "T88_AIO", "label": "T88 AIO"},
        #         {"prop": "Annual_Budget", "label": "年度預算"},
        #         {"prop": "Unsubscribed", "label": "未申購"},
        #         {"prop": "Subscription_In_Progress", "label": "申購中"},
        #         {"prop": "During_Acceptance", "label": "驗收中"},
        #         {"prop": "Acceptance_Completed", "label": "驗收完成"},
        #     ]
        # }
    ]

    errMsg = ''

    permission = 0  # 1:有權限
    roles = []
    onlineuser = request.session.get('account')
    # onlineuser = '0502413'
    onlineuserDepartment = ''
    # print(onlineuser,UserInfo.objects.get(account=onlineuser))
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    for i in roles:
        if 'admin' == i or 'DQA_LNV_CapitalExpenditure_admin' in i:
            permission = 1

    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            pass
        if request.POST.get('action') == 'addData':
            Year = request.POST.get('Year')
            Department_Code = request.POST.get('DepartmentCode')
            addDepartCode_dic = {"Year": Year, "Department_Code": Department_Code}
            if C38CustomerT88AIODepartmentCode.objects.filter(Year=Year):
                errMsg = "%s T88 AIO的部门代码已经存在" % Year
            else:
                C38CustomerT88AIODepartmentCode.objects.create(**addDepartCode_dic)

        if request.POST.get('isGetData') == 'SEARCH':
            # mock_data
            YearSearch = request.POST.get('Year')
            Customer = request.POST.get('Customer')
            for i in CapitalExpenditure.objects.exclude(Application_Department=None).filter(
                    PlanYear=YearSearch).annotate(
                first_seven=Substr(Upper('Application_Department'), 1, 7)).values('first_seven').distinct():
                # print(i['first_seven'], Departments.objects.filter(Department_Code__contains=i['first_seven']).first())
                CustomerToDepartmentSeven.append((Departments.objects.filter(Year=YearSearch,
                                                                             Department_Code__contains=i[
                                                                                 'first_seven']).first().Customer,
                                                  i['first_seven']))
            # print(CustomerToDepartmentSeven)
            DepartmentSeven = '部门代码没匹配到不能用空字符串会匹配到所有数据'
            for i in CustomerToDepartmentSeven:
                if Customer == i[0]:
                    DepartmentSeven = i[1]
                    break
            yearOptions = [
                # "2020", "2021", "2023"
            ]
            for i in CapitalExpenditure.objects.all().values("PlanYear").distinct().order_by("PlanYear"):
                yearOptions.append(i["PlanYear"])

            Check_dic_CapitalExpenditure = {}
            if YearSearch:
                Check_dic_CapitalExpenditure["PlanYear"] = YearSearch
                Check_dic_CapitalExpenditure["Application_Department__contains"] = DepartmentSeven
            # elif YearSearch_backup:
            #     Check_dic_CapitalExpenditure["PlanYear"] = YearSearch_backup
            # print(Check_dic_CapitalExpenditure)
            if CapitalExpenditure.objects.filter(**Check_dic_CapitalExpenditure):
                for i in CapitalExpenditure.objects.filter(**Check_dic_CapitalExpenditure):
                    # print(i)
                    mock_data.append(
                        {
                            "id": i.id, "PlanYear": i.PlanYear, "Customer": i.Customer, "BudgetCode": i.BudgetCode,
                            "Investment_Nature": i.Investment_Nature,
                            "Attribute_Code": i.Attribute_Code,
                            "Application_Department": i.Application_Department,
                            "Device_Name": i.Device_Name,
                            "Usage_Description": i.Usage_Description,
                            "Specifications": i.Specifications,
                            "Acceptance_Month": i.Acceptance_Month,
                            "Budget_Quantity": i.Budget_Quantity,
                            "Estimated_Original_Currency": i.Estimated_Original_Currency,
                            "Estimated_Original_Price": i.Estimated_Original_Price,
                            "Equivalent_To_RMB": i.Equivalent_To_RMB,
                            "Payment_Terms": i.Payment_Terms,
                            "Depreciation_Months": i.Depreciation_Months,
                            "Accounting_Subjects": i.Accounting_Subjects,
                            "Automated_Or_Not": i.Automated_Or_Not,
                            "Project_Code": i.Project_Code,
                            "Current_Situation": i.Current_Situation,
                            "Applicable_Scope": i.Applicable_Scope,
                            "Investment_Purpose": i.Investment_Purpose,
                            "Investment_Purpose_Des": i.Investment_Purpose_Des,
                            "Potential_Issues": i.Potential_Issues,
                            "Potential_Issues_Des": i.Potential_Issues_Des,
                            "Tighten_Expenses": i.Tighten_Expenses,
                            "Annual_Increase_PerYear": i.Annual_Increase_PerYear,
                            "Investment_Benefits_PerYear": i.Investment_Benefits_PerYear,
                            "Cash_Inflows_PerYear": i.Cash_Inflows_PerYear,
                            "Payback_Period": i.Payback_Period,
                            "Subscription_Status": i.Subscription_Status,
                            "Subscription_Quantity": i.Subscription_Quantity,
                            "Subscription_Amount": i.Subscription_Amount,
                            "Entry_Amount": i.Entry_Amount,
                        }
                    )
                # tables

                if Customer == "C38":
                    if C38CustomerT88AIODepartmentCode.objects.filter(Year=YearSearch) and DepartmentSeven:
                        AIOT88_DeparmentCode = C38CustomerT88AIODepartmentCode.objects.filter(
                            Year=YearSearch).first().Department_Code

                        if CapitalExpenditure.objects.filter(PlanYear=YearSearch):
                            tables_dic1 = {
                                "data": [
                                    {"C38_T89": "數量",
                                     "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                         'total'] else 0,
                                     "Unsubscribed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Budget_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Budget_Quantity'))[
                                             'total'] else 0,
                                     "Subscription_In_Progress":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0,
                                     "During_Acceptance":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0,
                                     "Acceptance_Completed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收完成").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收完成").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0
                                     },
                                    {"C38_T89": "金額(CNY)",
                                     "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] else 0,
                                     "Unsubscribed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Equivalent_To_RMB'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Equivalent_To_RMB'))[
                                             'total'] else 0,
                                     "Subscription_In_Progress":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] else 0,
                                     "During_Acceptance":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").exclude(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] else 0,
                                     "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                               Application_Department__contains=DepartmentSeven,
                                                                                               Subscription_Status="驗收完成").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                               Application_Department__contains=DepartmentSeven,
                                                                                               Subscription_Status="驗收完成").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0
                                     },
                                ],
                                "columns": [
                                    {"prop": "C38_T89", "label": "C38 & T89"},
                                    {"prop": "Annual_Budget", "label": "年度預算"},
                                    {"prop": "Unsubscribed", "label": "未申購"},
                                    {"prop": "Subscription_In_Progress", "label": "申購中"},
                                    {"prop": "During_Acceptance", "label": "驗收中"},
                                    {"prop": "Acceptance_Completed", "label": "驗收完成"},
                                ]
                            }

                            tables_dic2 = {
                                "data": [
                                    {"T88_AIO": "數量",
                                     "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                         'total'] else 0,
                                     "Unsubscribed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Budget_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Budget_Quantity'))[
                                             'total'] else 0,
                                     "Subscription_In_Progress":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0,
                                     "During_Acceptance":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0,
                                     "Acceptance_Completed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收完成").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收完成").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Quantity'))[
                                             'total'] else 0
                                     },
                                    {"T88_AIO": "金額(CNY)",
                                     "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] else 0,
                                     "Unsubscribed":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Equivalent_To_RMB'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="未申購").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Equivalent_To_RMB'))[
                                             'total'] else 0,
                                     "Subscription_In_Progress":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="申購中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] else 0,
                                     "During_Acceptance":
                                         CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收中").filter(
                                             Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                             total=Sum('Subscription_Amount'))[
                                             'total'] else 0,
                                     "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                               Application_Department__contains=DepartmentSeven,
                                                                                               Subscription_Status="驗收完成").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                               Application_Department__contains=DepartmentSeven,
                                                                                               Subscription_Status="驗收完成").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0
                                     },
                                ],
                                "columns": [
                                    {"prop": "T88_AIO", "label": "T88 AIO"},
                                    {"prop": "Annual_Budget", "label": "年度預算"},
                                    {"prop": "Unsubscribed", "label": "未申購"},
                                    {"prop": "Subscription_In_Progress", "label": "申購中"},
                                    {"prop": "During_Acceptance", "label": "驗收中"},
                                    {"prop": "Acceptance_Completed", "label": "驗收完成"},
                                ]
                            }
                            tables.append(tables_dic1)
                            tables.append(tables_dic2)
                    else:
                        errMsg = "没有该年的AIO部门代码，请先录入"

                else:
                    print(CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                 'total'],DepartmentSeven)
                    tables_dic = {
                        "data": [
                            {Customer: "數量",
                             "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,).exclude(BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                 'total'] else 0,
                             "Unsubscribed":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="未申購").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Budget_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="未申購").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Budget_Quantity'))[
                                     'total'] else 0,
                             "Subscription_In_Progress":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="申購中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="申購中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] else 0,
                             "During_Acceptance":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] else 0,
                             "Acceptance_Completed":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收完成").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收完成").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Quantity'))[
                                     'total'] else 0
                             },
                            {Customer: "金額(CNY)",
                             "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(BudgetCode="預算外").aggregate(
                                 total=Sum('Equivalent_To_RMB'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven).exclude(BudgetCode="預算外").aggregate(
                                 total=Sum('Equivalent_To_RMB'))[
                                 'total'] else 0,
                             "Unsubscribed":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="未申購").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="未申購").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] else 0,
                             "Subscription_In_Progress":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="申購中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="申購中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] else 0,
                             "During_Acceptance":
                                 CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                   Subscription_Status="驗收中").exclude(BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] else 0,
                             "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收完成").exclude(BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                        Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收完成").exclude(BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] else 0
                             },
                        ],
                        "columns": [
                            {"prop": Customer, "label": Customer},
                            {"prop": "Annual_Budget", "label": "年度預算"},
                            {"prop": "Unsubscribed", "label": "未申購"},
                            {"prop": "Subscription_In_Progress", "label": "申購中"},
                            {"prop": "During_Acceptance", "label": "驗收中"},
                            {"prop": "Acceptance_Completed", "label": "驗收完成"},
                        ]
                    }
                    tables.append(tables_dic)

        elif request.POST.get('action') == 'onSubmit':
            ID = request.POST.get('ID')
            PlanYear = request.POST.get('PlanYear')
            Customer = request.POST.get('Customer')
            BudgetCode = request.POST.get('BudgetCode')
            Investment_Nature = request.POST.get('Investment_Nature')
            Attribute_Code = request.POST.get('Attribute_Code')
            Application_Department = request.POST.get('Application_Department')
            Device_Name = request.POST.get('Device_Name')
            Usage_Description = request.POST.get('Usage_Description')
            Specifications = request.POST.get('Specifications')
            Acceptance_Month = request.POST.get('Acceptance_Month')
            Budget_Quantity = request.POST.get('Budget_Quantity')
            Estimated_Original_Currency = request.POST.get('Estimated_Original_Currency')
            Estimated_Original_Price = request.POST.get('Estimated_Original_Price')
            Equivalent_To_RMB = request.POST.get('Equivalent_To_RMB')
            Payment_Terms = request.POST.get('Payment_Terms')
            Depreciation_Months = request.POST.get('Depreciation_Months')
            Accounting_Subjects = request.POST.get('Accounting_Subjects')
            Automated_Or_Not = request.POST.get('Automated_Or_Not')
            Project_Code = request.POST.get('Project_Code')
            Current_Situation = request.POST.get('Current_Situation')
            Applicable_Scope = request.POST.get('Applicable_Scope')
            Investment_Purpose = request.POST.get('Investment_Purpose')
            Investment_Purpose_Des = request.POST.get('Investment_Purpose_Des')
            Potential_Issues = request.POST.get('Potential_Issues')
            Potential_Issues_Des = request.POST.get('Potential_Issues_Des')
            Tighten_Expenses = request.POST.get('Tighten_Expenses')
            Annual_Increase_PerYear = request.POST.get('Annual_Increase_PerYear')
            Investment_Benefits_PerYear = request.POST.get('Investment_Benefits_PerYear')
            Cash_Inflows_PerYear = request.POST.get('Cash_Inflows_PerYear')
            Payback_Period = request.POST.get('Payback_Period')
            Subscription_Status = request.POST.get('Subscription_Status')
            Subscription_Quantity = request.POST.get('Subscription_Quantity')
            Subscription_Amount = request.POST.get('Subscription_Amount')
            Entry_Amount = request.POST.get('Entry_Amount')
            update_dic = {
                "PlanYear": PlanYear, "Customer": Customer, "BudgetCode": BudgetCode,
                "Investment_Nature": Investment_Nature,
                "Attribute_Code": Attribute_Code,
                "Application_Department": Application_Department,
                "Device_Name": Device_Name,
                "Usage_Description": Usage_Description,
                "Specifications": Specifications,
                "Acceptance_Month": Acceptance_Month,
                "Budget_Quantity": Budget_Quantity if Budget_Quantity != "null" else None,
                "Estimated_Original_Currency": Estimated_Original_Currency,
                "Estimated_Original_Price": Estimated_Original_Price,
                "Equivalent_To_RMB": Equivalent_To_RMB if Equivalent_To_RMB != "null" else None,
                "Payment_Terms": Payment_Terms,
                "Depreciation_Months": Depreciation_Months if Depreciation_Months != "null" else None,
                "Accounting_Subjects": Accounting_Subjects,
                "Automated_Or_Not": Automated_Or_Not,
                "Project_Code": Project_Code,
                "Current_Situation": Current_Situation,
                "Applicable_Scope": Applicable_Scope,
                "Investment_Purpose": Investment_Purpose,
                "Investment_Purpose_Des": Investment_Purpose_Des,
                "Potential_Issues": Potential_Issues,
                "Potential_Issues_Des": Potential_Issues_Des,
                "Tighten_Expenses": Tighten_Expenses,
                "Annual_Increase_PerYear": Annual_Increase_PerYear if Annual_Increase_PerYear != "null" else None,
                "Investment_Benefits_PerYear": Investment_Benefits_PerYear if Investment_Benefits_PerYear != "null" else None,
                "Cash_Inflows_PerYear": Cash_Inflows_PerYear if Cash_Inflows_PerYear != "null" else None,
                "Payback_Period": Payback_Period if Payback_Period != "null" else None,
                "Subscription_Status": Subscription_Status,
                "Subscription_Quantity": Subscription_Quantity if Subscription_Quantity != "null" else None,
                "Subscription_Amount": Subscription_Amount if Subscription_Amount != "null" else None,
                "Entry_Amount": Entry_Amount if Entry_Amount != "null" else None,
            }
            # print(update_dic)
            try:
                with transaction.atomic():
                    CapitalExpenditure.objects.filter(id=ID).update(**update_dic)
            except Exception as e:
                # alert = '此数据正被其他使用者编辑中...'
                alert = str(e)
                print(alert)

            # mock_data
            YearSearch = request.POST.get('searchYear')
            Customer = request.POST.get('Customer')
            for i in CapitalExpenditure.objects.exclude(Application_Department=None).filter(
                    PlanYear=YearSearch).annotate(
                first_seven=Substr(Upper('Application_Department'), 1, 7)).values('first_seven').distinct():
                # print(i['first_seven'], Departments.objects.filter(Department_Code__contains=i['first_seven']).first())
                CustomerToDepartmentSeven.append((Departments.objects.filter(Year=YearSearch,
                                                                             Department_Code__contains=i[
                                                                                 'first_seven']).first().Customer,
                                                  i['first_seven']))
            # print(CustomerToDepartmentSeven)
            DepartmentSeven = '部门代码没匹配到不能用空字符串会匹配到所有数据'
            for i in CustomerToDepartmentSeven:
                if Customer == i[0]:
                    DepartmentSeven = i[1]
                    break
            yearOptions = [
                # "2020", "2021", "2023"
            ]
            for i in CapitalExpenditure.objects.all().values("PlanYear").distinct().order_by("PlanYear"):
                yearOptions.append(i["PlanYear"])

            Check_dic_CapitalExpenditure = {}
            if YearSearch:
                Check_dic_CapitalExpenditure["PlanYear"] = YearSearch
            # elif YearSearch_backup:
            #     Check_dic_CapitalExpenditure["PlanYear"] = YearSearch_backup

            for i in CapitalExpenditure.objects.filter(**Check_dic_CapitalExpenditure):
                # print(i)
                mock_data.append(
                    {
                        "id": i.id, "PlanYear": i.PlanYear, "Customer": i.Customer, "BudgetCode": i.BudgetCode,
                        "Investment_Nature": i.Investment_Nature,
                        "Attribute_Code": i.Attribute_Code,
                        "Application_Department": i.Application_Department,
                        "Device_Name": i.Device_Name,
                        "Usage_Description": i.Usage_Description,
                        "Specifications": i.Specifications,
                        "Acceptance_Month": i.Acceptance_Month,
                        "Budget_Quantity": i.Budget_Quantity,
                        "Estimated_Original_Currency": i.Estimated_Original_Currency,
                        "Estimated_Original_Price": i.Estimated_Original_Price,
                        "Equivalent_To_RMB": i.Equivalent_To_RMB,
                        "Payment_Terms": i.Payment_Terms,
                        "Depreciation_Months": i.Depreciation_Months,
                        "Accounting_Subjects": i.Accounting_Subjects,
                        "Automated_Or_Not": i.Automated_Or_Not,
                        "Project_Code": i.Project_Code,
                        "Current_Situation": i.Current_Situation,
                        "Applicable_Scope": i.Applicable_Scope,
                        "Investment_Purpose": i.Investment_Purpose,
                        "Investment_Purpose_Des": i.Investment_Purpose_Des,
                        "Potential_Issues": i.Potential_Issues,
                        "Potential_Issues_Des": i.Potential_Issues_Des,
                        "Tighten_Expenses": i.Tighten_Expenses,
                        "Annual_Increase_PerYear": i.Annual_Increase_PerYear,
                        "Investment_Benefits_PerYear": i.Investment_Benefits_PerYear,
                        "Cash_Inflows_PerYear": i.Cash_Inflows_PerYear,
                        "Payback_Period": i.Payback_Period,
                        "Subscription_Status": i.Subscription_Status,
                        "Subscription_Quantity": i.Subscription_Quantity,
                        "Subscription_Amount": i.Subscription_Amount,
                        "Entry_Amount": i.Entry_Amount,
                    }
                )
            # tables
            if Customer == "C38":
                if C38CustomerT88AIODepartmentCode.objects.filter(Year=YearSearch) and DepartmentSeven:
                    AIOT88_DeparmentCode = C38CustomerT88AIODepartmentCode.objects.filter(
                        Year=YearSearch).first().Department_Code

                    if CapitalExpenditure.objects.filter(PlanYear=YearSearch):
                        tables_dic1 = {
                            "data": [
                                {"C38_T89": "數量",
                                 "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                    Application_Department__contains=DepartmentSeven).exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven).exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                     'total'] else 0,
                                 "Unsubscribed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="未申購").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Budget_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="未申購").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Budget_Quantity'))[
                                         'total'] else 0,
                                 "Subscription_In_Progress":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="申購中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="申購中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0,
                                 "During_Acceptance":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0,
                                 "Acceptance_Completed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收完成").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收完成").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0
                                 },
                                {"C38_T89": "金額(CNY)",
                                 "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                    Application_Department__contains=DepartmentSeven).exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven).exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] else 0,
                                 "Unsubscribed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="未申購").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="未申購").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] else 0,
                                 "Subscription_In_Progress":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="申購中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="申購中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0,
                                 "During_Acceptance":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收中").exclude(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0,
                                 "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                           Application_Department__contains=DepartmentSeven,
                                                                                           Subscription_Status="驗收完成").exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven,
                                                                                   Subscription_Status="驗收完成").exclude(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] else 0
                                 },
                            ],
                            "columns": [
                                {"prop": "C38_T89", "label": "C38 & T89"},
                                {"prop": "Annual_Budget", "label": "年度預算"},
                                {"prop": "Unsubscribed", "label": "未申購"},
                                {"prop": "Subscription_In_Progress", "label": "申購中"},
                                {"prop": "During_Acceptance", "label": "驗收中"},
                                {"prop": "Acceptance_Completed", "label": "驗收完成"},
                            ]
                        }

                        tables_dic2 = {
                            "data": [
                                {"T88_AIO": "數量",
                                 "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                    Application_Department__contains=DepartmentSeven).filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven).filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                                     'total'] else 0,
                                 "Unsubscribed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="未申購").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Budget_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="未申購").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Budget_Quantity'))[
                                         'total'] else 0,
                                 "Subscription_In_Progress":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="申購中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="申購中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0,
                                 "During_Acceptance":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0,
                                 "Acceptance_Completed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收完成").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收完成").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Quantity'))[
                                         'total'] else 0
                                 },
                                {"T88_AIO": "金額(CNY)",
                                 "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                    Application_Department__contains=DepartmentSeven).filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven).filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Equivalent_To_RMB'))[
                                     'total'] else 0,
                                 "Unsubscribed":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="未申購").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="未申購").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Equivalent_To_RMB'))[
                                         'total'] else 0,
                                 "Subscription_In_Progress":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="申購中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="申購中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0,
                                 "During_Acceptance":
                                     CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                       Application_Department__contains=DepartmentSeven,
                                                                       Subscription_Status="驗收中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                       Application_Department__contains=DepartmentSeven,
                                                                                       Subscription_Status="驗收中").filter(
                                         Application_Department=AIOT88_DeparmentCode).exclude(
                                         BudgetCode="預算外").aggregate(
                                         total=Sum('Subscription_Amount'))[
                                         'total'] else 0,
                                 "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                           Application_Department__contains=DepartmentSeven,
                                                                                           Subscription_Status="驗收完成").filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven,
                                                                                   Subscription_Status="驗收完成").filter(
                                     Application_Department=AIOT88_DeparmentCode).exclude(
                                     BudgetCode="預算外").aggregate(
                                     total=Sum('Subscription_Amount'))[
                                     'total'] else 0
                                 },
                            ],
                            "columns": [
                                {"prop": "T88_AIO", "label": "T88 AIO"},
                                {"prop": "Annual_Budget", "label": "年度預算"},
                                {"prop": "Unsubscribed", "label": "未申購"},
                                {"prop": "Subscription_In_Progress", "label": "申購中"},
                                {"prop": "During_Acceptance", "label": "驗收中"},
                                {"prop": "Acceptance_Completed", "label": "驗收完成"},
                            ]
                        }
                        tables.append(tables_dic1)
                        tables.append(tables_dic2)
                else:
                    errMsg = "没有该年的AIO部门代码，请先录入"

            else:
                tables_dic = {
                    "data": [
                        {Customer: "數量",
                         "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                            Application_Department__contains=DepartmentSeven, ).exclude(
                             BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven, ).exclude(
                             BudgetCode="預算外").aggregate(total=Sum('Budget_Quantity'))[
                             'total'] else 0,
                         "Unsubscribed":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="未申購").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Budget_Quantity'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="未申購").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Budget_Quantity'))[
                                 'total'] else 0,
                         "Subscription_In_Progress":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="申購中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="申購中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] else 0,
                         "During_Acceptance":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="驗收中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="驗收中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] else 0,
                         "Acceptance_Completed":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="驗收完成").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="驗收完成").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Quantity'))[
                                 'total'] else 0
                         },
                        {Customer: "金額(CNY)",
                         "Annual_Budget": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                            Application_Department__contains=DepartmentSeven).exclude(
                             BudgetCode="預算外").aggregate(
                             total=Sum('Equivalent_To_RMB'))[
                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven).exclude(
                             BudgetCode="預算外").aggregate(
                             total=Sum('Equivalent_To_RMB'))[
                             'total'] else 0,
                         "Unsubscribed":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="未申購").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Equivalent_To_RMB'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="未申購").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Equivalent_To_RMB'))[
                                 'total'] else 0,
                         "Subscription_In_Progress":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="申購中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="申購中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] else 0,
                         "During_Acceptance":
                             CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                               Application_Department__contains=DepartmentSeven,
                                                               Subscription_Status="驗收中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                               Application_Department__contains=DepartmentSeven,
                                                                               Subscription_Status="驗收中").exclude(
                                 BudgetCode="預算外").aggregate(
                                 total=Sum('Subscription_Amount'))[
                                 'total'] else 0,
                         "Acceptance_Completed": CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                                   Application_Department__contains=DepartmentSeven,
                                                                                   Subscription_Status="驗收完成").exclude(
                             BudgetCode="預算外").aggregate(
                             total=Sum('Subscription_Amount'))[
                             'total'] if CapitalExpenditure.objects.filter(PlanYear=YearSearch,
                                                                           Application_Department__contains=DepartmentSeven,
                                                                           Subscription_Status="驗收完成").exclude(
                             BudgetCode="預算外").aggregate(
                             total=Sum('Subscription_Amount'))[
                             'total'] else 0
                         },
                    ],
                    "columns": [
                        {"prop": Customer, "label": Customer},
                        {"prop": "Annual_Budget", "label": "年度預算"},
                        {"prop": "Unsubscribed", "label": "未申購"},
                        {"prop": "Subscription_In_Progress", "label": "申購中"},
                        {"prop": "During_Acceptance", "label": "驗收中"},
                        {"prop": "Acceptance_Completed", "label": "驗收完成"},
                    ]
                }
                tables.append(tables_dic)
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'MUTIDELETE' in str(request.body):
                    responseData = json.loads(request.body)
                    Year = responseData["Year"]
                    # for i in responseData['params']:
                    #     ProjectPlan.objects.get(id=i).delete()
                    # print(Year)
                    try:
                        with transaction.atomic():
                            CapitalExpenditure.objects.filter(PlanYear=Year).delete()
                    except Exception as e:
                        # alert = '此数据正被其他使用者编辑中...'
                        alert = str(e)
                        print(alert)
                    # mock_data
                    yearOptions = [
                        # "2020", "2021", "2023"
                    ]
                    for i in CapitalExpenditure.objects.all().values("PlanYear").distinct().order_by("PlanYear"):
                        yearOptions.append(i["PlanYear"])

                    Check_dic_CapitalExpenditure = {}
                    YearSearch = request.POST.get('Year')
                    DataTypeSearch = request.POST.get('DataType')
                    if YearSearch:
                        Check_dic_CapitalExpenditure["PlanYear"] = YearSearch
                    # print(Check_dic_CapitalExpenditure)
                    for i in CapitalExpenditure.objects.filter(**Check_dic_CapitalExpenditure):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "PlanYear": i.PlanYear, "Customer": i.Customer, "BudgetCode": i.BudgetCode,
                                "Investment_Nature": i.Investment_Nature,
                                "Attribute_Code": i.Attribute_Code,
                                "Application_Department": i.Application_Department,
                                "Device_Name": i.Device_Name,
                                "Usage_Description": i.Usage_Description,
                                "Specifications": i.Specifications,
                                "Acceptance_Month": i.Acceptance_Month,
                                "Budget_Quantity": i.Budget_Quantity,
                                "Estimated_Original_Currency": i.Estimated_Original_Currency,
                                "Estimated_Original_Price": i.Estimated_Original_Price,
                                "Equivalent_To_RMB": i.Equivalent_To_RMB,
                                "Payment_Terms": i.Payment_Terms,
                                "Depreciation_Months": i.Depreciation_Months,
                                "Accounting_Subjects": i.Accounting_Subjects,
                                "Automated_Or_Not": i.Automated_Or_Not,
                                "Project_Code": i.Project_Code,
                                "Current_Situation": i.Current_Situation,
                                "Applicable_Scope": i.Applicable_Scope,
                                "Investment_Purpose": i.Investment_Purpose,
                                "Investment_Purpose_Des": i.Investment_Purpose_Des,
                                "Potential_Issues": i.Potential_Issues,
                                "Potential_Issues_Des": i.Potential_Issues_Des,
                                "Tighten_Expenses": i.Tighten_Expenses,
                                "Annual_Increase_PerYear": i.Annual_Increase_PerYear,
                                "Investment_Benefits_PerYear": i.Investment_Benefits_PerYear,
                                "Cash_Inflows_PerYear": i.Cash_Inflows_PerYear,
                                "Payback_Period": i.Payback_Period,
                                "Subscription_Status": i.Subscription_Status,
                                "Subscription_Quantity": i.Subscription_Quantity,
                                "Subscription_Amount": i.Subscription_Amount,
                                "Entry_Amount": i.Entry_Amount,
                            }
                        )

                elif 'upload' in str(request.body):

                    responseData = json.loads(request.body)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    YearSearch = responseData['Year']
                    YearSearch_backup = ''

                    # xlsxlist = json.loads(responseData['ExcelData'])[2:]#excel模板有三级表头
                    xlsxlist = json.loads(responseData['ExcelData'])#tool模板，只有一级表头
                    print(xlsxlist)
                    # pprint.pprint(xlsxlist)
                    # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                    # Check_dic_Project = {'Customer': CustomerSearch, 'Project': ProjectSearch, }
                    # # print(Check_dic_ProjectCQM)
                    # Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                    # print(Projectinfo)
                    # current_user = request.session.get('user_name')
                    # current_account = request.session.get('account')
                    # ProjectComparison_admin_user = "0301507" #Canny
                    # # if Projectinfo:s
                    # #                     #     for k in Projectinfo.Owner.all():
                    # #                     #         # print(k.username,current_user)
                    # #                     #         # print(type(k.username),type(current_user))
                    # #                     #         if k.username == current_uer:
                    # #             canEdit = 1
                    # #             break
                    # if current_account == ProjectComparison_admin_user:
                    #     canEdit = 1
                    # print(canEdit)
                    # try:
                    if permission:
                        rownum = 0
                        startupload = 0
                        # print(xlsxlist)
                        create_list = []
                        for i in xlsxlist:
                            # print(type(i),i)
                            rownum += 1
                            modeldata = {}
                            # print(headermodel_CapitalExpenditure.keys())
                            for key, value in i.items():
                                if key in headermodel_CapitalExpenditure.keys():
                                    # print(headermodel_CapitalExpenditure[key],value)
                                    modeldata[headermodel_CapitalExpenditure[key]] = value
                            # print(modeldata)

                            if 'PlanYear' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，PlanYear不能爲空
                                                            """ % rownum
                                break
                            if 'BudgetCode' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，BudgetCode不能爲空
                                                            """ % rownum
                                break

                            create_list.append(CapitalExpenditure(**modeldata))  # object(**dict)
                            if rownum == 1:
                                YearSearch_backup = modeldata['PlanYear']
                                # print(modeldata['Year'])
                        # print(errMsg, startupload)
                        # print(create_list, )
                        # print(startupload)
                        # print(rownum, type(rownum))
                        if startupload:
                            try:
                                with transaction.atomic():
                                    CapitalExpenditure.objects.bulk_create(create_list)
                            except Exception as e:
                                # alert = '此数据正被其他使用者编辑中...'
                                alert = str(e)
                                print(alert)

                    # print('IssuesBreakdown')
                    # mock_data
                    yearOptions = [
                        # "2020", "2021", "2023"
                    ]
                    for i in CapitalExpenditure.objects.all().values("PlanYear").distinct().order_by("PlanYear"):
                        yearOptions.append(i["PlanYear"])

                    Check_dic_CapitalExpenditure = {}
                    if YearSearch:
                        Check_dic_CapitalExpenditure["PlanYear"] = YearSearch
                    elif YearSearch_backup:
                        Check_dic_CapitalExpenditure["PlanYear"] = YearSearch_backup

                    for i in CapitalExpenditure.objects.filter(**Check_dic_CapitalExpenditure):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "PlanYear": i.PlanYear, "Customer": i.Customer, "BudgetCode": i.BudgetCode,
                                "Investment_Nature": i.Investment_Nature,
                                "Attribute_Code": i.Attribute_Code,
                                "Application_Department": i.Application_Department,
                                "Device_Name": i.Device_Name,
                                "Usage_Description": i.Usage_Description,
                                "Specifications": i.Specifications,
                                "Acceptance_Month": i.Acceptance_Month,
                                "Budget_Quantity": i.Budget_Quantity,
                                "Estimated_Original_Currency": i.Estimated_Original_Currency,
                                "Estimated_Original_Price": i.Estimated_Original_Price,
                                "Equivalent_To_RMB": i.Equivalent_To_RMB,
                                "Payment_Terms": i.Payment_Terms,
                                "Depreciation_Months": i.Depreciation_Months,
                                "Accounting_Subjects": i.Accounting_Subjects,
                                "Automated_Or_Not": i.Automated_Or_Not,
                                "Project_Code": i.Project_Code,
                                "Current_Situation": i.Current_Situation,
                                "Applicable_Scope": i.Applicable_Scope,
                                "Investment_Purpose": i.Investment_Purpose,
                                "Investment_Purpose_Des": i.Investment_Purpose_Des,
                                "Potential_Issues": i.Potential_Issues,
                                "Potential_Issues_Des": i.Potential_Issues_Des,
                                "Tighten_Expenses": i.Tighten_Expenses,
                                "Annual_Increase_PerYear": i.Annual_Increase_PerYear,
                                "Investment_Benefits_PerYear": i.Investment_Benefits_PerYear,
                                "Cash_Inflows_PerYear": i.Cash_Inflows_PerYear,
                                "Payback_Period": i.Payback_Period,
                                "Subscription_Status": i.Subscription_Status,
                                "Subscription_Quantity": i.Subscription_Quantity,
                                "Subscription_Amount": i.Subscription_Amount,
                                "Entry_Amount": i.Entry_Amount,
                            }
                        )
                    # except Exception as e:
                    #     errMsg = str(e)
        for i in tables:
            for j in i["data"]:
                for key, value in j.items():
                    try:
                        float(value)
                        j[key] = round(value)
                    except Exception as e:
                        print(str(e))

        data = {
            "errMsg": errMsg,
            "yearOptions": yearOptions,
            # "datatypeOption": datatypeOption,
            "content": mock_data,
            "permission": permission,
            "tables": tables,
            "customerOptions": CustomerOption,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CapitalExpenditure/CapitalExpenditure_Summary.html', locals())
