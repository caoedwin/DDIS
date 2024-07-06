from django.shortcuts import render,redirect,HttpResponse
from app01.models import UserInfo,lesson_learn,Imgs,files,ProjectinfoinDCT,Role,Permission,Menu
from django.views.decorators.csrf import csrf_exempt
from Bouncing.models import Bouncing_M
from Package.models import Package_M
from CDM.models import CDM
from TestPlanME.models import TestProjectME,TestItemME,TestPlanME
from LessonProjectME.models import lessonlearn_Project
from DriverTool.models import DriverList_M,ToolList_M
from MQM.models import MQM
from TestPlanSW.models import TestProjectSW, TestProjectSWAIO
from CQM.models import CQMProject, CQM, CQM_history
from QIL.models import QIL_M, QIL_Project
import datetime,os
from service.init_permission import init_permission
from django.conf import settings
# Create your views here.
from django.forms import forms
from DjangoUeditor.forms import UEditorField
from app01.forms import lessonlearn
from django.conf import settings
import datetime,json,requests,time,simplejson
from requests_ntlm import HttpNtlmAuth
from INVGantt.models import INVGantt
from django.http import HttpResponseRedirect
# from app01.templatetags.custom_tag import *
from .tasks import ProjectSync, ImportProjectinfoFromDCT

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
            return redirect(request.COOKIES['current_page_DDIS'])
        except:
            return redirect('/index/')

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
                request.session.set_expiry(12*60*60)
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
                print(Non_login_path,'Non_login_path')
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
    # Skin = request.COOKIES.get('Skin_raw')
    # # print(Skin)
    # if not Skin:
    #     Skin = "/static/src/blue.jpg"
    # weizhi="Home/Dashboard"
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
    R_P_data=Package_M.objects.all().values('Project').distinct().count()
    R_B_data=Bouncing_M.objects.all().values('Project').distinct().count()
    R_C_data=CDM.objects.all().values('Project').distinct().count()
    T_M_Project=TestProjectME.objects.all().values('Project').distinct().count()
    X_D_DriverList=DriverList_M.objects.all().values('Project').distinct().count()
    X_D_ToolList=ToolList_M.objects.all().values('Project').distinct().count()
    X_M_Project=MQM.objects.all().values('Project').distinct().count()
    T_S_Project=TestProjectSW.objects.all().values('Project').distinct().count()+TestProjectSWAIO.objects.all().values('Project').distinct().count()
    X_C_data = CQMProject.objects.all().values('Project').distinct().count()
    ProI_data = ProjectinfoinDCT.objects.all().values('ComPrjCode').distinct().count()
    # for i in TestProjectME.objects.all().values('Customer', 'Project', 'Phase').distinct():
    #     print(i)
    T_M_Items=TestItemME.objects.all().count()
    T_I_Project = INVGantt.objects.all().values("Project_Name").distinct().count()
    # importPrjResult = ImportProjectinfoFromDCT()
    # print(request.POST)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Reliability":
            #cookie
            # Redirect = redirect('/Lesson_search/')
            # Reliabilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Reliabilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Compatibility":
            #cookie
            # Redirect = redirect('/Lesson_search/')
            # Compatibilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Compatibilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    return render(request, 'index.html', locals())

