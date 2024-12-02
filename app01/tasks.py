from celery.task import task
from app01.models import UserInfo
from TestPlanSW.models import TestProjectSW, TestPlanSW
from CQM.models import CQM
from DriverTool.models import DriverList_M, ToolList_M
import datetime
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from requests_ntlm import HttpNtlmAuth
import datetime, json, requests, time, simplejson, os
from app01.models import UserInfo, lesson_learn, Imgs, ProjectinfoinDCT, Role, Permission, Menu
from CriticalIssueCrossCheck.models import CriticalIssue, CriticalIssueCrossResult


# 自定义要执行的task任务
# 在项目manage.py统计目录下cmd或pycharmTerminal运行celery worker -A mydjango -l info -P eventlet，celery -A mydjango beat -l info
# 窗口不能关闭
@task
def Ongoing_flag():
    path = settings.BASE_DIR
    file_flag = path + '/' + 'scheduleflag.txt'
    print(file_flag)
    with open(file_flag, 'w') as f:  # 设置文件对象
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), file=f)


@task
def ProjectSync():
    print("Start")
    DATE_NOW = str(datetime.datetime.now().date())
    importPrjResult = ImportProjectinfoFromDCT()
    path = settings.BASE_DIR
    file_flag = path + '/logs/' + 'ProjectSync-%s.txt' % (
            DATE_NOW.split("-")[0] + DATE_NOW.split("-")[1] + DATE_NOW.split("-")[2])
    # print(file_flag)
    with open(file_flag, 'w') as f:  # 设置文件对象
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), importPrjResult, file=f)
    if importPrjResult:
        return "OK"
    else:
        return "Fail"


