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
    permission = 1  # 權限  0是有權限 其他數字沒有權限
    roles = []
    onlineuser = request.session.get('account')
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    for i in roles:
        if i == 'admin' or i == 'PublicAreaAdmin':
            permission = 0

    if request.method == "POST":
        if request.POST:
            if request.POST.get('isGetData') == 'first':
                pass
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
        data = {
            # "selectItem":selectItem,
            # "powerOptions":powerOptions,
            # "content": mock_data,
            # "options":options,
            # "permission": permission
            "permission": permission
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CommonDevice/CommonDevice.html', locals())