@csrf_exempt
def ProjectInfoSearch(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Home/ProjectInfoSearch"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "Year": "Y2020", "Comprjcode": "FLAT4", "Prjengcode1": "TATA4",
        #  "Prjengcode2": "", "Mkt_Code": "E41-55",
        #  "Size": "14", "CPU": "AMD", "Platform": "AMD", "VGA": "UMA", "OS_Support": "WIN10 20H1", "SS": "2020-09-28",
        #  "LD": "陈威", "DQA_PL": "周课",
        #  "Modified_Date": "2020-09-11 21:19:01"},
        # {"id": "2", "Customer": "C38(AIO)", "Year": "Y2019", "Comprjcode": "EOC20", "Prjengcode1": "TATA4",
        #  "Prjengcode2": "", "Mkt_Code": "E41-55",
        #  "Size": "14", "CPU": "AMD", "Platform": "AMD", "VGA": "UMA", "OS_Support": "WIN10 20H1", "SS": "2019-07-28",
        #  "LD": "陈威", "DQA_PL": "周课",
        #  "Modified_Date": "2019-07-28 21:19:01"},
        # {"id": "3", "Customer": "T88(AIO)", "Year": "Y2018", "Comprjcode": "FLAT4", "Prjengcode1": "TATA4",
        #  "Prjengcode2": "", "Mkt_Code": "E41-55",
        #  "Size": "14", "CPU": "AMD", "Platform": "AMD", "VGA": "UMA", "OS_Support": "WIN10 20H1", "SS": "2018-10-28",
        #  "LD": "陈威", "DQA_PL": "周课",
        #  "Modified_Date": "2018-11-11 21:19:01"},
    ]
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
    print(ProjectinfoinDCT.objects.all().values("ComPrjCode").distinct().count(), ProjectinfoinDCT.objects.all().values("ComPrjCode").count(), ProjectinfoinDCT.objects.all().values("ComPrjCode", "Year").distinct().count())
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
                    {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode, "Prjengcode1": i.PrjEngCode1,
                     "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                     "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA, "OS_Support": i.OSSupport, "Type": i.Type,
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS,"LD": i.LD, "DQA_PL": i.DQAPL,
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
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LDNum": i.LDNum, "DQA_PL": i.DQAPL, "DQA_PLNum": i.DQAPLNum,
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
            for i in ProjectinfoinDCT.objects.filter(**checkdic_PRODCT):
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Year": i.Year, "Comprjcode": i.ComPrjCode,
                     "Prjengcode1": i.PrjEngCode1,
                     "Prjengcode2": i.PrjEngCode2, "Mkt_Code": i.ProjectName,
                     "Size": i.Size, "CPU": i.CPU, "Platform": i.Platform, "VGA": i.VGA, "OS_Support": i.OSSupport,
                     "Type": i.Type,
                     "PPA": i.PPA, "PQE": i.PQE, "SS": i.SS, "LD": i.LD, "LDNum": i.LDNum, "DQA_PL": i.DQAPL, "DQA_PLNum": i.DQAPLNum,
                     "Modified_Date": i.ModifiedDate}
                )
            pass
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            'addselect': selectYear,
            'canExport': canExport,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ProjectInfo_search.html', locals())