def ImportProjectinfoFromDCT():
    url = r'http://192.168.1.10/dct/api/ClientSvc/getAllProjectInfo'
    requests.adapters.DEFAULT_RETRIES = 1
    # s = requests.session()
    # s.keep_alive = False  # 关闭多余连接
    # getTestSpec=requests.get(url)
    headers = {'Connection': 'close'}
    try:
        r = requests.get(url, headers=headers)
        getTestSpec = requests.get(url)
        # print (getTestSpec.url)
    except:
        # time.sleep(0.1)
        print("Can't connect to DCT Sercer")
        return 0
    targetURL = getTestSpec.url
    # url=r"http://127.0.0.1"

    url.split('\n')[0]
    # print url
    # 输入用户名和密码python requests实现windows身份验证登录
    try:
        getTestSpec = requests.get(targetURL, auth=HttpNtlmAuth('DCT\\administrator', 'DQA3`2018'))
    except:
        # time.sleep(0.1)
        print("try request agian")
        return 0
    # print(type(getTestSpec.json()), getTestSpec.json())
    numb = 0
    for i in getTestSpec.json():
        numb += 1
        # print(i,i['Size'])
        localPrjCre = {"Customer": i['Customer'],
                       "Year": i['Year'],
                       "ComPrjCode": i['ComPrjCode'],
                       "PrjEngCode1": i['PrjEngCode1'],
                       "PrjEngCode2": i['PrjEngCode2'],
                       "ProjectName": i['ProjectName'],
                       "Size": i['Size'], "CPU": i['CPU'],
                       "Platform": i['Platform'],
                       "VGA": i['VGA'],
                       "OSSupport": i['OSSupport'],
                       "Type": i['Type'],
                       "PPA": i['PPA'],
                       "PQE": i['PQE'],
                       "SS": i['SS'],
                       "LD": i['LD'].split("-")[0],
                       "LDNum": i['LD'].split("-")[1] if len(i['LD'].split("-")) == 2 else "",
                       "DQAPL": i['DQAPL'].split("-")[0],
                       "DQAPLNum": i['DQAPL'].split("-")[1] if len(i['DQAPL'].split("-")) == 2 else "",
                       "ModifiedDate": i['ModifyDate']
                       }
        # print(localPrjCre)
        if ProjectinfoinDCT.objects.filter(Customer=i['Customer'], ComPrjCode=i['ComPrjCode']):
            ProjectinfoinDCT.objects.filter(Customer=i['Customer'], ComPrjCode=i['ComPrjCode']).update(**localPrjCre)
        else:
            ProjectinfoinDCT.objects.create(**localPrjCre)

    # print(getTestSpec.text)
    # print("Project數量：", numb)

    # ProjectNameList = []
    # for i in Package_M.objects.all().values('Project').distinct():
    #     # print(i['Project'])
    #     ProjectNameList.append(i['Project'])
    # for i in Bouncing_M.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in CDM.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in DriverList_M.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in ToolList_M.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in MQM.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in TestProjectME.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in TestProjectSW.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in CQMProject.objects.all().values('Project').distinct():
    #     ProjectNameList.append(i['Project'])
    # for i in INVGantt.objects.all().values('Project_Name').distinct():
    #     ProjectNameList.append(i['Project_Name'])
    #
    # # print(ProjectNameList)
    # ProjectNameList = list(set(ProjectNameList))
    # # print(ProjectNameList)
    # sameandlocal=[]
    # samePrj=[]
    # nosamePjr = []
    # numpro = 0
    # for i in ProjectNameList:
    #     numpro += 1
    #     project = "ProjectCode=" + i
    #     url = r'http://192.168.1.10/dct/api/ClientSvc/getProjectInfo'
    #     requests.adapters.DEFAULT_RETRIES = 1
    #     # s = requests.session()
    #     # s.keep_alive = False  # 关闭多余连接
    #     # getTestSpec=requests.get(url)
    #     headers = {'Connection': 'close'}
    #     try:
    #         r = requests.get(url, headers=headers)
    #         getTestSpec = requests.get(url, project)
    #         # print (getTestSpec.url)
    #     except:
    #         # time.sleep(0.1)
    #         print("Can't connect to DCT Sercer")
    #         return 0
    #     targetURL = getTestSpec.url
    #     # url=r"http://127.0.0.1"
    #
    #     url.split('\n')[0]
    #     # print url
    #     # 输入用户名和密码python requests实现windows身份验证登录
    #     try:
    #         getTestSpec = requests.get(targetURL, auth=HttpNtlmAuth('DCT\\administrator', 'DQA3`2018'))
    #     except:
    #         # time.sleep(0.1)
    #         print("try request agian")
    #         return 0
    #
    #     # print 1
    #     # print getTestSpec.url
    #     # newjson = getTestSpec.json()
    #     # print(newjson)
    #     newstr = getTestSpec.text.replace('<br>', ' ')
    #     # print (newstr)
    #     newstr1 = newstr.replace('":"', '*!')
    #     # print(newstr1)
    #     newstr2 = newstr1.replace('", "', '!*')
    #     newstr2 = newstr2.replace('","', '!*')
    #     newstr2 = newstr2.replace('" , "', '!*')
    #     # print(newstr2)
    #     newstr3 = newstr2.replace('{"', '/!')
    #     # print(newstr3)
    #     newstr4 = newstr3.replace('"  }', '!/')
    #     # print(newstr4)
    #     newstr5 = newstr4.replace('"', '')
    #     # print(newstr5)
    #     newstr6 = newstr5.replace('*!', '":"')
    #     # print(newstr6)
    #     newstr7 = newstr6.replace('!*', '","')
    #     # print(newstr7)
    #     newstr8 = newstr7.replace('/!', '{"')
    #     # print(newstr8)
    #     newstr9 = newstr8.replace('!/', '"}')
    #     # print("9", newstr9, type(newstr9))
    #     if not ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
    #         # print("j9", json.loads(newstr9))
    #         if json.loads(newstr9)['ComPrjCode']:
    #             samePrj.append(i)
    #             localPrjCre = {"Customer": json.loads(newstr9)['Customer'],
    #                         "Year": json.loads(newstr9)['Year'],
    #                            "ComPrjCode": json.loads(newstr9)['ComPrjCode'],
    #                            "PrjEngCode1": json.loads(newstr9)['PrjEngCode1'],
    #                            "PrjEngCode2": json.loads(newstr9)['PrjEngCode2'],
    #                            "ProjectName": json.loads(newstr9)['ProjectName'],
    #                            "Size": json.loads(newstr9)['Size'], "CPU": json.loads(newstr9)['CPU'],
    #                            "Platform": json.loads(newstr9)['Platform'],
    #                            "VGA": json.loads(newstr9)['VGA'],
    #                            "OSSupport": json.loads(newstr9)['OSSupport'],
    #                            "SS": json.loads(newstr9)['SS'],
    #                            "LD": json.loads(newstr9)['LD'], "DQAPL": json.loads(newstr9)['DQAPL'],
    #                            "ModifiedDate": json.loads(newstr9)['ModifyDate']
    #                            }
    #             ProjectinfoinDCT.objects.create(**localPrjCre)
    #         else:
    #             nosamePjr.append(i)
    #     else:
    #         sameandlocal.append(i)
    #         # print("j92", json.loads(newstr9))
    #         if json.loads(newstr9)['ComPrjCode']:
    #             localPrjUpdate = {"Customer": json.loads(newstr9)['Customer'],
    #                         "Year": json.loads(newstr9)['Year'],
    #                            "ComPrjCode": json.loads(newstr9)['ComPrjCode'],
    #                            "PrjEngCode1": json.loads(newstr9)['PrjEngCode1'],
    #                            "PrjEngCode2": json.loads(newstr9)['PrjEngCode2'],
    #                            "ProjectName": json.loads(newstr9)['ProjectName'],
    #                            "Size": json.loads(newstr9)['Size'], "CPU": json.loads(newstr9)['CPU'],
    #                            "Platform": json.loads(newstr9)['Platform'],
    #                            "VGA": json.loads(newstr9)['VGA'],
    #                            "OSSupport": json.loads(newstr9)['OSSupport'],
    #                            "SS": json.loads(newstr9)['SS'],
    #                            "LD": json.loads(newstr9)['LD'], "DQAPL": json.loads(newstr9)['DQAPL'],
    #                               "ModifiedDate": json.loads(newstr9)['ModifyDate']}
    #             ProjectinfoinDCT.objects.filter(ComPrjCode=i).update(**localPrjUpdate)

    # print(sameandlocal)
    # print(samePrj)
    # print(nosamePjr)
    # print(numpro)
    return numb


