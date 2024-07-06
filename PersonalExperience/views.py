from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime, json, simplejson, requests, time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import UserInfo, Role, ProjectinfoinDCT
from PersonalInfo.models import PersonalInfo, Positions
from django.db.models import Max, Min, Sum, Count, Q, F, Value, CharField
from django.db.models.functions import Substr
from operator import itemgetter, attrgetter
from collections import Counter
from .models import PerExperience, OSR_OSinfo
from django.db.models.functions import ExtractYear
from app01 import consumers

# from notifications.signals import notify
Approved_Officer_NPI_ME_C38 = '0701114'
Approved_Officer_NPI_ME_AIO = '0801046'
ME_funtion = 'Reliability'
Approved_Officer_INV_NB = "0576972"


@csrf_exempt
def NPI_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/NPI_upload"

    errMsgNumber = ''

    sectionProject = [
        # {"value": "GLMS1", "SS_Date": "2021/02/03"}, {"value": "HLS4I", "SS_Date": "2021/02/04"},
    ]

    for i in ProjectinfoinDCT.objects.all():
        datastr = i.SS.split(' ')[0].split('/')
        sectionProject.append({"value": i.ComPrjCode, "SS_Date": datastr[2] + "-" + datastr[0] + "-" + datastr[1]})
    # print(request.body)
    # print(request.POST)
    if request.method == "POST":
        consumers.send_group_msg('Reliability_Row_data', {'content': '正在安装系统', 'level': 2})
        try:
            if request.POST.get('action') == 'addSubmit':
                # print(request.POST.get('Project'))
                updata_dic = {}
                updata_dic['Proposer_Num'] = request.session.get('account')
                # updata_dic['Proposer_NameE'] = request.session.get('user_name')
                PersonalInfos = PersonalInfo.objects.filter(
                    Q(GroupNum=updata_dic['Proposer_Num']) | Q(SAPNum=updata_dic['Proposer_Num'])).first()
                # print(PersonalInfos)
                updata_dic['Project'] = request.POST.get('Project')
                updata_dic['Role'] = request.POST.get('Role')
                updata_dic['Function'] = request.POST.get('Function')
                updata_dic['SubFunction_Com'] = request.POST.get('SubFunction')
                updata_dic['Phase'] = request.POST.get('Phase')
                if PerExperience.objects.filter(**updata_dic):
                    errMsgNumber = "您已申请过：Project:%s-Phase:%s-Function:%s-SubFunction:%s-Role:%s" % (
                        updata_dic['Project'], updata_dic['Phase'],
                        updata_dic['Function'], updata_dic['SubFunction_Com'],
                        updata_dic['Role'])
                else:
                    # 填寫人信息
                    updata_dic['Proposer_Name'] = PersonalInfos.CNName
                    updata_dic['Department_Code'] = PersonalInfos.DepartmentCode
                    updata_dic['Item'] = PersonalInfos.PositionNow
                    YearNow = datetime.datetime.now().strftime("%Y")
                    updata_dic['Positions_Name'] = Positions.objects.filter(Item=PersonalInfos.PositionNow,
                                                                            Year=YearNow).first(). \
                        Positions_Name if Positions.objects.filter(Item=PersonalInfos.PositionNow, Year=YearNow) else ''
                    # 機種名變更可能隨之變動
                    updata_dic['Dalei'] = "NPI"
                    if ME_funtion == updata_dic['Function']:
                        CustomerPro = ProjectinfoinDCT.objects.filter(
                            ComPrjCode=request.POST.get('Project')).first().Customer
                        if CustomerPro == "C38(AIO)" or CustomerPro == "T88(AIO)":
                            updata_dic['Approved_Officer'] = Approved_Officer_NPI_ME_AIO
                        else:
                            updata_dic['Approved_Officer'] = Approved_Officer_NPI_ME_C38
                    else:
                        updata_dic['Approved_Officer'] = ProjectinfoinDCT.objects.filter(
                            ComPrjCode=request.POST.get('Project')).first().DQAPLNum
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first())
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first().DQAPLNum)
                    updata_dic['SS_Date'] = request.POST.get('SS_Date')
                    # 流程變更
                    updata_dic['Status'] = "待簽核"

                    updata_dic['Comments'] = request.POST.get('Comments')
                    updata_dic['EditTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    if updata_dic['Approved_Officer']:
                        PerExperience.objects.create(**updata_dic)
                        # notify.send(actor, recipient, verb, target, action_object)
                        # 其中的参数释义：
                        #
                        # actor：发送通知的对象
                        # recipient：接收通知的对象
                        # verb：动词短语
                        # target：链接到动作的对象（可选）
                        # action_object：执行通知的对象（可选）
                        # 有点绕，举个栗子：杜赛(actor),在Django搭建个人博客(target),中对你(recipient),发表了(verb),评论(action_object)。
                        # print(type(UserInfo.objects.filter(account=request.session.get('account'))))
                        # print(type(UserInfo.objects.get(account=request.session.get('account'))))
                        # print(request.user,type(request.user))
                        # notify.send(
                        #     # request.session.get('account'),
                        #     # sender=UserInfo.objects.get(account=request.session.get('account')),
                        #     sender=UserInfo.objects.get(account=request.session.get('account')),
                        #     recipient=UserInfo.objects.filter(account=ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first().DQAPLNum).first(),
                        #     # recipient=UserInfo.objects.get(account=ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first().DQAPLNum),
                        #     verb='需要签核',
                        #     # target="人员测试履历",# target：链接到动作的对象（可选）
                        #     # target=PerExperience.objects.filter(Project=updata_dic['Project'], Role=updata_dic['Role'], Function=updata_dic['Function'], SubFunction_Com=updata_dic['SubFunction_Com'], Phase=updata_dic['Phase']),# target：链接到动作的对象（可选）
                        #     # action_object=,# action_object：执行通知的对象（可选）
                        # )
                        # print(request.session.get('account'))
                    else:
                        errMsgNumber = "Project:%s DQAPL的工号缺失" % updata_dic['Project']
        except Exception as e:
            errMsgNumber = str(e)

        data = {
            "sectionProject": sectionProject,
            "errMsgNumber": errMsgNumber,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/NPI_upload.html', locals())


@csrf_exempt
def INV_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/INV_upload"

    errMsgNumber = ''

    sectionProject = [
        # {"value": "GLMS1", "SS_Date": "2021/02/03"}, {"value": "HLS4I", "SS_Date": "2021/02/04"},
    ]
    for i in ProjectinfoinDCT.objects.all():
        datastr = i.SS.split(' ')[0].split('/')
        sectionProject.append({"value": i.ComPrjCode, "SS_Date": datastr[2] + "-" + datastr[0] + "-" + datastr[1]})

    if request.method == 'POST':
        try:
            if request.POST.get('action') == 'addSubmit':
                # print(request.POST.get('Project'))
                updata_dic = {}
                updata_dic['Proposer_Num'] = request.session.get('account')
                # updata_dic['Proposer_NameE'] = request.session.get('user_name')
                PersonalInfos = PersonalInfo.objects.filter(
                    Q(GroupNum=updata_dic['Proposer_Num']) | Q(SAPNum=updata_dic['Proposer_Num'])).first()
                # print(PersonalInfos)
                updata_dic['Project'] = request.POST.get('Project')
                updata_dic['Role'] = request.POST.get('Role')
                updata_dic['Function'] = request.POST.get('Function')
                updata_dic['Time_Interval'] = request.POST.get('Month')
                updata_dic['Year'] = request.POST.get('Year')
                if PerExperience.objects.filter(**updata_dic):
                    errMsgNumber = "您已申请过：Project:%s-Function:%s-Time_Interval:%s-Year:%s-Role:%s" % (
                        updata_dic['Project'],
                        updata_dic['Function'], updata_dic['Time_Interval'], updata_dic['Year'],
                        updata_dic['Role'])
                else:
                    # 個人信息
                    updata_dic['Proposer_Name'] = PersonalInfos.CNName
                    updata_dic['Department_Code'] = PersonalInfos.DepartmentCode
                    updata_dic['Item'] = PersonalInfos.PositionNow
                    YearNow = datetime.datetime.now().strftime("%Y")
                    updata_dic['Positions_Name'] = Positions.objects.filter(Item=PersonalInfos.PositionNow,
                                                                            Year=YearNow).first(). \
                        Positions_Name if Positions.objects.filter(Item=PersonalInfos.PositionNow, Year=YearNow) else ''
                    # 機種名變更可能隨之變動
                    updata_dic['Dalei'] = "INV"
                    updata_dic['KeypartNum'] = request.POST.get('KeypartNum')
                    updata_dic['Approved_Officer'] = ProjectinfoinDCT.objects.filter(
                        ComPrjCode=request.POST.get('Project')).first().DQAPLNum
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first())
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first().DQAPLNum)
                    updata_dic['SS_Date'] = request.POST.get('SS_Date')
                    # 流程變更
                    updata_dic['Status'] = "待簽核"

                    updata_dic['Comments'] = request.POST.get('Comments')
                    updata_dic['EditTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    if updata_dic['Approved_Officer']:
                        PerExperience.objects.create(**updata_dic)
                    else:
                        errMsgNumber = "Project:%s DQAPL的工号缺失" % updata_dic['Project']
        except Exception as e:
            errMsgNumber = str(e)
        data = {
            "sectionProject": sectionProject,
            "errMsgNumber": errMsgNumber,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/INV_upload.html', locals())


@csrf_exempt
def OSR_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/OSR_upload"

    errMsgNumber = ''

    sectionProject = [
        # {"value": "GLMS1", "SS_Date": "2021/02/03"}, {"value": "HLS4I", "SS_Date": "2021/02/04"},
    ]

    sectionPhase = [
        # "Win11", "win10", "XP"
    ]
    for i in OSR_OSinfo.objects.all():
        sectionPhase.append(i.OSinfo)
    CanEdit = 0
    DQAPLNum = request.session.get('account')
    for i in ProjectinfoinDCT.objects.all():
        datastr = i.SS.split(' ')[0].split('/')
        sectionProject.append({"value": i.ComPrjCode, "SS_Date": datastr[2] + "-" + datastr[0] + "-" + datastr[1]})
        if DQAPLNum == i.DQAPLNum:
            CanEdit = 1
    if request.method == 'POST':
        try:
            if request.POST.get('action') == 'SubmitOSR':
                # print(request.POST.get('Project'))
                updataOS_dic = {}
                updataOS_dic['OSinfo'] = request.POST.get('OSR')
                if OSR_OSinfo.objects.filter(**updataOS_dic):
                    errMsgNumber = "OS:%s 已经存在" % updataOS_dic['OSinfo']
                else:
                    updataOS_dic['EditTime'] = datetime.datetime.now().strftime("%Y-%m-%d")
                    updataOS_dic['Editer'] = request.session.get('account')
                    OSR_OSinfo.objects.create(**updataOS_dic)
                    sectionPhase = [
                        # "Win11", "win10", "XP"
                    ]
                    for i in OSR_OSinfo.objects.all():
                        sectionPhase.append(i.OSinfo)
            if request.POST.get('action') == 'addSubmit':
                # print(request.POST.get('Project'))
                updata_dic = {}
                updata_dic['Proposer_Num'] = request.session.get('account')
                # updata_dic['Proposer_NameE'] = request.session.get('user_name')
                PersonalInfos = PersonalInfo.objects.filter(
                    Q(GroupNum=updata_dic['Proposer_Num']) | Q(SAPNum=updata_dic['Proposer_Num'])).first()
                # print(PersonalInfos)
                updata_dic['Project'] = request.POST.get('Project')
                updata_dic['Role'] = request.POST.get('Role')
                updata_dic['Function'] = request.POST.get('Function')
                updata_dic['SubFunction_Com'] = request.POST.get('SubFunction')
                updata_dic['Phase'] = request.POST.get('Phase')
                if PerExperience.objects.filter(**updata_dic):
                    errMsgNumber = "您已申请过：Project:%s-Phase:%s-Function:%s-SubFunction:%s-Role:%s" % (
                        updata_dic['Project'], updata_dic['Phase'],
                        updata_dic['Function'], updata_dic['SubFunction_Com'],
                        updata_dic['Role'])
                else:
                    updata_dic['Proposer_Name'] = PersonalInfos.CNName
                    updata_dic['Department_Code'] = PersonalInfos.DepartmentCode
                    updata_dic['Item'] = PersonalInfos.PositionNow
                    YearNow = datetime.datetime.now().strftime("%Y")
                    updata_dic['Positions_Name'] = Positions.objects.filter(Item=PersonalInfos.PositionNow,
                                                                            Year=YearNow).first(). \
                        Positions_Name if Positions.objects.filter(Item=PersonalInfos.PositionNow, Year=YearNow) else ''
                    # 機種名變更可能隨之變動
                    updata_dic['Dalei'] = "OSR"
                    updata_dic['Approved_Officer'] = ProjectinfoinDCT.objects.filter(
                        ComPrjCode=request.POST.get('Project')).first().DQAPLNum
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first())
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=request.POST.get('Project')).first().DQAPLNum)
                    updata_dic['SS_Date'] = request.POST.get('SS_Date')
                    # 流程變更
                    updata_dic['Status'] = "待簽核"

                    updata_dic['Comments'] = request.POST.get('Comments')
                    updata_dic['EditTime'] = datetime.datetime.now().strftime("%Y-%m-%d")

                    if updata_dic['Approved_Officer']:
                        PerExperience.objects.create(**updata_dic)
                    else:
                        errMsgNumber = "Project:%s DQAPL的工号缺失" % updata_dic['Project']
        except Exception as e:
            errMsgNumber = str(e)
        data = {
            "sectionProject": sectionProject,
            "sectionPhase": sectionPhase,
            "errMsgNumber": errMsgNumber,
            "CanEdit": CanEdit,

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/OSR_upload.html', locals())


@csrf_exempt
def My_application(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/My_application"

    tableData = [
        # {"id": 1, "Approved_Officer": "郭四梅", "Status": "待簽核", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OOC", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "234",
        #  },
        # {"id": 2, "Approved_Officer": "郭四梅", "Status": "同意", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OSR-Win11", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
        # {"id": 3, "Approved_Officer": "郭四梅", "Status": "拒絕", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
    ]

    sectionProject = [
        # {"value": "GLMS1", "SS_Date": "2021/02/03"}, {"value": "HLS4I", "SS_Date": "2021/02/04"},
    ]
    for i in ProjectinfoinDCT.objects.all():
        datastr = i.SS.split(' ')[0].split('/')
        sectionProject.append({"value": i.ComPrjCode, "SS_Date": datastr[2] + "-" + datastr[0] + "-" + datastr[1]})

    sectionPhase = [
        # "Win11", "Win10", "XP"
    ]
    for i in OSR_OSinfo.objects.all():
        sectionPhase.append(i.OSinfo)

    account_login = request.session.get('account')
    PersonalInfos = PersonalInfo.objects.filter(
        Q(GroupNum=account_login) | Q(SAPNum=account_login)).first()

    errMsgNumber = ''

    if request.method == "POST":
        try:
            if request.POST.get('isGetData') == 'first':
                for i in PerExperience.objects.filter(Proposer_Num=account_login):
                    tableData.append(
                        {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                            Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                        PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                            SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                         "Status": i.Status, "Department_Code": i.Department_Code,
                         "Proposer_Num": i.Proposer_Num,
                         "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                         "Project": i.Project, "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                         "Year": i.Year if i.Year else '',
                         "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                         "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                         "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                         "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                         "Comments": i.Comments if i.Comments else '',
                         "Item": i.Item, "Dalei": i.Dalei,

                         }
                    )
            elif request.POST.get('action') == 'addSubmit':
                ID = request.POST.get('ID')
                updata_dic = {}
                updata_dic['Proposer_Num'] = request.session.get('account')
                # updata_dic['Proposer_NameE'] = request.session.get('user_name')
                PersonalInfos = PersonalInfo.objects.filter(
                    Q(GroupNum=updata_dic['Proposer_Num']) | Q(SAPNum=updata_dic['Proposer_Num'])).first()
                # print(PersonalInfos)
                updata_dic['Project'] = request.POST.get('Project')
                updata_dic['Role'] = request.POST.get('Role')
                updata_dic['Function'] = request.POST.get('Function')
                # NPI&OSR
                if request.POST.get('SubFunction'):
                    updata_dic['SubFunction_Com'] = request.POST.get('SubFunction')
                if request.POST.get('Phase'):
                    updata_dic['Phase'] = request.POST.get('Phase')
                # INV
                if request.POST.get('Month'):
                    updata_dic['Time_Interval'] = request.POST.get('Month')
                if request.POST.get('Year'):
                    updata_dic['Year'] = request.POST.get('Year')
                if PerExperience.objects.exclude(id=ID).filter(**updata_dic) and 'Phase' in updata_dic.keys():
                    errMsgNumber = "您已申请过：Project:%s-Phase:%s-Function:%s-SubFunction:%s-Role:%s" % (
                        updata_dic['Project'], updata_dic['Phase'],
                        updata_dic['Function'], updata_dic['SubFunction_Com'],
                        updata_dic['Role'])
                elif PerExperience.objects.exclude(id=ID).filter(**updata_dic) and 'Phase' not in updata_dic.keys():
                    errMsgNumber = "您已申请过：Project:%s-Phase:%s-Function:%s-SubFunction:%s-Role:%s" % (
                        updata_dic['Project'], updata_dic['Phase'],
                        updata_dic['Function'], updata_dic['SubFunction_Com'],
                        updata_dic['Role'])
                else:
                    # 機種名變更可能隨之變動
                    if 'Phase' in updata_dic.keys():
                        if "OSR" in updata_dic['Phase']:
                            updata_dic['Dalei'] = "OSR"
                        else:
                            updata_dic['Dalei'] = "NPI"
                    else:
                        updata_dic['Dalei'] = "INV"
                    updata_dic['Approved_Officer'] = ProjectinfoinDCT.objects.filter(
                        ComPrjCode=request.POST.get('Project')).first().DQAPLNum
                    updata_dic['SS_Date'] = request.POST.get('SS_Date')
                    # 流程變更
                    updata_dic['Status'] = "待簽核"

                    updata_dic['Comments'] = request.POST.get('Comments')
                    updata_dic['EditTime'] = datetime.datetime.now().strftime("%Y-%m-%d")

                    if updata_dic['Approved_Officer']:
                        PerExperience.objects.filter(id=ID).update(**updata_dic)
                    else:
                        errMsgNumber = "Project:%s DQAPL的工号缺失" % updata_dic['Project']

                for i in PerExperience.objects.filter(Proposer_Num=account_login):
                    tableData.append(
                        {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                            Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                        PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                            SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                         "Status": i.Status, "Department_Code": i.Department_Code,
                         "Proposer_Num": i.Proposer_Num,
                         "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                         "Project": i.Project, "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                         "Year": i.Year if i.Year else '',
                         "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                         "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                         "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                         "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                         "Comments": i.Comments if i.Comments else '',
                         "Item": i.Item, "Dalei": i.Dalei,

                         }
                    )

            else:
                try:
                    request.body
                    # print(request.body)
                except:
                    # print('1')
                    pass
                else:
                    # print('2')
                    if 'Delete' in str(request.body):
                        responseData = json.loads(request.body)
                        for i in responseData['DeleteId']:
                            PerExperience.objects.filter(id=i).delete()

                        for i in PerExperience.objects.filter(Proposer_Num=account_login):
                            tableData.append(
                                {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                                    Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                                PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                                    SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                                 "Status": i.Status, "Department_Code": i.Department_Code,
                                 "Proposer_Num": i.Proposer_Num,
                                 "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                                 "Project": i.Project, "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                                 "Year": i.Year if i.Year else '',
                                 "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                                 "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                                 "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                                 "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                                 "Comments": i.Comments if i.Comments else '',
                                 "Item": i.Item, "Dalei": i.Dalei,

                                 }
                            )
        except Exception as e:
            errMsgNumber = str(e)
        data = {
            "EXPtable": tableData,
            "sectionProject": sectionProject,
            "sectionPhase": sectionPhase,
            "errMsgNumber": errMsgNumber,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/My_application.html', locals())


@csrf_exempt
def My_approve(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/My_approve"

    tableData = [
        # {"id": 1, "Status": "同意", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OOC", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
        # {"id": 2, "Status": "拒絕", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OSR-Win11", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
        # {"id": 3, "Status": "拒絕", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
    ]
    errMsgNumber = ''
    account_login = request.session.get('account')

    if request.method == "POST":
        try:
            if request.POST.get('isGetData') == 'first':
                pass

            else:
                try:
                    request.body
                    # print(request.body)
                except:
                    # print('1')
                    pass
                else:
                    # print('2')
                    if 'ApporveData' in str(request.body):
                        responseData = json.loads(request.body)
                        for i in responseData['ApporveId']:
                            updatedata = PerExperience.objects.filter(id=i).first()
                            updatedata.Status = "同意"
                            updatedata.save()
                    elif 'RefuseData' in str(request.body):
                        responseData = json.loads(request.body)
                        for i in responseData['RefuseId']:
                            updatedata = PerExperience.objects.filter(id=i).first()
                            updatedata.Status = "拒絕"
                            updatedata.save()
            for i in PerExperience.objects.filter(Approved_Officer=account_login, Status='待簽核'):
                tableData.append(
                    {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                        Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                    PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                        SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                     "Status": i.Status, "Department_Code": i.Department_Code,
                     "Proposer_Num": i.Proposer_Num,
                     "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                     "Project": i.Project, "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                     "Year": i.Year if i.Year else '',
                     "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                     "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                     "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                     "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                     "Comments": i.Comments if i.Comments else '',
                     "Item": i.Item, "Dalei": i.Dalei,
                     }
                )



        except Exception as e:
            print(e)
            errMsgNumber = str(e)
        data = {
            "EXPtable": tableData,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/My_approve.html', locals())


@csrf_exempt
def Summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalExperience/Summary"
    err_Msg = ''

    selectProposer = [
        # {"value": "20795434", "number": "張宵凌"}, {"value": "20720831", "number": "劉婭茹"},
    ]
    for i in PerExperience.objects.all().values("Proposer_Num", 'Proposer_Name').distinct():
        selectProposer.append({
            "value": i['Proposer_Num'], "number": i['Proposer_Name']
        })

    selectApprovedOfficer = [
        # {"value": "20795434", "number": "張宵凌"}, {"value": "20720831", "number": "劉婭茹"},
    ]
    for i in PerExperience.objects.all().values("Approved_Officer").distinct():
        selectApprovedOfficer.append({
            "value": i['Approved_Officer'], "number": PersonalInfo.objects.filter(
                Q(GroupNum=i['Approved_Officer']) | Q(SAPNum=i['Approved_Officer'])).first().CNName if
            PersonalInfo.objects.filter(Q(GroupNum=i['Approved_Officer']) | Q(
                SAPNum=i['Approved_Officer'])).first() else "人員信息中未匹配到該工號%s" % i['Approved_Officer']
        })

    sectionProject = [
        # "GLS4I", "FLMA0", "GLS4A"
    ]
    for i in ProjectinfoinDCT.objects.all():
        datastr = i.SS.split(' ')[0].split('/')
        sectionProject.append(i.ComPrjCode)
    # 表格數據
    mock_data = [
        # {"id": 1, "Status": "同意", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OOC", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
        # {"id": 2, "Status": "拒絕", "Department_Code": "KM0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "OSR-Win11", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
        # {"id": 3, "Status": "拒絕", "Department_Code": "KN0MAQAEA0", "Proposer_Num": "715859",
        #  "Proposer_Name": "郭四梅", "Position_Now": "副理", "Project": "GLMS1", "SS_Date": "2023/1/1", "Year": "2023",
        #  "Time_Interval": "上半年", "Phase": "", "Role": "QM", "Function": "Compatibility",
        #  "SubFunction_Com": "Multimedia",
        #  "KeypartNum": 3, "Comments": "",
        #  },
    ]
    err_Msg = ''
    account_login = request.session.get('account')

    canRegister = 0
    roles = []
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=account_login).role.all():
        roles.append(i.name)
    # print(roles)
    for i in roles:
        if 'admin' == i:
            canRegister = 1
    if request.method == "POST":
        try:
            if request.POST.get('isGetData') == 'first':
                for i in PerExperience.objects.filter(Proposer_Num=account_login).exclude(Status__in=["待簽核"]):
                    mock_data.append(
                        {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                            Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                        PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                            SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                         "Status": i.Status, "Department_Code": i.Department_Code,
                         "Proposer_Num": i.Proposer_Num,
                         "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                         "Project": i.Project,
                         "LNVCode": ProjectinfoinDCT.objects.filter(ComPrjCode=i.Project).first().PrjEngCode1,
                         "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                         "Year": i.Year if i.Year else '',
                         "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                         "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                         "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                         "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                         "Comments": i.Comments if i.Comments else '',
                         "Item": i.Item, "Dalei": i.Dalei,

                         }
                    )
            if request.POST.get('isGetData') == 'SEARCH':
                check_dic = {}
                Proposer_Num = request.POST.get('Proposer')
                if Proposer_Num:
                    check_dic["Proposer_Num"] = Proposer_Num
                Approved_Officer = request.POST.get('ApprovedOfficer')
                if Approved_Officer:
                    check_dic["Approved_Officer"] = Approved_Officer
                Project = request.POST.get('Project')
                if Project:
                    check_dic["Project"] = Project
                data_qure = PerExperience.objects.filter(**check_dic).exclude(Status__in=["待簽核"])
                for i in data_qure:
                    mock_data.append(
                        {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                            Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                        PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                            SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                         "Status": i.Status, "Department_Code": i.Department_Code,
                         "Proposer_Num": i.Proposer_Num,
                         "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                         "Project": i.Project,
                         "LNVCode": ProjectinfoinDCT.objects.filter(ComPrjCode=i.Project).first().PrjEngCode1,
                         "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                         "Year": i.Year if i.Year else '',
                         "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                         "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                         "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                         "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                         "Comments": i.Comments if i.Comments else '',
                         "Item": i.Item, "Dalei": i.Dalei,

                         }
                    )
            if request.POST.get('isGetData') == 'register':
                name_role = "DQA_LNV_PerEx_User"
                name_role_CQABO = "DQA_ABO_User"
                name_role_A31 = "DQA_A31_User"
                name_role_A32 = "DQA_A32_User"
                account_Now_list = list(UserInfo.objects.all().values("account").distinct())
                # print(account_Now_list)
                # LNV注册
                for i in PersonalInfo.objects.exclude(status="離職").filter(Status="在職", Customer='C38').values("GroupNum",
                                                                                         "EngName").distinct():
                    if {'account': i["GroupNum"]} in account_Now_list:
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role).first(), )
                    else:
                        createdic = {"account": i["GroupNum"], "password": '12345678',
                                     "username": i["EngName"],
                                     "email": i["EngName"] + '@compal.com' if '.' not in i["EngName"] else
                                     i["EngName"].replace(' ', '').split('.')[1] + '_' +
                                     i["EngName"].replace(' ', '').split('.')[0] + '@compal.com',
                                     "department": 1, "is_active": True, "is_staff": False, "is_SVPuser": False,
                                     }
                        # Role.objects.filter(name=role).first(),
                        # print(createdic)
                        UserInfo.objects.create(**createdic)
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role).first(), )
                # CQ 注册
                for i in PersonalInfo.objects.exclude(status="離職").filter(Status="在職", Customer__in=['CQABO']).values("GroupNum",
                                                                                                 "EngName").distinct():
                    if {'account': i["GroupNum"]} in account_Now_list:
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_CQABO).first(), )
                    else:
                        createdic = {"account": i["GroupNum"], "password": '12345678',
                                     "username": i["EngName"],
                                     "email": i["EngName"] + '@compal.com' if '.' not in i["EngName"] else
                                     i["EngName"].replace(' ', '').split('.')[1] + '_' +
                                     i["EngName"].replace(' ', '').split('.')[0] + '@compal.com',
                                     "department": 1, "is_active": True, "is_staff": False, "is_SVPuser": False,
                                     }
                        # Role.objects.filter(name=role).first(),
                        # print(createdic)
                        UserInfo.objects.create(**createdic)
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_CQABO).first(), )
                # A31 注册
                for i in PersonalInfo.objects.exclude(status="離職").filter(Status="在職", Customer__in=['A31']).values("GroupNum",
                                                                                                 "EngName").distinct():
                    if {'account': i["GroupNum"]} in account_Now_list:
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_CQABO).first(), )
                    else:
                        createdic = {"account": i["GroupNum"], "password": '12345678',
                                     "username": i["EngName"],
                                     "email": i["EngName"] + '@compal.com' if '.' not in i["EngName"] else
                                     i["EngName"].replace(' ', '').split('.')[1] + '_' +
                                     i["EngName"].replace(' ', '').split('.')[0] + '@compal.com',
                                     "department": 1, "is_active": True, "is_staff": False, "is_SVPuser": False,
                                     }
                        # Role.objects.filter(name=role).first(),
                        # print(createdic)
                        UserInfo.objects.create(**createdic)
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_A31).first(), )
                # A31 注册
                for i in PersonalInfo.objects.exclude(status="離職").filter(Status="在職", Customer__in=['A32']).values("GroupNum",
                                                                                               "EngName").distinct():
                    if {'account': i["GroupNum"]} in account_Now_list:
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_CQABO).first(), )
                    else:
                        createdic = {"account": i["GroupNum"], "password": '12345678',
                                     "username": i["EngName"],
                                     "email": i["EngName"] + '@compal.com' if '.' not in i["EngName"] else
                                     i["EngName"].replace(' ', '').split('.')[1] + '_' +
                                     i["EngName"].replace(' ', '').split('.')[0] + '@compal.com',
                                     "department": 1, "is_active": True, "is_staff": False, "is_SVPuser": False,
                                     }
                        # Role.objects.filter(name=role).first(),
                        # print(createdic)
                        UserInfo.objects.create(**createdic)
                        UserInfo.objects.filter(account=i["GroupNum"]).first().role.add(
                            Role.objects.filter(name=name_role_A32).first(), )
                        
                for i in PerExperience.objects.filter(Proposer_Num=account_login):
                    mock_data.append(
                        {"id": i.id, "Approved_Officer": PersonalInfo.objects.filter(
                            Q(GroupNum=i.Approved_Officer) | Q(SAPNum=i.Approved_Officer)).first().CNName if
                        PersonalInfo.objects.filter(Q(GroupNum=i.Approved_Officer) | Q(
                            SAPNum=i.Approved_Officer)).first() else "人員信息中未匹配到該工號%s" % i.Approved_Officer,
                         "Status": i.Status, "Department_Code": i.Department_Code,
                         "Proposer_Num": i.Proposer_Num,
                         "Proposer_Name": i.Proposer_Name, "Position_Now": i.Positions_Name,
                         "Project": i.Project,
                         "LNVCode": ProjectinfoinDCT.objects.filter(ComPrjCode=i.Project).first().PrjEngCode1,
                         "SS_Date": i.SS_Date.strftime("%Y-%m-%d"),
                         "Year": i.Year if i.Year else '',
                         "Time_Interval": i.Time_Interval if i.Time_Interval else '',
                         "Phase": i.Phase if i.Phase else '', "Role": i.Role, "Function": i.Function,
                         "SubFunction_Com": i.SubFunction_Com if i.SubFunction_Com else '',
                         "KeypartNum": int(i.KeypartNum) if i.KeypartNum else '',
                         "Comments": i.Comments if i.Comments else '',
                         "Item": i.Item, "Dalei": i.Dalei,

                         }
                    )
        except Exception as e:
            err_Msg = str(e)
            print(err_Msg)
        data = {
            "content": mock_data,
            "canRegister": canRegister,
            "sectionProject": sectionProject,
            "selectProposer": selectProposer,
            "selectApprovedOfficer": selectApprovedOfficer,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalExperience/Summary.html', locals())