from django.core.mail import EmailMultiAlternatives
from TestPlanSW.models import TestProjectSW,TestPlanSW
def Mailhtml():# settings Email设置1-外網qq
    print("Starthtmlmail")
    # subject 主题 content 内容 to_addr 是一个列表，发送给哪些人
    # msg = EmailMultiAlternatives('邮件标题', '邮件内容', '发送方', ['接收方'])
    Projectinfo_TestPlanSWMail = {}
    for i in TestProjectSW.objects.all().values("Project", "Phase").distinct().order_by("Project", "Phase"):
        # print(i["BR_per_code"])
        Projectinfo_TestPlanSW = []
        eachProj = TestProjectSW.objects.filter(Project=i["Project"], Phase=i["Phase"]).first()
        if eachProj.ScheduleEnd:
            if datetime.datetime.now().date() > eachProj.ScheduleEnd:
                Exceed_days = round(
                    float(
                        str((datetime.datetime.now().date() - eachProj.ScheduleEnd)).split(' ')[
                            0]),
                    0)
            else:
                Exceed_days = ''
        else:
            Exceed_days = ''
        flagTestPlanSW = len(TestPlanSW.objects.filter(Projectinfo=eachProj)) == 0
        flagCQM = len(CQM.objects.filter(Project=i["Project"], Phase=i["Phase"])) == 0
        flagDriverList_M = len(DriverList_M.objects.filter(Project=i["Project"], Phase0=i["Phase"])) == 0
        flagToolList_M = len(ToolList_M.objects.filter(Project=i["Project"], Phase0=i["Phase"])) == 0
        if Exceed_days and (flagTestPlanSW or flagCQM
                            or flagDriverList_M or flagToolList_M):
            # print(list(eachProj.Owner.all()),1)
            # print(flagCQM,flagDriverList_M,flagTestPlanSW,flagToolList_M)
            dataNotupdate = []
            if flagTestPlanSW:
                dataNotupdate.append('TestPlanSW')
            if flagCQM:
                dataNotupdate.append('CQM')
            if flagDriverList_M:
                dataNotupdate.append('DriverList')
            if flagToolList_M:
                dataNotupdate.append('ToolList')
            to_emails = []
            ProjectOwners = []
            for k in eachProj.Owner.all():
                to_emails.append(k.email)
                ProjectOwners.append(k.username)
            Projectinfo_TestPlanSW.append(
                {"id": eachProj.id, "Customer": eachProj.Customer, "Project": eachProj.Project,
                 "Phase": eachProj.Phase,
                 "ScheduleBegin": eachProj.ScheduleBegin,
                 "ScheduleEnd": eachProj.ScheduleEnd, "Full_Function_Duration": eachProj.Full_Function_Duration,
                 "Gerber": eachProj.Gerber,
                 "Project_Code": eachProj.Project,
                 # "Owner": list(eachProj.Owner.all()),
                 "Owner": ProjectOwners,
                 "to_emails": to_emails,
                 "dataNotupdate": dataNotupdate,
                 "Exceed_days": Exceed_days,
                 },
            )
            # print(Projectinfo_TestPlanSW)
        if Projectinfo_TestPlanSW:
            Projectinfo_TestPlanSWMail[i["Project"]] = Projectinfo_TestPlanSW
        message = ""
    # print(BR_perinfo,len(BR_perinfo))
    # print(Projectinfo_TestPlanSWMail)

    #每个机种发一个邮件，过于频繁，可能会受邮箱限制，导致报错smtplib.SMTPDataError: (550, b'Mail content denied.
    # for key, value in Projectinfo_TestPlanSWMail.items():
    #     # print(value)
    #     messagecontend = """<p>Dear All:</p>
    #         <p>您的如下机种已經超期， 請儘快上传到DDIS系统：</p>
    #         <a href="http://10.129.83.21:8002/index/" style="font-size: 20px;background-color: yellow;font-weight: bolder;" target="_blank">点击此处，处理设备</a>
    #         <p>未更新数据详情：</p>
    #           <p></p>
    #           <table border="1" cellpadding="0" cellspacing="0" width="1800" style="border-collapse: collapse;">
    #            <tbody>
    #             <tr>
    #              <th style="background-color: #8c9eff">机种信息</th>
    #              <th style="background-color: #8c9eff">Phase</th>
    #              <th style="background-color: #8c9eff">数据类型</th>
    #              <th style="background-color: #8c9eff">超期天数（天）</th>
    #             </tr>
    #             {sub_td}
    #           </tbody>
    #           </table>
    #         <p style="color:red;">注：此郵件由系統自動發出，請勿直接回復,如特殊情况无需更新数据，请忽略。</p>
    #                                 """ \
    #                      # % value[0]["Owner"]
    #     sub_td = ""
    #     sub_td_items = """
    #         <tr>
    #          <td  style="text-align:center"> {sub_item_Project} </td>
    #          <td  style="text-align:center"> {sub_item_Phase} </td>
    #          <td  style="text-align:center"> {sub_item_data} </td>
    #          <td  style="text-align:center;color:red;"> {sub_item_Exceedday} </td>
    #         </tr>
    #         """
    #     for j in value:
    #         # print(j)
    #         sub_td += sub_td_items.format(sub_item_Project=j["Project"], sub_item_Phase=j["Phase"],
    #                                       sub_item_data=j["dataNotupdate"], sub_item_Exceedday=j["Exceed_days"],)
    #     message = messagecontend.format(sub_td=sub_td)
    #     # print(message)
    #     subject = '【DDIS】数据上传提醒'
    #     from_email = '416434871@qq.com'
    #     to_email = []
    #     # to_email.append(value[0]["to_emails"])
    #     to_email.append('edwin_cao@compal.com')
    #     # print(key)
    #     # print(to_email)
    #     msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    #     msg.content_subtype = "html"
    #     # 添加附件（可选）
    #     # msg.attach_file('test.txt')
    #     # 发送
    #     msg.send()
    #发一个总的邮件
    messagecontend = """<p>Dear All:</p>
                <p>您的如下机种已經超期， 請儘快上传到DDIS系统：</p>
                <a href="http://10.129.83.21:8002/index/" style="font-size: 20px;background-color: yellow;font-weight: bolder;" target="_blank">点击此处，处理设备</a>
                <p>未更新数据详情：</p>
                  <p></p>
                  <table border="1" cellpadding="0" cellspacing="0" width="1800" style="border-collapse: collapse;">
                   <tbody>
                    <tr>
                     <th style="background-color: #8c9eff">机种信息</th>
                     <th style="background-color: #8c9eff">Phase</th>
                     <th style="background-color: #8c9eff">数据类型</th>
                     <th style="background-color: #8c9eff">超期天数（天）</th>
                    </tr>
                    {sub_td}
                  </tbody>
                  </table> 
                <p style="color:red;">注：此郵件由系統自動發出，請勿直接回復,如特殊情况无需更新数据，请忽略。</p>
                                        """ \
        # % value[0]["Owner"]
    sub_td = ""
    to_email = []
    for key, value in Projectinfo_TestPlanSWMail.items():
        # print(value)
        sub_td_items = """
            <tr>
             <td  style="text-align:center"> {sub_item_Project} </td>
             <td  style="text-align:center"> {sub_item_Phase} </td>
             <td  style="text-align:center"> {sub_item_data} </td>
             <td  style="text-align:center;color:red;"> {sub_item_Exceedday} </td>
            </tr>
            """
        # to_email.append(value[0]["to_emails"])
        to_email.extend(value[0]["to_emails"])#合并list
        for j in value:
            # print(j)
            sub_td += sub_td_items.format(sub_item_Project=j["Project"], sub_item_Phase=j["Phase"],
                                          sub_item_data=j["dataNotupdate"], sub_item_Exceedday=j["Exceed_days"],)
    message = messagecontend.format(sub_td=sub_td)
    # print(message)
    subject = '【DDIS】数据上传提醒'
    from_email = '416434871@qq.com'

    # to_email.append('edwin_cao@compal.com')

    # print(key)
    # print(to_email)
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.content_subtype = "html"
    # 添加附件（可选）
    # msg.attach_file('test.txt')
    # 发送
    msg.send()