@task
def MailhtmlSync():
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

    # 每个机种发一个邮件，过于频繁，可能会受邮箱限制，导致报错smtplib.SMTPDataError: (550, b'Mail content denied.
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
    # 发一个总的邮件
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
        to_email.extend(value[0]["to_emails"])  # 合并list
        for j in value:
            # print(j)
            sub_td += sub_td_items.format(sub_item_Project=j["Project"], sub_item_Phase=j["Phase"],
                                          sub_item_data=j["dataNotupdate"], sub_item_Exceedday=j["Exceed_days"], )
    message = messagecontend.format(sub_td=sub_td)
    # print(message)
    subject = '【DDIS】数据上传提醒'
    from_email = '416434871@qq.com'
    # from_email = 'Edwin_Cao@compal.com'

    # to_email.append('edwin_cao@compal.com')

    # print(key)
    # print(to_email)
    msg = EmailMultiAlternatives(subject, message, from_email, to_email)
    msg.content_subtype = "html"
    # 添加附件（可选）
    # msg.attach_file('test.txt')
    # 发送
    msg.send()


@task
def Mailhtml():  # settings Email设置1-外網qq
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

    # 每个机种发一个邮件，过于频繁，可能会受邮箱限制，导致报错smtplib.SMTPDataError: (550, b'Mail content denied.
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
    # 发一个总的邮件
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
        to_email.extend(value[0]["to_emails"])  # 合并list
        for j in value:
            # print(j)
            sub_td += sub_td_items.format(sub_item_Project=j["Project"], sub_item_Phase=j["Phase"],
                                          sub_item_data=j["dataNotupdate"], sub_item_Exceedday=j["Exceed_days"], )
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


from exchangelib import Credentials, Account, Message, Mailbox, HTMLBody, Configuration, DELEGATE, NTLM, FileAttachment, \
    CalendarItem
from exchangelib.protocol import BaseProtocol, NoVerifyHTTPAdapter
from exchangelib.recurrence import Recurrence, WeeklyPattern, DailyPattern, RelativeMonthlyPattern
from exchangelib.fields import MONDAY, WEDNESDAY, FRIDAY
from exchangelib.items import MeetingRequest, MeetingCancellation, SEND_TO_ALL_AND_SAVE_COPY
import urllib3
from datetime import datetime, timedelta


