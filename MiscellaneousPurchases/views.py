from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from app01.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
import datetime, os

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

    mock_data = []
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            pass
        if request.POST.get("isGetData") == "Search":
            Year = request.POST.get("Year")
            Ledger = request.POST.get("Ledger")
            chedcic = {}

            if Year:
                chedcic['Year'] = Year
            if Ledger:
                chedcic['Ledger'] = Ledger
            # mock_data
            if chedcic:
                datas = SubscriptionStatus.objects.filter(**chedcic)
            else:
                datas = SubscriptionStatus.objects.all()

            for i in datas:
                mock_data.append(
                    {
                        "id": i.id,
                        "Year": i.Year,
                        "Ledger": i.Ledger,
                        "Name": i.Name,
                        "Status": i.Status,
                        "ModelSpecifications": i.ModelSpecifications,
                        "SubscribeDate": i.SubscribeDate,
                        "SubscribeForm": i.SubscribeForm,
                        "SubscribeUnitPrice": i.SubscribeUnitPrice,
                        "Number": i.Number,
                        "AcceptanceForm": i.AcceptanceForm,
                        "AcceptanceDate": i.AcceptanceDate,
                        "ActUnitPrice": i.ActUnitPrice,
                        "Customer": i.Customer,
                        "ProjectCode": i.ProjectCode,
                        "Department": i.Department,
                        "RequisitionerNum": i.RequisitionerNum,
                        "Requisitioner": i.Requisitioner,
                        "Ownerflag": 1 if request.session.get('account') == i.RequisitionerNum else 0
                    },
                )



        data = {
            #     'fileList': fileList
            'content': mock_data,
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
            update_dic = {
                "Jan": request.POST.get('Jan'),
                "Feb": request.POST.get('Feb'), "Mar": request.POST.get('Mar'), "Apr": request.POST.get('Apr'),
                "May": request.POST.get('May'), "Jun": request.POST.get('Jun'), "Jul": request.POST.get('July'),
                "Aug": request.POST.get('Aug'), "Sep": request.POST.get('Sep'), "Oct": request.POST.get('Oct'),
                "Nov": request.POST.get('Nov'), "Dec": request.POST.get('Dec'),
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