def MailOAtest():# settings Email设置2-内網OA
    message = 'ddistest'
    print(message)
    subject = '【DDIS】数据上传提醒'
    from_email = 'DDIS@compal.com'
    to_email = []
    to_email.append('edwin_cao@compal.com')

    # print(key)
    # print(to_email)
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.content_subtype = "html"
    # 添加附件（可选）
    # msg.attach_file('test.txt')
    # 发送
    msg.send()

@csrf_exempt
def FilesDownload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Home/ProjectInfo"
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
    weizhi="Home/ProjectInfo"
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
def logout(request):
    # print('t')
    # print (request.session.get('is_login', None))
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        # print('logout')
        return redirect("/login/")
    #flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意
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
        OldPassword=request.POST.get('OldPassword')
        Password = request.POST.get('Password')
        Passwordc = request.POST.get('Confirm')
        user=request.session.get('user_name')
        userpass=UserInfo.objects.get(username=user).password
        # print(OldPassword,userpass)
        if OldPassword==userpass:
            if Password==Passwordc:
                # print(request.session.get('user_name', None))
                updatep = UserInfo.objects.filter(username=request.session.get('user_name', None))
                # print (updatep)
                # for e in updatep:
                #    print (e.password)
                updatep.update(password=Password)
                request.session.flush()
                return redirect("/login/")
            else:
                message="Password is not same"
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
    weizhi = "Change Skin"
    Render = render(request, 'ChangeSkin.html', locals())
    Redirect=redirect('/Change_Skin/')
    if request.method == "POST":

        if 'blue' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/blue.jpg", 3600 * 24 * 30 * 12)
        if 'kiwi' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/kiwi.jpg", 3600 * 24 * 30 * 12)
        if 'sunny' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/sunny.jpg",3600*24*30*12)
        if 'yellow' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/yellow.jpg",3600*24*30*12)
        if 'chrome' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/chrome.jpg",3600*24*30*12)
        if 'ocean' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/ocean.jpg",3600*24*30*12)
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
    weizhi="Lesson-Learn/Reliability/Upload"
    message=''
    message_err=0
    # form=TestUEditorForm()
    lesson_form=lessonlearn(request.POST)
    if request.method == "POST":
        lesson=lessonlearn(request.POST)
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
            Object_check =lesson_learn.objects.filter(Object=Object)
            Symptom_check=lesson_learn.objects.filter(Symptom=Symptom)
            # print (Object_check,Symptom_check)
            # if Object_check:
            #     #message = "Object '%s' already exists" % (Object)
            #     message_err=1
            #     return render(request, 'Lesson_upload.html',locals())
            # else:
            if Symptom_check:
                #message = "Symptom '%s' already exists" % (Symptom)
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
                lesson=lesson_learn()
                lesson.Category = Category
                lesson.Object=Object
                lesson.Symptom=Symptom
                lesson.Reproduce_Steps = Reproduce_Steps
                lesson.Root_Cause = Root_Cause
                lesson.Solution=Comments
                lesson.Action = Action
                lesson.Status = Status
                # lesson.Photo=Photos
                lesson.editor=request.session.get('user_name')
                lesson.edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
                    empt = files()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.files = f
                    empt.save()
                    lesson.video.add(empt)
                message="Upload '%s' Successfully" %(Object)

                # print (lessonlearn())
                # print(lessonlearn(request.POST))
                # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                return render(request, 'Lesson_upload.html', locals())
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    # print (locals())
    return render(request, 'Lesson_upload.html',locals())#{'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})