# 如果需要设置日历提醒，可以添加CalendarItem
@task
def MailOAtest(**kwargs):  # settings Email设置2-内網OA(Exchange)
    # 此句用来消除ssl证书错误，exchange使用自签证书需加上
    print(kwargs)

    CriticalIssues = kwargs['ids']
    Projects = kwargs['Projects']
    to_recipients = []
    cc_recipients = []
    for i in Projects:
        print(i)
        if UserInfo.objects.filter(
            account=ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPLNum):
            to_recipients.append(Mailbox(email_address=str(UserInfo.objects.filter(
                account=ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPLNum).first().email)))
        if UserInfo.objects.filter(
            account=ProjectinfoinDCT.objects.filter(ComPrjCode=i).first()):
            cc_recipients.append(Mailbox(email_address=str(UserInfo.objects.filter(
                account=ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAQMNum).first().email)))



    BaseProtocol.HTTP_ADAPTER_CLS = NoVerifyHTTPAdapter
    urllib3.disable_warnings()  # 取消SSL安全连接警告
    # 填入你的Exchange服务器地址、用户名和密码
    server = 'webmail.compal.com'
    primary_smtp_address = 'edwin_cao@compal.com'
    # username = 'gi\edwin_cao'
    # password = '~1234qwer'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mailaccount_file = os.path.join(BASE_DIR, 'OAmail_account.json')
    # print(mailaccount_file)
    if os.path.exists(mailaccount_file):
        try:
            with open(mailaccount_file, 'r', encoding='utf-8') as file:
                data = file.read()
            username = data.split(",")[0]
            password = data.split(",")[1]
            print(username, password)

            # html = '<html><body>Hello happy <blink>OWA user!</blink></body></html>'

            # 用凭证连接到Exchange服务器
            credentials = Credentials(username=username, password=password)
            config = Configuration(server=server, credentials=credentials, auth_type=NTLM)
            account = Account(primary_smtp_address=primary_smtp_address, credentials=credentials, config=config,
                              autodiscover=False, access_type=DELEGATE)

            # 邮件
            html = Html(**kwargs)
            mail = Message(
                account=account,
                subject='【DDIS-CriticalIssue】Cross Check提醒第一次',
                body=HTMLBody(html),
                to_recipients=to_recipients,
                cc_recipients=cc_recipients,
                # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
                #                Mailbox(email_address='edwin_cao@compal.com')],
            )

            # logo_filename = 'logo.png'
            # with open(logo_filename, 'rb') as f:
            #     logo = FileAttachment(
            #         filename=logo_filename,
            #         content=f.read(),
            #     )
            # mail.attach(logo)
            # 发送邮件
            mail.send()

            # # 创建日历提醒
            # start = datetime.datetime.now(tz=account.default_timezone)
            # # start = datetime.datetime(2017, 9, 1, 11, tzinfo=account.default_timezone)  # 放在CalendarItem外面
            # end = start + datetime.timedelta(hours=24)
            # ci = CalendarItem(
            #     folder=account.calendar,
            #     subject='Test Appointment',
            #     body=HTMLBody(html),
            #     start=start,
            #     end=end,
            #     recurrence=Recurrence(
            #         pattern=DailyPattern(interval=1),
            #         start=start.date(),
            #         number=1,)
            # )
            # ci.save()  # 用来发送会议邀请邮件ci.save()#用来发送会议邀请邮件

            # # 會議
            # ci = CalendarItem(
            #     account=account,
            #     folder=account.calendar,
            #     start=datetime.datetime.now(tz=account.default_timezone),
            #     end=datetime.datetime.now(tz=account.default_timezone) + timedelta(hours=24),
            #     subject="Test meeting",
            #     body=HTMLBody(html),
            #     required_attendees=["edwin_cao@compal.com", "edwin_cao@compal.com"],
            #     recurrence=Recurrence(
            #
            #     )
            # )
            # ci.save(send_meeting_invitations=SEND_TO_ALL_AND_SAVE_COPY)

            # 获取当前时间
            now = datetime.now()

            # 设置当天10点的时间
            excute_of_day1 = datetime.combine(now.date(), datetime.strptime('10:00', '%H:%M').time())
            # 设置当天15点的时间
            excute_of_day2 = datetime.combine(now.date(), datetime.strptime('15:00', '%H:%M').time())

            # 如果当前时间超过了上午10点，则10点还有多少秒就是下个10点的秒数
            if now > excute_of_day1:
                excute_of_day1 += timedelta(days=1)
            # 如果当前时间超过了下午15点，则15点还有多少秒就是下个15点的秒数
            if now > excute_of_day2:
                excute_of_day2 += timedelta(days=1)

            # 计算时间差
            seconds_until_1 = (excute_of_day1 - now).seconds
            seconds_until_2 = (excute_of_day2 - now).seconds

            # if seconds_until_1 > seconds_until_2:
            #     time.sleep(seconds_until_2)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check第二次',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
            #     time.sleep(seconds_until_1 - seconds_until_2)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check第三次',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
            #     time.sleep(24 * 60 * 60 - seconds_until_1)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check截至',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
            # else:
            #     time.sleep(seconds_until_1)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check第二次',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
            #     time.sleep(seconds_until_2 - seconds_until_1)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check第三次',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
            #     time.sleep(24 * 60 * 60 - seconds_until_2)
            #     html = Html(**kwargs)
            #     mail = Message(
            #         account=account,
            #         subject='【DDIS-CriticalIssue】Cross Check截止',
            #         body=HTMLBody(html),
            #         to_recipients=to_recipients,
            #         cc_recipients=cc_recipients,
            #         # bcc_recipients=[Mailbox(email_address='edwin_cao@compal.com'),
            #         #                Mailbox(email_address='edwin_cao@compal.com')],
            #     )
            #     mail.send()
        except Exception as e:
            print(str(e))

    else:
        print("OAmail_account.json不存在")


