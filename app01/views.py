from django.shortcuts import render, redirect, HttpResponse
from app01.models import UserInfo, lesson_learn, Imgs, Files, ProjectinfoinDCT, Role, Permission, Menu
from django.views.decorators.csrf import csrf_exempt
from Bouncing.models import Bouncing_M
from Package.models import Package_M
from CDM.models import CDM
from TestPlanME.models import TestProjectME, TestItemME, TestPlanME
from LessonProjectME.models import lessonlearn_Project
from DriverTool.models import DriverList_M, ToolList_M
from MQM.models import MQM
from TestPlanSW.models import TestProjectSW, TestProjectSWAIO
from CQM.models import CQMProject, CQM, CQM_history
from QIL.models import QIL_M, QIL_Project
import datetime, os
from service.init_permission import init_permission
from django.db import transaction
from django.conf import settings
# Create your views here.
from django.forms import forms
from DjangoUeditor.forms import UEditorField
from app01.forms import lessonlearn
from django.conf import settings
import datetime, json, requests, time, simplejson
from requests_ntlm import HttpNtlmAuth
from INVGantt.models import INVGantt
from django.http import HttpResponseRedirect
# from app01.templatetags.custom_tag import *
from .tasks import ProjectSync, ImportProjectinfoFromDCT, MailOAtest


# class TestUEditorForm(forms.Form):
#     content = UEditorField('Solution/Action', width=800, height=500,
#                             toolbars="full", imagePath="upimg/", filePath="upfile/",
#                             upload_settings={"imageMaxSize": 1204000},
#                             settings={}, command=None#, blank=True
#                             )
# import logging
#
# logger = logging.getLogger('Django')
# logger.debug('Debug')
# logger.info('Info')
# logger.warning('Warning')
# logger.error('Error')
# logger.critical('Critical')


@csrf_exempt
def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        # print(request.GET.get('next'), '11', request.POST.get('next', '/'))
        # print(request.session, 'ses')
        # print(request.COOKIES, 'coo')
        # print(request.COOKIES['current_page'])
        # # print(request.COOKIES['Non_login_path'])
        try:
            # return redirect(request.COOKIES['current_page_DDIS'])
            return redirect('/Navigations/')
        except:
            # return redirect('/index/')
            return redirect('/Navigations/')

    # print(request.method)
    fbclid = request.GET.get('fbclid')
    # print(request.GET.get('next'), fbclid, '11', request.POST.get('next', '/'))

    if request.method == "POST":
        # login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        # if login_form.is_valid():
        Account = request.POST.get('inputEmail')
        Password = request.POST.get('inputPassword')
        user_obj = UserInfo.objects.filter(account=Account, password=Password).first()
        # print (Account)
        # print (Password)
        # print (user_obj)
        # print(request.user)
        # print(request.user.type)
        # t= UserInfo.objects.get(account=Account)
        user = UserInfo.objects.filter(account=Account).first()
        # print(type(user),type(user_obj))
        if user:
            # print (user.password)
            if user.password == Password:
                # 往session字典内写入用户状态和数据,你完全可以往里面写任何数据，不仅仅限于用户相关！
                # request.session.clear_expired()  # 将所有Session失效日期小于当前日期的数据删除，将过期的删除
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session['account'] = Account
                # request.session['Skin'] = "/static/src/blue.jpg"
                request.session.set_expiry(12 * 60 * 60)
                # print('11')
                Skin = request.COOKIES.get('Skin_raw')
                # print(Skin)
                if not Skin:
                    Skin = "/static/src/blue.jpg"
                # print(Skin)
                # print('21')
                init_permission(request, user_obj)  # 调用init_permission，初始化权限
                # print('21')
                # print(settings.MEDIA_ROOT,settings.MEDIA_URL)
                # return HttpResponseRedirect(request.session['login_from'])
                Non_login_path = request.session.get('Non_login_path')
                print(Non_login_path, 'Non_login_path')
                if Non_login_path:
                    # 记住来源的url，如果没有则设置为首页('/')
                    return redirect(Non_login_path)
                # print(request.POST.get('next', '/'),'postnext')
                # if request.GET.get('next'):
                #     # 记住来源的url，如果没有则设置为首页('/')
                #     print(request.GET.get('next'), request.META.get('HTTP_REFERER'), 'tttt')
                #     return redirect(request.GET.get('next'))
                else:
                    # return redirect('/index/')
                    return redirect(request.META.get('HTTP_REFERER'))
            else:
                message = "密码不正确！"
        else:
            message = "用户不存在！"
        return render(request, 'login.html', locals())

    return render(request, 'login.html', locals())


@csrf_exempt
def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Home/Dashboard"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    # print (permission_url)
    # L_R_data_object=lesson_learn.objects.all().order_by('edit_time')
    # # print(type(L_R_data_object.first().edit_time))
    # # print(L_R_data_object.last().edit_time)
    # time_first=L_R_data_object.first().edit_time
    # L_R_data_first=datetime.datetime.strptime(str(time_first)[0:10],'%Y-%m-%d')
    # time_last = L_R_data_object.last().edit_time
    # L_R_data_last = datetime.datetime.strptime(str(time_last)[0:10], '%Y-%m-%d')
    # # print(type(L_R_data_first))
    # L_R_data = (L_R_data_last-L_R_data_first).days/365
    # L_R_data=format(L_R_data,'.2f')

    # print(UserInfo.objects.filter(account="C1010S3").first().role.all())
    # for i in UserInfo.objects.filter(account="C1010S3").first().role.all():
    #     print(i.perms.all())
    #     for j in i.perms.all():
    #         print(j)
    # for f in UserInfo._meta.fields:
    #     print(f.name)
    # for f in UserInfo._meta.fields_map:
    #     print(f)
    # for f in UserInfo._meta.get_fields(include_parents=False):
    #     print(f,f.name)
    # for item in UserInfo.objects.filter(account="C1010S3").first().role.values('perms__url','perms__menu__id','perms__menu__title'):
    #     print(item)

    L_R_data = lesson_learn.objects.filter(Category="Reliability").values('Symptom').count()
    L_C_data = lesson_learn.objects.filter(Category="Compatibility").values('Symptom').count()
    L_Q_data = QIL_M.objects.all().values('QIL_No').count()
    R_P_data = Package_M.objects.all().values('Project').distinct().count()
    R_B_data = Bouncing_M.objects.all().values('Project').distinct().count()
    R_C_data = CDM.objects.all().values('Project').distinct().count()
    T_M_Project = TestProjectME.objects.all().values('Project').distinct().count()
    X_D_DriverList = DriverList_M.objects.all().values('Project').distinct().count()
    X_D_ToolList = ToolList_M.objects.all().values('Project').distinct().count()
    X_M_Project = MQM.objects.all().values('Project').distinct().count()
    T_S_Project = TestProjectSW.objects.all().values(
        'Project').distinct().count() + TestProjectSWAIO.objects.all().values('Project').distinct().count()
    X_C_data = CQMProject.objects.all().values('Project').distinct().count()
    ProI_data = ProjectinfoinDCT.objects.all().values('ComPrjCode').distinct().count()
    # for i in TestProjectME.objects.all().values('Customer', 'Project', 'Phase').distinct():
    #     print(i)
    T_M_Items = TestItemME.objects.all().count()
    T_I_Project = INVGantt.objects.all().values("Project_Name").distinct().count()
    # importPrjResult = ImportProjectinfoFromDCT()
    # print(request.POST)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Reliability":
            # cookie
            # Redirect = redirect('/Lesson_search/')
            # Reliabilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Reliabilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Compatibility":
            # cookie
            # Redirect = redirect('/Lesson_search/')
            # Compatibilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Compatibilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    return render(request, 'index.html', locals())

