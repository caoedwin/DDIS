from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from app01.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
import datetime, os
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Sum, F, Value

import datetime, json


# Create your views here.


@csrf_exempt
def SubscriptionStatus_view(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "杂项购置/状况"
    onlineuser = request.session.get('account')
    mock_data = [
        # {"Year": "預算", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950", "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950", "Total": "1111111"},
        # {"Year": "實際入賬", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950", "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950",
        #  "Nov": "69950",
        #  "Dec": "69950", "Total": "1111111"},
        # {"Year": "申購金額", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950", "Total": "1111111"},

    ]

    mock_data1 = [
        # {"id": "1", "Year": "2025", "Ledger": 6202, "Name": "飛利浦HDMI2.1傳輸線", "Status": "Cancel",
        #  "ModelSpecifications": "SWL4281B/93",
        #  "SubscribeDate": "2025-01-06", "AcceptanceForm": "xxxxxxxx", "AcceptanceDate": "2025-01-06",
        #  "SubscribeForm": "R230317015",
        #  "SubscribeUnitPrice": "277", "Number": 1, "TotalPrice": 277, "Customer": "C38", "ProjectCode": "INRG000000",
        #  "Department": "DQA二部三課", "Requisitioner": "陳媛", "editPermission": 0,
        #  },
        # {"id": "2", "Year": "2025", "Ledger": 6202, "Name": "飛利浦HDMI2.1傳輸線", "Status": "Cancel",
        #  "ModelSpecifications": "SWL4281B/93",
        #  "SubscribeDate": "2025-01-06", "AcceptanceForm": "xxxxxxxx", "AcceptanceDate": "2025-01-06",
        #  "SubscribeForm": "R230317015",
        #  "SubscribeUnitPrice": "277", "Number": 1, "TotalPrice": 277, "Customer": "C38", "ProjectCode": "INRG000000",
        #  "Department": "DQA二部三課", "Requisitioner": "陳媛", "editPermission": 0,
        #  },
        # {"id": "3", "Year": "2025", "Ledger": 6202, "Name": "飛利浦HDMI2.1傳輸線", "Status": "Cancel",
        #  "ModelSpecifications": "SWL4281B/93",
        #  "SubscribeDate": "2025-01-06", "AcceptanceForm": "xxxxxxxx", "AcceptanceDate": "2025-01-06",
        #  "SubscribeForm": "R230317015",
        #  "SubscribeUnitPrice": "277", "Number": 1, "TotalPrice": 277, "Customer": "C38", "ProjectCode": "INRG000000",
        #  "Department": "DQA二部三課", "Requisitioner": "陳媛", "editPermission": 1,
        #  },

    ]

    yearOptions = [
        # "2019", "2020", "2021"
    ]
    for i in SubscriptionStatus.objects.all().values("Year").distinct().order_by("Year"):
        yearOptions.append(i["Year"])
    ledgerOptions = [
        # "6202", "6203", "6204"
                     ]
    for i in SubscriptionStatus.objects.all().values("Ledger").distinct().order_by("Ledger"):
        ledgerOptions.append(i["Ledger"])

    errMessage = ""
    editPermission = 1  # 1:可编辑 0:不可编辑

    YearSearch = ''
    LedgerSearch = ''
    chedcic = {}

    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            pass
        if request.POST.get("isGetData") == "SEARCH":
            YearSearch = request.POST.get("Year")
            LedgerSearch = request.POST.get("Ledger")
        if request.POST.get("action") == "addSubmit":
            YearSearch = request.POST.get("searchYear")
            LedgerSearch = request.POST.get("searchLedger")
            Add_dic = {
                "Year": request.POST.get("Year"),
                "Ledger": request.POST.get("Ledger"),
                "Name": request.POST.get("Name"),
                "Status": request.POST.get("Status"),
                "ModelSpecifications": request.POST.get("ModelSpecifications"),
                "SubscribeDate": request.POST.get("SubscribeDate"),
                "SubscribeForm": request.POST.get("SubscribeForm"),
                "SubscribeUnitPrice": request.POST.get("SubscribeUnitPrice"),
                "Number": request.POST.get("Number"),
                "AcceptanceForm": request.POST.get("AcceptanceForm"),
                "AcceptanceDate": request.POST.get("AcceptanceDate"),
                # "ActUnitPrice": request.POST.get("ActUnitPrice"),
                "Customer": request.POST.get("Customer"),
                "ProjectCode": request.POST.get("ProjectCode"),
                "Department": request.POST.get("Department"),
                "RequisitionerNum": request.session.get('account'),
                "Requisitioner": request.session.get('user_name'),
            }
            # print(Add_dic)
            SubscriptionStatus.objects.create(**Add_dic)
        if request.POST.get("action") == "updateSubmit":
            editID = request.POST.get("editID")
            YearSearch = request.POST.get("searchYear")
            LedgerSearch = request.POST.get("searchLedger")
            update_dic = {
                "Year": request.POST.get("Year"),
                "Ledger": request.POST.get("Ledger"),
                "Name": request.POST.get("Name"),
                "Status": request.POST.get("Status"),
                "ModelSpecifications": request.POST.get("ModelSpecifications"),
                "SubscribeDate": request.POST.get("SubscribeDate"),
                "SubscribeForm": request.POST.get("SubscribeForm"),
                "SubscribeUnitPrice": request.POST.get("SubscribeUnitPrice"),
                "Number": request.POST.get("Number"),
                "AcceptanceForm": request.POST.get("AcceptanceForm"),
                "AcceptanceDate": request.POST.get("AcceptanceDate"),
                # "ActUnitPrice": request.POST.get("ActUnitPrice"),
                "Customer": request.POST.get("Customer"),
                "ProjectCode": request.POST.get("ProjectCode"),
                "Department": request.POST.get("Department"),
                "RequisitionerNum": request.session.get('account'),
                "Requisitioner": request.session.get('user_name'),
            }
            # print(update_dic)
            SubscriptionStatus.objects.filter(id=editID).update(**update_dic)

        if YearSearch and LedgerSearch:
            # mock_data
            for i in Budget.objects.filter(Year=YearSearch, Ledger=LedgerSearch):
                mock_data.append(
                    {
                        "Year": "預算", "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May,
                         "Jun": i.Jun, "July": i.Jul, "Aug": i.Aug, "Sep": i.Sep, "Oct": i.Oct, "Nov": i.Nov,
                         "Dec": i.Dec,
                        # "Total": i.Jan + i.Feb + i.Mar + i.Apr + i.May + i.Jun + i.Jul + i.Aug + i.Sep + i.Oct + i.Nov + i.Dec
                    }
                )
                Total_Budget = 0
                if i.Jan:
                    Total_Budget += i.Jan
                if i.Feb:
                    Total_Budget += i.Feb
                if i.Mar:
                    Total_Budget += i.Mar
                if i.Apr:
                    Total_Budget += i.Apr
                if i.May:
                    Total_Budget += i.May
                if i.Jun:
                    Total_Budget += i.Jun
                if i.Jul:
                    Total_Budget += i.Jul
                if i.Aug:
                    Total_Budget += i.Aug
                if i.Sep:
                    Total_Budget += i.Sep
                if i.Oct:
                    Total_Budget += i.Oct
                if i.Nov:
                    Total_Budget += i.Nov
                if i.Dec:
                    Total_Budget += i.Dec
                mock_data[0]["Total"] = Total_Budget
            for i in ReceiptAmount.objects.filter(Year=YearSearch, Ledger=LedgerSearch):
                mock_data.append(
                    {
                        "Year": "實際入賬", "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May,
                         "Jun": i.Jun, "July": i.Jul, "Aug": i.Aug, "Sep": i.Sep, "Oct": i.Oct, "Nov": i.Nov,
                         "Dec": i.Dec,
                        # "Total": i.Jan + i.Feb + i.Mar + i.Apr + i.May + i.Jun + i.Jul + i.Aug + i.Sep + i.Oct + i.Nov + i.Dec
                    }
                )
                Total_ReceiptAmount = 0
                if i.Jan:
                    Total_ReceiptAmount += i.Jan
                if i.Feb:
                    Total_ReceiptAmount += i.Feb
                if i.Mar:
                    Total_ReceiptAmount += i.Mar
                if i.Apr:
                    Total_ReceiptAmount += i.Apr
                if i.May:
                    Total_ReceiptAmount += i.May
                if i.Jun:
                    Total_ReceiptAmount += i.Jun
                if i.Jul:
                    Total_ReceiptAmount += i.Jul
                if i.Aug:
                    Total_ReceiptAmount += i.Aug
                if i.Sep:
                    Total_ReceiptAmount += i.Sep
                if i.Oct:
                    Total_ReceiptAmount += i.Oct
                if i.Nov:
                    Total_ReceiptAmount += i.Nov
                if i.Dec:
                    Total_ReceiptAmount += i.Dec
                mock_data[1]["Total"] = Total_ReceiptAmount
            shengoujine = {"Year": "申購金額"}
            Shengou_Total = 0
            # 按年份和月份分组，并计算总金额
            monthly_totals = SubscriptionStatus.objects.exclude(Status="Cancel").annotate(
                year=ExtractYear('SubscribeDate'),
                month=ExtractMonth('SubscribeDate')
            ).values('year', 'month').annotate(total=Sum(F('SubscribeUnitPrice') * F('Number'), output_field=models.FloatField()))
            Mounthlist = [
                ("Jan", 1), ("Feb", 2), ("Mar", 3), ("Apr", 4), ("May", 5), ("July", 6), ("Jul", 7), ("Aug", 8), ("Sep", 9), ("Oct", 10), ("Nov", 11), ("Dec", 12),
            ]

            for monthly_total in monthly_totals:
                Shengou_Total +=  monthly_total['total']
                for j in Mounthlist:
                    if monthly_total['month'] == j[1]:
                        shengoujine[j[0]] = monthly_total['total']
                        continue
                # print(f"Year: {monthly_total['year']}, Month: {monthly_total['month']}, Total: {monthly_total['total']}")
            shengoujine["Total"] = Shengou_Total
            mock_data.append(shengoujine)

            if YearSearch:
                chedcic['Year'] = YearSearch
            if LedgerSearch:
                chedcic['Ledger'] = LedgerSearch
            datas = SubscriptionStatus.objects.filter(**chedcic)

        else:
            datas = SubscriptionStatus.objects.all()
        # mock_data1
        for i in datas:
            mock_data1.append(
                {
                    "id": i.id,
                    "Year": i.Year,
                    "Ledger": i.Ledger,
                    "Name": i.Name,
                    "Status": i.Status,
                    "ModelSpecifications": i.ModelSpecifications,
                    "SubscribeDate": str(i.SubscribeDate),
                    "SubscribeForm": i.SubscribeForm,
                    "SubscribeUnitPrice": i.SubscribeUnitPrice,
                    "Number": i.Number,
                    "AcceptanceForm": i.AcceptanceForm,
                    "AcceptanceDate": str(i.AcceptanceDate),
                    "ActUnitPrice": i.ActUnitPrice,
                    "Customer": i.Customer,
                    "ProjectCode": i.ProjectCode,
                    "Department": i.Department,
                    "RequisitionerNum": i.RequisitionerNum,
                    "Requisitioner": i.Requisitioner,
                    "editPermission": 1 if request.session.get('account') == i.RequisitionerNum else 0
                },
            )
        # print(mock_data1)


        data = {
            "content": mock_data,
            "content1": mock_data1,
            "errMessage": errMessage,
            "editPermission": editPermission,
            "yearOptions": yearOptions,
            "ledgerOptions": ledgerOptions,
        }
        # print(updateData)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'MiscellaneousPurchases/SubscriptionStatus.html', locals())

@csrf_exempt
def Budget_view(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "杂项购置/预算"

    yearOptions = [
        # "2020", "2021", "2023"
                   ]


    mock_data = [
        # {"id": "1", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},
        # {"id": "2", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},
        # {"id": "3", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},

    ]

    errMsg = ''
    # mock_data
    YearSearch = str(datetime.datetime.now().year)
    # print(YearSearch)
    mock_data_obj = Budget.objects.filter(Year=YearSearch)

    if request.method == 'POST':
        if request.POST.get('isGetData') == "first":
            pass
        if request.POST.get('isGetData') == "SEARCH":
            YearSearch = request.POST.get('Year')
            mock_data_obj = Budget.objects.filter(Year=YearSearch)
        if request.POST.get('action') == "addData":
            YearSearch = request.POST.get('searchYear')
            Year = request.POST.get('Year')
            Ledger = request.POST.get('Ledger')
            check_dic = {"Year": Year, "Ledger": Ledger, }
            if Year and Ledger:
                if Budget.objects.filter(**check_dic):
                    errMsg = "%s-%s预算已经存在" % (Year, Ledger)
                else:
                    add_dic = {
                       "Year": Year, "Ledger": Ledger, "Jan": request.POST.get('Jan'),
                        "Feb": request.POST.get('Feb'), "Mar": request.POST.get('Mar'),  "Apr": request.POST.get('Apr'),
                        "May": request.POST.get('May'), "Jun": request.POST.get('Jun'),  "Jul": request.POST.get('July'),
                        "Aug": request.POST.get('Aug'), "Sep": request.POST.get('Sep'),  "Oct": request.POST.get('Oct'),
                        "Nov": request.POST.get('Nov'), "Dec": request.POST.get('Dec'),
                    }
                    Budget.objects.create(**add_dic)

            else:
                errMsg = "Year和会计科目不能为空"
            if YearSearch:
                mock_data_obj = Budget.objects.filter(Year=YearSearch)
        if request.POST.get('action') == "update":
            YearSearch = request.POST.get('searchYear')
            ID = request.POST.get('ID')
            # Year = request.POST.get('Year')
            # Ledger = request.POST.get('Ledger')
            update_dic = {
               "Jan": request.POST.get('Jan'),
                "Feb": request.POST.get('Feb'), "Mar": request.POST.get('Mar'),  "Apr": request.POST.get('Apr'),
                "May": request.POST.get('May'), "Jun": request.POST.get('Jun'),  "Jul": request.POST.get('July'),
                "Aug": request.POST.get('Aug'), "Sep": request.POST.get('Sep'),  "Oct": request.POST.get('Oct'),
                "Nov": request.POST.get('Nov'), "Dec": request.POST.get('Dec'),
            }
            Budget.objects.filter(id=ID).update(**update_dic)
            if YearSearch:
                mock_data_obj = Budget.objects.filter(Year=YearSearch)
        # mock_data
        for i in Budget.objects.all().values("Year").distinct().order_by("Year"):
            yearOptions.append(i['Year'])
        for i in mock_data_obj:
            mock_data.append(
                {"id": i.id, "Year": i.Year, "Ledger": i.Ledger, "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar,
                 "Apr": i.Apr,
                 "May": i.May,
                 "Jun": i.Jun, "July": i.Jul, "Aug": i.Aug, "Sep": i.Sep, "Oct": i.Oct, "Nov": i.Nov,
                 "Dec": i.Dec},
            )
        data = {
            "errMsg": errMsg,
            "yearOptions": yearOptions,
            "content": mock_data,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'MiscellaneousPurchases/Budget.html', locals())

@csrf_exempt
def ReceiptAmount_view(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    weizhi = "杂项购置/入賬"
    # print(Skin)
    yearOptions = [
        # "2020", "2021", "2023"
    ]

    mock_data = [
        # {"id": "1", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},
        # {"id": "2", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},
        # {"id": "3", "Year": "2024", "Ledger": "6202", "Jan": "69950", "Feb": "69950", "Mar": "69950", "Apr": "69950",
        #  "May": "69950",
        #  "Jun": "69950", "July": "69950", "Aug": "69950", "Sep": "69950", "Oct": "69950", "Nov": "69950",
        #  "Dec": "69950"},

    ]

    errMsg = ''
    # mock_data
    YearSearch = str(datetime.datetime.now().year)
    # print(YearSearch)
    mock_data_obj = ReceiptAmount.objects.filter(Year=YearSearch)

    if request.method == 'POST':
        if request.POST.get('isGetData') == "first":
            pass
        if request.POST.get('isGetData') == "SEARCH":
            YearSearch = request.POST.get('Year')
            mock_data_obj = ReceiptAmount.objects.filter(Year=YearSearch)
        if request.POST.get('action') == "addData":
            YearSearch = request.POST.get('searchYear')
            Year = request.POST.get('Year')
            Ledger = request.POST.get('Ledger')
            check_dic = {"Year": Year, "Ledger": Ledger, }
            if Year and Ledger:
                if ReceiptAmount.objects.filter(**check_dic):
                    errMsg = "%s-%s预算已经存在" % (Year, Ledger)
                else:
                    add_dic = {
                        "Year": Year, "Ledger": Ledger, "Jan": request.POST.get('Jan'),
                        "Feb": request.POST.get('Feb'), "Mar": request.POST.get('Mar'), "Apr": request.POST.get('Apr'),
                        "May": request.POST.get('May'), "Jun": request.POST.get('Jun'), "Jul": request.POST.get('July'),
                        "Aug": request.POST.get('Aug'), "Sep": request.POST.get('Sep'), "Oct": request.POST.get('Oct'),
                        "Nov": request.POST.get('Nov'), "Dec": request.POST.get('Dec'),
                    }
                    ReceiptAmount.objects.create(**add_dic)

            else:
                errMsg = "Year和会计科目不能为空"
            if YearSearch:
                mock_data_obj = ReceiptAmount.objects.filter(Year=YearSearch)
        if request.POST.get('action') == "update":
            YearSearch = request.POST.get('searchYear')
            ID = request.POST.get('ID')
            # Year = request.POST.get('Year')
            # Ledger = request.POST.get('Ledger')
            print(request.POST.get('Dec'), type(request.POST.get('Dec')))
            update_dic = {
                "Jan": request.POST.get('Jan') if request.POST.get('Jan') else None,
                "Feb": request.POST.get('Feb') if request.POST.get('Feb') else None,
                "Mar": request.POST.get('Mar') if request.POST.get('Mar') else None,
                "Apr": request.POST.get('Apr') if request.POST.get('Apr') else None,
                "May": request.POST.get('May') if request.POST.get('May') else None,
                "Jun": request.POST.get('Jun') if request.POST.get('Jun') else None,
                "Jul": request.POST.get('July') if request.POST.get('July') else None,
                "Aug": request.POST.get('Aug') if request.POST.get('Aug') else None,
                "Sep": request.POST.get('Sep') if request.POST.get('Sep') else None,
                "Oct": request.POST.get('Oct') if request.POST.get('Oct') else None,
                "Nov": request.POST.get('Nov') if request.POST.get('Nov') else None,
                "Dec": request.POST.get('Dec') if request.POST.get('Dec') else None,
            }
            ReceiptAmount.objects.filter(id=ID).update(**update_dic)
            if YearSearch:
                mock_data_obj = ReceiptAmount.objects.filter(Year=YearSearch)
        # mock_data
        for i in ReceiptAmount.objects.all().values("Year").distinct().order_by("Year"):
            yearOptions.append(i['Year'])
        for i in mock_data_obj:
            mock_data.append(
                {"id": i.id, "Year": i.Year, "Ledger": i.Ledger, "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar,
                 "Apr": i.Apr,
                 "May": i.May,
                 "Jun": i.Jun, "July": i.Jul, "Aug": i.Aug, "Sep": i.Sep, "Oct": i.Oct, "Nov": i.Nov,
                 "Dec": i.Dec},
            )
        data = {
            "errMsg": errMsg,
            "yearOptions": yearOptions,
            "content": mock_data,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'MiscellaneousPurchases/ReceiptAmount.html', locals())