def Html(**kwargs):
    CriticalIssues = kwargs['ids']
    CriticalIssues = kwargs['ids']
    Projects = kwargs['Projects']

    messagecontend = """
                        <p style="color:red;">注：此郵件由系統自動發出，請勿直接回復!!!</p>
                        <p>Dear All:</p>
                        <p>您的机种需要check如下issue并更新结果到DDIS：</p>
                        <a href="http://10.129.83.21:8002/CriticalIssueCrossCheck/CriticalIssue_ProjectResult/" style="font-size: 20px;background-color: yellow;font-weight: bolder;" target="_blank">点击此处，更新结果</a>
                        
                          <p></p>
                          <table border="1" cellpadding="0" cellspacing="0" width="1800" style="border-collapse: collapse;">
                           <tbody>
                             <tr>
                                 <th rowspan=2 style="background-color: #8c9eff">IssueNum</th>
                                 <th rowspan=2 style="background-color: #8c9eff">CG</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Category</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Symptom</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Reproduce_Steps</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Root_Cause</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Solution</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Action</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Project</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Status</th>
                                 <th rowspan=2 style="background-color: #8c9eff">Owner</th>
                                {sub_th}
                            </tr>
                            <tr>
                                {sub_th_2cd}
                            </tr>
                                {sub_td}
                          </tbody>
                          </table> 
                                                """
    sub_th = ""
    sub_thItem = """
                <th colspan=2 style="background-color: #8c9eff">{Projectname}</th>
        """
    sub_th_2cd = ""
    sub_th_2cdItem = """
                    <th>Result</th>
                    <th>Comments</th>
            """
    for i in Projects:
        sub_th += sub_thItem.format(Projectname=i)
    num = 0
    for i in Projects:
        num += 1
        if num <= len(Projects):
            sub_th_2cd += sub_th_2cdItem



    sub_td = ""
    to_email = []
    for i in CriticalIssues:
        # print(value)
        sub_td_items = """
                                    <tr>
                                         <td  style="text-align:center"> {sub_IssueNum} </td>
                                         <td  style="text-align:center"> {sub_CG} </td>
                                         <td  style="text-align:center"> {sub_Category} </td>
                                         <td  style="text-align:center;"> {sub_Symptom} </td>
                                         <td  style="text-align:center;"> {sub_Reproduce_Steps} </td>
                                         <td  style="text-align:center;"> {sub_Root_Cause} </td>
                                         <td  style="text-align:center;"> {sub_Solution} </td>
                                         <td  style="text-align:center;"> {sub_Action} </td>
                                         <td  style="text-align:center;"> {sub_Project} </td>
                                         <td  style="text-align:center;"> {sub_Status} </td>
                                         <td  style="text-align:center;"> {sub_Owner} </td>
                                        {sub_sub_Projectreult}
                                    </tr>
                                    """
        CI = CriticalIssue.objects.filter(id=i).first()
        sub_sub_Projectreult = ""
        sub_sub_Projectreult_Items = """
                <td>{result}</td>
                <td>{comments}</td>
            """
        for j in Projects:
            # print(j)
            Projectlink = ProjectinfoinDCT.objects.filter(ComPrjCode=j).first()
            CIR = CriticalIssueCrossResult.objects.filter(Projectinfo=Projectlink, CriticalIssue=CI).first()
            sub_sub_Projectreult += sub_sub_Projectreult_Items.format(result=CIR.result, comments=CIR.Comment)
        sub_td += sub_td_items.format(sub_IssueNum=CI.id, sub_CG=CI.CG, sub_Category=CI.Category,
                                      sub_Symptom=CI.Symptom,
                                      sub_Reproduce_Steps=CI.Reproduce_Steps, sub_Root_Cause=CI.Root_Cause,
                                      sub_Solution=CI.Solution, sub_Action=CI.Action,
                                      sub_Project=CI.Project, sub_Status=CI.Status, sub_Owner=CI.editor,
                                      sub_sub_Projectreult=sub_sub_Projectreult)
    html = messagecontend.format(sub_th=sub_th, sub_th_2cd=sub_th_2cd, sub_td=sub_td)
    print(html)
    return html


@task
def scheduleMailOA_CriticalIssue():
    pass