@csrf_exempt
def Lesson_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Lesson-Learn/Reliability/Redit"
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
    # print(request.POST)
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    Lesson_list=lesson_learn.objects.all()
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
                    fileListO.append({'name': '', 'url': '/media/'+i.img.name})

                for i in editlesson.video.all():
                    fileListO.append({'name': '', 'url': '/media/'+i.files.name})
            data = {
                    'form': form,
                    'fileListO': fileListO
                }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("action") == "submit":
            serchCategory = request.POST.get("serchCategory")
            editID = request.POST.get('id')
            # print(serchCategory, request.POST.get('Category'))
            Photolist = request.FILES.getlist("fileList", "")
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
                        if f.name.split(".")[1] == "mp4" or f.name.split(".")[1] == "AVI" or f.name.split(".")[1] == "mov" or f.name.split(".")[1] == "rmvb":
                            empt = files()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            editlesson.video.add(empt)
                        else:
                            empt = Imgs()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.img = f
                            empt.save()
                            editlesson.Photo.add(empt)
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

            # fileList = [{name: 'food.jpeg', url: '/static/images/spec.png'},
            #             {name: 'food2.jpeg', url: '/static/images/spec.png'}]
            data = {
            #     'fileList': fileList
                'addselect': selectCategory,
                'content': mock_data,
             }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Lesson_edit.html', locals())

def Lesson_update(request,id):
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
            if choose=="删除原图片":
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
            if choosev=="删除原视频":
                lesson_formdefault.video.clear()
            for f in request.FILES.getlist('myvideos'):
                # print(f)
                empt = files()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                lesson_formdefault.video.add(empt)
                # lesson_formdefault.video.remove()
            id=id
            message_redit = "Redit '%s' Successfully" % (id)
            # print (lessonlearn())
            # print(lessonlearn(request.POST))
            # return render(request, 'Lesson_update.html',locals())
            return redirect('/Lesson_edit/')
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    else:
        values = {'Object': lesson_formdefault.Object, 'Symptom': lesson_formdefault.Symptom, 'Root_Cause': lesson_formdefault.Root_Cause, 'Solution': lesson_formdefault.Solution, 'Action': lesson_formdefault.Action}
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
    weizhi="Lesson-Learn/Reliability/Search"
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
    weizhi="Lesson-Learn/Reliability/Search"
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
    weizhi="/ttt"

    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (img)
    #     for i in img:
    #         print (i.img)
    return render(request, 'ttt.html', locals())


from django.http import JsonResponse
from app01 import tasks
@csrf_exempt
def ctest(request,*args,**kwargs):
    res=tasks.print_test.delay()
    #任务逻辑
    return JsonResponse({'status':'successful','task_id':res.task_id})