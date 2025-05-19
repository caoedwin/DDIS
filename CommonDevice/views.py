from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime, json, simplejson, requests, time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import UserInfo
from django.db.models import Max, Min, Sum, Count, Q, F, Value, CharField
from django.db.models.functions import Substr
from operator import itemgetter, attrgetter
from collections import Counter
from .models import CommonDevice
from django.db.models.functions import ExtractYear


@csrf_exempt
def CommonDevice_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DepartmentManage/公共設備"
    categoryOptions = [
        # "網絡設備1", "網絡設備2"
    ]
    for i in CommonDevice.objects.all().values('Category').distinct():
        categoryOptions.append(
            i['Category']
        )

    ProductTypeOptions = [
        # "智慧家庭", "宽带"
                          ]
    for i in CommonDevice.objects.all().values('Product_Type').distinct():
        ProductTypeOptions.append(
            i['Product_Type']
        )

    sectionOwner = [
        # {"value": "姚麗麗", "number": "22314345"}, {"value": "張亞萍", "number": "123456789"},
    ]
    for i in UserInfo.objects.all():
        sectionOwner.append(
            {
                "value": i.username, "number": i.account
            }
        )

    # classOptions = ["Sensor test device", "USB Keyboard", "USB Mouse"]

    # DeviceOptions = [
    #     {"key": "姚丽丽", "label": "2222222"},
    #     {"key": "张颖", "label": "1111111"},
    # ]

    OwnersOptions = [
        # {"key": "姚丽丽", "label": "2222222"},
        # {"key": "张颖", "label": "1111111"},
    ]
    for i in UserInfo.objects.all():
        OwnersOptions.append(
            {
                "key": i.username, "label": i.account
            }
        )

    mock_data = [
        # {"id": "1", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
        #
        # {"id": "2", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
        #
        # {"id": "3", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
    ]

    errMsg = ''
    permission = 1  # 權限  0是有權限 其他數字沒有權限
    roles = []
    onlineuser = request.session.get('account')
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    # for i in roles:
    #     if i == 'admin' or i == 'PublicAreaAdmin':
    #         permission = 0
    mock_obj = CommonDevice.objects.all()
    if request.method == "POST":
        if request.POST:
            ch_dic = {}
            if request.POST.get('isGetData') == 'SEARCH':
                if request.POST.get('Category'):
                    ch_dic['Category'] = request.POST.get('Category')
                if request.POST.get('Owner'):
                    user = UserInfo.objects.filter(account=request.POST.get('OwnerNumber')).first()
                    ch_dic['Owner'] = user
                if ch_dic:
                    mock_obj = CommonDevice.objects.filter(**ch_dic)
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'Delete' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData['DeleteId'])
                    pass

        # mock_data
        for i in mock_obj:
            Duration = ''
            if i.Purchasing_Date:
                if datetime.datetime.now().date() > i.Purchasing_Date:
                    Useyears = round(
                        float(
                            str((datetime.datetime.now().date() - i.Purchasing_Date)).split(' ')[
                                0]) / 365,
                        1)
            Owner_list = []
            Ownerflag = False
            for j in i.Owner.all():
                Owner_list.append([j.username, j.account])
                if not Ownerflag:
                    if j.account == onlineuser:
                        Ownerflag = True

            mock_data.append(
                {
                    "id": i.id, "Category": i.Category, "Product_Type": i.Product_Type,
                    "Name": i.Name,
                    "Num": i.Num,
                    "Manufacturer": i.Manufacturer,
                    "Cost": i.Cost,
                    "Account": i.Account,
                    "PW": i.PW,
                    "Purchasing_Date": str(i.Purchasing_Date) if i.Purchasing_Date else '',
                    "Duration": Duration,
                    "Department": i.Department,
                    "Asset_Num": i.Asset_Num,
                    "Owner": Owner_list,
                    "Mail": i.Mail,
                    "Contact_info": i.Contact_info,
                    "Comments": i.Comments,
                    "Creator": i.Creator,
                    # "Ownerflag": i.Creator == onlineuser, creator才有权限。
                    "Ownerflag": Ownerflag, # 只要是Owner中的一个有权限，Owner改变了权限就会随之变化
                }
            )

        data = {
            "errMsg": errMsg,
            "categoryOptions": categoryOptions,
            "ProductTypeOptions": ProductTypeOptions,
            # "classOptions": classOptions,
            "sectionOwner": sectionOwner,
            # "DeviceOptions": DeviceOptions,
            "OwnersOptions": OwnersOptions,
            "content": mock_data,
            "permission": permission,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CommonDevice/CommonDevice.html', locals())