headermodel_Projectinfo = {
    'Customer': 'Customer', 'Project Code': 'ComPrjCode', 'MKT Name': 'ProjectName', 'Size': 'Size',
    'CPU': 'CPU', 'Platform': 'Platform',
    'VGA': 'VGA',
    'OS': 'OSSupport',
    'SS/MP Date': 'SS', 'DQAPLNum': 'DQAPLNum', 'DQA PL': 'DQAPL', 'DQAQMNum': 'DQAQMNum', 'DQA QM': 'DQAQM',
    'PrjEngCode1': 'PrjEngCode1', 'PrjEngCode2': 'PrjEngCode2', 'Type': 'Type', 'PPA': 'PPA', 'PQE': 'PQE',
    'LD': 'LD', 'LDNum': 'LDNum', 'Year': 'Year',
}
@csrf_exempt
def ProjectInfoSearch(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Home/ProjectInfoSearch"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "Comprjcode": "KLS71", "Mkt_Code": "FLAT4", "Size": "14",
        #  "CPU": "AMD", "Platform": "Intel Lunar Lake-MX",
        #  "VGA": "UMA", "OS_Support": "WIN11 24H2", "SS": "2023-05-22", "DQA_PLNum": "C123456", "DQA_PL": "錢嬌",
        #  "DQA_QMNum": "C123456",
        #  "DQA_QM": "錢嬌", "Prjengcode1": "", "Prjengcode2": "", "Type": "", "PPA": "", "PQE": "", "LD": "", "LD_Num": "",
        #  "Year": "",
        #  "Modified_Date": "2023-05-22"},
        # {"id": "1", "Customer": "C38(NB)", "Year": "Y2020", "Comprjcode": "FLAT4", "Prjengcode1": "TATA4",
        #  "Prjengcode2": "", "Mkt_Code": "E41-55",
        #  "Size": "14", "CPU": "AMD", "Platform": "AMD", "VGA": "UMA", "OS_Support": "WIN10 20H1", "SS": "2020-09-28",
        #  "LD": "陈威", "DQA_PL": "周课",
        #  "Modified_Date": "2020-09-11 21:19:01"},
    ]
    errMsg = ''
    selectItem = [
        # 'C38(NB)', 'C38(AIO)', 'T88(AIO)'
    ]

    selectYear = {
        # "Y2020": [{"ProjectCode": "FLAT4"}, {"ProjectCode": "FLMD0"}, {"ProjectCode": "FLV34"},
        #           {"ProjectCode": "FLV3B"}],
        # "Y2019": [{"ProjectCode": "FL435"}, {"ProjectCode": "EL534"}, {"ProjectCode": "FLMS0"},
        #           {"ProjectCode": "FLPR5"}],
        # "Y2018": [{"ProjectCode": "DLADE"}, {"ProjectCode": "EL431"}, {"ProjectCode": "EL4C1"},
        #           {"ProjectCode": "EL5C3"}]
    }
    for i in ProjectinfoinDCT.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    for i in ProjectinfoinDCT.objects.all().values("Year").distinct().order_by("Year"):
        YearPro = []
        for j in ProjectinfoinDCT.objects.filter(Year=i["Year"]).values("ComPrjCode").distinct().order_by("ComPrjCode"):
            YearPro.append({"ProjectCode": j["ComPrjCode"]})
        selectYear[i["Year"]] = YearPro
    # print(ProjectinfoinDCT.objects.all().values("ComPrjCode").distinct().count(),
    #       ProjectinfoinDCT.objects.all().values("ComPrjCode").count(),
    #       ProjectinfoinDCT.objects.all().values("ComPrjCode", "Year").distinct().count())
    DQAnum_no_account = []
    permission = 1
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if 'admin' in i:
            # editPpriority = 4
            canExport = 1
        # elif 'DQA' in i:
        #     canExport = 1
    if request.method == "GET":
        # print(request.GET)
        if request.GET.get("action") == "first":
            importPrjResult = ProjectSync()

            # print(data)
            for i in ProjectinfoinDCT.objects.all():
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode,
                     "Prjengcode1": i.PrjEngCode1,
                     "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                     "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA, "OS_Support": i.OSSupport,
                     "Type": i.Type,
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LD_Num": i.LDNum, "DQA_PLNum": i.DQAPLNum, "DQA_PL": i.DQAPL,
                     "DQA_QMNum": i.DQAQMNum, "DQA_QM": i.DQAQM,
                     "Modified_Date": i.ModifiedDate}
                )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                'addselect': selectYear,
            }
            if importPrjResult:
                data['result'] = 1
            else:
                data['result'] = 0
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == "POST":
        # print(request.GET)
        if request.POST.get("isGetData") == "first":
            for i in ProjectinfoinDCT.objects.all():
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode,
                     "Prjengcode1": i.PrjEngCode1,
                     "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                     "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA, "OS_Support": i.OSSupport,
                     "Type": i.Type,
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LD_Num": i.LDNum, "DQA_PLNum": i.DQAPLNum,
                     "DQA_PL": i.DQAPL,
                     "DQA_QMNum": i.DQAQMNum, "DQA_QM": i.DQAQM,
                     "Modified_Date": i.ModifiedDate}
                )
            pass
        if request.POST.get("isGetData") == "SEARCH":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Year")
            ProjectCode = request.POST.get("ProjectCode")
            checkdic_PRODCT = {}
            if Customer != "All" and Customer != "":
                checkdic_PRODCT["Customer"] = Customer
            if Year != "All" and Year != "":
                checkdic_PRODCT["Year"] = Year
            if ProjectCode != "All" and ProjectCode != "":
                checkdic_PRODCT["ComPrjCode"] = ProjectCode

            checkdic_PRODCTSSYear = {}
            if Customer != "All" and Customer != "":
                checkdic_PRODCTSSYear["Customer"] = Customer
            if Year != "All" and Year != "":
                checkdic_PRODCTSSYear["SS__contains"] = Year #这里的日期数据用的是字符型不是日期行，如果是日期型要用SS__year
            if ProjectCode != "All" and ProjectCode != "":
                checkdic_PRODCTSSYear["ComPrjCode"] = ProjectCode
            ProjectObject = ProjectinfoinDCT.objects.filter(**checkdic_PRODCT) | ProjectinfoinDCT.objects.filter(**checkdic_PRODCTSSYear)
            for i in ProjectObject:
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode,
                     "Prjengcode1": i.PrjEngCode1,
                     "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                     "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA, "OS_Support": i.OSSupport,
                     "Type": i.Type,
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LD_Num": i.LDNum, "DQA_PLNum": i.DQAPLNum,
                     "DQA_PL": i.DQAPL,
                     "DQA_QMNum": i.DQAQMNum, "DQA_QM": i.DQAQM,
                     "Modified_Date": i.ModifiedDate}
                )
            # datamail = {"ids": [100002, 100003], "Projects": ['ForTest1', 'ForTest2', ]}
            # MailOAtest.delay(**datamail) # 启动异步任务
            pass
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'upload' in str(request.body):
                    responseData = json.loads(request.body)

                    xlsxlist = json.loads(responseData['ExcelData'])
                    # print(xlsxlist)
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
                        uploadxlsxlist = []
                        for i in xlsxlist:
                            # print(type(i),i)
                            rownum += 1
                            modeldata = {}
                            for key, value in i.items():
                                if key in headermodel_Projectinfo.keys():
                                    # print(headermodel_Projectinfo[key],value)
                                    modeldata[headermodel_Projectinfo[key]] = value
                                modeldata['ModifiedDate'] = datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                                # modeldata['ModifiedDate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            # print(modeldata)

                            if 'Customer' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Customer不能爲空
                                                            """ % rownum
                                break
                            if 'ComPrjCode' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Project Code不能爲空
                                                            """ % rownum
                                break
                            if 'ProjectName' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，MKT Name不能爲空
                                                            """ % rownum
                                break
                            if 'Size' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Size不能爲空
                                                            """ % rownum
                                break
                            if 'CPU' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，CPU不能爲空
                                                            """ % rownum
                                break
                            if 'Platform' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Platform不能爲空
                                                            """ % rownum
                                break
                            if 'VGA' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，VGA不能爲空
                                                            """ % rownum
                                break
                            if 'OSSupport' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，OS不能爲空
                                                            """ % rownum
                                break
                            if 'SS' in modeldata.keys():
                                if len(modeldata['SS'].split('-')) != 3 and len(modeldata['SS']) != 10 and len(modeldata['SS'].split('-')[0]) != 4:
                                    startupload = 0
                                    errMsg = """
                                            第"%s"條數據，SS/MP Date格式不对，请使用YYYY-MM-DD格式
                                                                                                """ % rownum
                                else:
                                    modeldata['SS'] = modeldata['SS'].split('-')[1] + "/" + modeldata['SS'].split('-')[2] + "/" + modeldata['SS'].split('-')[0] + " 12:00:00 AM"
                                    startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，SS/MP Date不能爲空
                                                            """ % rownum
                                break
                            if 'DQAPLNum' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，DQAPLNum不能爲空
                                                            """ % rownum
                                break
                            if 'DQAPL' in modeldata.keys():
                                startupload = 1
                                if not UserInfo.objects.filter(account=modeldata['DQAPLNum']):
                                    DQAnum_no_account.append([modeldata['DQAPLNum'], modeldata['DQAPL']])
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，DQA PL不能爲空
                                                            """ % rownum
                                break
                            if 'DQAQMNum' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，DQAQMNum不能爲空
                                                            """ % rownum
                                break
                            if 'DQAQM' in modeldata.keys():
                                startupload = 1
                                if not UserInfo.objects.filter(account=modeldata['DQAQMNum']):
                                    DQAnum_no_account.append([modeldata['DQAQMNum'], modeldata['DQAQM']])
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，DQAQM不能爲空
                                                            """ % rownum
                                break

                            uploadxlsxlist.append(modeldata)
                            # print(create_list)
                        # print(errMsg, startupload)
                        # print(create_list,)
                        # print(startupload)
                        # print(rownum, type(rownum))
                        if startupload:
                            # 让数据可以从有值更新为无值
                            create_list = []
                            update_list = []
                            DevieModelfiedlist = []
                            for i in ProjectinfoinDCT._meta.fields:
                                if i.name != 'id':
                                    DevieModelfiedlist.append([i.name, i.get_internal_type()])
                            for i in uploadxlsxlist:
                                for j in DevieModelfiedlist:
                                    if j[0] not in i.keys():
                                        # print(j)
                                        if j[1] == "DateField":
                                            i[j[0]] = None
                                        else:
                                            i[j[0]] = ''
                                if ProjectinfoinDCT.objects.filter(Customer=i['Customer'],
                                                                   ComPrjCode=i['ComPrjCode']):
                                    update_list.append(i)
                                else:
                                    create_list.append(ProjectinfoinDCT(**i))  # object(**dict)
                            try:
                                with transaction.atomic():
                                    if create_list:
                                        ProjectinfoinDCT.objects.bulk_create(create_list)
                                    if update_list:
                                        for i in update_list:
                                            ProjectinfoinDCT.objects.filter(Customer=i['Customer'], ComPrjCode=i['ComPrjCode']).update(**i)
                                    if DQAnum_no_account:
                                        errMsg = """%s 以上用户没有DDIS账户，请联系管理员注册，否则可能会影响邮件通知""" % str(DQAnum_no_account)
                            except Exception as e:
                                # alert = '此数据正被其他使用者编辑中...'
                                alert = str(e)
                                print(alert)

                    # print('IssuesBreakdown')
                    # mock_data
                    for i in ProjectinfoinDCT.objects.all():
                        mock_data.append(
                            {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode,
                             "Prjengcode1": i.PrjEngCode1,
                             "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                             "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA,
                             "OS_Support": i.OSSupport,
                             "Type": i.Type,
                             "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LD_Num": i.LDNum,
                             "DQA_PLNum": i.DQAPLNum,
                             "DQA_PL": i.DQAPL,
                             "DQA_QMNum": i.DQAQMNum, "DQA_QM": i.DQAQM,
                             "Modified_Date": i.ModifiedDate}
                        )
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            'addselect': selectYear,
            'canExport': canExport,
            'errMsg': errMsg,
            'permission': permission,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ProjectInfo_search.html', locals())


from django.core.mail import EmailMultiAlternatives
from TestPlanSW.models import TestProjectSW, TestPlanSW






@csrf_exempt
def FilesDownload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Home/ProjectInfo"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    if request.method == "GET":
        # print(request.GET)
        if request.GET.get("action") == "first":
            # # Mailhtml()
            # # MailOAtest()
            # # print('mailend')
            importPrjResult = ImportProjectinfoFromDCT()
            if importPrjResult:
                data['result'] = 1
            else:
                data['result'] = 0
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'FilesDownload.html', locals())


def Navigation(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Home/ProjectInfo"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    if request.method == "GET":
        # print(request.GET)
        if request.GET.get("action") == "first":
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigation.html', locals())

@csrf_exempt
def Navigations(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Category"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    tableData = [
    ]
    data = {
        "tableData": tableData,
    }
    if request.method == "POST":
        # print(request.GET)
        if request.POST.get("isGetData") == "first":
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations.html', locals())

@csrf_exempt
def Navigations_Category(request, Category):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Systems"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    Category = Category
    print(Category)
    if request.method == "GET":
        # print(request.GET)
        if request.GET.get("action") == "first":
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsCategory.html', locals())

@csrf_exempt
def Navigations_Category_axios(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Systems"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    All_system_dic = {
        #部門管理
        "DepartMent": [
        {
        'name': '人員信息',
        'Key': 'PersonalInfo',
        'address': "",
        'Comment': "",
        'name2': '人員履歷',
        'Key2': 'PersonalExperience',
        'address2': "",
        'Comment2': "",
        'name3': '區域管理',
        'Key3': 'PublicArea',
        'address3': "",
        'Comment3': "",
        'name4': '',
        'Key4': '',
        'address4': "",
        'Comment4': "",
    }, {
        'name': '',
        'address': "",
        'Comment': "",
        'name2': '',
        'address2': "",
        'Comment2': "",
        'name3': '',
        'address3': "",
        'Comment3': "",
        'name4': '',
        'address4': "",
        'Comment4': "",},
            {
        'name': '',
        'address': "",
        'Comment': "",
        'name2': '',
        'address2': "",
        'Comment2': "",
        'name3': '',
        'address3': "",
        'Comment3': "",
        'name4': '',
        'address4': "",
        'Comment4': "",}
                        ],
        # 資產管理
        "Property": [
            {

                'name': "關鍵組件",
                'Key': "Materia",
                'address': "",
                'Comment': "",
                'name2': "電源適配器",
                'Key2': "Adapter",
                'address2': "",
                'Comment2': "",
                'name3': "工作機",
                'Key3': "Computer",
                'address3': "",
                'Comment3': "",
                'name4': "辦公櫃椅",
                'Key4': "ChairCabine",
                'address4': "",
                'Comment4': "",
            }, {
                'name': "测试設備",
                'Key': "Device",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }
        ],
        # 預算管理
        "Budget": [
            {

                'name': "資本支出",
                'Key': "CapitalExpenditure",
                'address': "",
                'Comment': "",
                'name2': "專案預算",
                'Key2': "ProjectComparison",
                'address2': "",
                'Comment2': "",
                'name3': "測試機臺",
                'Key3': "TestUnits",
                'address3': "",
                'Comment3': "",
                'name4': "申購記錄",
                'Key4': "MiscellaneousPurchases",
                'address4': "",
                'Comment4': "",
            },
            {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            },
            {
                'name': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }],
        # 管理辦法
        "SOPManager": [
            {
                'name': '測試規格下載',
                'Key': 'SpecDownload',
                'address': "",
                'Comment': "",
                'name2': '實驗室管理規範',
                'Key2': 'ManagementSop',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': '',
                'Key': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "", },
            {
                'name': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],

        #專案管理
        "Project": [
            {
                'name': '專案信息',
                'Key': 'ProjectInfo',
                'address': "",
                'Comment': "",
                'name2': '機構測試',
                'Key2': 'TestPlanME',
                'address2': "",
                'Comment2': "",
                'name3': '軟體測試',
                'Key3': 'TestPlanSW',
                'address3': "",
                'Comment3': "",
                'name4': 'OSR測試',
                'Key4': 'TestPlanSW-OSR',
                'address4': "",
                'Comment4': "",
            }, {
                'name': 'INV測試',
                'Key': 'TestPlanINV',
                'address': "",
                'Comment': "",
                'name2': 'CQM',
                'Key2': 'CQM',
                'address2': "",
                'Comment2': "",
                'name3': 'MQM',
                'Key3': 'MQM',
                'address3': "",
                'Comment3': "",
                'name4': 'Driver',
                'Key4': 'Driver',
                'address4': "",
                'Comment4': "",
            },
            {
                'name': 'Tool',
                'Key': 'Tool',
                'address': "",
                'Comment': "",
                'name2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],
        # 測試規範
        "TestSpec": [
            {
                'name': '測試規格下載',
                'Key': 'SpecDownload',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': '',
                'Key': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "", },
            {
                'name': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],
        # 智能測試
        "Automation": [
            {
                'name': "智能测试",
                'Key': "Automation",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            },
            {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            },

        ],
        # 測試數據
        "TestData": [
            {
                'name': 'OBI測試結果',
                'Key': 'OBIResult',
                'address': "",
                'Comment': "",
                'name2': 'PackageGValue',
                'Key2': 'PackageGValue',
                'address2': "",
                'Comment2': "",
                'name3': 'CDM',
                'Key3': 'CDM',
                'address3': "",
                'Comment3': "",
                'name4': 'Bouncing',
                'Key4': 'Bouncing',
                'address4': "",
                'Comment4': "",
            }, {
                'name': '',
                'Key': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "", },
            {
                'name': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],

        #品質管理
        "Quality": [
            {
                'name': "QIL",
                'Key': "QIL",
                'address': "",
                'Comment': "",
                'name2': 'LessonLearn',
                'Key2': 'LessonLearn',
                'address2': "",
                'Comment2': "",
                'name3': 'LowLight',
                'Key3': 'LowLight',
                'address3': "",
                'Comment3': "",
                'name4': 'IssueBreakdown',
                'Key4': 'IssueBreakdown',
                'address4': "",
                'Comment4': "",
            }, {
                'name': 'NonDQA-Lesson',
                'Key': 'NonDQA-Lesson',
                'address': "",
                'Comment': "",
                'name2': '',#'"CriticalIssue",
                'Key2': '',#'"CriticalIssue",
                'address2': "",
                'Comment2': "",
                'name3': "",  # Issue Notes
                'Key3': "",  # IssueNotes
                'address3': "",
                'Comment3': "",
                'name4': '',  # Known Issue
                'Key4': '',  # KnownIssue
                'address4': "",
                'Comment4': "",
            }, {
                'name': '',
                'address': "",
                'Comment': "",
                'name2': "",
                'address2': "",
                'Comment2': "",
                'name3': "",
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],
        #公共事務
        "Common": [
            {
                'name': '',
                'Key': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': '',
                'Key': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'Key2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "", },
            {
                'name': '',
                'address': "",
                'Comment': "",
                'name2': '',
                'address2': "",
                'Comment2': "",
                'name3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'address4': "",
                'Comment4': "", }
        ],
        #討論交流
        "Discussing": [
            {
                'name': "讨论版",
                'Key': "Discussing",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }
        ],
        #其他
        "Others": [
            {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }, {
                'name': "",
                'Key': "",
                'address': "",
                'Comment': "",
                'name2': "",
                'Key2': "",
                'address2': "",
                'Comment2': "",
                'name3': '',
                'Key3': '',
                'address3': "",
                'Comment3': "",
                'name4': '',
                'Key4': '',
                'address4': "",
                'Comment4': "",
            }
        ],

    }
    gridData_Category = []
    Navigations_Category_name = ''
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("Categoryname"))
            if request.POST.get("Categoryname"):

                gridData_Category = All_system_dic[request.POST.get("Categoryname")]
                data = {
                    "gridData_Category": gridData_Category,
                }
                response = HttpResponse(json.dumps(data), content_type="application/json")
                response.set_cookie('Navigations_Category_name', json.dumps(request.POST.get("Categoryname")), max_age=3600 * 24 * 7)

                return response
            else:
                Navigations_Category_name = json.loads(request.COOKIES.get('Navigations_Category_name'))
                # print(Navigations_Category_name,'category_axios')
                gridData_Category = All_system_dic[Navigations_Category_name]
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
        data = {
            "gridData_Category": gridData_Category,
            "Navigations_Category_name": Navigations_Category_name,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsCategory.html', locals())


from django.utils.html import escape
@csrf_exempt
def Navigations_system(request, name):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Customer"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    name = name
    Customer_System_list = []
    # Customer_System_list = All_system_dic[name]
    # print(request.method, name)
    # print(request.GET)
    # print(request.POST)
    if request.method == "GET":
        # print(request.GET)

        if request.GET.get("action") == "first":
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsSystem.html', locals())

@csrf_exempt
def Navigations_system_axios(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Customer"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    DDMS_add = 'http://10.129.83.21:8004'
    Discussing_add = 'http://10.129.83.21:8003'
    RTMS_add = 'http://10.129.83.21:8001'
    DCT_add = 'http://10.128.82.23'
    EQUIP_add = 'http://kspqiswww'
    All_system_dic = {
        # 部门管理
        "PersonalInfo": [
            {"Comment": "",
             "name1": "C38", "url1": "/PersonalInfo/PersonalInfo-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "/PersonalInfo/PersonalInfo-search/", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "/PersonalInfo/PersonalInfo-search/", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/PersonalInfo/PersonalInfo-search/", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "PersonalExperience": [
            {"Comment": "",
             "name1": "C38", "url1": "/PersonalExperience/Summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "PublicArea": [
            {"Comment": "",
             "name1": "C38", "url1": "/PersonalInfo/PublicArea/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # 專案管理
        "ProjectInfo": [
            {"Comment": "",
             "name1": "C38", "url1": "/ProjectInfoSearch/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "/ProjectInfoSearch/", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "/ProjectInfoSearch/", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "TestPlanME": [
            {"Comment": "",
             "name1": "C38", "url1": "/TestPlanME/TestPlanME-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "TestPlanSW": [
            {"Comment": "",
             "name1": "C38", "url1": "/TestPlanSW/TestPlanSW-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/ABOTestPlan/ABOTestPlan_summary/", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "TestPlanSW-OSR": [
            {"Comment": "",
             "name1": "C38", "url1": "/TestPlanSWOS/TestPlanSWOS-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "TestPlanINV": [
            {"Comment": "",
             "name1": "C38", "url1": "/INVGantt/INVGantt-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "CQM": [
            {"Comment": "",
             "name1": "C38", "url1": "/CQM/CQM_search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "MQM": [
            {"Comment": "",
             "name1": "C38", "url1": "/MQM/MQM_search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "Driver": [
            {"Comment": "",
             "name1": "C38", "url1": "/DriverTool/DriverList_search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/ABODriverTool/ABODriverList_search/", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "Tool": [
            {"Comment": "",
             "name1": "C38", "url1": "/DriverTool/ToolList_search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/ABODriverTool/ABOToolList_search/", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # 資產管理
        "Materia": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/TUMHistory/SummaryMateria/", "Comment1": "", "CustomerFlag1": 0,
             # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "Adapter": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/AdapterPowerCode/BorrowedAdapter/", "Comment1": "",
             "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "Computer": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/ComputerMS/BorrowedComputer/", "Comment1": "", "CustomerFlag1": 0,
             # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "ChairCabine": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/ChairCabinetMS/BorrowedChairCabinet/", "Comment1": "",
             "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        # "DevicePerson": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": DDMS_add + "/Summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
        #      "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": 'ABO', "url4": DDMS_add + "/Summary_ABO/", "Comment4": "", "CustomerFlag4": 0,  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
        #      "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
        #      "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
        #      "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
        #      },
        #     {"Comment": "",
        #      "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
        #      "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
        #      },
        # ],
        "Device": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/DeviceLNV/BorrowedDeviceLNV/", "Comment1": "", "CustomerFlag1": 0,
             # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": DDMS_add + "/DeviceABO/BorrowedDeviceABO/", "Comment4": "", "CustomerFlag4": 0,
             # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "A39", "url4": DDMS_add + "/DeviceA39/BorrowedDeviceA39/", "Comment4": "", "CustomerFlag4": 0,
             # A39

             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],


        # 品质管控
        "QIL": [
            {"Comment": "",
             "name1": "C38", "url1": "/QIL/QIL_searchbyproject/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/ABOQIL/ABOQIL_searchbyproject/", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "LessonLearn": [
            {"Comment": "",
             "name1": "C38", "url1": "/LessonProjectME/Lesson_SearchByProject/", "Comment1": "",  # C38
             "name2": "A31", "url2": "/A31LessonLProject/Lesson_SearchByProject/", "Comment2": "",  # A31
             "name3": "", "url3": "/LessonLProject/Lesson_SearchByProject/", "Comment3": "",  #
             "name4": 'ABO', "url4": "/ABOProjectLessonL/Lesson_SearchByProject/", "Comment4": "",  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "LowLight": [
            {"Comment": "",
             "name1": "C38", "url1": "/LowLightList/LowLightList_edit/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "IssueBreakdown": [
            {"Comment": "",
             "name1": "C38", "url1": "/IssuesBreakdown/IssuesBreakdown_Summary/", "Comment1": "", "CustomerFlag1": 0,
             # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        # "IssueNotes": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": "/Issue_Notes/Issue_Notes-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
        #      "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
        #      "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
        #      "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
        #      "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
        #      },
        #     {"Comment": "",
        #      "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
        #      "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
        #      },
        # ],
        # "KnownIssue": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": "/KnowIssue/KnowIssue-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
        #      "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
        #      "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
        #      "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
        #      "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
        #      },
        #     {"Comment": "",
        #      "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
        #      "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
        #      "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
        #      "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
        #      },
        # ],
        "NonDQA-Lesson": [
            {"Comment": "",
             "name1": "C38", "url1": "/NonDQALesson/NonDQALesson-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "CriticalIssue": [
            {"Comment": "",
             "name1": "C38", "url1": "/CriticalIssueCrossCheck/CriticalIssue_SearchByIssue/", "Comment1": "",
             "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "/CriticalIssueCrossCheck/CriticalIssue_SearchByIssue/", "Comment2": "",
             "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "/CriticalIssueCrossCheck/CriticalIssue_SearchByIssue/", "Comment3": "",
             "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "/CriticalIssueCrossCheck/CriticalIssue_SearchByIssue/", "Comment4": "",
             "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # 預算管理
        "CapitalExpenditure": [
            {"Comment": "",
             "name1": "C38", "url1": "/CapitalExpenditure/CapitalExpenditure_Summary/", "Comment1": "",
             "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFla3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "ProjectComparison": [
            {"Comment": "",
             "name1": "C38", "url1": "/ProjectComparison/ProjectComparison_Summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "TestUnits": [
            {"Comment": "",
             "name1": "C38", "url1": DDMS_add + "/TUMHistory/SummaryTUM/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "MiscellaneousPurchases": [
            {"Comment": "",
             "name1": "C38", "url1": "/MiscellaneousPurchases/SubscriptionStatus/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # 測試數據
        "SpecDownload": [
            {"Comment": "",
             "name1": "C38", "url1": "/SpecDownload/SpecDownload-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "ManagementSop": [
            {"Comment": "",
             "name1": "管理規範", "url1": "/SpecDownload/ManagementSop-summary/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": '', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "OBIResult": [
            {"Comment": "",
             "name1": "C38", "url1": "/OBIDeviceResult/OBIDeviceResult_search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "PackageGValue": [
            {"Comment": "",
             "name1": "C38", "url1": "/Package/Package-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "CDM": [
            {"Comment": "",
             "name1": "C38", "url1": "/CDM/CDM-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        "Bouncing": [
            {"Comment": "",
             "name1": "C38", "url1": "/Bouncing/Bouncing-search/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # 智能测试
        "Automation": [
            {"Comment": "",
             "name1": "C38", "url1": "/AutoResult/AutoResult_search/", "Comment1": "",  "CustomerFlag1": 0, # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,# A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,#
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,# ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],
        # 讨论交流
        "Discussing": [
            {"Comment": "",
             "name1": "C38", "url1": Discussing_add + "/index/", "Comment1": "", "CustomerFlag1": 0,  # C38
             "name2": "A31", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # A31
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": 'ABO', "url4": "", "Comment4": "", "CustomerFlag4": 0,  # ABO
             },
            {"Comment": "",
             "name1": "T88", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # T88
             "name2": "T89", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # T89
             "name3": 'T99', "url3": "", "Comment3": "", "CustomerFlag3": 0,  # T99
             "name4": "", "url4": "", "Comment4": "", "CustomerFlag4": 0,  # A39
             },
            {"Comment": "",
             "name1": "", "url1": "", "Comment1": "", "CustomerFlag1": 0,  # CQT88
             "name2": "", "url2": "", "Comment2": "", "CustomerFlag2": 0,  # AIO
             "name3": "", "url3": "", "Comment3": "", "CustomerFlag3": 0,  #
             "name4": '', "url4": "", "Comment4": "", "CustomerFlag4": 0,  #
             },
        ],

        # # 其他
        # "RTMS": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": RTMS_add + "/index/", "Comment1": "",  # C38
        #      "name2": "A31", "url2": "", "Comment2": "",  # A31
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": 'ABO', "url4": "", "Comment4": "",  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "CQT88", "url1": "", "Comment1": "",  # CQT88
        #      "name2": "T88", "url2": "", "Comment2": "",  # T88
        #      "name3": "T89", "url3": "", "Comment3": "",  # T89
        #      "name4": 'T99', "url4": "", "Comment4": "",  # T99
        #      },
        #     {"Comment": "",
        #      "name1": "AIO", "url1": "", "Comment1": "",  # AIO
        #      "name2": "", "url2": "", "Comment2": "",  # A39
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": '', "url4": "", "Comment4": "",  #
        #      },
        # ],
        # "DCT": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": DCT_add + "/DCT/RealTime/Index", "Comment1": "",  # C38
        #      "name2": "A31", "url2": "", "Comment2": "",  # A31
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": 'ABO', "url4": "", "Comment4": "",  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "CQT88", "url1": "", "Comment1": "",  # CQT88
        #      "name2": "T88", "url2": "", "Comment2": "",  # T88
        #      "name3": "T89", "url3": "", "Comment3": "",  # T89
        #      "name4": 'T99', "url4": "", "Comment4": "",  # T99
        #      },
        #     {"Comment": "",
        #      "name1": "AIO", "url1": "", "Comment1": "",  # AIO
        #      "name2": "", "url2": "", "Comment2": "",  # A39
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": '', "url4": "", "Comment4": "",  #
        #      },
        # ],
        # "EQUIP": [
        #     {"Comment": "",
        #      "name1": "C38", "url1": EQUIP_add + "/DQA_ELR/index.html", "Comment1": "",  # C38
        #      "name2": "A31", "url2": "", "Comment2": "",  # A31
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": 'ABO', "url4": "", "Comment4": "",  # ABO
        #      },
        #     {"Comment": "",
        #      "name1": "CQT88", "url1": "", "Comment1": "",  # CQT88
        #      "name2": "T88", "url2": "", "Comment2": "",  # T88
        #      "name3": "T89", "url3": "", "Comment3": "",  # T89
        #      "name4": 'T99', "url4": "", "Comment4": "",  # T99
        #      },
        #     {"Comment": "",
        #      "name1": "AIO", "url1": "", "Comment1": "",  # AIO
        #      "name2": "", "url2": "", "Comment2": "",  # A39
        #      "name3": "", "url3": "", "Comment3": "",  #
        #      "name4": '', "url4": "", "Comment4": "",  #
        #      },
        # ],

    }
    data = {}
    gridData = []
    Navigations_system_name =''
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    if request.method == "POST":
        # print(request.GET)
        if request.POST.get("isGetData") == "first":
            pass
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'first' in str(request.body):
                    responseData = json.loads(request.body)
                    Sysname = responseData["Sysname"]
                    print(Sysname)
                    if Sysname:
                        gridData = All_system_dic[Sysname]
                        data = {
                            "gridData": gridData,
                        }
                        response = HttpResponse(json.dumps(data), content_type="application/json")
                        # 设置中文字符的cookie需要序列化和反序列化过程
                        response.set_cookie('Navigations_system_name', json.dumps(Sysname), max_age=3600 * 24 * 7)

                        return response
                    else:
                        # 设置中文字符的cookie需要序列化和反序列化过程
                        Navigations_system_name = json.loads(request.COOKIES.get('Navigations_system_name'))
                        print(Navigations_system_name)
                        gridData = All_system_dic[Navigations_system_name]
        data = {
            "gridData": gridData,
            "Navigations_system_name": Navigations_system_name
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsSystem.html', locals())

@csrf_exempt
def Navigations_customer(request, customer):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Customer"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    customer = customer
    Customer_System_list = []
    # Customer_System_list = All_system_dic[name]
    # print(request.method, name)
    # print(request.GET)
    # print(request.POST)
    if request.method == "GET":
        # print(request.GET)

        if request.GET.get("action") == "first":
            # importPrjResult = ImportProjectinfoFromDCT()
            # if importPrjResult:
            #     data['result'] = 1
            # else:
            #     data['result'] = 0
            # # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsCustomer.html', locals())

@csrf_exempt
def Navigations_customer_axios(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Customer"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    DDMS_add = 'http://10.129.83.21:8004'
    Discussing_add = 'http://10.129.83.21:8003'
    RTMS_add = 'http://10.129.83.21:8001'
    DCT_add = 'http://10.128.82.23'
    EQUIP_add = 'http://kspqiswww'
    All_system_dic = {}
    data = {}
    gridData = []
    Navigations_system_name =''
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    if request.method == "POST":
        # print(request.GET)
        if request.POST.get("isGetData") == "first":
            pass
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'first' in str(request.body):
                    responseData = json.loads(request.body)
                    Sysname = responseData["Sysname"]
                    print(Sysname)
                    if Sysname:
                        gridData = All_system_dic[Sysname]
                        data = {
                            "gridData": gridData,
                        }
                        response = HttpResponse(json.dumps(data), content_type="application/json")
                        # 设置中文字符的cookie需要序列化和反序列化过程
                        response.set_cookie('Navigations_system_name', json.dumps(Sysname), max_age=3600 * 24 * 7)

                        return response
                    else:
                        # 设置中文字符的cookie需要序列化和反序列化过程
                        Navigations_system_name = json.loads(request.COOKIES.get('Navigations_system_name'))
                        print(Navigations_system_name)
                        gridData = All_system_dic[Navigations_system_name]
        data = {
            "gridData": gridData,
            "Navigations_system_name": Navigations_system_name
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsCustomer.html', locals())

@csrf_exempt
def PermInfo_axios(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/Customer"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)

    data = {}
    tableContent1 = []
    tableContent_C38 = [
        {
            "Category": "品質管控", "System": "NonDQA_LL", "RoleName": "DQA_ME_edit", "DQA_All": "", "ME_Manager": "V", "SW_Manager": "", "DQA_QM": "V", "DQA_AQM": "V",
            "RD_DD": "V", "RD_LD": "V", "RD_MEFG": "V", "RD_SW_Search": "V",
        },
        {
            "Category": "品質管控", "System": "QIL", "RoleName": "DQA_INV_edit, DQA_ME_edit, DQA_SW_edit, ", "DQA_All": "", "ME_Manager": "V",
            "SW_Manager": "V", "DQA_QM": "V", "DQA_AQM": "V",
            "RD_DD": "V", "RD_LD": "V", "RD_MEFG": "V", "RD_SW_Search": "V",
        },

    ]
    heBingNum_C38 = [2,]
    tableContent_ABO = [

    ]
    heBingNum_ABO = []
    tableContent_CQT88 = [

    ]
    heBingNum_CQT88 = []
    tableContent_A31 = [

    ]
    heBingNum_A31 = []
    tableContent_ = [

    ]
    heBingNum_ = []
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    if request.method == "POST":
        # print(request.GET)
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("Sysname"))
            permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
            for i in permission_url:
                tableContent1.append({"url": i})
        data = {
            "tableContent_C38": tableContent_C38,
            "tableContent_ABO": tableContent_ABO,
            "tableContent_CQT88": tableContent_CQT88,
            "tableContent_A31": tableContent_A31,
            "tableContent_": tableContent_,
            "heBingNum_C38": heBingNum_C38,
            "heBingNum_ABO": heBingNum_ABO,
            "heBingNum_CQT88": heBingNum_CQT88,
            "heBingNum_A31": heBingNum_A31,
            "heBingNum_": heBingNum_,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Navigations/NavigationsSystem.html', locals())

@csrf_exempt
def logout(request):
    # print('t')
    # print (request.session.get('is_login', None))
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        # print('logout')
        return redirect("/login/")
    # flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")


@csrf_exempt
def Change_Password(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    # print (request.method)
    if request.method == "POST":
        OldPassword = request.POST.get('OldPassword')
        Password = request.POST.get('Password')
        Passwordc = request.POST.get('Confirm')
        user = request.session.get('user_name')
        userpass = UserInfo.objects.get(username=user).password
        # print(OldPassword,userpass)
        if OldPassword == userpass:
            if Password == Passwordc:
                # print(request.session.get('user_name', None))
                updatep = UserInfo.objects.filter(username=request.session.get('user_name', None))
                # print (updatep)
                # for e in updatep:
                #    print (e.password)
                updatep.update(password=Password)
                request.session.flush()
                return redirect("/login/")
            else:
                message = "Password is not same"
                return render(request, 'changepassword.html', locals())
        else:
            message = "Incorrect Password"
            return render(request, 'changepassword.html', locals())
    return render(request, 'changepassword.html', locals())


@csrf_exempt
def Change_Skin(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # print(request.method)
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    # print(Skin)
    # print(request.method, request.POST)
    weizhi = "Change Skin"
    Render = render(request, 'ChangeSkin.html', locals())
    Redirect = redirect('/Change_Skin/')
    if request.method == "POST":
        print(2)
        if 'blue' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/blue.jpg", 3600 * 24 * 30 * 12)
        if 'kiwi' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/kiwi.jpg", 3600 * 24 * 30 * 12)
        if 'sunny' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/sunny.jpg", 3600 * 24 * 30 * 12)
        if 'yellow' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/yellow.jpg", 3600 * 24 * 30 * 12)
        if 'chrome' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/chrome.jpg", 3600 * 24 * 30 * 12)
        if 'ocean' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/ocean.jpg", 3600 * 24 * 30 * 12)
        return Redirect
        # return redirect('/index/')
    # return redirect('/index/')
    # print(Skin)
    return Render


@csrf_exempt
def Lesson_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Upload"
    message = ''
    message_err = 0
    # form=TestUEditorForm()
    lesson_form = lessonlearn(request.POST)
    if request.method == "POST":
        lesson = lessonlearn(request.POST)
        # test = request.POST.get('test')
        # print(test)
        if lesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
            Category = lesson.cleaned_data['Category']
            Object = lesson.cleaned_data['Object']
            Symptom = lesson.cleaned_data['Symptom']
            Reproduce_Steps = lesson.cleaned_data['Reproduce_Steps']
            Root_Cause = lesson.cleaned_data['Root_Cause']
            Comments = lesson.cleaned_data['Solution']
            Action = lesson.cleaned_data['Action']
            Status = lesson.cleaned_data['Status']
            # print(Comments)
            Photo = request.FILES.getlist("myfiles", "")
            print(Photo)
            Object_check = lesson_learn.objects.filter(Object=Object)
            Symptom_check = lesson_learn.objects.filter(Symptom=Symptom)
            # print (Object_check,Symptom_check)
            # if Object_check:
            #     #message = "Object '%s' already exists" % (Object)
            #     message_err=1
            #     return render(request, 'Lesson_upload.html',locals())
            # else:
            if Symptom_check:
                # message = "Symptom '%s' already exists" % (Symptom)
                message_err = 2
                return render(request, 'Lesson_upload.html', locals())
            else:
                # Photos=''
                # for image in Photo:
                #     # print (image.name)
                #     if not Photos:
                #         Photos='img/test/'+image.name
                #     else:
                #         Photos=Photos+','+'img/test/'+image.name
                # print (Photos)
                lesson = lesson_learn()
                lesson.Category = Category
                lesson.Object = Object
                lesson.Symptom = Symptom
                lesson.Reproduce_Steps = Reproduce_Steps
                lesson.Root_Cause = Root_Cause
                lesson.Solution = Comments
                lesson.Action = Action
                lesson.Status = Status
                # lesson.Photo=Photos
                lesson.editor = request.session.get('user_name')
                lesson.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lesson.save()
                # print(request.FILES.getlist('myfiles'),request.POST.get('myfiles'))
                # print(request.FILES)
                for f in request.FILES.getlist('myfiles'):
                    # print(f)
                    empt = Imgs()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.img = f
                    empt.save()
                    lesson.Photo.add(empt)
                for f in request.FILES.getlist('myvideos'):
                    # print(f)
                    empt = Files()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.Files = f
                    empt.save()
                    lesson.video.add(empt)
                message = "Upload '%s' Successfully" % (Object)

                # print (lessonlearn())
                # print(lessonlearn(request.POST))
                # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                return render(request, 'Lesson_upload.html', locals())
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    # print (locals())
    return render(request, 'Lesson_upload.html',
                  locals())  # {'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})


@csrf_exempt
def Lesson_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Redit"
    errMsg = ''
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
    form = {
        # "Category": "SW",
        # "Object": "Design",
        # "Symptom": "asdfghjghtjymk,jkjh",
        # "Reproduce_Steps": "esyrtduyfukigliukyjtyt",
        # "Root_Cause": "esrdtgfjyhjjhgryter",
        # "Solution": "esrthdyhyjytrwetgrthyjtyrhtjyjyrghthygr",
        # "Action": "grhdtgyjhygrhtjthyrthygrzhh"
        # # "photo":[{name: 'food.jpeg', url: '/static/images/spec.png'},
        # #           {name: 'food2.jpeg', url: '/static/images/spec.png'}]
    }
    fileListO = [
        # {'name': 'Screenshot_15.png', 'url': '/media/img/test/Screenshot_15.png'}
    ]
    fileList1 = [
        # {'name': 'Screenshot_15.png', 'url': '/media/img/test/Screenshot_15.png'}
    ]
    # print(request.POST)
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    Lesson_list = lesson_learn.objects.all()
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append({"id": h.id, "url": "/media/" + str(h.img)})
                    else:
                        filelist.append({"id": h.id, "url": "/media/" + str(h.img)})
                Videolist = []
                for h in i.video.all():
                    Videolist.append({"id": h.id, "url": "/media/" + str(h.files)})
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Status": i.Status,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "alertID":
            id = request.POST.get('ID')
            if id:
                editlesson = lesson_learn.objects.get(id=id)
                form["Category"] = editlesson.Category
                form["Object"] = editlesson.Object
                form["Symptom"] = editlesson.Symptom
                form["Reproduce_Steps"] = editlesson.Reproduce_Steps
                form["Root_Cause"] = editlesson.Root_Cause
                form["Solution"] = editlesson.Solution
                form["Action"] = editlesson.Action
                form["Status"] = editlesson.Status
                # print(len(editlesson.Photo.all()),len(editlesson.video.all()))
                for i in editlesson.Photo.all():
                    # print(i.img,type(i.img),)
                    # print(i.img.name)
                    fileListO.append({'name': '', 'url': '/media/' + i.img.name})

                for i in editlesson.video.all():
                    fileList1.append({'name': '', 'url': '/media/'+i.files.name})
            data = {
                'form': form,
                'fileListO': fileListO,
                'fileList1': fileList1,
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "submit":
            errMsg = ''
            try:
                serchCategory = request.POST.get("serchCategory")
                editID = request.POST.get('id')
                # print(serchCategory, request.POST.get('Category'))
                Photolist = request.FILES.getlist("new_photos", "")
                videolist = request.FILES.getlist("new_videos", "")
                # 获取待删除文件列表
                photos_to_delete = json.loads(request.POST.get('photos_to_delete', '[]'))
                videos_to_delete = json.loads(request.POST.get('videos_to_delete', '[]'))
                # print(photos_to_delete, videos_to_delete)

                # print(Photolist,editID)
                if editID:
                    # print("1")
                    editlesson = lesson_learn.objects.get(id=editID)
                    editlesson.Category = request.POST.get('Category')
                    editlesson.Object = request.POST.get('Object')
                    editlesson.Symptom = request.POST.get('Symptom')
                    editlesson.Reproduce_Steps = request.POST.get('Reproduce_Steps')
                    editlesson.Root_Cause = request.POST.get('Root_Cause')
                    editlesson.Solution = request.POST.get('Solution')
                    editlesson.Action = request.POST.get('Action')
                    editlesson.Status = request.POST.get('Status')
                    # lesson.Photo=Photos
                    editlesson.editor = request.session.get('user_name')
                    editlesson.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    editlesson.save()
                    if Photolist:
                        for f in Photolist:
                            # print(f)
                            if f.name.split(".")[1] == "mp4" or f.name.split(".")[1] == "AVI" or f.name.split(".")[
                                1] == "mov" or f.name.split(".")[1] == "rmvb":
                                # empt = files()
                                # # 增加其他字段应分别对应填写
                                # empt.single = f
                                # empt.files = f
                                # empt.save()
                                # editlesson.video.add(empt)
                                pass
                            else:
                                empt = Imgs()
                                # 增加其他字段应分别对应填写
                                empt.single = f
                                empt.img = f
                                empt.save()
                                editlesson.Photo.add(empt)

                    # image_ids = request.POST.getlist('image_ids[]')

                    # 获取图片对象
                    # images = Imgs.objects.filter(single__in=image_ids)
                    images = Imgs.objects.filter(id__in=photos_to_delete)#最好是用id，这样搜索时就需要返回带id的信息
                    # print(images)

                    # 解除关联
                    editlesson.Photo.remove(*images)  # 使用 * 解包列表
                    images.delete()  # 删除实体文件 model中的files_SopRom_delete方法
                    if videolist:
                        for f in videolist:
                            # print(f)
                            empt = Files()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            editlesson.video.add(empt)
                    vedios = Files.objects.filter(id__in=videos_to_delete)  # 最好是用id，这样搜索时就需要返回带id的信息
                    # print(vedios)

                    # 解除关联
                    editlesson.video.remove(*vedios)  # 使用 * 解包列表
                    vedios.delete()  # 删除实体文件 model中的files_SopRom_delete方法
                if serchCategory:
                    # print(Category)
                    Check_dic = {"Category": serchCategory}
                    Lesson_list = lesson_learn.objects.filter(**Check_dic)
                else:
                    Lesson_list = lesson_learn.objects.all()
                for i in Lesson_list:
                    Photolist = []
                    filelist = []
                    for h in i.Photo.all():
                        # print(str(h.img).split("."))
                        if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                            Photolist.append({"id": h.id, "url": "/media/" + str(h.img)})
                        else:
                            filelist.append({"id": h.id, "url": "/media/" + str(h.img)})
                    Videolist = []
                    for h in i.video.all():
                        Videolist.append({"id": h.id, "url": "/media/" + str(h.files)})
                    # print(Photolist)
                    mock_data.append(
                        {
                            "id": i.id,
                            "Category": i.Category,
                            "Object": i.Object,
                            "Symptom": i.Symptom,
                            "Reproduce_Steps": i.Reproduce_Steps,
                            "Root_Cause": i.Root_Cause,
                            "Solution": i.Solution,
                            "Action": i.Action,
                            "Status": i.Status,
                            "Photo": Photolist,
                            "file": filelist,
                            "Video": Videolist,
                            "editor": i.editor,
                            "edit_time": i.edit_time,
                        },
                    )
                # print(mock_data)

                # fileList = [{name: 'food.jpeg', url: '/static/images/spec.png'},
                #             {name: 'food2.jpeg', url: '/static/images/spec.png'}]
            except Exception as e:
                errMsg = str(e)
            data = {
                #     'fileList': fileList
                'addselect': selectCategory,
                'content': mock_data,
                'errMsg': errMsg,
            }
                # print(updateData)

            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Lesson_edit.html', locals())


def Lesson_update(request, id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Redit/%s" % id
    message = ''
    # form=TestUEditorForm()
    lesson_formdefault = lesson_learn.objects.get(id=id)
    # print(lesson_formdefault)
    # print(request.POST)
    lesson_form = lessonlearn(request.POST)

    if request.method == "POST":
        lesson = lessonlearn(request.POST)
        if lesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
            Object = lesson.cleaned_data['Object']
            Symptom = lesson.cleaned_data['Symptom']
            Root_Cause = lesson.cleaned_data['Root_Cause']
            # print(Root_Cause)
            Comments = lesson.cleaned_data['Solution']
            Action = lesson.cleaned_data['Action']
            choose = request.POST.get('choose')
            choosev = request.POST.get('choosev')
            # print(choose)
            # print(Root_Cause,Comments)
            Photo = request.FILES.getlist("myfiles", "")
            # lesson = lesson_learn()
            # print(lesson_formdefault)
            # print (lesson)
            lesson_formdefault.Object = Object
            lesson_formdefault.Symptom = Symptom
            lesson_formdefault.Root_Cause = Root_Cause
            lesson_formdefault.Solution = Comments
            lesson_formdefault.Action = Action
            # lesson.Photo=Photos
            lesson_formdefault.editor = request.session.get('user_name')
            lesson_formdefault.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lesson_formdefault.save()
            if choose == "删除原图片":
                lesson_formdefault.Photo.clear()
            for f in request.FILES.getlist('myfiles'):
                # print(f)
                empt = Imgs()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.img = f
                empt.save()
                lesson_formdefault.Photo.add(empt)
                # lesson_formdefault.Photo.remove()
            if choosev == "删除原视频":
                lesson_formdefault.video.clear()
            for f in request.FILES.getlist('myvideos'):
                # print(f)
                empt = Files()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                lesson_formdefault.video.add(empt)
                # lesson_formdefault.video.remove()
            id = id
            message_redit = "Redit '%s' Successfully" % (id)
            # print (lessonlearn())
            # print(lessonlearn(request.POST))
            # return render(request, 'Lesson_update.html',locals())
            return redirect('/Lesson_edit/')
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    else:
        values = {'Object': lesson_formdefault.Object, 'Symptom': lesson_formdefault.Symptom,
                  'Root_Cause': lesson_formdefault.Root_Cause, 'Solution': lesson_formdefault.Solution,
                  'Action': lesson_formdefault.Action}
        lesson_form = lessonlearn(values)
    # print (locals())
    # print(settings.BASE_DIR,settings.STATICFILES_DIRS)
    return render(request, 'Lesson_update.html',
                  locals())  # {'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})
    # return render(request, 'Lesson_update.html', locals())


@csrf_exempt
def Lesson_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # Categoryfromcookie = request.COOKIES.get('cookieSWME')#cookie也是可以的，但是每次设置cookie时都要返回redirect，如果要返回Jason给axios，就没法用了
    Categoryfromcookie = request.session.get('sessionSWME')
    print(Categoryfromcookie)
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Search"
    # Lesson_list=lesson_learn.objects.all()
    Lesson_list = lesson_learn.objects.filter(Category=Categoryfromcookie)
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
    canEdit = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    # print(roles)
    editPpriority = 100
    for i in roles:
        if 'admin' in i:
            editPpriority = 4
            canEdit = 1
        # elif 'PM' in i:
        #     if editPpriority != 4:
        #         editPpriority = 1
        # elif 'RD' in i:
        #     if editPpriority != 4 and editPpriority != 1:
        #         editPpriority = 2
        elif 'DQA' in i:
            canEdit = 1
            # if 'DQA_SW' in i:
            #     if editPpriority != 4 and editPpriority != 1:
            #         editPpriority = 5
            # if 'DQA_ME' in i:
            #     if editPpriority != 4 and editPpriority != 1:
            #         editPpriority = 6
        # elif "JQE" in i:
        #     editPpriority = 3
        # else:
        #     editPpriority = 0
    # print(request.method)
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if i == 'admin':
            # editPpriority = 4
            canExport = 1
        elif i == 'DQA_director':
            canExport = 1
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("isGetData"), '111')
            if Categoryfromcookie:
                for i in Lesson_list:
                    Photolist = []
                    filelist = []
                    for h in i.Photo.all():
                        # print(str(h.img).split("."))
                        if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(h.img))
                        else:
                            filelist.append("/media/" + str(h.img))
                    Videolist = []
                    for h in i.video.all():
                        Videolist.append("/media/" + str(h.files))
                    # print(Photolist)
                    mock_data.append(
                        {
                            "id": i.id,
                            "Category": i.Category,
                            "Object": i.Object,
                            "Symptom": i.Symptom,
                            "Reproduce_Steps": i.Reproduce_Steps,
                            "Root_Cause": i.Root_Cause,
                            "Solution": i.Solution,
                            "Action": i.Action,
                            "Status": i.Status,
                            "Photo": Photolist,
                            "file": filelist,
                            "Video": Videolist,
                            "editor": i.editor,
                            "edit_time": i.edit_time,
                        },
                    )
                request.session['sessionSWME'] = None

            data = {
                'addselect': selectCategory,
                'content': mock_data,
                "canEdit": canEdit,
                'canExport': canExport,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Status": i.Status,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
                "canEdit": canEdit,
                'canExport': canExport,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        # Lesson_list_dic = []
        # for i in Lesson_list:
        #     Photolist = []
        #     for j in i.Photo.all():
        #         Photolist.append("/media/"+str(j.img))
        #     videolist = []
        #     for j in i.video.all():
        #         videolist.append("/media/"+str(j.files))
        #     Lesson_list_dic.append({"id":i.id, "Category":i.Category, "Object":i.Object, "Symptom":i.Symptom, "Reproduce_Steps":i.Reproduce_Steps,
        #                             "Root_Cause":i.Root_Cause, "Solution":i.Solution, "Action":i.Action, "Photo":Photolist, "video":videolist, "edit_time":i.edit_time,})
        #         # data = {
        #         #     'Lesson_list': Lesson_list_dic,
        # }
        # return HttpResponse(json.dumps(data), content_type="application/json")
        # print(locals())
    return render(request, 'Lesson_search.html', locals())


@csrf_exempt
def Lesson_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Search"
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
    # print(request.method)
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("isGetData"), '111')
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        # Lesson_list_dic = []
        # for i in Lesson_list:
        #     Photolist = []
        #     for j in i.Photo.all():
        #         Photolist.append("/media/"+str(j.img))
        #     videolist = []
        #     for j in i.video.all():
        #         videolist.append("/media/"+str(j.files))
        #     Lesson_list_dic.append({"id":i.id, "Category":i.Category, "Object":i.Object, "Symptom":i.Symptom, "Reproduce_Steps":i.Reproduce_Steps,
        #                             "Root_Cause":i.Root_Cause, "Solution":i.Solution, "Action":i.Action, "Photo":Photolist, "video":videolist, "edit_time":i.edit_time,})
        #         # data = {
        #         #     'Lesson_list': Lesson_list_dic,
        # }
        # return HttpResponse(json.dumps(data), content_type="application/json")
        # print(locals())

    return render(request, 'Lesson_export.html', locals())


@csrf_exempt
def ttt(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "/ttt"

    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (img)
    #     for i in img:
    #         print (i.img)
    return render(request, 'ttt.html', locals())


from django.http import JsonResponse
from app01 import tasks


@csrf_exempt
def ctest(request, *args, **kwargs):
    res = tasks.print_test.delay()
    # 任务逻辑
    return JsonResponse({'status': 'successful', 'task_id': res.task_id})
