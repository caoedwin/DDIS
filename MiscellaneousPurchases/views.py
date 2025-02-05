from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from app01.models import UserInfo
from django.views.decorators.csrf import csrf_exempt
import datetime, os

import datetime, json


# Create your views here.


@csrf_exempt
def SubscriptionStatus(request):
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

def Budget(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "杂项购置/预算"


    if request.method == "POST":
        pass

    return render(request, 'MiscellaneousPurchases/Budget.html', locals())


def ReceiptAmount(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "杂项购置/入账金额"

    if request.method == "POST":
        pass

    return render(request, 'MiscellaneousPurchases/ReceiptAmount.html', locals())