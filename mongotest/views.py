from django.shortcuts import render,redirect
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import exceptions
from .models import StudentModel,ToolList_Mongo
from .serializers import StudentSerializers
from .forms import ToolList
from rest_framework_mongoengine import generics

from . import models
from . import serializers

import json,simplejson,datetime

from django.shortcuts import render
from django.core.paginator import Paginator # 分页
from django.http import HttpResponseRedirect

# Create your views here.

#SQL
# class FirstMongoView(APIView):
#
#     def post(self, request):
#         print("2")
#         print(request)
#         print(request.method)
#         print(request._request.method)
#         print(request.data)
#         name = request.data["name"]
#         age = request.data["age"]
#         password = request.data["password"]
#         print(name,age,password)
#         StudentModel.objects.create(name=name, age=age, password=password)
#         return HttpResponse(dict(msg="OK", code=10000))
        # data = {
        #     "result": "pass"
        # }
        # return HttpResponse(data)
# class FirstMongoView1(ModelViewSet):#应该是mysql的，model
#     # print("1")
#     queryset = StudentModel.objects.all()#在views中没有定义queryset字段时在路由的注册必须加上basename
#     serializer_class = StudentSerializers

class FirstMongoView1(generics.ListCreateAPIView):#应该是mysql的，model
    # print("1")
    queryset = StudentModel.objects.all()#在views中没有定义queryset字段时在路由的注册必须加上basename
    serializer_class = StudentSerializers
#mongodb
class ListView(generics.ListCreateAPIView):
    queryset = models.data1.objects.all()
    serializer_class = serializers.data1Serializer

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from CQM.permissions import MyPermission
from CQM.authentication import MyJWTAuthentication
class ToolListmongo(generics.ListCreateAPIView):
    authentication_classes = [MyJWTAuthentication, SessionAuthentication, BasicAuthentication]
    # authentication_classes = [MyAuth]	# 局部认证(全局在setting里面设置),不写默认用全局（全局需要用DRF写用户的注册登陆接口，可以另外创建一个用于DRF的用户module）
    permission_classes = [MyPermission]  # 局部配置(全局在setting里面设置),不写默认用全局（全局需要用DRF写用户的注册登陆接口，可以另外创建一个用于DRF的用户module）
    # 所有用户都可以访问
    queryset = models.ToolList_Mongo.objects.all()
    serializer_class = serializers.ToolSerializer


def addInvitations(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/ToolList_upload"
    ToolList_upload = ToolList(request.POST)
    ToolList_M_lists = [{'Customer': 'Customer', 'Project': 'Project',
                         'Phase0': 'Phase', 'Vendor': 'Vendor', 'Version': 'Version',
                         'ToolName': 'ToolName', 'TestCase': 'TestCase'}]
    result = '00'
    ToolList_M_dic = {}
    result = 4
    if request.method == "POST":
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            n = 0

            for i in simplejson.loads(xlsxlist):
                n += 1
                if 'Customer' in i.keys():
                    Customer = i['Customer']
                else:
                    Customer = ''
                if 'Project' in i.keys():
                    Project = i['Project']
                else:
                    Project = ''
                if 'Phase' in i.keys():
                    Phase0 = i['Phase']
                else:
                    Phase0 = ''
                if 'Vendor' in i.keys():
                    Vendor = i['Vendor']
                else:
                    Vendor = ''
                if 'Version' in i.keys():
                    Version = i['Version']
                else:
                    Version = ''
                if 'ToolName' in i.keys():
                    ToolName = i['ToolName']
                else:
                    ToolName = ''
                if 'TestCase' in i.keys():
                    TestCase = i['TestCase']
                else:
                    TestCase = ''
                # print(len(Version))
                check_dic = {'Customer': Customer, 'Project': Project,
                             'Phase0': Phase0, 'Vendor': Vendor,
                             'Version': Version, 'ToolName': ToolName, 'TestCase': TestCase}
                check_list = ToolList_Mongo.objects.filter(**check_dic)
                if check_list:
                    err_ok = 1
                    ToolList_M_dic['Customer'] = Customer
                    ToolList_M_dic['Project'] = Project
                    ToolList_M_dic['Phase0'] = Phase0
                    ToolList_M_dic['Vendor'] = Vendor
                    ToolList_M_dic['Version'] = Version
                    ToolList_M_dic['ToolName'] = ToolName
                    ToolList_M_dic['TestCase'] = TestCase
                    ToolList_M_lists.append(ToolList_M_dic)
                    continue
                else:
                    ToolList_Mmodule = ToolList_Mongo()
                    ToolList_Mmodule.Customer = Customer
                    ToolList_Mmodule.Project = Project
                    ToolList_Mmodule.Phase0 = Phase0
                    ToolList_Mmodule.Vendor = Vendor
                    ToolList_Mmodule.Version = Version
                    ToolList_Mmodule.ToolName = ToolName
                    ToolList_Mmodule.TestCase = TestCase
                    ToolList_Mmodule.editor = request.session.get('user_name')
                    ToolList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ToolList_Mmodule.save()
            datajason = {
                'err_ok': err_ok,
                'content': ToolList_M_lists
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if 'Upload' in request.POST:
            if ToolList_upload.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                Customer = ToolList_upload.cleaned_data['Customer']
                Project = ToolList_upload.cleaned_data['Project']
                Phase0 = ToolList_upload.cleaned_data['Phase0']
                Vendor = ToolList_upload.cleaned_data['Vendor']
                Version = ToolList_upload.cleaned_data['Version']
                ToolName = ToolList_upload.cleaned_data['ToolName']
                TestCase = ToolList_upload.cleaned_data['TestCase']
                check_dic = {'Customer': Customer, 'Project': Project, 'Phase0': Phase0, 'Vendor': Vendor,
                             'Version': Version, 'ToolName': ToolName, 'TestCase': TestCase}
                print(check_dic)
                if ToolList_Mongo.objects.filter(**check_dic):
                    result = 1
                else:
                    ToolList_Mmodule = ToolList_Mongo()
                    ToolList_Mmodule.Customer = Customer
                    ToolList_Mmodule.Project = Project
                    ToolList_Mmodule.Phase0 = Phase0
                    ToolList_Mmodule.Vendor = Vendor
                    ToolList_Mmodule.Version = Version
                    ToolList_Mmodule.ToolName = ToolName
                    ToolList_Mmodule.TestCase = TestCase
                    ToolList_Mmodule.editor = request.session.get('user_name')
                    ToolList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ToolList_Mmodule.save()
                    message_CDM = "Upload Successfully"
                    result = 0
                return render(request, 'mongotest/mongotest_upload.html',
                              {'weizhi': weizhi, 'Skin': Skin, 'ToolList_upload': ToolList(),
                               'result': result})
            else:
                cleanData = ToolList_upload.errors
        return render(request, 'mongotest/mongotest_upload.html',
                      {'weizhi': weizhi, 'Skin': Skin, 'ToolList_upload': ToolList(), 'result': result})

    return render(request,'mongotest/mongotest_upload.html',locals())


