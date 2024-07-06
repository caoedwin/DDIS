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
from .models import local_identity, Departments, Positions, MajorIfo, Portraits, PersonalInfo, PersonalInfoHisByPer, \
    PersonalInfoHisByYear, MainPower, WorkOvertime, LeaveInfo, PublicAreaM
from django.db.models.functions import ExtractYear


class Reversinator(object):
    def __init__(self, obj):
        self.obj = obj

    def __lt__(self, other):
        return other.obj < self.obj


# Create your views here.
headermodel_Departments = {
    '年份': 'Year', '公司別': 'Companys', '廠區': 'Plants', '處': 'CHU', '部': 'BU', '課': 'KE',
    '客戶別': 'Customer', '部門代碼': 'Department_Code', '管理者': 'Manager',
}
headermodel_Positions = {
    '職等': 'Grade', '項次': 'Item', '國籍': 'Nationality', '職稱代碼': 'Positions_Code', '職稱': 'Positions_Name', '年份': 'Year',
}
headermodel_MajorIfo = {
    '學歷': 'Education', '大類': 'Categories', '學科': 'Subject', '門類': 'category', '專業': 'Major',
    '專業 for 公式查找': 'MajorForExcel',
}
headermodel_PersonalInfo = {
    '狀態': 'Status', '報到日期': 'RegistrationDate', '離職日期': 'QuitDate', '預計離職日期': 'PlanQuitDate', '離職原因': 'QuitReason',
    '離職詳情': 'QuitDetail', '離職去向': 'Whereabouts', '新公司名稱': 'NewCompany', '薪資': 'Aalary', '最近一次績效': 'LastAchievements',
    '客戶': 'Customer', '部門': 'Department', '課別': 'DepartmentCode', '集團員工': 'GroupNum', 'SAP員工': 'SAPNum',
    '中文姓名': 'CNName',
    '英文姓名': 'EngName', '性別': 'Sex', '現職稱': 'PositionNow', '最近一次晉升日期': 'LastPromotionData',
    '入職職稱': 'RegistPosition', '晉升次數': 'PositionTimes', '是否承認工作經驗': 'Experience', '畢業年度': 'GraduationYear',
    '學歷': 'Education', '學校': 'School', '專業': 'Major', '專業歸屬': 'MajorAscription', '英語': 'ENLevel', '身份証號': 'IdCard',
    '籍貫省份': 'NativeProvince', '籍貫地市': 'NativeCity', '籍貫縣市': 'NativeCounty', '戶口省份': 'ResidenceProvince',
    '戶口地市': 'ResidenceCity', '戶口縣市': 'ResidenceCounty', '手機號碼': 'MobileNum',
}
headermodel_MainPower = {
    '年份': 'Year', '公司別': 'Companys', '廠區': 'Plants', '部門代碼': 'DepartmentCode', '處': 'CHU', '部': 'BU', '課': 'KE',
    '客戶別': 'Customer', '項次': 'Item', '職稱': 'Positions_Name', 'CodeNoH01': 'CodeNoH01', 'CodeNoH02': 'CodeNoH02',
    '一月': 'Jan', '二月': 'Feb', '三月': 'Mar', '四月': 'Apr', '五月': 'May', '六月': 'Jun', '七月': 'Jul',
    '八月': 'Aug', '九月': 'Sep', '十月': 'Oct', '十一月': 'Nov', '十二月': 'Dec',
}
headermodel_WorkOvertime = {
    '計薪區間': 'SalaryRange', '部門代號': 'Department_Code', '部門描述': 'Department_Des', '工號': 'GroupNum',
    '姓名': 'CNName', '報到日期': 'RegistDate', '人員性質': 'PerNature', '班別': 'Classes', '年份': 'Year', '月份': 'Mounth',
    '平時加班': 'Peacetime', '國假加班': 'NationalHoliday', '例假加班': 'PeriodHoliday', 'Total': 'Total',
}
headermodel_LeaveInfo = {
    '部門代號': 'Department_Code', '請假人工號': 'GroupNum', '請假人姓名': 'CNName', '年份': 'Year', '月份': 'Mounth',
    '公假': 'PublicHoliday', '工傷假': 'WorkInjury', '事假': 'Matters', '續事假': 'MattersContinuation', '病假': 'Sick',
    '續病假': 'SickContinuation', '婚假': 'Marriage', '喪假': 'Bereavement', '特休假': 'Special',
    '不上班假': 'OffDuty', '補休': 'Compensatory', '防疫假': 'EpidemicPrevention', '無排程假': 'NoScheduling',
    '陪產假': 'PaternityLeave', '曠工': 'Absenteeism', '產假': 'Maternity', '產檢假': 'PregnancyExamination',
    '哺乳假': 'Lactation', '其他': 'Others', '總時數': 'Total',
}


@csrf_exempt
def Infos_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/Infos_upload"
    err_ok = 0  # excel上传1为重复
    err_msg = ''
    result = 0  # 为1 forms 上传重复
    canEdit = 1
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))

    # print(request.POST)
    if request.method == 'POST':
        if request.POST.get("type") == "xlsx":  # 部門代碼
            xlsxlist = request.POST.get('upload')
            Departmentlist = [
                {'Year': '年份',
                 'Department_Code': '部門代碼', }
            ]
            # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
            rownum = 0
            startupload = 0
            for i in simplejson.loads(xlsxlist):
                # print(type(i),i)
                rownum += 1
                modeldata = {}
                for key, value in i.items():
                    modeldata[headermodel_Departments[key]] = value
                if 'Year' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                第"%s"條數據，年份不能爲空
                                    """ % rownum
                    break
                if 'Department_Code' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                第"%s"條數據，部門代碼不能爲空
                                    """ % rownum
                    break
            if startupload:
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        modeldata[headermodel_Departments[key]] = value
                    Check_dic = {"Year": modeldata['Year'],
                                 'Department_Code': modeldata['Department_Code'],
                                 }
                    # print(Check_dic)
                    exsitdata = {}
                    if Departments.objects.filter(
                            **Check_dic).first():  # 已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                        err_ok = 1
                        Departmentlist.append(Check_dic)
                        # print(Departmentlist, err_ok)
                    else:
                        # updatedic = {}
                        # for j in modeldata.keys():
                        #     updatedic[j] = modeldata[j]
                        Departments.objects.create(**modeldata)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': Departmentlist
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if request.POST.get("type") == "xlsx1":  # 職位信息
            xlsxlist = request.POST.get('upload')
            Positionlist = [
                {'Grade': '職等', 'Item': '項次', 'Positions_Code': '職稱代碼', }]
            rownum = 0
            startupload = 0
            # print(simplejson.loads(xlsxlist))
            for i in simplejson.loads(xlsxlist):
                # print(type(i),i)
                rownum += 1
                modeldata = {}
                for key, value in i.items():
                    modeldata[headermodel_Positions[key]] = value
                if 'Grade' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，職等不能爲空
                                                """ % rownum
                    break
                if 'Grade' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，職等不能爲空
                                                """ % rownum
                    break
                if 'Item' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，項次不能爲空
                                                """ % rownum
                    break
                if 'Nationality' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，國籍不能爲空
                                                """ % rownum
                    break
                if 'Positions_Code' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，職稱代碼不能爲空
                                                """ % rownum
                    break
                if 'Positions_Name' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，職稱不能爲空
                                                """ % rownum
                    break
                if 'Year' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，年份不能爲空
                                                """ % rownum
                    break
            if startupload:
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        modeldata[headermodel_Positions[key]] = value
                    Check_dic = {'Grade': modeldata['Grade'], 'Item': modeldata['Item'],
                                 'Positions_Code': modeldata['Positions_Code'], 'Year': modeldata['Year'],
                                 }
                    # print(Check_dic)
                    exsitdata = {}
                    if Positions.objects.filter(
                            **Check_dic).first():  # 已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                        err_ok = 1
                        Positionlist.append(
                            Check_dic)
                        # print(Departmentlist, err_ok)
                    else:
                        # updatedic = {}
                        # for j in modeldata.keys():
                        #     updatedic[j] = modeldata[j]
                        Positions.objects.create(**modeldata)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': Positionlist
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
            pass
        if request.POST.get("type") == "xlsx2":  # 專業信息
            xlsxlist = request.POST.get('upload')
            MajorIfolist = [
                {'Education': '學歷', 'category': '大類',
                 'Major': '專業',
                 # 'MajorForExcel': '專業 for 公式查找', 'Subject': '學科', 'Categories': '門類',
                 }]
            rownum = 0
            startupload = 0
            for i in simplejson.loads(xlsxlist):
                # print(type(i),i)
                rownum += 1
                modeldata = {}
                # print(i)
                for key, value in i.items():
                    modeldata[headermodel_MajorIfo[key]] = value
                if 'Education' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                                        第"%s"條數據，學歷不能爲空
                                                            """ % rownum
                    break
                if 'Categories' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                                        第"%s"條數據，大類不能爲空
                                                            """ % rownum
                    break
                if 'Major' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                                        第"%s"條數據，專業不能爲空
                                                            """ % rownum
                    break
                # if 'MajorForExcel' in modeldata.keys():
                #     startupload = 1
                # else:
                #     # canEdit = 0
                #     startupload = 0
                #     err_ok = 2
                #     err_msg = """
                #                         第"%s"條數據，專業 for 公式查找 不能爲空
                #                                             """ % rownum
                #     break
            if startupload:
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        modeldata[headermodel_MajorIfo[key]] = value
                    Check_dic = {'Education': modeldata['Education'], 'Categories': modeldata['Categories'],
                                 # 'Subject': modeldata['Subject'], 'category': modeldata['category'],
                                 'Major': modeldata['Major'],
                                 # 'MajorForExcel': modeldata['MajorForExcel'],
                                 }
                    if 'Subject' in modeldata.keys():
                        Check_dic['Subject'] = modeldata['Subject']
                    else:
                        Check_dic['Subject'] = ''
                    if 'category' in modeldata.keys():
                        Check_dic['category'] = modeldata['category']
                    else:
                        Check_dic['category'] = ''
                    # print(Check_dic)
                    exsitdata = {}
                    if MajorIfo.objects.filter(
                            **Check_dic).first():  # 已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                        err_ok = 1
                        MajorIfolist.append(
                            Check_dic)
                        # print(Departmentlist, err_ok)
                    else:
                        # updatedic = {}
                        # for j in modeldata.keys():
                        #     updatedic[j] = modeldata[j]
                        MajorIfo.objects.create(**modeldata)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': MajorIfolist
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
            pass
        if request.POST.get("type") == "xlsx3":  # 加班信息
            xlsxlist = request.POST.get('upload')
            WorkOvertimelist = [
                {'Year': '年份', 'Mounth': '月份', 'GroupNum': '工號', }]
            rownum = 0
            startupload = 0
            for i in simplejson.loads(xlsxlist):
                # print(type(i),i)
                rownum += 1
                modeldata = {}
                for key, value in i.items():
                    modeldata[headermodel_WorkOvertime[key]] = value
                if 'GroupNum' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，工號不能爲空
                                                """ % rownum
                    break
                if 'Year' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，年份不能爲空
                                                """ % rownum
                    break
                if 'Mounth' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，月份不能爲空
                                                """ % rownum
                    break
            if startupload:
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        modeldata[headermodel_WorkOvertime[key]] = value
                    Check_dic = {"Year": modeldata['Year'],
                                 'Mounth': modeldata['Mounth'], 'GroupNum': modeldata['GroupNum'],
                                 }
                    # print(Check_dic)
                    exsitdata = {}
                    if WorkOvertime.objects.filter(
                            **Check_dic).first():  # 已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                        err_ok = 1
                        WorkOvertimelist.append(
                            Check_dic)
                        # print(Departmentlist, err_ok)
                    else:
                        # updatedic = {}
                        # for j in modeldata.keys():
                        #     updatedic[j] = modeldata[j]
                        WorkOvertime.objects.create(**modeldata)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': WorkOvertimelist
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
            pass
        if request.POST.get("type") == "xlsx4":  # 請假信息
            xlsxlist = request.POST.get('upload')
            LeaveInfolist = [
                {'Year': '年份', 'Mounth': '月份', 'GroupNum': '工號', }]
            rownum = 0
            startupload = 0
            for i in simplejson.loads(xlsxlist):
                # print(type(i),i)
                rownum += 1
                modeldata = {}
                for key, value in i.items():
                    modeldata[headermodel_LeaveInfo[key]] = value
                if 'GroupNum' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，工號不能爲空
                                                """ % rownum
                    break
                if 'Year' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，年份不能爲空
                                                """ % rownum
                    break
                if 'Mounth' in modeldata.keys():
                    startupload = 1
                else:
                    # canEdit = 0
                    startupload = 0
                    err_ok = 2
                    err_msg = """
                            第"%s"條數據，月份不能爲空
                                                """ % rownum
                    break
            if startupload:
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        modeldata[headermodel_LeaveInfo[key]] = value
                    Check_dic = {"Year": modeldata['Year'],
                                 'Mounth': modeldata['Mounth'], 'GroupNum': modeldata['GroupNum'],
                                 }
                    # print(Check_dic)
                    exsitdata = {}
                    if LeaveInfo.objects.filter(
                            **Check_dic).first():  # 已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                        err_ok = 1
                        LeaveInfolist.append(
                            Check_dic)
                        # print(Departmentlist, err_ok)
                    else:
                        # updatedic = {}
                        # for j in modeldata.keys():
                        #     updatedic[j] = modeldata[j]
                        LeaveInfo.objects.create(**modeldata)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': LeaveInfolist
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
            pass

    return render(request, 'PersonalInfo/Infos_upload.html', locals())


@csrf_exempt
def PersonalInfo_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/PersonalInfo_search"
    customerOptions = {
        # "C38(NB)": [{"Department": "DQA1"},
        #             {"Department": "RD1"},
        #             {"Department": "QA1"},
        #             {"Department": "SA1"}],
        # "C38(AIO)": [{"Department": "DQA2"},
        #              {"Department": "RD2"},
        #              {"Department": "QA2"},
        #              {"Department": "SA2"}],

    }
    lessonOptions = {
        # "一课": [{"GroupEmployees": "Jun"},
        #        {"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}],
        # "二课": [{"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Lux"}],
        # "三课": [{"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}],
        # "四课": [{"GroupEmployees": "Jun"}],
        # "五课": [{"GroupEmployees": "Jun"},
        #        {"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}]
    }
    # 表格數據
    mock_data = [
        # {"id": "1", "Status": "离职", "RegistrationDate": "2014.12.06", "DepartureDate": "2020.12.14",
        #           "ExpectedDepartureDate": "2020.12.14",
        #           "DepartureReasons": "薪资太低", "DepartureDetails": "sdfghjnm", "DepartureTo": "昆山",
        #           "NewCompanyName": "牧田有限公司",
        #           "Salary": "7500/月", "Seniority": "0.5", "Customer": "C38(NB)", "Department": "DQA1", "Lesson": "二课",
        #           "GroupEmployees": "Erin",
        #           "SAPEmployees": "Jun", "ChineseName": "孙俊清", "EnglishName": "Erin", "Gender": "女",
        #           "CurrentTitle": "工程师", "LastPromotionDate": "无",
        #           "EntryTitle": "助工师", "PromotionNumber": "1", "WorkExperience": "是", "GraduationYear": "2019",
        #           "Education": "本科", "School": "江苏大学",
        #           "Profession": "计算机科学与技术", "ProfessionAttribution": "STEM", "English": "六级",
        #           "IdNumber": "320918199604221844",
        #           "Birthday": "1996.04.22", "NativeProvince": "江苏省", "NativeCity": "盐城市", "HukouProvinces": "江苏省",
        #           "HukouCity": "盐城市",
        #           "PhoneNumber": "15203512496"},
    ]
    # 下面是彈出名片的數據
    form = {
        # "SAPEmployees": "5624rtyugytdrse", "ChineseName": "付亞楠", "GroupEmployees": "20709023",
        #     "EnglishName": "Eason_Fu", "Profession": "微電子科學與工程", "School": "池州學院", "CurrentTitle": "技術員",
        #     "Birthday": "1997/05", "NativeProvinceCity": "安徽省合肥市", "RegistrationDate": "2020/11/24",
        #     "Department": "KMOMAQACF0", "Status": "在職",
    }
    tableData = [
        # {"Department": "KMOMAQACF0", "GroupEmployees": "20709023", "ChineseName": "付亞楠", "EntryTitle": "助工師",
        #           "CurrentTitle": "助工師", "PromotionDate": "12/5/2015", "Intervaltime": "", "beizhu": "入職", },
        #          {"Department": "KMOMAQACF0", "GroupEmployees": "20709023", "ChineseName": "付亞楠", "EntryTitle": "助工師",
        #           "CurrentTitle": "工程師", "PromotionDate": "10/26/2017", "Intervaltime": "1.9", "beizhu": "晉升1", },
        #          {"Department": "KMOMAQACF0", "GroupEmployees": "20709023", "ChineseName": "付亞楠", "EntryTitle": "工程師",
        #           "CurrentTitle": "資工師", "PromotionDate": "4/26/2020", "Intervaltime": "2.5", "beizhu": "晉升2", },
    ]
    GroupEmployeesNum = [
        # {"value": "20652552"}, {"value": "12345678"}, {"value": "34567890"}
    ]
    Imageurl = ""  # '/static/images/touxiang.jpg'  # 頭像地址放這裡
    canExport = 0  # 0為DQA權限，可以導出

    onlineuser = request.session.get('account')
    roles = []
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100

    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i:
            canExport = 0
        elif 'Department' in i:
            canExport = 1
    # print(request.method)
    for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
        CustomerDep = []
        for j in PersonalInfo.objects.filter(Customer=i["Customer"]).values("Department").distinct().order_by(
                "Department"):
            CustomerDep.append({"Department": j["Department"]})
        customerOptions[i["Customer"]] = CustomerDep

    for i in PersonalInfo.objects.all().values("GroupNum").distinct().order_by("GroupNum"):
        GroupEmployeesNum.append({"value": i['GroupNum']})

    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            for i in PersonalInfo.objects.all():
                if i.Status == "在職":
                    # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                    # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                    # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                    Seniority = round(
                        float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                else:
                    Seniority = round(
                        float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                Photolist = []
                for h in i.Portrait.all():
                    Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                mock_data.append(
                    {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                     "DepartureDate": str(i.QuitDate),
                     "ExpectedDepartureDate": str(i.PlanQuitDate),
                     "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail, "DepartureTo": i.Whereabouts,
                     "NewCompanyName": i.NewCompany,
                     "Salary": i.Aalary,
                     "Seniority": Seniority,
                     "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                     "GroupEmployees": i.GroupNum,
                     "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName, "Gender": i.Sex,
                     "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                     "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes, "WorkExperience": i.Experience,
                     "GraduationYear": i.GraduationYear,
                     "Education": i.Education, "School": i.School,
                     "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                     "IdNumber": i.IdCard,
                     "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                     "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                     "HukouProvinces": i.ResidenceProvince,
                     "HukouCity": i.ResidenceCounty,
                     "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                )
        if request.POST.get("isGetData") == "JiLian":
            checkjilian = {"Customer": request.POST.get("Customer"),
                           "Department": request.POST.get("Department")}
            for i in PersonalInfo.objects.filter(**checkjilian).values("DepartmentCode").distinct().order_by(
                    "DepartmentCode"):
                GroupNumlist = []
                checkjilian2 = checkjilian
                checkjilian2['DepartmentCode'] = i['DepartmentCode']
                for j in PersonalInfo.objects.filter(**checkjilian2).values("GroupNum").distinct().order_by(
                        "GroupNum"):
                    GroupNumlist.append({"GroupEmployees": j["GroupNum"]})
                lessonOptions[i["DepartmentCode"]] = GroupNumlist
        if request.POST.get("isGetData") == "SEARCH":
            YearSearch = request.POST.get("Year")
            CustomerSearch = request.POST.get("Customer")
            DepartmentSearch = request.POST.get("Department")
            LessonSearch = request.POST.get("Lesson")
            GroupEmployeesSearch = request.POST.get("GroupEmployees")
            YearNow = str(datetime.datetime.now().year)
            checkPerdic = {
                # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                #            "GroupNum": GroupEmployeesSearch,
            }
            if CustomerSearch and CustomerSearch != "All":
                checkPerdic['Customer'] = CustomerSearch
            if DepartmentSearch and DepartmentSearch != "All":
                checkPerdic['Department'] = DepartmentSearch
            if LessonSearch and LessonSearch != "All":
                checkPerdic['DepartmentCode'] = LessonSearch
            if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                checkPerdic['GroupNum'] = GroupEmployeesSearch
            if not YearSearch:
                YearSearch = YearNow
            if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                for i in PersonalInfo.objects.filter(**checkPerdic):
                    if i.Status == "在職":
                        # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                        # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                        # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                        Seniority = round(
                            float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    else:
                        Seniority = round(
                            float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    Photolist = []
                    for h in i.Portrait.all():
                        Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                    mock_data.append(
                        {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                         "DepartureDate": str(i.QuitDate),
                         "ExpectedDepartureDate": str(i.PlanQuitDate),
                         "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                         "DepartureTo": i.Whereabouts,
                         "NewCompanyName": i.NewCompany,
                         "Salary": i.Aalary,
                         "Seniority": Seniority,
                         "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                         "GroupEmployees": i.GroupNum,
                         "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName, "Gender": i.Sex,
                         "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                         "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                         "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                         "Education": i.Education, "School": i.School,
                         "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                         "IdNumber": i.IdCard,
                         "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                         "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                         "HukouProvinces": i.ResidenceProvince,
                         "HukouCity": i.ResidenceCounty,
                         "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                    )
            else:  # 往年的到PersonalInfoHisByYear里面查找
                checkPerdic["Year"] = YearSearch
                for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                    if i.Status == "在職":
                        # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                        # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                        # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                        Seniority = round(
                            float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    else:
                        Seniority = round(
                            float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    Photolist = []
                    for h in i.Portrait.all():
                        Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                    mock_data.append(
                        {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                         "DepartureDate": str(i.QuitDate),
                         "ExpectedDepartureDate": str(i.PlanQuitDate),
                         "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                         "DepartureTo": i.Whereabouts,
                         "NewCompanyName": i.NewCompany,
                         "Salary": i.Aalary,
                         "Seniority": Seniority,
                         "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                         "GroupEmployees": i.GroupNum,
                         "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName, "Gender": i.Sex,
                         "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                         "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                         "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                         "Education": i.Education, "School": i.School,
                         "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                         "IdNumber": i.IdCard,
                         "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                         "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                         "HukouProvinces": i.ResidenceProvince,
                         "HukouCity": i.ResidenceCounty,
                         "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                    )
        if request.POST.get("isGetData") == "selectDetail":
            YearSearch = request.POST.get("Year")
            YearNow = str(datetime.datetime.now().year)
            if not YearSearch:
                YearSearch = YearNow
            GroupNumSearch = request.POST.get(
                "GroupEmployees")  # 不管是PersonalInfo還是PersonalInfoHisByYear裏面的數據，都用工號到PersonalInfo裏面搜索，因爲晉升記錄鏈接的他，并且頭像都是一樣的
            if not YearSearch or YearSearch == YearNow:
                registinfo = PersonalInfo.objects.get(GroupNum=GroupNumSearch)
            else:
                registinfo = PersonalInfoHisByYear.objects.get(GroupNum=GroupNumSearch, Year=YearSearch)
            # print(Positions.objects.filter(Positions_Code=registinfo.PositionNow).first(),registinfo.PositionNow)
            if Positions.objects.filter(Item=registinfo.PositionNow, Year=YearSearch).first():
                CurrentTitle = Positions.objects.filter(Item=registinfo.PositionNow,
                                                        Year=YearSearch).first().Positions_Name
            else:
                CurrentTitle = "該項次沒有對應的職稱名"
            if Positions.objects.filter(Item=registinfo.PositionNow, Year=YearSearch).first():
                EntryTitle = Positions.objects.filter(Item=registinfo.PositionNow,
                                                      Year=YearSearch).first().Positions_Name
            else:
                EntryTitle = "該項次沒有對應的職稱名"

            form = {
                "SAPEmployees": registinfo.SAPNum, "ChineseName": registinfo.CNName, "GroupEmployees": GroupNumSearch,
                "EnglishName": registinfo.EngName, "Profession": registinfo.Major, "School": registinfo.School,
                "Education": registinfo.Education, "CurrentTitle": CurrentTitle,
                "Birthday": registinfo.IdCard[6:10] + "-" + registinfo.IdCard[10:12] + "-" + registinfo.IdCard[12:14],
                "NativeProvinceCity": registinfo.NativeProvince + registinfo.NativeCounty,
                "RegistrationDate": str(registinfo.RegistrationDate) if registinfo.RegistrationDate else '',
                "Department": registinfo.DepartmentCode, "Status": registinfo.Status,
                "ExpectedDepartureDate": str(registinfo.QuitDate) if registinfo.QuitDate else '',
            }
            # print(form)
            for h in registinfo.Portrait.all():
                Imageurl = '/media/' + h.img.name
            tableData.append(
                {"Department": registinfo.DepartmentCode, "GroupEmployees": registinfo.GroupNum,
                 "ChineseName": registinfo.CNName, "EntryTitle": EntryTitle,
                 "CurrentTitle": CurrentTitle, "PromotionDate": str(registinfo.RegistrationDate), "Intervaltime": "",
                 "beizhu": "入職", }
            )
            num = 0
            LastLastPromotionData = registinfo.RegistrationDate
            for i in PersonalInfoHisByPer.objects.filter(GroupNum=GroupNumSearch).values("DepartmentCode", "CNName",
                                                                                         "PositionOld", "PositionNow",
                                                                                         "LastPromotionData").order_by(
                "LastPromotionData"):
                num += 1
                print(i)
                tableData.append(
                    {"Department": i["DepartmentCode"], "GroupEmployees": GroupNumSearch,
                     "ChineseName": i["CNName"], "EntryTitle": i["PositionOld"],
                     "CurrentTitle": i["PositionNow"], "PromotionDate": str(i["LastPromotionData"]),
                     "Intervaltime": round(
                         float(str((i["LastPromotionData"] - LastLastPromotionData)).split(' ')[0]) / 365, 1) if i[
                         "LastPromotionData"] else "缺少晋升日期",
                     "beizhu": "晉升%s" % num, }
                )
                LastLastPromotionData = i["LastPromotionData"]

        data = {
            "err_ok": "0",
            "GroupEmployeesNum": GroupEmployeesNum,
            "select": customerOptions,
            "lessonOptions": lessonOptions,
            "content": mock_data,
            "form": form,
            "tableData": tableData,
            "Imageurl": Imageurl,
            "canExport": canExport

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/PersonalInfo_search.html', locals())


@csrf_exempt
def PersonalInfo_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/PersonalInfo_edit"
    GroupEmployeesNum = [
        # {"value": "20652552"}, {"value": "12345678"}, {"value": "34567890"}
    ]
    customerOptions = {
        # "C38(NB)": [{"Department": "DQA1"},
        #             {"Department": "RD1"},
        #             {"Department": "QA1"},
        #             {"Department": "SA1"}],
        # "C38(AIO)": [{"Department": "DQA2"},
        #              {"Department": "RD2"},
        #              {"Department": "QA2"},
        #              {"Department": "SA2"}],
        # "A39": [{"Department": "DQA3"},
        #         {"Department": "RD3"},
        #         {"Department": "QA3"},
        #         {"Department": "SA3"}],
        # "T88(AIO)": [{"Department": "DQA4"},
        #              {"Department": "RD4"},
        #              {"Department": "QA4"},
        #              {"Department": "SA4"}],
        # "Other": [{"Department": "DQA5"},
        #           {"Department": "RD5"},
        #           {"Department": "QA5"},
        #           {"Department": "SA5"}]
    }
    lessonOptions = {
        # "一课": [{"GroupEmployees": "Jun"},
        #        {"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}],
        # "二课": [{"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Lux"}],
        # "三课": [{"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}],
        # "四课": [{"GroupEmployees": "Jun"}],
        # "五课": [{"GroupEmployees": "Jun"},
        #        {"GroupEmployees": "Erin"},
        #        {"GroupEmployees": "Edwin"},
        #        {"GroupEmployees": "Lux"}]
    }
    mock_data = [
        # {"id": "1", "Status": "离职", "RegistrationDate": "2014.12.06", "DepartureDate": "2020.12.14",
        #           "ExpectedDepartureDate": "2020.12.14",
        #           "DepartureReasons": "薪资太低", "DepartureDetails": "sdfghjnm", "DepartureTo": "昆山",
        #           "NewCompanyName": "牧田有限公司",
        #           "Salary": "7500/月", "Seniority": "0.5", "Customer": "C38(NB)", "Department": "DQA1", "Lesson": "二课",
        #           "GroupEmployees": "Erin",
        #           "SAPEmployees": "Jun", "ChineseName": "孙俊清", "EnglishName": "Erin", "Gender": "女",
        #           "CurrentTitle": "工程师", "LastPromotionDate": "无",
        #           "EntryTitle": "助工师", "PromotionNumber": "1", "WorkExperience": "是", "GraduationYear": "2019",
        #           "Education": "本科", "School": "江苏大学",
        #           "Profession": "计算机科学与技术", "ProfessionAttribution": "STEM", "English": "六级",
        #           "IdNumber": "320918199604221844",
        #           "Birthday": "1996.04.22", "NativeProvince": "江苏省", "NativeCity": "盐城市", "HukouProvinces": "江苏省",
        #           "HukouCity": "盐城市",
        #           "PhoneNumber": "15203512496"},
    ]
    Customeroptions1 = [
        # 'C38(NB)', 'C38(AIO)', 'A39', 'T88(AIO)'
    ]
    Departmentoptions1 = [
        # 'DQA5', 'RD', 'QA', 'SA'
    ]
    Lessonoptions1 = [
        # '一课', '二课', '三课', '四课'
    ]
    Titleoptions1 = [
        # '助工師', '工程師', '資工師', '副課長', '課長'
    ]
    ProfessionAttributionoptions1 = [
        # {‘value': 数学类'}
    ]
    err_msg = ''
    form = {}
    fileListO = []
    permission = 100  # 助理编辑权限为1（所有信息皆可编辑），课长级编辑权限为2（只能编辑离职信息）
    roles = []
    onlineuser = request.session.get('account')
    # onlineuser = '0502413'
    onlineuserDepartment = ''
    # print(onlineuser,UserInfo.objects.get(account=onlineuser))
    if Departments.objects.filter(Manager=onlineuser):
        permission = 2
        onlineuserDepartment = Departments.objects.filter(Manager=onlineuser).first().Department_Code
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i:
            permission = 1
        elif 'Department' in i:
            permission = 3
    # print(request.method)
    for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
        CustomerDep = []
        for j in PersonalInfo.objects.filter(Customer=i["Customer"]).values("Department").distinct().order_by(
                "Department"):
            CustomerDep.append({"Department": j["Department"]})
        customerOptions[i["Customer"]] = CustomerDep
    for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
        Customeroptions1.append(i['Customer'])
    for i in PersonalInfo.objects.all().values("Department").distinct().order_by("Department"):
        Departmentoptions1.append(i['Department'])
    for i in PersonalInfo.objects.all().values("DepartmentCode").distinct().order_by("DepartmentCode"):
        Lessonoptions1.append(i['DepartmentCode'])
    for i in PersonalInfo.objects.all().values("GroupNum").distinct().order_by("GroupNum"):
        GroupEmployeesNum.append({"value": i['GroupNum']})
    YearNow = str(datetime.datetime.now().year)
    # print(Positions.objects.filter(Year=YearSearch).values("Item").distinct())
    for i in Positions.objects.filter(Year=YearNow).values("Item").distinct().order_by("Item"):
        Titleoptions1.append(i["Item"])
    for i in MajorIfo.objects.all().values("MajorForExcel").distinct().order_by("MajorForExcel"):
        ProfessionAttributionoptions1.append({'value': i['MajorForExcel']})

    # print(request.method)
    # print(request.POST)
    # print(request.body)
    if request.method == 'POST':
        if request.POST:
            if request.POST.get("isGetData") == "first":
                for i in PersonalInfo.objects.all():
                    if i.Status == "在職":
                        # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                        # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                        # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                        Seniority = round(
                            float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    else:
                        Seniority = round(
                            float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                    Photolist = []
                    for h in i.Portrait.all():
                        Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                    mock_data.append(
                        {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                         "DepartureDate": str(i.QuitDate),
                         "ExpectedDepartureDate": str(i.PlanQuitDate),
                         "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                         "DepartureTo": i.Whereabouts,
                         "NewCompanyName": i.NewCompany,
                         "Salary": i.Aalary,
                         "Seniority": Seniority,
                         "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                         "GroupEmployees": i.GroupNum,
                         "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName, "Gender": i.Sex,
                         "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                         "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                         "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                         "Education": i.Education, "School": i.School,
                         "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                         "IdNumber": i.IdCard,
                         "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                         "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                         "HukouProvinces": i.ResidenceProvince,
                         "HukouCity": i.ResidenceCounty,
                         "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                    )
            if request.POST.get("isGetData") == "JiLian":
                checkjilian = {"Customer": request.POST.get("Customer"),
                               "Department": request.POST.get("Department")}
                for i in PersonalInfo.objects.filter(**checkjilian).values("DepartmentCode").distinct().order_by(
                        "DepartmentCode"):
                    GroupNumlist = []
                    checkjilian2 = checkjilian
                    checkjilian2['DepartmentCode'] = i['DepartmentCode']
                    for j in PersonalInfo.objects.filter(**checkjilian2).values("GroupNum").distinct().order_by(
                            "GroupNum"):
                        GroupNumlist.append({"GroupEmployees": j["GroupNum"]})
                    lessonOptions[i["DepartmentCode"]] = GroupNumlist
                # 更具年份變更職位信息列表
                YearSearch = request.POST.get("Year")
                YearNow = str(datetime.datetime.now().year)
                if not YearSearch:
                    YearSearch = YearNow
                Titleoptions1 = []
                # print(Positions.objects.filter(Year=YearSearch).values("Item").distinct())
                for i in Positions.objects.filter(Year=YearSearch).values("Item").distinct().order_by("Item"):
                    Titleoptions1.append(i["Item"])
            if request.POST.get("isGetData") == "SEARCH":
                YearSearch = request.POST.get("Year")
                CustomerSearch = request.POST.get("Customer")
                DepartmentSearch = request.POST.get("Department")
                LessonSearch = request.POST.get("Lesson")
                GroupEmployeesSearch = request.POST.get("GroupEmployees")
                YearNow = str(datetime.datetime.now().year)
                checkPerdic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if CustomerSearch and CustomerSearch != "All":
                    checkPerdic['Customer'] = CustomerSearch
                if DepartmentSearch and DepartmentSearch != "All":
                    checkPerdic['Department'] = DepartmentSearch
                if LessonSearch and LessonSearch != "All":
                    checkPerdic['DepartmentCode'] = LessonSearch
                if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                    checkPerdic['GroupNum'] = GroupEmployeesSearch
                if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                    for i in PersonalInfo.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(
                                float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
                else:  # 往年的到PersonalInfoHisByYear里面查找
                    checkPerdic["Year"] = YearSearch
                    for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(
                                float(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription, "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
                if not YearSearch:
                    YearSearch = YearNow
                Titleoptions1 = []
                # print(YearSearch,Positions.objects.filter(Year=YearSearch).values("Item").distinct().order_by("Item"))
                for i in Positions.objects.filter(Year=YearSearch).values("Item").distinct().order_by("Item"):
                    Titleoptions1.append(i["Item"])
            if request.POST.get("action") == "submit":
                # 虽然与新增用的同一个form，但是编辑时需要先赋值默认值，复制后为空的数据就不是空字符串了。
                YearSearch = request.POST.get("searchYear")
                if YearSearch == "null":
                    YearSearch = ''
                CustomerSearch = request.POST.get("searchCustomer")
                if CustomerSearch == "null":
                    CustomerSearch = ''
                DepartmentSearch = request.POST.get("searchDepartment")
                if DepartmentSearch == "null":
                    DepartmentSearch = ''
                LessonSearch = request.POST.get("searchLesson")
                if LessonSearch == "null":
                    LessonSearch = ''
                GroupEmployeesSearch = request.POST.get("searchGroupEmployees")
                if GroupEmployeesSearch == "null":
                    GroupEmployeesSearch = ''
                YearNow = str(datetime.datetime.now().year)

                id = request.POST.get("id")
                Photolist = request.FILES.getlist("fileList", "")
                Status = request.POST.get("Status")
                RegistrationDate = request.POST.get("RegistrationDate")
                if RegistrationDate == "NaN-NaN-NaN" or RegistrationDate == "null" or RegistrationDate == "":
                    RegistrationDate = None
                # print(type(RegistrationDate))
                QuitDate = request.POST.get("DepartureDate")
                if QuitDate == "NaN-NaN-NaN" or QuitDate == "null" or QuitDate == "":
                    QuitDate = None
                PlanQuitDate = request.POST.get("ExpectedDepartureDate")
                if PlanQuitDate == "NaN-NaN-NaN" or PlanQuitDate == "null" or PlanQuitDate == "":
                    PlanQuitDate = None
                # print(PlanQuitDate,type(PlanQuitDate))
                QuitReason = request.POST.get("DepartureReasons")
                if QuitReason == "null":
                    QuitReason = ''
                # print(QuitReason, type(QuitReason))
                QuitDetail = request.POST.get("DepartureDetails")
                if QuitDetail == "null":
                    QuitDetail = ''
                Whereabouts = request.POST.get("DepartureTo")
                if Whereabouts == "null":
                    Whereabouts = ''
                NewCompany = request.POST.get("NewCompanyName")
                if NewCompany == "null":
                    NewCompany = ''
                Aalary = request.POST.get("Salary")
                if Aalary == "null":
                    Aalary = ''
                Customer = request.POST.get("Customer")
                Department = request.POST.get("Department")
                DepartmentCode = request.POST.get("Lesson")
                GroupNum = request.POST.get("GroupEmployees")
                SAPNum = request.POST.get("SAPEmployees")
                CNName = request.POST.get("ChineseName")
                EngName = request.POST.get("EnglishName")
                Sex = request.POST.get("Gender")
                PositionNow = request.POST.get("CurrentTitle")
                LastPromotionData = request.POST.get("LastPromotionDate")
                if LastPromotionData == "NaN-NaN-NaN" or LastPromotionData == "null" or LastPromotionData == "":
                    LastPromotionData = None
                # print(type(LastPromotionData))
                RegistPosition = request.POST.get("EntryTitle")
                PositionTimes = request.POST.get("PromotionNumber")
                Experience = request.POST.get("WorkExperience")
                GraduationYear = request.POST.get("GraduationYear")
                Education = request.POST.get("Education")
                School = request.POST.get("School")
                Major = request.POST.get("Profession")
                MajorAscription = request.POST.get("ProfessionAttribution")
                ENLevel = request.POST.get("English")
                IdCard = request.POST.get("IdNumber")
                NativeProvince = request.POST.get("NativeProvince")
                NativeCounty = request.POST.get("NativeCity")
                ResidenceProvince = request.POST.get("HukouProvinces")
                ResidenceCounty = request.POST.get("HukouCity")
                MobileNum = request.POST.get("PhoneNumber")
                updatadivPer = {"Status": Status, "RegistrationDate": RegistrationDate, "QuitDate": QuitDate,
                                "PlanQuitDate": PlanQuitDate,
                                "QuitReason": QuitReason, "QuitDetail": QuitDetail, "Whereabouts": Whereabouts,
                                "NewCompany": NewCompany,
                                "Aalary": Aalary, "Customer": Customer, "Department": Department,
                                "DepartmentCode": DepartmentCode,
                                "GroupNum": GroupNum, "SAPNum": SAPNum, "CNName": CNName, "EngName": EngName,
                                "Sex": Sex, "PositionNow": PositionNow, "LastPromotionData": LastPromotionData,
                                "RegistPosition": RegistPosition,
                                "PositionTimes": PositionTimes, "Experience": Experience,
                                "GraduationYear": GraduationYear, "Education": Education,
                                "School": School, "Major": Major, "MajorAscription": MajorAscription,
                                "ENLevel": ENLevel,
                                "IdCard": IdCard, "NativeProvince": NativeProvince, "NativeCounty": NativeCounty,
                                "ResidenceProvince": ResidenceProvince,
                                "ResidenceCounty": ResidenceCounty, "MobileNum": MobileNum, }
                # print(updatadivPer)
                # print(YearSearch,YearNow)
                if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面修改,年份为空默认修改当年数据,并且职位发生变化时存到PersonalInfoHisByPer
                    if PersonalInfo.objects.filter(id=id).first():
                        # print('1')
                        Percheck1 = PersonalInfo.objects.filter(id=id).first()
                        if Percheck1.PositionNow != PositionNow and Status == "在職":  # 职位信息变化，先存晋升记录再覆盖
                            PersonalInfoHisByPerCreate = {"Personallink": Percheck1,
                                                          "ChangeType": "1", "Department": Department,
                                                          "DepartmentCode": DepartmentCode,
                                                          "DepartmentCodeYear": '', "GroupNum": GroupNum,
                                                          "SAPNum": SAPNum,
                                                          "CNName": CNName,
                                                          "EngName": EngName, "Sex": Sex,
                                                          "PositionNow": PositionNow,
                                                          "PositionOld": Percheck1.PositionNow,
                                                          "LastPromotionData": LastPromotionData,
                                                          "Editor": request.session.get('user_name'),
                                                          "EditTime": datetime.datetime.now().strftime(
                                                              "%Y-%m-%d %H:%M:%S"), }
                            PersonalInfoHisByPer.objects.create(**PersonalInfoHisByPerCreate)

                            PersonalInfo.objects.filter(id=id).update(**updatadivPer)
                            if Photolist:
                                for m in PersonalInfo.objects.filter(
                                        id=id).first().Portrait.all():  # 每次接受图片前清除原来的图片，而不是叠加
                                    # print(m.id)
                                    Portraits.objects.filter(
                                        id=m.id).delete()  # 无需先将子表里面相关联的数据都删除（或者断开关联），才能删除母表的图片（并且物理路径下的文件也被删除了），应该是model里面加了mymodel_delete的原因
                                for f in Photolist:  # 数据上允许传多张照片，实际生产环境中头像只会传一张
                                    # print(f)
                                    empt = Portraits()
                                    # 增加其他字段应分别对应填写
                                    empt.single = f
                                    empt.img = f
                                    empt.save()
                                    PersonalInfo.objects.filter(id=id).first().Portrait.add(empt)
                                    # 将往年的数据里面的头像自动更新，往年有多个数据，将所有这个功能工号的数据都更新
                                    for Person in PersonalInfoHisByYear.objects.filter(
                                            GroupNum=PersonalInfo.objects.filter(id=id).first().GroupNum):
                                        Person.Portrait.add(empt)
                            else:  # 如果没传头像，看看原来同工号的其他数据有没有头像，如果有，更新到本条数据中
                                for Person in PersonalInfoHisByYear.objects.filter(
                                        GroupNum=PersonalInfo.objects.filter(id=id).first().GroupNum):
                                    if Person.Portrait.all():
                                        for photos in Person.Portrait.all():
                                            PersonalInfo.objects.filter(id=id).first().Portrait.add(photos.id)
                                        break

                        else:
                            # print('2')
                            PersonalInfo.objects.filter(id=id).update(**updatadivPer)
                            if Photolist:
                                for m in PersonalInfo.objects.filter(
                                        id=id).first().Portrait.all():  # 每次接受图片前清除原来的图片，而不是叠加
                                    # print(m.id)
                                    Portraits.objects.filter(
                                        id=m.id).delete()  # 无需先将子表里面相关联的数据都删除（或者断开关联），才能删除母表的图片（并且物理路径下的文件也被删除了），应该是model里面加了mymodel_delete的原因
                                for f in Photolist:  # 数据上允许传多张照片，实际生产环境中头像只会传一张
                                    # print(f)
                                    empt = Portraits()
                                    # 增加其他字段应分别对应填写
                                    empt.single = f
                                    empt.img = f
                                    empt.save()
                                    PersonalInfo.objects.filter(id=id).first().Portrait.add(empt)
                                    # 将往年的数据里面的头像自动更新，往年有多个数据，将所有这个功能工号的数据都更新
                                    for Person in PersonalInfoHisByYear.objects.filter(
                                            GroupNum=PersonalInfo.objects.filter(id=id).first().GroupNum):
                                        # print(Person)
                                        Person.Portrait.add(empt)
                            else:  # 如果没传头像，看看原来同工号的其他数据有没有头像，如果有，更新到本条数据中
                                for Person in PersonalInfoHisByYear.objects.filter(
                                        GroupNum=PersonalInfo.objects.filter(id=id).first().GroupNum):
                                    if Person.Portrait.all():
                                        for photos in Person.Portrait.all():
                                            PersonalInfo.objects.filter(id=id).first().Portrait.add(photos.id)
                                        break

                else:  # 往年的到PersonalInfoHisByYear里面修改
                    # print('3')
                    PersonalInfoHisByYear.objects.filter(id=id).update(**updatadivPer)
                    if Photolist:
                        for m in PersonalInfoHisByYear.objects.filter(
                                id=id).first().Portrait.all():  # 每次接受图片前清除原来的图片，而不是叠加
                            # print(m.id)
                            Portraits.objects.filter(
                                id=m.id).delete()  # 无需先将子表里面相关联的数据都删除（或者断开关联），才能删除母表的图片（并且物理路径下的文件也被删除了），应该是model里面加了mymodel_delete的原因
                        for f in Photolist:
                            # print(f)
                            empt = Portraits()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.img = f
                            empt.save()
                            PersonalInfoHisByYear.objects.filter(id=id).first().Portrait.add(empt)
                            # 将往年的其他数据里面的头像自动更新，往年的数据同一个工号有多个，不能只更新编辑的这个
                            for Person in PersonalInfoHisByYear.objects.filter(
                                    GroupNum=PersonalInfoHisByYear.objects.filter(id=id).first().GroupNum):
                                # print(Person)
                                Person.Portrait.add(empt)
                            # 将当年的数据里面的头像自动更新，当年同意个工号只有一个数据
                            PersonalInfo.objects.filter(
                                GroupNum=PersonalInfoHisByYear.objects.filter(
                                    id=id).first().GroupNum).first().Portrait.add(empt)
                    else:  # 如果没传头像，看看原来同工号的其他数据有没有头像，如果有，更新到本条数据中
                        for Person in PersonalInfoHisByYear.objects.filter(
                                GroupNum=PersonalInfoHisByYear.objects.filter(id=id).first().GroupNum):
                            if Person.Portrait.all():
                                for photos in Person.Portrait.all():
                                    PersonalInfoHisByYear.objects.filter(id=id).first().Portrait.add(photos.id)
                                break
                        if PersonalInfo.objects.filter(
                                GroupNum=PersonalInfoHisByYear.objects.filter(
                                    id=id).first().GroupNum).first().Portrait.all():
                            for photos in PersonalInfo.objects.filter(
                                    GroupNum=PersonalInfoHisByYear.objects.filter(
                                        id=id).first().GroupNum).first().Portrait.all():
                                PersonalInfoHisByYear.objects.filter(id=id).first().Portrait.add(photos.id)

                checkPerdic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if CustomerSearch and CustomerSearch != "All":
                    checkPerdic['Customer'] = CustomerSearch
                if DepartmentSearch and DepartmentSearch != "All":
                    checkPerdic['Department'] = DepartmentSearch
                if LessonSearch and LessonSearch != "All":
                    checkPerdic['DepartmentCode'] = LessonSearch
                if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                    checkPerdic['GroupNum'] = GroupEmployeesSearch
                if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                    for i in PersonalInfo.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(float(
                                str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                             "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
                else:  # 往年的到PersonalInfoHisByYear里面查找
                    checkPerdic["Year"] = YearSearch
                    for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(
                                float(
                                    str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                             "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
            if request.POST.get("action") == "onAppend":
                YearSearch = request.POST.get("searchYear")
                CustomerSearch = request.POST.get("searchCustomer")
                DepartmentSearch = request.POST.get("searchDepartment")
                LessonSearch = request.POST.get("searchLesson")
                GroupEmployeesSearch = request.POST.get("searchGroupEmployees")
                YearNow = str(datetime.datetime.now().year)

                # id = request.POST.get("id")
                Photolist = request.FILES.getlist("fileList", "")
                Status = request.POST.get("Status")
                RegistrationDate = request.POST.get("RegistrationDate")
                if RegistrationDate == "NaN-NaN-NaN" or RegistrationDate == "null" or RegistrationDate == "" or RegistrationDate == "undefined":
                    RegistrationDate = None
                # print(type(RegistrationDate))
                QuitDate = request.POST.get("DepartureDate")
                if QuitDate == "NaN-NaN-NaN" or QuitDate == "null" or QuitDate == "" or QuitDate == "undefined":
                    QuitDate = None
                PlanQuitDate = request.POST.get("ExpectedDepartureDate")
                if PlanQuitDate == "NaN-NaN-NaN" or PlanQuitDate == "null" or PlanQuitDate == "" or PlanQuitDate == "undefined":
                    PlanQuitDate = None
                # print(PlanQuitDate,type(PlanQuitDate))
                QuitReason = request.POST.get("DepartureReasons")
                if QuitReason == "null" or QuitReason == "undefined":
                    QuitReason = ''
                # print(QuitReason, type(QuitReason))
                QuitDetail = request.POST.get("DepartureDetails")
                if QuitDetail == "null" or QuitDetail == "undefined":
                    QuitDetail = ''
                Whereabouts = request.POST.get("DepartureTo")
                if Whereabouts == "null" or Whereabouts == "undefined":
                    Whereabouts = ''
                NewCompany = request.POST.get("NewCompanyName")
                if NewCompany == "null" or NewCompany == "undefined":
                    NewCompany = ''
                Aalary = request.POST.get("Salary")
                if Aalary == "null" or Aalary == "undefined":
                    Aalary = ''
                Customer = request.POST.get("Customer")
                Department = request.POST.get("Department")
                DepartmentCode = request.POST.get("Lesson")
                GroupNum = request.POST.get("GroupEmployees")
                SAPNum = request.POST.get("SAPEmployees")
                CNName = request.POST.get("ChineseName")
                EngName = request.POST.get("EnglishName")
                Sex = request.POST.get("Gender")
                PositionNow = request.POST.get("CurrentTitle")
                LastPromotionData = request.POST.get("LastPromotionDate")
                if LastPromotionData == "NaN-NaN-NaN" or LastPromotionData == "null" or LastPromotionData == "" or LastPromotionData == "undefined":
                    LastPromotionData = None
                # print(type(LastPromotionData))
                RegistPosition = request.POST.get("EntryTitle")
                PositionTimes = request.POST.get("PromotionNumber")
                Experience = request.POST.get("WorkExperience")
                GraduationYear = request.POST.get("GraduationYear")
                Education = request.POST.get("Education")
                School = request.POST.get("School")
                Major = request.POST.get("Profession")
                MajorAscription = request.POST.get("ProfessionAttribution")
                ENLevel = request.POST.get("English")
                IdCard = request.POST.get("IdNumber")
                NativeProvince = request.POST.get("NativeProvince")
                NativeCounty = request.POST.get("NativeCity")
                ResidenceProvince = request.POST.get("HukouProvinces")
                ResidenceCounty = request.POST.get("HukouCity")
                MobileNum = request.POST.get("PhoneNumber")
                updatadivPer = {"Status": Status, "RegistrationDate": RegistrationDate, "QuitDate": QuitDate,
                                "PlanQuitDate": PlanQuitDate,
                                "QuitReason": QuitReason, "QuitDetail": QuitDetail, "Whereabouts": Whereabouts,
                                "NewCompany": NewCompany,
                                "Aalary": Aalary, "Customer": Customer, "Department": Department,
                                "DepartmentCode": DepartmentCode,
                                "GroupNum": GroupNum, "SAPNum": SAPNum, "CNName": CNName, "EngName": EngName,
                                "Sex": Sex, "PositionNow": PositionNow, "LastPromotionData": LastPromotionData,
                                "RegistPosition": RegistPosition,
                                "PositionTimes": PositionTimes, "Experience": Experience,
                                "GraduationYear": GraduationYear, "Education": Education,
                                "School": School, "Major": Major, "MajorAscription": MajorAscription,
                                "ENLevel": ENLevel,
                                "IdCard": IdCard, "NativeProvince": NativeProvince, "NativeCounty": NativeCounty,
                                "ResidenceProvince": ResidenceProvince,
                                "ResidenceCounty": ResidenceCounty, "MobileNum": MobileNum, }
                # print(YearSearch)
                if not YearSearch or YearSearch == YearNow:  # 当年的添加到PersonalInfo里面,年份为空默认修改当年数据
                    print('1')
                    if not PersonalInfo.objects.filter(GroupNum=GroupNum):  # 没有同一工号的数据才添加，否则不添加
                        print(updatadivPer)
                        PersonalInfo.objects.create(**updatadivPer)
                        if Photolist:
                            if PersonalInfoHisByYear.objects.filter(
                                    GroupNum=GroupNum).first():
                                for m in PersonalInfoHisByYear.objects.filter(
                                        GroupNum=GroupNum).first().Portrait.all():  # 每次接受图片前清除原来的图片（如果该工号存在与往年数据中），而不是叠加。由于可以之际而删除母表图片，所以不需要遍历往年的所有同一工号的数据，理论上是指向同一母表图片的
                                    # print(m.id)
                                    Portraits.objects.filter(
                                        id=m.id).delete()  # 无需先将子表里面相关联的数据都删除（或者断开关联），才能删除母表的图片（并且物理路径下的文件也被删除了），应该是model里面加了mymodel_delete的原因
                            for f in Photolist:  # 数据上允许传多张照片，实际生产环境中头像只会传一张
                                # print(f)
                                empt = Portraits()
                                # 增加其他字段应分别对应填写
                                empt.single = f
                                empt.img = f
                                empt.save()
                                PersonalInfo.objects.filter(GroupNum=GroupNum).first().Portrait.add(empt)
                                # 将往年的数据里面的头像自动更新，往年有多个数据，将所有这个功能工号的数据都更新
                                for Person in PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum):
                                    # print(Person)
                                    Person.Portrait.add(empt)
                        else:  # 如果没传头像，看看原来同工号的其他数据有没有头像，如果有，更新到本条数据中
                            for Person in PersonalInfoHisByYear.objects.filter(
                                    GroupNum=PersonalInfo.objects.filter(GroupNum=GroupNum).first().GroupNum):
                                if Person.Portrait.all():
                                    for photos in Person.Portrait.all():
                                        PersonalInfo.objects.filter(GroupNum=GroupNum).first().Portrait.add(photos.id)
                                    break

                else:  # 往年的到PersonalInfoHisByYear里面修改
                    # print('3')
                    if not PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum,
                                                                Year=YearSearch):  # 没有同一工号同一年份的数据才添加，否则不添加
                        updatadivPer['Year'] = YearSearch
                        PersonalInfoHisByYear.objects.create(**updatadivPer)
                        if Photolist:
                            for list in PersonalInfoHisByYear.objects.filter(
                                    GroupNum=GroupNum):  # 防止新增加的数据刚好是PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum).first()
                                if list.Portrait.all():
                                    for m in list.Portrait.all():  # 每次接受图片前清除原来的图片，而不是叠加
                                        # print(m.id)
                                        Portraits.objects.filter(
                                            id=m.id).delete()  # 无需先将子表里面相关联的数据都删除（或者断开关联），才能删除母表的图片（并且物理路径下的文件也被删除了），应该是model里面加了mymodel_delete的原因
                                    break
                            for f in Photolist:
                                # print(f)
                                empt = Portraits()
                                # 增加其他字段应分别对应填写
                                empt.single = f
                                empt.img = f
                                empt.save()
                                PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum,
                                                                     Year=YearSearch).first().Portrait.add(empt)
                                # 将往年的其他数据里面的头像自动更新，往年的数据同一个工号有多个，不能只更新编辑的这个
                                for Person in PersonalInfoHisByYear.objects.filter(
                                        GroupNum=PersonalInfoHisByYear.objects.filter(
                                            GroupNum=GroupNum).first().GroupNum):
                                    # print(Person)
                                    Person.Portrait.add(empt)
                                # 将当年的数据里面的头像自动更新，当年同意个工号只有一个数据
                                PersonalInfo.objects.filter(
                                    GroupNum=PersonalInfoHisByYear.objects.filter(
                                        GroupNum=GroupNum).first().GroupNum).first().Portrait.add(empt)
                        else:  # 如果没传头像，看看原来同工号的其他数据有没有头像，如果有，更新到本条数据中
                            for Person in PersonalInfoHisByYear.objects.filter(
                                    GroupNum=GroupNum):
                                if Person.Portrait.all():
                                    for photos in Person.Portrait.all():
                                        PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum,
                                                                             Year=YearSearch).first().Portrait.add(
                                            photos.id)
                                    break
                                if PersonalInfo.objects.filter(
                                        GroupNum=GroupNum).first():
                                    if PersonalInfo.objects.filter(
                                            GroupNum=GroupNum).first().Portrait.all():
                                        for photos in PersonalInfo.objects.filter(
                                                GroupNum=GroupNum).first().Portrait.all():
                                            PersonalInfoHisByYear.objects.filter(GroupNum=GroupNum,
                                                                                 Year=YearSearch).first().Portrait.add(
                                                photos.id)

                checkPerdic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if CustomerSearch and CustomerSearch != "All":
                    checkPerdic['Customer'] = CustomerSearch
                if DepartmentSearch and DepartmentSearch != "All":
                    checkPerdic['Department'] = DepartmentSearch
                if LessonSearch and LessonSearch != "All":
                    checkPerdic['DepartmentCode'] = LessonSearch
                if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                    checkPerdic['GroupNum'] = GroupEmployeesSearch
                if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                    for i in PersonalInfo.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(float(
                                str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                             "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
                else:  # 往年的到PersonalInfoHisByYear里面查找
                    checkPerdic["Year"] = YearSearch
                    for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                        if i.Status == "在職":
                            # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                            # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                            # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                            Seniority = round(
                                float(
                                    str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                1)
                        else:
                            Seniority = round(
                                float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                        Photolist = []
                        for h in i.Portrait.all():
                            Photolist.append({'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                        mock_data.append(
                            {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                             "DepartureDate": str(i.QuitDate),
                             "ExpectedDepartureDate": str(i.PlanQuitDate),
                             "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                             "DepartureTo": i.Whereabouts,
                             "NewCompanyName": i.NewCompany,
                             "Salary": i.Aalary,
                             "Seniority": Seniority,
                             "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                             "GroupEmployees": i.GroupNum,
                             "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                             "Gender": i.Sex,
                             "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                             "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                             "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                             "Education": i.Education, "School": i.School,
                             "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                             "English": i.ENLevel,
                             "IdNumber": i.IdCard,
                             "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                             "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                             "HukouProvinces": i.ResidenceProvince,
                             "HukouCity": i.ResidenceCounty,
                             "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                        )
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'MUTIDELETE' in str(request.body):
                    responseData = json.loads(request.body)
                    YearSearch = responseData['Year']
                    CustomerSearch = responseData['Customer']
                    DepartmentSearch = responseData['Department']
                    LessonSearch = responseData['Lesson']
                    GroupEmployeesSearch = responseData['GroupEmployees']
                    YearNow = str(datetime.datetime.now().year)
                    checkPerdic = {"Customer": CustomerSearch, "Department": DepartmentSearch,
                                   "DepartmentCode": LessonSearch,
                                   "GroupNum": GroupEmployeesSearch, }
                    if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面删除,年份为空默认删除当年数据
                        for i in responseData['params']:
                            PersonalInfoHisByPer.objects.filter(Personallink=PersonalInfo.objects.get(id=i)).delete()
                            PersonalInfo.objects.get(id=i).delete()
                        pass
                    else:  # 往年的到PersonalInfoHisByYear里面删除
                        for i in responseData['params']:
                            PersonalInfoHisByYear.objects.get(id=i).delete()

                    checkPerdic = {
                        # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                        #            "GroupNum": GroupEmployeesSearch,
                    }
                    if CustomerSearch and CustomerSearch != "All":
                        checkPerdic['Customer'] = CustomerSearch
                    if DepartmentSearch and DepartmentSearch != "All":
                        checkPerdic['Department'] = DepartmentSearch
                    if LessonSearch and LessonSearch != "All":
                        checkPerdic['DepartmentCode'] = LessonSearch
                    if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                        checkPerdic['GroupNum'] = GroupEmployeesSearch
                    if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                        for i in PersonalInfo.objects.filter(**checkPerdic):
                            if i.Status == "在職":
                                # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                                # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                                # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                                Seniority = round(float(
                                    str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            else:
                                Seniority = round(
                                    float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            Photolist = []
                            for h in i.Portrait.all():
                                Photolist.append(
                                    {'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                            mock_data.append(
                                {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                                 "DepartureDate": str(i.QuitDate),
                                 "ExpectedDepartureDate": str(i.PlanQuitDate),
                                 "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                                 "DepartureTo": i.Whereabouts,
                                 "NewCompanyName": i.NewCompany,
                                 "Salary": i.Aalary,
                                 "Seniority": Seniority,
                                 "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                                 "GroupEmployees": i.GroupNum,
                                 "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                                 "Gender": i.Sex,
                                 "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                                 "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                                 "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                                 "Education": i.Education, "School": i.School,
                                 "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                                 "English": i.ENLevel,
                                 "IdNumber": i.IdCard,
                                 "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                                 "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                                 "HukouProvinces": i.ResidenceProvince,
                                 "HukouCity": i.ResidenceCounty,
                                 "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                            )
                    else:  # 往年的到PersonalInfoHisByYear里面查找
                        checkPerdic["Year"] = YearSearch
                        for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                            if i.Status == "在職":
                                # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                                # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                                # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                                Seniority = round(
                                    float(
                                        str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                    1)
                            else:
                                Seniority = round(
                                    float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            Photolist = []
                            for h in i.Portrait.all():
                                Photolist.append(
                                    {'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                            mock_data.append(
                                {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                                 "DepartureDate": str(i.QuitDate),
                                 "ExpectedDepartureDate": str(i.PlanQuitDate),
                                 "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                                 "DepartureTo": i.Whereabouts,
                                 "NewCompanyName": i.NewCompany,
                                 "Salary": i.Aalary,
                                 "Seniority": Seniority,
                                 "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                                 "GroupEmployees": i.GroupNum,
                                 "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                                 "Gender": i.Sex,
                                 "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                                 "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                                 "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                                 "Education": i.Education, "School": i.School,
                                 "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                                 "English": i.ENLevel,
                                 "IdNumber": i.IdCard,
                                 "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                                 "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                                 "HukouProvinces": i.ResidenceProvince,
                                 "HukouCity": i.ResidenceCounty,
                                 "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                            )
                if 'ExcelData' in str(request.body):

                    responseData = json.loads(request.body)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    YearSearch = responseData['Year']
                    CustomerSearch = responseData['Customer']
                    DepartmentSearch = responseData['Department']
                    LessonSearch = responseData['Lesson']
                    GroupEmployeesSearch = responseData['GroupEmployees']
                    YearNow = str(datetime.datetime.now().year)

                    xlsxlist = json.loads(responseData['ExcelData'])
                    Departmentlist = [
                        {
                            # 'Year': '年份',
                            'GroupNum': '集團員工', 'SAPNum': 'SAP員工', }
                    ]
                    # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                    rownum = 0
                    startupload = 0
                    # print(xlsxlist)
                    for i in xlsxlist:
                        # print(type(i),i)
                        rownum += 1
                        modeldata = {}
                        for key, value in i.items():
                            if key in headermodel_PersonalInfo.keys():
                                modeldata[headermodel_PersonalInfo[key]] = value
                        # print(modeldata)
                        if 'Status' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，狀態不能爲空
                                                        """ % rownum
                            break
                        if 'RegistrationDate' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，報到日期不能爲空
                                                        """ % rownum
                            break
                        if 'QuitDate' in modeldata.keys() and modeldata['Status'] != "轉部門":
                            # if 'Whereabouts' in modeldata.keys() and 'QuitReason' in modeldata.keys():
                            if 'Whereabouts' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_ok = 2
                                err_msg = """
                                        第"%s"條數據，有離職日期，離職去向不能爲空
                                                            """ % rownum
                                break
                        if 'Status' in modeldata.keys() and modeldata['Status'] == "离职":
                            if 'QuitDate' in modeldata.keys() and 'RegistrationDate' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_ok = 2
                                err_msg = """
                                        第"%s"條數據，離職狀態，離職日期,報到日期不能爲空
                                                            """ % rownum
                                break
                        if 'Customer' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，客戶不能爲空
                                                        """ % rownum
                            break
                        if 'Department' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，部門不能爲空
                                                        """ % rownum
                            break
                        if 'DepartmentCode' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，課別不能爲空
                                                        """ % rownum
                            break
                        if 'GroupNum' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，集團員工不能爲空
                                                        """ % rownum
                            break
                        if 'CNName' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，中文姓名不能爲空
                                                        """ % rownum
                            break
                        # if 'EngName' in modeldata.keys():
                        #     startupload = 1
                        # else:
                        #     # canEdit = 0
                        #     startupload = 0
                        #     err_ok = 2
                        #     err_msg = """
                        #             第"%s"條數據，英文姓名不能爲空
                        #                                 """ % rownum
                        #     break
                        if 'Sex' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，性別不能爲空
                                                        """ % rownum
                            break
                        if 'PositionNow' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，現職稱不能爲空
                                                        """ % rownum
                            break
                        if 'RegistPosition' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，入職職稱不能爲空
                                                        """ % rownum
                            break
                        if 'PositionTimes' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，晉升次數不能爲空
                                                        """ % rownum
                            break
                        if 'Experience' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，是否承認工作經驗不能爲空
                                                        """ % rownum
                            break
                        if 'GraduationYear' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，畢業年度不能爲空
                                                        """ % rownum
                            break
                        if 'Education' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，學歷不能爲空
                                                        """ % rownum
                            break
                        if 'School' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，學校不能爲空
                                                        """ % rownum
                            break
                        if 'Major' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，專業不能爲空
                                                        """ % rownum
                            break
                        # if 'MajorAscription' in modeldata.keys():
                        #     startupload = 1
                        # else:
                        #     # canEdit = 0
                        #     startupload = 0
                        #     err_ok = 2
                        #     err_msg = """
                        #             第"%s"條數據，專業歸屬不能爲空
                        #                                 """ % rownum
                        #     break
                        if 'ENLevel' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，英語不能爲空
                                                        """ % rownum
                            break
                        if 'IdCard' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，身份証號不能爲空
                                                        """ % rownum
                            break
                        if 'NativeProvince' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，籍貫省份不能爲空
                                                        """ % rownum
                            break
                        if 'NativeCounty' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，籍貫縣市不能爲空
                                                        """ % rownum
                            break
                        if 'ResidenceProvince' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，戶口省份不能爲空
                                                        """ % rownum
                            break
                        if 'ResidenceCounty' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，戶口縣市不能爲空
                                                        """ % rownum
                            break
                        if 'MobileNum' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                    第"%s"條數據，手機號碼不能爲空
                                                        """ % rownum
                            break
                    if responseData['historyYear'] and responseData['historyYear'] != "null":  # 存到PersonalInfoHisByYear
                        Check_dic = {
                            'Year': responseData['historyYear'],
                            # 'GroupNum': modeldata['GroupNum'],
                        }
                        if PersonalInfoHisByYear.objects.filter(
                                **Check_dic):
                            err_msg = """
                                                    %s年的历史数据已经存在，如需覆盖请联系管理员
                                                                                                    """ % responseData[
                                'historyYear']
                            startupload = 0
                            err_ok = 2
                        if startupload:
                            for i in xlsxlist:
                                modeldata = {}
                                for key, value in i.items():
                                    if key in headermodel_PersonalInfo.keys():
                                        if headermodel_PersonalInfo[key] == "RegistrationDate" or \
                                                headermodel_PersonalInfo[
                                                    key] == "QuitDate" or headermodel_PersonalInfo[
                                            key] == "LastPromotionData":
                                            # value = value.replace('/', '-')
                                            # value = value.replace('.', '-')
                                            if len(value.split("/")) == 3:
                                                modeldata[headermodel_PersonalInfo[key]] = value.split("/")[2] + "-" + \
                                                                                           value.split("/")[0] + "-" + \
                                                                                           value.split("/")[1]
                                            else:
                                                modeldata[headermodel_PersonalInfo[key]] = value.split("-")[2] + "-" + \
                                                                                           value.split("-")[0] + "-" + \
                                                                                           value.split("-")[1]
                                        else:
                                            modeldata[headermodel_PersonalInfo[key]] = value
                                modeldata['Year'] = responseData['historyYear']
                                # print(modeldata)
                                PersonalInfoHisByYear.objects.create(**modeldata)
                                for perhis in PersonalInfoHisByYear.objects.filter(GroupNum=modeldata['GroupNum']):
                                    if perhis.Portrait.all():
                                        for photos in perhis.Portrait.all():
                                            PersonalInfoHisByYear.objects.filter(
                                                GroupNum=modeldata['GroupNum'],
                                                Year=responseData['historyYear']).first().Portrait.add(photos.id)
                                        break
                                if PersonalInfo.objects.filter(GroupNum=modeldata['GroupNum']).first():
                                    if PersonalInfo.objects.filter(
                                            GroupNum=modeldata['GroupNum']).first().Portrait.all():
                                        for photos in PersonalInfo.objects.filter(
                                                GroupNum=modeldata['GroupNum']).first().Portrait.all():
                                            PersonalInfoHisByYear.objects.filter(
                                                GroupNum=modeldata['GroupNum'],
                                                Year=responseData['historyYear']).first().Portrait.add(photos.id)


                    else:  # 存到PersonalInfo&PersonalInfoHisByPer
                        if startupload:
                            for i in xlsxlist:
                                modeldata = {}
                                for key, value in i.items():
                                    if key in headermodel_PersonalInfo.keys():
                                        if headermodel_PersonalInfo[key] == "RegistrationDate" or \
                                                headermodel_PersonalInfo[key] == "QuitDate" or headermodel_PersonalInfo[
                                            key] == "LastPromotionData":
                                            # value = value.replace('/', '-')
                                            # value = value.replace('.', '-')
                                            if len(value.split("/")) == 3:
                                                modeldata[headermodel_PersonalInfo[key]] = value.split("/")[2] + "-" + \
                                                                                           value.split("/")[0] + "-" + \
                                                                                           value.split("/")[1]
                                            else:
                                                modeldata[headermodel_PersonalInfo[key]] = value.split("-")[2] + "-" + \
                                                                                           value.split("-")[0] + "-" + \
                                                                                           value.split("-")[1]
                                        else:
                                            modeldata[headermodel_PersonalInfo[key]] = value
                                Check_dic = {
                                    'GroupNum': modeldata['GroupNum'],
                                }
                                # print(Check_dic)
                                # exsitdata = {}
                                if PersonalInfo.objects.filter(
                                        **Check_dic):  # 已存在的覆盖，并且如果升职的要存到PersonalInfoHisByPer
                                    Percheck1 = PersonalInfo.objects.filter(
                                        **Check_dic).first()
                                    if Percheck1.PositionNow != str(modeldata['PositionNow']) and modeldata[
                                        'Status'] == "在職":  # 职位信息变化，先存晋升记录再覆盖
                                        PersonalInfoHisByPerCreate = {"Personallink": Percheck1,
                                                                      "ChangeType": "1",
                                                                      "Department": modeldata['Department'],
                                                                      "DepartmentCode": modeldata['DepartmentCode'],
                                                                      "DepartmentCodeYear": '',
                                                                      "GroupNum": modeldata['GroupNum'],
                                                                      "SAPNum": modeldata['SAPNum'],
                                                                      "CNName": modeldata['CNName'],
                                                                      "Sex": modeldata['Sex'],
                                                                      "PositionNow": modeldata['PositionNow'],
                                                                      "PositionOld": Percheck1.PositionNow,
                                                                      "LastPromotionData": modeldata[
                                                                          'LastPromotionData'],
                                                                      # "EngName": modeldata['EngName'],
                                                                      "Editor": request.session.get('user_name'),
                                                                      "EditTime": datetime.datetime.now().strftime(
                                                                          "%Y-%m-%d %H:%M:%S"), }
                                        # if "LastPromotionData" in modeldata.keys():
                                        #     PersonalInfoHisByPerCreate['LastPromotionData'] = modeldata['LastPromotionData']
                                        if "EngName" in modeldata.keys():
                                            PersonalInfoHisByPerCreate['EngName'] = modeldata['EngName']
                                        PersonalInfoHisByPer.objects.create(**PersonalInfoHisByPerCreate)
                                        PersonalInfo.objects.filter(
                                            **Check_dic).update(**modeldata)
                                        for perhis in PersonalInfoHisByYear.objects.filter(**Check_dic):
                                            if perhis.Portrait.all():
                                                for photos in perhis.Portrait.all():
                                                    PersonalInfo.objects.filter(**Check_dic).first().Portrait.add(
                                                        photos.id)
                                                break

                                    else:  # 职位信息没有变化，直接覆盖
                                        PersonalInfo.objects.filter(
                                            **Check_dic).update(**modeldata)
                                        for perhis in PersonalInfoHisByYear.objects.filter(**Check_dic):
                                            if perhis.Portrait.all():
                                                for photos in perhis.Portrait.all():
                                                    PersonalInfo.objects.filter(**Check_dic).first().Portrait.add(
                                                        photos.id)
                                                break
                                    # print(Departmentlist, err_ok)
                                else:  # 新建新入职人员
                                    # updatedic = {}
                                    # for j in modeldata.keys():
                                    #     updatedic[j] = modeldata[j]
                                    # print(modeldata)
                                    PersonalInfo.objects.create(**modeldata)
                                    for perhis in PersonalInfoHisByYear.objects.filter(**Check_dic):
                                        if perhis.Portrait.all():
                                            for photos in perhis.Portrait.all():
                                                PersonalInfo.objects.filter(**Check_dic).first().Portrait.add(
                                                    photos.id)
                                            break

                    checkPerdic = {
                        # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                        #            "GroupNum": GroupEmployeesSearch,
                    }
                    if CustomerSearch and CustomerSearch != "All":
                        checkPerdic['Customer'] = CustomerSearch
                    if DepartmentSearch and DepartmentSearch != "All":
                        checkPerdic['Department'] = DepartmentSearch
                    if LessonSearch and LessonSearch != "All":
                        checkPerdic['DepartmentCode'] = LessonSearch
                    if GroupEmployeesSearch and GroupEmployeesSearch != "All":
                        checkPerdic['GroupNum'] = GroupEmployeesSearch
                    if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                        for i in PersonalInfo.objects.filter(**checkPerdic):
                            if i.Status == "在職":
                                # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                                # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                                # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                                Seniority = round(float(
                                    str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            else:
                                Seniority = round(
                                    float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            Photolist = []
                            for h in i.Portrait.all():
                                Photolist.append(
                                    {'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                            mock_data.append(
                                {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                                 "DepartureDate": str(i.QuitDate),
                                 "ExpectedDepartureDate": str(i.PlanQuitDate),
                                 "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                                 "DepartureTo": i.Whereabouts,
                                 "NewCompanyName": i.NewCompany,
                                 "Salary": i.Aalary,
                                 "Seniority": Seniority,
                                 "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                                 "GroupEmployees": i.GroupNum,
                                 "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                                 "Gender": i.Sex,
                                 "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                                 "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                                 "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                                 "Education": i.Education, "School": i.School,
                                 "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                                 "English": i.ENLevel,
                                 "IdNumber": i.IdCard,
                                 "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                                 "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                                 "HukouProvinces": i.ResidenceProvince,
                                 "HukouCity": i.ResidenceCounty,
                                 "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                            )
                    else:  # 往年的到PersonalInfoHisByYear里面查找
                        checkPerdic["Year"] = YearSearch
                        for i in PersonalInfoHisByYear.objects.filter(**checkPerdic):
                            if i.Status == "在職":
                                # print(type(datetime.datetime.now().date()),datetime.datetime.now().date(), type(i.RegistrationDate), i.RegistrationDate)
                                # print(type((datetime.datetime.now().date() - i.RegistrationDate)/365),(datetime.datetime.now().date() - i.RegistrationDate)/365)
                                # print(str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0])
                                Seniority = round(
                                    float(
                                        str((datetime.datetime.now().date() - i.RegistrationDate)).split(' ')[0]) / 365,
                                    1)
                            else:
                                Seniority = round(
                                    float(str((i.QuitDate - i.RegistrationDate)).split(' ')[0]) / 365, 1)
                            Photolist = []
                            for h in i.Portrait.all():
                                Photolist.append(
                                    {'name': '', 'url': '/media/' + h.img.name})  # fileListO需要的是对象列表而不是字符串列表
                            mock_data.append(
                                {"id": i.id, "Status": i.Status, "RegistrationDate": str(i.RegistrationDate),
                                 "DepartureDate": str(i.QuitDate),
                                 "ExpectedDepartureDate": str(i.PlanQuitDate),
                                 "DepartureReasons": i.QuitReason, "DepartureDetails": i.QuitDetail,
                                 "DepartureTo": i.Whereabouts,
                                 "NewCompanyName": i.NewCompany,
                                 "Salary": i.Aalary,
                                 "Seniority": Seniority,
                                 "Customer": i.Customer, "Department": i.Department, "Lesson": i.DepartmentCode,
                                 "GroupEmployees": i.GroupNum,
                                 "SAPEmployees": i.SAPNum, "ChineseName": i.CNName, "EnglishName": i.EngName,
                                 "Gender": i.Sex,
                                 "CurrentTitle": i.PositionNow, "LastPromotionDate": str(i.LastPromotionData),
                                 "EntryTitle": i.RegistPosition, "PromotionNumber": i.PositionTimes,
                                 "WorkExperience": i.Experience, "GraduationYear": i.GraduationYear,
                                 "Education": i.Education, "School": i.School,
                                 "Profession": i.Major, "ProfessionAttribution": i.MajorAscription,
                                 "English": i.ENLevel,
                                 "IdNumber": i.IdCard,
                                 "Birthday": i.IdCard[6:10] + "-" + i.IdCard[10:12] + "-" + i.IdCard[12:14],
                                 "NativeProvince": i.NativeProvince, "NativeCity": i.NativeCounty,
                                 "HukouProvinces": i.ResidenceProvince,
                                 "HukouCity": i.ResidenceCounty,
                                 "PhoneNumber": i.MobileNum, "fileListO": Photolist},
                            )

        data = {
            "err_ok": "0",
            "select": customerOptions,
            "GroupEmployeesNum": GroupEmployeesNum,
            "lessonOptions": lessonOptions,
            "content": mock_data,
            "Customeroptions1": Customeroptions1,
            "Departmentoptions1": Departmentoptions1,
            "Lessonoptions1": Lessonoptions1,
            "Titleoptions1": Titleoptions1,
            "ProfessionAttributionoptions1": ProfessionAttributionoptions1,
            'form': form,
            'fileListO': fileListO,
            "permission": permission,
            "errMsg": err_msg,
            "loginLesson": onlineuserDepartment,
            # "ProfessionAttributionoptions1": ProfessionAttributionoptions1,
        }
        # print(json.dumps(data),type(json.dumps(data)))
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/PersonalInfo_edit.html', locals())


@csrf_exempt
def ManPower_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/ManPower_search"
    canEdit = 1  # DQA权限
    mock_data = [
        # {"id": "1", "Customer": "C38", "Department_Code": "KMN0AQA000", "Chu": "DQA1", "Ministry": "一部",
        #  "Section": "二課",
        #  "Item": "7_2", "Title": "助理工程師", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0",
        #  "Nov": "0", "Dec": "0"},
        # {"id": "2", "Customer": "C38", "Department_Code": "KMN0AQA000", "Chu": "DQA2", "Ministry": "二部",
        #  "Section": "一課",
        #  "Item": "7_2", "Title": "課長", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0", "Nov": "0", "Dec": "0"},
        # {"id": "3", "Customer": "C38", "Department_Code": "KMN0AQA000", "Chu": "DQA3", "Ministry": "三部",
        #  "Section": "三課",
        #  "Item": "7_2", "Title": "工程師", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0", "Nov": "0", "Dec": "0"},
        # {"id": "4", "Customer": "C38", "Department_Code": "KMN0AQA000", "Chu": "DQA2", "Ministry": "一部",
        #  "Section": "四課",
        #  "Item": "7_2", "Title": "助理工程師", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0", "Nov": "0", "Dec": "0"},
    ]

    selectCustomer = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]

    selectYear = {
        # "2020": [{"Chu": "DQA1"}, {"Chu": "DQA2"}, {"Chu": "DQA3"}, {"Chu": "DQA4"}],
        # "2019": [{"Chu": "DQA1"}, {"Chu": "DQA2"}],
    }

    selectSection = {
        # "一部": [{"Section": "KM0MAQA000"}],
        # "二部": [{"Section": "KM0MAQAB00"}],
        # "三部": [{"Section": "KM0MAQABC0"}],
        # "四部": [{"Section": "KM0MAQABA0"}],
    }

    for i in MainPower.objects.all().values("Year").distinct().order_by("Year"):
        YearCHU = []
        for j in MainPower.objects.filter(Year=i['Year']).values("CHU").distinct().order_by("CHU"):
            YearCHU.append({"Chu": j["CHU"]})
        selectYear[i['Year']] = YearCHU

    onlineuser = request.session.get('account')
    roles = []
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100

    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i:
            canEdit = 1
        elif 'Department' in i:
            canEdit = 2
    # print(request.method)

    if request.method == 'POST':
        if request.POST.get("isGetData") == "first":
            YearSearch = request.POST.get("Year")
            CustomerSearch = request.POST.get("Customer")
            CHUSearch = request.POST.get("Chu")
            BUSearch = request.POST.get("Ministry")
            DepartmentCodeSearch = request.POST.get("Section")
            YearNow = str(datetime.datetime.now().year)
            checkMaindic = {
                # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                #            "GroupNum": GroupEmployeesSearch,
            }
            if YearSearch:
                checkMaindic['Year'] = YearNow
            if CustomerSearch and CustomerSearch != "All":
                checkMaindic['Customer'] = CustomerSearch
            if CHUSearch and CHUSearch != "All":
                checkMaindic['CHU'] = CHUSearch
            if BUSearch and BUSearch != "All":
                checkMaindic['BU'] = BUSearch
            if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                checkMaindic['DepartmentCode'] = DepartmentCodeSearch
            for i in MainPower.objects.filter(**checkMaindic):
                # print(i.DepartmentCode)
                Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                                                                Status="在職").count()
                # print(Current_Workforce)
                # DateNow = datetime.datetime.now().date()
                # print(DateNow)
                # Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                #                                                  RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                #     DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                # print(Current_Workforce1)
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                     "Ministry": i.BU, "Section": i.KE,
                     "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01, "CodeNoH02": i.CodeNoH02,
                     "Year": i.Year, "Current_Workforce": Current_Workforce,
                     "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan, "Jul": i.Jul,
                     "Aug": i.Aug, "Sep": i.Sep,
                     "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                )
        if request.POST.get("isGetData") == "SEARCH":
            YearSearch = request.POST.get("Year")
            CustomerSearch = request.POST.get("Customer")
            CHUSearch = request.POST.get("Chu")
            BUSearch = request.POST.get("Ministry")
            DepartmentCodeSearch = request.POST.get("Section")
            YearNow = str(datetime.datetime.now().year)
            checkMaindic = {
                # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                #            "GroupNum": GroupEmployeesSearch,
            }
            if YearSearch:
                checkMaindic['Year'] = YearSearch
            if CustomerSearch and CustomerSearch != "All":
                checkMaindic['Customer'] = CustomerSearch
            if CHUSearch and CHUSearch != "All":
                checkMaindic['CHU'] = CHUSearch
            if BUSearch and BUSearch != "All":
                checkMaindic['BU'] = BUSearch
            if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                checkMaindic['DepartmentCode'] = DepartmentCodeSearch
            for i in MainPower.objects.filter(**checkMaindic):
                # print(i.DepartmentCode)
                Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                                                                Status="在職").count()
                # print(Current_Workforce)
                # DateNow = datetime.datetime.now().date()
                # print(DateNow)
                # Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                #                                                  RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                #     DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                # print(Current_Workforce1)
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                     "Ministry": i.BU, "Section": i.KE,
                     "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01, "CodeNoH02": i.CodeNoH02,
                     "Year": i.Year, "Current_Workforce": Current_Workforce,
                     "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan, "Jul": i.Jul,
                     "Aug": i.Aug, "Sep": i.Sep,
                     "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                )
        if request.POST.get("isGetData") == "changeChu":
            YearSearch = request.POST.get("Year")
            CHUSearch = request.POST.get("chu")
            checkbuke = {}
            if YearSearch:
                checkbuke["Year"] = YearSearch
            if CHUSearch:
                checkbuke["CHU"] = CHUSearch
            for i in MainPower.objects.filter(**checkbuke).values("BU").distinct().order_by("BU"):
                YearCHU = []
                checkbuke1 = checkbuke
                checkbuke1['BU'] = i['BU']
                for j in MainPower.objects.filter(**checkbuke1).values("DepartmentCode").distinct().order_by(
                        "DepartmentCode"):
                    YearCHU.append({"Section": j["DepartmentCode"]})
                if not i['BU']:
                    selectSection[''] = YearCHU
                else:
                    selectSection[i['BU']] = YearCHU
        data = {
            "canEdit": canEdit,
            "content": mock_data,
            "selectCustomer": selectCustomer,
            "selectYear": selectYear,
            "selectSection": selectSection

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/ManPower_search.html', locals())


@csrf_exempt
def ManPower_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/ManPower_edit"
    mock_data = [
        # {"id": "1", "Customer":"C38(NB)", "Department_Code": "KMN0AQA000", "Chu": "DQA1", "Ministry": "一部", "Section": "二課",
        #  "Item": "7_2", "Title": "助理工程師", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0", "Nov": "0", "Dec": "0"},
        # {"id": "2", "Department_Code": "KMN0AQAB00", "Chu": "DQA2", "Ministry": "二部", "Section": "一課",
        #  "Item": "7_2", "Title": "課長", "CodeNoH01": "CN", "CodeNoH02": "N", "Year": "2019", "Current_Workforce": "2",
        #  "Jan": "1", "Feb": "1", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0",
        #  "Oct": "0", "Nov": "0", "Dec": "0"},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]

    selectCustomer = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]

    selectYear = {
        # "2020": [{"Chu": "DQA1"}, {"Chu": "DQA2"}, {"Chu": "DQA3"}, {"Chu": "DQA4"}],
        # "2019": [{"Chu": "DQA1"}, {"Chu": "DQA2"}],
    }

    selectSection = {
        # "一部": [{"Section": "KM0MAQA000"}],
        # "二部": [{"Section": "KM0MAQAB00"}],
        # "三部": [{"Section": "KM0MAQABC0"}],
        # "四部": [{"Section": "KM0MAQABA0"}],
    }

    sectionOption = [
        # "KM0MAQA000", "KM0MAQAB00", "KM0MAQABC0", "KM0MAQABA0",
    ]
    itemOption = [
        # '7_2', '6_1_Other'
    ]
    err_msg = ''
    department = ''  # 'KMN0AQA000'
    onlineuserDepartment = ''
    permission = 100  # 助理编辑权限为1（所有信息皆可编辑），课长级编辑权限为2（只能编辑离职信息）
    roles = []
    onlineuser = request.session.get('account')
    # onlineuser = '0502413'
    onlineuserDepartment = ''
    # print(onlineuser,UserInfo.objects.get(account=onlineuser))
    if Departments.objects.filter(Manager=onlineuser):
        permission = 2
        onlineuserDepartment = Departments.objects.filter(Manager=onlineuser).first().Department_Code
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i:
            permission = 1
        elif 'Department' in i:
            permission = 3
    # print(request.method)
    for i in MainPower.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i['Customer'])
    for i in MainPower.objects.all().values("Year").distinct().order_by("Year"):
        YearCHU = []
        for j in MainPower.objects.filter(Year=i['Year']).values("CHU").distinct().order_by("CHU"):
            YearCHU.append({"Chu": j["CHU"]})
        selectYear[i['Year']] = YearCHU
    # YearNow = str(datetime.datetime.now().year)
    # for i in Positions.objects.filter(Year=YearNow).values("Item").distinct().order_by("Item"):
    #     itemOption.append(i["Item"])
    YearNow = str(datetime.datetime.now().year)
    for i in Positions.objects.filter(Year=YearNow).values("Item").distinct().order_by("Item"):
        itemOption.append(i["Item"])

    if request.method == 'POST':
        if request.POST:
            if request.POST.get("isGetData") == "first":
                YearSearch = request.POST.get("Year")
                CustomerSearch = request.POST.get("Customer")
                CHUSearch = request.POST.get("Chu")
                BUSearch = request.POST.get("Ministry")
                DepartmentCodeSearch = request.POST.get("Section")
                YearNow = str(datetime.datetime.now().year)
                checkMaindic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if YearSearch:
                    checkMaindic['Year'] = YearNow
                if CustomerSearch and CustomerSearch != "All":
                    checkMaindic['Customer'] = CustomerSearch
                if CHUSearch and CHUSearch != "All":
                    checkMaindic['CHU'] = CHUSearch
                if BUSearch and BUSearch != "All":
                    checkMaindic['BU'] = BUSearch
                if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                    checkMaindic['DepartmentCode'] = DepartmentCodeSearch
                for i in MainPower.objects.filter(**checkMaindic):
                    # print(i.DepartmentCode)
                    Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                                                                    Status="在職").count()
                    # print(Current_Workforce)
                    # DateNow = datetime.datetime.now().date()
                    # print(DateNow)
                    # Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                    #                                                  RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                    #     DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                    # print(Current_Workforce1)
                    mock_data.append(
                        {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                         "Ministry": i.BU, "Section": i.KE,
                         "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01, "CodeNoH02": i.CodeNoH02,
                         "Year": i.Year, "Current_Workforce": Current_Workforce,
                         "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan,
                         "Jul": i.Jul,
                         "Aug": i.Aug, "Sep": i.Sep,
                         "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                    )
            if request.POST.get("isGetData") == "SEARCH":
                YearSearch = request.POST.get("Year")
                CustomerSearch = request.POST.get("Customer")
                CHUSearch = request.POST.get("Chu")
                BUSearch = request.POST.get("Ministry")
                DepartmentCodeSearch = request.POST.get("Section")
                YearNow = str(datetime.datetime.now().year)
                checkMaindic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if YearSearch:
                    checkMaindic['Year'] = YearSearch
                if CustomerSearch and CustomerSearch != "All":
                    checkMaindic['Customer'] = CustomerSearch
                if CHUSearch and CHUSearch != "All":
                    checkMaindic['CHU'] = CHUSearch
                if BUSearch and BUSearch != "All":
                    checkMaindic['BU'] = BUSearch
                if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                    checkMaindic['DepartmentCode'] = DepartmentCodeSearch
                for i in MainPower.objects.filter(**checkMaindic):
                    # print(i.DepartmentCode)
                    Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                                                                    Status="在職").count()
                    # print(Current_Workforce)
                    # DateNow = datetime.datetime.now().date()
                    # print(DateNow)
                    # Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                    #                                                  RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                    #     DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                    # print(Current_Workforce1)
                    mock_data.append(
                        {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                         "Ministry": i.BU, "Section": i.KE,
                         "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01, "CodeNoH02": i.CodeNoH02,
                         "Year": i.Year, "Current_Workforce": Current_Workforce,
                         "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan,
                         "Jul": i.Jul, "Aug": i.Aug, "Sep": i.Sep,
                         "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                    )
                if not YearSearch:
                    YearSearch = YearNow
                itemOption = []
                for i in Positions.objects.filter(Year=YearSearch).values("Item").distinct().order_by("Item"):
                    itemOption.append(i["Item"])
            if request.POST.get("isGetData") == "changeChu":
                YearSearch = request.POST.get("Year")
                CHUSearch = request.POST.get("chu")
                checkbuke = {}
                if YearSearch:
                    checkbuke["Year"] = YearSearch
                if CHUSearch:
                    checkbuke["CHU"] = CHUSearch
                for i in MainPower.objects.filter(**checkbuke).values("BU").distinct().order_by("BU"):
                    YearCHU = []
                    checkbuke1 = checkbuke
                    checkbuke1['BU'] = i['BU']
                    for j in MainPower.objects.filter(**checkbuke1).values("DepartmentCode").distinct().order_by(
                            "DepartmentCode"):
                        YearCHU.append({"Section": j["DepartmentCode"]})
                    if not i['BU']:
                        selectSection[''] = YearCHU
                    else:
                        selectSection[i['BU']] = YearCHU
            if request.POST.get("action") == "submit":
                YearSearch = request.POST.get("YearSearch")
                CustomerSearch = request.POST.get("CustomerSearch")
                CHUSearch = request.POST.get("ChuSearch")
                BUSearch = request.POST.get("MinistrySearch")
                DepartmentCodeSearch = request.POST.get("SectionSearch")
                # YearNow = str(datetime.datetime.now().year)

                ManID = request.POST.get("id")
                MainPowerupdate = {"Customer": request.POST.get("Customer"),
                                   "DepartmentCode": request.POST.get("Department_Code"),
                                   "CHU": request.POST.get("Chu"), "BU": request.POST.get("Ministry"),
                                   "KE": request.POST.get("Section"),
                                   "Item": request.POST.get("Item"), "Positions_Name": request.POST.get("Title"),
                                   "CodeNoH01": request.POST.get("CodeNoH01"),
                                   "CodeNoH02": request.POST.get("CodeNoH02"),
                                   "Year": request.POST.get("Year"),
                                   "Jan": request.POST.get("Jan"), "Feb": request.POST.get("Feb"),
                                   "Mar": request.POST.get("Mar"),
                                   "Apr": request.POST.get("Apr"), "May": request.POST.get("May"),
                                   "Jun": request.POST.get("Jun"),
                                   "Jul": request.POST.get("Jul"), "Aug": request.POST.get("Aug"),
                                   "Sep": request.POST.get("Sep"),
                                   "Oct": request.POST.get("Oct"), "Nov": request.POST.get("Nov"),
                                   "Dec": request.POST.get("Dec")}

                MainPower.objects.filter(id=ManID).update(**MainPowerupdate)

                checkMaindic = {
                    # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                    #            "GroupNum": GroupEmployeesSearch,
                }
                if YearSearch:
                    checkMaindic['Year'] = YearSearch
                if CustomerSearch and CustomerSearch != "All":
                    checkMaindic['Customer'] = CustomerSearch
                if CHUSearch and CHUSearch != "All":
                    checkMaindic['CHU'] = CHUSearch
                if BUSearch and BUSearch != "All":
                    checkMaindic['BU'] = BUSearch
                if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                    checkMaindic['DepartmentCode'] = DepartmentCodeSearch
                for i in MainPower.objects.filter(**checkMaindic):
                    # print(i.DepartmentCode)
                    Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode, PositionNow=i.Item,
                                                                    Status="在職").count()
                    # print(Current_Workforce)
                    # DateNow = datetime.datetime.now().date()
                    # print(DateNow)
                    # Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode,
                    #                                                  PositionNow=i.Item,
                    #                                                  RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                    #     DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                    # print(Current_Workforce1)
                    mock_data.append(
                        {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                         "Ministry": i.BU,
                         "Section": i.KE,
                         "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01, "CodeNoH02": i.CodeNoH02,
                         "Year": i.Year, "Current_Workforce": Current_Workforce,
                         "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan,
                         "Jul": i.Jul, "Aug": i.Aug, "Sep": i.Sep,
                         "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                    )


        else:
            try:
                request.body
            except:
                pass
            else:
                if 'ExcelData' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    YearSearch = responseData['year']
                    CustomerSearch = responseData['customer']
                    CHUSearch = responseData['chu']
                    BUSearch = responseData['ministry']
                    DepartmentCodeSearch = responseData['section']
                    YearNow = str(datetime.datetime.now().year)

                    xlsxlist = json.loads(responseData['ExcelData'])
                    Departmentlist = [
                        {
                            'Year': '年份', 'DepartmentCode': '課別', 'Item': '項次',
                        }
                    ]
                    # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                    rownum = 0
                    startupload = 0
                    # print(xlsxlist)
                    for i in xlsxlist:
                        # print(type(i),i)
                        rownum += 1
                        modeldata = {}
                        for key, value in i.items():
                            if key in headermodel_MainPower.keys():
                                modeldata[headermodel_MainPower[key]] = value
                        if 'Year' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，年份不能爲空
                                                                            """ % rownum
                            break
                        if 'DepartmentCode' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，部門代碼不能爲空
                                                                            """ % rownum
                            break
                        if 'Customer' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，客戶別不能爲空
                                                                            """ % rownum
                            break
                        if 'Item' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，項次不能爲空
                                                                            """ % rownum
                            break
                        if 'CodeNoH01' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，CodeNoH01不能爲空
                                                                            """ % rownum
                            break
                        if 'CodeNoH02' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，CodeNoH02不能爲空
                                                                            """ % rownum
                            break
                        if 'Jan' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，一月不能爲空
                                                                            """ % rownum
                            break
                        if 'Feb' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，二月不能爲空
                                                                            """ % rownum
                            break
                        if 'Mar' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，三月不能爲空
                                                                            """ % rownum
                            break
                        if 'Apr' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，四月不能爲空
                                                                            """ % rownum
                            break
                        if 'May' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，五月不能爲空
                                                                            """ % rownum
                            break
                        if 'Jun' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，六月次數不能爲空
                                                                            """ % rownum
                            break
                        if 'Jul' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，七月不能爲空
                                                                            """ % rownum
                            break
                        if 'Aug' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，八月不能爲空
                                                                            """ % rownum
                            break
                        if 'Sep' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，九月不能爲空
                                                                            """ % rownum
                            break
                        if 'Oct' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，十月不能爲空
                                                                            """ % rownum
                            break
                        if 'Nov' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，十一月不能爲空
                                                                            """ % rownum
                            break
                        if 'Dec' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                                                        第"%s"條數據，十二月不能爲空
                                                                            """ % rownum
                            break

                    if startupload:
                        for i in xlsxlist:
                            # print(i)
                            modeldata = {}
                            for key, value in i.items():
                                if key in headermodel_MainPower.keys():
                                    modeldata[headermodel_MainPower[key]] = value
                            # print(modeldata)
                            Check_dic = {
                                'Year': modeldata['Year'], 'DepartmentCode': modeldata['DepartmentCode'],
                                'Item': modeldata['Item'],
                            }
                            # print(Check_dic)
                            # exsitdata = {}
                            if MainPower.objects.filter(
                                    **Check_dic):  # 已存在的覆盖，
                                Maincheck1 = MainPower.objects.filter(
                                    **Check_dic).first()

                                MainPower.objects.filter(
                                    **Check_dic).update(**modeldata)
                            else:  # 新建
                                MainPower.objects.create(**modeldata)

                    checkMaindic = {
                        # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                        #            "GroupNum": GroupEmployeesSearch,
                    }
                    if YearSearch:
                        checkMaindic['Year'] = YearSearch
                    if CustomerSearch and CustomerSearch != "All":
                        checkMaindic['Customer'] = CustomerSearch
                    if CHUSearch and CHUSearch != "All":
                        checkMaindic['CHU'] = CHUSearch
                    if BUSearch and BUSearch != "All":
                        checkMaindic['BU'] = BUSearch
                    if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                        checkMaindic['DepartmentCode'] = DepartmentCodeSearch
                    for i in MainPower.objects.filter(**checkMaindic):
                        # print(i.DepartmentCode)
                        Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode,
                                                                        PositionNow=i.Item, Status="在職").count()
                        # print(Current_Workforce)
                        DateNow = datetime.datetime.now().date()
                        # print(DateNow)
                        Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode,
                                                                         PositionNow=i.Item,
                                                                         RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                            DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                        # print(Current_Workforce1)
                        mock_data.append(
                            {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                             "Ministry": i.BU,
                             "Section": i.KE,
                             "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01,
                             "CodeNoH02": i.CodeNoH02, "Year": i.Year, "Current_Workforce": Current_Workforce,
                             "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan,
                             "Jul": i.Jul, "Aug": i.Aug, "Sep": i.Sep,
                             "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                        )
                if 'MUTICANCEL' in str(request.body):
                    responseData = json.loads(request.body)
                    YearSearch = responseData['Year']
                    CustomerSearch = responseData['Customer']
                    CHUSearch = responseData['Chu']
                    BUSearch = responseData['Ministry']
                    DepartmentCodeSearch = responseData['Section']

                    for i in responseData['params']:
                        MainPower.objects.filter(id=i).delete()

                    checkMaindic = {
                        # "Customer": CustomerSearch, "Department": DepartmentSearch, "DepartmentCode": LessonSearch,
                        #            "GroupNum": GroupEmployeesSearch,
                    }
                    if YearSearch:
                        checkMaindic['Year'] = YearSearch
                    if CustomerSearch and CustomerSearch != "All":
                        checkMaindic['Customer'] = CustomerSearch
                    if CHUSearch and CHUSearch != "All":
                        checkMaindic['CHU'] = CHUSearch
                    if BUSearch and BUSearch != "All":
                        checkMaindic['BU'] = BUSearch
                    if DepartmentCodeSearch and DepartmentCodeSearch != "All":
                        checkMaindic['DepartmentCode'] = DepartmentCodeSearch
                    for i in MainPower.objects.filter(**checkMaindic):
                        # print(i.DepartmentCode)
                        Current_Workforce = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode,
                                                                        PositionNow=i.Item, Status="在職").count()
                        # print(Current_Workforce)
                        DateNow = datetime.datetime.now().date()
                        # print(DateNow)
                        Current_Workforce1 = PersonalInfo.objects.filter(DepartmentCode=i.DepartmentCode,
                                                                         PositionNow=i.Item,
                                                                         RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                            DepartmentCode=i.DepartmentCode, PositionNow=i.Item, QuitDate__lte=DateNow).count()
                        # print(Current_Workforce1)
                        mock_data.append(
                            {"id": i.id, "Customer": i.Customer, "Department_Code": i.DepartmentCode, "Chu": i.CHU,
                             "Ministry": i.BU,
                             "Section": i.KE,
                             "Item": i.Item, "Title": i.Positions_Name, "CodeNoH01": i.CodeNoH01,
                             "CodeNoH02": i.CodeNoH02, "Year": i.Year, "Current_Workforce": Current_Workforce,
                             "Jan": i.Jan, "Feb": i.Feb, "Mar": i.Mar, "Apr": i.Apr, "May": i.May, "Jun": i.Jan,
                             "Jul": i.Jul, "Aug": i.Aug, "Sep": i.Sep,
                             "Oct": i.Oct, "Nov": i.Nov, "Dec": i.Dec},
                        )

        data = {
            "content": mock_data,
            "select": selectItem,
            "permission": permission,
            "selectCustomer": selectCustomer,
            "selectYear": selectYear,
            "selectSection": selectSection,
            "sectionOption": sectionOption,
            "itemOption": itemOption,
            "department": onlineuserDepartment,
            "errMsg": err_msg,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/ManPower_edit.html', locals())


@csrf_exempt
def Summary1(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/Summary1"

    mock_data1 = [
        # {"Department": "KF0MAQAA00(DQA1 五部)", "QM": "謝信福", "IDL_Sum": "65", "Jan": "43.45", "Feb": "0.41",
        #  "Mar": "23.93", "Apr": "60.07",
        #  "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
        #  "Year_Average": "31.97"},
        # {"Department": "KF0MAQAB00(DQA1 六部)", "QM": "朱紹貴", "IDL_Sum": "57", "Jan": "43.45", "Feb": "0.41",
        #  "Mar": "23.93", "Apr": "60.07",
        #  "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
        #  "Year_Average": "31.97"},
        # {"Department": "KF0MAQAC00(DQA1 七部)", "QM": "鄧琴", "IDL_Sum": "71", "Jan": "43.45", "Feb": "0.41",
        #  "Mar": "23.93", "Apr": "60.07",
        #  "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
        #  "Year_Average": "31.97"},
        # {"Department": "KF0MAQAD00(DQA1 八部)", "QM": "林益成", "IDL_Sum": "60", "Jan": "43.45", "Feb": "0.41",
        #  "Mar": "23.93", "Apr": "60.07",
        #  "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
        #  "Year_Average": "31.97"},
    ]
    overtimeTable1 = [
        # {"Chu": "A31", "Program": "人數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A31", "Program": "加班時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A31", "Program": "請假時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A31", "Program": "平均加班(A)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A31", "Program": "平均請假(B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A31", "Program": "有效加班\n(C=A-B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "人數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "加班時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "請假時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "平均加班(A)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "平均請假(B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "A32", "Program": "有效加班\n(C=A-B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "人數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "加班時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "請假時數", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "平均加班(A)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "平均請假(B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
        # {"Chu": "C38", "Program": "有效加班\n(C=A-B)", "Jan": "168", "Feb": "178", "Mar": "233", "Apr": "233", "May": "233", "Jun": "233", "Jul": "233", "Aug": "233", "Sep": "233", "Oct": "233", "Nov": "233", "Dec": "233", },
    ]
    heBingNum = [
        # 6, 6, 6,
    ]
    monthDiagram1Data = [
        # {
        #     'name': 'A31',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': 'A32',
        #     'type': 'bar',
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },
        # {
        #     'name': 'C38',
        #     'type': 'bar',
        #     'data': [210, 209, 210, 203, 199, 194, 209, 203, 212, 214, 218, 220]
        # },
        # {
        #     'name': '預算',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [659, 682, 677, 678, 609, 572, 567, 575, 575, 577, 567, 628]
        # },
        # {
        #     'name': '在職',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [628, 622, 625, 615, 602, 588, 635, 612, 613, 631, 646, 667]
        # }
    ]  # X轴是固定的1~12月 平均加班
    monthDiagram2Data = [
        # {
        #     'name': 'A31',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': 'A32',
        #     'type': 'bar',
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },
        # {
        #     'name': 'C38',
        #     'type': 'bar',
        #     'data': [210, 209, 210, 203, 199, 194, 209, 203, 212, 214, 218, 220]
        # },
        # {
        #     'name': '預算',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [659, 682, 677, 678, 609, 572, 567, 575, 575, 577, 567, 628]
        # },
        # {
        #     'name': '在職',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [628, 622, 625, 615, 602, 588, 635, 612, 613, 631, 646, 667]
        # }
    ]  # X轴是固定的1~12月 平均請假
    monthDiagram3Data = [
        # {
        #     'name': 'A31',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': 'A32',
        #     'type': 'bar',
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },
        # {
        #     'name': 'C38',
        #     'type': 'bar',
        #     'data': [210, 209, 210, 203, 199, 194, 209, 203, 212, 214, 218, 220]
        # },
        # {
        #     'name': '預算',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [659, 682, 677, 678, 609, 572, 567, 575, 575, 577, 567, 628]
        # },
        # {
        #     'name': '在職',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [628, 622, 625, 615, 602, 588, 635, 612, 613, 631, 646, 667]
        # }
    ]  # X轴是固定的1~12月
    monthDiagramA31Data = [
        # {
        #     'name': '平均加班',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': '平均請假',
        #     'type': 'bar',
        #     'yAxisIndex': 1,
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },

    ]  # X轴是固定的1~12月
    monthDiagramA32Data = [
        # {
        #     'name': '平均加班',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': '平均請假',
        #     'type': 'bar',
        #     'yAxisIndex': 1,
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },

    ]  # X轴是固定的1~12月
    monthDiagramC38Data = [
        # {
        #     'name': '平均加班',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': '平均請假',
        #     'type': 'bar',
        #     'yAxisIndex': 1,
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },

    ]  # X轴是固定的1~12月

    mock_data2 = [
        # {"Department_Code": "DX0MAQAA00", "Job_Num": "38021381", "Name": "沈寶珍", "Title": "補休", "Year": "2020",
        #  "Month": "5", "Hours": "2"},
        # {"Department_Code": "DX0MAQAAA0", "Job_Num": "38018430", "Name": "王勁璇", "Title": "補休", "Year": "2020",
        #  "Month": "6", "Hours": "1"},
        # {"Department_Code": "DX0MAQAB00", "Job_Num": "38021381", "Name": "汪玨", "Title": "補休", "Year": "2020",
        #  "Month": "7", "Hours": "2"},
    ]
    selectItem = [
        # "KF0MAQAA00", "KF0MAQAB00", "KF0MAQAC00", "KH0MAQAB00"
    ]

    Summary = {
        # "Department_key": ['KF0MAQAA00(DQA1 五部)', 'KF0MAQAB00(DQA1 六部)', 'KF0MAQAC00(DQA1 七部)', 'KF0MAQAD00(DQA1 八部)',
        #                    'KH0MAQAA00(DQA2 四部)', 'KH0MAQAB00(DQA2 五部)'],
    }
    Month = [
        # {
        #     "name": "Jan",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [43.5, 47.65, 38.81, 39.47, 52.81, 57.79]
        # },
        # {
        #     "name": "Feb",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [0.41, 0.6, 0.21, 0, 2.63, 0]
        # },
        # {
        #     "name": "Mar",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [23.93, 35.99, 32.36, 28.01, 45.84, 49.18]
        # },
        # {
        #     "name": "Apr",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [60.07, 61.66, 58.46, 54.03, 67.97, 71.45]
        # },
    ]

    Month_Singal = [
        # {
        #     "name": "Jan",
        #     "type": "bar",
        #     "barMaxWidth": 50,
        #     "data": [43.5, 47.65, 38.81, 39.47, 52.81, 57.79]
        # },
        # {
        #     "name": "IDL人數",
        #     "type": "line",
        #     "yAxisIndex": 1,
        #     "data": [61, 76, 85, 44, 56, 85]
        # },
    ]
    # 如果有parent的话
    # DepartmentDetail = [
    #     {
    #     "id": "1", "Companys":"", "Plants": "", "CHU": "DQA3", "BU": "", "KE": "", "Customer": "C38", "Department_Code": "KMA000000", "Manager": "C1010S3",
    #     "Children": [
    #         {"id": "2", "Companys":"", "Plants": "", "CHU": "DQA3", "BU": "KM0MAQAB00", "KE": "", "Customer": "C38", "Department_Code": "KMA000000", "Manager": "C1010S3",
    #         "Children": [
    #                         {"id": "3", "Companys":"", "Plants": "", "CHU": "DQA3", "BU": "KM0MAQAB00", "KE": "KM0MAQABC0", "Customer": "C38", "Department_Code": "KMA000000", "Manager": "C1010S3",
    #                                                                     "Children": []
    #                                                                 }
    #                                                ]
    #                                 }
    #     ]
    #     }
    # ]

    if request.method == 'POST':
        if request.POST.get("isGetData") == "first":
            # Search1 default
            YearSearch = request.POST.get("Date")
            Department_Code = request.POST.get("Department_Code")
            YearNow = str(datetime.datetime.now().year)
            # Month
            if not YearSearch or YearSearch == YearNow:
                mounthnow = datetime.datetime.now().month
                # for i in Departments.objects.filter(Year=YearNow, BU__isnull=True, KE__isnull=True):
                #     print(i)
                Yuefenlist = [("Jan", "1"), ("Feb", "2"), ("Mar", "3"), ("Apr", "4"), ("May", "5"), ("Jun", "6"),
                              ("Jul", "7"), ("Aug", "8"), ("Sep", "9"), ("Oct", "10"), ("Nov", "11"), ("Dec", "12")]
                for i in Departments.objects.filter(Year=YearNow, BU__isnull=False, KE__isnull=True):
                    mock_data1_dict = {
                        #            "Department": "KF0MAQAA00(DQA1 五部)", "QM": "謝信福", "IDL_Sum": "65", "Jan": "43.45", "Feb": "0.41",
                        # "Mar": "23.93", "Apr": "60.07",
                        # "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
                        # "Year_Average": "31.97"
                    }
                    mock_data1_dict["Department"] = i.Department_Code + "(" + i.CHU + i.BU + ")"
                    mock_data1_dict["QM"] = PersonalInfo.objects.filter(GroupNum=i.Manager).first().CNName
                    # print(mock_data1_dict["QM"])
                    IDL_Sum = 0
                    Yuefen = {"Jan": 0, "Feb": 0,
                              "Mar": 0, "Apr": 0,
                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
                    for j in Departments.objects.filter(Year=YearNow, CHU=i.CHU, BU=i.BU,
                                                        KE__isnull=False):  # 每个部下面的课的部门代码
                        # print(i.Department_Code, j)
                        # 每个课下的除了课长的所有人
                        # IDL_Sum += PersonalInfo.objects.filter(DepartmentCode=j).exclude(
                        #     PositionNow__in=["6_2_Other", "6_2_ZG", "6_1_Other", "6_1_ZG"]).count()
                        IDL_Sum += PersonalInfo.objects.filter(DepartmentCode=j).count()
                        mounthnum = 1
                        for k in Yuefenlist:
                            if mounthnum > mounthnow:
                                break
                            else:
                                # 加班时数
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Peacetime"))["Peacetime__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("Peacetime"))["Peacetime__sum"]
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("PeriodHoliday"))["PeriodHoliday__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("PeriodHoliday"))["PeriodHoliday__sum"]
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("NationalHoliday"))["NationalHoliday__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("NationalHoliday"))["NationalHoliday__sum"]
                                # 请假时数，除了产假,方式一
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PublicHoliday"))["PublicHoliday__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PublicHoliday"))["PublicHoliday__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("WorkInjury"))["WorkInjury__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("WorkInjury"))["WorkInjury__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Matters"))["Matters__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Matters"))["Matters__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("MattersContinuation"))["MattersContinuation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("MattersContinuation"))["MattersContinuation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Sick"))["Sick__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Sick"))["Sick__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("SickContinuation"))["SickContinuation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("SickContinuation"))["SickContinuation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Marriage"))["Marriage__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Marriage"))["Marriage__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Bereavement"))["Bereavement__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Bereavement"))["Bereavement__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Special"))["Special__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Special"))["Special__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("OffDuty"))["OffDuty__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("OffDuty"))["OffDuty__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Compensatory"))["Compensatory__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Compensatory"))["Compensatory__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("NoScheduling"))["NoScheduling__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("NoScheduling"))["NoScheduling__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PaternityLeave"))["PaternityLeave__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PaternityLeave"))["PaternityLeave__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Absenteeism"))["Absenteeism__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Absenteeism"))["Absenteeism__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Lactation"))["Lactation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Lactation"))["Lactation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Others"))["Others__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Others"))["Others__sum"]
                                # 请假时数，除了产假,方式2
                                if LeaveInfo.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Total"))["Total__sum"]:
                                    Yuefen[k[0]] -= \
                                        LeaveInfo.objects.filter(Year=YearNow, Department_Code=j,
                                                                 Mounth=k[1]).aggregate(
                                            Sum("Total"))["Total__sum"]
                                if LeaveInfo.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Maternity"))["Maternity__sum"]:
                                    Yuefen[k[0]] += \
                                        LeaveInfo.objects.filter(Year=YearNow, Department_Code=j,
                                                                 Mounth=k[1]).aggregate(
                                            Sum("Maternity"))["Maternity__sum"]
                            mounthnum += 1

                    mock_data1_dict["IDL_Sum"] = IDL_Sum
                    mock_data1_dict["Jan"] = Yuefen["Jan"]
                    mock_data1_dict["Feb"] = Yuefen["Feb"]
                    mock_data1_dict["Mar"] = Yuefen["Mar"]
                    mock_data1_dict["Apr"] = Yuefen["Apr"]
                    mock_data1_dict["May"] = Yuefen["May"]
                    mock_data1_dict["Jun"] = Yuefen["Jun"]
                    mock_data1_dict["Jul"] = Yuefen["Jul"]
                    mock_data1_dict["Aug"] = Yuefen["Aug"]
                    mock_data1_dict["Sep"] = Yuefen["Sep"]
                    mock_data1_dict["Oct"] = Yuefen["Oct"]
                    mock_data1_dict["Nov"] = Yuefen["Nov"]
                    mock_data1_dict["Dec"] = Yuefen["Dec"]
                    mock_data1_dict["Year_Sum"] = Yuefen["Jan"] + Yuefen["Feb"] + Yuefen["Mar"] + Yuefen["Apr"] + \
                                                  Yuefen["May"] + Yuefen["Jun"] + \
                                                  Yuefen["Jul"] + Yuefen["Aug"] + Yuefen["Sep"] + Yuefen["Oct"] + \
                                                  Yuefen["Nov"] + Yuefen["Dec"]
                    mock_data1_dict["Year_Average"] = round(mock_data1_dict["Year_Sum"] / mounthnow, 2)
                    mock_data1.append(mock_data1_dict)
                SubCount = 0
                Monthly_Average = 0
                Bunum = 0
                mock_data1_SubCount = {"Department": "Sub- Count", "QM": "", "IDL_Sum": 0, "Jan": 0, "Feb": 0, "Mar": 0,
                                       "Apr": 0,
                                       "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0,
                                       "Year_Sum": 0, "Year_Average": 0}
                mock_data1_Monthly_Average = {"Department": "Monthly Average", "QM": "", "Jan": 0, "Feb": 0, "Mar": 0,
                                              "Apr": 0,
                                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0,
                                              "Dec": 0, }
                for i in mock_data1:
                    Bunum += 1
                    mock_data1_SubCount["IDL_Sum"] += i["IDL_Sum"]
                    mock_data1_SubCount["Jan"] += i["Jan"]
                    mock_data1_SubCount["Feb"] += i["Feb"]
                    mock_data1_SubCount["Mar"] += i["Mar"]
                    mock_data1_SubCount["Apr"] += i["Apr"]
                    mock_data1_SubCount["May"] += i["May"]
                    mock_data1_SubCount["Jun"] += i["Jun"]
                    mock_data1_SubCount["Jul"] += i["Jul"]
                    mock_data1_SubCount["Aug"] += i["Aug"]
                    mock_data1_SubCount["Sep"] += i["Sep"]
                    mock_data1_SubCount["Oct"] += i["Oct"]
                    mock_data1_SubCount["Nov"] += i["Nov"]
                    mock_data1_SubCount["Dec"] += i["Dec"]
                    mock_data1_SubCount["Year_Sum"] += i["Year_Sum"]
                mock_data1_SubCount["Year_Average"] += round(mock_data1_SubCount["Year_Sum"] / mounthnow, 2)
                mock_data1.append(mock_data1_SubCount)
                if Bunum:
                    mock_data1_Monthly_Average["Jan"] = round(mock_data1_SubCount["Jan"] / Bunum, 2)
                    mock_data1_Monthly_Average["Feb"] = round(mock_data1_SubCount["Feb"] / Bunum, 2)
                    mock_data1_Monthly_Average["Mar"] = round(mock_data1_SubCount["Mar"] / Bunum, 2)
                    mock_data1_Monthly_Average["Apr"] = round(mock_data1_SubCount["Apr"] / Bunum, 2)
                    mock_data1_Monthly_Average["May"] = round(mock_data1_SubCount["May"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jun"] = round(mock_data1_SubCount["Jun"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jul"] = round(mock_data1_SubCount["Jul"] / Bunum, 2)
                    mock_data1_Monthly_Average["Aug"] = round(mock_data1_SubCount["Aug"] / Bunum, 2)
                    mock_data1_Monthly_Average["Sep"] = round(mock_data1_SubCount["Sep"] / Bunum, 2)
                    mock_data1_Monthly_Average["Oct"] = round(mock_data1_SubCount["Oct"] / Bunum, 2)
                    mock_data1_Monthly_Average["Nov"] = round(mock_data1_SubCount["Nov"] / Bunum, 2)
                    mock_data1_Monthly_Average["Dec"] = round(mock_data1_SubCount["Dec"] / Bunum, 2)
                mock_data1.append(mock_data1_Monthly_Average)

                for i in mock_data1:
                    for j in Yuefenlist:
                        if int(j[1]) > mounthnow:
                            # print(j[0])
                            i[j[0]] = ''
            Yuefenlist = [("Jan", "1"), ("Feb", "2"), ("Mar", "3"), ("Apr", "4"), ("May", "5"),
                          ("Jun", "6"),
                          ("Jul", "7"), ("Aug", "8"), ("Sep", "9"), ("Oct", "10"), ("Nov", "11"),
                          ("Dec", "12")]
            mounthnow = datetime.datetime.now().month
            for i in Yuefenlist:
                if (not YearSearch or YearSearch == YearNow) and int(i[1]) > mounthnow:
                    break
                else:
                    Month_data = []
                    Department_key = []
                    for j in mock_data1:
                        if j["Department"] != "Sub- Count" and j["Department"] != "Monthly Average":
                            Department_key.append(j["Department"])
                            Month_data.append(j[i[0]])
                    Monthdict = {
                        "name": i[0],
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": Month_data
                    }
                    Month.append(Monthdict)
            Summary["Department_key"] = Department_key

            # overtimeTable1
            # Search_Endperiod = request.POST.getlist("YearRange", [])
            # by Customer
            if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                overtimeerrormegGroupNum = []
                LeaveerrormegGroupNum = []
                for i in range(PersonalInfo.objects.all().values("Customer").distinct().count()):
                    heBingNum.append(6)
                if (int(YearNow) % 4) == 0:
                    if (int(YearNow) % 100) == 0:
                        if (int(YearNow) % 400) == 0:
                            # print("{0} 是闰年".format(YearNow))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearNow))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearNow))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearNow))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                # mounthlist = ["Jan", "Fer", "Mar", "Apr", "May", "Jun",
                #               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "monthSummary"]
                mounthnow = datetime.datetime.now().month
                for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
                    Department_Codechu = PersonalInfo.objects.filter(Customer=i[
                        "Customer"]).first().DepartmentCode[:7]
                    zaizhidic = {"Chu": i["Customer"], "Program": "人數"}
                    overtimedic = {"Chu": i["Customer"], "Program": "加班時數"}
                    leavedic = {"Chu": i["Customer"], "Program": "請假時數"}
                    overtimePdic = {"Chu": i["Customer"], "Program": "平均加班(A)"}
                    leavePdic = {"Chu": i["Customer"], "Program": "平均請假(B)"}
                    effectivePdic = {"Chu": i["Customer"], "Program": "有效加班\n(C=A-B)"}

                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            # zaizhidic
                            DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                       RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                                Customer=i["Customer"], QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            # overtimedic
                            overtimedic[j[0]] = WorkOvertime.objects.filter(Year=YearNow,
                                                                            Department_Code__contains=Department_Codechu,
                                                                            Mounth=j[1].split("-")[1]).aggregate(
                                Sum("Total"))["Total__sum"]
                            if not overtimedic[j[0]]:
                                overtimedic[j[0]] = 0.00
                            # WorkOvertimeQuerySet = WorkOvertime.objects.filter(Year=YearNow,
                            #                                                    Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # overtimedicAll = WorkOvertimeQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # overtimedic[j[0]] = 0.0
                            # for n in overtimedicAll:
                            #     if PersonalInfo.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                    Year=YearNow).first().Customer == i[
                            #         "Customer"]:
                            #         overtimedic[j[0]] = n["Total__sum"]

                            # leavedic
                            leavedic[j[0]] = LeaveInfo.objects.filter(Year=YearNow,
                                                                      Department_Code__contains=Department_Codechu,
                                                                      Mounth=j[1].split("-")[1]).aggregate(
                                Sum("Total"))["Total__sum"]
                            if not leavedic[j[0]]:
                                leavedic[j[0]] = 0.00
                            # LeaveInfoQuerySet = LeaveInfo.objects.filter(Year=YearNow,
                            #                                              Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # leavedicAll = LeaveInfoQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # leavedic[j[0]] = 0.0
                            # for n in leavedicAll:
                            #     if PersonalInfo.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                    Year=YearNow).first().Customer == i["Customer"]:
                            #         leavedic[j[0]] = n["Total__sum"]
                            # overtimePdic
                            overtimePdic[j[0]] = round(overtimedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # leavePdic
                            leavePdic[j[0]] = round(leavedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # effectivePdic
                            effectivePdic[j[0]] = overtimePdic[j[0]] - leavePdic[j[0]]
                        mounthnum += 1
                    overtimeTable1.append(zaizhidic)
                    overtimeTable1.append(overtimedic)
                    overtimeTable1.append(leavedic)
                    overtimeTable1.append(overtimePdic)
                    overtimeTable1.append(leavePdic)
                    overtimeTable1.append(effectivePdic)

        if request.POST.get("isGetData") == "SEARCH1":
            YearSearch = request.POST.get("Date")
            Department_Code = request.POST.get("Department_Code")
            YearNow = str(datetime.datetime.now().year)
            # print(YearSearch)

            # Month
            if not YearSearch or YearSearch == YearNow:
                mounthnow = datetime.datetime.now().month
                # for i in Departments.objects.filter(Year=YearNow, BU__isnull=True, KE__isnull=True):
                #     print(i)
                Yuefenlist = [("Jan", "1"), ("Feb", "2"), ("Mar", "3"), ("Apr", "4"), ("May", "5"), ("Jun", "6"),
                              ("Jul", "7"), ("Aug", "8"), ("Sep", "9"), ("Oct", "10"), ("Nov", "11"), ("Dec", "12")]
                for i in Departments.objects.filter(Year=YearNow, BU__isnull=False, KE__isnull=True):
                    mock_data1_dict = {
                        #            "Department": "KF0MAQAA00(DQA1 五部)", "QM": "謝信福", "IDL_Sum": "65", "Jan": "43.45", "Feb": "0.41",
                        # "Mar": "23.93", "Apr": "60.07",
                        # "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
                        # "Year_Average": "31.97"
                    }
                    mock_data1_dict["Department"] = i.Department_Code + "(" + i.CHU + i.BU + ")"
                    mock_data1_dict["QM"] = PersonalInfo.objects.filter(GroupNum=i.Manager).first().CNName
                    # print(mock_data1_dict["QM"])
                    IDL_Sum = 0
                    Yuefen = {"Jan": 0, "Feb": 0,
                              "Mar": 0, "Apr": 0,
                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
                    for j in Departments.objects.filter(Year=YearNow, CHU=i.CHU, BU=i.BU,
                                                        KE__isnull=False):  # 每个部下面的课的部门代码
                        # print(i.Department_Code, j)
                        # 每个课下的除了课长的所有人
                        # IDL_Sum += PersonalInfo.objects.filter(DepartmentCode=j).exclude(
                        #     PositionNow__in=["6_2_Other", "6_2_ZG", "6_1_Other", "6_1_ZG"]).count()
                        IDL_Sum += PersonalInfo.objects.filter(DepartmentCode=j).count()
                        mounthnum = 1
                        for k in Yuefenlist:
                            if mounthnum > mounthnow:
                                break
                            else:
                                # 加班时数
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Peacetime"))["Peacetime__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("Peacetime"))["Peacetime__sum"]
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("PeriodHoliday"))["PeriodHoliday__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("PeriodHoliday"))["PeriodHoliday__sum"]
                                if WorkOvertime.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("NationalHoliday"))["NationalHoliday__sum"]:
                                    Yuefen[k[0]] += \
                                        WorkOvertime.objects.filter(Year=YearNow, Department_Code=j,
                                                                    Mounth=k[1]).aggregate(
                                            Sum("NationalHoliday"))["NationalHoliday__sum"]
                                # 请假时数，除了产假,方式一
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PublicHoliday"))["PublicHoliday__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PublicHoliday"))["PublicHoliday__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("WorkInjury"))["WorkInjury__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("WorkInjury"))["WorkInjury__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Matters"))["Matters__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Matters"))["Matters__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("MattersContinuation"))["MattersContinuation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("MattersContinuation"))["MattersContinuation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Sick"))["Sick__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Sick"))["Sick__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("SickContinuation"))["SickContinuation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("SickContinuation"))["SickContinuation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Marriage"))["Marriage__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Marriage"))["Marriage__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Bereavement"))["Bereavement__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Bereavement"))["Bereavement__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Special"))["Special__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Special"))["Special__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("OffDuty"))["OffDuty__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("OffDuty"))["OffDuty__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Compensatory"))["Compensatory__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Compensatory"))["Compensatory__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("NoScheduling"))["NoScheduling__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("NoScheduling"))["NoScheduling__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PaternityLeave"))["PaternityLeave__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PaternityLeave"))["PaternityLeave__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Absenteeism"))["Absenteeism__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Absenteeism"))["Absenteeism__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Lactation"))["Lactation__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Lactation"))["Lactation__sum"]
                                # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Others"))["Others__sum"]:
                                #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                #     Sum("Others"))["Others__sum"]
                                # 请假时数，除了产假,方式2
                                if LeaveInfo.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Total"))["Total__sum"]:
                                    Yuefen[k[0]] -= \
                                        LeaveInfo.objects.filter(Year=YearNow, Department_Code=j,
                                                                 Mounth=k[1]).aggregate(
                                            Sum("Total"))["Total__sum"]
                                if LeaveInfo.objects.filter(Year=YearNow, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Maternity"))["Maternity__sum"]:
                                    Yuefen[k[0]] += \
                                        LeaveInfo.objects.filter(Year=YearNow, Department_Code=j,
                                                                 Mounth=k[1]).aggregate(
                                            Sum("Maternity"))["Maternity__sum"]
                            mounthnum += 1

                    mock_data1_dict["IDL_Sum"] = IDL_Sum
                    mock_data1_dict["Jan"] = Yuefen["Jan"]
                    mock_data1_dict["Feb"] = Yuefen["Feb"]
                    mock_data1_dict["Mar"] = Yuefen["Mar"]
                    mock_data1_dict["Apr"] = Yuefen["Apr"]
                    mock_data1_dict["May"] = Yuefen["May"]
                    mock_data1_dict["Jun"] = Yuefen["Jun"]
                    mock_data1_dict["Jul"] = Yuefen["Jul"]
                    mock_data1_dict["Aug"] = Yuefen["Aug"]
                    mock_data1_dict["Sep"] = Yuefen["Sep"]
                    mock_data1_dict["Oct"] = Yuefen["Oct"]
                    mock_data1_dict["Nov"] = Yuefen["Nov"]
                    mock_data1_dict["Dec"] = Yuefen["Dec"]
                    mock_data1_dict["Year_Sum"] = Yuefen["Jan"] + Yuefen["Feb"] + Yuefen["Mar"] + Yuefen["Apr"] + \
                                                  Yuefen["May"] + Yuefen["Jun"] + \
                                                  Yuefen["Jul"] + Yuefen["Aug"] + Yuefen["Sep"] + Yuefen["Oct"] + \
                                                  Yuefen["Nov"] + Yuefen["Dec"]
                    mock_data1_dict["Year_Average"] = round(mock_data1_dict["Year_Sum"] / mounthnow, 2)
                    mock_data1.append(mock_data1_dict)
                SubCount = 0
                Monthly_Average = 0
                Bunum = 0
                mock_data1_SubCount = {"Department": "Sub- Count", "QM": "", "IDL_Sum": 0, "Jan": 0, "Feb": 0, "Mar": 0,
                                       "Apr": 0,
                                       "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0,
                                       "Year_Sum": 0, "Year_Average": 0}
                mock_data1_Monthly_Average = {"Department": "Monthly Average", "QM": "", "Jan": 0, "Feb": 0, "Mar": 0,
                                              "Apr": 0,
                                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0,
                                              "Dec": 0, }
                for i in mock_data1:
                    Bunum += 1
                    mock_data1_SubCount["IDL_Sum"] += i["IDL_Sum"]
                    mock_data1_SubCount["Jan"] += i["Jan"]
                    mock_data1_SubCount["Feb"] += i["Feb"]
                    mock_data1_SubCount["Mar"] += i["Mar"]
                    mock_data1_SubCount["Apr"] += i["Apr"]
                    mock_data1_SubCount["May"] += i["May"]
                    mock_data1_SubCount["Jun"] += i["Jun"]
                    mock_data1_SubCount["Jul"] += i["Jul"]
                    mock_data1_SubCount["Aug"] += i["Aug"]
                    mock_data1_SubCount["Sep"] += i["Sep"]
                    mock_data1_SubCount["Oct"] += i["Oct"]
                    mock_data1_SubCount["Nov"] += i["Nov"]
                    mock_data1_SubCount["Dec"] += i["Dec"]
                    mock_data1_SubCount["Year_Sum"] += i["Year_Sum"]
                mock_data1_SubCount["Year_Average"] += round(mock_data1_SubCount["Year_Sum"] / mounthnow, 2)
                mock_data1.append(mock_data1_SubCount)
                if Bunum:
                    mock_data1_Monthly_Average["Jan"] = round(mock_data1_SubCount["Jan"] / Bunum, 2)
                    mock_data1_Monthly_Average["Feb"] = round(mock_data1_SubCount["Feb"] / Bunum, 2)
                    mock_data1_Monthly_Average["Mar"] = round(mock_data1_SubCount["Mar"] / Bunum, 2)
                    mock_data1_Monthly_Average["Apr"] = round(mock_data1_SubCount["Apr"] / Bunum, 2)
                    mock_data1_Monthly_Average["May"] = round(mock_data1_SubCount["May"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jun"] = round(mock_data1_SubCount["Jun"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jul"] = round(mock_data1_SubCount["Jul"] / Bunum, 2)
                    mock_data1_Monthly_Average["Aug"] = round(mock_data1_SubCount["Aug"] / Bunum, 2)
                    mock_data1_Monthly_Average["Sep"] = round(mock_data1_SubCount["Sep"] / Bunum, 2)
                    mock_data1_Monthly_Average["Oct"] = round(mock_data1_SubCount["Oct"] / Bunum, 2)
                    mock_data1_Monthly_Average["Nov"] = round(mock_data1_SubCount["Nov"] / Bunum, 2)
                    mock_data1_Monthly_Average["Dec"] = round(mock_data1_SubCount["Dec"] / Bunum, 2)
                mock_data1.append(mock_data1_Monthly_Average)

                for i in mock_data1:
                    for j in Yuefenlist:
                        if int(j[1]) > mounthnow:
                            # print(j[0])
                            i[j[0]] = ''
            else:
                # for i in Departments.objects.filter(Q(Year=YearSearch)& Q(BU=None)&Q(KE=None)):
                # for i in Departments.objects.filter(Year=YearSearch, BU=None, KE=None):
                # for i in Departments.objects.filter(Year=YearSearch, BU__isnull=True, KE__isnull=True):
                #     print(i)

                Yuefenlist = [("Jan", "1"), ("Feb", "2"), ("Mar", "3"), ("Apr", "4"), ("May", "5"), ("Jun", "6"),
                              ("Jul", "7"), ("Aug", "8"), ("Sep", "9"), ("Oct", "10"), ("Nov", "11"), ("Dec", "12")]
                for i in Departments.objects.filter(Year=YearSearch, BU__isnull=False, KE__isnull=True):
                    mock_data1_dict = {
                        #            "Department": "KF0MAQAA00(DQA1 五部)", "QM": "謝信福", "IDL_Sum": "65", "Jan": "43.45", "Feb": "0.41",
                        # "Mar": "23.93", "Apr": "60.07",
                        # "May": "", "Jun": "", "Jul": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": "", "Year_Sum": "127.86",
                        # "Year_Average": "31.97"
                    }
                    mock_data1_dict["Department"] = i.Department_Code + "(" + i.CHU + i.BU + ")"
                    mock_data1_dict["QM"] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                 GroupNum=i.Manager).first().CNName if PersonalInfoHisByYear.objects.filter(
                        Year=YearSearch, GroupNum=i.Manager).first() else "該年份人員信心缺少該QM信息"
                    # print(mock_data1_dict["QM"])
                    IDL_Sum = 0
                    Yuefen = {"Jan": 0, "Feb": 0,
                              "Mar": 0, "Apr": 0,
                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0}
                    for j in Departments.objects.filter(Year=YearSearch, CHU=i.CHU, BU=i.BU,
                                                        KE__isnull=False):  # 每个部下面的课的部门代码
                        # print(i.Department_Code, j)
                        # 每个课下的除了课长的所有人
                        # IDL_Sum += PersonalInfoHisByYear.objects.filter(Year=YearSearch, DepartmentCode=j).exclude(PositionNow__in=["6_2_Other", "6_2_ZG", "6_1_Other", "6_1_ZG"]).count()
                        IDL_Sum += PersonalInfoHisByYear.objects.filter(Year=YearSearch, DepartmentCode=j).count()
                        for k in Yuefenlist:
                            # 加班时数
                            if WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                    Sum("Peacetime"))["Peacetime__sum"]:
                                Yuefen[k[0]] += \
                                    WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j,
                                                                Mounth=k[1]).aggregate(
                                        Sum("Peacetime"))["Peacetime__sum"]
                            if WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                    Sum("PeriodHoliday"))["PeriodHoliday__sum"]:
                                Yuefen[k[0]] += \
                                    WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j,
                                                                Mounth=k[1]).aggregate(
                                        Sum("PeriodHoliday"))["PeriodHoliday__sum"]
                            if WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                    Sum("NationalHoliday"))["NationalHoliday__sum"]:
                                Yuefen[k[0]] += \
                                    WorkOvertime.objects.filter(Year=YearSearch, Department_Code=j,
                                                                Mounth=k[1]).aggregate(
                                        Sum("NationalHoliday"))["NationalHoliday__sum"]
                            # 请假时数，除了产假,方式一
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PublicHoliday"))["PublicHoliday__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PublicHoliday"))["PublicHoliday__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("WorkInjury"))["WorkInjury__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("WorkInjury"))["WorkInjury__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Matters"))["Matters__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Matters"))["Matters__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("MattersContinuation"))["MattersContinuation__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("MattersContinuation"))["MattersContinuation__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Sick"))["Sick__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Sick"))["Sick__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("SickContinuation"))["SickContinuation__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("SickContinuation"))["SickContinuation__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Marriage"))["Marriage__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Marriage"))["Marriage__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Bereavement"))["Bereavement__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Bereavement"))["Bereavement__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Special"))["Special__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Special"))["Special__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("OffDuty"))["OffDuty__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("OffDuty"))["OffDuty__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Compensatory"))["Compensatory__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Compensatory"))["Compensatory__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("EpidemicPrevention"))["EpidemicPrevention__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("NoScheduling"))["NoScheduling__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("NoScheduling"))["NoScheduling__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PaternityLeave"))["PaternityLeave__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PaternityLeave"))["PaternityLeave__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Absenteeism"))["Absenteeism__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Absenteeism"))["Absenteeism__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("PregnancyExamination"))["PregnancyExamination__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Lactation"))["Lactation__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Lactation"))["Lactation__sum"]
                            # if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Others"))["Others__sum"]:
                            #     Yuefen[k[0]] -= LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                            #     Sum("Others"))["Others__sum"]
                            # 请假时数，除了产假,方式2
                            if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                    Sum("Total"))["Total__sum"]:
                                Yuefen[k[0]] -= \
                                    LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Total"))["Total__sum"]
                            if LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                    Sum("Maternity"))["Maternity__sum"]:
                                Yuefen[k[0]] += \
                                    LeaveInfo.objects.filter(Year=YearSearch, Department_Code=j, Mounth=k[1]).aggregate(
                                        Sum("Maternity"))["Maternity__sum"]

                    mock_data1_dict["IDL_Sum"] = IDL_Sum
                    mock_data1_dict["Jan"] = Yuefen["Jan"]
                    mock_data1_dict["Feb"] = Yuefen["Feb"]
                    mock_data1_dict["Mar"] = Yuefen["Mar"]
                    mock_data1_dict["Apr"] = Yuefen["Apr"]
                    mock_data1_dict["May"] = Yuefen["May"]
                    mock_data1_dict["Jun"] = Yuefen["Jun"]
                    mock_data1_dict["Jul"] = Yuefen["Jul"]
                    mock_data1_dict["Aug"] = Yuefen["Aug"]
                    mock_data1_dict["Sep"] = Yuefen["Sep"]
                    mock_data1_dict["Oct"] = Yuefen["Oct"]
                    mock_data1_dict["Nov"] = Yuefen["Nov"]
                    mock_data1_dict["Dec"] = Yuefen["Dec"]
                    mock_data1_dict["Year_Sum"] = Yuefen["Jan"] + Yuefen["Feb"] + Yuefen["Mar"] + Yuefen["Apr"] + \
                                                  Yuefen["May"] + Yuefen["Jun"] + \
                                                  Yuefen["Jul"] + Yuefen["Aug"] + Yuefen["Sep"] + Yuefen["Oct"] + \
                                                  Yuefen["Nov"] + Yuefen["Dec"]
                    mock_data1_dict["Year_Average"] = round(mock_data1_dict["Year_Sum"] / 12, 2)
                    mock_data1.append(mock_data1_dict)
                SubCount = 0
                Monthly_Average = 0
                Bunum = 0
                mock_data1_SubCount = {"Department": "Sub- Count", "QM": "", "IDL_Sum": 0, "Jan": 0, "Feb": 0, "Mar": 0,
                                       "Apr": 0,
                                       "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0, "Dec": 0,
                                       "Year_Sum": 0, "Year_Average": 0}
                mock_data1_Monthly_Average = {"Department": "Monthly Average", "QM": "", "Jan": 0, "Feb": 0, "Mar": 0,
                                              "Apr": 0,
                                              "May": 0, "Jun": 0, "Jul": 0, "Aug": 0, "Sep": 0, "Oct": 0, "Nov": 0,
                                              "Dec": 0, }
                for i in mock_data1:
                    Bunum += 1
                    mock_data1_SubCount["IDL_Sum"] += i["IDL_Sum"]
                    mock_data1_SubCount["Jan"] += i["Jan"]
                    mock_data1_SubCount["Feb"] += i["Feb"]
                    mock_data1_SubCount["Mar"] += i["Mar"]
                    mock_data1_SubCount["Apr"] += i["Apr"]
                    mock_data1_SubCount["May"] += i["May"]
                    mock_data1_SubCount["Jun"] += i["Jun"]
                    mock_data1_SubCount["Jul"] += i["Jul"]
                    mock_data1_SubCount["Aug"] += i["Aug"]
                    mock_data1_SubCount["Sep"] += i["Sep"]
                    mock_data1_SubCount["Oct"] += i["Oct"]
                    mock_data1_SubCount["Nov"] += i["Nov"]
                    mock_data1_SubCount["Dec"] += i["Dec"]
                    mock_data1_SubCount["Year_Sum"] += i["Year_Sum"]
                mock_data1_SubCount["Year_Average"] += round(mock_data1_SubCount["Year_Sum"] / 12, 2)
                mock_data1.append(mock_data1_SubCount)
                if Bunum:
                    mock_data1_Monthly_Average["Jan"] = round(mock_data1_SubCount["Jan"] / Bunum, 2)
                    mock_data1_Monthly_Average["Feb"] = round(mock_data1_SubCount["Feb"] / Bunum, 2)
                    mock_data1_Monthly_Average["Mar"] = round(mock_data1_SubCount["Mar"] / Bunum, 2)
                    mock_data1_Monthly_Average["Apr"] = round(mock_data1_SubCount["Apr"] / Bunum, 2)
                    mock_data1_Monthly_Average["May"] = round(mock_data1_SubCount["May"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jun"] = round(mock_data1_SubCount["Jun"] / Bunum, 2)
                    mock_data1_Monthly_Average["Jul"] = round(mock_data1_SubCount["Jul"] / Bunum, 2)
                    mock_data1_Monthly_Average["Aug"] = round(mock_data1_SubCount["Aug"] / Bunum, 2)
                    mock_data1_Monthly_Average["Sep"] = round(mock_data1_SubCount["Sep"] / Bunum, 2)
                    mock_data1_Monthly_Average["Oct"] = round(mock_data1_SubCount["Oct"] / Bunum, 2)
                    mock_data1_Monthly_Average["Nov"] = round(mock_data1_SubCount["Nov"] / Bunum, 2)
                    mock_data1_Monthly_Average["Dec"] = round(mock_data1_SubCount["Dec"] / Bunum, 2)
                mock_data1.append(mock_data1_Monthly_Average)
            Yuefenlist = [("Jan", "1"), ("Feb", "2"), ("Mar", "3"), ("Apr", "4"), ("May", "5"),
                          ("Jun", "6"),
                          ("Jul", "7"), ("Aug", "8"), ("Sep", "9"), ("Oct", "10"), ("Nov", "11"),
                          ("Dec", "12")]
            mounthnow = datetime.datetime.now().month
            for i in Yuefenlist:
                if (not YearSearch or YearSearch == YearNow) and int(i[1]) > mounthnow:
                    break
                else:
                    Month_data = []
                    Department_key = []
                    for j in mock_data1:
                        if j["Department"] != "Sub- Count" and j["Department"] != "Monthly Average":
                            Department_key.append(j["Department"])
                            Month_data.append(j[i[0]])
                    Monthdict = {
                        "name": i[0],
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": Month_data
                    }
                    Month.append(Monthdict)
            Summary["Department_key"] = Department_key

            # overtimeTable1
            # Search_Endperiod = request.POST.getlist("YearRange", [])
            # by Customer
            if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                overtimeerrormegGroupNum = []
                LeaveerrormegGroupNum = []
                for i in range(PersonalInfo.objects.all().values("Customer").distinct().count()):
                    heBingNum.append(6)
                if (int(YearNow) % 4) == 0:
                    if (int(YearNow) % 100) == 0:
                        if (int(YearNow) % 400) == 0:
                            # print("{0} 是闰年".format(YearNow))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearNow))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearNow))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearNow))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                # mounthlist = ["Jan", "Fer", "Mar", "Apr", "May", "Jun",
                #               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "monthSummary"]
                mounthnow = datetime.datetime.now().month
                for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
                    Department_Codechu = PersonalInfo.objects.filter(Customer=i[
                        "Customer"]).first().DepartmentCode[:7]
                    zaizhidic = {"Chu": i["Customer"], "Program": "人數"}
                    overtimedic = {"Chu": i["Customer"], "Program": "加班時數"}
                    leavedic = {"Chu": i["Customer"], "Program": "請假時數"}
                    overtimePdic = {"Chu": i["Customer"], "Program": "平均加班(A)"}
                    leavePdic = {"Chu": i["Customer"], "Program": "平均請假(B)"}
                    effectivePdic = {"Chu": i["Customer"], "Program": "有效加班\n(C=A-B)"}

                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            # zaizhidic
                            DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                       RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                                Customer=i["Customer"], QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            # overtimedic

                            overtimedic[j[0]] = 0.00
                            if WorkOvertime.objects.filter(Year=YearNow,
                                                           Department_Code__contains=Department_Codechu,
                                                           Mounth=j[1].split("-")[1]).first():
                                overtimedic[j[0]] = WorkOvertime.objects.filter(Year=YearNow,
                                                                                Department_Code__contains=Department_Codechu,
                                                                                Mounth=j[1].split("-")[1]).aggregate(
                                    Sum("Total"))["Total__sum"]

                            # WorkOvertimeQuerySet = WorkOvertime.objects.filter(Year=YearNow,
                            #                                                    Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # overtimedicAll = WorkOvertimeQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # overtimedic[j[0]] = 0.0
                            # for n in overtimedicAll:
                            #     if PersonalInfo.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                    Year=YearNow).first().Customer == i[
                            #         "Customer"]:
                            #         overtimedic[j[0]] = n["Total__sum"]

                            # leavedic

                            leavedic[j[0]] = 0.00
                            if LeaveInfo.objects.filter(Year=YearNow,
                                                        Department_Code__contains=Department_Codechu,
                                                        Mounth=j[1].split("-")[1]).first():
                                leavedic[j[0]] = LeaveInfo.objects.filter(Year=YearNow,
                                                                          Department_Code__contains=Department_Codechu,
                                                                          Mounth=j[1].split("-")[1]).aggregate(
                                    Sum("Total"))["Total__sum"]

                            # LeaveInfoQuerySet = LeaveInfo.objects.filter(Year=YearNow,
                            #                                              Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # leavedicAll = LeaveInfoQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # leavedic[j[0]] = 0.0
                            # for n in leavedicAll:
                            #     if PersonalInfo.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                    Year=YearNow).first().Customer == i["Customer"]:
                            #         leavedic[j[0]] = n["Total__sum"]
                            # overtimePdic
                            overtimePdic[j[0]] = round(overtimedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # leavePdic
                            leavePdic[j[0]] = round(leavedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # effectivePdic
                            effectivePdic[j[0]] = overtimePdic[j[0]] - leavePdic[j[0]]
                        mounthnum += 1
                    overtimeTable1.append(zaizhidic)
                    overtimeTable1.append(overtimedic)
                    overtimeTable1.append(leavedic)
                    overtimeTable1.append(overtimePdic)
                    overtimeTable1.append(leavePdic)
                    overtimeTable1.append(effectivePdic)
            else:
                for i in range(
                        PersonalInfoHisByYear.objects.filter(Year=YearSearch).values("Customer").distinct().count()):
                    heBingNum.append(6)
                if (int(YearSearch) % 4) == 0:
                    if (int(YearSearch) % 100) == 0:
                        if (int(YearSearch) % 400) == 0:
                            # print("{0} 是闰年".format(YearSearch))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearSearch))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearSearch))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearSearch))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                mounthnow = 12  # datetime.datetime.now().month
                overtimeerrormegGroupNum = []
                LeaveerrormegGroupNum = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch).values("Customer").distinct().order_by(
                        "Customer"):
                    Department_Codechu = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Customer=i[
                        "Customer"]).first().DepartmentCode[:7]
                    # print(Department_Codechu)
                    zaizhidic = {"Chu": i["Customer"], "Program": "人數"}
                    overtimedic = {"Chu": i["Customer"], "Program": "加班時數"}
                    leavedic = {"Chu": i["Customer"], "Program": "請假時數"}
                    overtimePdic = {"Chu": i["Customer"], "Program": "平均加班(A)"}
                    leavePdic = {"Chu": i["Customer"], "Program": "平均請假(B)"}
                    effectivePdic = {"Chu": i["Customer"], "Program": "有效加班\n(C=A-B)"}
                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            # zaizhidic
                            DateNow_begin = datetime.datetime.strptime(YearSearch + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearSearch + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"], Year=YearSearch,
                                                                                RegistrationDate__lte=DateNow).count() - PersonalInfoHisByYear.objects.filter(
                                Customer=i["Customer"], Year=YearSearch, QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            # overtimedic

                            overtimedic[j[0]] = 0.00
                            if WorkOvertime.objects.filter(Year=YearSearch,
                                                           Department_Code__contains=Department_Codechu,
                                                           Mounth=j[1].split("-")[1]).first():
                                overtimedic[j[0]] = WorkOvertime.objects.filter(Year=YearSearch,
                                                                                Department_Code__contains=Department_Codechu,
                                                                                Mounth=j[1].split("-")[1]).aggregate(
                                    Sum("Total"))["Total__sum"]

                            # print(overtimedic[j[0]], 'yyy')
                            # WorkOvertimeQuerySet = WorkOvertime.objects.filter(Year=YearSearch,
                            #                                                    Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # overtimedicAll = WorkOvertimeQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # overtimedic[j[0]] = 0.0
                            # for n in overtimedicAll:
                            #     if PersonalInfoHisByYear.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                             Year=YearSearch).first().Customer == i[
                            #         "Customer"]:
                            #         overtimedic[j[0]] = n["Total__sum"]
                            # print(overtimedic[j[0]])

                            # leavedic

                            leavedic[j[0]] = 0.00
                            if LeaveInfo.objects.filter(Year=YearSearch,
                                                        Department_Code__contains=Department_Codechu,
                                                        Mounth=j[1].split("-")[1]).first():
                                leavedic[j[0]] = LeaveInfo.objects.filter(Year=YearSearch,
                                                                          Department_Code__contains=Department_Codechu,
                                                                          Mounth=j[1].split("-")[1]).aggregate(
                                    Sum("Total"))["Total__sum"]

                            # LeaveInfoQuerySet = LeaveInfo.objects.filter(Year=YearSearch,
                            #                                              Mounth=j[1].split("-")[1]).annotate(
                            #     chuinfo=Substr("Department_Code", 1, 7))
                            # leavedicAll = LeaveInfoQuerySet.values("chuinfo").annotate(Sum(
                            #     "Total"))  # queryset增加字段二次运用时，无法保存下来，用的是原始的数据？annotate，就像filter一样，不改变查询集但是返回一个新的查询集。你需要重新分配
                            # leavedic[j[0]] = 0.0
                            # for n in leavedicAll:
                            #     if PersonalInfoHisByYear.objects.filter(DepartmentCode__contains=n["chuinfo"],
                            #                                             Year=YearSearch).first().Customer == i[
                            #         "Customer"]:
                            #         leavedic[j[0]] = n["Total__sum"]

                            # overtimePdic
                            overtimePdic[j[0]] = round(overtimedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # leavePdic
                            leavePdic[j[0]] = round(leavedic[j[0]] / zaizhimounth, 2) if zaizhimounth else 0.00
                            # effectivePdic
                            effectivePdic[j[0]] = round(overtimePdic[j[0]] - leavePdic[j[0]], 2)
                        mounthnum += 1
                    # print(overtimeerrormegGroupNum)
                    # print(LeaveerrormegGroupNum)
                    overtimeTable1.append(zaizhidic)
                    overtimeTable1.append(overtimedic)
                    overtimeTable1.append(leavedic)
                    overtimeTable1.append(overtimePdic)
                    overtimeTable1.append(leavePdic)
                    overtimeTable1.append(effectivePdic)

        mounthname = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", ]
        for i in overtimeTable1:
            monthDiagram1Data_data = []
            monthDiagram2Data_data = []
            monthDiagram3Data_data = []
            if i["Program"] == "平均加班(A)":
                for j in mounthname:
                    if j in i.keys():
                        monthDiagram1Data_data.append(i[j])
                    else:
                        monthDiagram1Data_data.append(0)
                monthDiagram1Data.append(
                    {
                        'name': i["Chu"],
                        'type': 'line',
                        # 'stack': 'Total',#堆叠数据累加
                        'data': monthDiagram1Data_data,  # 對應月份 從一月到十二月
                        'label': {
                            'show': 'true',
                            'position': 'top'
                        },
                    }
                )
            if i["Program"] == "平均請假(B)":
                for j in mounthname:
                    if j in i.keys():
                        monthDiagram2Data_data.append(i[j])
                    else:
                        monthDiagram2Data_data.append(0)
                monthDiagram2Data.append(
                    {
                        'name': i["Chu"],
                        'type': 'line',
                        # 'stack': 'Total',#堆叠数据累加
                        'data': monthDiagram2Data_data,  # 對應月份 從一月到十二月
                        'label': {
                            'show': 'true',
                            'position': 'top'
                        },
                    }
                )
            if i["Program"] == "有效加班\n(C=A-B)":
                for j in mounthname:
                    if j in i.keys():
                        monthDiagram3Data_data.append(i[j])
                    else:
                        monthDiagram3Data_data.append(0)
                monthDiagram3Data.append(
                    {
                        'name': i["Chu"],
                        'type': 'line',
                        # 'stack': 'Total',#堆叠数据累加
                        'data': monthDiagram3Data_data,  # 對應月份 從一月到十二月
                        'label': {
                            'show': 'true',
                            'position': 'top'
                        },
                    }
                )
        monthDiagramA31Data = [
            # {
            #     'name': '平均加班',
            #     'type': 'bar',
            #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
            # },
            # {
            #     'name': '平均請假',
            #     'type': 'bar',
            #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
            # },

        ]
        for i in monthDiagram1Data:
            if i['name'] == 'A31':
                monthDiagramA31Data.append(
                    {
                        'name': '平均加班',
                        'type': 'line',
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )
            elif i['name'] == 'A32':
                monthDiagramA32Data.append(
                    {
                        'name': '平均加班',
                        'type': 'line',
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )
            elif i['name'] == 'C38':
                monthDiagramC38Data.append(
                    {
                        'name': '平均加班',
                        'type': 'line',
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )
        for i in monthDiagram2Data:
            if i['name'] == 'A31':
                monthDiagramA31Data.append(
                    {
                        'name': '平均請假',
                        'type': 'line',
                        'yAxisIndex': 1,
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )
            elif i['name'] == 'A32':
                monthDiagramA32Data.append(
                    {
                        'name': '平均請假',
                        'type': 'line',
                        'yAxisIndex': 1,
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )
            elif i['name'] == 'C38':
                monthDiagramC38Data.append(
                    {
                        'name': '平均請假',
                        'type': 'line',
                        'yAxisIndex': 1,
                        'data': i['data']  # 對應月份 從一月到十二月
                    },
                )

        data = {
            "err_ok": "0",
            "content1": mock_data1,
            "overtimeTable1": overtimeTable1,
            "heBingNum": heBingNum,
            "content2": mock_data2,
            "select": selectItem,
            "Month": Month,
            "Month_Singal": Month_Singal,
            "Summary": Summary,
            "monthDiagram1Data": monthDiagram1Data,
            "monthDiagram2Data": monthDiagram2Data,
            "monthDiagram3Data": monthDiagram3Data,
            "monthDiagramA31Data": monthDiagramA31Data,
            "monthDiagramA32Data": monthDiagramA32Data,
            "monthDiagramC38Data": monthDiagramC38Data,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'PersonalInfo/Summary1.html', locals())


@csrf_exempt
def Summary2(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/Summary2"
    monthTable = [
        # {"Customer": "A31", "Classify": "預算", "Jan": "244", "Feb": "240", "Mar": "236", "Apr": "232", "May": "229",
        #  "Jun": "226", "Jul": "283", "Aug": "280", "Sep": "277", "Oct": "274", "Nov": "271", "Dec": "268",
        #  "monthSummary": "3060"},
        # {"Customer": "A31", "Classify": "在職", "Jan": "229", "Feb": "228", "Mar": "221", "Apr": "216", "May": "208",
        #  "Jun": "205", "Jul": "230", "Aug": "216", "Sep": "209", "Oct": "217", "Nov": "223", "Dec": "230",
        #  "monthSummary": ""},
        # {"Customer": "A31", "Classify": "離職", "Jan": "8", "Feb": "2", "Mar": "8", "Apr": "5", "May": "9", "Jun": "5",
        #  "Jul": "12", "Aug": "14", "Sep": "8", "Oct": "6", "Nov": "2", "Dec": "3", "monthSummary": ""},
        # {"Customer": "A31", "Classify": "離職率", "Jan": "3.49%", "Feb": "0.88%", "Mar": "3.62%", "Apr": "%", "May": "%",
        #  "Jun": "%", "Jul": "%", "Aug": "%", "Sep": "%", "Oct": "%", "Nov": "%", "Dec": "%", "monthSummary": "%"},

    ]
    searchYear = YearNow = str(datetime.datetime.now().year)  # 初始化時月份表格中的動態年份標題 （如初始化時沒有默認數據則不需要）

    titleTable = [
        # {"Title": "助技員", "A31": "0", "A32": "64", "C38": "0", "titleSummary": "64"},
        #   {"Title": "技術員", "A31": "18", "A32": "30", "C38": "23", "titleSummary": "71"},
        #   {"Title": "助工師", "A31": "59", "A32": "83", "C38": "63", "titleSummary": "205"},
        #   {"Title": "工程師", "A31": "43", "A32": "35", "C38": "26", "titleSummary": "104"},
        #   {"Title": "資工師", "A31": "33", "A32": "34", "C38": "41", "titleSummary": "108"},
        #   {"Title": "副課長", "A31": "20", "A32": "19", "C38": "24", "titleSummary": "63"},
        #   {"Title": "課長", "A31": "25", "A32": "19", "C38": "25", "titleSummary": "69"},
        #   {"Title": "襄理", "A31": "2", "A32": "6", "C38": "4", "titleSummary": "12"},
        #   {"Title": "副理", "A31": "1", "A32": "1", "C38": "1", "titleSummary": "3"},
        #   {"Title": "經理", "A31": "1", "A32": "0", "C38": "2", "titleSummary": "3"},
        #   {"Title": "資深經理", "A31": "1", "A32": "0", "C38": "0", "titleSummary": "1"}
    ]

    seniorityTable = [
        # {"Seniority": "0.25年以下", "A31": "12", "A32": "54", "C38": "19", "senioritySummary": "85"},
        #   {"Seniority": "0.25~1年", "A31": "23", "A32": "99", "C38": "42", "senioritySummary": "164"},
        #   {"Seniority": "1~2年", "A31": "", "A32": "", "C38": "", "senioritySummary": ""},
        #   {"Seniority": "2~3年", "A31": "63", "A32": "58", "C38": "43", "senioritySummary": "164"},
        #   {"Seniority": "3~5年", "A31": "24", "A32": "8", "C38": "13", "senioritySummary": "45"},
        #   {"Seniority": "5~10年", "A31": "21", "A32": "23", "C38": "22", "senioritySummary": "66"},
        #   {"Seniority": "10~15年", "A31": "35", "A32": "25", "C38": "39", "senioritySummary": "99"},
        #   {"Seniority": "15~20年", "A31": "20", "A32": "22", "C38": "23", "senioritySummary": "65"},
        #   {"Seniority": "20年以上", "A31": "5", "A32": "2", "C38": "8", "senioritySummary": "15"}
    ]

    educationTable = [
        # {"Education": "本科", "A31": "149", "A32": "168", "C38": "178", "educationSummary": "495", "accountFor": ""},
        # {"Education": "大專", "A31": "53", "A32": "124", "C38": "28", "educationSummary": "205", "accountFor": ""},
        # {"Education": "中專", "A31": "1", "A32": "1", "C38": "0", "educationSummary": "2", "accountFor": ""}
    ]

    heBingNum = [
        # 3, 6
    ]
    professionTable = [
        # {"daLei": "S.T.E.M", "Profession": "電氣信息類", "A31": "12", "A32": "54", "C38": "19", "professionSummary": "85"},
    ]

    regionsTable = [
        # {"Regions": "江蘇", "A31": "12", "A32": "54", "C38": "19", "regionsSummary": "85"},
        # {"Regions": "安徽", "A31": "23", "A32": "99", "C38": "42", "regionsSummary": "164"},
        # {"Regions": "山東", "A31": "", "A32": "", "C38": "", "regionsSummary": ""},
        # {"Regions": "四川", "A31": "63", "A32": "58", "C38": "43", "regionsSummary": "164"},
        # {"Regions": "黑龍江", "A31": "24", "A32": "8", "C38": "13", "regionsSummary": "45"},
        # {"Regions": "山西", "A31": "21", "A32": "23", "C38": "22", "regionsSummary": "66"},
        # {"Regions": "河南", "A31": "35", "A32": "25", "C38": "39", "regionsSummary": "99"},
        # {"Regions": "陝西", "A31": "20", "A32": "22", "C38": "23", "regionsSummary": "65"},
        # {"Regions": "甘肅", "A31": "5", "A32": "2", "C38": "8", "regionsSummary": "15"}
    ]
    monthDiagram1Data = [
        # {
        #     'name': 'A31',
        #     'type': 'bar',
        #     'data': [229, 228, 221, 216, 208, 205, 230, 216, 209, 217, 223, 230]  # 對應月份 從一月到十二月
        # },
        # {
        #     'name': 'A32',
        #     'type': 'bar',
        #     'data': [189, 185, 194, 196, 195, 189, 196, 193, 192, 200, 205, 217]
        # },
        # {
        #     'name': 'C38',
        #     'type': 'bar',
        #     'data': [210, 209, 210, 203, 199, 194, 209, 203, 212, 214, 218, 220]
        # },
        # {
        #     'name': '預算',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [659, 682, 677, 678, 609, 572, 567, 575, 575, 577, 567, 628]
        # },
        # {
        #     'name': '在職',
        #     'type': 'line',
        #     'yAxisIndex': 1,
        #     'data': [628, 622, 625, 615, 602, 588, 635, 612, 613, 631, 646, 667]
        # }
    ]  # X轴是固定的1~12月
    monthDiagram2Data = {
        # 'LIZHI': [13, 7, 18, 19, 14, 17, 21, 28, 18, 12, 7, 8],  # 對應月份 從一月到十二月
        # 'LIZHILV': [0.0207006, 0.011254, 0.0288, 0.0308943, 0.0232558, 0.0289115, 0.0330708, 0.0457516, 0.0293637,
        #             0.0190174, 0.0108359, 0.011994]
    }

    titleDiagram = {
        # "legendData": ['DQA', 'A31', 'A32', 'C38'],  # 做圖表顏色表示用的
        # "titleDiagramname": ['助技員', '技術員', '助工師', '工程師', '資工師', '副課長', '課長', '襄理', '副理', '經理', '資深經理'],  # 圖表x軸數據
        # "titleDiagramData": [
        #     {
        #         'name': 'DQA',
        #         'type': 'bar',
        #         'data': [64, 71, 205, 104, 108, 63, 6912, 3, 3, 1]
        #     },
        #     {
        #         'name': 'A31',
        #         'type': 'bar',
        #         'data': [0, 18, 59, 43, 33, 20, 25, 2, 1, 1, 1]
        #     },
        #     {
        #         'name': 'A32',
        #         'type': 'bar',
        #         'data': [64, 30, 83, 35, 34, 19, 19, 6, 1, 0, 0]
        #     },
        #     {
        #         'name': 'C38',
        #         'type': 'bar',
        #         'data': [64, 30, 83, 35, 34, 19, 19, 6, 1, 0, 0]
        #     }]
    }
    seniorityDiagram = {
        # "legendData": ['DQA', 'A32'],#柱状图的顺序
        # "seniorityDiagramname": ['0.25年以下', '0.25~1年', '1~2年', '2~3年', '3~5年', '5~10年', '10~15年', "15~20年", '20年以上'],#X轴的顺序
        # "seniorityDiagramData": [
        #     {
        #         'name': 'DQA',
        #         'type': 'bar',
        #         'data': [85, 164, 164, 45, 66, 99, 65, 15, 2]
        #     },
        #     {
        #         'name': 'A32',
        #         'type': 'bar',
        #         'data': [54, 99, 58, 8, 23, 25, 22, 2, 1]
        #     }
        # ]
    }
    educationDiagram = {
        # "educationDiagramname": ['本科', '大專', '中專'],
        # "educationDiagramHE": [495, 205, 2],  # 對應 從本科到中專
        # "educationDiagramZH": [0.705128205, 0.292022792, 0.002849003]
    }
    selectItem = [
        # "A31", "A32", "C38"
    ]
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":

            YearNow = str(datetime.datetime.now().year)
            YearSearch = YearNow
            # By月份
            RunnYearflag = 0
            if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                if (int(YearNow) % 4) == 0:
                    if (int(YearNow) % 100) == 0:
                        if (int(YearNow) % 400) == 0:
                            # print("{0} 是闰年".format(YearNow))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearNow))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearNow))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearNow))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                # mounthlist = ["Jan", "Fer", "Mar", "Apr", "May", "Jun",
                #               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "monthSummary"]
                mounthnow = datetime.datetime.now().month
                for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
                    yusuandic = {"Customer": i["Customer"], "Classify": "預算"}
                    zaizhidic = {"Customer": i["Customer"], "Classify": "在職"}
                    ruzhidic = {"Customer": i["Customer"], "Classify": "入職"}
                    lizhidic = {"Customer": i["Customer"], "Classify": "離職"}
                    lizhilvdic = {"Customer": i["Customer"], "Classify": "離職率"}
                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            yusuandic[j[0]] = \
                                MainPower.objects.filter(Year=YearNow, Customer=i["Customer"]).aggregate(Sum(j[0]))[
                                    j[0] + "__sum"]
                            if not yusuandic[j[0]]:
                                yusuandic[j[0]] = 0
                            DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                       RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                                Customer=i["Customer"], QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            ruzhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                         RegistrationDate__range=Test_Endperiod).count()
                            # lizhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                            #                                              QuitDate__lte=DateNow).count()
                            lizhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                         QuitDate__range=Test_Endperiod).count()
                            if zaizhidic[j[0]]:
                                lizhilvdic[j[0]] = round(float(lizhidic[j[0]] / zaizhidic[j[0]]), 4)
                            else:
                                lizhilvdic[j[0]] = 0
                            lizhilvdic[j[0]] = '%.2f%%' % (lizhilvdic[j[0]] * 100)
                        mounthnum += 1
                    monthTable.append(yusuandic)
                    monthTable.append(zaizhidic)
                    monthTable.append(ruzhidic)
                    monthTable.append(lizhidic)
                    monthTable.append(lizhilvdic)
                # 合计
                totalyusuandic = {"Customer": "合計", "Classify": "預算"}
                totalzaizhidic = {"Customer": "合計", "Classify": "在職"}
                totalruzhidic = {"Customer": "合計", "Classify": "入職"}
                totallizhidic = {"Customer": "合計", "Classify": "離職"}
                totallizhilvdic = {"Customer": "合計", "Classify": "離職率"}
                mounthnum = 1
                for j in mounthlist:
                    if mounthnum > mounthnow:
                        break
                    else:
                        totalyusuandic[j[0]] = \
                            MainPower.objects.filter(Year=YearNow).aggregate(Sum(j[0]))[
                                j[0] + "__sum"]
                        if not totalyusuandic[j[0]]:
                            totalyusuandic[j[0]] = 0
                        DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                   '%Y-%m-%d')
                        # print(DateNow_begin)
                        DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                        Test_Endperiod = [DateNow_begin, DateNow]
                        zaizhimounth = PersonalInfo.objects.filter(
                            RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                            QuitDate__lte=DateNow).count()
                        totalzaizhidic[j[0]] = zaizhimounth
                        totalruzhidic[j[0]] = PersonalInfo.objects.filter(
                            RegistrationDate__range=Test_Endperiod).count()
                        # totallizhidic[j[0]] = PersonalInfo.objects.filter(
                        #     QuitDate__lte=DateNow).count()
                        totallizhidic[j[0]] = PersonalInfo.objects.filter(
                            QuitDate__range=Test_Endperiod).count()
                        if totalzaizhidic[j[0]]:
                            totallizhilvdic[j[0]] = round(float(totallizhidic[j[0]] / totalzaizhidic[j[0]]), 4)
                        else:
                            totallizhilvdic[j[0]] = 0
                        totallizhilvdic[j[0]] = '%.2f%%' % (totallizhilvdic[j[0]] * 100)
                    mounthnum += 1
                monthTable.append(totalyusuandic)
                monthTable.append(totalzaizhidic)
                monthTable.append(totalruzhidic)
                monthTable.append(totallizhidic)
                monthTable.append(totallizhilvdic)
            else:
                if (int(YearSearch) % 4) == 0:
                    if (int(YearSearch) % 100) == 0:
                        if (int(YearSearch) % 400) == 0:
                            # print("{0} 是闰年".format(YearSearch))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearSearch))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearSearch))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearSearch))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                mounthnow = 12  # datetime.datetime.now().month
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch).values("Customer").distinct().order_by(
                        "Customer"):
                    yusuandic = {"Customer": i["Customer"], "Classify": "預算"}
                    zaizhidic = {"Customer": i["Customer"], "Classify": "在職"}
                    ruzhidic = {"Customer": i["Customer"], "Classify": "入職"}
                    lizhidic = {"Customer": i["Customer"], "Classify": "離職"}
                    lizhilvdic = {"Customer": i["Customer"], "Classify": "離職率"}
                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            yusuandic[j[0]] = \
                                MainPower.objects.filter(Year=YearSearch, Customer=i["Customer"]).aggregate(Sum(j[0]))[
                                    j[0] + "__sum"]
                            if not yusuandic[j[0]]:
                                yusuandic[j[0]] = 0

                            DateNow_begin = datetime.datetime.strptime(YearSearch + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearSearch + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"], Year=YearSearch,
                                                                                RegistrationDate__lte=DateNow).count() - PersonalInfoHisByYear.objects.filter(
                                Customer=i["Customer"], Year=YearSearch, QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            ruzhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"],
                                                                                  Year=YearSearch,
                                                                                  RegistrationDate__range=Test_Endperiod).count()
                            lizhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"],
                                                                                  Year=YearSearch,
                                                                                  QuitDate__range=Test_Endperiod).count()
                            if zaizhidic[j[0]]:
                                lizhilvdic[j[0]] = round(float(lizhidic[j[0]] / zaizhidic[j[0]]), 4)
                            else:
                                lizhilvdic[j[0]] = 0
                            lizhilvdic[j[0]] = '%.2f%%' % (lizhilvdic[j[0]] * 100)
                        mounthnum += 1
                    monthTable.append(yusuandic)
                    monthTable.append(zaizhidic)
                    monthTable.append(ruzhidic)
                    monthTable.append(lizhidic)
                    monthTable.append(lizhilvdic)
                # 合计
                totalyusuandic = {"Customer": "合計", "Classify": "預算"}
                totalzaizhidic = {"Customer": "合計", "Classify": "在職"}
                totalruzhidic = {"Customer": "合計", "Classify": "入職"}
                totallizhidic = {"Customer": "合計", "Classify": "離職"}
                totallizhilvdic = {"Customer": "合計", "Classify": "離職率"}
                mounthnum = 1
                for j in mounthlist:
                    if mounthnum > mounthnow:
                        break
                    else:
                        totalyusuandic[j[0]] = \
                            MainPower.objects.filter(Year=YearSearch).aggregate(Sum(j[0]))[
                                j[0] + "__sum"]
                        if not totalyusuandic[j[0]]:
                            totalyusuandic[j[0]] = 0
                        DateNow_begin = datetime.datetime.strptime(YearSearch + "-" + j[1].split("-")[1] + "-1",
                                                                   '%Y-%m-%d')
                        # print(DateNow_begin)
                        DateNow = datetime.datetime.strptime(YearSearch + j[1], '%Y-%m-%d')
                        Test_Endperiod = [DateNow_begin, DateNow]
                        zaizhimounth = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                            RegistrationDate__lte=DateNow).count() - PersonalInfoHisByYear.objects.filter(
                            Year=YearSearch,
                            QuitDate__lte=DateNow).count()
                        totalzaizhidic[j[0]] = zaizhimounth
                        totallizhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                   QuitDate__range=Test_Endperiod).count()
                        if totalzaizhidic[j[0]]:
                            totallizhilvdic[j[0]] = round(float(totallizhidic[j[0]] / totalzaizhidic[j[0]]), 4)
                        else:
                            totallizhilvdic[j[0]] = 0
                        totallizhilvdic[j[0]] = '%.2f%%' % (totallizhilvdic[j[0]] * 100)
                    mounthnum += 1
                monthTable.append(totalyusuandic)
                monthTable.append(totalzaizhidic)
                monthTable.append(totalruzhidic)
                monthTable.append(totallizhidic)
                monthTable.append(totallizhilvdic)
            # Summary
            for i in monthTable:
                # print(i)

                if i["Classify"] == "離職率":

                    # # i["monthSummary"] = '%.2f%%' % (round((i["Jan"] + i["Feb"] + i["Mar"] + i["Apr"] + i["May"] + \
                    # #             i["Jan"] + i["Jul"] + i["Aug"] + i["Sep"] + i["Oct"] + \
                    # #             i["Nov"] + i["Dec"]), 2)*100)
                    # if everyzaizhi:
                    #     i["monthSummary"] = '%.2f%%' % (round(everylizhi / everyzaizhi, 4) * 100)
                    # else:
                    #     i["monthSummary"] = '%.2f%%' % 0
                    monthSummaryValue = 0
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthSummaryValue += float(i[j[0]].split("%")[0]) / 100
                    i["monthSummary"] = '%.2f%%' % (round(monthSummaryValue, 4) * 100)
                else:
                    monthSummaryValue = 0
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthSummaryValue += i[j[0]]
                    i["monthSummary"] = monthSummaryValue
                    if i["Classify"] == "離職":
                        everylizhi = monthSummaryValue
                    elif i["Classify"] == "在職":
                        everyzaizhi = monthSummaryValue
            # monthDiagram1Data&monthDiagram2Data
            for i in monthTable:
                if i["Classify"] == "在職" and i["Customer"] != "合計":
                    monthDiagram1Data_data = []
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthDiagram1Data_data.append(i[j[0]])
                    monthDiagram1Data.append(
                        {
                            'name': i["Customer"],
                            'type': 'bar',
                            'data': monthDiagram1Data_data,  # 對應月份 從一月到十二月
                            'label': {
                                'show': 'true',
                                'position': 'top'
                            },
                        }
                    )
                if i["Customer"] == "合計":
                    if i["Classify"] == "預算":
                        monthDiagram1Data_data = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram1Data_data.append(i[j[0]])
                        monthDiagram1Data.append(
                            {
                                'name': i["Classify"],
                                'type': 'line',
                                'yAxisIndex': 1,
                                'data': monthDiagram1Data_data
                            }
                        )
                    elif i["Classify"] == "在職":
                        monthDiagram1Data_data = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram1Data_data.append(i[j[0]])
                        monthDiagram1Data.append(
                            {
                                'name': i["Classify"],
                                'type': 'line',
                                'yAxisIndex': 1,
                                'data': monthDiagram1Data_data
                            }
                        )
                    elif i["Classify"] == "離職":
                        monthDiagram2Data_LIZHI = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram2Data_LIZHI.append(i[j[0]])
                            else:
                                monthDiagram2Data_LIZHI.append('')
                        monthDiagram2Data["LIZHI"] = monthDiagram2Data_LIZHI
                    elif i["Classify"] == "離職率":
                        monthDiagram2Data_LIZHILV = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                # monthDiagram2Data_LIZHILV.append(float(i[j[0]].strip('%')))
                                monthDiagram2Data_LIZHILV.append(i[j[0]])
                            else:
                                monthDiagram2Data_LIZHILV.append('')
                        monthDiagram2Data["LIZHILV"] = monthDiagram2Data_LIZHILV

            # By职称
            if not YearSearch or YearSearch == YearNow:
                # legendData = ["DQA"]
                YearSearch = YearNow
                legendData = []
                titleDiagramname = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by(
                        "Customer"):
                    selectItem.append(i["Customer"])
                    legendData.append(i["Customer"])
                PositionQuerySet = PersonalInfo.objects.filter(Status="在職").values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleTable_data = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "無對應的年份的職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItem:
                        titleTable_data[j] = PersonalInfo.objects.filter(PositionNow=i["PositionNow"],
                                                                         Customer=j,
                                                                         Status="在職").count()
                        titleSummary += titleTable_data[j]
                    titleTable_data["titleSummary"] = titleSummary
                    titleTable.append(titleTable_data)
                    titleDiagramname.append(
                        Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "無對應的年份的職稱")  # Year=YearNow,
            else:
                # legendData = ["DQA"]
                legendData = []
                titleDiagramname = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItem.append(i["Customer"])
                    legendData.append(i["Customer"])
                PositionQuerySet = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                        Status="在職").values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    # print(i["PositionNow"])
                    titleTable_data = {
                        "Title": Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch) else "無對應的年份的職稱", }  # Year=YearSearch,
                    titleSummary = 0
                    for j in selectItem:
                        titleTable_data[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                  PositionNow=i[
                                                                                      "PositionNow"],
                                                                                  Customer=j,
                                                                                  Status="在職").count()
                        titleSummary += titleTable_data[j]
                    titleTable_data["titleSummary"] = titleSummary
                    titleTable.append(titleTable_data)
                    titleDiagramname.append(
                        Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch) else "無對應的年份的職稱", )  # Year=YearSearch,
            # titleDiagram
            titleDiagram["legendData"] = legendData
            titleDiagram["titleDiagramname"] = titleDiagramname
            titleDiagramData = []
            for i in legendData:
                # print(i)
                titleDiagramData_Data = []
                for m in titleDiagramname:
                    for j in titleTable:
                        if m == j["Title"]:  # 确保data与seniorityDiagramname值对应
                            # print(j)
                            if i == "DQA":
                                titleDiagramData_Data.append(j["titleSummary"])
                            else:
                                titleDiagramData_Data.append(j[i])
                titleDiagramData.append(
                    {
                        'name': i,
                        'type': 'bar',
                        'data': titleDiagramData_Data
                    }
                )
            titleDiagram["titleDiagramData"] = titleDiagramData

            # By年资
            seniorityDiagramname = ['0.25年以下', '0.25~1年', '1~2年', '2~3年', '3~5年', '5~10年', '10~15年', "15~20年", '20年以上']
            if not YearSearch or YearSearch == YearNow:
                # legendDataseniority = ["DQA"]  # 与By职称里的名称区分开
                legendDataseniority = []  # 与By职称里的名称区分开
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    legendDataseniority.append(i["Customer"])
                CustomerSeniorityData = {
                    # "C38": {"0.25年以下": 20, "0.25~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for j in selectItem:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(Customer=j, Status="在職"):
                        # if Per.Status == "在職":
                        Seniority = round(
                            float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                            1)
                        # else:
                        #     Seniority = round(
                        #         float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[j] = {"0.25年以下": number025, "0.25~1年": number025_1, '1~2年': number1_2,
                                                '2~3年': number2_3, '3~5年': number3_5,
                                                '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                                '20年以上': number20, }
                # print(CustomerSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable_data = {"Seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_data[key] = value[i]
                    seniorityTable.append(seniorityTable_data)
                # print(seniorityTable)
                # Summary
                for i in seniorityTable:
                    senioritySummary = 0
                    for j in selectItem:
                        if j in i.keys():
                            senioritySummary += i[j]
                    i["senioritySummary"] = senioritySummary
                seniorityDiagram = {
                    "legendData": legendDataseniority,
                    "seniorityDiagramname": seniorityDiagramname,
                }
                seniorityDiagramData = []
                for i in legendDataseniority:
                    # print(i)
                    seniorityDiagramData_Data = []
                    for m in seniorityDiagramname:
                        for j in seniorityTable:
                            if m == j["Seniority"]:  # 确保data与seniorityDiagramname值对应
                                # print(j)
                                if i == "DQA":
                                    seniorityDiagramData_Data.append(j["senioritySummary"])
                                else:
                                    seniorityDiagramData_Data.append(j[i])
                    seniorityDiagramData.append(
                        {
                            'name': i,
                            'type': 'bar',
                            'data': seniorityDiagramData_Data
                        }
                    )
                seniorityDiagram["seniorityDiagramData"] = seniorityDiagramData
            else:
                pass  # 往年数据算年资无意义

            # By学历
            if not YearSearch or YearSearch == YearNow:
                educationDiagramname = []
                Total_Summary = 0
                for i in PersonalInfo.objects.filter(Status="在職").values("Education").distinct().order_by("Education"):
                    educationDiagramname.append(i["Education"])
                    educationTable_data = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in selectItem:
                        educationTable_data[j] = PersonalInfo.objects.filter(Education=i["Education"], Customer=j,
                                                                             Status="在職").count()
                        educationSummary += educationTable_data[j]
                    educationTable_data["educationSummary"] = educationSummary
                    Total_Summary += educationSummary
                    educationTable.append(educationTable_data)
            else:
                educationDiagramname = []
                Total_Summary = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Education").distinct().order_by("Education"):
                    educationDiagramname.append(i["Education"])
                    educationTable_data = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in selectItem:
                        educationTable_data[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                      Education=i["Education"],
                                                                                      Customer=j,
                                                                                      Status="在職").count()
                        educationSummary += educationTable_data[j]
                    educationTable_data["educationSummary"] = educationSummary
                    Total_Summary += educationSummary
                    educationTable.append(educationTable_data)
            # educationTable占比
            if educationTable:
                if Total_Summary:
                    for i in educationTable:
                        i["accountFor"] = '%.2f%%' % ((float(i["educationSummary"]) / Total_Summary) * 100)
                else:
                    for i in educationTable:
                        i["accountFor"] = '%.2f%%' % 0
            # educationDiagram
            educationDiagram = {
                "educationDiagramname": educationDiagramname,
            }
            educationDiagramHE = []
            educationDiagramZH = []
            for i in educationDiagramname:
                # print(i)
                for j in educationTable:
                    if i == j["Education"]:
                        educationDiagramHE.append(j["educationSummary"])
                        educationDiagramZH.append(float(j["accountFor"].strip('%')))
            educationDiagram["educationDiagramHE"] = educationDiagramHE
            educationDiagram["educationDiagramZH"] = educationDiagramZH

            # By专业
            if not YearSearch or YearSearch == YearNow:
                Customer_major = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Education", "Major").distinct().order_by(
                        "Education"):
                    # print(i["Education"], i["Major"])
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfo.objects.filter(Education=i["Education"],
                                                                                 Major=i["Major"],
                                                                                 Customer=j, Status="在職").count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfo.objects.filter(Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status="在職").count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
            else:
                Customer_major = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Education", "Major").distinct().order_by("Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                          Status="在職",
                                                                                          Education=i["Education"],
                                                                                          Major=i["Major"],
                                                                                          Customer=j).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
            if MajorIfo.objects.filter(Education__contains=i["Education"],
                                       Major="TBC").first():
                professionTableData_TBC = {
                    "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                     Major="TBC").first().Categories,
                    "Profession": "TBC",
                }
                # print(TBCnum)
                TBCnum_professionSummary = 0
                for j in Customer_major:
                    professionTableData_TBC[j] = 0
                    for i in TBCnum:
                        professionTableData_TBC[j] += i[j]
                        TBCnum_professionSummary += i["professionSummary"]
                professionTableData_TBC["professionSummary"] = TBCnum_professionSummary
                professionTable.append(professionTableData_TBC)
            professionTable = sorted(professionTable,
                                     key=lambda e: (e.__getitem__('daLei'), e.__getitem__('professionSummary')),
                                     reverse=True)
            # heBingNum
            professionTablenew = []
            for i in professionTable:
                professionTablenew.append(i["daLei"])
            professionTable_counter = Counter(professionTablenew)
            # print(professionTable)
            # print(professionTable_counter)
            # print(dict(professionTable_counter))
            # heBing里的数值与professionTable["daLei"] 的value排序保持一致
            heBingNum_sort = sorted(dict(professionTable_counter).items(), key=lambda e: e[0], reverse=True)
            # print(heBingNum_sort)
            for i in heBingNum_sort:
                heBingNum.append(i[1])

            # By地区
            if not YearSearch or YearSearch == YearNow:
                Customer_region = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfo.objects.filter(Status="在職").values("NativeProvince").distinct().order_by(
                        "NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfo.objects.filter(Status="在職",
                                                                          NativeProvince=i["NativeProvince"],
                                                                          Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            else:
                Customer_region = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "NativeProvince").distinct().order_by("NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職",
                                                                                   NativeProvince=i["NativeProvince"],
                                                                                   Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            regionsTable = sorted(regionsTable, key=lambda x: x.__getitem__("regionsSummary"), reverse=True)
        if request.POST.get("isGetData") == "SEARCH":
            YearSearch = request.POST.get("Year")
            YearNow = str(datetime.datetime.now().year)
            # Search_Endperiod = request.POST.getlist("YearRange", [])
            # By月份
            RunnYearflag = 0
            if not YearSearch or YearSearch == YearNow:  # 当年的到PersonalInfo里面查找,年份为空默认查找当年数据
                if (int(YearNow) % 4) == 0:
                    if (int(YearNow) % 100) == 0:
                        if (int(YearNow) % 400) == 0:
                            # print("{0} 是闰年".format(YearNow))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearNow))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearNow))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearNow))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                # mounthlist = ["Jan", "Fer", "Mar", "Apr", "May", "Jun",
                #               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "monthSummary"]
                mounthnow = datetime.datetime.now().month
                for i in PersonalInfo.objects.all().values("Customer").distinct().order_by("Customer"):
                    yusuandic = {"Customer": i["Customer"], "Classify": "預算"}
                    zaizhidic = {"Customer": i["Customer"], "Classify": "在職"}
                    ruzhidic = {"Customer": i["Customer"], "Classify": "入職"}
                    lizhidic = {"Customer": i["Customer"], "Classify": "離職"}
                    lizhilvdic = {"Customer": i["Customer"], "Classify": "離職率"}
                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            yusuandic[j[0]] = \
                                MainPower.objects.filter(Year=YearNow, Customer=i["Customer"]).aggregate(Sum(j[0]))[
                                    j[0] + "__sum"]
                            if not yusuandic[j[0]]:
                                yusuandic[j[0]] = 0
                            DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                       RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                                Customer=i["Customer"], QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            ruzhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                         RegistrationDate__range=Test_Endperiod).count()
                            # lizhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                            #                                              QuitDate__lte=DateNow).count()
                            lizhidic[j[0]] = PersonalInfo.objects.filter(Customer=i["Customer"],
                                                                         QuitDate__range=Test_Endperiod).count()
                            if zaizhidic[j[0]]:
                                lizhilvdic[j[0]] = round(float(lizhidic[j[0]] / zaizhidic[j[0]]), 4)
                            else:
                                lizhilvdic[j[0]] = 0
                            lizhilvdic[j[0]] = '%.2f%%' % (lizhilvdic[j[0]] * 100)
                        mounthnum += 1
                    monthTable.append(yusuandic)
                    monthTable.append(zaizhidic)
                    monthTable.append(ruzhidic)
                    monthTable.append(lizhidic)
                    monthTable.append(lizhilvdic)
                # 合计
                totalyusuandic = {"Customer": "合計", "Classify": "預算"}
                totalzaizhidic = {"Customer": "合計", "Classify": "在職"}
                totalruzhidic = {"Customer": "合計", "Classify": "入職"}
                totallizhidic = {"Customer": "合計", "Classify": "離職"}
                totallizhilvdic = {"Customer": "合計", "Classify": "離職率"}
                mounthnum = 1
                for j in mounthlist:
                    if mounthnum > mounthnow:
                        break
                    else:
                        totalyusuandic[j[0]] = \
                            MainPower.objects.filter(Year=YearNow).aggregate(Sum(j[0]))[
                                j[0] + "__sum"]
                        if not totalyusuandic[j[0]]:
                            totalyusuandic[j[0]] = 0
                        DateNow_begin = datetime.datetime.strptime(YearNow + "-" + j[1].split("-")[1] + "-1",
                                                                   '%Y-%m-%d')
                        # print(DateNow_begin)
                        DateNow = datetime.datetime.strptime(YearNow + j[1], '%Y-%m-%d')
                        Test_Endperiod = [DateNow_begin, DateNow]
                        zaizhimounth = PersonalInfo.objects.filter(
                            RegistrationDate__lte=DateNow).count() - PersonalInfo.objects.filter(
                            QuitDate__lte=DateNow).count()
                        totalzaizhidic[j[0]] = zaizhimounth
                        totalruzhidic[j[0]] = PersonalInfo.objects.filter(
                            RegistrationDate__range=Test_Endperiod).count()
                        # totallizhidic[j[0]] = PersonalInfo.objects.filter(
                        #     QuitDate__lte=DateNow).count()
                        totallizhidic[j[0]] = PersonalInfo.objects.filter(
                            QuitDate__range=Test_Endperiod).count()
                        if totalzaizhidic[j[0]]:
                            totallizhilvdic[j[0]] = round(float(totallizhidic[j[0]] / totalzaizhidic[j[0]]), 4)
                        else:
                            totallizhilvdic[j[0]] = 0
                        totallizhilvdic[j[0]] = '%.2f%%' % (totallizhilvdic[j[0]] * 100)
                    mounthnum += 1
                monthTable.append(totalyusuandic)
                monthTable.append(totalzaizhidic)
                monthTable.append(totalruzhidic)
                monthTable.append(totallizhidic)
                monthTable.append(totallizhilvdic)
            else:
                if (int(YearSearch) % 4) == 0:
                    if (int(YearSearch) % 100) == 0:
                        if (int(YearSearch) % 400) == 0:
                            # print("{0} 是闰年".format(YearSearch))  # 整百年能被400整除的是闰年
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                        else:
                            # print("{0} 不是闰年".format(YearSearch))
                            mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                          ("May", "-5-31"), ("Jun", "-6-30"),
                                          ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                          ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                    else:
                        # print("{0} 是闰年".format(YearSearch))  # 非整百年能被4整除的为闰年
                        mounthlist = [("Jan", "-1-31"), ("Feb", "-2-29"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                      ("May", "-5-31"), ("Jun", "-6-30"),
                                      ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                      ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                else:
                    # print("{0} 不是闰年".format(YearSearch))
                    mounthlist = [("Jan", "-1-31"), ("Feb", "-2-28"), ("Mar", "-3-31"), ("Apr", "-4-30"),
                                  ("May", "-5-31"),
                                  ("Jun", "-6-30"),
                                  ("Jul", "-7-31"), ("Aug", "-8-31"), ("Sep", "-9-30"), ("Oct", "-10-31"),
                                  ("Nov", "-11-30"), ("Dec", "-12-31"), ]
                mounthnow = 12  # datetime.datetime.now().month
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch).values("Customer").distinct().order_by(
                        "Customer"):
                    yusuandic = {"Customer": i["Customer"], "Classify": "預算"}
                    zaizhidic = {"Customer": i["Customer"], "Classify": "在職"}
                    ruzhidic = {"Customer": i["Customer"], "Classify": "入職"}
                    lizhidic = {"Customer": i["Customer"], "Classify": "離職"}
                    lizhilvdic = {"Customer": i["Customer"], "Classify": "離職率"}
                    mounthnum = 1
                    for j in mounthlist:
                        if mounthnum > mounthnow:
                            break
                        else:
                            yusuandic[j[0]] = \
                                MainPower.objects.filter(Year=YearSearch, Customer=i["Customer"]).aggregate(Sum(j[0]))[
                                    j[0] + "__sum"]
                            if not yusuandic[j[0]]:
                                yusuandic[j[0]] = 0

                            DateNow_begin = datetime.datetime.strptime(YearSearch + "-" + j[1].split("-")[1] + "-1",
                                                                       '%Y-%m-%d')
                            # print(DateNow_begin)
                            DateNow = datetime.datetime.strptime(YearSearch + j[1], '%Y-%m-%d')
                            Test_Endperiod = [DateNow_begin, DateNow]
                            zaizhimounth = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"], Year=YearSearch,
                                                                                RegistrationDate__lte=DateNow).count() - PersonalInfoHisByYear.objects.filter(
                                Customer=i["Customer"], Year=YearSearch, QuitDate__lte=DateNow).count()
                            zaizhidic[j[0]] = zaizhimounth
                            ruzhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"],
                                                                                  Year=YearSearch,
                                                                                  RegistrationDate__range=Test_Endperiod).count()
                            lizhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Customer=i["Customer"],
                                                                                  Year=YearSearch,
                                                                                  QuitDate__range=Test_Endperiod).count()
                            if zaizhidic[j[0]]:
                                lizhilvdic[j[0]] = round(float(lizhidic[j[0]] / zaizhidic[j[0]]), 4)
                            else:
                                lizhilvdic[j[0]] = 0
                            lizhilvdic[j[0]] = '%.2f%%' % (lizhilvdic[j[0]] * 100)
                        mounthnum += 1
                    monthTable.append(yusuandic)
                    monthTable.append(zaizhidic)
                    monthTable.append(ruzhidic)
                    monthTable.append(lizhidic)
                    monthTable.append(lizhilvdic)
                # 合计
                totalyusuandic = {"Customer": "合計", "Classify": "預算"}
                totalzaizhidic = {"Customer": "合計", "Classify": "在職"}
                totalruzhidic = {"Customer": "合計", "Classify": "入職"}
                totallizhidic = {"Customer": "合計", "Classify": "離職"}
                totallizhilvdic = {"Customer": "合計", "Classify": "離職率"}
                mounthnum = 1
                for j in mounthlist:
                    if mounthnum > mounthnow:
                        break
                    else:
                        totalyusuandic[j[0]] = \
                            MainPower.objects.filter(Year=YearSearch).aggregate(Sum(j[0]))[
                                j[0] + "__sum"]
                        if not totalyusuandic[j[0]]:
                            totalyusuandic[j[0]] = 0
                        DateNow_begin = datetime.datetime.strptime(YearSearch + "-" + j[1].split("-")[1] + "-1",
                                                                   '%Y-%m-%d')
                        # print(DateNow_begin)
                        DateNow = datetime.datetime.strptime(YearSearch + j[1], '%Y-%m-%d')
                        Test_Endperiod = [DateNow_begin, DateNow]
                        zaizhimounth = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                            RegistrationDate__lte=DateNow).count() - PersonalInfoHisByYear.objects.filter(
                            Year=YearSearch,
                            QuitDate__lte=DateNow).count()
                        totalzaizhidic[j[0]] = zaizhimounth
                        totalruzhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                   RegistrationDate__range=Test_Endperiod).count()
                        totallizhidic[j[0]] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                   QuitDate__range=Test_Endperiod).count()
                        if totalzaizhidic[j[0]]:
                            totallizhilvdic[j[0]] = round(float(totallizhidic[j[0]] / totalzaizhidic[j[0]]), 4)
                        else:
                            totallizhilvdic[j[0]] = 0
                        totallizhilvdic[j[0]] = '%.2f%%' % (totallizhilvdic[j[0]] * 100)
                    mounthnum += 1
                monthTable.append(totalyusuandic)
                monthTable.append(totalzaizhidic)
                monthTable.append(totalruzhidic)
                monthTable.append(totallizhidic)
                monthTable.append(totallizhilvdic)
            # Summary
            for i in monthTable:
                # print(i)

                if i["Classify"] == "離職率":

                    # # i["monthSummary"] = '%.2f%%' % (round((i["Jan"] + i["Feb"] + i["Mar"] + i["Apr"] + i["May"] + \
                    # #             i["Jan"] + i["Jul"] + i["Aug"] + i["Sep"] + i["Oct"] + \
                    # #             i["Nov"] + i["Dec"]), 2)*100)
                    # if everyzaizhi:
                    #     i["monthSummary"] = '%.2f%%' % (round(everylizhi / everyzaizhi, 4) * 100)
                    # else:
                    #     i["monthSummary"] = '%.2f%%' % 0
                    monthSummaryValue = 0
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthSummaryValue += float(i[j[0]].split("%")[0]) / 100
                    i["monthSummary"] = '%.2f%%' % (round(monthSummaryValue, 4) * 100)
                else:
                    monthSummaryValue = 0
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthSummaryValue += i[j[0]]
                    i["monthSummary"] = monthSummaryValue
                    if i["Classify"] == "離職":
                        everylizhi = monthSummaryValue
                    elif i["Classify"] == "在職":
                        everyzaizhi = monthSummaryValue
            # monthDiagram1Data&monthDiagram2Data
            for i in monthTable:
                if i["Classify"] == "在職" and i["Customer"] != "合計":
                    monthDiagram1Data_data = []
                    for j in mounthlist:
                        if j[0] in i.keys():
                            monthDiagram1Data_data.append(i[j[0]])
                    monthDiagram1Data.append(
                        {
                            'name': i["Customer"],
                            'type': 'bar',
                            'data': monthDiagram1Data_data,  # 對應月份 從一月到十二月
                            'label': {
                                'show': 'true',
                                'position': 'top'
                            },
                        }
                    )
                if i["Customer"] == "合計":
                    if i["Classify"] == "預算":
                        monthDiagram1Data_data = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram1Data_data.append(i[j[0]])
                        monthDiagram1Data.append(
                            {
                                'name': i["Classify"],
                                'type': 'line',
                                'yAxisIndex': 1,
                                'data': monthDiagram1Data_data
                            }
                        )
                    elif i["Classify"] == "在職":
                        monthDiagram1Data_data = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram1Data_data.append(i[j[0]])
                        monthDiagram1Data.append(
                            {
                                'name': i["Classify"],
                                'type': 'line',
                                'yAxisIndex': 1,
                                'data': monthDiagram1Data_data
                            }
                        )
                    elif i["Classify"] == "離職":
                        monthDiagram2Data_LIZHI = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                monthDiagram2Data_LIZHI.append(i[j[0]])
                            else:
                                monthDiagram2Data_LIZHI.append('')
                        monthDiagram2Data["LIZHI"] = monthDiagram2Data_LIZHI
                    elif i["Classify"] == "離職率":
                        monthDiagram2Data_LIZHILV = []
                        for j in mounthlist:
                            if j[0] in i.keys():
                                # monthDiagram2Data_LIZHILV.append(float(i[j[0]].strip('%')))
                                monthDiagram2Data_LIZHILV.append(i[j[0]])
                            else:
                                monthDiagram2Data_LIZHILV.append('')
                        monthDiagram2Data["LIZHILV"] = monthDiagram2Data_LIZHILV

            # By职称
            if not YearSearch or YearSearch == YearNow:
                # legendData = ["DQA"]
                YearSearch = YearNow
                legendData = []
                titleDiagramname = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    selectItem.append(i["Customer"])
                    legendData.append(i["Customer"])
                PositionQuerySet = PersonalInfo.objects.filter(Status="在職").values("PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleTable_data = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItem:
                        titleTable_data[j] = PersonalInfo.objects.filter(PositionNow=i["PositionNow"], Customer=j,
                                                                         Status="在職").count()
                        titleSummary += titleTable_data[j]
                    titleTable_data["titleSummary"] = titleSummary
                    titleTable.append(titleTable_data)
                    titleDiagramname.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")  # Year=YearNow,
            else:
                # legendData = ["DQA"]
                legendData = []
                titleDiagramname = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItem.append(i["Customer"])
                    legendData.append(i["Customer"])
                PositionQuerySet = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    # print(i["PositionNow"])
                    titleTable_data = {
                        "Title": Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearSearch,
                    titleSummary = 0
                    for j in selectItem:
                        titleTable_data[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                  PositionNow=i["PositionNow"],
                                                                                  Customer=j, Status="在職").count()
                        titleSummary += titleTable_data[j]
                    titleTable_data["titleSummary"] = titleSummary
                    titleTable.append(titleTable_data)
                    titleDiagramname.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")  # Year=YearSearch,
            # titleDiagram
            titleDiagram["legendData"] = legendData
            titleDiagram["titleDiagramname"] = titleDiagramname
            titleDiagramData = []
            for i in legendData:
                # print(i)
                titleDiagramData_Data = []
                for m in titleDiagramname:
                    for j in titleTable:
                        if m == j["Title"]:  # 确保data与seniorityDiagramname值对应
                            # print(j)
                            if i == "DQA":
                                titleDiagramData_Data.append(j["titleSummary"])
                            else:
                                titleDiagramData_Data.append(j[i])
                titleDiagramData.append(
                    {
                        'name': i,
                        'type': 'bar',
                        'data': titleDiagramData_Data
                    }
                )
            titleDiagram["titleDiagramData"] = titleDiagramData

            # By年资
            seniorityDiagramname = ['0.25年以下', '0.25~1年', '1~2年', '2~3年', '3~5年', '5~10年', '10~15年', "15~20年", '20年以上']
            if not YearSearch or YearSearch == YearNow:
                # legendDataseniority = ["DQA"]
                legendDataseniority = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    legendDataseniority.append(i["Customer"])
                CustomerSeniorityData = {
                    # "C38": {"0.25年以下": 20, "0.25~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for j in selectItem:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(Customer=j, Status="在職"):
                        # if Per.Status == "在職":
                        Seniority = round(
                            float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                            1)
                        # else:
                        #     Seniority = round(
                        #         float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[j] = {"0.25年以下": number025, "0.25~1年": number025_1, '1~2年': number1_2,
                                                '2~3年': number2_3, '3~5年': number3_5,
                                                '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                                '20年以上': number20, }
                # print(CustomerSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable_data = {"Seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_data[key] = value[i]
                    seniorityTable.append(seniorityTable_data)
                # print(seniorityTable)
                # Summary
                for i in seniorityTable:
                    senioritySummary = 0
                    for j in selectItem:
                        if j in i.keys():
                            senioritySummary += i[j]
                    i["senioritySummary"] = senioritySummary
                seniorityDiagram = {
                    "legendData": legendDataseniority,
                    "seniorityDiagramname": seniorityDiagramname,
                }
                seniorityDiagramData = []
                for i in legendDataseniority:
                    # print(i)
                    seniorityDiagramData_Data = []
                    for m in seniorityDiagramname:
                        for j in seniorityTable:
                            if m == j["Seniority"]:  # 确保data与seniorityDiagramname值对应
                                # print(j)
                                if i == "DQA":
                                    seniorityDiagramData_Data.append(j["senioritySummary"])
                                else:
                                    seniorityDiagramData_Data.append(j[i])
                    seniorityDiagramData.append(
                        {
                            'name': i,
                            'type': 'bar',
                            'data': seniorityDiagramData_Data
                        }
                    )
                seniorityDiagram["seniorityDiagramData"] = seniorityDiagramData
            else:
                seniorityTable = [
                    {"Seniority": "往年數據的在職年資無意義", "A31": "Null", "A32": "Null", "C38": "Null",
                     "senioritySummary": "Null"}
                ]
                # print(seniorityTable)
                # pass  # 往年数据算年资无意义
            # print(seniorityTable,seniorityDiagram)

            # By学历
            if not YearSearch or YearSearch == YearNow:
                educationDiagramname = []
                Total_Summary = 0
                for i in PersonalInfo.objects.filter(Status="在職").values("Education").distinct().order_by("Education"):
                    educationDiagramname.append(i["Education"])
                    educationTable_data = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in selectItem:
                        educationTable_data[j] = PersonalInfo.objects.filter(Education=i["Education"], Customer=j,
                                                                             Status="在職").count()
                        educationSummary += educationTable_data[j]
                    educationTable_data["educationSummary"] = educationSummary
                    Total_Summary += educationSummary
                    educationTable.append(educationTable_data)
            else:
                educationDiagramname = []
                Total_Summary = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Education").distinct().order_by(
                    "Education"):
                    educationDiagramname.append(i["Education"])
                    educationTable_data = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in selectItem:
                        educationTable_data[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                      Education=i["Education"],
                                                                                      Customer=j, Status="在職").count()
                        educationSummary += educationTable_data[j]
                    educationTable_data["educationSummary"] = educationSummary
                    Total_Summary += educationSummary
                    educationTable.append(educationTable_data)
            # educationTable占比
            if educationTable:
                if Total_Summary:
                    for i in educationTable:
                        i["accountFor"] = '%.2f%%' % ((float(i["educationSummary"]) / Total_Summary) * 100)
                else:
                    for i in educationTable:
                        i["accountFor"] = '%.2f%%' % 0
            # educationDiagram
            educationDiagram = {
                "educationDiagramname": educationDiagramname,
            }
            educationDiagramHE = []
            educationDiagramZH = []
            for i in educationDiagramname:
                # print(i)
                for j in educationTable:
                    if i == j["Education"]:
                        educationDiagramHE.append(j["educationSummary"])
                        educationDiagramZH.append(float(j["accountFor"].strip('%')))
            educationDiagram["educationDiagramHE"] = educationDiagramHE
            educationDiagram["educationDiagramZH"] = educationDiagramZH

            # By专业
            if not YearSearch or YearSearch == YearNow:
                Customer_major = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Education", "Major").distinct().order_by(
                        "Education"):
                    # print(i["Education"], i["Major"])
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfo.objects.filter(Education=i["Education"],
                                                                                 Major=i["Major"],
                                                                                 Customer=j, Status="在職").count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfo.objects.filter(Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status="在職").count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
            else:
                Customer_major = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Education", "Major").distinct().order_by("Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                          Status="在職",
                                                                                          Education=i["Education"],
                                                                                          Major=i["Major"],
                                                                                          Customer=j).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                    if MajorIfo.objects.filter(Education__contains=i["Education"],
                                               Major="TBC").first():
                        professionTableData_TBC = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major="TBC").first().Categories,
                            "Profession": "TBC",
                        }
                        # print(TBCnum)
                        TBCnum_professionSummary = 0
                        for j in Customer_major:
                            professionTableData_TBC[j] = 0
                            for i in TBCnum:
                                professionTableData_TBC[j] += i[j]
                                TBCnum_professionSummary += i["professionSummary"]
                        professionTableData_TBC["professionSummary"] = TBCnum_professionSummary
                        professionTable.append(professionTableData_TBC)
            professionTable = sorted(professionTable,
                                     key=lambda e: (e.__getitem__('daLei'), e.__getitem__('professionSummary')),
                                     reverse=True)
            # heBingNum
            professionTablenew = []
            for i in professionTable:
                professionTablenew.append(i["daLei"])
            professionTable_counter = Counter(professionTablenew)
            # print(professionTable)
            # print(professionTable_counter)
            # print(dict(professionTable_counter))
            # heBing里的数值与professionTable["daLei"] 的value排序保持一致
            heBingNum_sort = sorted(dict(professionTable_counter).items(), key=lambda e: e[0], reverse=True)
            # print(heBingNum_sort)
            for i in heBingNum_sort:
                heBingNum.append(i[1])

            # By地区
            if not YearSearch or YearSearch == YearNow:
                Customer_region = []
                for i in PersonalInfo.objects.filter(Status="在職").values("Customer").distinct().order_by("Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfo.objects.filter(Status="在職").values("NativeProvince").distinct().order_by(
                        "NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfo.objects.filter(Status="在職",
                                                                          NativeProvince=i["NativeProvince"],
                                                                          Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            else:
                Customer_region = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職").values(
                        "NativeProvince").distinct().order_by("NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status="在職",
                                                                                   NativeProvince=i["NativeProvince"],
                                                                                   Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            regionsTable = sorted(regionsTable, key=lambda x: x.__getitem__("regionsSummary"), reverse=True)

        data = {
            "monthTable": monthTable,
            "searchYear": searchYear,
            "titleTable": titleTable,
            "seniorityTable": seniorityTable,
            "educationTable": educationTable,
            "professionTable": professionTable,
            "regionsTable": regionsTable,
            "monthDiagram1Data": monthDiagram1Data,
            "monthDiagram2Data": monthDiagram2Data,
            "titleDiagram": titleDiagram,
            "seniorityDiagram": seniorityDiagram,
            "educationDiagram": educationDiagram,
            "selectItem": selectItem,
            "heBingNum": heBingNum,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/Summary2.html', locals())


@csrf_exempt
def Summary3(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "PersonalInfo/Summary3"
    perinTable = [
        # {"RegistrationDate": "2018/7/17", "Seniority": "1.9", "Customer": "A31", "Department": "二處",
        #  "Lesson": "KH0MAQADA0", "GroupEmployees": "20471750", "ChineseName": "葉爍", "EnglishName": "Ye. Steven",
        #  "Gender": "男", "CurrentTitle": "工程師", "DepartureDate": "2020/5/28", "LastPerformance": "B",
        #  "DepartureReasons": "B"},
    ]
    searchYear = str(datetime.datetime.now().year)  # 姿势first是有用
    selectItem = [
        # "A31", "A32", "C38"
    ]
    reasonsTable = [
        # {"Reasons": "A-薪資福利因素", "A31": "32", "A32": "28", "C38": "27", "reasonsSummary": "87", "zhanReasons": "50.3"},
        # {"Reasons": "B-工作環境因素", "A31": "7", "A32": "6", "C38": "3", "reasonsSummary": "16", "zhanReasons": "9.2"},
        # {"Reasons": "C-家庭因素", "A31": "16", "A32": "12", "C38": "19", "reasonsSummary": "47", "zhanReasons": "27.2"},
        # {"Reasons": "D-進修學習", "A31": "2", "A32": "6", "C38": "5", "reasonsSummary": "13", "zhanReasons": "7.5"},
        # {"Reasons": "E-其他", "A31": "3", "A32": "5", "C38": "2", "reasonsSummary": "10", "zhanReasons": "5.8"},
    ]
    reasonsDiagramData = {
        # 'LABEL': ["A-薪資福利因素", "B-工作環境因素", "C-家庭因素", "D-進修學習", "E-其他"],
        # 'HEJI': [87, 16, 47, 13, 10],
        # 'ZHANZONG': [0.502890173, 0.092485549, 0.271676301, 0.075144509, 0.057803468]
    }

    titleTable = [
        # {"Title": "助技員", "A31": "0", "A32": "64", "C38": "0", "titleSummary": "64", "titleDeparture": "15.7%"},
        # {"Title": "技術員", "A31": "18", "A32": "30", "C38": "23", "titleSummary": "71", "titleDeparture": "14.7%"},
        # {"Title": "助工師", "A31": "59", "A32": "83", "C38": "63", "titleSummary": "205", "titleDeparture": "30.9%"},
        # {"Title": "工程師", "A31": "43", "A32": "35", "C38": "26", "titleSummary": "104", "titleDeparture": "11.3%"},
        # {"Title": "資工師", "A31": "33", "A32": "34", "C38": "41", "titleSummary": "108", "titleDeparture": "23.5%"},
        # {"Title": "副課長", "A31": "20", "A32": "19", "C38": "24", "titleSummary": "63", "titleDeparture": "2.0%"},
        # {"Title": "課長", "A31": "25", "A32": "19", "C38": "25", "titleSummary": "69", "titleDeparture": "2.0%"},
        # {"Title": "襄理", "A31": "2", "A32": "6", "C38": "4", "titleSummary": "12", "titleDeparture": "0.0%"},
        # {"Title": "副理", "A31": "1", "A32": "1", "C38": "1", "titleSummary": "3", "titleDeparture": "0.0%"},
        # {"Title": "經理", "A31": "1", "A32": "0", "C38": "2", "titleSummary": "3", "titleDeparture": "0.0%"},
        # {"Title": "資深經理", "A31": "1", "A32": "0", "C38": "0", "titleSummary": "1", "titleDeparture": "0.0%"}
    ]
    titleSeniorityData = [
        # "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
    ]
    titleTable1 = [
        # {"Title": "助技員", "3个月以下": "0", "3个月~1年": "64", "1~2年": "0", "2~3年": "1", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "64"},
        # {"Title": "技術員", "3个月以下": "18", "3个月~1年": "30", "1~2年": "23", "2~3年": "", "3~5年": "3", "5~10年": "",
        #  "10~15年": "", "15~20年": "", "20年以上": "", "titleSummary": "71"},
        # {"Title": "助工師", "3个月以下": "59", "3个月~1年": "83", "1~2年": "63", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "205"},
        # {"Title": "工程師", "3个月以下": "43", "3个月~1年": "35", "1~2年": "26", "2~3年": "", "3~5年": "", "5~10年": "5",
        #  "10~15年": "", "15~20年": "", "20年以上": "", "titleSummary": "104"},
        # {"Title": "資工師", "3个月以下": "33", "3个月~1年": "34", "1~2年": "41", "2~3年": "", "3~5年": "", "5~10年": "",
        #  "10~15年": "6", "15~20年": "", "20年以上": "", "titleSummary": "108"},
        # {"Title": "副課長", "3个月以下": "20", "3个月~1年": "19", "1~2年": "24", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "63"},
        # {"Title": "課長", "3个月以下": "25", "3个月~1年": "19", "1~2年": "25", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "3", "20年以上": "42", "titleSummary": "69"},
        # {"Title": "襄理", "3个月以下": "2", "3个月~1年": "6", "1~2年": "4", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "12"},
        # {"Title": "副理", "3个月以下": "1", "3个月~1年": "1", "1~2年": "1", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "3"},
        # {"Title": "經理", "3个月以下": "1", "3个月~1年": "0", "1~2年": "2", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "3"},
        # {"Title": "資深經理", "3个月以下": "1", "3个月~1年": "0", "1~2年": "0", "2~3年": "", "3~5年": "", "5~10年": "", "10~15年": "",
        #  "15~20年": "", "20年以上": "", "titleSummary": "1"}
    ]
    titleDiagram2Data = {
        # 'LABEL': ["助技員", "技術員", "助工師", "工程師", "資工師", "副課長", "課長", "襄理", "副理", "經理", "資深經理"],
        # 'HEJILIZHI': [32, 30, 63, 23, 48, 4, 4, 0, 0, 0, 0],
        # 'LIZHIBI': [0.15686274, 0.14705882, 0.30882352, 0.11274509, 0.23529411, 0.01960784, 0.01960784, 0, 0, 0, 0]
    }
    TitleText = ""  # "助技員"
    titleSeniorityDiagram2 = [
        # {"name": "3个月以下", "value": "0"},
        #   {"name": "3个月~1年", "value": "64"},
        #   {"name": "1~2年", "value": "0"},
        #   {"name": "2~3年", "value": "1"},
        #   {"name": "3~5年", "value": ""},
        #   {"name": "5~10年", "value": ""},
        #   {"name": "10~15年", "value": ""},
        #   {"name": "15~20年", "value": ""},
        #   {"name": "20年以上", "value": ""}
    ]

    seniorityTable = [
        # {"seniority": "3个月以下", "A31": "0", "A32": "64", "C38": "0", "senioritySummary": "64",
        #  "seniorityDeparture": "15.7%"},
        # {"seniority": "3个月~1年", "A31": "18", "A32": "30", "C38": "23", "senioritySummary": "71",
        #  "seniorityDeparture": "14.7%"},
        # {"seniority": "1~2年", "A31": "59", "A32": "83", "C38": "63", "senioritySummary": "205",
        #  "seniorityDeparture": "30.9%"},
        # {"seniority": "2~3年", "A31": "43", "A32": "35", "C38": "26", "senioritySummary": "104",
        #  "seniorityDeparture": "11.3%"},
        # {"seniority": "3~5年", "A31": "33", "A32": "34", "C38": "41", "senioritySummary": "108",
        #  "seniorityDeparture": "23.5%"},
        # {"seniority": "5~10年", "A31": "20", "A32": "19", "C38": "24", "senioritySummary": "63",
        #  "seniorityDeparture": "2.0%"},
        # {"seniority": "10~15年", "A31": "25", "A32": "19", "C38": "25", "senioritySummary": "69",
        #  "seniorityDeparture": "2.0%"},
        # {"seniority": "15~20年", "A31": "2", "A32": "6", "C38": "4", "senioritySummary": "12",
        #  "seniorityDeparture": "0.0%"},
        # {"seniority": "20年以上", "A31": "1", "A32": "1", "C38": "1", "senioritySummary": "3",
        #  "seniorityDeparture": "0.0%"}
    ]
    seniorityTitleData = [
        # "助技員", "技術員", "助工師", "工程師", "資工師", "副課長", "課長", "襄理", "副理", "經理", "資深經理"
    ]
    seniorityTable1 = [
        # {"seniority": "3个月以下", "助技員": "0", "技術員": "64", "助工師": "0", "工程師": "1", "資工師": "", "副課長": "", "課長": "",
        #  "襄理": "", "副理": "", "經理": "64"},
        # {"seniority": "3个月~1年", "助技員": "18", "技術員": "30", "助工師": "23", "工程師": "", "資工師": "3", "副課長": "", "課長": "",
        #  "襄理": "", "副理": "", "經理": "71"},
        # {"seniority": "1~2年", "助技員": "59", "技術員": "83", "助工師": "63", "工程師": "", "資工師": "", "副課長": "", "課長": "",
        #  "襄理": "", "副理": "", "經理": "205"},
        # {"seniority": "2~3年", "助技員": "43", "技術員": "35", "助工師": "26", "工程師": "", "資工師": "", "副課長": "5", "課長": "",
        #  "襄理": "", "副理": "", "經理": "104"},
        # {"seniority": "3~5年", "助技員": "33", "技術員": "34", "助工師": "41", "工程師": "", "資工師": "", "副課長": "", "課長": "6",
        #  "襄理": "", "副理": "", "經理": "108"},
        # {"seniority": "5~10年", "助技員": "20", "技術員": "19", "助工師": "24", "工程師": "", "資工師": "", "副課長": "", "課長": "",
        #  "襄理": "", "副理": "", "經理": "63"},
        # {"seniority": "10~15年", "助技員": "25", "技術員": "19", "助工師": "25", "工程師": "", "資工師": "", "副課長": "", "課長": "",
        #  "襄理": "3", "副理": "42", "經理": "69"},
        # {"seniority": "15~20年", "助技員": "2", "技術員": "6", "助工師": "4", "工程師": "", "資工師": "", "副課長": "", "課長": "", "襄理": "",
        #  "副理": "", "經理": "12"},
        # {"seniority": "20年以上", "助技員": "1", "技術員": "1", "助工師": "1", "工程師": "", "資工師": "", "副課長": "", "課長": "", "襄理": "",
        #  "副理": "", "經理": "3"}
    ]
    seniorityDiagramData1 = {
        # 'LABEL': ["3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"],
        # 'HEJILIZHI': [86, 39, 23, 37, 11, 8, 0, 0],
        # 'LIZHIBI': [0.421568627, 0.191176471, 0.112745098, 0.181372549, 0.053921569, 0.039215686, 0, 0]
    }
    seniorityText = ""  # "三個月以下"
    SeniorityTitleDiagram0 = [
        # {"name": "助技員", "value": "0"},
        #   {"name": "技術員", "value": "64"},
        #   {"name": "助工師", "value": "0"},
        #   {"name": "工程師", "value": "1"},
        #   {"name": "資工師", "value": ""},
        #   {"name": "副課長", "value": ""},
        #   {"name": "課長", "value": ""},
        #   {"name": "襄理", "value": ""},
        #   {"name": "副理", "value": ""},
        #   {"name": "經理", "value": "64"},
        #   {"name": "資深經理", "value": ""}
    ]

    reasonTable = [
        # {"reason": "薪資福利", "reasonSummary": "24", "reasonDeparture": "25.00",},
    ]
    reasonDiagramData = {
        # 'LABEL': ["薪資福利", "家庭因素", "進修學習", "實習借宿"],
        # 'HEJIRENSHU': [86, 39, 23, 37, 11, 8, 0, 0],
        # 'YUANYINBI': [0.421568627, 0.191176471, 0.112745098, 0.181372549, 0.053921569, 0.039215686, 0, 0]
    }

    educationTable = [
        # {"Education": "本科", "A31": "149", "A32": "168", "C38": "178", "educationSummary": "495", "accountFor": ""},
        # {"Education": "大專", "A31": "53", "A32": "124", "C38": "28", "educationSummary": "205", "accountFor": ""},
        # {"Education": "中專", "A31": "1", "A32": "1", "C38": "0", "educationSummary": "2", "accountFor": ""}
    ]
    educationDiagram = {
        # "LABEL": ["本科", "大專", "中專"],
        # "educationDiagramHE": [495, 205, 2],  # 對應 從本科到中專
        # "educationDiagramZH": [0.705128205, 0.292022792, 0.002849003]
    }

    professionTable = [
        # {"daLei": "S.T.E.M", "Profession": "電氣信息類", "A31": "12", "A32": "54", "C38": "19", "professionSummary": "85"},
        # {"daLei": "S.T.E.M", "Profession": "機械類", "A31": "23", "A32": "99", "C38": "42", "professionSummary": "164"},
        # {"daLei": "S.T.E.M", "Profession": "電子信息科學類", "A31": "", "A32": "", "C38": "", "professionSummary": ""},
        # {"daLei": "Non S.T.E.M", "Profession": "管理科學與工程類", "A31": "63", "A32": "58", "C38": "43",
        #  "professionSummary": "164"},
        # {"daLei": "Non S.T.E.M", "Profession": "自動化類", "A31": "24", "A32": "8", "C38": "13", "professionSummary": "45"},
        # {"daLei": "Non S.T.E.M", "Profession": "數學類", "A31": "21", "A32": "23", "C38": "22", "professionSummary": "66"},
        # {"daLei": "Non S.T.E.M", "Profession": "物理學類", "A31": "35", "A32": "25", "C38": "39",
        #  "professionSummary": "99"},
        # {"daLei": "Non S.T.E.M", "Profession": "工商管理類", "A31": "20", "A32": "22", "C38": "23",
        #  "professionSummary": "65"},
        # {"daLei": "Non S.T.E.M", "Profession": "材料類", "A31": "5", "A32": "2", "C38": "8", "professionSummary": "15"}
    ]
    # heBingNum = {"STEM": 3, "NON_STEM": 6}  # 要合併的行數
    heBingNum = [
        # 3, 6
    ]  # 要合併的行數
    regionsTable = [
        # {"Regions": "江蘇", "A31": "12", "A32": "54", "C38": "19", "regionsSummary": "85"},
        #             {"Regions": "安徽", "A31": "23", "A32": "99", "C38": "42", "regionsSummary": "164"},
        #             {"Regions": "山東", "A31": "", "A32": "", "C38": "", "regionsSummary": ""},
        #             {"Regions": "四川", "A31": "63", "A32": "58", "C38": "43", "regionsSummary": "164"},
        #             {"Regions": "黑龍江", "A31": "24", "A32": "8", "C38": "13", "regionsSummary": "45"},
        #             {"Regions": "山西", "A31": "21", "A32": "23", "C38": "22", "regionsSummary": "66"},
        #             {"Regions": "河南", "A31": "35", "A32": "25", "C38": "39", "regionsSummary": "99"},
        #             {"Regions": "陝西", "A31": "20", "A32": "22", "C38": "23", "regionsSummary": "65"},
        #             {"Regions": "甘肅", "A31": "5", "A32": "2", "C38": "8", "regionsSummary": "15"}
    ]
    canExport = 0  # 0為DQA權限，可以導出

    onlineuser = request.session.get('account')
    roles = []
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i:
            canExport = 0
        elif 'Department' in i:
            canExport = 1
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            YearSearch = request.POST.get("Year")  # 为空
            YearNow = str(datetime.datetime.now().year)
            # 离职人员信息
            if not YearSearch or YearSearch == YearNow:
                for Per in PersonalInfo.objects.filter(Status="離職"):
                    Seniority = round(
                        float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                    perinTable.append(
                        {"RegistrationDate": Per.RegistrationDate.strftime('%Y-%m-%d'), "Seniority": Seniority,
                         "Customer": Per.Customer, "Department": Per.Department,
                         "Lesson": Per.DepartmentCode, "GroupEmployees": Per.GroupNum, "ChineseName": Per.CNName,
                         "EnglishName": Per.EngName,
                         "Gender": Per.Sex, "CurrentTitle": Per.PositionNow,
                         "DepartureDate": Per.QuitDate.strftime('%Y-%m-%d'),
                         # "LastPerformance": "B",
                         "DepartureReasons": Per.Whereabouts}
                    )
            else:
                for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]):
                    Seniority = round(
                        float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                    perinTable.append(
                        {"RegistrationDate": Per.RegistrationDate.strftime('%Y-%m-%d'), "Seniority": Seniority,
                         "Customer": Per.Customer,
                         "Department": Per.Department,
                         "Lesson": Per.DepartmentCode, "GroupEmployees": Per.GroupNum, "ChineseName": Per.CNName,
                         "EnglishName": Per.EngName,
                         "Gender": Per.Sex, "CurrentTitle": Per.PositionNow,
                         "DepartureDate": Per.QuitDate.strftime('%Y-%m-%d'),
                         # "LastPerformance": "B",
                         "DepartureReasons": Per.Whereabouts}
                    )

            # 離職去向分析
            if not YearSearch or YearSearch == YearNow:
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    selectItem.append(i["Customer"])
                reasonsSummaryTotal = 0
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values(
                        "Whereabouts").distinct().order_by(
                    "Whereabouts"):
                    reasonsTable_dict = {"Reasons": i["Whereabouts"]}
                    reasonsSummary = 0
                    for j in selectItem:
                        reasonsTable_dict[j] = PersonalInfo.objects.filter(Status__in=["離職"], Customer=j,
                                                                           Whereabouts=i["Whereabouts"]).count()
                        reasonsSummary += reasonsTable_dict[j]
                    reasonsTable_dict["reasonsSummary"] = reasonsSummary
                    reasonsTable.append(reasonsTable_dict)
                    reasonsSummaryTotal += reasonsSummary
            else:
                titleDiagramname = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItem.append(i["Customer"])
                reasonsSummaryTotal = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Whereabouts").distinct().order_by("Whereabouts"):
                    reasonsTable_dict = {"Reasons": i["Whereabouts"]}
                    reasonsSummary = 0
                    for j in selectItem:
                        reasonsTable_dict[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                    Status__in=["離職"],
                                                                                    Customer=j, Whereabouts=i[
                                "Whereabouts"]).count()
                        reasonsSummary += reasonsTable_dict[j]
                    reasonsTable_dict["reasonsSummary"] = reasonsSummary
                    reasonsTable.append(reasonsTable_dict)
                    reasonsSummaryTotal += reasonsSummary
            # zhanReasons
            if reasonsSummaryTotal:
                for i in reasonsTable:
                    i["zhanReasons"] = round(float(i["reasonsSummary"] / reasonsSummaryTotal * 100), 4)  # %分數
                    # print(round(float(i["reasonsSummary"] / reasonsSummaryTotal), 3), reasonsSummaryTotal, i["reasonsSummary"], i["zhanReasons"])
            # reasonsDiagramData
            LABEL = []
            HEJI = []
            ZHANZONG = []
            for i in reasonsTable:
                LABEL.append(i["Reasons"])
                HEJI.append(i["reasonsSummary"])
                ZHANZONG.append(round(i["zhanReasons"] / 100, 4))
            reasonsDiagramData["LABEL"] = LABEL
            reasonsDiagramData["HEJI"] = HEJI
            reasonsDiagramData["ZHANZONG"] = ZHANZONG

            # 職稱
            if not YearSearch or YearSearch == YearNow:
                YearSearch = YearNow
                selectItemzhicheng = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    selectItemzhicheng.append(i["Customer"])
                titleDiagram2Data_LABLE = []
                titleDiagram2Data_Position = []
                PositionQuerySet = PersonalInfo.objects.filter(Status__in=["離職"]).values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleDiagram2Data_LABLE.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                    titleDiagram2Data_Position.append(i["PositionNow"])
                # titleTable
                titleSummary_Total = 0
                for i in Positionlistnew:
                    titleTable_dict = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItemzhicheng:
                        titleTable_dict[j] = PersonalInfo.objects.filter(Status__in=["離職"], Customer=j,
                                                                         PositionNow=i["PositionNow"]).count()
                        titleSummary += titleTable_dict[j]
                    titleTable_dict["titleSummary"] = titleSummary
                    titleSummary_Total += titleSummary
                    titleTable.append(titleTable_dict)
                # titleSeniorityData&titleTable1
                titleSeniorityData = [
                    "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                ]
                for j in titleDiagram2Data_Position:
                    titleTable1_dict = {}
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(PositionNow=j, Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                          Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                        '2~3年': number2_3, '3~5年': number3_5,
                                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                        '20年以上': number20,
                                        "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                    titleTable1.append(titleTable1_dict)
            else:
                selectItemzhicheng = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItemzhicheng.append(i["Customer"])
                titleDiagram2Data_LABLE = []
                titleDiagram2Data_Position = []
                PositionQuerySet = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleDiagram2Data_LABLE.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", )
                    titleDiagram2Data_Position.append(i["PositionNow"])
                # titleTable
                titleSummary_Total = 0
                for i in Positionlistnew:
                    titleTable_dict = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItemzhicheng:
                        titleTable_dict[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                                  Customer=j,
                                                                                  PositionNow=i["PositionNow"]).count()
                        titleSummary += titleTable_dict[j]
                    titleTable_dict["titleSummary"] = titleSummary
                    titleSummary_Total += titleSummary
                    titleTable.append(titleTable_dict)
                # titleSeniorityData&titleTable1
                titleSeniorityData = [
                    "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                ]
                for j in titleDiagram2Data_Position:
                    titleTable1_dict = {}
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, PositionNow=j,
                                                                    Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                          Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                        '2~3年': number2_3, '3~5年': number3_5,
                                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                        '20年以上': number20,
                                        "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                    titleTable1.append(titleTable1_dict)
            # titleDeparture
            for i in titleTable:
                if titleSummary_Total:
                    i["titleDeparture"] = '%.2f%%' % round(float(i["titleSummary"] / titleSummary_Total * 100), 4)
                else:
                    i["titleDeparture"] = '%.2f%%' % round(0, 1)
            # titleDiagram2Data
            LABEL_titleDiagram2Data = []
            HEJILIZHI_titleDiagram2Data = []
            LIZHIBI_titleDiagram2Data = []
            for i in titleTable:
                LABEL_titleDiagram2Data.append(i["Title"])
                HEJILIZHI_titleDiagram2Data.append(i["titleSummary"])
                # LIZHIBI_titleDiagram2Data.append(round(float(i["titleDeparture"].split("%")[0]), 4))
                LIZHIBI_titleDiagram2Data.append(i["titleDeparture"])
            titleDiagram2Data["LABEL"] = LABEL_titleDiagram2Data
            titleDiagram2Data["HEJILIZHI"] = HEJILIZHI_titleDiagram2Data
            titleDiagram2Data["LIZHIBI"] = LIZHIBI_titleDiagram2Data
            # TitleText&titleSeniorityDiagram2
            if titleTable1:
                TitleText = titleTable1[0]["Title"]
                titleSeniorityDiagram2 = [
                    {"name": "3个月以下", "value": titleTable1[0]["3个月以下"]},
                    {"name": "3个月~1年", "value": titleTable1[0]["3个月~1年"]},
                    {"name": "1~2年", "value": titleTable1[0]["1~2年"]},
                    {"name": "2~3年", "value": titleTable1[0]["2~3年"]},
                    {"name": "3~5年", "value": titleTable1[0]["3~5年"]},
                    {"name": "5~10年", "value": titleTable1[0]["5~10年"]},
                    {"name": "10~15年", "value": titleTable1[0]["10~15年"]},
                    {"name": "15~20年", "value": titleTable1[0]["15~20年"]},
                    {"name": "20年以上", "value": titleTable1[0]["20年以上"]}
                ]

            # 年资
            seniorityDiagramname = ['3个月以下', '3个月~1年', '1~2年', '2~3年', '3~5年', '5~10年', '10~15年', "15~20年", '20年以上']
            if not YearSearch or YearSearch == YearNow:
                selectItem_seniorityTable = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    selectItem_seniorityTable.append(i["Customer"])
                seniorityTable1_Positioncode = []
                seniorityTable1_Position = []
                YearSearch = YearNow
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("PositionNow").distinct().order_by(
                        "PositionNow"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    seniorityTable1_Positioncode.append(i["PositionNow"])
                    seniorityTable1_Position.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                CustomerSeniorityData = {
                    # "C38": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in selectItem_seniorityTable:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(Customer=i, Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[i] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(CustomerSeniorityData)
                senioritySummary_Total = 0
                for i in seniorityDiagramname:
                    seniorityTable_dict = {"seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_dict[key] = value[i]
                        senioritySummary += seniorityTable_dict[key]
                    seniorityTable_dict["senioritySummary"] = senioritySummary
                    seniorityTable.append(seniorityTable_dict)
                    senioritySummary_Total += senioritySummary
                if senioritySummary_Total:
                    for i in seniorityTable:
                        i["seniorityDeparture"] = '%.2f%%' % round(
                            float(i["senioritySummary"] / senioritySummary_Total * 100), 4)
                # print(seniorityTable)
                # seniorityTable1
                seniorityTitleData = seniorityTable1_Position
                PositionSeniorityData = {
                    # "技术员": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in seniorityTable1_Positioncode:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(PositionNow=i, Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    PositionSeniorityData[Positions.objects.filter(Item=i,
                                                                   Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i, Year=YearSearch).first() else "沒有該年份的對應職稱"] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(PositionSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable1_dict = {"seniority": i}
                    for key, value in PositionSeniorityData.items():
                        seniorityTable1_dict[key] = value[i]
                    seniorityTable1_dict["senioritySummary"] = senioritySummary
                    seniorityTable1.append(seniorityTable1_dict)
            else:
                selectItem_seniorityTable = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    selectItem_seniorityTable.append(i["Customer"])
                seniorityTable1_Positioncode = []
                seniorityTable1_Position = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "PositionNow").distinct().order_by(
                    "PositionNow"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    seniorityTable1_Positioncode.append(i["PositionNow"])
                    seniorityTable1_Position.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                CustomerSeniorityData = {
                    # "C38": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in selectItem_seniorityTable:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Customer=i, Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[i] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(CustomerSeniorityData)
                senioritySummary_Total = 0
                for i in seniorityDiagramname:
                    seniorityTable_dict = {"seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_dict[key] = value[i]
                        senioritySummary += seniorityTable_dict[key]
                    seniorityTable_dict["senioritySummary"] = senioritySummary
                    seniorityTable.append(seniorityTable_dict)
                    senioritySummary_Total += senioritySummary
                if senioritySummary_Total:
                    for i in seniorityTable:
                        i["seniorityDeparture"] = '%.2f%%' % round(
                            float(i["senioritySummary"] / senioritySummary_Total * 100), 4)
                # print(seniorityTable)
                # seniorityTable1
                seniorityTitleData = seniorityTable1_Position
                PositionSeniorityData = {
                    # "技术员": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in seniorityTable1_Positioncode:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, PositionNow=i,
                                                                    Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    PositionSeniorityData[Positions.objects.filter(Item=i,
                                                                   Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i, Year=YearSearch).first() else "沒有該年份的對應職稱"] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(PositionSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable1_dict = {"seniority": i}
                    for key, value in PositionSeniorityData.items():
                        seniorityTable1_dict[key] = value[i]
                    seniorityTable1_dict["senioritySummary"] = senioritySummary
                    seniorityTable1.append(seniorityTable1_dict)
            # seniorityDiagramData1
            LABEL_seniorityDiagramData1 = []
            HEJILIZHI_seniorityDiagramData1 = []
            LIZHIBI_seniorityDiagramData1 = []

            for i in seniorityTable:
                # print(i)
                LABEL_seniorityDiagramData1.append(i["seniority"])
                HEJILIZHI_seniorityDiagramData1.append(i["senioritySummary"])
                if "seniorityDeparture" in i.keys():
                    # LIZHIBI_seniorityDiagramData1.append(round(float(i["seniorityDeparture"].split("%")[0]), 4))
                    LIZHIBI_seniorityDiagramData1.append(i["seniorityDeparture"])
            seniorityDiagramData1["LABEL"] = LABEL_seniorityDiagramData1
            seniorityDiagramData1["HEJILIZHI"] = HEJILIZHI_seniorityDiagramData1
            seniorityDiagramData1["LIZHIBI"] = LIZHIBI_seniorityDiagramData1
            # seniorityText&SeniorityTitleDiagram0
            if seniorityTable1:
                seniorityText = seniorityTable1[0]["seniority"]
                for i in seniorityTitleData:
                    SeniorityTitleDiagram0.append({"name": i, "value": seniorityTable1[0][i]})

            # 離職原因
            if not YearSearch or YearSearch == YearNow:
                reasonSummaryTotal = 0
                if PersonalInfo.objects.filter(Status__in=["離職"]).values(
                        "QuitReason").distinct():
                    for i in PersonalInfo.objects.filter(Status__in=["離職"]).values(
                            "QuitReason").distinct().order_by(
                        "QuitReason"):
                        # print(i["QuitReason"])
                        reasonTable_dict = {"reason": i["QuitReason"]}
                        reasonTable_dict['reasonSummary'] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                        QuitReason=i[
                                                                                            "QuitReason"]).count()
                        reasonTable_dict['reasonDeparture'] = '%.2f%%' % round(
                            float(PersonalInfo.objects.filter(Status__in=["離職"],
                                                              QuitReason=i[
                                                                  "QuitReason"]).count() / PersonalInfo.objects.filter(
                                Status__in=["離職"], ).count() * 100), 4)

                        reasonTable.append(reasonTable_dict)
            else:
                if PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "QuitReason").distinct():
                    for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                            "QuitReason").distinct().order_by("QuitReason"):
                        reasonTable_dict = {"reason": i["QuitReason"]}
                        reasonsSummary = 0
                        reasonTable_dict['reasonSummary'] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                                 Status__in=["離職"],
                                                                                                 QuitReason=i[
                                                                                                     "QuitReason"]).count()
                        reasonTable_dict['reasonDeparture'] = '%.2f%%' % round(
                            float(PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                       QuitReason=i[
                                                                           "QuitReason"]).count() / PersonalInfoHisByYear.objects.filter(
                                Year=YearSearch,
                                Status__in=["離職"], ).count() * 100), 4)

                        reasonTable.append(reasonTable_dict)

            # reasonDiagramData
            LABEL = []
            HEJIRENSHU = []
            YUANYINBI = []
            if reasonTable:
                for i in reasonTable:
                    LABEL.append(i["reason"])
                    HEJIRENSHU.append(i["reasonSummary"])
                    YUANYINBI.append(i["reasonDeparture"])
            reasonDiagramData["LABEL"] = LABEL
            reasonDiagramData["HEJIRENSHU"] = HEJIRENSHU
            reasonDiagramData["YUANYINBI"] = YUANYINBI

            # 學歷
            if not YearSearch or YearSearch == YearNow:
                educationSummary_Total = 0
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Education").distinct().order_by(
                        "Education"):
                    educationTable_dict = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                            "Customer"):
                        educationTable_dict[j["Customer"]] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                         Education=i["Education"],
                                                                                         Customer=j[
                                                                                             "Customer"]).count()
                        educationSummary += educationTable_dict[j["Customer"]]
                    educationTable_dict["educationSummary"] = educationSummary
                    educationSummary_Total += educationSummary
                    educationTable.append(educationTable_dict)
                if educationSummary_Total:
                    for i in educationTable:
                        i["accountFor"] = round(i["educationSummary"] / educationSummary_Total * 100, 4)
            else:
                educationSummary_Total = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Education").distinct().order_by(
                    "Education"):
                    educationTable_dict = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                            "Customer").distinct().order_by(
                        "Customer"):
                        educationTable_dict[j["Customer"]] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                                  Status__in=["離職"],
                                                                                                  Education=i[
                                                                                                      "Education"],
                                                                                                  Customer=j[
                                                                                                      "Customer"]).count()
                        educationSummary += educationTable_dict[j["Customer"]]
                    educationTable_dict["educationSummary"] = educationSummary
                    educationSummary_Total += educationSummary
                    educationTable.append(educationTable_dict)
                if educationSummary_Total:
                    for i in educationTable:
                        i["accountFor"] = round(i["educationSummary"] / educationSummary_Total * 100, 4)
            # educationDiagram
            LABEL_educationDiagram = []
            educationDiagramHE_educationDiagram = []
            educationDiagramZH_educationDiagram = []
            for i in educationTable:
                LABEL_educationDiagram.append(i["Education"])
                educationDiagramHE_educationDiagram.append(i["educationSummary"])
                educationDiagramZH_educationDiagram.append(round(i["accountFor"] / 100, 4))
            educationDiagram = {
                "LABEL": LABEL_educationDiagram,
                "educationDiagramHE": educationDiagramHE_educationDiagram,  # 對應 從本科到中專
                "educationDiagramZH": educationDiagramZH_educationDiagram
            }

            # 專業
            if not YearSearch or YearSearch == YearNow:
                Customer_major = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                print(PersonalInfo.objects.filter(Status__in=["離職"]).values("Education",
                                                                            "Major").distinct().count(),
                      MajorIfo.objects.all().values("Education", "Major").count())
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Education",
                                                                               "Major").distinct().order_by(
                    "Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                 Education__contains=i["Education"],
                                                                                 Major=i["Major"],
                                                                                 Customer=j).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfoHisByYear.objects.filter(Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status__in=["離職"]).count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
            else:
                Customer_major = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Education", "Major").distinct().order_by("Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                          Status__in=["離職"],
                                                                                          Education=i["Education"],
                                                                                          Major=i["Major"],
                                                                                          Customer=j).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status__in=["離職"]).count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
            if MajorIfo.objects.filter(Education__contains=i["Education"],
                                       Major="TBC").first():
                professionTableData_TBC = {
                    "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                     Major="TBC").first().Categories,
                    "Profession": "TBC",
                }
                # print(TBCnum)
                TBCnum_professionSummary = 0
                for j in Customer_major:
                    professionTableData_TBC[j] = 0
                    for i in TBCnum:
                        professionTableData_TBC[j] += i[j]
                        TBCnum_professionSummary += i["professionSummary"]
                professionTableData_TBC["professionSummary"] = TBCnum_professionSummary
                professionTable.append(professionTableData_TBC)
            professionTable = sorted(professionTable,
                                     key=lambda e: (e.__getitem__('daLei'), e.__getitem__('professionSummary')),
                                     reverse=True)
            # heBingNum
            professionTablenew = []
            for i in professionTable:
                professionTablenew.append(i["daLei"])
            professionTable_counter = Counter(professionTablenew)
            # print(professionTable)
            # print(professionTable_counter)
            # print(dict(professionTable_counter))
            # heBing里的数值与professionTable["daLei"] 的value排序保持一致
            heBingNum_sort = sorted(dict(professionTable_counter).items(), key=lambda e: e[0], reverse=True)
            # print(heBingNum_sort)
            for i in heBingNum_sort:
                heBingNum.append(i[1])

            # 地區
            if not YearSearch or YearSearch == YearNow:
                Customer_region = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values(
                        "NativeProvince").distinct().order_by(
                    "NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                          NativeProvince=i["NativeProvince"],
                                                                          Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            else:
                Customer_region = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "NativeProvince").distinct().order_by("NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                   Status__in=["離職"],
                                                                                   NativeProvince=i[
                                                                                       "NativeProvince"],
                                                                                   Customer=j).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            regionsTable = sorted(regionsTable, key=lambda x: x.__getitem__("regionsSummary"), reverse=True)

        if request.POST.get("isGetData") == "SEARCH":
            YearSearch = request.POST.get("Year")
            YearNow = str(datetime.datetime.now().year)
            Search_Endperiod = request.POST.getlist("YearRange",
                                                    ['0000-00-00', '0000-00-00'])  # 经尝试这个默认值与没有这个搜索条件是一样的效果
            print(Search_Endperiod)
            if Search_Endperiod == ['']:
                # print(PersonalInfo.objects.exclude(QuitDate=None).values("QuitDate").distinct().order_by("QuitDate"))
                if PersonalInfo.objects.exclude(QuitDate=None).values("QuitDate").distinct().order_by("QuitDate"):
                    Search_start = PersonalInfo.objects.exclude(QuitDate=None).values("QuitDate").distinct().order_by(
                        "QuitDate").first()["QuitDate"].strftime("%Y-%m-%d")
                if PersonalInfoHisByYear.objects.exclude(QuitDate=None).values("QuitDate").distinct().order_by(
                        "QuitDate"):
                    Search_start = \
                        PersonalInfoHisByYear.objects.exclude(QuitDate=None).values("QuitDate").distinct().order_by(
                            "QuitDate").first()["QuitDate"].strftime("%Y-%m-%d")
                Search_Endperiod = [Search_start, datetime.datetime.now().strftime("%Y-%m-%d")]
            # print(Search_Endperiod)

            # 离职人员信息
            if not YearSearch or YearSearch == YearNow:
                for Per in PersonalInfo.objects.filter(Status__in=["離職"], QuitDate__range=Search_Endperiod):
                    Seniority = round(
                        float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                    perinTable.append(
                        {"RegistrationDate": Per.RegistrationDate.strftime('%Y-%m-%d'), "Seniority": Seniority,
                         "Customer": Per.Customer, "Department": Per.Department,
                         "Lesson": Per.DepartmentCode, "GroupEmployees": Per.GroupNum, "ChineseName": Per.CNName,
                         "EnglishName": Per.EngName,
                         "Gender": Per.Sex, "CurrentTitle": Per.PositionNow,
                         "DepartureDate": Per.QuitDate.strftime('%Y-%m-%d'),
                         # "LastPerformance": "B",
                         "DepartureReasons": Per.Whereabouts}
                    )
            else:
                for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                QuitDate__range=Search_Endperiod):
                    Seniority = round(
                        float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                    perinTable.append(
                        {"RegistrationDate": Per.RegistrationDate.strftime('%Y-%m-%d'), "Seniority": Seniority,
                         "Customer": Per.Customer,
                         "Department": Per.Department,
                         "Lesson": Per.DepartmentCode, "GroupEmployees": Per.GroupNum, "ChineseName": Per.CNName,
                         "EnglishName": Per.EngName,
                         "Gender": Per.Sex, "CurrentTitle": Per.PositionNow,
                         "DepartureDate": Per.QuitDate.strftime('%Y-%m-%d'),
                         # "LastPerformance": "B",
                         "DepartureReasons": Per.Whereabouts}
                    )
            # print(perinTable)

            # 離職去向分析
            if not YearSearch or YearSearch == YearNow:
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    selectItem.append(i["Customer"])
                reasonsSummaryTotal = 0
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Whereabouts").distinct().order_by(
                        "Whereabouts"):
                    reasonsTable_dict = {"Reasons": i["Whereabouts"]}
                    reasonsSummary = 0
                    for j in selectItem:
                        reasonsTable_dict[j] = PersonalInfo.objects.filter(Status__in=["離職"], Customer=j,
                                                                           Whereabouts=i["Whereabouts"],
                                                                           QuitDate__range=Search_Endperiod).count()
                        reasonsSummary += reasonsTable_dict[j]
                    reasonsTable_dict["reasonsSummary"] = reasonsSummary
                    reasonsTable.append(reasonsTable_dict)
                    reasonsSummaryTotal += reasonsSummary
            else:
                titleDiagramname = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItem.append(i["Customer"])
                reasonsSummaryTotal = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Whereabouts").distinct().order_by("Whereabouts"):
                    reasonsTable_dict = {"Reasons": i["Whereabouts"]}
                    reasonsSummary = 0
                    for j in selectItem:
                        reasonsTable_dict[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                                    Customer=j, Whereabouts=i[
                                "Whereabouts"], QuitDate__range=Search_Endperiod).count()
                        reasonsSummary += reasonsTable_dict[j]
                    reasonsTable_dict["reasonsSummary"] = reasonsSummary
                    reasonsTable.append(reasonsTable_dict)
                    reasonsSummaryTotal += reasonsSummary
            # zhanReasons
            if reasonsSummaryTotal:
                for i in reasonsTable:
                    i["zhanReasons"] = round(float(i["reasonsSummary"] / reasonsSummaryTotal * 100), 4)  # %分數
            # reasonsDiagramData
            LABEL = []
            HEJI = []
            ZHANZONG = []
            for i in reasonsTable:
                # print(i)
                LABEL.append(i["Reasons"])
                HEJI.append(i["reasonsSummary"])
                if reasonsSummaryTotal:
                    ZHANZONG.append(round(i["zhanReasons"] / 100, 4))
            reasonsDiagramData["LABEL"] = LABEL
            reasonsDiagramData["HEJI"] = HEJI
            reasonsDiagramData["ZHANZONG"] = ZHANZONG

            # 職稱
            if not YearSearch or YearSearch == YearNow:
                selectItemzhicheng = []
                YearSearch = YearNow
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    selectItemzhicheng.append(i["Customer"])
                titleDiagram2Data_LABLE = []
                titleDiagram2Data_Position = []
                PositionQuerySet = PersonalInfo.objects.filter(Status__in=["離職"],
                                                               QuitDate__range=Search_Endperiod).values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱項次"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleDiagram2Data_LABLE.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                    titleDiagram2Data_Position.append(i["PositionNow"])
                # titleTable
                titleSummary_Total = 0
                for i in Positionlistnew:
                    titleTable_dict = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItemzhicheng:
                        titleTable_dict[j] = PersonalInfo.objects.filter(Status__in=["離職"], Customer=j,
                                                                         QuitDate__range=Search_Endperiod,
                                                                         PositionNow=i["PositionNow"]).count()
                        titleSummary += titleTable_dict[j]
                    titleTable_dict["titleSummary"] = titleSummary
                    titleSummary_Total += titleSummary
                    titleTable.append(titleTable_dict)
                # titleSeniorityData&titleTable1
                titleSeniorityData = [
                    "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                ]
                for j in titleDiagram2Data_Position:
                    titleTable1_dict = {}
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(PositionNow=j, Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                          Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                        '2~3年': number2_3, '3~5年': number3_5,
                                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                        '20年以上': number20,
                                        "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                    titleTable1.append(titleTable1_dict)
            else:
                selectItemzhicheng = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    selectItemzhicheng.append(i["Customer"])
                titleDiagram2Data_LABLE = []
                titleDiagram2Data_Position = []
                PositionQuerySet = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                        QuitDate__range=Search_Endperiod).values(
                    "PositionNow").distinct().order_by(
                    "PositionNow").annotate(entry_Code=Value('', CharField()))
                for i in PositionQuerySet:
                    i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                               Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱"
                # print(type(Positionlist), Positionlist)
                # print(list(PositionQuerySet))
                Positionlist = list(PositionQuerySet)
                Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                # print(Positionlistnew)
                for i in Positionlistnew:
                    titleDiagram2Data_LABLE.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                    titleDiagram2Data_Position.append(i["PositionNow"])
                # titleTable
                titleSummary_Total = 0
                for i in Positionlistnew:
                    titleTable_dict = {"Title": Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                    titleSummary = 0
                    for j in selectItemzhicheng:
                        titleTable_dict[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                                  Customer=j,
                                                                                  PositionNow=i["PositionNow"]).count()
                        titleSummary += titleTable_dict[j]
                    titleTable_dict["titleSummary"] = titleSummary
                    titleSummary_Total += titleSummary
                    titleTable.append(titleTable_dict)
                # titleSeniorityData&titleTable1
                titleSeniorityData = [
                    "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                ]
                for j in titleDiagram2Data_Position:
                    titleTable1_dict = {}
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, PositionNow=j,
                                                                    Status__in=["離職"], ):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                          Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                        '2~3年': number2_3, '3~5年': number3_5,
                                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                        '20年以上': number20,
                                        "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                    titleTable1.append(titleTable1_dict)
            # titleDeparture
            for i in titleTable:
                if titleSummary_Total:
                    i["titleDeparture"] = '%.2f%%' % round(float(i["titleSummary"] / titleSummary_Total * 100), 4)
                else:
                    i["titleDeparture"] = '%.2f%%' % round(0, 1)
            # titleDiagram2Data
            LABEL_titleDiagram2Data = []
            HEJILIZHI_titleDiagram2Data = []
            LIZHIBI_titleDiagram2Data = []
            for i in titleTable:
                LABEL_titleDiagram2Data.append(i["Title"])
                HEJILIZHI_titleDiagram2Data.append(i["titleSummary"])
                # LIZHIBI_titleDiagram2Data.append(round(float(i["titleDeparture"].split("%")[0]), 4))
                LIZHIBI_titleDiagram2Data.append(i["titleDeparture"])
            titleDiagram2Data["LABEL"] = LABEL_titleDiagram2Data
            titleDiagram2Data["HEJILIZHI"] = HEJILIZHI_titleDiagram2Data
            titleDiagram2Data["LIZHIBI"] = LIZHIBI_titleDiagram2Data
            # TitleText&titleSeniorityDiagram2
            if titleTable1:
                TitleText = titleTable1[0]["Title"]
                titleSeniorityDiagram2 = [
                    {"name": "3个月以下", "value": titleTable1[0]["3个月以下"]},
                    {"name": "3个月~1年", "value": titleTable1[0]["3个月~1年"]},
                    {"name": "1~2年", "value": titleTable1[0]["1~2年"]},
                    {"name": "2~3年", "value": titleTable1[0]["2~3年"]},
                    {"name": "3~5年", "value": titleTable1[0]["3~5年"]},
                    {"name": "5~10年", "value": titleTable1[0]["5~10年"]},
                    {"name": "10~15年", "value": titleTable1[0]["10~15年"]},
                    {"name": "15~20年", "value": titleTable1[0]["15~20年"]},
                    {"name": "20年以上", "value": titleTable1[0]["20年以上"]}
                ]

            # 年资
            seniorityDiagramname = ['3个月以下', '3个月~1年', '1~2年', '2~3年', '3~5年', '5~10年', '10~15年', "15~20年", '20年以上']
            if not YearSearch or YearSearch == YearNow:
                YearSearch = YearNow
                selectItem_seniorityTable = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    selectItem_seniorityTable.append(i["Customer"])
                seniorityTable1_Positioncode = []
                seniorityTable1_Position = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("PositionNow").distinct().order_by(
                        "PositionNow"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    seniorityTable1_Positioncode.append(i["PositionNow"])
                    seniorityTable1_Position.append(Positions.objects.filter(Item=i["PositionNow"],
                                                                             Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                CustomerSeniorityData = {
                    # "C38": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in selectItem_seniorityTable:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(Customer=i, Status__in=["離職"],
                                                           QuitDate__range=Search_Endperiod):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[i] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(CustomerSeniorityData)
                senioritySummary_Total = 0
                for i in seniorityDiagramname:
                    seniorityTable_dict = {"seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_dict[key] = value[i]
                        senioritySummary += seniorityTable_dict[key]
                    seniorityTable_dict["senioritySummary"] = senioritySummary
                    seniorityTable.append(seniorityTable_dict)
                    senioritySummary_Total += senioritySummary
                if senioritySummary_Total:
                    for i in seniorityTable:
                        i["seniorityDeparture"] = '%.2f%%' % round(
                            float(i["senioritySummary"] / senioritySummary_Total * 100), 4)
                # print(seniorityTable)
                # seniorityTable1
                seniorityTitleData = seniorityTable1_Position
                PositionSeniorityData = {
                    # "技术员": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in seniorityTable1_Positioncode:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfo.objects.filter(PositionNow=i, Status__in=["離職"],
                                                           QuitDate__range=Search_Endperiod):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    PositionSeniorityData[Positions.objects.filter(Item=i,
                                                                   Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i, Year=YearSearch).first() else "沒有該年份的對應職稱"] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(PositionSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable1_dict = {"seniority": i}
                    for key, value in PositionSeniorityData.items():
                        seniorityTable1_dict[key] = value[i]
                    seniorityTable1_dict["senioritySummary"] = senioritySummary
                    seniorityTable1.append(seniorityTable1_dict)
            else:
                selectItem_seniorityTable = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    selectItem_seniorityTable.append(i["Customer"])
                seniorityTable1_Positioncode = []
                seniorityTable1_Position = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "PositionNow").distinct().order_by(
                    "PositionNow"):
                    # selectItem.append(i["Customer"])#前端是用的同一个
                    seniorityTable1_Positioncode.append(i["PositionNow"])
                    seniorityTable1_Position.append(
                        Positions.objects.filter(Item=i["PositionNow"],
                                                 Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                CustomerSeniorityData = {
                    # "C38": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in selectItem_seniorityTable:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Customer=i, Status__in=["離職"],
                                                                    QuitDate__range=Search_Endperiod):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    CustomerSeniorityData[i] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(CustomerSeniorityData)
                senioritySummary_Total = 0
                for i in seniorityDiagramname:
                    seniorityTable_dict = {"seniority": i}
                    senioritySummary = 0
                    for key, value in CustomerSeniorityData.items():
                        seniorityTable_dict[key] = value[i]
                        senioritySummary += seniorityTable_dict[key]
                    seniorityTable_dict["senioritySummary"] = senioritySummary
                    seniorityTable.append(seniorityTable_dict)
                    senioritySummary_Total += senioritySummary
                if senioritySummary_Total:
                    for i in seniorityTable:
                        i["seniorityDeparture"] = '%.2f%%' % round(
                            float(i["senioritySummary"] / senioritySummary_Total * 100), 4)
                # print(seniorityTable)
                # seniorityTable1
                seniorityTitleData = seniorityTable1_Position
                PositionSeniorityData = {
                    # "技术员": {"3个月以下": 20, "3个月~1年": 20, '1~2年': 20, '2~3年': 20, '3~5年': 20, '5~10年': 20, '10~15年': 20, "15~20年": 20, '20年以上': 20, }
                }
                for i in seniorityTable1_Positioncode:
                    number025 = 0
                    number025_1 = 0
                    number1_2 = 0
                    number2_3 = 0
                    number3_5 = 0
                    number5_10 = 0
                    number10_15 = 0
                    number15_20 = 0
                    number20 = 0
                    for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, PositionNow=i, Status__in=["離職"],
                                                                    QuitDate__range=Search_Endperiod):
                        # if Per.Status == "在職":
                        # Seniority = round(
                        #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                        #     1)
                        # else:
                        Seniority = round(
                            float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                        if Seniority <= 0.25:
                            number025 += 1
                        elif Seniority > 0.25 and Seniority <= 1:
                            number025_1 += 1
                        elif Seniority > 1 and Seniority <= 2:
                            number1_2 += 1
                        elif Seniority > 2 and Seniority <= 3:
                            number2_3 += 1
                        elif Seniority > 3 and Seniority <= 5:
                            number3_5 += 1
                        elif Seniority > 5 and Seniority <= 10:
                            number5_10 += 1
                        elif Seniority > 10 and Seniority <= 15:
                            number10_15 += 1
                        elif Seniority > 15 and Seniority <= 20:
                            number15_20 += 1
                        elif Seniority > 20:
                            number20 += 1
                    PositionSeniorityData[Positions.objects.filter(Item=i,
                                                                   Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                        Item=i, Year=YearSearch).first() else "沒有該年份的對應職稱"] = {
                        "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                        '2~3年': number2_3, '3~5年': number3_5,
                        '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                        '20年以上': number20,
                    }
                # print(PositionSeniorityData)
                for i in seniorityDiagramname:
                    seniorityTable1_dict = {"seniority": i}
                    for key, value in PositionSeniorityData.items():
                        seniorityTable1_dict[key] = value[i]
                    seniorityTable1_dict["senioritySummary"] = senioritySummary
                    seniorityTable1.append(seniorityTable1_dict)
            # seniorityDiagramData1
            LABEL_seniorityDiagramData1 = []
            HEJILIZHI_seniorityDiagramData1 = []
            LIZHIBI_seniorityDiagramData1 = []
            # print(seniorityTable)
            # for i in seniorityTable:
            #     LABEL_seniorityDiagramData1.append(i["seniority"])
            #     HEJILIZHI_seniorityDiagramData1.append(i["senioritySummary"])
            #     if "seniorityDeparture" in i.keys():
            #         LIZHIBI_seniorityDiagramData1.append(i["seniorityDeparture"])
            for i in seniorityTable:
                LABEL_seniorityDiagramData1.append(i["seniority"])
                HEJILIZHI_seniorityDiagramData1.append(i["senioritySummary"])
                if "seniorityDeparture" in i.keys():
                    # LIZHIBI_seniorityDiagramData1.append(round(float(i["seniorityDeparture"].split("%")[0]), 4))
                    LIZHIBI_seniorityDiagramData1.append(i["seniorityDeparture"])
            seniorityDiagramData1["LABEL"] = LABEL_seniorityDiagramData1
            seniorityDiagramData1["HEJILIZHI"] = HEJILIZHI_seniorityDiagramData1
            seniorityDiagramData1["LIZHIBI"] = LIZHIBI_seniorityDiagramData1
            # seniorityText&SeniorityTitleDiagram0
            if seniorityTable1:
                seniorityText = seniorityTable1[0]["seniority"]
                for i in seniorityTitleData:
                    SeniorityTitleDiagram0.append({"name": i, "value": seniorityTable1[0][i]})

            # 離職原因
            if not YearSearch or YearSearch == YearNow:
                if PersonalInfo.objects.filter(Status__in=["離職"], QuitDate__range=Search_Endperiod).values(
                        "QuitReason").distinct():
                    for i in PersonalInfo.objects.filter(Status__in=["離職"], QuitDate__range=Search_Endperiod).values(
                            "QuitReason").distinct().order_by(
                        "QuitReason"):
                        reasonTable_dict = {"reason": i["QuitReason"]}
                        reasonTable_dict['reasonSummary'] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                        QuitReason=i[
                                                                                            "QuitReason"],
                                                                                        QuitDate__range=Search_Endperiod).count()
                        reasonTable_dict['reasonDeparture'] = '%.2f%%' % round(
                            float(PersonalInfo.objects.filter(Status__in=["離職"],
                                                              QuitReason=i[
                                                                  "QuitReason"],
                                                              QuitDate__range=Search_Endperiod).count() / PersonalInfo.objects.filter(
                                Status__in=["離職"], ).count() * 100), 4)

                        reasonTable.append(reasonTable_dict)
            else:
                if PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                        QuitDate__range=Search_Endperiod).values(
                    "QuitReason").distinct():
                    for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                  QuitDate__range=Search_Endperiod).values(
                        "QuitReason").distinct().order_by("QuitReason"):
                        reasonTable_dict = {"reason": i["QuitReason"]}
                        reasonsSummary = 0
                        reasonTable_dict['reasonSummary'] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                                 Status__in=["離職"],
                                                                                                 QuitReason=i[
                                                                                                     "QuitReason"],
                                                                                                 QuitDate__range=Search_Endperiod).count()
                        reasonTable_dict['reasonDeparture'] = '%.2f%%' % round(
                            float(PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                       QuitReason=i[
                                                                           "QuitReason"],
                                                                       QuitDate__range=Search_Endperiod).count() / PersonalInfoHisByYear.objects.filter(
                                Year=YearSearch,
                                Status__in=["離職"], ).count() * 100), 4)

                        reasonTable.append(reasonTable_dict)

            # reasonDiagramData
            LABEL = []
            HEJIRENSHU = []
            YUANYINBI = []
            if reasonTable:
                for i in reasonTable:
                    LABEL.append(i["reason"])
                    HEJIRENSHU.append(i["reasonSummary"])
                    YUANYINBI.append(i["reasonDeparture"])
            reasonDiagramData["LABEL"] = LABEL
            reasonDiagramData["HEJIRENSHU"] = HEJIRENSHU
            reasonDiagramData["YUANYINBI"] = YUANYINBI

            # 學歷
            if not YearSearch or YearSearch == YearNow:
                educationSummary_Total = 0
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Education").distinct().order_by(
                        "Education"):
                    educationTable_dict = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                            "Customer"):
                        educationTable_dict[j["Customer"]] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                         Education=i["Education"],
                                                                                         Customer=j["Customer"],
                                                                                         QuitDate__range=Search_Endperiod).count()
                        educationSummary += educationTable_dict[j["Customer"]]
                    educationTable_dict["educationSummary"] = educationSummary
                    educationSummary_Total += educationSummary
                    educationTable.append(educationTable_dict)
                if educationSummary_Total:
                    for i in educationTable:
                        i["accountFor"] = round(i["educationSummary"] / educationSummary_Total * 100, 4)
            else:
                educationSummary_Total = 0
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Education").distinct().order_by(
                    "Education"):
                    educationTable_dict = {"Education": i["Education"]}
                    educationSummary = 0
                    for j in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                            "Customer").distinct().order_by(
                        "Customer"):
                        educationTable_dict[j["Customer"]] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                                  Status__in=["離職"],
                                                                                                  Education=i[
                                                                                                      "Education"],
                                                                                                  Customer=j[
                                                                                                      "Customer"],
                                                                                                  QuitDate__range=Search_Endperiod).count()
                        educationSummary += educationTable_dict[j["Customer"]]
                    educationTable_dict["educationSummary"] = educationSummary
                    educationSummary_Total += educationSummary
                    educationTable.append(educationTable_dict)
                if educationSummary_Total:
                    for i in educationTable:
                        i["accountFor"] = round(i["educationSummary"] / educationSummary_Total * 100, 4)
            # educationDiagram
            LABEL_educationDiagram = []
            educationDiagramHE_educationDiagram = []
            educationDiagramZH_educationDiagram = []
            for i in educationTable:
                LABEL_educationDiagram.append(i["Education"])
                educationDiagramHE_educationDiagram.append(i["educationSummary"])
                if educationSummary_Total:
                    educationDiagramZH_educationDiagram.append(round(i["accountFor"] / 100, 4))
            educationDiagram = {
                "LABEL": LABEL_educationDiagram,
                "educationDiagramHE": educationDiagramHE_educationDiagram,  # 對應 從本科到中專
                "educationDiagramZH": educationDiagramZH_educationDiagram
            }

            # 專業
            if not YearSearch or YearSearch == YearNow:
                Customer_major = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Education",
                                                                               "Major").distinct().order_by(
                    "Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                                 Education__contains=i["Education"],
                                                                                 Major=i["Major"],
                                                                                 Customer=j,
                                                                                 QuitDate__range=Search_Endperiod).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfoHisByYear.objects.filter(Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status__in=["離職"]).count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
            else:
                Customer_major = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_major.append(i["Customer"])
                TBCnum = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Education", "Major").distinct().order_by("Education"):
                    # if i["Education"] == "本科":
                    if MajorIfo.objects.filter(Education__contains=i["Education"], Major=i["Major"]).first():
                        professionTableData = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major=i["Major"]).first().Categories,
                            "Profession": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                                  Major=i["Major"]).first().Major,
                        }
                        professionSummary = 0
                        for j in Customer_major:
                            professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                          Status__in=["離職"],
                                                                                          Education=i["Education"],
                                                                                          Major=i["Major"],
                                                                                          Customer=j,
                                                                                          QuitDate__range=Search_Endperiod).count()
                            professionSummary += professionTableData[j]
                        professionTableData["professionSummary"] = professionSummary
                        professionTable.append(professionTableData)
                    else:
                        print("專業信息裏面沒有：", i["Education"], i["Major"])
                        # else:
                        #     professionTableData = {
                        #         "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                        #                                          Major="TBC").first().Categories,
                        #         "Profession": "TBC",
                        #     }
                        #     professionSummary = 0
                        #     for j in Customer_major:
                        #         professionTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Education=i["Education"],
                        #                                                              Major=i["Major"],
                        #                                                              Customer=j, Status__in=["離職"]).count()
                        #         professionSummary += professionTableData[j]
                        #     professionTableData["professionSummary"] = professionSummary
                        #     TBCnum.append(professionTableData)
                    if MajorIfo.objects.filter(Education__contains=i["Education"],
                                               Major="TBC").first():
                        professionTableData_TBC = {
                            "daLei": MajorIfo.objects.filter(Education__contains=i["Education"],
                                                             Major="TBC").first().Categories,
                            "Profession": "TBC",
                        }
                        # print(TBCnum)
                        TBCnum_professionSummary = 0
                        for j in Customer_major:
                            professionTableData_TBC[j] = 0
                            for i in TBCnum:
                                professionTableData_TBC[j] += i[j]
                                TBCnum_professionSummary += i["professionSummary"]
                        professionTableData_TBC["professionSummary"] = TBCnum_professionSummary
                        professionTable.append(professionTableData_TBC)
            professionTable = sorted(professionTable,
                                     key=lambda e: (e.__getitem__('daLei'), e.__getitem__('professionSummary')),
                                     reverse=True)
            # heBingNum
            professionTablenew = []
            for i in professionTable:
                professionTablenew.append(i["daLei"])
            professionTable_counter = Counter(professionTablenew)
            # print(professionTable)
            # print(professionTable_counter)
            # print(dict(professionTable_counter))
            # heBing里的数值与professionTable["daLei"] 的value排序保持一致
            heBingNum_sort = sorted(dict(professionTable_counter).items(), key=lambda e: e[0], reverse=True)
            # print(heBingNum_sort)
            for i in heBingNum_sort:
                heBingNum.append(i[1])

            # 地區
            if not YearSearch or YearSearch == YearNow:
                Customer_region = []
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                        "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("NativeProvince").distinct().order_by(
                        "NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfo.objects.filter(Status__in=["離職"],
                                                                          NativeProvince=i["NativeProvince"],
                                                                          Customer=j,
                                                                          QuitDate__range=Search_Endperiod).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            else:
                Customer_region = []
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "Customer").distinct().order_by(
                    "Customer"):
                    Customer_region.append(i["Customer"])
                for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "NativeProvince").distinct().order_by("NativeProvince"):
                    regionsTableData = {"Regions": i["NativeProvince"]}
                    regionsSummary = 0
                    for j in Customer_region:
                        regionsTableData[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"],
                                                                                   NativeProvince=i[
                                                                                       "NativeProvince"],
                                                                                   Customer=j,
                                                                                   QuitDate__range=Search_Endperiod).count()
                        regionsSummary += regionsTableData[j]
                    regionsTableData["regionsSummary"] = regionsSummary
                    regionsTable.append(regionsTableData)
            regionsTable = sorted(regionsTable, key=lambda x: x.__getitem__("regionsSummary"), reverse=True)

        if request.POST.get("isGetData") == "SEARCH2":
            startYear = request.POST.get("startYear")
            endYear = request.POST.get("endYear")
            YearSearch = request.POST.get("Year")
            YearNow = str(datetime.datetime.now().year)
            if not startYear:
                startYear = YearNow
            if not endYear:
                endYear = YearNow
            if endYear >= startYear:
                DateNow_begin = startYear + "-1-1"
                DateNow_end = endYear + "-12-31"
                Test_Endperiod = [DateNow_begin, DateNow_end]
                # 職稱
                # print(Test_Endperiod)
                if not YearSearch or YearSearch == YearNow:
                    YearSearch = YearNow
                    # print(1)
                    selectItemzhicheng = []
                    selectItem = []
                    for i in PersonalInfo.objects.filter(Status__in=["離職"]).values("Customer").distinct().order_by(
                            "Customer"):
                        selectItemzhicheng.append(i["Customer"])
                        selectItem.append(i["Customer"])
                    titleDiagram2Data_LABLE = []
                    titleDiagram2Data_Position = []
                    PositionQuerySet = PersonalInfo.objects.filter(Status__in=["離職"]).values(
                        "PositionNow").distinct().order_by(
                        "PositionNow").annotate(entry_Code=Value('', CharField()))
                    for i in PositionQuerySet:
                        i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                                   Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱代碼"
                    # print(type(Positionlist), Positionlist)
                    # print(list(PositionQuerySet))
                    Positionlist = list(PositionQuerySet)
                    Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                    # print(Positionlistnew)
                    for i in Positionlistnew:
                        titleDiagram2Data_LABLE.append(
                            Positions.objects.filter(Item=i["PositionNow"],
                                                     Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                                Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                        titleDiagram2Data_Position.append(i["PositionNow"])
                    # titleTable
                    # print(titleDiagram2Data_Position)
                    titleSummary_Total = 0
                    for i in Positionlistnew:
                        titleTable_dict = {"Title": Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                        titleSummary = 0
                        for j in selectItemzhicheng:
                            titleTable_dict[j] = PersonalInfo.objects.filter(Status__in=["離職"], Customer=j,
                                                                             PositionNow=i["PositionNow"],
                                                                             QuitDate__range=Test_Endperiod).count()
                            titleSummary += titleTable_dict[j]
                        titleTable_dict["titleSummary"] = titleSummary
                        titleSummary_Total += titleSummary
                        titleTable.append(titleTable_dict)
                    # print(titleTable)
                    # titleSeniorityData&titleTable1
                    titleSeniorityData = [
                        "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                    ]
                    for j in titleDiagram2Data_Position:
                        titleTable1_dict = {}
                        number025 = 0
                        number025_1 = 0
                        number1_2 = 0
                        number2_3 = 0
                        number3_5 = 0
                        number5_10 = 0
                        number10_15 = 0
                        number15_20 = 0
                        number20 = 0
                        for Per in PersonalInfo.objects.filter(PositionNow=j, Status__in=["離職"],
                                                               QuitDate__range=Test_Endperiod):
                            # if Per.Status == "在職":
                            # Seniority = round(
                            #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                            #     1)
                            # else:
                            Seniority = round(
                                float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                            if Seniority <= 0.25:
                                number025 += 1
                            elif Seniority > 0.25 and Seniority <= 1:
                                number025_1 += 1
                            elif Seniority > 1 and Seniority <= 2:
                                number1_2 += 1
                            elif Seniority > 2 and Seniority <= 3:
                                number2_3 += 1
                            elif Seniority > 3 and Seniority <= 5:
                                number3_5 += 1
                            elif Seniority > 5 and Seniority <= 10:
                                number5_10 += 1
                            elif Seniority > 10 and Seniority <= 15:
                                number10_15 += 1
                            elif Seniority > 15 and Seniority <= 20:
                                number15_20 += 1
                            elif Seniority > 20:
                                number20 += 1
                        titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                              Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                            "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                            '2~3年': number2_3, '3~5年': number3_5,
                                            '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                            '20年以上': number20,
                                            "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                        titleTable1.append(titleTable1_dict)
                else:
                    print(2)
                    selectItemzhicheng = []
                    for i in PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                            "Customer").distinct().order_by(
                        "Customer"):
                        selectItemzhicheng.append(i["Customer"])
                    titleDiagram2Data_LABLE = []
                    titleDiagram2Data_Position = []
                    PositionQuerySet = PersonalInfoHisByYear.objects.filter(Year=YearSearch, Status__in=["離職"]).values(
                        "PositionNow").distinct().order_by(
                        "PositionNow").annotate(entry_Code=Value('', CharField()))
                    for i in PositionQuerySet:
                        i["entry_Code"] = Positions.objects.filter(Item=i["PositionNow"],
                                                                   Year=YearSearch).first().Positions_Code if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的職稱代碼"
                    # print(type(Positionlist), Positionlist)
                    # print(list(PositionQuerySet))
                    Positionlist = list(PositionQuerySet)
                    Positionlistnew = sorted(Positionlist, key=lambda x: (x["entry_Code"]))
                    # print(Positionlistnew)
                    for i in Positionlistnew:
                        titleDiagram2Data_LABLE.append(
                            Positions.objects.filter(Item=i["PositionNow"],
                                                     Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                                Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱")
                        titleDiagram2Data_Position.append(i["PositionNow"])
                    # titleTable
                    titleSummary_Total = 0
                    for i in Positionlistnew:
                        titleTable_dict = {"Title": Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=i["PositionNow"], Year=YearSearch).first() else "沒有該年份的對應職稱", }  # Year=YearNow,
                        titleSummary = 0
                        for j in selectItemzhicheng:
                            titleTable_dict[j] = PersonalInfoHisByYear.objects.filter(Year=YearSearch,
                                                                                      Status__in=["離職"],
                                                                                      Customer=j,
                                                                                      PositionNow=i[
                                                                                          "PositionNow"],
                                                                                      QuitDate__range=Test_Endperiod).count()
                            titleSummary += titleTable_dict[j]
                        titleTable_dict["titleSummary"] = titleSummary
                        titleSummary_Total += titleSummary
                        titleTable.append(titleTable_dict)
                    # titleSeniorityData&titleTable1
                    titleSeniorityData = [
                        "3个月以下", "3个月~1年", "1~2年", "2~3年", "3~5年", "5~10年", "10~15年", "15~20年", "20年以上"
                    ]
                    for j in titleDiagram2Data_Position:
                        titleTable1_dict = {}
                        number025 = 0
                        number025_1 = 0
                        number1_2 = 0
                        number2_3 = 0
                        number3_5 = 0
                        number5_10 = 0
                        number10_15 = 0
                        number15_20 = 0
                        number20 = 0
                        for Per in PersonalInfoHisByYear.objects.filter(Year=YearSearch, PositionNow=j,
                                                                        Status__in=["離職"],
                                                                        QuitDate__range=Test_Endperiod):
                            # if Per.Status == "在職":
                            # Seniority = round(
                            #     float(str((datetime.datetime.now().date() - Per.RegistrationDate)).split(' ')[0]) / 365,
                            #     1)
                            # else:
                            Seniority = round(
                                float(str((Per.QuitDate - Per.RegistrationDate)).split(' ')[0]) / 365, 1)
                            if Seniority <= 0.25:
                                number025 += 1
                            elif Seniority > 0.25 and Seniority <= 1:
                                number025_1 += 1
                            elif Seniority > 1 and Seniority <= 2:
                                number1_2 += 1
                            elif Seniority > 2 and Seniority <= 3:
                                number2_3 += 1
                            elif Seniority > 3 and Seniority <= 5:
                                number3_5 += 1
                            elif Seniority > 5 and Seniority <= 10:
                                number5_10 += 1
                            elif Seniority > 10 and Seniority <= 15:
                                number10_15 += 1
                            elif Seniority > 15 and Seniority <= 20:
                                number15_20 += 1
                            elif Seniority > 20:
                                number20 += 1
                        titleTable1_dict = {"Title": Positions.objects.filter(Item=j,
                                                                              Year=YearSearch).first().Positions_Name if Positions.objects.filter(
                            Item=j, Year=YearSearch).first() else "沒有該年份的對應職稱",
                                            "3个月以下": number025, "3个月~1年": number025_1, '1~2年': number1_2,
                                            '2~3年': number2_3, '3~5年': number3_5,
                                            '5~10年': number5_10, '10~15年': number10_15, "15~20年": number15_20,
                                            '20年以上': number20,
                                            "titleSummary": number025 + number025_1 + number1_2 + number2_3 + number3_5 + number5_10 + number10_15 + number15_20 + number20}
                        titleTable1.append(titleTable1_dict)
                # titleDeparture

                for i in titleTable:
                    if titleSummary_Total:
                        i["titleDeparture"] = '%.2f%%' % round(float(i["titleSummary"] / titleSummary_Total * 100), 4)
                    else:
                        i["titleDeparture"] = '%.2f%%' % round(0, 1)
                # titleDiagram2Data
                LABEL_titleDiagram2Data = []
                HEJILIZHI_titleDiagram2Data = []
                LIZHIBI_titleDiagram2Data = []
                # print(titleSummary_Total, titleTable)
                for i in titleTable:
                    LABEL_titleDiagram2Data.append(i["Title"])
                    HEJILIZHI_titleDiagram2Data.append(i["titleSummary"])
                    LIZHIBI_titleDiagram2Data.append(round(float(i["titleDeparture"].split("%")[0]), 4))
                titleDiagram2Data["LABEL"] = LABEL_titleDiagram2Data
                titleDiagram2Data["HEJILIZHI"] = HEJILIZHI_titleDiagram2Data
                titleDiagram2Data["LIZHIBI"] = LIZHIBI_titleDiagram2Data
                # TitleText&titleSeniorityDiagram2
                if titleTable1:
                    TitleText = titleTable1[0]["Title"]
                    titleSeniorityDiagram2 = [
                        {"name": "3个月以下", "value": titleTable1[0]["3个月以下"]},
                        {"name": "3个月~1年", "value": titleTable1[0]["3个月~1年"]},
                        {"name": "1~2年", "value": titleTable1[0]["1~2年"]},
                        {"name": "2~3年", "value": titleTable1[0]["2~3年"]},
                        {"name": "3~5年", "value": titleTable1[0]["3~5年"]},
                        {"name": "5~10年", "value": titleTable1[0]["5~10年"]},
                        {"name": "10~15年", "value": titleTable1[0]["10~15年"]},
                        {"name": "15~20年", "value": titleTable1[0]["15~20年"]},
                        {"name": "20年以上", "value": titleTable1[0]["20年以上"]}
                    ]

        data = {
            "perinTable": perinTable,
            "selectItem": selectItem,
            "searchYear": searchYear,
            "reasonsTable": reasonsTable,
            "titleTable": titleTable,
            "titleSeniorityData": titleSeniorityData,
            "titleTable1": titleTable1,
            "titleDiagram2Data": titleDiagram2Data,
            "reasonsDiagramData": reasonsDiagramData,
            "seniorityTable": seniorityTable,
            "seniorityTable1": seniorityTable1,
            "seniorityTitleData": seniorityTitleData,
            "professionTable": professionTable,
            "regionsTable": regionsTable,
            "heBingNum": heBingNum,
            "seniorityDiagramData1": seniorityDiagramData1,
            "educationTable": educationTable,
            "educationDiagram": educationDiagram,
            "TitleText": TitleText,
            "titleSeniorityDiagram2": titleSeniorityDiagram2,
            "seniorityText": seniorityText,
            "SeniorityTitleDiagram0": SeniorityTitleDiagram0,
            "reasonTable": reasonTable,
            "reasonDiagramData": reasonDiagramData,
            "canExport": canExport,

        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PersonalInfo/Summary3.html', locals())


@csrf_exempt
def PublicArea(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DepartmentManage/公共區域"
    FJtable = [
        # {"id":1,"XX":"V2FA-14","FZR":"沈亮亮","CHU":"一處","DEPARTMENT":"三部","MAIL":"xx@compal.com  ","LXFS":"18626216826"},
        #  {"id":2,"XX": "V2FA-15", "FZR": "殷秀梅", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "13584985565"},
        #  {"id":3,"XX": "V2FA-16", "FZR": "王勇", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "681537"},
        #  {"id":4,"XX": "V2FA-17", "FZR": "王君", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "18915749821"},
        #  {"id":5,"XX": "V2FA-18", "FZR": "王文娟","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "642325"},
        #  {"id":6,"XX": "V2FA-19", "FZR": "王文娟","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "642325"},
        #  {"id":7,"XX": "V2FA-20", "FZR": "王勇", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "681537"},
        #  {"id":8,"XX": "V2FA-21", "FZR": "汪娟娟", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21806/624804"},
        #  {"id":9,"XX": "V2FA-22", "FZR": "任學梅", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21838"},
        #  {"id":10,"XX": "V2FA-23", "FZR": "張亞萍","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "13812952261"},
        #  {"id":11,"XX": "V2FA-24", "FZR": "吳嚴肅","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "13584909481"},
        #  {"id":12,"XX": "V2FA-25", "FZR": "王新偉", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21806/642753"},
        #  {"id":13,"XX": "V2FA-26", "FZR": "桂淑娟", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21831"},
        #  {"id":14,"XX": "V2FA-27", "FZR": "陽光", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21827/642462"},
        #  {"id":15,"XX": "V2FA-28", "FZR": "江鴻飛","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21810"},
        #  {"id":16,"XX": "V2FA-29", "FZR": "單桂萍","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "13405058756"},
        #  {"id":17,"XX": "V2FA-30", "FZR": "王勇", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "681537"},
        #  {"id":18,"XX": "V2FA-31", "FZR": "王勇", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "681537"},
        #  {"id":19,"XX": "V2FA-32", "FZR": "張沛新", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21867/626622"},
        #  {"id":20,"XX": "V2FA-33", "FZR": "鐘曉麗", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21865"},
        #  {"id":21,"XX": "V2FA-34", "FZR": "盧少青","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21877"},
        #  {"id":22,"XX": "V2FA-35", "FZR": "潘明明","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21875"},
        #  {"id":23,"XX": "V2FA-42", "FZR": "梅吉波","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21830"},
        #  {"id":24,"XX": "V2FA-43", "FZR": "王萬松", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "13771824535"},
        #  {"id":25,"XX": "#26", "FZR": "王棟","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21867"},
        #  {"id":26,"XX": "#27", "FZR": "王棟","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21867"},
        #  {"id":27,"XX": "#28", "FZR": "朱曉寧","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "655775"},
        #  {"id":28,"XX": "萬利管隔墻區", "FZR": "王勇", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "681537"}
    ]
    SBtable = [
        # {"id":29,"XX":"機構設備-NB","FZR":"彭祝彪","CHU":"","DEPARTMENT":"","MAIL":"","LXFS":"21848/621422"},
        #  {"id":30,"XX": "機構設備-AIO", "FZR": "張沛新","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21867/626622"},
        #  {"id":31,"XX": "自動化設備", "FZR": "王君","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "18915749821"},
        #  {"id":32,"XX": "網絡設備", "FZR": "曹澤","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21850"},
        #  {"id":34,"XX": "eQuip設備", "FZR": "曹麗華", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21850"},
        #  {"id":35,"XX": "實驗室Cisco AP監控", "FZR": "陳燕平","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21850"},
        #  {"id":36,"XX": "Monitor", "FZR": "江鴻飛", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21810"},
        #  {"id":37,"XX": "Device-C38", "FZR": "江鴻飛", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21810"},
        #  {"id":38,"XX": "Device-A39", "FZR": "孫玉旺", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21839"},
        #  {"id":39,"XX": "雜項設備", "FZR": "","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": ""},
        #  {"id":40,"XX": "雜項設備", "FZR": "", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": ""}
    ]
    JTtable = [
        # {"id":41,"XX": "幾台材料", "FZR": "高亞娟", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21870"}
    ]
    ZHtable = [
        # {"id":42,"XX": "Steam賬號", "FZR": "施佳媛","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "218806"},
        #  {"id":43,"XX": "愛奇藝賬號", "FZR": "單桂萍", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "13405058756"}
    ]
    WLtable = [
        # {"id":44,"XX":"實驗室網絡維護-V2FA14","FZR":"彭祝彪","CHU":"","DEPARTMENT":"","MAIL":"","LXFS":"21848/621422"},
        #  {"id":45,"XX": "實驗室網絡維護-V2FA15", "FZR": "張沛新","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "21867/626622"},
        #  {"id":46,"XX": "實驗室網絡維護-V2FA21", "FZR": "王君","CHU":"","DEPARTMENT":"","MAIL":"", "LXFS": "18915749821"},
        #  {"id":47,"XX": "實驗室網絡維護-V2FA22", "FZR": "曹澤", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21850"},
        #  {"id":48,"XX": "實驗室網絡維護-V2FA23", "FZR": "曹麗華", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21850"},
        #  {"id":49,"XX": "外網點-ADSL-27", "FZR": "陳燕平", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21850"},
        #  {"id":50,"XX": "外網點-ADSL-28", "FZR": "江鴻飛", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21810"},
        #  {"id":51,"XX": "外網點-ADSL-25（GAME）", "FZR": "江鴻飛", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21810"},
        #  {"id":52,"XX": "外網點-ADSL-34", "FZR": "孫玉旺", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "21839"},
        #  {"id":53,"XX": "雜項設備", "FZR": "", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": ""},
        #  {"id":54,"XX": "雜項設備", "FZR": "", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": ""}
    ]
    Others = [
        # {"id": 55, "XX": "Steam賬號", "FZR": "施佳媛", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "218806"},
        #        {"id": 56, "XX": "愛奇藝賬號", "FZR": "單桂萍", "CHU":"","DEPARTMENT":"","MAIL":"","LXFS": "13405058756"}
    ]
    permission = 1  # 權限  0是有權限 其他數字沒有權限
    roles = []
    onlineuser = request.session.get('account')
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    # editPpriority = 100
    for i in roles:
        if 'admin' in i or 'DepartmentAdmin' in i or 'PublicAreaAdmin' in i:
            permission = 0

    if request.method == "POST":
        if request.POST:
            if request.POST.get('isGetData') == 'first':
                for i in PublicAreaM.objects.filter(Category="房間"):
                    FJtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="設備"):
                    SBtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="機台材料"):
                    JTtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="賬號"):
                    ZHtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="網絡環境"):
                    WLtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="其他"):
                    Others.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
            if request.POST.get('action') == 'addSubmit':
                check_dic = {}
                create_dic = {}
                if request.POST.get('DX'):
                    check_dic['Category'] = request.POST.get('DX')
                    create_dic['Category'] = request.POST.get('DX')
                if request.POST.get('XX'):
                    check_dic['XX'] = request.POST.get('XX')
                    create_dic['XX'] = request.POST.get('XX')
                create_dic['FZR'] = request.POST.get('FZR')
                create_dic['DEPARTMENT'] = request.POST.get('DEPARTMENT')
                create_dic['MAIL'] = request.POST.get('MAIL')
                create_dic['LXFS'] = request.POST.get('LXFS')
                if check_dic:
                    if not PublicAreaM.objects.filter(**check_dic):
                        PublicAreaM.objects.create(**create_dic)
                for i in PublicAreaM.objects.filter(Category="房間"):
                    FJtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="設備"):
                    SBtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="機台材料"):
                    JTtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="賬號"):
                    ZHtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="網絡環境"):
                    WLtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="其他"):
                    Others.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
            if request.POST.get('isGetData') == 'editSubmit':
                id = request.POST.get('id')
                update_dic = {}

                update_dic['Category'] = request.POST.get('DX')
                update_dic['XX'] = request.POST.get('XX')
                update_dic['FZR'] = request.POST.get('FZR')
                update_dic['DEPARTMENT'] = request.POST.get('DEPARTMENT')
                update_dic['MAIL'] = request.POST.get('MAIL')
                update_dic['LXFS'] = request.POST.get('LXFS')
                # print(update_dic)
                PublicAreaM.objects.filter(id=id).update(**update_dic)
                for i in PublicAreaM.objects.filter(Category="房間"):
                    FJtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="設備"):
                    SBtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="機台材料"):
                    JTtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="賬號"):
                    ZHtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="網絡環境"):
                    WLtable.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
                for i in PublicAreaM.objects.filter(Category="其他"):
                    Others.append(
                        {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                         "DEPARTMENT": i.DEPARTMENT,
                         "MAIL": i.MAIL, "LXFS": i.LXFS}
                    )
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'Delete' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData['DeleteId'])
                    for i in responseData['DeleteId']:
                        PublicAreaM.objects.filter(id=i).delete()
                    for i in PublicAreaM.objects.filter(Category="房間"):
                        FJtable.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
                    for i in PublicAreaM.objects.filter(Category="設備"):
                        SBtable.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
                    for i in PublicAreaM.objects.filter(Category="機台材料"):
                        JTtable.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
                    for i in PublicAreaM.objects.filter(Category="賬號"):
                        ZHtable.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
                    for i in PublicAreaM.objects.filter(Category="網絡環境"):
                        WLtable.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
                    for i in PublicAreaM.objects.filter(Category="其他"):
                        Others.append(
                            {"id": i.id, "DX": i.Category, "XX": i.XX, "FZR": i.FZR, "CHU": i.CHU,
                             "DEPARTMENT": i.DEPARTMENT,
                             "MAIL": i.MAIL, "LXFS": i.LXFS}
                        )
        data = {
            # "selectItem":selectItem,
            # "powerOptions":powerOptions,
            # "content": mock_data,
            # "options":options,
            # "permission": permission

            "FJtable": FJtable,
            "SBtable": SBtable,
            "JTtable": JTtable,
            "ZHtable": ZHtable,
            "WLtable": WLtable,
            "Others": Others,
            "permission": permission
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'PublicArea/PublicArea_Edit.html', locals())


@csrf_exempt
def codeareacheck(code):
    codelenth = len(code)
    returninfo = {}
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    if codelenth == 18:
        # age = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # print(datetime.date.today().year, int(code[6:10]))
        age = datetime.date.today().year - int(code[6:10])
        sex = int(code[16:17])
        birth = code[6:10] + "-" + code[10:12] + "-" + code[12:14]
        if (int(code[10: 12]) > month or (int(code[10: 12]) == month and int(code[12: 14]) >= day)):
            age = age - 1
        if sex % 2 == 0:
            sex = "女"
        else:
            sex = "男"
        returninfo["age"] = age
        returninfo["sex"] = sex
        returninfo["birth"] = birth
        arealocalcheck = local_identity.objects.filter(countycode=code[:6]).first()
        if arealocalcheck:
            returninfo["area"] = arealocalcheck.provincevalue + arealocalcheck.cityvalue + arealocalcheck.countyvalue
        else:
            returninfo["area"] = "未查询到"
    elif codelenth == 15:
        # age = datetime.date.today().year - int(code[6:8]) - 1901
        # sex = int(code[13:14])
        # birth = "19" + code[6:8] + "-" + code[8:10] + "-" + code[10:12]
        # if (int(code[10: 12]) > month or (int(code[10: 12]) == month and int(code[12: 14]) >= day)):
        #     age = age - 1
        # if sex%2 == 0:
        #     sex = "女"
        # else:
        #     sex = "男"
        # returninfo["age"] = age
        # returninfo["sex"] = sex
        # returninfo["birth"] = birth
        # if code[:2] in area.keys():
        #     returninfo["area"] = area[code[:2]]
        # else:
        #     returninfo["area"] = "未查询到"
        return "非18身份证"
    else:
        return "无效身份证"
    print(returninfo)
    return returninfo


@csrf_exempt
def codeareadata():
    arealist = [
        (1, 110000, '北京', 110100, '北京市', 110101, '东城区', 116.42, 39.93),
        (2, 110000, '北京', 110100, '北京市', 110102, '西城区', 116.37, 39.92),
        (3, 110000, '北京', 110100, '北京市', 110103, '崇文区', 116.43, 39.88),
        (4, 110000, '北京', 110100, '北京市', 110104, '宣武区', 116.35, 39.87),
        (5, 110000, '北京', 110100, '北京市', 110105, '朝阳区', 116.43, 39.92),
        (6, 110000, '北京', 110100, '北京市', 110106, '丰台区', 116.28, 39.85),
        (7, 110000, '北京', 110100, '北京市', 110107, '石景山区', 116.22, 39.9),
        (8, 110000, '北京', 110100, '北京市', 110108, '海淀区', 116.3, 39.95),
        (9, 110000, '北京', 110100, '北京市', 110109, '门头沟区', 116.1, 39.93),
        (10, 110000, '北京', 110100, '北京市', 110111, '房山区', 116.13, 39.75),
        (11, 110000, '北京', 110100, '北京市', 110112, '通州区', 116.65, 39.92),
        (12, 110000, '北京', 110100, '北京市', 110113, '顺义区', 116.65, 40.13),
        (13, 110000, '北京', 110100, '北京市', 110114, '昌平区', 116.23, 40.22),
        (14, 110000, '北京', 110100, '北京市', 110115, '大兴区', 116.33, 39.73),
        (15, 110000, '北京', 110100, '北京市', 110116, '怀柔区', 116.63, 40.32),
        (16, 110000, '北京', 110100, '北京市', 110117, '平谷区', 117.12, 40.13),
        (17, 110000, '北京', 110200, '北京市', 110228, '密云县', 116.83, 40.37),
        (18, 110000, '北京', 110200, '北京市', 110229, '延庆县', 115.97, 40.45),
        (19, 120000, '天津', 120100, '天津市', 120101, '和平区', 117.2, 39.12),
        (20, 120000, '天津', 120100, '天津市', 120102, '河东区', 117.22, 39.12),
        (21, 120000, '天津', 120100, '天津市', 120103, '河西区', 117.22, 39.12),
        (22, 120000, '天津', 120100, '天津市', 120104, '南开区', 117.15, 39.13),
        (23, 120000, '天津', 120100, '天津市', 120105, '河北区', 117.18, 39.15),
        (24, 120000, '天津', 120100, '天津市', 120106, '红桥区', 117.15, 39.17),
        (25, 120000, '天津', 120100, '天津市', 120107, '塘沽区', 117.65, 39.02),
        (26, 120000, '天津', 120100, '天津市', 120108, '汉沽区', 117.8, 39.25),
        (27, 120000, '天津', 120100, '天津市', 120109, '大港区', 117.45, 38.83),
        (28, 120000, '天津', 120100, '天津市', 120110, '东丽区', 117.3, 39.08),
        (29, 120000, '天津', 120100, '天津市', 120111, '西青区', 117, 39.13),
        (30, 120000, '天津', 120100, '天津市', 120112, '津南区', 117.38, 38.98),
        (31, 120000, '天津', 120100, '天津市', 120113, '北辰区', 117.13, 39.22),
        (32, 120000, '天津', 120100, '天津市', 120114, '武清区', 117.03, 39.38),
        (33, 120000, '天津', 120100, '天津市', 120115, '宝坻区', 117.3, 39.72),
        (34, 120000, '天津', 120200, '天津市', 120221, '宁河县', 117.82, 39.33),
        (35, 120000, '天津', 120200, '天津市', 120223, '静海县', 116.92, 38.93),
        (36, 120000, '天津', 120200, '天津市', 120225, '蓟县', 117.4, 40.05),
        (37, 130000, '河北省', 130100, '石家庄市', 130101, '市辖区', 114.52, 38.05),
        (38, 130000, '河北省', 130100, '石家庄市', 130102, '长安区', 114.52, 38.05),
        (39, 130000, '河北省', 130100, '石家庄市', 130103, '桥东区', 114.5, 37.07),
        (40, 130000, '河北省', 130100, '石家庄市', 130104, '桥西区', 114.47, 38.03),
        (41, 130000, '河北省', 130100, '石家庄市', 130105, '新华区', 116.87, 38.32),
        (42, 130000, '河北省', 130100, '石家庄市', 130107, '井陉矿区', 114.05, 38.08),
        (43, 130000, '河北省', 130100, '石家庄市', 130108, '裕华区', 114.52, 38.02),
        (44, 130000, '河北省', 130100, '石家庄市', 130121, '井陉县', 114.13, 38.03),
        (45, 130000, '河北省', 130100, '石家庄市', 130123, '正定县', 114.57, 38.15),
        (46, 130000, '河北省', 130100, '石家庄市', 130124, '栾城县', 114.65, 37.88),
        (47, 130000, '河北省', 130100, '石家庄市', 130125, '行唐县', 114.55, 38.43),
        (48, 130000, '河北省', 130100, '石家庄市', 130126, '灵寿县', 114.37, 38.3),
        (49, 130000, '河北省', 130100, '石家庄市', 130127, '高邑县', 114.6, 37.6),
        (50, 130000, '河北省', 130100, '石家庄市', 130128, '深泽县', 115.2, 38.18),
        (51, 130000, '河北省', 130100, '石家庄市', 130129, '赞皇县', 114.38, 37.67),
        (52, 130000, '河北省', 130100, '石家庄市', 130130, '无极县', 114.97, 38.18),
        (53, 130000, '河北省', 130100, '石家庄市', 130131, '平山县', 114.2, 38.25),
        (54, 130000, '河北省', 130100, '石家庄市', 130132, '元氏县', 114.52, 37.75),
        (55, 130000, '河北省', 130100, '石家庄市', 130133, '赵县', 114.77, 37.75),
        (56, 130000, '河北省', 130100, '石家庄市', 130181, '辛集市', 115.22, 37.92),
        (57, 130000, '河北省', 130100, '石家庄市', 130182, '藁城市', 114.83, 38.03),
        (58, 130000, '河北省', 130100, '石家庄市', 130183, '晋州市', 115.03, 38.03),
        (59, 130000, '河北省', 130100, '石家庄市', 130184, '新乐市', 114.68, 38.35),
        (60, 130000, '河北省', 130100, '石家庄市', 130185, '鹿泉市', 114.3, 38.08),
        (61, 130000, '河北省', 130200, '唐山市', 130201, '市辖区', 118.2, 39.63),
        (62, 130000, '河北省', 130200, '唐山市', 130202, '路南区', 118.17, 39.63),
        (63, 130000, '河北省', 130200, '唐山市', 130203, '路北区', 118.22, 39.63),
        (64, 130000, '河北省', 130200, '唐山市', 130204, '古冶区', 118.42, 39.73),
        (65, 130000, '河北省', 130200, '唐山市', 130205, '开平区', 118.27, 39.68),
        (66, 130000, '河北省', 130200, '唐山市', 130207, '丰南区', 118.1, 39.57),
        (67, 130000, '河北省', 130200, '唐山市', 130208, '丰润区', 118.17, 39.83),
        (68, 130000, '河北省', 130200, '唐山市', 130223, '滦县', 118.7, 39.75),
        (69, 130000, '河北省', 130200, '唐山市', 130224, '滦南县', 118.68, 39.5),
        (70, 130000, '河北省', 130200, '唐山市', 130225, '乐亭县', 118.9, 39.42),
        (71, 130000, '河北省', 130200, '唐山市', 130227, '迁西县', 118.32, 40.15),
        (72, 130000, '河北省', 130200, '唐山市', 130229, '玉田县', 117.73, 39.88),
        (73, 130000, '河北省', 130200, '唐山市', 130230, '唐海县', 118.45, 39.27),
        (74, 130000, '河北省', 130200, '唐山市', 130281, '遵化市', 117.95, 40.18),
        (75, 130000, '河北省', 130200, '唐山市', 130283, '迁安市', 118.7, 40.02),
        (76, 130000, '河北省', 130300, '秦皇岛市', 130301, '市辖区', 119.6, 39.93),
        (77, 130000, '河北省', 130300, '秦皇岛市', 130302, '海港区', 119.6, 39.93),
        (78, 130000, '河北省', 130300, '秦皇岛市', 130303, '山海关区', 119.77, 40),
        (79, 130000, '河北省', 130300, '秦皇岛市', 130304, '北戴河区', 119.48, 39.83),
        (80, 130000, '河北省', 130300, '秦皇岛市', 130321, '青龙满族自治县', 118.95, 40.4),
        (81, 130000, '河北省', 130300, '秦皇岛市', 130322, '昌黎县', 119.17, 39.7),
        (82, 130000, '河北省', 130300, '秦皇岛市', 130323, '抚宁县', 119.23, 39.88),
        (83, 130000, '河北省', 130300, '秦皇岛市', 130324, '卢龙县', 118.87, 39.88),
        (84, 130000, '河北省', 130400, '邯郸市', 130401, '市辖区', 114.48, 36.62),
        (85, 130000, '河北省', 130400, '邯郸市', 130402, '邯山区', 114.48, 36.6),
        (86, 130000, '河北省', 130400, '邯郸市', 130403, '丛台区', 114.48, 36.63),
        (87, 130000, '河北省', 130400, '邯郸市', 130404, '复兴区', 114.45, 36.63),
        (88, 130000, '河北省', 130400, '邯郸市', 130406, '峰峰矿区', 114.2, 36.42),
        (89, 130000, '河北省', 130400, '邯郸市', 130421, '邯郸县', 114.53, 36.6),
        (90, 130000, '河北省', 130400, '邯郸市', 130423, '临漳县', 114.62, 36.35),
        (91, 130000, '河北省', 130400, '邯郸市', 130424, '成安县', 114.68, 36.43),
        (92, 130000, '河北省', 130400, '邯郸市', 130425, '大名县', 115.15, 36.28),
        (93, 130000, '河北省', 130400, '邯郸市', 130426, '涉县', 113.67, 36.57),
        (94, 130000, '河北省', 130400, '邯郸市', 130427, '磁县', 114.37, 36.35),
        (95, 130000, '河北省', 130400, '邯郸市', 130428, '肥乡县', 114.8, 36.55),
        (96, 130000, '河北省', 130400, '邯郸市', 130429, '永年县', 114.48, 36.78),
        (97, 130000, '河北省', 130400, '邯郸市', 130430, '邱县', 115.17, 36.82),
        (98, 130000, '河北省', 130400, '邯郸市', 130431, '鸡泽县', 114.87, 36.92),
        (99, 130000, '河北省', 130400, '邯郸市', 130432, '广平县', 114.93, 36.48),
        (100, 130000, '河北省', 130400, '邯郸市', 130433, '馆陶县', 115.3, 36.53),
        (101, 130000, '河北省', 130400, '邯郸市', 130434, '魏县', 114.93, 36.37),
        (102, 130000, '河北省', 130400, '邯郸市', 130435, '曲周县', 114.95, 36.78),
        (103, 130000, '河北省', 130400, '邯郸市', 130481, '武安市', 114.2, 36.7),
        (104, 130000, '河北省', 130500, '邢台市', 130501, '市辖区', 114.48, 37.07),
        (105, 130000, '河北省', 130500, '邢台市', 130502, '桥东区', 114.5, 37.07),
        (106, 130000, '河北省', 130500, '邢台市', 130503, '桥西区', 114.47, 37.05),
        (107, 130000, '河北省', 130500, '邢台市', 130521, '邢台县', 114.5, 37.08),
        (108, 130000, '河北省', 130500, '邢台市', 130522, '临城县', 114.5, 37.43),
        (109, 130000, '河北省', 130500, '邢台市', 130523, '内丘县', 114.52, 37.3),
        (110, 130000, '河北省', 130500, '邢台市', 130524, '柏乡县', 114.68, 37.5),
        (111, 130000, '河北省', 130500, '邢台市', 130525, '隆尧县', 114.77, 37.35),
        (112, 130000, '河北省', 130500, '邢台市', 130526, '任县', 114.68, 37.13),
        (113, 130000, '河北省', 130500, '邢台市', 130527, '南和县', 114.68, 37),
        (114, 130000, '河北省', 130500, '邢台市', 130528, '宁晋县', 114.92, 37.62),
        (115, 130000, '河北省', 130500, '邢台市', 130529, '巨鹿县', 115.03, 37.22),
        (116, 130000, '河北省', 130500, '邢台市', 130530, '新河县', 115.25, 37.53),
        (117, 130000, '河北省', 130500, '邢台市', 130531, '广宗县', 115.15, 37.07),
        (118, 130000, '河北省', 130500, '邢台市', 130532, '平乡县', 115.03, 37.07),
        (119, 130000, '河北省', 130500, '邢台市', 130533, '威县', 115.25, 36.98),
        (120, 130000, '河北省', 130500, '邢台市', 130534, '清河县', 115.67, 37.07),
        (121, 130000, '河北省', 130500, '邢台市', 130535, '临西县', 115.5, 36.85),
        (122, 130000, '河北省', 130500, '邢台市', 130581, '南宫市', 115.38, 37.35),
        (123, 130000, '河北省', 130500, '邢台市', 130582, '沙河市', 114.5, 36.85),
        (124, 130000, '河北省', 130600, '保定市', 130601, '市辖区', 115.47, 38.87),
        (125, 130000, '河北省', 130600, '保定市', 130602, '新市区', 115.45, 38.87),
        (126, 130000, '河北省', 130600, '保定市', 130603, '北市区', 115.48, 38.87),
        (127, 130000, '河北省', 130600, '保定市', 130604, '南市区', 115.5, 38.85),
        (128, 130000, '河北省', 130600, '保定市', 130621, '满城县', 115.32, 38.95),
        (129, 130000, '河北省', 130600, '保定市', 130622, '清苑县', 115.48, 38.77),
        (130, 130000, '河北省', 130600, '保定市', 130623, '涞水县', 115.72, 39.4),
        (131, 130000, '河北省', 130600, '保定市', 130624, '阜平县', 114.18, 38.85),
        (132, 130000, '河北省', 130600, '保定市', 130625, '徐水县', 115.65, 39.02),
        (133, 130000, '河北省', 130600, '保定市', 130626, '定兴县', 115.77, 39.27),
        (134, 130000, '河北省', 130600, '保定市', 130627, '唐县', 114.98, 38.75),
        (135, 130000, '河北省', 130600, '保定市', 130628, '高阳县', 115.78, 38.68),
        (136, 130000, '河北省', 130600, '保定市', 130629, '容城县', 115.87, 39.05),
        (137, 130000, '河北省', 130600, '保定市', 130630, '涞源县', 114.68, 39.35),
        (138, 130000, '河北省', 130600, '保定市', 130631, '望都县', 115.15, 38.72),
        (139, 130000, '河北省', 130600, '保定市', 130632, '安新县', 115.93, 38.92),
        (140, 130000, '河北省', 130600, '保定市', 130633, '易县', 115.5, 39.35),
        (141, 130000, '河北省', 130600, '保定市', 130634, '曲阳县', 114.7, 38.62),
        (142, 130000, '河北省', 130600, '保定市', 130635, '蠡县', 115.57, 38.48),
        (143, 130000, '河北省', 130600, '保定市', 130636, '顺平县', 115.13, 38.83),
        (144, 130000, '河北省', 130600, '保定市', 130637, '博野县', 115.47, 38.45),
        (145, 130000, '河北省', 130600, '保定市', 130638, '雄县', 116.1, 38.98),
        (146, 130000, '河北省', 130600, '保定市', 130681, '涿州市', 115.97, 39.48),
        (147, 130000, '河北省', 130600, '保定市', 130682, '定州市', 114.97, 38.52),
        (148, 130000, '河北省', 130600, '保定市', 130683, '安国市', 115.32, 38.42),
        (149, 130000, '河北省', 130600, '保定市', 130684, '高碑店市', 115.85, 39.33),
        (150, 130000, '河北省', 130700, '张家口市', 130701, '市辖区', 114.88, 40.82),
        (151, 130000, '河北省', 130700, '张家口市', 130702, '桥东区', 114.5, 37.07),
        (152, 130000, '河北省', 130700, '张家口市', 130703, '桥西区', 114.47, 37.05),
        (153, 130000, '河北省', 130700, '张家口市', 130705, '宣化区', 115.05, 40.6),
        (154, 130000, '河北省', 130700, '张家口市', 130706, '下花园区', 115.27, 40.48),
        (155, 130000, '河北省', 130700, '张家口市', 130721, '宣化县', 115.02, 40.55),
        (156, 130000, '河北省', 130700, '张家口市', 130722, '张北县', 114.7, 41.15),
        (157, 130000, '河北省', 130700, '张家口市', 130723, '康保县', 114.62, 41.85),
        (158, 130000, '河北省', 130700, '张家口市', 130724, '沽源县', 115.7, 41.67),
        (159, 130000, '河北省', 130700, '张家口市', 130725, '尚义县', 113.97, 41.08),
        (160, 130000, '河北省', 130700, '张家口市', 130726, '蔚县', 114.57, 39.85),
        (161, 130000, '河北省', 130700, '张家口市', 130727, '阳原县', 114.17, 40.12),
        (162, 130000, '河北省', 130700, '张家口市', 130728, '怀安县', 114.42, 40.67),
        (163, 130000, '河北省', 130700, '张家口市', 130729, '万全县', 114.72, 40.75),
        (164, 130000, '河北省', 130700, '张家口市', 130730, '怀来县', 115.52, 40.4),
        (165, 130000, '河北省', 130700, '张家口市', 130731, '涿鹿县', 115.22, 40.38),
        (166, 130000, '河北省', 130700, '张家口市', 130732, '赤城县', 115.83, 40.92),
        (167, 130000, '河北省', 130700, '张家口市', 130733, '崇礼县', 115.27, 40.97),
        (168, 130000, '河北省', 130800, '承德市', 130801, '市辖区', 117.93, 40.97),
        (169, 130000, '河北省', 130800, '承德市', 130802, '双桥区', 117.93, 40.97),
        (170, 130000, '河北省', 130800, '承德市', 130803, '双滦区', 117.78, 40.95),
        (171, 130000, '河北省', 130800, '承德市', 130804, '鹰手营子矿区', 117.65, 40.55),
        (172, 130000, '河北省', 130800, '承德市', 130821, '承德县', 118.17, 40.77),
        (173, 130000, '河北省', 130800, '承德市', 130822, '兴隆县', 117.52, 40.43),
        (174, 130000, '河北省', 130800, '承德市', 130823, '平泉县', 118.68, 41),
        (175, 130000, '河北省', 130800, '承德市', 130824, '滦平县', 117.33, 40.93),
        (176, 130000, '河北省', 130800, '承德市', 130825, '隆化县', 117.72, 41.32),
        (177, 130000, '河北省', 130800, '承德市', 130826, '丰宁满族自治县', 116.65, 41.2),
        (178, 130000, '河北省', 130800, '承德市', 130827, '宽城满族自治县', 118.48, 40.6),
        (179, 130000, '河北省', 130800, '承德市', 130828, '围场满族蒙古族自治县', 117.75, 41.93),
        (180, 130000, '河北省', 130900, '沧州市', 130901, '市辖区', 116.83, 38.3),
        (181, 130000, '河北省', 130900, '沧州市', 130902, '新华区', 116.87, 38.32),
        (182, 130000, '河北省', 130900, '沧州市', 130903, '运河区', 116.85, 38.32),
        (183, 130000, '河北省', 130900, '沧州市', 130921, '沧县', 116.87, 38.3),
        (184, 130000, '河北省', 130900, '沧州市', 130922, '青县', 116.82, 38.58),
        (185, 130000, '河北省', 130900, '沧州市', 130923, '东光县', 116.53, 37.88),
        (186, 130000, '河北省', 130900, '沧州市', 130924, '海兴县', 117.48, 38.13),
        (187, 130000, '河北省', 130900, '沧州市', 130925, '盐山县', 117.22, 38.05),
        (188, 130000, '河北省', 130900, '沧州市', 130926, '肃宁县', 115.83, 38.43),
        (189, 130000, '河北省', 130900, '沧州市', 130927, '南皮县', 116.7, 38.03),
        (190, 130000, '河北省', 130900, '沧州市', 130928, '吴桥县', 116.38, 37.62),
        (191, 130000, '河北省', 130900, '沧州市', 130929, '献县', 116.12, 38.18),
        (192, 130000, '河北省', 130900, '沧州市', 130930, '孟村回族自治县', 117.1, 38.07),
        (193, 130000, '河北省', 130900, '沧州市', 130981, '泊头市', 116.57, 38.07),
        (194, 130000, '河北省', 130900, '沧州市', 130982, '任丘市', 116.1, 38.72),
        (195, 130000, '河北省', 130900, '沧州市', 130983, '黄骅市', 117.35, 38.37),
        (196, 130000, '河北省', 130900, '沧州市', 130984, '河间市', 116.08, 38.43),
        (197, 130000, '河北省', 131000, '廊坊市', 131001, '市辖区', 116.7, 39.52),
        (198, 130000, '河北省', 131000, '廊坊市', 131002, '安次区', 116.68, 39.52),
        (199, 130000, '河北省', 131000, '廊坊市', 131003, '广阳区', 116.72, 39.53),
        (200, 130000, '河北省', 131000, '廊坊市', 131022, '固安县', 116.3, 39.43),
        (201, 130000, '河北省', 131000, '廊坊市', 131023, '永清县', 116.5, 39.32),
        (202, 130000, '河北省', 131000, '廊坊市', 131024, '香河县', 117, 39.77),
        (203, 130000, '河北省', 131000, '廊坊市', 131025, '大城县', 116.63, 38.7),
        (204, 130000, '河北省', 131000, '廊坊市', 131026, '文安县', 116.47, 38.87),
        (205, 130000, '河北省', 131000, '廊坊市', 131028, '大厂回族自治县', 116.98, 39.88),
        (206, 130000, '河北省', 131000, '廊坊市', 131081, '霸州市', 116.4, 39.1),
        (207, 130000, '河北省', 131000, '廊坊市', 131082, '三河市', 117.07, 39.98),
        (208, 130000, '河北省', 131100, '衡水市', 131101, '市辖区', 115.68, 37.73),
        (209, 130000, '河北省', 131100, '衡水市', 131102, '桃城区', 115.68, 37.73),
        (210, 130000, '河北省', 131100, '衡水市', 131121, '枣强县', 115.72, 37.52),
        (211, 130000, '河北省', 131100, '衡水市', 131122, '武邑县', 115.88, 37.82),
        (212, 130000, '河北省', 131100, '衡水市', 131123, '武强县', 115.98, 38.03),
        (213, 130000, '河北省', 131100, '衡水市', 131124, '饶阳县', 115.73, 38.23),
        (214, 130000, '河北省', 131100, '衡水市', 131125, '安平县', 115.52, 38.23),
        (215, 130000, '河北省', 131100, '衡水市', 131126, '故城县', 115.97, 37.35),
        (216, 130000, '河北省', 131100, '衡水市', 131127, '景县', 116.27, 37.7),
        (217, 130000, '河北省', 131100, '衡水市', 131128, '阜城县', 116.15, 37.87),
        (218, 130000, '河北省', 131100, '衡水市', 131181, '冀州市', 115.57, 37.57),
        (219, 130000, '河北省', 131100, '衡水市', 131182, '深州市', 115.55, 38.02),
        (220, 140000, '山西省', 140100, '太原市', 140101, '市辖区', 112.55, 37.87),
        (221, 140000, '山西省', 140100, '太原市', 140105, '小店区', 112.57, 37.73),
        (222, 140000, '山西省', 140100, '太原市', 140106, '迎泽区', 112.57, 37.87),
        (223, 140000, '山西省', 140100, '太原市', 140107, '杏花岭区', 112.57, 37.88),
        (224, 140000, '山西省', 140100, '太原市', 140108, '尖草坪区', 112.48, 37.93),
        (225, 140000, '山西省', 140100, '太原市', 140109, '万柏林区', 112.52, 37.87),
        (226, 140000, '山西省', 140100, '太原市', 140110, '晋源区', 112.48, 37.73),
        (227, 140000, '山西省', 140100, '太原市', 140121, '清徐县', 112.35, 37.6),
        (228, 140000, '山西省', 140100, '太原市', 140122, '阳曲县', 112.67, 38.07),
        (229, 140000, '山西省', 140100, '太原市', 140123, '娄烦县', 111.78, 38.07),
        (230, 140000, '山西省', 140100, '太原市', 140181, '古交市', 112.17, 37.92),
        (231, 140000, '山西省', 140200, '大同市', 140201, '市辖区', 113.3, 40.08),
        (232, 140000, '山西省', 140200, '大同市', 140202, '城区', 112.83, 35.5),
        (233, 140000, '山西省', 140200, '大同市', 140203, '矿区', 113.57, 37.87),
        (234, 140000, '山西省', 140200, '大同市', 140211, '南郊区', 113.13, 40),
        (235, 140000, '山西省', 140200, '大同市', 140212, '新荣区', 113.15, 40.27),
        (236, 140000, '山西省', 140200, '大同市', 140221, '阳高县', 113.75, 40.37),
        (237, 140000, '山西省', 140200, '大同市', 140222, '天镇县', 114.08, 40.42),
        (238, 140000, '山西省', 140200, '大同市', 140223, '广灵县', 114.28, 39.77),
        (239, 140000, '山西省', 140200, '大同市', 140224, '灵丘县', 114.23, 39.43),
        (240, 140000, '山西省', 140200, '大同市', 140225, '浑源县', 113.68, 39.7),
        (241, 140000, '山西省', 140200, '大同市', 140226, '左云县', 112.7, 40),
        (242, 140000, '山西省', 140200, '大同市', 140227, '大同县', 113.6, 40.03),
        (243, 140000, '山西省', 140300, '阳泉市', 140301, '市辖区', 113.57, 37.85),
        (244, 140000, '山西省', 140300, '阳泉市', 140302, '城区', 112.83, 35.5),
        (245, 140000, '山西省', 140300, '阳泉市', 140303, '矿区', 113.57, 37.87),
        (246, 140000, '山西省', 140300, '阳泉市', 140311, '郊区', 113.12, 36.2),
        (247, 140000, '山西省', 140300, '阳泉市', 140321, '平定县', 113.62, 37.8),
        (248, 140000, '山西省', 140300, '阳泉市', 140322, '盂县', 113.4, 38.08),
        (249, 140000, '山西省', 140400, '长治市', 140401, '市辖区', 113.12, 36.2),
        (250, 140000, '山西省', 140400, '长治市', 140402, '城区', 112.83, 35.5),
        (251, 140000, '山西省', 140400, '长治市', 140411, '郊区', 113.12, 36.2),
        (252, 140000, '山西省', 140400, '长治市', 140421, '长治县', 113.03, 36.05),
        (253, 140000, '山西省', 140400, '长治市', 140423, '襄垣县', 113.05, 36.53),
        (254, 140000, '山西省', 140400, '长治市', 140424, '屯留县', 112.88, 36.32),
        (255, 140000, '山西省', 140400, '长治市', 140425, '平顺县', 113.43, 36.2),
        (256, 140000, '山西省', 140400, '长治市', 140426, '黎城县', 113.38, 36.5),
        (257, 140000, '山西省', 140400, '长治市', 140427, '壶关县', 113.2, 36.12),
        (258, 140000, '山西省', 140400, '长治市', 140428, '长子县', 112.87, 36.12),
        (259, 140000, '山西省', 140400, '长治市', 140429, '武乡县', 112.85, 36.83),
        (260, 140000, '山西省', 140400, '长治市', 140430, '沁县', 112.7, 36.75),
        (261, 140000, '山西省', 140400, '长治市', 140431, '沁源县', 112.33, 36.5),
        (262, 140000, '山西省', 140400, '长治市', 140481, '潞城市', 113.22, 36.33),
        (263, 140000, '山西省', 140500, '晋城市', 140501, '市辖区', 112.83, 35.5),
        (264, 140000, '山西省', 140500, '晋城市', 140502, '城区', 112.83, 35.5),
        (265, 140000, '山西省', 140500, '晋城市', 140521, '沁水县', 112.18, 35.68),
        (266, 140000, '山西省', 140500, '晋城市', 140522, '阳城县', 112.42, 35.48),
        (267, 140000, '山西省', 140500, '晋城市', 140524, '陵川县', 113.27, 35.78),
        (268, 140000, '山西省', 140500, '晋城市', 140525, '泽州县', 112.83, 35.5),
        (269, 140000, '山西省', 140500, '晋城市', 140581, '高平市', 112.92, 35.8),
        (270, 140000, '山西省', 140600, '朔州市', 140601, '市辖区', 112.43, 39.33),
        (271, 140000, '山西省', 140600, '朔州市', 140602, '朔城区', 112.43, 39.33),
        (272, 140000, '山西省', 140600, '朔州市', 140603, '平鲁区', 0, 0),
        (273, 140000, '山西省', 140600, '朔州市', 140621, '山阴县', 112.82, 39.52),
        (274, 140000, '山西省', 140600, '朔州市', 140622, '应县', 113.18, 39.55),
        (275, 140000, '山西省', 140600, '朔州市', 140623, '右玉县', 112.47, 39.98),
        (276, 140000, '山西省', 140600, '朔州市', 140624, '怀仁县', 113.08, 39.83),
        (277, 140000, '山西省', 140700, '晋中市', 140701, '市辖区', 112.75, 37.68),
        (278, 140000, '山西省', 140700, '晋中市', 140702, '榆次区', 112.75, 37.68),
        (279, 140000, '山西省', 140700, '晋中市', 140721, '榆社县', 112.97, 37.07),
        (280, 140000, '山西省', 140700, '晋中市', 140722, '左权县', 113.37, 37.07),
        (281, 140000, '山西省', 140700, '晋中市', 140723, '和顺县', 113.57, 37.33),
        (282, 140000, '山西省', 140700, '晋中市', 140724, '昔阳县', 113.7, 37.62),
        (283, 140000, '山西省', 140700, '晋中市', 140725, '寿阳县', 113.18, 37.88),
        (284, 140000, '山西省', 140700, '晋中市', 140726, '太谷县', 112.55, 37.42),
        (285, 140000, '山西省', 140700, '晋中市', 140727, '祁县', 112.33, 37.35),
        (286, 140000, '山西省', 140700, '晋中市', 140728, '平遥县', 112.17, 37.18),
        (287, 140000, '山西省', 140700, '晋中市', 140729, '灵石县', 111.77, 36.85),
        (288, 140000, '山西省', 140700, '晋中市', 140781, '介休市', 111.92, 37.03),
        (289, 140000, '山西省', 140800, '运城市', 140801, '市辖区', 110.98, 35.02),
        (290, 140000, '山西省', 140800, '运城市', 140802, '盐湖区', 110.98, 35.02),
        (291, 140000, '山西省', 140800, '运城市', 140821, '临猗县', 110.77, 35.15),
        (292, 140000, '山西省', 140800, '运城市', 140822, '万荣县', 110.83, 35.42),
        (293, 140000, '山西省', 140800, '运城市', 140823, '闻喜县', 111.22, 35.35),
        (294, 140000, '山西省', 140800, '运城市', 140824, '稷山县', 110.97, 35.6),
        (295, 140000, '山西省', 140800, '运城市', 140825, '新绛县', 111.22, 35.62),
        (296, 140000, '山西省', 140800, '运城市', 140826, '绛县', 111.57, 35.48),
        (297, 140000, '山西省', 140800, '运城市', 140827, '垣曲县', 111.67, 35.3),
        (298, 140000, '山西省', 140800, '运城市', 140828, '夏县', 111.22, 35.15),
        (299, 140000, '山西省', 140800, '运城市', 140829, '平陆县', 111.22, 34.83),
        (300, 140000, '山西省', 140800, '运城市', 140830, '芮城县', 110.68, 34.7),
        (301, 140000, '山西省', 140800, '运城市', 140881, '永济市', 0, 0),
        (302, 140000, '山西省', 140800, '运城市', 140882, '河津市', 110.7, 35.6),
        (303, 140000, '山西省', 140900, '忻州市', 140901, '市辖区', 112.73, 38.42),
        (304, 140000, '山西省', 140900, '忻州市', 140902, '忻府区', 112.73, 38.42),
        (305, 140000, '山西省', 140900, '忻州市', 140921, '定襄县', 112.95, 38.48),
        (306, 140000, '山西省', 140900, '忻州市', 140922, '五台县', 113.25, 38.73),
        (307, 140000, '山西省', 140900, '忻州市', 140923, '代县', 112.95, 39.07),
        (308, 140000, '山西省', 140900, '忻州市', 140924, '繁峙县', 113.25, 39.18),
        (309, 140000, '山西省', 140900, '忻州市', 140925, '宁武县', 112.3, 39),
        (310, 140000, '山西省', 140900, '忻州市', 140926, '静乐县', 111.93, 38.37),
        (311, 140000, '山西省', 140900, '忻州市', 140927, '神池县', 112.2, 39.08),
        (312, 140000, '山西省', 140900, '忻州市', 140928, '五寨县', 111.85, 38.9),
        (313, 140000, '山西省', 140900, '忻州市', 140929, '岢岚县', 111.57, 38.7),
        (314, 140000, '山西省', 140900, '忻州市', 140930, '河曲县', 111.13, 39.38),
        (315, 140000, '山西省', 140900, '忻州市', 140931, '保德县', 0, 0),
        (316, 140000, '山西省', 140900, '忻州市', 140932, '偏关县', 111.5, 39.43),
        (317, 140000, '山西省', 140900, '忻州市', 140981, '原平市', 112.7, 38.73),
        (318, 140000, '山西省', 141000, '临汾市', 141001, '市辖区', 111.52, 36.08),
        (319, 140000, '山西省', 141000, '临汾市', 141002, '尧都区', 111.52, 36.08),
        (320, 140000, '山西省', 141000, '临汾市', 141021, '曲沃县', 111.47, 35.63),
        (321, 140000, '山西省', 141000, '临汾市', 141022, '翼城县', 111.72, 35.73),
        (322, 140000, '山西省', 141000, '临汾市', 141023, '襄汾县', 111.43, 35.88),
        (323, 140000, '山西省', 141000, '临汾市', 141024, '洪洞县', 111.67, 36.25),
        (324, 140000, '山西省', 141000, '临汾市', 141025, '古县', 111.92, 36.27),
        (325, 140000, '山西省', 141000, '临汾市', 141026, '安泽县', 112.25, 36.15),
        (326, 140000, '山西省', 141000, '临汾市', 141027, '浮山县', 111.83, 35.97),
        (327, 140000, '山西省', 141000, '临汾市', 141028, '吉县', 110.68, 36.1),
        (328, 140000, '山西省', 141000, '临汾市', 141029, '乡宁县', 110.83, 35.97),
        (329, 140000, '山西省', 141000, '临汾市', 141030, '大宁县', 110.75, 36.47),
        (330, 140000, '山西省', 141000, '临汾市', 141031, '隰县', 110.93, 36.7),
        (331, 140000, '山西省', 141000, '临汾市', 141032, '永和县', 110.63, 36.77),
        (332, 140000, '山西省', 141000, '临汾市', 141033, '蒲县', 111.08, 36.42),
        (333, 140000, '山西省', 141000, '临汾市', 141034, '汾西县', 111.57, 36.65),
        (334, 140000, '山西省', 141000, '临汾市', 141081, '侯马市', 111.35, 35.62),
        (335, 140000, '山西省', 141000, '临汾市', 141082, '霍州市', 111.72, 36.57),
        (336, 140000, '山西省', 141100, '吕梁市', 141101, '市辖区', 111.13, 37.52),
        (337, 140000, '山西省', 141100, '吕梁市', 141102, '离石区', 111.13, 37.52),
        (338, 140000, '山西省', 141100, '吕梁市', 141121, '文水县', 112.02, 37.43),
        (339, 140000, '山西省', 141100, '吕梁市', 141122, '交城县', 112.15, 37.55),
        (340, 140000, '山西省', 141100, '吕梁市', 141123, '兴县', 111.12, 38.47),
        (341, 140000, '山西省', 141100, '吕梁市', 141124, '临县', 110.98, 37.95),
        (342, 140000, '山西省', 141100, '吕梁市', 141125, '柳林县', 110.9, 37.43),
        (343, 140000, '山西省', 141100, '吕梁市', 141126, '石楼县', 110.83, 37),
        (344, 140000, '山西省', 141100, '吕梁市', 141127, '岚县', 111.67, 38.28),
        (345, 140000, '山西省', 141100, '吕梁市', 141128, '方山县', 111.23, 37.88),
        (346, 140000, '山西省', 141100, '吕梁市', 141129, '中阳县', 111.18, 37.33),
        (347, 140000, '山西省', 141100, '吕梁市', 141130, '交口县', 111.2, 36.97),
        (348, 140000, '山西省', 141100, '吕梁市', 141181, '孝义市', 111.77, 37.15),
        (349, 140000, '山西省', 141100, '吕梁市', 141182, '汾阳市', 111.78, 37.27),
        (350, 150000, '内蒙古', 150100, '呼和浩特市', 150101, '市辖区', 111.73, 40.83),
        (351, 150000, '内蒙古', 150100, '呼和浩特市', 150102, '新城区', 111.65, 40.87),
        (352, 150000, '内蒙古', 150100, '呼和浩特市', 150103, '回民区', 111.6, 40.8),
        (353, 150000, '内蒙古', 150100, '呼和浩特市', 150104, '玉泉区', 111.67, 40.75),
        (354, 150000, '内蒙古', 150100, '呼和浩特市', 150105, '赛罕区', 111.68, 40.8),
        (355, 150000, '内蒙古', 150100, '呼和浩特市', 150121, '土默特左旗', 111.13, 40.72),
        (356, 150000, '内蒙古', 150100, '呼和浩特市', 150122, '托克托县', 111.18, 40.27),
        (357, 150000, '内蒙古', 150100, '呼和浩特市', 150123, '和林格尔县', 111.82, 40.38),
        (358, 150000, '内蒙古', 150100, '呼和浩特市', 150124, '清水河县', 111.68, 39.92),
        (359, 150000, '内蒙古', 150100, '呼和浩特市', 150125, '武川县', 111.45, 41.08),
        (360, 150000, '内蒙古', 150200, '包头市', 150201, '市辖区', 109.83, 40.65),
        (361, 150000, '内蒙古', 150200, '包头市', 150202, '东河区', 110.02, 40.58),
        (362, 150000, '内蒙古', 150200, '包头市', 150203, '昆都仑区', 109.83, 40.63),
        (363, 150000, '内蒙古', 150200, '包头市', 150204, '青山区', 109.9, 40.65),
        (364, 150000, '内蒙古', 150200, '包头市', 150205, '石拐区', 110.27, 40.68),
        (365, 150000, '内蒙古', 150200, '包头市', 150206, '白云矿区', 0, 0),
        (366, 150000, '内蒙古', 150200, '包头市', 150207, '九原区', 109.97, 40.6),
        (367, 150000, '内蒙古', 150200, '包头市', 150221, '土默特右旗', 110.52, 40.57),
        (368, 150000, '内蒙古', 150200, '包头市', 150222, '固阳县', 110.05, 41.03),
        (369, 150000, '内蒙古', 150200, '包头市', 150223, '达尔罕茂明安联合旗', 110.43, 41.7),
        (370, 150000, '内蒙古', 150300, '乌海市', 150301, '市辖区', 106.82, 39.67),
        (371, 150000, '内蒙古', 150300, '乌海市', 150302, '海勃湾区', 106.83, 39.7),
        (372, 150000, '内蒙古', 150300, '乌海市', 150303, '海南区', 106.88, 39.43),
        (373, 150000, '内蒙古', 150300, '乌海市', 150304, '乌达区', 106.7, 39.5),
        (374, 150000, '内蒙古', 150400, '赤峰市', 150401, '市辖区', 118.92, 42.27),
        (375, 150000, '内蒙古', 150400, '赤峰市', 150402, '红山区', 118.97, 42.28),
        (376, 150000, '内蒙古', 150400, '赤峰市', 150403, '元宝山区', 119.28, 42.03),
        (377, 150000, '内蒙古', 150400, '赤峰市', 150404, '松山区', 118.92, 42.28),
        (378, 150000, '内蒙古', 150400, '赤峰市', 150421, '阿鲁科尔沁旗', 120.08, 43.88),
        (379, 150000, '内蒙古', 150400, '赤峰市', 150422, '巴林左旗', 119.38, 43.98),
        (380, 150000, '内蒙古', 150400, '赤峰市', 150423, '巴林右旗', 118.67, 43.52),
        (381, 150000, '内蒙古', 150400, '赤峰市', 150424, '林西县', 118.05, 43.6),
        (382, 150000, '内蒙古', 150400, '赤峰市', 150425, '克什克腾旗', 117.53, 43.25),
        (383, 150000, '内蒙古', 150400, '赤峰市', 150426, '翁牛特旗', 119.02, 42.93),
        (384, 150000, '内蒙古', 150400, '赤峰市', 150428, '喀喇沁旗', 118.7, 41.93),
        (385, 150000, '内蒙古', 150400, '赤峰市', 150429, '宁城县', 119.33, 41.6),
        (386, 150000, '内蒙古', 150400, '赤峰市', 150430, '敖汉旗', 119.9, 42.28),
        (387, 150000, '内蒙古', 150500, '通辽市', 150501, '市辖区', 122.27, 43.62),
        (388, 150000, '内蒙古', 150500, '通辽市', 150502, '科尔沁区', 122.27, 43.62),
        (389, 150000, '内蒙古', 150500, '通辽市', 150521, '科尔沁左翼中旗', 123.32, 44.13),
        (390, 150000, '内蒙古', 150500, '通辽市', 150522, '科尔沁左翼后旗', 122.35, 42.95),
        (391, 150000, '内蒙古', 150500, '通辽市', 150523, '开鲁县', 121.3, 43.6),
        (392, 150000, '内蒙古', 150500, '通辽市', 150524, '库伦旗', 121.77, 42.73),
        (393, 150000, '内蒙古', 150500, '通辽市', 150525, '奈曼旗', 120.65, 42.85),
        (394, 150000, '内蒙古', 150500, '通辽市', 150526, '扎鲁特旗', 120.92, 44.55),
        (395, 150000, '内蒙古', 150500, '通辽市', 150581, '霍林郭勒市', 119.65, 45.53),
        (396, 150000, '内蒙古', 150600, '鄂尔多斯市', 150602, '东胜区', 110, 39.82),
        (397, 150000, '内蒙古', 150600, '鄂尔多斯市', 150621, '达拉特旗', 110.03, 40.4),
        (398, 150000, '内蒙古', 150600, '鄂尔多斯市', 150622, '准格尔旗', 111.23, 39.87),
        (399, 150000, '内蒙古', 150600, '鄂尔多斯市', 150623, '鄂托克前旗', 107.48, 38.18),
        (400, 150000, '内蒙古', 150600, '鄂尔多斯市', 150624, '鄂托克旗', 107.98, 39.1),
        (401, 150000, '内蒙古', 150600, '鄂尔多斯市', 150625, '杭锦旗', 108.72, 39.83),
        (402, 150000, '内蒙古', 150600, '鄂尔多斯市', 150626, '乌审旗', 108.85, 38.6),
        (403, 150000, '内蒙古', 150600, '鄂尔多斯市', 150627, '伊金霍洛旗', 109.73, 39.57),
        (404, 150000, '内蒙古', 150700, '呼伦贝尔市', 150701, '市辖区', 119.77, 49.22),
        (405, 150000, '内蒙古', 150700, '呼伦贝尔市', 150702, '海拉尔区', 119.77, 49.22),
        (406, 150000, '内蒙古', 150700, '呼伦贝尔市', 150721, '阿荣旗', 123.47, 48.13),
        (407, 150000, '内蒙古', 150700, '呼伦贝尔市', 150722, '莫力达瓦达斡尔族自治旗', 0, 0),
        (408, 150000, '内蒙古', 150700, '呼伦贝尔市', 150723, '鄂伦春自治旗', 123.72, 50.58),
        (409, 150000, '内蒙古', 150700, '呼伦贝尔市', 150724, '鄂温克族自治旗', 119.75, 49.13),
        (410, 150000, '内蒙古', 150700, '呼伦贝尔市', 150725, '陈巴尔虎旗', 119.43, 49.32),
        (411, 150000, '内蒙古', 150700, '呼伦贝尔市', 150726, '新巴尔虎左旗', 118.27, 48.22),
        (412, 150000, '内蒙古', 150700, '呼伦贝尔市', 150727, '新巴尔虎右旗', 116.82, 48.67),
        (413, 150000, '内蒙古', 150700, '呼伦贝尔市', 150781, '满洲里市', 117.45, 49.58),
        (414, 150000, '内蒙古', 150700, '呼伦贝尔市', 150782, '牙克石市', 120.73, 49.28),
        (415, 150000, '内蒙古', 150700, '呼伦贝尔市', 150783, '扎兰屯市', 122.75, 47.98),
        (416, 150000, '内蒙古', 150700, '呼伦贝尔市', 150784, '额尔古纳市', 120.18, 50.23),
        (417, 150000, '内蒙古', 150700, '呼伦贝尔市', 150785, '根河市', 121.52, 50.78),
        (418, 150000, '内蒙古', 150800, '巴彦淖尔市', 150801, '市辖区', 107.42, 40.75),
        (419, 150000, '内蒙古', 150800, '巴彦淖尔市', 150802, '临河区', 107.4, 40.75),
        (420, 150000, '内蒙古', 150800, '巴彦淖尔市', 150821, '五原县', 108.27, 41.1),
        (421, 150000, '内蒙古', 150800, '巴彦淖尔市', 150822, '磴口县', 107.02, 40.33),
        (422, 150000, '内蒙古', 150800, '巴彦淖尔市', 150823, '乌拉特前旗', 108.65, 40.72),
        (423, 150000, '内蒙古', 150800, '巴彦淖尔市', 150824, '乌拉特中旗', 108.52, 41.57),
        (424, 150000, '内蒙古', 150800, '巴彦淖尔市', 150825, '乌拉特后旗', 107.07, 41.1),
        (425, 150000, '内蒙古', 150800, '巴彦淖尔市', 150826, '杭锦后旗', 107.15, 40.88),
        (426, 150000, '内蒙古', 150900, '乌兰察布市', 150901, '市辖区', 113.12, 40.98),
        (427, 150000, '内蒙古', 150900, '乌兰察布市', 150902, '集宁区', 113.1, 41.03),
        (428, 150000, '内蒙古', 150900, '乌兰察布市', 150921, '卓资县', 112.57, 40.9),
        (429, 150000, '内蒙古', 150900, '乌兰察布市', 150922, '化德县', 114, 41.9),
        (430, 150000, '内蒙古', 150900, '乌兰察布市', 150923, '商都县', 113.53, 41.55),
        (431, 150000, '内蒙古', 150900, '乌兰察布市', 150924, '兴和县', 113.88, 40.88),
        (432, 150000, '内蒙古', 150900, '乌兰察布市', 150925, '凉城县', 112.48, 40.53),
        (433, 150000, '内蒙古', 150900, '乌兰察布市', 150926, '察哈尔右翼前旗', 113.22, 40.78),
        (434, 150000, '内蒙古', 150900, '乌兰察布市', 150927, '察哈尔右翼中旗', 112.63, 41.27),
        (435, 150000, '内蒙古', 150900, '乌兰察布市', 150928, '察哈尔右翼后旗', 113.18, 41.45),
        (436, 150000, '内蒙古', 150900, '乌兰察布市', 150929, '四子王旗', 111.7, 41.52),
        (437, 150000, '内蒙古', 150900, '乌兰察布市', 150981, '丰镇市', 113.15, 40.43),
        (438, 150000, '内蒙古', 152200, '兴安盟', 152201, '乌兰浩特市', 122.05, 46.08),
        (439, 150000, '内蒙古', 152200, '兴安盟', 152202, '阿尔山市', 119.93, 47.18),
        (440, 150000, '内蒙古', 152200, '兴安盟', 152221, '科尔沁右翼前旗', 121.92, 46.07),
        (441, 150000, '内蒙古', 152200, '兴安盟', 152222, '科尔沁右翼中旗', 121.47, 45.05),
        (442, 150000, '内蒙古', 152200, '兴安盟', 152223, '扎赉特旗', 122.9, 46.73),
        (443, 150000, '内蒙古', 152200, '兴安盟', 152224, '突泉县', 121.57, 45.38),
        (444, 150000, '内蒙古', 152500, '锡林郭勒盟', 152501, '二连浩特市', 111.98, 43.65),
        (445, 150000, '内蒙古', 152500, '锡林郭勒盟', 152502, '锡林浩特市', 116.07, 43.93),
        (446, 150000, '内蒙古', 152500, '锡林郭勒盟', 152522, '阿巴嘎旗', 114.97, 44.02),
        (447, 150000, '内蒙古', 152500, '锡林郭勒盟', 152523, '苏尼特左旗', 113.63, 43.85),
        (448, 150000, '内蒙古', 152500, '锡林郭勒盟', 152524, '苏尼特右旗', 112.65, 42.75),
        (449, 150000, '内蒙古', 152500, '锡林郭勒盟', 152525, '东乌珠穆沁旗', 116.97, 45.52),
        (450, 150000, '内蒙古', 152500, '锡林郭勒盟', 152526, '西乌珠穆沁旗', 117.6, 44.58),
        (451, 150000, '内蒙古', 152500, '锡林郭勒盟', 152527, '太仆寺旗', 115.28, 41.9),
        (452, 150000, '内蒙古', 152500, '锡林郭勒盟', 152528, '镶黄旗', 113.83, 42.23),
        (453, 150000, '内蒙古', 152500, '锡林郭勒盟', 152529, '正镶白旗', 115, 42.3),
        (454, 150000, '内蒙古', 152500, '锡林郭勒盟', 152530, '正蓝旗', 116, 42.25),
        (455, 150000, '内蒙古', 152500, '锡林郭勒盟', 152531, '多伦县', 116.47, 42.18),
        (456, 150000, '内蒙古', 152900, '阿拉善盟', 152921, '阿拉善左旗', 105.67, 38.83),
        (457, 150000, '内蒙古', 152900, '阿拉善盟', 152922, '阿拉善右旗', 101.68, 39.2),
        (458, 150000, '内蒙古', 152900, '阿拉善盟', 152923, '额济纳旗', 101.07, 41.97),
        (459, 210000, '辽宁省', 210100, '沈阳市', 210101, '市辖区', 123.43, 41.8),
        (460, 210000, '辽宁省', 210100, '沈阳市', 210102, '和平区', 123.4, 41.78),
        (461, 210000, '辽宁省', 210100, '沈阳市', 210103, '沈河区', 123.45, 41.8),
        (462, 210000, '辽宁省', 210100, '沈阳市', 210104, '大东区', 123.47, 41.8),
        (463, 210000, '辽宁省', 210100, '沈阳市', 210105, '皇姑区', 123.42, 41.82),
        (464, 210000, '辽宁省', 210100, '沈阳市', 210106, '铁西区', 123.35, 41.8),
        (465, 210000, '辽宁省', 210100, '沈阳市', 210111, '苏家屯区', 123.33, 41.67),
        (466, 210000, '辽宁省', 210100, '沈阳市', 210112, '东陵区', 123.47, 41.77),
        (467, 210000, '辽宁省', 210100, '沈阳市', 210113, '沈北新区', 0, 0),
        (468, 210000, '辽宁省', 210100, '沈阳市', 210114, '于洪区', 123.3, 41.78),
        (469, 210000, '辽宁省', 210100, '沈阳市', 210122, '辽中县', 122.72, 41.52),
        (470, 210000, '辽宁省', 210100, '沈阳市', 210123, '康平县', 123.35, 42.75),
        (471, 210000, '辽宁省', 210100, '沈阳市', 210124, '法库县', 123.4, 42.5),
        (472, 210000, '辽宁省', 210100, '沈阳市', 210181, '新民市', 122.82, 42),
        (473, 210000, '辽宁省', 210200, '大连市', 210201, '市辖区', 121.62, 38.92),
        (474, 210000, '辽宁省', 210200, '大连市', 210202, '中山区', 121.63, 38.92),
        (475, 210000, '辽宁省', 210200, '大连市', 210203, '西岗区', 121.6, 38.92),
        (476, 210000, '辽宁省', 210200, '大连市', 210204, '沙河口区', 121.58, 38.9),
        (477, 210000, '辽宁省', 210200, '大连市', 210211, '甘井子区', 121.57, 38.95),
        (478, 210000, '辽宁省', 210200, '大连市', 210212, '旅顺口区', 121.27, 38.82),
        (479, 210000, '辽宁省', 210200, '大连市', 210213, '金州区', 121.7, 39.1),
        (480, 210000, '辽宁省', 210200, '大连市', 210224, '长海县', 122.58, 39.27),
        (481, 210000, '辽宁省', 210200, '大连市', 210281, '瓦房店市', 122, 39.62),
        (482, 210000, '辽宁省', 210200, '大连市', 210282, '普兰店市', 121.95, 39.4),
        (483, 210000, '辽宁省', 210200, '大连市', 210283, '庄河市', 122.98, 39.7),
        (484, 210000, '辽宁省', 210300, '鞍山市', 210301, '市辖区', 122.98, 41.1),
        (485, 210000, '辽宁省', 210300, '鞍山市', 210302, '铁东区', 122.98, 41.1),
        (486, 210000, '辽宁省', 210300, '鞍山市', 210303, '铁西区', 123.35, 41.8),
        (487, 210000, '辽宁省', 210300, '鞍山市', 210304, '立山区', 123, 41.15),
        (488, 210000, '辽宁省', 210300, '鞍山市', 210311, '千山区', 122.97, 41.07),
        (489, 210000, '辽宁省', 210300, '鞍山市', 210321, '台安县', 122.42, 41.38),
        (490, 210000, '辽宁省', 210300, '鞍山市', 210323, '岫岩满族自治县', 123.28, 40.28),
        (491, 210000, '辽宁省', 210300, '鞍山市', 210381, '海城市', 122.7, 40.88),
        (492, 210000, '辽宁省', 210400, '抚顺市', 210401, '市辖区', 123.98, 41.88),
        (493, 210000, '辽宁省', 210400, '抚顺市', 210402, '新抚区', 123.88, 41.87),
        (494, 210000, '辽宁省', 210400, '抚顺市', 210403, '东洲区', 124.02, 41.85),
        (495, 210000, '辽宁省', 210400, '抚顺市', 210404, '望花区', 123.78, 41.85),
        (496, 210000, '辽宁省', 210400, '抚顺市', 210411, '顺城区', 123.93, 41.88),
        (497, 210000, '辽宁省', 210400, '抚顺市', 210421, '抚顺县', 123.9, 41.88),
        (498, 210000, '辽宁省', 210400, '抚顺市', 210422, '新宾满族自治县', 125.03, 41.73),
        (499, 210000, '辽宁省', 210400, '抚顺市', 210423, '清原满族自治县', 124.92, 42.1),
        (500, 210000, '辽宁省', 210500, '本溪市', 210501, '市辖区', 123.77, 41.3),
        (501, 210000, '辽宁省', 210500, '本溪市', 210502, '平山区', 123.77, 41.3),
        (502, 210000, '辽宁省', 210500, '本溪市', 210503, '溪湖区', 123.77, 41.33),
        (503, 210000, '辽宁省', 210500, '本溪市', 210504, '明山区', 123.82, 41.3),
        (504, 210000, '辽宁省', 210500, '本溪市', 210505, '南芬区', 123.73, 41.1),
        (505, 210000, '辽宁省', 210500, '本溪市', 210521, '本溪满族自治县', 124.12, 41.3),
        (506, 210000, '辽宁省', 210500, '本溪市', 210522, '桓仁满族自治县', 125.35, 41.27),
        (507, 210000, '辽宁省', 210600, '丹东市', 210601, '市辖区', 124.38, 40.13),
        (508, 210000, '辽宁省', 210600, '丹东市', 210602, '元宝区', 124.38, 40.13),
        (509, 210000, '辽宁省', 210600, '丹东市', 210603, '振兴区', 124.35, 40.08),
        (510, 210000, '辽宁省', 210600, '丹东市', 210604, '振安区', 124.42, 40.17),
        (511, 210000, '辽宁省', 210600, '丹东市', 210624, '宽甸满族自治县', 124.78, 40.73),
        (512, 210000, '辽宁省', 210600, '丹东市', 210681, '东港市', 124.15, 39.87),
        (513, 210000, '辽宁省', 210600, '丹东市', 210682, '凤城市', 124.07, 40.45),
        (514, 210000, '辽宁省', 210700, '锦州市', 210701, '市辖区', 121.13, 41.1),
        (515, 210000, '辽宁省', 210700, '锦州市', 210702, '古塔区', 121.12, 41.13),
        (516, 210000, '辽宁省', 210700, '锦州市', 210703, '凌河区', 121.15, 41.12),
        (517, 210000, '辽宁省', 210700, '锦州市', 210711, '太和区', 121.1, 41.1),
        (518, 210000, '辽宁省', 210700, '锦州市', 210726, '黑山县', 122.12, 41.7),
        (519, 210000, '辽宁省', 210700, '锦州市', 210727, '义县', 121.23, 41.53),
        (520, 210000, '辽宁省', 210700, '锦州市', 210781, '凌海市', 121.35, 41.17),
        (521, 210000, '辽宁省', 210700, '锦州市', 210782, '北镇市', 0, 0),
        (522, 210000, '辽宁省', 210800, '营口市', 210801, '市辖区', 122.23, 40.67),
        (523, 210000, '辽宁省', 210800, '营口市', 210802, '站前区', 122.27, 40.68),
        (524, 210000, '辽宁省', 210800, '营口市', 210803, '西市区', 122.22, 40.67),
        (525, 210000, '辽宁省', 210800, '营口市', 210804, '鲅鱼圈区', 122.12, 40.27),
        (526, 210000, '辽宁省', 210800, '营口市', 210811, '老边区', 122.37, 40.67),
        (527, 210000, '辽宁省', 210800, '营口市', 210881, '盖州市', 122.35, 40.4),
        (528, 210000, '辽宁省', 210800, '营口市', 210882, '大石桥市', 122.5, 40.65),
        (529, 210000, '辽宁省', 210900, '阜新市', 210901, '市辖区', 121.67, 42.02),
        (530, 210000, '辽宁省', 210900, '阜新市', 210902, '海州区', 121.65, 42.02),
        (531, 210000, '辽宁省', 210900, '阜新市', 210903, '新邱区', 0, 0),
        (532, 210000, '辽宁省', 210900, '阜新市', 210904, '太平区', 121.67, 42.02),
        (533, 210000, '辽宁省', 210900, '阜新市', 210905, '清河门区', 121.42, 41.75),
        (534, 210000, '辽宁省', 210900, '阜新市', 210911, '细河区', 121.68, 42.03),
        (535, 210000, '辽宁省', 210900, '阜新市', 210921, '阜新蒙古族自治县', 121.75, 42.07),
        (536, 210000, '辽宁省', 210900, '阜新市', 210922, '彰武县', 122.53, 42.38),
        (537, 210000, '辽宁省', 211000, '辽阳市', 211001, '市辖区', 123.17, 41.27),
        (538, 210000, '辽宁省', 211000, '辽阳市', 211002, '白塔区', 123.17, 41.27),
        (539, 210000, '辽宁省', 211000, '辽阳市', 211003, '文圣区', 123.18, 41.27),
        (540, 210000, '辽宁省', 211000, '辽阳市', 211004, '宏伟区', 123.2, 41.2),
        (541, 210000, '辽宁省', 211000, '辽阳市', 211005, '弓长岭区', 123.45, 41.13),
        (542, 210000, '辽宁省', 211000, '辽阳市', 211011, '太子河区', 123.18, 41.25),
        (543, 210000, '辽宁省', 211000, '辽阳市', 211021, '辽阳县', 123.07, 41.22),
        (544, 210000, '辽宁省', 211000, '辽阳市', 211081, '灯塔市', 123.33, 41.42),
        (545, 210000, '辽宁省', 211100, '盘锦市', 211101, '市辖区', 122.07, 41.12),
        (546, 210000, '辽宁省', 211100, '盘锦市', 211102, '双台子区', 122.05, 41.2),
        (547, 210000, '辽宁省', 211100, '盘锦市', 211103, '兴隆台区', 122.07, 41.12),
        (548, 210000, '辽宁省', 211100, '盘锦市', 211121, '大洼县', 122.07, 40.98),
        (549, 210000, '辽宁省', 211100, '盘锦市', 211122, '盘山县', 122.02, 41.25),
        (550, 210000, '辽宁省', 211200, '铁岭市', 211201, '市辖区', 123.83, 42.28),
        (551, 210000, '辽宁省', 211200, '铁岭市', 211202, '银州区', 123.85, 42.28),
        (552, 210000, '辽宁省', 211200, '铁岭市', 211204, '清河区', 124.15, 42.53),
        (553, 210000, '辽宁省', 211200, '铁岭市', 211221, '铁岭县', 123.83, 42.3),
        (554, 210000, '辽宁省', 211200, '铁岭市', 211223, '西丰县', 124.72, 42.73),
        (555, 210000, '辽宁省', 211200, '铁岭市', 211224, '昌图县', 124.1, 42.78),
        (556, 210000, '辽宁省', 211200, '铁岭市', 211281, '调兵山市', 123.55, 42.47),
        (557, 210000, '辽宁省', 211200, '铁岭市', 211282, '开原市', 124.03, 42.55),
        (558, 210000, '辽宁省', 211300, '朝阳市', 211301, '市辖区', 120.45, 41.57),
        (559, 210000, '辽宁省', 211300, '朝阳市', 211302, '双塔区', 120.45, 41.57),
        (560, 210000, '辽宁省', 211300, '朝阳市', 211303, '龙城区', 120.43, 41.6),
        (561, 210000, '辽宁省', 211300, '朝阳市', 211321, '朝阳县', 120.47, 41.58),
        (562, 210000, '辽宁省', 211300, '朝阳市', 211322, '建平县', 119.63, 41.4),
        (563, 210000, '辽宁省', 211300, '朝阳市', 211324, '喀喇沁左翼蒙古族自治县', 0, 0),
        (564, 210000, '辽宁省', 211300, '朝阳市', 211381, '北票市', 120.77, 41.8),
        (565, 210000, '辽宁省', 211300, '朝阳市', 211382, '凌源市', 119.4, 41.25),
        (566, 210000, '辽宁省', 211400, '葫芦岛市', 211401, '市辖区', 120.83, 40.72),
        (567, 210000, '辽宁省', 211400, '葫芦岛市', 211402, '连山区', 120.87, 40.77),
        (568, 210000, '辽宁省', 211400, '葫芦岛市', 211403, '龙港区', 120.93, 40.72),
        (569, 210000, '辽宁省', 211400, '葫芦岛市', 211404, '南票区', 120.75, 41.1),
        (570, 210000, '辽宁省', 211400, '葫芦岛市', 211421, '绥中县', 120.33, 40.32),
        (571, 210000, '辽宁省', 211400, '葫芦岛市', 211422, '建昌县', 119.8, 40.82),
        (572, 210000, '辽宁省', 211400, '葫芦岛市', 211481, '兴城市', 120.72, 40.62),
        (573, 220000, '吉林省', 220100, '长春市', 220101, '市辖区', 125.32, 43.9),
        (574, 220000, '吉林省', 220100, '长春市', 220102, '南关区', 125.33, 43.87),
        (575, 220000, '吉林省', 220100, '长春市', 220103, '宽城区', 125.32, 43.92),
        (576, 220000, '吉林省', 220100, '长春市', 220104, '朝阳区', 125.28, 43.83),
        (577, 220000, '吉林省', 220100, '长春市', 220105, '二道区', 125.37, 43.87),
        (578, 220000, '吉林省', 220100, '长春市', 220106, '绿园区', 125.25, 43.88),
        (579, 220000, '吉林省', 220100, '长春市', 220112, '双阳区', 125.67, 43.52),
        (580, 220000, '吉林省', 220100, '长春市', 220122, '农安县', 125.18, 44.43),
        (581, 220000, '吉林省', 220100, '长春市', 220181, '九台市', 125.83, 44.15),
        (582, 220000, '吉林省', 220100, '长春市', 220182, '榆树市', 126.55, 44.82),
        (583, 220000, '吉林省', 220100, '长春市', 220183, '德惠市', 125.7, 44.53),
        (584, 220000, '吉林省', 220200, '吉林市', 220201, '市辖区', 126.55, 43.83),
        (585, 220000, '吉林省', 220200, '吉林市', 220202, '昌邑区', 126.57, 43.88),
        (586, 220000, '吉林省', 220200, '吉林市', 220203, '龙潭区', 126.57, 43.92),
        (587, 220000, '吉林省', 220200, '吉林市', 220204, '船营区', 126.53, 43.83),
        (588, 220000, '吉林省', 220200, '吉林市', 220211, '丰满区', 126.57, 43.82),
        (589, 220000, '吉林省', 220200, '吉林市', 220221, '永吉县', 126.5, 43.67),
        (590, 220000, '吉林省', 220200, '吉林市', 220281, '蛟河市', 127.33, 43.72),
        (591, 220000, '吉林省', 220200, '吉林市', 220282, '桦甸市', 126.73, 42.97),
        (592, 220000, '吉林省', 220200, '吉林市', 220283, '舒兰市', 126.95, 44.42),
        (593, 220000, '吉林省', 220200, '吉林市', 220284, '磐石市', 126.05, 42.95),
        (594, 220000, '吉林省', 220300, '四平市', 220301, '市辖区', 124.35, 43.17), \
        (595, 220000, '吉林省', 220300, '四平市', 220302, '铁西区', 124.35, 43.15), \
        (596, 220000, '吉林省', 220300, '四平市', 220303, '铁东区', 124.38, 43.17), \
        (597, 220000, '吉林省', 220300, '四平市', 220322, '梨树县', 124.33, 43.32), \
        (598, 220000, '吉林省', 220300, '四平市', 220323, '伊通满族自治县', 125.3, 43.35), \
        (599, 220000, '吉林省', 220300, '四平市', 220381, '公主岭市', 124.82, 43.5), \
        (600, 220000, '吉林省', 220300, '四平市', 220382, '双辽市', 123.5, 43.52), \
        (601, 220000, '吉林省', 220400, '辽源市', 220401, '市辖区', 125.13, 42.88), \
        (602, 220000, '吉林省', 220400, '辽源市', 220402, '龙山区', 125.12, 42.9), \
        (603, 220000, '吉林省', 220400, '辽源市', 220403, '西安区', 125.15, 42.92), \
        (604, 220000, '吉林省', 220400, '辽源市', 220421, '东丰县', 125.53, 42.68), \
        (605, 220000, '吉林省', 220400, '辽源市', 220422, '东辽县', 125, 42.92), \
        (606, 220000, '吉林省', 220500, '通化市', 220501, '市辖区', 125.93, 41.73), \
        (607, 220000, '吉林省', 220500, '通化市', 220502, '东昌区', 125.95, 41.73), \
        (608, 220000, '吉林省', 220500, '通化市', 220503, '二道江区', 126.03, 41.77), \
        (609, 220000, '吉林省', 220500, '通化市', 220521, '通化县', 125.75, 41.68), \
        (610, 220000, '吉林省', 220500, '通化市', 220523, '辉南县', 126.03, 42.68), \
        (611, 220000, '吉林省', 220500, '通化市', 220524, '柳河县', 125.73, 42.28), \
        (612, 220000, '吉林省', 220500, '通化市', 220581, '梅河口市', 125.68, 42.53), \
        (613, 220000, '吉林省', 220500, '通化市', 220582, '集安市', 126.18, 41.12), \
        (614, 220000, '吉林省', 220600, '白山市', 220601, '市辖区', 126.42, 41.93), \
        (615, 220000, '吉林省', 220600, '白山市', 220602, '八道江区', 126.4, 41.93), \
        (616, 220000, '吉林省', 220600, '白山市', 220604, '江源区', 0, 0), \
        (617, 220000, '吉林省', 220600, '白山市', 220621, '抚松县', 127.28, 42.33), \
        (618, 220000, '吉林省', 220600, '白山市', 220622, '靖宇县', 126.8, 42.4), \
        (619, 220000, '吉林省', 220600, '白山市', 220623, '长白朝鲜族自治县', 128.2, 41.42), \
        (620, 220000, '吉林省', 220600, '白山市', 220681, '临江市', 126.9, 41.8), \
        (621, 220000, '吉林省', 220700, '松原市', 220701, '市辖区', 124.82, 45.13), \
        (622, 220000, '吉林省', 220700, '松原市', 220702, '宁江区', 124.8, 45.17), \
        (623, 220000, '吉林省', 220700, '松原市', 220721, '前郭尔罗斯蒙古族自治县', 0, 0), \
        (624, 220000, '吉林省', 220700, '松原市', 220722, '长岭县', 123.98, 44.28), \
        (625, 220000, '吉林省', 220700, '松原市', 220723, '乾安县', 124.02, 45.02), \
        (626, 220000, '吉林省', 220700, '松原市', 220724, '扶余县', 126.02, 44.98), \
        (627, 220000, '吉林省', 220800, '白城市', 220801, '市辖区', 122.83, 45.62), \
        (628, 220000, '吉林省', 220800, '白城市', 220802, '洮北区', 122.85, 45.62), \
        (629, 220000, '吉林省', 220800, '白城市', 220821, '镇赉县', 123.2, 45.85), \
        (630, 220000, '吉林省', 220800, '白城市', 220822, '通榆县', 123.08, 44.82), \
        (631, 220000, '吉林省', 220800, '白城市', 220881, '洮南市', 122.78, 45.33), \
        (632, 220000, '吉林省', 220800, '白城市', 220882, '大安市', 124.28, 45.5), \
        (633, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222401, '延吉市', 129.5, 42.88), \
        (634, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222402, '图们市', 129.83, 42.97), \
        (635, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222403, '敦化市', 128.23, 43.37), \
        (636, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222404, '珲春市', 130.37, 42.87), \
        (637, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222405, '龙井市', 129.42, 42.77), \
        (638, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222406, '和龙市', 129, 42.53), \
        (639, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222424, '汪清县', 129.75, 43.32), \
        (640, 220000, '吉林省', 222400, '延边朝鲜族自治州', 222426, '安图县', 128.9, 43.12), \
        (641, 230000, '黑龙江', 230100, '哈尔滨市', 230101, '市辖区', 126.53, 45.8), \
        (642, 230000, '黑龙江', 230100, '哈尔滨市', 230102, '道里区', 126.62, 45.77), \
        (643, 230000, '黑龙江', 230100, '哈尔滨市', 230103, '南岗区', 126.68, 45.77), \
        (644, 230000, '黑龙江', 230100, '哈尔滨市', 230104, '道外区', 126.65, 45.78), \
        (645, 230000, '黑龙江', 230100, '哈尔滨市', 230108, '平房区', 126.62, 45.62), \
        (646, 230000, '黑龙江', 230100, '哈尔滨市', 230109, '松北区', 126.55, 45.8), \
        (647, 230000, '黑龙江', 230100, '哈尔滨市', 230110, '香坊区', 126.68, 45.72), \
        (648, 230000, '黑龙江', 230100, '哈尔滨市', 230111, '呼兰区', 126.58, 45.9), \
        (649, 230000, '黑龙江', 230100, '哈尔滨市', 230112, '阿城区', 0, 0), \
        (650, 230000, '黑龙江', 230100, '哈尔滨市', 230123, '依兰县', 129.55, 46.32), \
        (651, 230000, '黑龙江', 230100, '哈尔滨市', 230124, '方正县', 128.83, 45.83), \
        (652, 230000, '黑龙江', 230100, '哈尔滨市', 230125, '宾县', 127.48, 45.75), \
        (653, 230000, '黑龙江', 230100, '哈尔滨市', 230126, '巴彦县', 127.4, 46.08), \
        (654, 230000, '黑龙江', 230100, '哈尔滨市', 230127, '木兰县', 128.03, 45.95), \
        (655, 230000, '黑龙江', 230100, '哈尔滨市', 230128, '通河县', 128.75, 45.97), \
        (656, 230000, '黑龙江', 230100, '哈尔滨市', 230129, '延寿县', 128.33, 45.45), \
        (657, 230000, '黑龙江', 230100, '哈尔滨市', 230182, '双城市', 126.32, 45.37), \
        (658, 230000, '黑龙江', 230100, '哈尔滨市', 230183, '尚志市', 127.95, 45.22), \
        (659, 230000, '黑龙江', 230100, '哈尔滨市', 230184, '五常市', 127.15, 44.92), \
        (660, 230000, '黑龙江', 230200, '齐齐哈尔市', 230201, '市辖区', 123.95, 47.33), \
        (661, 230000, '黑龙江', 230200, '齐齐哈尔市', 230202, '龙沙区', 123.95, 47.32), \
        (662, 230000, '黑龙江', 230200, '齐齐哈尔市', 230203, '建华区', 123.95, 47.35), \
        (663, 230000, '黑龙江', 230200, '齐齐哈尔市', 230204, '铁锋区', 123.98, 47.35), \
        (664, 230000, '黑龙江', 230200, '齐齐哈尔市', 230205, '昂昂溪区', 123.8, 47.15), \
        (665, 230000, '黑龙江', 230200, '齐齐哈尔市', 230206, '富拉尔基区', 123.62, 47.2), \
        (666, 230000, '黑龙江', 230200, '齐齐哈尔市', 230207, '碾子山区', 0, 0), \
        (667, 230000, '黑龙江', 230200, '齐齐哈尔市', 230208, '梅里斯达斡尔族区', 0, 0), \
        (668, 230000, '黑龙江', 230200, '齐齐哈尔市', 230221, '龙江县', 123.18, 47.33), \
        (669, 230000, '黑龙江', 230200, '齐齐哈尔市', 230223, '依安县', 125.3, 47.88), \
        (670, 230000, '黑龙江', 230200, '齐齐哈尔市', 230224, '泰来县', 123.42, 46.4), \
        (671, 230000, '黑龙江', 230200, '齐齐哈尔市', 230225, '甘南县', 123.5, 47.92), \
        (672, 230000, '黑龙江', 230200, '齐齐哈尔市', 230227, '富裕县', 124.47, 47.82), \
        (673, 230000, '黑龙江', 230200, '齐齐哈尔市', 230229, '克山县', 125.87, 48.03), \
        (674, 230000, '黑龙江', 230200, '齐齐哈尔市', 230230, '克东县', 126.25, 48.03), \
        (675, 230000, '黑龙江', 230200, '齐齐哈尔市', 230231, '拜泉县', 126.08, 47.6), \
        (676, 230000, '黑龙江', 230200, '齐齐哈尔市', 230281, '讷河市', 124.87, 48.48), \
        (677, 230000, '黑龙江', 230300, '鸡西市', 230301, '市辖区', 130.97, 45.3), \
        (678, 230000, '黑龙江', 230300, '鸡西市', 230302, '鸡冠区', 130.97, 45.3), \
        (679, 230000, '黑龙江', 230300, '鸡西市', 230303, '恒山区', 130.93, 45.2), \
        (680, 230000, '黑龙江', 230300, '鸡西市', 230304, '滴道区', 130.78, 45.37), \
        (681, 230000, '黑龙江', 230300, '鸡西市', 230305, '梨树区', 130.68, 45.08), \
        (682, 230000, '黑龙江', 230300, '鸡西市', 230306, '城子河区', 131, 45.33), \
        (683, 230000, '黑龙江', 230300, '鸡西市', 230307, '麻山区', 130.52, 45.2), \
        (684, 230000, '黑龙江', 230300, '鸡西市', 230321, '鸡东县', 131.13, 45.25), \
        (685, 230000, '黑龙江', 230300, '鸡西市', 230381, '虎林市', 132.98, 45.77), \
        (686, 230000, '黑龙江', 230300, '鸡西市', 230382, '密山市', 131.87, 45.55), \
        (687, 230000, '黑龙江', 230400, '鹤岗市', 230401, '市辖区', 130.27, 47.33), \
        (688, 230000, '黑龙江', 230400, '鹤岗市', 230402, '向阳区', 130.33, 46.8), \
        (689, 230000, '黑龙江', 230400, '鹤岗市', 230403, '工农区', 130.25, 47.32), \
        (690, 230000, '黑龙江', 230400, '鹤岗市', 230404, '南山区', 130.28, 47.3), \
        (691, 230000, '黑龙江', 230400, '鹤岗市', 230405, '兴安区', 130.22, 47.27), \
        (692, 230000, '黑龙江', 230400, '鹤岗市', 230406, '东山区', 130.32, 47.33), \
        (693, 230000, '黑龙江', 230400, '鹤岗市', 230407, '兴山区', 130.3, 47.37), \
        (694, 230000, '黑龙江', 230400, '鹤岗市', 230421, '萝北县', 130.83, 47.58), \
        (695, 230000, '黑龙江', 230400, '鹤岗市', 230422, '绥滨县', 131.85, 47.28), \
        (696, 230000, '黑龙江', 230500, '双鸭山市', 230501, '市辖区', 131.15, 46.63), \
        (697, 230000, '黑龙江', 230500, '双鸭山市', 230502, '尖山区', 131.17, 46.63), \
        (698, 230000, '黑龙江', 230500, '双鸭山市', 230503, '岭东区', 131.13, 46.57), \
        (699, 230000, '黑龙江', 230500, '双鸭山市', 230505, '四方台区', 131.33, 46.58), \
        (700, 230000, '黑龙江', 230500, '双鸭山市', 230506, '宝山区', 131.4, 46.57), \
        (701, 230000, '黑龙江', 230500, '双鸭山市', 230521, '集贤县', 131.13, 46.72), \
        (702, 230000, '黑龙江', 230500, '双鸭山市', 230522, '友谊县', 131.8, 46.78), \
        (703, 230000, '黑龙江', 230500, '双鸭山市', 230523, '宝清县', 132.2, 46.32), \
        (704, 230000, '黑龙江', 230500, '双鸭山市', 230524, '饶河县', 134.02, 46.8), \
        (705, 230000, '黑龙江', 230600, '大庆市', 230601, '市辖区', 125.03, 46.58), \
        (706, 230000, '黑龙江', 230600, '大庆市', 230602, '萨尔图区', 125.02, 46.6), \
        (707, 230000, '黑龙江', 230600, '大庆市', 230603, '龙凤区', 125.1, 46.53), \
        (708, 230000, '黑龙江', 230600, '大庆市', 230604, '让胡路区', 124.85, 46.65), \
        (709, 230000, '黑龙江', 230600, '大庆市', 230605, '红岗区', 124.88, 46.4), \
        (710, 230000, '黑龙江', 230600, '大庆市', 230606, '大同区', 124.82, 46.03), \
        (711, 230000, '黑龙江', 230600, '大庆市', 230621, '肇州县', 125.27, 45.7), \
        (712, 230000, '黑龙江', 230600, '大庆市', 230622, '肇源县', 125.08, 45.52), \
        (713, 230000, '黑龙江', 230600, '大庆市', 230623, '林甸县', 124.87, 47.18), \
        (714, 230000, '黑龙江', 230600, '大庆市', 230624, '杜尔伯特蒙古族自治县', 124.45, 46.87), \
        (715, 230000, '黑龙江', 230700, '伊春市', 230701, '市辖区', 128.9, 47.73), \
        (716, 230000, '黑龙江', 230700, '伊春市', 230702, '伊春区', 0, 0), \
        (717, 230000, '黑龙江', 230700, '伊春市', 230703, '南岔区', 129.28, 47.13), \
        (718, 230000, '黑龙江', 230700, '伊春市', 230704, '友好区', 128.82, 47.85), \
        (719, 230000, '黑龙江', 230700, '伊春市', 230705, '西林区', 129.28, 47.48), \
        (720, 230000, '黑龙江', 230700, '伊春市', 230706, '翠峦区', 128.65, 47.72), \
        (721, 230000, '黑龙江', 230700, '伊春市', 230707, '新青区', 129.53, 48.28), \
        (722, 230000, '黑龙江', 230700, '伊春市', 230708, '美溪区', 129.13, 47.63), \
        (723, 230000, '黑龙江', 230700, '伊春市', 230709, '金山屯区', 129.43, 47.42), \
        (724, 230000, '黑龙江', 230700, '伊春市', 230710, '五营区', 129.25, 48.12), \
        (725, 230000, '黑龙江', 230700, '伊春市', 230711, '乌马河区', 128.78, 47.72), \
        (726, 230000, '黑龙江', 230700, '伊春市', 230712, '汤旺河区', 129.57, 48.45), \
        (727, 230000, '黑龙江', 230700, '伊春市', 230713, '带岭区', 129.02, 47.02), \
        (728, 230000, '黑龙江', 230700, '伊春市', 230714, '乌伊岭区', 129.42, 48.6), \
        (729, 230000, '黑龙江', 230700, '伊春市', 230715, '红星区', 129.38, 48.23), \
        (730, 230000, '黑龙江', 230700, '伊春市', 230716, '上甘岭区', 129.02, 47.97), \
        (731, 230000, '黑龙江', 230700, '伊春市', 230722, '嘉荫县', 130.38, 48.88), \
        (732, 230000, '黑龙江', 230700, '伊春市', 230781, '铁力市', 128.02, 46.98), \
        (733, 230000, '黑龙江', 230800, '佳木斯市', 230801, '市辖区', 130.37, 46.82), \
        (734, 230000, '黑龙江', 230800, '佳木斯市', 230803, '向阳区', 130.33, 46.8), \
        (735, 230000, '黑龙江', 230800, '佳木斯市', 230804, '前进区', 130.37, 46.82), \
        (736, 230000, '黑龙江', 230800, '佳木斯市', 230805, '东风区', 130.4, 46.82), \
        (737, 230000, '黑龙江', 230800, '佳木斯市', 230811, '郊区', 130.32, 46.8), \
        (738, 230000, '黑龙江', 230800, '佳木斯市', 230822, '桦南县', 130.57, 46.23), \
        (739, 230000, '黑龙江', 230800, '佳木斯市', 230826, '桦川县', 130.72, 47.02), \
        (740, 230000, '黑龙江', 230800, '佳木斯市', 230828, '汤原县', 129.9, 46.73), \
        (741, 230000, '黑龙江', 230800, '佳木斯市', 230833, '抚远县', 134.28, 48.37), \
        (742, 230000, '黑龙江', 230800, '佳木斯市', 230881, '同江市', 132.52, 47.65), \
        (743, 230000, '黑龙江', 230800, '佳木斯市', 230882, '富锦市', 132.03, 47.25), \
        (744, 230000, '黑龙江', 230900, '七台河市', 230901, '市辖区', 130.95, 45.78), \
        (745, 230000, '黑龙江', 230900, '七台河市', 230902, '新兴区', 130.83, 45.8), \
        (746, 230000, '黑龙江', 230900, '七台河市', 230903, '桃山区', 130.97, 45.77), \
        (747, 230000, '黑龙江', 230900, '七台河市', 230904, '茄子河区', 131.07, 45.77), \
        (748, 230000, '黑龙江', 230900, '七台河市', 230921, '勃利县', 130.57, 45.75), \
        (749, 230000, '黑龙江', 231000, '牡丹江市', 231001, '市辖区', 129.6, 44.58), \
        (750, 230000, '黑龙江', 231000, '牡丹江市', 231002, '东安区', 129.62, 44.58), \
        (751, 230000, '黑龙江', 231000, '牡丹江市', 231003, '阳明区', 129.63, 44.6), \
        (752, 230000, '黑龙江', 231000, '牡丹江市', 231004, '爱民区', 129.58, 44.58), \
        (753, 230000, '黑龙江', 231000, '牡丹江市', 231005, '西安区', 129.62, 44.57), \
        (754, 230000, '黑龙江', 231000, '牡丹江市', 231024, '东宁县', 131.12, 44.07), \
        (755, 230000, '黑龙江', 231000, '牡丹江市', 231025, '林口县', 130.27, 45.3), \
        (756, 230000, '黑龙江', 231000, '牡丹江市', 231081, '绥芬河市', 131.15, 44.42), \
        (757, 230000, '黑龙江', 231000, '牡丹江市', 231083, '海林市', 129.38, 44.57), \
        (758, 230000, '黑龙江', 231000, '牡丹江市', 231084, '宁安市', 129.47, 44.35), \
        (759, 230000, '黑龙江', 231000, '牡丹江市', 231085, '穆棱市', 130.52, 44.92), \
        (760, 230000, '黑龙江', 231100, '黑河市', 231101, '市辖区', 127.48, 50.25), \
        (761, 230000, '黑龙江', 231100, '黑河市', 231102, '爱辉区', 127.48, 50.25), \
        (762, 230000, '黑龙江', 231100, '黑河市', 231121, '嫩江县', 0, 0), \
        (763, 230000, '黑龙江', 231100, '黑河市', 231123, '逊克县', 128.47, 49.58), \
        (764, 230000, '黑龙江', 231100, '黑河市', 231124, '孙吴县', 127.32, 49.42), \
        (765, 230000, '黑龙江', 231100, '黑河市', 231181, '北安市', 126.52, 48.23), \
        (766, 230000, '黑龙江', 231100, '黑河市', 231182, '五大连池市', 126.2, 48.52), \
        (767, 230000, '黑龙江', 231200, '绥化市', 231201, '市辖区', 126.98, 46.63), \
        (768, 230000, '黑龙江', 231200, '绥化市', 231202, '北林区', 126.98, 46.63), \
        (769, 230000, '黑龙江', 231200, '绥化市', 231221, '望奎县', 126.48, 46.83), \
        (770, 230000, '黑龙江', 231200, '绥化市', 231222, '兰西县', 126.28, 46.27), \
        (771, 230000, '黑龙江', 231200, '绥化市', 231223, '青冈县', 126.1, 46.68), \
        (772, 230000, '黑龙江', 231200, '绥化市', 231224, '庆安县', 127.52, 46.88), \
        (773, 230000, '黑龙江', 231200, '绥化市', 231225, '明水县', 125.9, 47.18), \
        (774, 230000, '黑龙江', 231200, '绥化市', 231226, '绥棱县', 127.1, 47.25), \
        (775, 230000, '黑龙江', 231200, '绥化市', 231281, '安达市', 125.33, 46.4), \
        (776, 230000, '黑龙江', 231200, '绥化市', 231282, '肇东市', 125.98, 46.07), \
        (777, 230000, '黑龙江', 231200, '绥化市', 231283, '海伦市', 126.97, 47.47), \
        (778, 230000, '黑龙江', 232700, '大兴安岭地区', 232701, '加格达奇区', 0, 0), \
        (779, 230000, '黑龙江', 232700, '大兴安岭地区', 232702, '松岭区', 0, 0), \
        (780, 230000, '黑龙江', 232700, '大兴安岭地区', 232703, '新林区', 0, 0), \
        (781, 230000, '黑龙江', 232700, '大兴安岭地区', 232704, '呼中区', 0, 0), \
        (782, 230000, '黑龙江', 232700, '大兴安岭地区', 232721, '呼玛县', 126.65, 51.73), \
        (783, 230000, '黑龙江', 232700, '大兴安岭地区', 232722, '塔河县', 124.7, 52.32), \
        (784, 230000, '黑龙江', 232700, '大兴安岭地区', 232723, '漠河县', 122.53, 52.97), \
        (785, 310000, '上海', 310100, '上海市', 310101, '黄浦区', 121.48, 31.23), \
        (786, 310000, '上海', 310100, '上海市', 310103, '卢湾区', 121.47, 31.22), \
        (787, 310000, '上海', 310100, '上海市', 310104, '徐汇区', 121.43, 31.18), \
        (788, 310000, '上海', 310100, '上海市', 310105, '长宁区', 121.42, 31.22), \
        (789, 310000, '上海', 310100, '上海市', 310106, '静安区', 121.45, 31.23), \
        (790, 310000, '上海', 310100, '上海市', 310107, '普陀区', 121.4, 31.25), \
        (791, 310000, '上海', 310100, '上海市', 310108, '闸北区', 121.45, 31.25), \
        (792, 310000, '上海', 310100, '上海市', 310109, '虹口区', 121.5, 31.27), \
        (793, 310000, '上海', 310100, '上海市', 310110, '杨浦区', 121.52, 31.27), \
        (794, 310000, '上海', 310100, '上海市', 310112, '闵行区', 121.38, 31.12), \
        (795, 310000, '上海', 310100, '上海市', 310113, '宝山区', 121.48, 31.4), \
        (796, 310000, '上海', 310100, '上海市', 310114, '嘉定区', 121.27, 31.38), \
        (797, 310000, '上海', 310100, '上海市', 310115, '浦东新区', 121.53, 31.22), \
        (798, 310000, '上海', 310100, '上海市', 310116, '金山区', 121.33, 30.75), \
        (799, 310000, '上海', 310100, '上海市', 310117, '松江区', 121.22, 31.03), \
        (800, 310000, '上海', 310100, '上海市', 310118, '青浦区', 121.12, 31.15), \
        (801, 310000, '上海', 310100, '上海市', 310119, '南汇区', 121.75, 31.05), \
        (802, 310000, '上海', 310100, '上海市', 310120, '奉贤区', 121.47, 30.92), \
        (803, 310000, '上海', 310200, '上海市', 310230, '崇明县', 121.4, 31.62), \
        (804, 320000, '江苏省', 320100, '南京市', 320101, '市辖区', 118.78, 32.07), \
        (805, 320000, '江苏省', 320100, '南京市', 320102, '玄武区', 118.8, 32.05), \
        (806, 320000, '江苏省', 320100, '南京市', 320103, '白下区', 118.78, 32.03), \
        (807, 320000, '江苏省', 320100, '南京市', 320104, '秦淮区', 118.8, 32.02), \
        (808, 320000, '江苏省', 320100, '南京市', 320105, '建邺区', 118.75, 32.03), \
        (809, 320000, '江苏省', 320100, '南京市', 320106, '鼓楼区', 118.77, 32.07), \
        (810, 320000, '江苏省', 320100, '南京市', 320107, '下关区', 118.73, 32.08), \
        (811, 320000, '江苏省', 320100, '南京市', 320111, '浦口区', 118.62, 32.05), \
        (812, 320000, '江苏省', 320100, '南京市', 320113, '栖霞区', 118.88, 32.12), \
        (813, 320000, '江苏省', 320100, '南京市', 320114, '雨花台区', 118.77, 32), \
        (814, 320000, '江苏省', 320100, '南京市', 320115, '江宁区', 118.85, 31.95), \
        (815, 320000, '江苏省', 320100, '南京市', 320116, '六合区', 118.83, 32.35), \
        (816, 320000, '江苏省', 320100, '南京市', 320124, '溧水县', 119.02, 31.65), \
        (817, 320000, '江苏省', 320100, '南京市', 320125, '高淳县', 118.88, 31.33), \
        (818, 320000, '江苏省', 320200, '无锡市', 320201, '市辖区', 120.3, 31.57), \
        (819, 320000, '江苏省', 320200, '无锡市', 320202, '崇安区', 120.3, 31.58), \
        (820, 320000, '江苏省', 320200, '无锡市', 320203, '南长区', 120.3, 31.57), \
        (821, 320000, '江苏省', 320200, '无锡市', 320204, '北塘区', 120.28, 31.58), \
        (822, 320000, '江苏省', 320200, '无锡市', 320205, '锡山区', 120.35, 31.6), \
        (823, 320000, '江苏省', 320200, '无锡市', 320206, '惠山区', 120.28, 31.68), \
        (824, 320000, '江苏省', 320200, '无锡市', 320211, '滨湖区', 120.27, 31.57), \
        (825, 320000, '江苏省', 320200, '无锡市', 320281, '江阴市', 120.27, 31.9), \
        (826, 320000, '江苏省', 320200, '无锡市', 320282, '宜兴市', 119.82, 31.35), \
        (827, 320000, '江苏省', 320300, '徐州市', 320301, '市辖区', 117.18, 34.27), \
        (828, 320000, '江苏省', 320300, '徐州市', 320302, '鼓楼区', 118.77, 32.07), \
        (829, 320000, '江苏省', 320300, '徐州市', 320303, '云龙区', 117.22, 34.25), \
        (830, 320000, '江苏省', 320300, '徐州市', 320304, '九里区', 117.13, 34.3), \
        (831, 320000, '江苏省', 320300, '徐州市', 320305, '贾汪区', 117.45, 34.45), \
        (832, 320000, '江苏省', 320300, '徐州市', 320311, '泉山区', 117.18, 34.25), \
        (833, 320000, '江苏省', 320300, '徐州市', 320321, '丰县', 116.6, 34.7), \
        (834, 320000, '江苏省', 320300, '徐州市', 320322, '沛县', 116.93, 34.73), \
        (835, 320000, '江苏省', 320300, '徐州市', 320323, '铜山县', 117.17, 34.18), \
        (836, 320000, '江苏省', 320300, '徐州市', 320324, '睢宁县', 117.95, 33.9), \
        (837, 320000, '江苏省', 320300, '徐州市', 320381, '新沂市', 118.35, 34.38), \
        (838, 320000, '江苏省', 320300, '徐州市', 320382, '邳州市', 117.95, 34.32), \
        (839, 320000, '江苏省', 320400, '常州市', 320401, '市辖区', 119.95, 31.78), \
        (840, 320000, '江苏省', 320400, '常州市', 320402, '天宁区', 119.93, 31.75), \
        (841, 320000, '江苏省', 320400, '常州市', 320404, '钟楼区', 119.93, 31.78), \
        (842, 320000, '江苏省', 320400, '常州市', 320405, '戚墅堰区', 120.05, 31.73), \
        (843, 320000, '江苏省', 320400, '常州市', 320411, '新北区', 119.97, 31.83), \
        (844, 320000, '江苏省', 320400, '常州市', 320412, '武进区', 119.93, 31.72), \
        (845, 320000, '江苏省', 320400, '常州市', 320481, '溧阳市', 119.48, 31.42), \
        (846, 320000, '江苏省', 320400, '常州市', 320482, '金坛市', 119.57, 31.75), \
        (847, 320000, '江苏省', 320500, '苏州市', 320501, '市辖区', 120.58, 31.3), \
        (848, 320000, '江苏省', 320500, '苏州市', 320502, '沧浪区', 120.63, 31.3), \
        (849, 320000, '江苏省', 320500, '苏州市', 320503, '平江区', 120.63, 31.32), \
        (850, 320000, '江苏省', 320500, '苏州市', 320504, '金阊区', 120.6, 31.32), \
        (851, 320000, '江苏省', 320500, '苏州市', 320505, '虎丘区', 120.57, 31.3), \
        (852, 320000, '江苏省', 320500, '苏州市', 320506, '吴中区', 120.63, 31.27), \
        (853, 320000, '江苏省', 320500, '苏州市', 320507, '相城区', 120.63, 31.37), \
        (854, 320000, '江苏省', 320500, '苏州市', 320581, '常熟市', 120.75, 31.65), \
        (855, 320000, '江苏省', 320500, '苏州市', 320582, '张家港市', 120.55, 31.87), \
        (856, 320000, '江苏省', 320500, '苏州市', 320583, '昆山市', 120.98, 31.38), \
        (857, 320000, '江苏省', 320500, '苏州市', 320584, '吴江市', 120.63, 31.17), \
        (858, 320000, '江苏省', 320500, '苏州市', 320585, '太仓市', 121.1, 31.45), \
        (859, 320000, '江苏省', 320600, '南通市', 320601, '市辖区', 120.88, 31.98), \
        (860, 320000, '江苏省', 320600, '南通市', 320602, '崇川区', 120.85, 32), \
        (861, 320000, '江苏省', 320600, '南通市', 320611, '港闸区', 120.8, 32.03), \
        (862, 320000, '江苏省', 320600, '南通市', 320621, '海安县', 120.45, 32.55), \
        (863, 320000, '江苏省', 320600, '南通市', 320623, '如东县', 121.18, 32.32), \
        (864, 320000, '江苏省', 320600, '南通市', 320681, '启东市', 121.65, 31.82), \
        (865, 320000, '江苏省', 320600, '南通市', 320682, '如皋市', 120.57, 32.4), \
        (866, 320000, '江苏省', 320600, '南通市', 320683, '通州市', 121.07, 32.08), \
        (867, 320000, '江苏省', 320600, '南通市', 320684, '海门市', 121.17, 31.9), \
        (868, 320000, '江苏省', 320700, '连云港市', 320701, '市辖区', 119.22, 34.6), \
        (869, 320000, '江苏省', 320700, '连云港市', 320703, '连云区', 119.37, 34.75), \
        (870, 320000, '江苏省', 320700, '连云港市', 320705, '新浦区', 119.17, 34.6), \
        (871, 320000, '江苏省', 320700, '连云港市', 320706, '海州区', 119.12, 34.57), \
        (872, 320000, '江苏省', 320700, '连云港市', 320721, '赣榆县', 119.12, 34.83), \
        (873, 320000, '江苏省', 320700, '连云港市', 320722, '东海县', 118.77, 34.53), \
        (874, 320000, '江苏省', 320700, '连云港市', 320723, '灌云县', 119.25, 34.3), \
        (875, 320000, '江苏省', 320700, '连云港市', 320724, '灌南县', 119.35, 34.08), \
        (876, 320000, '江苏省', 320800, '淮安市', 320801, '市辖区', 119.02, 33.62), \
        (877, 320000, '江苏省', 320800, '淮安市', 320802, '清河区', 119.02, 33.6), \
        (878, 320000, '江苏省', 320800, '淮安市', 320803, '楚州区', 119.13, 33.5), \
        (879, 320000, '江苏省', 320800, '淮安市', 320804, '淮阴区', 119.03, 33.63), \
        (880, 320000, '江苏省', 320800, '淮安市', 320811, '清浦区', 119.03, 33.58), \
        (881, 320000, '江苏省', 320800, '淮安市', 320826, '涟水县', 119.27, 33.78), \
        (882, 320000, '江苏省', 320800, '淮安市', 320829, '洪泽县', 118.83, 33.3), \
        (883, 320000, '江苏省', 320800, '淮安市', 320830, '盱眙县', 118.48, 33), \
        (884, 320000, '江苏省', 320800, '淮安市', 320831, '金湖县', 119.02, 33.02), \
        (885, 320000, '江苏省', 320900, '盐城市', 320901, '市辖区', 120.15, 33.35), \
        (886, 320000, '江苏省', 320900, '盐城市', 320902, '亭湖区', 120.13, 33.4), \
        (887, 320000, '江苏省', 320900, '盐城市', 320903, '盐都区', 120.15, 33.33), \
        (888, 320000, '江苏省', 320900, '盐城市', 320921, '响水县', 119.57, 34.2), \
        (889, 320000, '江苏省', 320900, '盐城市', 320922, '滨海县', 119.83, 33.98), \
        (890, 320000, '江苏省', 320900, '盐城市', 320923, '阜宁县', 119.8, 33.78), \
        (891, 320000, '江苏省', 320900, '盐城市', 320924, '射阳县', 120.25, 33.78), \
        (892, 320000, '江苏省', 320900, '盐城市', 320925, '建湖县', 119.8, 33.47), \
        (893, 320000, '江苏省', 320900, '盐城市', 320981, '东台市', 120.3, 32.85), \
        (894, 320000, '江苏省', 320900, '盐城市', 320982, '大丰市', 120.47, 33.2), \
        (895, 320000, '江苏省', 321000, '扬州市', 321001, '市辖区', 119.4, 32.4), \
        (896, 320000, '江苏省', 321000, '扬州市', 321002, '广陵区', 119.43, 32.38), \
        (897, 320000, '江苏省', 321000, '扬州市', 321003, '邗江区', 119.4, 32.38), \
        (898, 320000, '江苏省', 321000, '扬州市', 321011, '维扬区', 119.4, 32.42), \
        (899, 320000, '江苏省', 321000, '扬州市', 321023, '宝应县', 119.3, 33.23), \
        (900, 320000, '江苏省', 321000, '扬州市', 321081, '仪征市', 119.18, 32.27), \
        (901, 320000, '江苏省', 321000, '扬州市', 321084, '高邮市', 119.43, 32.78), \
        (902, 320000, '江苏省', 321000, '扬州市', 321088, '江都市', 119.55, 32.43), \
        (903, 320000, '江苏省', 321100, '镇江市', 321101, '市辖区', 119.45, 32.2), \
        (904, 320000, '江苏省', 321100, '镇江市', 321102, '京口区', 119.47, 32.2), \
        (905, 320000, '江苏省', 321100, '镇江市', 321111, '润州区', 119.4, 32.2), \
        (906, 320000, '江苏省', 321100, '镇江市', 321112, '丹徒区', 119.45, 32.13), \
        (907, 320000, '江苏省', 321100, '镇江市', 321181, '丹阳市', 119.57, 32), \
        (908, 320000, '江苏省', 321100, '镇江市', 321182, '扬中市', 119.82, 32.23), \
        (909, 320000, '江苏省', 321100, '镇江市', 321183, '句容市', 119.17, 31.95), \
        (910, 320000, '江苏省', 321200, '泰州市', 321201, '市辖区', 119.92, 32.45), \
        (911, 320000, '江苏省', 321200, '泰州市', 321202, '海陵区', 0, 0), \
        (912, 320000, '江苏省', 321200, '泰州市', 321203, '高港区', 0, 0), \
        (913, 320000, '江苏省', 321200, '泰州市', 321281, '兴化市', 119.85, 32.92), \
        (914, 320000, '江苏省', 321200, '泰州市', 321282, '靖江市', 120.27, 32.02), \
        (915, 320000, '江苏省', 321200, '泰州市', 321283, '泰兴市', 120.02, 32.17), \
        (916, 320000, '江苏省', 321200, '泰州市', 321284, '姜堰市', 120.15, 32.52), \
        (917, 320000, '江苏省', 321300, '宿迁市', 321301, '市辖区', 118.28, 33.97), \
        (918, 320000, '江苏省', 321300, '宿迁市', 321302, '宿城区', 118.25, 33.97), \
        (919, 320000, '江苏省', 321300, '宿迁市', 321311, '宿豫区', 118.32, 33.95), \
        (920, 320000, '江苏省', 321300, '宿迁市', 321322, '沭阳县', 118.77, 34.13), \
        (921, 320000, '江苏省', 321300, '宿迁市', 321323, '泗阳县', 118.68, 33.72), \
        (922, 320000, '江苏省', 321300, '宿迁市', 321324, '泗洪县', 118.22, 33.47), \
        (923, 330000, '浙江省', 330100, '杭州市', 330101, '市辖区', 120.15, 30.28), \
        (924, 330000, '浙江省', 330100, '杭州市', 330102, '上城区', 120.17, 30.25), \
        (925, 330000, '浙江省', 330100, '杭州市', 330103, '下城区', 120.17, 30.28), \
        (926, 330000, '浙江省', 330100, '杭州市', 330104, '江干区', 120.2, 30.27), \
        (927, 330000, '浙江省', 330100, '杭州市', 330105, '拱墅区', 120.13, 30.32), \
        (928, 330000, '浙江省', 330100, '杭州市', 330106, '西湖区', 120.13, 30.27), \
        (929, 330000, '浙江省', 330100, '杭州市', 330108, '滨江区', 120.2, 30.2), \
        (930, 330000, '浙江省', 330100, '杭州市', 330109, '萧山区', 120.27, 30.17), \
        (931, 330000, '浙江省', 330100, '杭州市', 330110, '余杭区', 120.3, 30.42), \
        (932, 330000, '浙江省', 330100, '杭州市', 330122, '桐庐县', 119.67, 29.8), \
        (933, 330000, '浙江省', 330100, '杭州市', 330127, '淳安县', 119.03, 29.6), \
        (934, 330000, '浙江省', 330100, '杭州市', 330182, '建德市', 119.28, 29.48), \
        (935, 330000, '浙江省', 330100, '杭州市', 330183, '富阳市', 119.95, 30.05), \
        (936, 330000, '浙江省', 330100, '杭州市', 330185, '临安市', 119.72, 30.23), \
        (937, 330000, '浙江省', 330200, '宁波市', 330201, '市辖区', 121.55, 29.88), \
        (938, 330000, '浙江省', 330200, '宁波市', 330203, '海曙区', 121.55, 29.87), \
        (939, 330000, '浙江省', 330200, '宁波市', 330204, '江东区', 121.57, 29.87), \
        (940, 330000, '浙江省', 330200, '宁波市', 330205, '江北区', 121.55, 29.88), \
        (941, 330000, '浙江省', 330200, '宁波市', 330206, '北仑区', 121.85, 29.93), \
        (942, 330000, '浙江省', 330200, '宁波市', 330211, '镇海区', 121.72, 29.95), \
        (943, 330000, '浙江省', 330200, '宁波市', 330212, '鄞州区', 121.53, 29.83), \
        (944, 330000, '浙江省', 330200, '宁波市', 330225, '象山县', 121.87, 29.48), \
        (945, 330000, '浙江省', 330200, '宁波市', 330226, '宁海县', 121.43, 29.28), \
        (946, 330000, '浙江省', 330200, '宁波市', 330281, '余姚市', 121.15, 30.03), \
        (947, 330000, '浙江省', 330200, '宁波市', 330282, '慈溪市', 121.23, 30.17), \
        (948, 330000, '浙江省', 330200, '宁波市', 330283, '奉化市', 121.4, 29.65), \
        (949, 330000, '浙江省', 330300, '温州市', 330301, '市辖区', 120.7, 28), \
        (950, 330000, '浙江省', 330300, '温州市', 330302, '鹿城区', 120.65, 28.02), \
        (951, 330000, '浙江省', 330300, '温州市', 330303, '龙湾区', 120.82, 27.93), \
        (952, 330000, '浙江省', 330300, '温州市', 330304, '瓯海区', 0, 0), \
        (953, 330000, '浙江省', 330300, '温州市', 330322, '洞头县', 121.15, 27.83), \
        (954, 330000, '浙江省', 330300, '温州市', 330324, '永嘉县', 120.68, 28.15), \
        (955, 330000, '浙江省', 330300, '温州市', 330326, '平阳县', 120.57, 27.67), \
        (956, 330000, '浙江省', 330300, '温州市', 330327, '苍南县', 120.4, 27.5), \
        (957, 330000, '浙江省', 330300, '温州市', 330328, '文成县', 120.08, 27.78), \
        (958, 330000, '浙江省', 330300, '温州市', 330329, '泰顺县', 119.72, 27.57), \
        (959, 330000, '浙江省', 330300, '温州市', 330381, '瑞安市', 120.63, 27.78), \
        (960, 330000, '浙江省', 330300, '温州市', 330382, '乐清市', 120.95, 28.13), \
        (961, 330000, '浙江省', 330400, '嘉兴市', 330401, '市辖区', 120.75, 30.75), \
        (962, 330000, '浙江省', 330400, '嘉兴市', 330402, '秀城区', 0, 0), \
        (963, 330000, '浙江省', 330400, '嘉兴市', 330411, '秀洲区', 120.7, 30.77), \
        (964, 330000, '浙江省', 330400, '嘉兴市', 330421, '嘉善县', 120.92, 30.85), \
        (965, 330000, '浙江省', 330400, '嘉兴市', 330424, '海盐县', 120.95, 30.53), \
        (966, 330000, '浙江省', 330400, '嘉兴市', 330481, '海宁市', 120.68, 30.53), \
        (967, 330000, '浙江省', 330400, '嘉兴市', 330482, '平湖市', 121.02, 30.7), \
        (968, 330000, '浙江省', 330400, '嘉兴市', 330483, '桐乡市', 120.57, 30.63), \
        (969, 330000, '浙江省', 330500, '湖州市', 330501, '市辖区', 120.08, 30.9), \
        (970, 330000, '浙江省', 330500, '湖州市', 330502, '吴兴区', 120.12, 30.87), \
        (971, 330000, '浙江省', 330500, '湖州市', 330503, '南浔区', 120.43, 30.88), \
        (972, 330000, '浙江省', 330500, '湖州市', 330521, '德清县', 119.97, 30.53), \
        (973, 330000, '浙江省', 330500, '湖州市', 330522, '长兴县', 119.9, 31.02), \
        (974, 330000, '浙江省', 330500, '湖州市', 330523, '安吉县', 119.68, 30.63), \
        (975, 330000, '浙江省', 330600, '绍兴市', 330601, '市辖区', 120.57, 30), \
        (976, 330000, '浙江省', 330600, '绍兴市', 330602, '越城区', 120.57, 30), \
        (977, 330000, '浙江省', 330600, '绍兴市', 330621, '绍兴县', 120.47, 30.08), \
        (978, 330000, '浙江省', 330600, '绍兴市', 330624, '新昌县', 120.9, 29.5), \
        (979, 330000, '浙江省', 330600, '绍兴市', 330681, '诸暨市', 120.23, 29.72), \
        (980, 330000, '浙江省', 330600, '绍兴市', 330682, '上虞市', 120.87, 30.03), \
        (981, 330000, '浙江省', 330600, '绍兴市', 330683, '嵊州市', 120.82, 29.58), \
        (982, 330000, '浙江省', 330700, '金华市', 330701, '市辖区', 119.65, 29.08), \
        (983, 330000, '浙江省', 330700, '金华市', 330702, '婺城区', 119.65, 29.08), \
        (984, 330000, '浙江省', 330700, '金华市', 330703, '金东区', 119.7, 29.08), \
        (985, 330000, '浙江省', 330700, '金华市', 330723, '武义县', 119.82, 28.9), \
        (986, 330000, '浙江省', 330700, '金华市', 330726, '浦江县', 119.88, 29.45), \
        (987, 330000, '浙江省', 330700, '金华市', 330727, '磐安县', 120.43, 29.05), \
        (988, 330000, '浙江省', 330700, '金华市', 330781, '兰溪市', 119.45, 29.22), \
        (989, 330000, '浙江省', 330700, '金华市', 330782, '义乌市', 120.07, 29.3), \
        (990, 330000, '浙江省', 330700, '金华市', 330783, '东阳市', 120.23, 29.28), \
        (991, 330000, '浙江省', 330700, '金华市', 330784, '永康市', 120.03, 28.9), \
        (992, 330000, '浙江省', 330800, '衢州市', 330801, '市辖区', 118.87, 28.93), \
        (993, 330000, '浙江省', 330800, '衢州市', 330802, '柯城区', 118.87, 28.93), \
        (994, 330000, '浙江省', 330800, '衢州市', 330803, '衢江区', 118.93, 28.98), \
        (995, 330000, '浙江省', 330800, '衢州市', 330822, '常山县', 118.52, 28.9), \
        (996, 330000, '浙江省', 330800, '衢州市', 330824, '开化县', 118.42, 29.13), \
        (997, 330000, '浙江省', 330800, '衢州市', 330825, '龙游县', 119.17, 29.03), \
        (998, 330000, '浙江省', 330800, '衢州市', 330881, '江山市', 118.62, 28.75), \
        (999, 330000, '浙江省', 330900, '舟山市', 330901, '市辖区', 122.2, 30), \
        (1000, 330000, '浙江省', 330900, '舟山市', 330902, '定海区', 122.1, 30.02), \
        (1001, 330000, '浙江省', 330900, '舟山市', 330903, '普陀区', 122.3, 29.95), \
        (1002, 330000, '浙江省', 330900, '舟山市', 330921, '岱山县', 122.2, 30.25), \
        (1003, 330000, '浙江省', 330900, '舟山市', 330922, '嵊泗县', 122.45, 30.73), \
        (1004, 330000, '浙江省', 331000, '台州市', 331001, '市辖区', 121.43, 28.68), \
        (1005, 330000, '浙江省', 331000, '台州市', 331002, '椒江区', 121.43, 28.68), \
        (1006, 330000, '浙江省', 331000, '台州市', 331003, '黄岩区', 121.27, 28.65), \
        (1007, 330000, '浙江省', 331000, '台州市', 331004, '路桥区', 121.38, 28.58), \
        (1008, 330000, '浙江省', 331000, '台州市', 331021, '玉环县', 121.23, 28.13), \
        (1009, 330000, '浙江省', 331000, '台州市', 331022, '三门县', 121.38, 29.12), \
        (1010, 330000, '浙江省', 331000, '台州市', 331023, '天台县', 121.03, 29.13), \
        (1011, 330000, '浙江省', 331000, '台州市', 331024, '仙居县', 120.73, 28.87), \
        (1012, 330000, '浙江省', 331000, '台州市', 331081, '温岭市', 121.37, 28.37), \
        (1013, 330000, '浙江省', 331000, '台州市', 331082, '临海市', 121.12, 28.85), \
        (1014, 330000, '浙江省', 331100, '丽水市', 331101, '市辖区', 119.92, 28.45), \
        (1015, 330000, '浙江省', 331100, '丽水市', 331102, '莲都区', 119.92, 28.45), \
        (1016, 330000, '浙江省', 331100, '丽水市', 331121, '青田县', 120.28, 28.15), \
        (1017, 330000, '浙江省', 331100, '丽水市', 331122, '缙云县', 120.07, 28.65), \
        (1018, 330000, '浙江省', 331100, '丽水市', 331123, '遂昌县', 119.27, 28.6), \
        (1019, 330000, '浙江省', 331100, '丽水市', 331124, '松阳县', 119.48, 28.45), \
        (1020, 330000, '浙江省', 331100, '丽水市', 331125, '云和县', 119.57, 28.12), \
        (1021, 330000, '浙江省', 331100, '丽水市', 331126, '庆元县', 119.05, 27.62), \
        (1022, 330000, '浙江省', 331100, '丽水市', 331127, '景宁畲族自治县', 119.63, 27.98), \
        (1023, 330000, '浙江省', 331100, '丽水市', 331181, '龙泉市', 119.13, 28.08), \
        (1024, 340000, '安徽省', 340100, '合肥市', 340101, '市辖区', 117.25, 31.83), \
        (1025, 340000, '安徽省', 340100, '合肥市', 340102, '瑶海区', 117.3, 31.87), \
        (1026, 340000, '安徽省', 340100, '合肥市', 340103, '庐阳区', 117.25, 31.88), \
        (1027, 340000, '安徽省', 340100, '合肥市', 340104, '蜀山区', 117.27, 31.85), \
        (1028, 340000, '安徽省', 340100, '合肥市', 340111, '包河区', 117.3, 31.8), \
        (1029, 340000, '安徽省', 340100, '合肥市', 340121, '长丰县', 117.17, 32.48), \
        (1030, 340000, '安徽省', 340100, '合肥市', 340122, '肥东县', 117.47, 31.88), \
        (1031, 340000, '安徽省', 340100, '合肥市', 340123, '肥西县', 117.17, 31.72), \
        (1032, 340000, '安徽省', 340200, '芜湖市', 340201, '市辖区', 118.38, 31.33), \
        (1033, 340000, '安徽省', 340200, '芜湖市', 340202, '镜湖区', 118.37, 31.35), \
        (1034, 340000, '安徽省', 340200, '芜湖市', 340203, '弋江区', 0, 0), \
        (1035, 340000, '安徽省', 340200, '芜湖市', 340207, '鸠江区', 118.38, 31.37), \
        (1036, 340000, '安徽省', 340200, '芜湖市', 340208, '三山区', 0, 0), \
        (1037, 340000, '安徽省', 340200, '芜湖市', 340221, '芜湖县', 118.57, 31.15), \
        (1038, 340000, '安徽省', 340200, '芜湖市', 340222, '繁昌县', 118.2, 31.08), \
        (1039, 340000, '安徽省', 340200, '芜湖市', 340223, '南陵县', 118.33, 30.92), \
        (1040, 340000, '安徽省', 340300, '蚌埠市', 340301, '市辖区', 117.38, 32.92), \
        (1041, 340000, '安徽省', 340300, '蚌埠市', 340302, '龙子湖区', 117.38, 32.95), \
        (1042, 340000, '安徽省', 340300, '蚌埠市', 340303, '蚌山区', 117.35, 32.95), \
        (1043, 340000, '安徽省', 340300, '蚌埠市', 340304, '禹会区', 117.33, 32.93), \
        (1044, 340000, '安徽省', 340300, '蚌埠市', 340311, '淮上区', 117.35, 32.97), \
        (1045, 340000, '安徽省', 340300, '蚌埠市', 340321, '怀远县', 117.18, 32.97), \
        (1046, 340000, '安徽省', 340300, '蚌埠市', 340322, '五河县', 117.88, 33.15), \
        (1047, 340000, '安徽省', 340300, '蚌埠市', 340323, '固镇县', 117.32, 33.32), \
        (1048, 340000, '安徽省', 340400, '淮南市', 340401, '市辖区', 117, 32.63), \
        (1049, 340000, '安徽省', 340400, '淮南市', 340402, '大通区', 117.05, 32.63), \
        (1050, 340000, '安徽省', 340400, '淮南市', 340403, '田家庵区', 117, 32.67), \
        (1051, 340000, '安徽省', 340400, '淮南市', 340404, '谢家集区', 116.85, 32.6), \
        (1052, 340000, '安徽省', 340400, '淮南市', 340405, '八公山区', 116.83, 32.63), \
        (1053, 340000, '安徽省', 340400, '淮南市', 340406, '潘集区', 116.82, 32.78), \
        (1054, 340000, '安徽省', 340400, '淮南市', 340421, '凤台县', 116.72, 32.7), \
        (1055, 340000, '安徽省', 340500, '马鞍山市', 340501, '市辖区', 118.5, 31.7), \
        (1056, 340000, '安徽省', 340500, '马鞍山市', 340502, '金家庄区', 118.48, 31.73), \
        (1057, 340000, '安徽省', 340500, '马鞍山市', 340503, '花山区', 118.5, 31.72), \
        (1058, 340000, '安徽省', 340500, '马鞍山市', 340504, '雨山区', 118.48, 31.68), \
        (1059, 340000, '安徽省', 340500, '马鞍山市', 340521, '当涂县', 118.48, 31.55), \
        (1060, 340000, '安徽省', 340600, '淮北市', 340601, '市辖区', 116.8, 33.95), \
        (1061, 340000, '安徽省', 340600, '淮北市', 340602, '杜集区', 116.82, 34), \
        (1062, 340000, '安徽省', 340600, '淮北市', 340603, '相山区', 116.8, 33.95), \
        (1063, 340000, '安徽省', 340600, '淮北市', 340604, '烈山区', 116.8, 33.9), \
        (1064, 340000, '安徽省', 340600, '淮北市', 340621, '濉溪县', 116.77, 33.92), \
        (1065, 340000, '安徽省', 340700, '铜陵市', 340701, '市辖区', 117.82, 30.93), \
        (1066, 340000, '安徽省', 340700, '铜陵市', 340702, '铜官山区', 117.82, 30.93), \
        (1067, 340000, '安徽省', 340700, '铜陵市', 340703, '狮子山区', 117.85, 30.95), \
        (1068, 340000, '安徽省', 340700, '铜陵市', 340711, '郊区', 117.78, 30.92), \
        (1069, 340000, '安徽省', 340700, '铜陵市', 340721, '铜陵县', 117.78, 30.95), \
        (1070, 340000, '安徽省', 340800, '安庆市', 340801, '市辖区', 117.05, 30.53), \
        (1071, 340000, '安徽省', 340800, '安庆市', 340802, '迎江区', 117.05, 30.5), \
        (1072, 340000, '安徽省', 340800, '安庆市', 340803, '大观区', 117.03, 30.52), \
        (1073, 340000, '安徽省', 340800, '安庆市', 340811, '宜秀区', 0, 0), \
        (1074, 340000, '安徽省', 340800, '安庆市', 340822, '怀宁县', 116.83, 30.72), \
        (1075, 340000, '安徽省', 340800, '安庆市', 340823, '枞阳县', 117.2, 30.7), \
        (1076, 340000, '安徽省', 340800, '安庆市', 340824, '潜山县', 116.57, 30.63), \
        (1077, 340000, '安徽省', 340800, '安庆市', 340825, '太湖县', 116.27, 30.43), \
        (1078, 340000, '安徽省', 340800, '安庆市', 340826, '宿松县', 116.12, 30.15), \
        (1079, 340000, '安徽省', 340800, '安庆市', 340827, '望江县', 116.68, 30.13), \
        (1080, 340000, '安徽省', 340800, '安庆市', 340828, '岳西县', 116.35, 30.85), \
        (1081, 340000, '安徽省', 340800, '安庆市', 340881, '桐城市', 116.95, 31.05), \
        (1082, 340000, '安徽省', 341000, '黄山市', 341001, '市辖区', 118.33, 29.72), \
        (1083, 340000, '安徽省', 341000, '黄山市', 341002, '屯溪区', 118.33, 29.72), \
        (1084, 340000, '安徽省', 341000, '黄山市', 341003, '黄山区', 118.13, 30.3), \
        (1085, 340000, '安徽省', 341000, '黄山市', 341004, '徽州区', 118.33, 29.82), \
        (1086, 340000, '安徽省', 341000, '黄山市', 341021, '歙县', 118.43, 29.87), \
        (1087, 340000, '安徽省', 341000, '黄山市', 341022, '休宁县', 118.18, 29.78), \
        (1088, 340000, '安徽省', 341000, '黄山市', 341023, '黟县', 117.93, 29.93), \
        (1089, 340000, '安徽省', 341000, '黄山市', 341024, '祁门县', 117.72, 29.87), \
        (1090, 340000, '安徽省', 341100, '滁州市', 341101, '市辖区', 118.32, 32.3), \
        (1091, 340000, '安徽省', 341100, '滁州市', 341102, '琅琊区', 118.3, 32.3), \
        (1092, 340000, '安徽省', 341100, '滁州市', 341103, '南谯区', 118.3, 32.32), \
        (1093, 340000, '安徽省', 341100, '滁州市', 341122, '来安县', 118.43, 32.45), \
        (1094, 340000, '安徽省', 341100, '滁州市', 341124, '全椒县', 118.27, 32.1), \
        (1095, 340000, '安徽省', 341100, '滁州市', 341125, '定远县', 117.67, 32.53), \
        (1096, 340000, '安徽省', 341100, '滁州市', 341126, '凤阳县', 117.57, 32.87), \
        (1097, 340000, '安徽省', 341100, '滁州市', 341181, '天长市', 119, 32.7), \
        (1098, 340000, '安徽省', 341100, '滁州市', 341182, '明光市', 117.98, 32.78), \
        (1099, 340000, '安徽省', 341200, '阜阳市', 341201, '市辖区', 115.82, 32.9), \
        (1100, 340000, '安徽省', 341200, '阜阳市', 341202, '颍州区', 115.8, 32.88), \
        (1101, 340000, '安徽省', 341200, '阜阳市', 341203, '颍东区', 115.85, 32.92), \
        (1102, 340000, '安徽省', 341200, '阜阳市', 341204, '颍泉区', 115.8, 32.93), \
        (1103, 340000, '安徽省', 341200, '阜阳市', 341221, '临泉县', 115.25, 33.07), \
        (1104, 340000, '安徽省', 341200, '阜阳市', 341222, '太和县', 115.62, 33.17), \
        (1105, 340000, '安徽省', 341200, '阜阳市', 341225, '阜南县', 115.58, 32.63), \
        (1106, 340000, '安徽省', 341200, '阜阳市', 341226, '颍上县', 116.27, 32.63), \
        (1107, 340000, '安徽省', 341200, '阜阳市', 341282, '界首市', 0, 0), \
        (1108, 340000, '安徽省', 341300, '宿州市', 341301, '市辖区', 116.98, 33.63), \
        (1109, 340000, '安徽省', 341300, '宿州市', 341302, '埇桥区', 116.97, 33.63), \
        (1110, 340000, '安徽省', 341300, '宿州市', 341321, '砀山县', 116.35, 34.42), \
        (1111, 340000, '安徽省', 341300, '宿州市', 341322, '萧县', 116.93, 34.18), \
        (1112, 340000, '安徽省', 341300, '宿州市', 341323, '灵璧县', 117.55, 33.55), \
        (1113, 340000, '安徽省', 341300, '宿州市', 341324, '泗县', 117.88, 33.48), \
        (1114, 340000, '安徽省', 341400, '巢湖市', 341401, '市辖区', 117.87, 31.6), \
        (1115, 340000, '安徽省', 341400, '巢湖市', 341402, '居巢区', 117.85, 31.6), \
        (1116, 340000, '安徽省', 341400, '巢湖市', 341421, '庐江县', 117.28, 31.25), \
        (1117, 340000, '安徽省', 341400, '巢湖市', 341422, '无为县', 117.92, 31.3), \
        (1118, 340000, '安徽省', 341400, '巢湖市', 341423, '含山县', 118.1, 31.72), \
        (1119, 340000, '安徽省', 341400, '巢湖市', 341424, '和县', 118.37, 31.72), \
        (1120, 340000, '安徽省', 341500, '六安市', 341501, '市辖区', 116.5, 31.77), \
        (1121, 340000, '安徽省', 341500, '六安市', 341502, '金安区', 116.5, 31.77), \
        (1122, 340000, '安徽省', 341500, '六安市', 341503, '裕安区', 116.48, 31.77), \
        (1123, 340000, '安徽省', 341500, '六安市', 341521, '寿县', 116.78, 32.58), \
        (1124, 340000, '安徽省', 341500, '六安市', 341522, '霍邱县', 116.27, 32.33), \
        (1125, 340000, '安徽省', 341500, '六安市', 341523, '舒城县', 116.93, 31.47), \
        (1126, 340000, '安徽省', 341500, '六安市', 341524, '金寨县', 115.92, 31.72), \
        (1127, 340000, '安徽省', 341500, '六安市', 341525, '霍山县', 116.33, 31.4), \
        (1128, 340000, '安徽省', 341600, '亳州市', 341601, '市辖区', 115.78, 33.85), \
        (1129, 340000, '安徽省', 341600, '亳州市', 341602, '谯城区', 115.77, 33.88), \
        (1130, 340000, '安徽省', 341600, '亳州市', 341621, '涡阳县', 116.22, 33.52), \
        (1131, 340000, '安徽省', 341600, '亳州市', 341622, '蒙城县', 116.57, 33.27), \
        (1132, 340000, '安徽省', 341600, '亳州市', 341623, '利辛县', 116.2, 33.15), \
        (1133, 340000, '安徽省', 341700, '池州市', 341701, '市辖区', 117.48, 30.67), \
        (1134, 340000, '安徽省', 341700, '池州市', 341702, '贵池区', 117.48, 30.65), \
        (1135, 340000, '安徽省', 341700, '池州市', 341721, '东至县', 117.02, 30.1), \
        (1136, 340000, '安徽省', 341700, '池州市', 341722, '石台县', 117.48, 30.22), \
        (1137, 340000, '安徽省', 341700, '池州市', 341723, '青阳县', 117.85, 30.65), \
        (1138, 340000, '安徽省', 341800, '宣城市', 341801, '市辖区', 118.75, 30.95), \
        (1139, 340000, '安徽省', 341800, '宣城市', 341802, '宣州区', 118.75, 30.95), \
        (1140, 340000, '安徽省', 341800, '宣城市', 341821, '郎溪县', 119.17, 31.13), \
        (1141, 340000, '安徽省', 341800, '宣城市', 341822, '广德县', 119.42, 30.9), \
        (1142, 340000, '安徽省', 341800, '宣城市', 341823, '泾县', 118.4, 30.7), \
        (1143, 340000, '安徽省', 341800, '宣城市', 341824, '绩溪县', 118.6, 30.07), \
        (1144, 340000, '安徽省', 341800, '宣城市', 341825, '旌德县', 118.53, 30.28), \
        (1145, 340000, '安徽省', 341800, '宣城市', 341881, '宁国市', 118.98, 30.63), \
        (1146, 350000, '福建省', 350100, '福州市', 350101, '市辖区', 119.3, 26.08), \
        (1147, 350000, '福建省', 350100, '福州市', 350102, '鼓楼区', 119.3, 26.08), \
        (1148, 350000, '福建省', 350100, '福州市', 350103, '台江区', 119.3, 26.07), \
        (1149, 350000, '福建省', 350100, '福州市', 350104, '仓山区', 119.32, 26.05), \
        (1150, 350000, '福建省', 350100, '福州市', 350105, '马尾区', 119.45, 26), \
        (1151, 350000, '福建省', 350100, '福州市', 350111, '晋安区', 119.32, 26.08), \
        (1152, 350000, '福建省', 350100, '福州市', 350121, '闽侯县', 119.13, 26.15), \
        (1153, 350000, '福建省', 350100, '福州市', 350122, '连江县', 119.53, 26.2), \
        (1154, 350000, '福建省', 350100, '福州市', 350123, '罗源县', 119.55, 26.48), \
        (1155, 350000, '福建省', 350100, '福州市', 350124, '闽清县', 118.85, 26.22), \
        (1156, 350000, '福建省', 350100, '福州市', 350125, '永泰县', 118.93, 25.87), \
        (1157, 350000, '福建省', 350100, '福州市', 350128, '平潭县', 119.78, 25.52), \
        (1158, 350000, '福建省', 350100, '福州市', 350181, '福清市', 119.38, 25.72), \
        (1159, 350000, '福建省', 350100, '福州市', 350182, '长乐市', 119.52, 25.97), \
        (1160, 350000, '福建省', 350200, '厦门市', 350201, '市辖区', 118.08, 24.48), \
        (1161, 350000, '福建省', 350200, '厦门市', 350203, '思明区', 118.08, 24.45), \
        (1162, 350000, '福建省', 350200, '厦门市', 350205, '海沧区', 117.98, 24.47), \
        (1163, 350000, '福建省', 350200, '厦门市', 350206, '湖里区', 118.08, 24.52), \
        (1164, 350000, '福建省', 350200, '厦门市', 350211, '集美区', 118.1, 24.57), \
        (1165, 350000, '福建省', 350200, '厦门市', 350212, '同安区', 118.15, 24.73), \
        (1166, 350000, '福建省', 350200, '厦门市', 350213, '翔安区', 118.23, 24.62), \
        (1167, 350000, '福建省', 350300, '莆田市', 350301, '市辖区', 119, 25.43), \
        (1168, 350000, '福建省', 350300, '莆田市', 350302, '城厢区', 119, 25.43), \
        (1169, 350000, '福建省', 350300, '莆田市', 350303, '涵江区', 119.1, 25.45), \
        (1170, 350000, '福建省', 350300, '莆田市', 350304, '荔城区', 119.02, 25.43), \
        (1171, 350000, '福建省', 350300, '莆田市', 350305, '秀屿区', 119.08, 25.32), \
        (1172, 350000, '福建省', 350300, '莆田市', 350322, '仙游县', 118.68, 25.37), \
        (1173, 350000, '福建省', 350400, '三明市', 350401, '市辖区', 117.62, 26.27), \
        (1174, 350000, '福建省', 350400, '三明市', 350402, '梅列区', 117.63, 26.27), \
        (1175, 350000, '福建省', 350400, '三明市', 350403, '三元区', 117.6, 26.23), \
        (1176, 350000, '福建省', 350400, '三明市', 350421, '明溪县', 117.2, 26.37), \
        (1177, 350000, '福建省', 350400, '三明市', 350423, '清流县', 116.82, 26.18), \
        (1178, 350000, '福建省', 350400, '三明市', 350424, '宁化县', 116.65, 26.27), \
        (1179, 350000, '福建省', 350400, '三明市', 350425, '大田县', 117.85, 25.7), \
        (1180, 350000, '福建省', 350400, '三明市', 350426, '尤溪县', 118.18, 26.17), \
        (1181, 350000, '福建省', 350400, '三明市', 350427, '沙县', 117.78, 26.4), \
        (1182, 350000, '福建省', 350400, '三明市', 350428, '将乐县', 117.47, 26.73), \
        (1183, 350000, '福建省', 350400, '三明市', 350429, '泰宁县', 117.17, 26.9), \
        (1184, 350000, '福建省', 350400, '三明市', 350430, '建宁县', 116.83, 26.83), \
        (1185, 350000, '福建省', 350400, '三明市', 350481, '永安市', 117.37, 25.98), \
        (1186, 350000, '福建省', 350500, '泉州市', 350501, '市辖区', 118.67, 24.88), \
        (1187, 350000, '福建省', 350500, '泉州市', 350502, '鲤城区', 118.6, 24.92), \
        (1188, 350000, '福建省', 350500, '泉州市', 350503, '丰泽区', 118.6, 24.92),
        (1189, 350000, '福建省', 350500, '泉州市', 350504, '洛江区', 118.67, 24.95), \
        (1190, 350000, '福建省', 350500, '泉州市', 350505, '泉港区', 118.88, 25.12), \
        (1191, 350000, '福建省', 350500, '泉州市', 350521, '惠安县', 118.8, 25.03), \
        (1192, 350000, '福建省', 350500, '泉州市', 350524, '安溪县', 118.18, 25.07), \
        (1193, 350000, '福建省', 350500, '泉州市', 350525, '永春县', 118.3, 25.32), \
        (1194, 350000, '福建省', 350500, '泉州市', 350526, '德化县', 118.23, 25.5), \
        (1195, 350000, '福建省', 350500, '泉州市', 350527, '金门县', 118.32, 24.43), \
        (1196, 350000, '福建省', 350500, '泉州市', 350581, '石狮市', 118.65, 24.73), \
        (1197, 350000, '福建省', 350500, '泉州市', 350582, '晋江市', 118.58, 24.82), \
        (1198, 350000, '福建省', 350500, '泉州市', 350583, '南安市', 118.38, 24.97), \
        (1199, 350000, '福建省', 350600, '漳州市', 350601, '市辖区', 117.65, 24.52), \
        (1200, 350000, '福建省', 350600, '漳州市', 350602, '芗城区', 117.65, 24.52), \
        (1201, 350000, '福建省', 350600, '漳州市', 350603, '龙文区', 117.72, 24.52), \
        (1202, 350000, '福建省', 350600, '漳州市', 350622, '云霄县', 117.33, 23.95), \
        (1203, 350000, '福建省', 350600, '漳州市', 350623, '漳浦县', 117.62, 24.13), \
        (1204, 350000, '福建省', 350600, '漳州市', 350624, '诏安县', 117.18, 23.72), \
        (1205, 350000, '福建省', 350600, '漳州市', 350625, '长泰县', 117.75, 24.62), \
        (1206, 350000, '福建省', 350600, '漳州市', 350626, '东山县', 117.43, 23.7), \
        (1207, 350000, '福建省', 350600, '漳州市', 350627, '南靖县', 117.37, 24.52), \
        (1208, 350000, '福建省', 350600, '漳州市', 350628, '平和县', 117.3, 24.37), \
        (1209, 350000, '福建省', 350600, '漳州市', 350629, '华安县', 117.53, 25.02), \
        (1210, 350000, '福建省', 350600, '漳州市', 350681, '龙海市', 117.82, 24.45), \
        (1211, 350000, '福建省', 350700, '南平市', 350701, '市辖区', 118.17, 26.65), \
        (1212, 350000, '福建省', 350700, '南平市', 350702, '延平区', 118.17, 26.65), \
        (1213, 350000, '福建省', 350700, '南平市', 350721, '顺昌县', 117.8, 26.8), \
        (1214, 350000, '福建省', 350700, '南平市', 350722, '浦城县', 118.53, 27.92), \
        (1215, 350000, '福建省', 350700, '南平市', 350723, '光泽县', 117.33, 27.55), \
        (1216, 350000, '福建省', 350700, '南平市', 350724, '松溪县', 118.78, 27.53), \
        (1217, 350000, '福建省', 350700, '南平市', 350725, '政和县', 118.85, 27.37), \
        (1218, 350000, '福建省', 350700, '南平市', 350781, '邵武市', 117.48, 27.37), \
        (1219, 350000, '福建省', 350700, '南平市', 350782, '武夷山市', 118.03, 27.77), \
        (1220, 350000, '福建省', 350700, '南平市', 350783, '建瓯市', 118.32, 27.03), \
        (1221, 350000, '福建省', 350700, '南平市', 350784, '建阳市', 118.12, 27.33), \
        (1222, 350000, '福建省', 350800, '龙岩市', 350801, '市辖区', 117.03, 25.1), \
        (1223, 350000, '福建省', 350800, '龙岩市', 350802, '新罗区', 117.03, 25.1), \
        (1224, 350000, '福建省', 350800, '龙岩市', 350821, '长汀县', 116.35, 25.83), \
        (1225, 350000, '福建省', 350800, '龙岩市', 350822, '永定县', 116.73, 24.72), \
        (1226, 350000, '福建省', 350800, '龙岩市', 350823, '上杭县', 116.42, 25.05), \
        (1227, 350000, '福建省', 350800, '龙岩市', 350824, '武平县', 116.1, 25.1), \
        (1228, 350000, '福建省', 350800, '龙岩市', 350825, '连城县', 116.75, 25.72), \
        (1229, 350000, '福建省', 350800, '龙岩市', 350881, '漳平市', 117.42, 25.3), \
        (1230, 350000, '福建省', 350900, '宁德市', 350901, '市辖区', 119.52, 26.67), \
        (1231, 350000, '福建省', 350900, '宁德市', 350902, '蕉城区', 119.52, 26.67), \
        (1232, 350000, '福建省', 350900, '宁德市', 350921, '霞浦县', 120, 26.88), \
        (1233, 350000, '福建省', 350900, '宁德市', 350922, '古田县', 118.75, 26.58), \
        (1234, 350000, '福建省', 350900, '宁德市', 350923, '屏南县', 118.98, 26.92), \
        (1235, 350000, '福建省', 350900, '宁德市', 350924, '寿宁县', 119.5, 27.47), \
        (1236, 350000, '福建省', 350900, '宁德市', 350925, '周宁县', 119.33, 27.12), \
        (1237, 350000, '福建省', 350900, '宁德市', 350926, '柘荣县', 119.9, 27.23), \
        (1238, 350000, '福建省', 350900, '宁德市', 350981, '福安市', 119.65, 27.08), \
        (1239, 350000, '福建省', 350900, '宁德市', 350982, '福鼎市', 120.22, 27.33), \
        (1240, 360000, '江西省', 360100, '南昌市', 360101, '市辖区', 115.85, 28.68), \
        (1241, 360000, '江西省', 360100, '南昌市', 360102, '东湖区', 115.9, 28.68), \
        (1242, 360000, '江西省', 360100, '南昌市', 360103, '西湖区', 115.87, 28.67), \
        (1243, 360000, '江西省', 360100, '南昌市', 360104, '青云谱区', 115.92, 28.63), \
        (1244, 360000, '江西省', 360100, '南昌市', 360105, '湾里区', 115.73, 28.72), \
        (1245, 360000, '江西省', 360100, '南昌市', 360111, '青山湖区', 115.95, 28.68), \
        (1246, 360000, '江西省', 360100, '南昌市', 360121, '南昌县', 115.93, 28.55), \
        (1247, 360000, '江西省', 360100, '南昌市', 360122, '新建县', 115.82, 28.7), \
        (1248, 360000, '江西省', 360100, '南昌市', 360123, '安义县', 115.55, 28.85), \
        (1249, 360000, '江西省', 360100, '南昌市', 360124, '进贤县', 116.27, 28.37), \
        (1250, 360000, '江西省', 360200, '景德镇市', 360201, '市辖区', 117.17, 29.27), \
        (1251, 360000, '江西省', 360200, '景德镇市', 360202, '昌江区', 117.17, 29.27), \
        (1252, 360000, '江西省', 360200, '景德镇市', 360203, '珠山区', 117.2, 29.3), \
        (1253, 360000, '江西省', 360200, '景德镇市', 360222, '浮梁县', 117.25, 29.37), \
        (1254, 360000, '江西省', 360200, '景德镇市', 360281, '乐平市', 117.12, 28.97), \
        (1255, 360000, '江西省', 360300, '萍乡市', 360301, '市辖区', 113.85, 27.63), \
        (1256, 360000, '江西省', 360300, '萍乡市', 360302, '安源区', 113.87, 27.65), \
        (1257, 360000, '江西省', 360300, '萍乡市', 360313, '湘东区', 113.73, 27.65), \
        (1258, 360000, '江西省', 360300, '萍乡市', 360321, '莲花县', 113.95, 27.13), \
        (1259, 360000, '江西省', 360300, '萍乡市', 360322, '上栗县', 113.8, 27.88), \
        (1260, 360000, '江西省', 360300, '萍乡市', 360323, '芦溪县', 114.03, 27.63), \
        (1261, 360000, '江西省', 360400, '九江市', 360401, '市辖区', 116, 29.7), \
        (1262, 360000, '江西省', 360400, '九江市', 360402, '庐山区', 115.98, 29.68), \
        (1263, 360000, '江西省', 360400, '九江市', 360403, '浔阳区', 115.98, 29.73), \
        (1264, 360000, '江西省', 360400, '九江市', 360421, '九江县', 115.88, 29.62), \
        (1265, 360000, '江西省', 360400, '九江市', 360423, '武宁县', 115.1, 29.27), \
        (1266, 360000, '江西省', 360400, '九江市', 360424, '修水县', 114.57, 29.03), \
        (1267, 360000, '江西省', 360400, '九江市', 360425, '永修县', 115.8, 29.03), \
        (1268, 360000, '江西省', 360400, '九江市', 360426, '德安县', 115.77, 29.33), \
        (1269, 360000, '江西省', 360400, '九江市', 360427, '星子县', 116.03, 29.45), \
        (1270, 360000, '江西省', 360400, '九江市', 360428, '都昌县', 116.18, 29.27), \
        (1271, 360000, '江西省', 360400, '九江市', 360429, '湖口县', 116.22, 29.73), \
        (1272, 360000, '江西省', 360400, '九江市', 360430, '彭泽县', 116.55, 29.9), \
        (1273, 360000, '江西省', 360400, '九江市', 360481, '瑞昌市', 115.67, 29.68), \
        (1274, 360000, '江西省', 360500, '新余市', 360501, '市辖区', 114.92, 27.82), \
        (1275, 360000, '江西省', 360500, '新余市', 360502, '渝水区', 114.93, 27.8), \
        (1276, 360000, '江西省', 360500, '新余市', 360521, '分宜县', 114.67, 27.82), \
        (1277, 360000, '江西省', 360600, '鹰潭市', 360601, '市辖区', 117.07, 28.27), \
        (1278, 360000, '江西省', 360600, '鹰潭市', 360602, '月湖区', 117.05, 28.23), \
        (1279, 360000, '江西省', 360600, '鹰潭市', 360622, '余江县', 116.82, 28.2), \
        (1280, 360000, '江西省', 360600, '鹰潭市', 360681, '贵溪市', 117.22, 28.28), \
        (1281, 360000, '江西省', 360700, '赣州市', 360701, '市辖区', 114.93, 25.83), \
        (1282, 360000, '江西省', 360700, '赣州市', 360702, '章贡区', 114.93, 25.87), \
        (1283, 360000, '江西省', 360700, '赣州市', 360721, '赣县', 115, 25.87), \
        (1284, 360000, '江西省', 360700, '赣州市', 360722, '信丰县', 114.93, 25.38), \
        (1285, 360000, '江西省', 360700, '赣州市', 360723, '大余县', 114.35, 25.4), \
        (1286, 360000, '江西省', 360700, '赣州市', 360724, '上犹县', 114.53, 25.8), \
        (1287, 360000, '江西省', 360700, '赣州市', 360725, '崇义县', 114.3, 25.7), \
        (1288, 360000, '江西省', 360700, '赣州市', 360726, '安远县', 115.38, 25.13), \
        (1289, 360000, '江西省', 360700, '赣州市', 360727, '龙南县', 114.78, 24.92), \
        (1290, 360000, '江西省', 360700, '赣州市', 360728, '定南县', 115.03, 24.78), \
        (1291, 360000, '江西省', 360700, '赣州市', 360729, '全南县', 114.52, 24.75), \
        (1292, 360000, '江西省', 360700, '赣州市', 360730, '宁都县', 116.02, 26.48), \
        (1293, 360000, '江西省', 360700, '赣州市', 360731, '于都县', 115.42, 25.95), \
        (1294, 360000, '江西省', 360700, '赣州市', 360732, '兴国县', 115.35, 26.33), \
        (1295, 360000, '江西省', 360700, '赣州市', 360733, '会昌县', 115.78, 25.6), \
        (1296, 360000, '江西省', 360700, '赣州市', 360734, '寻乌县', 115.65, 24.95), \
        (1297, 360000, '江西省', 360700, '赣州市', 360735, '石城县', 116.33, 26.33), \
        (1298, 360000, '江西省', 360700, '赣州市', 360781, '瑞金市', 116.03, 25.88), \
        (1299, 360000, '江西省', 360700, '赣州市', 360782, '南康市', 114.75, 25.65), \
        (1300, 360000, '江西省', 360800, '吉安市', 360801, '市辖区', 114.98, 27.12), \
        (1301, 360000, '江西省', 360800, '吉安市', 360802, '吉州区', 114.98, 27.12), \
        (1302, 360000, '江西省', 360800, '吉安市', 360803, '青原区', 115, 27.1), \
        (1303, 360000, '江西省', 360800, '吉安市', 360821, '吉安县', 114.9, 27.05), \
        (1304, 360000, '江西省', 360800, '吉安市', 360822, '吉水县', 115.13, 27.22), \
        (1305, 360000, '江西省', 360800, '吉安市', 360823, '峡江县', 115.33, 27.62), \
        (1306, 360000, '江西省', 360800, '吉安市', 360824, '新干县', 115.4, 27.77), \
        (1307, 360000, '江西省', 360800, '吉安市', 360825, '永丰县', 115.43, 27.32), \
        (1308, 360000, '江西省', 360800, '吉安市', 360826, '泰和县', 114.88, 26.8), \
        (1309, 360000, '江西省', 360800, '吉安市', 360827, '遂川县', 114.52, 26.33), \
        (1310, 360000, '江西省', 360800, '吉安市', 360828, '万安县', 114.78, 26.47), \
        (1311, 360000, '江西省', 360800, '吉安市', 360829, '安福县', 0, 0), \
        (1312, 360000, '江西省', 360800, '吉安市', 360830, '永新县', 114.23, 26.95), \
        (1313, 360000, '江西省', 360800, '吉安市', 360881, '井冈山市', 114.27, 26.72), \
        (1314, 360000, '江西省', 360900, '宜春市', 360901, '市辖区', 114.38, 27.8), \
        (1315, 360000, '江西省', 360900, '宜春市', 360902, '袁州区', 114.38, 27.8), \
        (1316, 360000, '江西省', 360900, '宜春市', 360921, '奉新县', 115.38, 28.7), \
        (1317, 360000, '江西省', 360900, '宜春市', 360922, '万载县', 114.43, 28.12), \
        (1318, 360000, '江西省', 360900, '宜春市', 360923, '上高县', 114.92, 28.23), \
        (1319, 360000, '江西省', 360900, '宜春市', 360924, '宜丰县', 114.78, 28.38), \
        (1320, 360000, '江西省', 360900, '宜春市', 360925, '靖安县', 115.35, 28.87), \
        (1321, 360000, '江西省', 360900, '宜春市', 360926, '铜鼓县', 114.37, 28.53), \
        (1322, 360000, '江西省', 360900, '宜春市', 360981, '丰城市', 115.78, 28.2), \
        (1323, 360000, '江西省', 360900, '宜春市', 360982, '樟树市', 115.53, 28.07), \
        (1324, 360000, '江西省', 360900, '宜春市', 360983, '高安市', 115.37, 28.42), \
        (1325, 360000, '江西省', 361000, '抚州市', 361001, '市辖区', 116.35, 28), \
        (1326, 360000, '江西省', 361000, '抚州市', 361002, '临川区', 116.35, 27.98), \
        (1327, 360000, '江西省', 361000, '抚州市', 361021, '南城县', 116.63, 27.55), \
        (1328, 360000, '江西省', 361000, '抚州市', 361022, '黎川县', 116.92, 27.3), \
        (1329, 360000, '江西省', 361000, '抚州市', 361023, '南丰县', 116.53, 27.22), \
        (1330, 360000, '江西省', 361000, '抚州市', 361024, '崇仁县', 116.05, 27.77), \
        (1331, 360000, '江西省', 361000, '抚州市', 361025, '乐安县', 115.83, 27.43), \
        (1332, 360000, '江西省', 361000, '抚州市', 361026, '宜黄县', 116.22, 27.55), \
        (1333, 360000, '江西省', 361000, '抚州市', 361027, '金溪县', 116.77, 27.92), \
        (1334, 360000, '江西省', 361000, '抚州市', 361028, '资溪县', 117.07, 27.7), \
        (1335, 360000, '江西省', 361000, '抚州市', 361029, '东乡县', 116.62, 28.23), \
        (1336, 360000, '江西省', 361000, '抚州市', 361030, '广昌县', 116.32, 26.83), \
        (1337, 360000, '江西省', 361100, '上饶市', 361101, '市辖区', 117.97, 28.45), \
        (1338, 360000, '江西省', 361100, '上饶市', 361102, '信州区', 117.95, 28.43), \
        (1339, 360000, '江西省', 361100, '上饶市', 361121, '上饶县', 117.92, 28.43), \
        (1340, 360000, '江西省', 361100, '上饶市', 361122, '广丰县', 118.18, 28.43), \
        (1341, 360000, '江西省', 361100, '上饶市', 361123, '玉山县', 118.25, 28.68), \
        (1342, 360000, '江西省', 361100, '上饶市', 361124, '铅山县', 117.7, 28.32), \
        (1343, 360000, '江西省', 361100, '上饶市', 361125, '横峰县', 117.6, 28.42), \
        (1344, 360000, '江西省', 361100, '上饶市', 361126, '弋阳县', 117.43, 28.4), \
        (1345, 360000, '江西省', 361100, '上饶市', 361127, '余干县', 116.68, 28.7), \
        (1346, 360000, '江西省', 361100, '上饶市', 361128, '鄱阳县', 116.67, 29), \
        (1347, 360000, '江西省', 361100, '上饶市', 361129, '万年县', 117.07, 28.7), \
        (1348, 360000, '江西省', 361100, '上饶市', 361130, '婺源县', 117.85, 29.25), \
        (1349, 360000, '江西省', 361100, '上饶市', 361181, '德兴市', 117.57, 28.95), \
        (1350, 370000, '山东省', 370100, '济南市', 370101, '市辖区', 116.98, 36.67), \
        (1351, 370000, '山东省', 370100, '济南市', 370102, '历下区', 117.08, 36.67), \
        (1352, 370000, '山东省', 370100, '济南市', 370103, '市中区', 117.57, 34.87), \
        (1353, 370000, '山东省', 370100, '济南市', 370104, '槐荫区', 116.93, 36.65), \
        (1354, 370000, '山东省', 370100, '济南市', 370105, '天桥区', 116.98, 36.68), \
        (1355, 370000, '山东省', 370100, '济南市', 370112, '历城区', 117.07, 36.68), \
        (1356, 370000, '山东省', 370100, '济南市', 370113, '长清区', 116.73, 36.55), \
        (1357, 370000, '山东省', 370100, '济南市', 370124, '平阴县', 116.45, 36.28), \
        (1358, 370000, '山东省', 370100, '济南市', 370125, '济阳县', 117.22, 36.98), \
        (1359, 370000, '山东省', 370100, '济南市', 370126, '商河县', 117.15, 37.32), \
        (1360, 370000, '山东省', 370100, '济南市', 370181, '章丘市', 117.53, 36.72), \
        (1361, 370000, '山东省', 370200, '青岛市', 370201, '市辖区', 120.38, 36.07), \
        (1362, 370000, '山东省', 370200, '青岛市', 370202, '市南区', 120.38, 36.07), \
        (1363, 370000, '山东省', 370200, '青岛市', 370203, '市北区', 120.38, 36.08), \
        (1364, 370000, '山东省', 370200, '青岛市', 370205, '四方区', 120.35, 36.1), \
        (1365, 370000, '山东省', 370200, '青岛市', 370211, '黄岛区', 120.18, 35.97), \
        (1366, 370000, '山东省', 370200, '青岛市', 370212, '崂山区', 120.47, 36.1), \
        (1367, 370000, '山东省', 370200, '青岛市', 370213, '李沧区', 120.43, 36.15), \
        (1368, 370000, '山东省', 370200, '青岛市', 370214, '城阳区', 120.37, 36.3), \
        (1369, 370000, '山东省', 370200, '青岛市', 370281, '胶州市', 120.03, 36.27), \
        (1370, 370000, '山东省', 370200, '青岛市', 370282, '即墨市', 120.45, 36.38), \
        (1371, 370000, '山东省', 370200, '青岛市', 370283, '平度市', 119.95, 36.78), \
        (1372, 370000, '山东省', 370200, '青岛市', 370284, '胶南市', 120.03, 35.87), \
        (1373, 370000, '山东省', 370200, '青岛市', 370285, '莱西市', 120.5, 36.87), \
        (1374, 370000, '山东省', 370300, '淄博市', 370301, '市辖区', 118.05, 36.82), \
        (1375, 370000, '山东省', 370300, '淄博市', 370302, '淄川区', 0, 0), \
        (1376, 370000, '山东省', 370300, '淄博市', 370303, '张店区', 118.03, 36.82), \
        (1377, 370000, '山东省', 370300, '淄博市', 370304, '博山区', 117.85, 36.5), \
        (1378, 370000, '山东省', 370300, '淄博市', 370305, '临淄区', 118.3, 36.82), \
        (1379, 370000, '山东省', 370300, '淄博市', 370306, '周村区', 117.87, 36.8), \
        (1380, 370000, '山东省', 370300, '淄博市', 370321, '桓台县', 118.08, 36.97), \
        (1381, 370000, '山东省', 370300, '淄博市', 370322, '高青县', 117.82, 37.17), \
        (1382, 370000, '山东省', 370300, '淄博市', 370323, '沂源县', 118.17, 36.18), \
        (1383, 370000, '山东省', 370400, '枣庄市', 370401, '市辖区', 117.32, 34.82), \
        (1384, 370000, '山东省', 370400, '枣庄市', 370402, '市中区', 117.57, 34.87), \
        (1385, 370000, '山东省', 370400, '枣庄市', 370403, '薛城区', 117.25, 34.8), \
        (1386, 370000, '山东省', 370400, '枣庄市', 370404, '峄城区', 117.58, 34.77), \
        (1387, 370000, '山东省', 370400, '枣庄市', 370405, '台儿庄区', 117.73, 34.57), \
        (1388, 370000, '山东省', 370400, '枣庄市', 370406, '山亭区', 117.45, 35.08), \
        (1389, 370000, '山东省', 370400, '枣庄市', 370481, '滕州市', 117.15, 35.08), \
        (1390, 370000, '山东省', 370500, '东营市', 370501, '市辖区', 118.67, 37.43), \
        (1391, 370000, '山东省', 370500, '东营市', 370502, '东营区', 118.5, 37.47), \
        (1392, 370000, '山东省', 370500, '东营市', 370503, '河口区', 118.53, 37.88), \
        (1393, 370000, '山东省', 370500, '东营市', 370521, '垦利县', 118.55, 37.58), \
        (1394, 370000, '山东省', 370500, '东营市', 370522, '利津县', 118.25, 37.48), \
        (1395, 370000, '山东省', 370500, '东营市', 370523, '广饶县', 118.4, 37.07), \
        (1396, 370000, '山东省', 370600, '烟台市', 370601, '市辖区', 121.43, 37.45), \
        (1397, 370000, '山东省', 370600, '烟台市', 370602, '芝罘区', 121.38, 37.53), \
        (1398, 370000, '山东省', 370600, '烟台市', 370611, '福山区', 121.25, 37.5), \
        (1399, 370000, '山东省', 370600, '烟台市', 370612, '牟平区', 121.6, 37.38), \
        (1400, 370000, '山东省', 370600, '烟台市', 370613, '莱山区', 121.43, 37.5), \
        (1401, 370000, '山东省', 370600, '烟台市', 370634, '长岛县', 120.73, 37.92), \
        (1402, 370000, '山东省', 370600, '烟台市', 370681, '龙口市', 120.52, 37.65), \
        (1403, 370000, '山东省', 370600, '烟台市', 370682, '莱阳市', 120.7, 36.98), \
        (1404, 370000, '山东省', 370600, '烟台市', 370683, '莱州市', 119.93, 37.18), \
        (1405, 370000, '山东省', 370600, '烟台市', 370684, '蓬莱市', 120.75, 37.82), \
        (1406, 370000, '山东省', 370600, '烟台市', 370685, '招远市', 120.4, 37.37), \
        (1407, 370000, '山东省', 370600, '烟台市', 370686, '栖霞市', 120.83, 37.3), \
        (1408, 370000, '山东省', 370600, '烟台市', 370687, '海阳市', 121.15, 36.78), \
        (1409, 370000, '山东省', 370700, '潍坊市', 370701, '市辖区', 119.15, 36.7), \
        (1410, 370000, '山东省', 370700, '潍坊市', 370702, '潍城区', 119.1, 36.72), \
        (1411, 370000, '山东省', 370700, '潍坊市', 370703, '寒亭区', 119.22, 36.77), \
        (1412, 370000, '山东省', 370700, '潍坊市', 370704, '坊子区', 119.17, 36.67), \
        (1413, 370000, '山东省', 370700, '潍坊市', 370705, '奎文区', 119.12, 36.72), \
        (1414, 370000, '山东省', 370700, '潍坊市', 370724, '临朐县', 118.53, 36.52), \
        (1415, 370000, '山东省', 370700, '潍坊市', 370725, '昌乐县', 118.82, 36.7), \
        (1416, 370000, '山东省', 370700, '潍坊市', 370781, '青州市', 118.47, 36.68), \
        (1417, 370000, '山东省', 370700, '潍坊市', 370782, '诸城市', 119.4, 36), \
        (1418, 370000, '山东省', 370700, '潍坊市', 370783, '寿光市', 118.73, 36.88), \
        (1419, 370000, '山东省', 370700, '潍坊市', 370784, '安丘市', 119.2, 36.43), \
        (1420, 370000, '山东省', 370700, '潍坊市', 370785, '高密市', 119.75, 36.38), \
        (1421, 370000, '山东省', 370700, '潍坊市', 370786, '昌邑市', 119.4, 36.87), \
        (1422, 370000, '山东省', 370800, '济宁市', 370801, '市辖区', 116.58, 35.42), \
        (1423, 370000, '山东省', 370800, '济宁市', 370802, '市中区', 117.57, 34.87), \
        (1424, 370000, '山东省', 370800, '济宁市', 370811, '任城区', 116.58, 35.42), \
        (1425, 370000, '山东省', 370800, '济宁市', 370826, '微山县', 117.13, 34.82), \
        (1426, 370000, '山东省', 370800, '济宁市', 370827, '鱼台县', 116.65, 35), \
        (1427, 370000, '山东省', 370800, '济宁市', 370828, '金乡县', 116.3, 35.07), \
        (1428, 370000, '山东省', 370800, '济宁市', 370829, '嘉祥县', 116.33, 35.42), \
        (1429, 370000, '山东省', 370800, '济宁市', 370830, '汶上县', 116.48, 35.73), \
        (1430, 370000, '山东省', 370800, '济宁市', 370831, '泗水县', 117.27, 35.67), \
        (1431, 370000, '山东省', 370800, '济宁市', 370832, '梁山县', 116.08, 35.8), \
        (1432, 370000, '山东省', 370800, '济宁市', 370881, '曲阜市', 116.98, 35.58), \
        (1433, 370000, '山东省', 370800, '济宁市', 370882, '兖州市', 116.83, 35.55), \
        (1434, 370000, '山东省', 370800, '济宁市', 370883, '邹城市', 116.97, 35.4), \
        (1435, 370000, '山东省', 370900, '泰安市', 370901, '市辖区', 117.08, 36.2), \
        (1436, 370000, '山东省', 370900, '泰安市', 370902, '泰山区', 117.13, 36.18), \
        (1437, 370000, '山东省', 370900, '泰安市', 370903, '岱岳区', 117, 36.18), \
        (1438, 370000, '山东省', 370900, '泰安市', 370921, '宁阳县', 116.8, 35.77), \
        (1439, 370000, '山东省', 370900, '泰安市', 370923, '东平县', 116.47, 35.93), \
        (1440, 370000, '山东省', 370900, '泰安市', 370982, '新泰市', 117.77, 35.92), \
        (1441, 370000, '山东省', 370900, '泰安市', 370983, '肥城市', 116.77, 36.18), \
        (1442, 370000, '山东省', 371000, '威海市', 371001, '市辖区', 122.12, 37.52), \
        (1443, 370000, '山东省', 371000, '威海市', 371002, '环翠区', 122.12, 37.5), \
        (1444, 370000, '山东省', 371000, '威海市', 371081, '文登市', 122.05, 37.2), \
        (1445, 370000, '山东省', 371000, '威海市', 371082, '荣成市', 122.42, 37.17), \
        (1446, 370000, '山东省', 371000, '威海市', 371083, '乳山市', 121.53, 36.92), \
        (1447, 370000, '山东省', 371100, '日照市', 371101, '市辖区', 119.52, 35.42), \
        (1448, 370000, '山东省', 371100, '日照市', 371102, '东港区', 119.45, 35.42), \
        (1449, 370000, '山东省', 371100, '日照市', 371103, '岚山区', 119.33, 35.1), \
        (1450, 370000, '山东省', 371100, '日照市', 371121, '五莲县', 119.2, 35.75), \
        (1451, 370000, '山东省', 371100, '日照市', 371122, '莒县', 118.83, 35.58), \
        (1452, 370000, '山东省', 371200, '莱芜市', 371201, '市辖区', 117.67, 36.22), \
        (1453, 370000, '山东省', 371200, '莱芜市', 371202, '莱城区', 117.65, 36.2), \
        (1454, 370000, '山东省', 371200, '莱芜市', 371203, '钢城区', 117.8, 36.07), \
        (1455, 370000, '山东省', 371300, '临沂市', 371301, '市辖区', 118.35, 35.05), \
        (1456, 370000, '山东省', 371300, '临沂市', 371302, '兰山区', 118.33, 35.07), \
        (1457, 370000, '山东省', 371300, '临沂市', 371311, '罗庄区', 118.28, 34.98), \
        (1458, 370000, '山东省', 371300, '临沂市', 371312, '河东区', 118.4, 35.08), \
        (1459, 370000, '山东省', 371300, '临沂市', 371321, '沂南县', 118.47, 35.55), \
        (1460, 370000, '山东省', 371300, '临沂市', 371322, '郯城县', 118.35, 34.62), \
        (1461, 370000, '山东省', 371300, '临沂市', 371323, '沂水县', 118.62, 35.78), \
        (1462, 370000, '山东省', 371300, '临沂市', 371324, '苍山县', 118.05, 34.85), \
        (1463, 370000, '山东省', 371300, '临沂市', 371325, '费县', 117.97, 35.27), \
        (1464, 370000, '山东省', 371300, '临沂市', 371326, '平邑县', 117.63, 35.5), \
        (1465, 370000, '山东省', 371300, '临沂市', 371327, '莒南县', 118.83, 35.18), \
        (1466, 370000, '山东省', 371300, '临沂市', 371328, '蒙阴县', 117.93, 35.72), \
        (1467, 370000, '山东省', 371300, '临沂市', 371329, '临沭县', 118.65, 34.92), \
        (1468, 370000, '山东省', 371400, '德州市', 371401, '市辖区', 116.3, 37.45), \
        (1469, 370000, '山东省', 371400, '德州市', 371402, '德城区', 116.3, 37.45), \
        (1470, 370000, '山东省', 371400, '德州市', 371421, '陵县', 116.57, 37.33), \
        (1471, 370000, '山东省', 371400, '德州市', 371422, '宁津县', 116.78, 37.65), \
        (1472, 370000, '山东省', 371400, '德州市', 371423, '庆云县', 117.38, 37.78), \
        (1473, 370000, '山东省', 371400, '德州市', 371424, '临邑县', 116.87, 37.18), \
        (1474, 370000, '山东省', 371400, '德州市', 371425, '齐河县', 116.75, 36.8), \
        (1475, 370000, '山东省', 371400, '德州市', 371426, '平原县', 116.43, 37.17), \
        (1476, 370000, '山东省', 371400, '德州市', 371427, '夏津县', 116, 36.95), \
        (1477, 370000, '山东省', 371400, '德州市', 371428, '武城县', 116.07, 37.22), \
        (1478, 370000, '山东省', 371400, '德州市', 371481, '乐陵市', 117.23, 37.73), \
        (1479, 370000, '山东省', 371400, '德州市', 371482, '禹城市', 116.63, 36.93), \
        (1480, 370000, '山东省', 371500, '聊城市', 371501, '市辖区', 115.98, 36.45), \
        (1481, 370000, '山东省', 371500, '聊城市', 371502, '东昌府区', 115.98, 36.45), \
        (1482, 370000, '山东省', 371500, '聊城市', 371521, '阳谷县', 115.78, 36.12), \
        (1483, 370000, '山东省', 371500, '聊城市', 371522, '莘县', 115.67, 36.23), \
        (1484, 370000, '山东省', 371500, '聊城市', 371523, '茌平县', 116.25, 36.58), \
        (1485, 370000, '山东省', 371500, '聊城市', 371524, '东阿县', 116.25, 36.33), \
        (1486, 370000, '山东省', 371500, '聊城市', 371525, '冠县', 115.43, 36.48), \
        (1487, 370000, '山东省', 371500, '聊城市', 371526, '高唐县', 116.23, 36.87), \
        (1488, 370000, '山东省', 371500, '聊城市', 371581, '临清市', 115.7, 36.85), \
        (1489, 370000, '山东省', 371600, '滨州市', 371601, '市辖区', 117.97, 37.38), \
        (1490, 370000, '山东省', 371600, '滨州市', 371602, '滨城区', 118, 37.38), \
        (1491, 370000, '山东省', 371600, '滨州市', 371621, '惠民县', 117.5, 37.48), \
        (1492, 370000, '山东省', 371600, '滨州市', 371622, '阳信县', 117.58, 37.63), \
        (1493, 370000, '山东省', 371600, '滨州市', 371623, '无棣县', 117.6, 37.73), \
        (1494, 370000, '山东省', 371600, '滨州市', 371624, '沾化县', 118.13, 37.7), \
        (1495, 370000, '山东省', 371600, '滨州市', 371625, '博兴县', 118.13, 37.15), \
        (1496, 370000, '山东省', 371600, '滨州市', 371626, '邹平县', 117.73, 36.88), \
        (1497, 370000, '山东省', 371700, '菏泽市', 371701, '市辖区', 0, 0), \
        (1498, 370000, '山东省', 371700, '菏泽市', 371702, '牡丹区', 0, 0), \
        (1499, 370000, '山东省', 371700, '菏泽市', 371721, '曹县', 0, 0), \
        (1500, 370000, '山东省', 371700, '菏泽市', 371722, '单县', 0, 0), \
        (1501, 370000, '山东省', 371700, '菏泽市', 371723, '成武县', 0, 0), \
        (1502, 370000, '山东省', 371700, '菏泽市', 371724, '巨野县', 0, 0), \
        (1503, 370000, '山东省', 371700, '菏泽市', 371725, '郓城县', 0, 0), \
        (1504, 370000, '山东省', 371700, '菏泽市', 371726, '鄄城县', 0, 0), \
        (1505, 370000, '山东省', 371700, '菏泽市', 371727, '定陶县', 0, 0), \
        (1506, 370000, '山东省', 371700, '菏泽市', 371728, '东明县', 0, 0), \
        (1507, 410000, '河南省', 410100, '郑州市', 410101, '市辖区', 113.62, 34.75), \
        (1508, 410000, '河南省', 410100, '郑州市', 410102, '中原区', 113.6, 34.75), \
        (1509, 410000, '河南省', 410100, '郑州市', 410103, '二七区', 113.65, 34.73), \
        (1510, 410000, '河南省', 410100, '郑州市', 410104, '管城回族区', 113.67, 34.75), \
        (1511, 410000, '河南省', 410100, '郑州市', 410105, '金水区', 113.65, 34.78), \
        (1512, 410000, '河南省', 410100, '郑州市', 410106, '上街区', 113.28, 34.82), \
        (1513, 410000, '河南省', 410100, '郑州市', 410108, '惠济区', 113.6, 34.87), \
        (1514, 410000, '河南省', 410100, '郑州市', 410122, '中牟县', 113.97, 34.72), \
        (1515, 410000, '河南省', 410100, '郑州市', 410181, '巩义市', 112.98, 34.77), \
        (1516, 410000, '河南省', 410100, '郑州市', 410182, '荥阳市', 113.4, 34.78), \
        (1517, 410000, '河南省', 410100, '郑州市', 410183, '新密市', 113.38, 34.53), \
        (1518, 410000, '河南省', 410100, '郑州市', 410184, '新郑市', 113.73, 34.4), \
        (1519, 410000, '河南省', 410100, '郑州市', 410185, '登封市', 113.03, 34.47), \
        (1520, 410000, '河南省', 410200, '开封市', 410201, '市辖区', 114.3, 34.8), \
        (1521, 410000, '河南省', 410200, '开封市', 410202, '龙亭区', 114.35, 34.8), \
        (1522, 410000, '河南省', 410200, '开封市', 410203, '顺河回族区', 114.35, 34.8), \
        (1523, 410000, '河南省', 410200, '开封市', 410204, '鼓楼区', 114.35, 34.78), \
        (1524, 410000, '河南省', 410200, '开封市', 410205, '禹王台区', 0, 0), \
        (1525, 410000, '河南省', 410200, '开封市', 410211, '金明区', 0, 0), \
        (1526, 410000, '河南省', 410200, '开封市', 410221, '杞县', 114.78, 34.55), \
        (1527, 410000, '河南省', 410200, '开封市', 410222, '通许县', 114.47, 34.48), \
        (1528, 410000, '河南省', 410200, '开封市', 410223, '尉氏县', 114.18, 34.42), \
        (1529, 410000, '河南省', 410200, '开封市', 410224, '开封县', 114.43, 34.77), \
        (1530, 410000, '河南省', 410200, '开封市', 410225, '兰考县', 114.82, 34.82), \
        (1531, 410000, '河南省', 410300, '洛阳市', 410301, '市辖区', 112.45, 34.62), \
        (1532, 410000, '河南省', 410300, '洛阳市', 410302, '老城区', 112.47, 34.68), \
        (1533, 410000, '河南省', 410300, '洛阳市', 410303, '西工区', 112.43, 34.67), \
        (1534, 410000, '河南省', 410300, '洛阳市', 410304, '廛河回族区', 0, 0), \
        (1535, 410000, '河南省', 410300, '洛阳市', 410305, '涧西区', 112.4, 34.67), \
        (1536, 410000, '河南省', 410300, '洛阳市', 410306, '吉利区', 112.58, 34.9), \
        (1537, 410000, '河南省', 410300, '洛阳市', 410307, '洛龙区', 112.45, 34.62), \
        (1538, 410000, '河南省', 410300, '洛阳市', 410322, '孟津县', 112.43, 34.83), \
        (1539, 410000, '河南省', 410300, '洛阳市', 410323, '新安县', 112.15, 34.72), \
        (1540, 410000, '河南省', 410300, '洛阳市', 410324, '栾川县', 111.62, 33.78), \
        (1541, 410000, '河南省', 410300, '洛阳市', 410325, '嵩县', 112.1, 34.15), \
        (1542, 410000, '河南省', 410300, '洛阳市', 410326, '汝阳县', 112.47, 34.15), \
        (1543, 410000, '河南省', 410300, '洛阳市', 410327, '宜阳县', 112.17, 34.52), \
        (1544, 410000, '河南省', 410300, '洛阳市', 410328, '洛宁县', 111.65, 34.38), \
        (1545, 410000, '河南省', 410300, '洛阳市', 410329, '伊川县', 112.42, 34.42), \
        (1546, 410000, '河南省', 410300, '洛阳市', 410381, '偃师市', 112.78, 34.73), \
        (1547, 410000, '河南省', 410400, '平顶山市', 410401, '市辖区', 113.18, 33.77), \
        (1548, 410000, '河南省', 410400, '平顶山市', 410402, '新华区', 113.3, 33.73), \
        (1549, 410000, '河南省', 410400, '平顶山市', 410403, '卫东区', 113.33, 33.73), \
        (1550, 410000, '河南省', 410400, '平顶山市', 410404, '石龙区', 112.88, 33.9), \
        (1551, 410000, '河南省', 410400, '平顶山市', 410411, '湛河区', 113.28, 33.73), \
        (1552, 410000, '河南省', 410400, '平顶山市', 410421, '宝丰县', 113.07, 33.88), \
        (1553, 410000, '河南省', 410400, '平顶山市', 410422, '叶县', 113.35, 33.62), \
        (1554, 410000, '河南省', 410400, '平顶山市', 410423, '鲁山县', 112.9, 33.73), \
        (1555, 410000, '河南省', 410400, '平顶山市', 410425, '郏县', 113.22, 33.97), \
        (1556, 410000, '河南省', 410400, '平顶山市', 410481, '舞钢市', 113.52, 33.3), \
        (1557, 410000, '河南省', 410400, '平顶山市', 410482, '汝州市', 112.83, 34.17), \
        (1558, 410000, '河南省', 410500, '安阳市', 410501, '市辖区', 114.38, 36.1), \
        (1559, 410000, '河南省', 410500, '安阳市', 410502, '文峰区', 114.35, 36.08), \
        (1560, 410000, '河南省', 410500, '安阳市', 410503, '北关区', 114.35, 36.12), \
        (1561, 410000, '河南省', 410500, '安阳市', 410505, '殷都区', 114.3, 36.12), \
        (1562, 410000, '河南省', 410500, '安阳市', 410506, '龙安区', 114.32, 36.1), \
        (1563, 410000, '河南省', 410500, '安阳市', 410522, '安阳县', 114.35, 36.1), \
        (1564, 410000, '河南省', 410500, '安阳市', 410523, '汤阴县', 114.35, 35.92), \
        (1565, 410000, '河南省', 410500, '安阳市', 410526, '滑县', 114.52, 35.58), \
        (1566, 410000, '河南省', 410500, '安阳市', 410527, '内黄县', 114.9, 35.95), \
        (1567, 410000, '河南省', 410500, '安阳市', 410581, '林州市', 113.82, 36.07), \
        (1568, 410000, '河南省', 410600, '鹤壁市', 410601, '市辖区', 114.28, 35.75), \
        (1569, 410000, '河南省', 410600, '鹤壁市', 410602, '鹤山区', 114.15, 35.95), \
        (1570, 410000, '河南省', 410600, '鹤壁市', 410603, '山城区', 114.18, 35.9), \
        (1571, 410000, '河南省', 410600, '鹤壁市', 410611, '淇滨区', 114.3, 35.73), \
        (1572, 410000, '河南省', 410600, '鹤壁市', 410621, '浚县', 114.55, 35.67), \
        (1573, 410000, '河南省', 410600, '鹤壁市', 410622, '淇县', 114.2, 35.6), \
        (1574, 410000, '河南省', 410700, '新乡市', 410701, '市辖区', 113.9, 35.3), \
        (1575, 410000, '河南省', 410700, '新乡市', 410702, '红旗区', 113.87, 35.3), \
        (1576, 410000, '河南省', 410700, '新乡市', 410703, '卫滨区', 113.85, 35.3), \
        (1577, 410000, '河南省', 410700, '新乡市', 410704, '凤泉区', 113.92, 35.38), \
        (1578, 410000, '河南省', 410700, '新乡市', 410711, '牧野区', 113.9, 35.32), \
        (1579, 410000, '河南省', 410700, '新乡市', 410721, '新乡县', 113.8, 35.2), \
        (1580, 410000, '河南省', 410700, '新乡市', 410724, '获嘉县', 113.65, 35.27), \
        (1581, 410000, '河南省', 410700, '新乡市', 410725, '原阳县', 113.97, 35.05), \
        (1582, 410000, '河南省', 410700, '新乡市', 410726, '延津县', 114.2, 35.15), \
        (1583, 410000, '河南省', 410700, '新乡市', 410727, '封丘县', 114.42, 35.05), \
        (1584, 410000, '河南省', 410700, '新乡市', 410728, '长垣县', 114.68, 35.2), \
        (1585, 410000, '河南省', 410700, '新乡市', 410781, '卫辉市', 114.07, 35.4), \
        (1586, 410000, '河南省', 410700, '新乡市', 410782, '辉县市', 113.8, 35.47), \
        (1587, 410000, '河南省', 410800, '焦作市', 410801, '市辖区', 113.25, 35.22), \
        (1588, 410000, '河南省', 410800, '焦作市', 410802, '解放区', 113.22, 35.25), \
        (1589, 410000, '河南省', 410800, '焦作市', 410803, '中站区', 113.17, 35.23), \
        (1590, 410000, '河南省', 410800, '焦作市', 410804, '马村区', 113.32, 35.27), \
        (1591, 410000, '河南省', 410800, '焦作市', 410811, '山阳区', 113.25, 35.22), \
        (1592, 410000, '河南省', 410800, '焦作市', 410821, '修武县', 113.43, 35.23), \
        (1593, 410000, '河南省', 410800, '焦作市', 410822, '博爱县', 113.07, 35.17), \
        (1594, 410000, '河南省', 410800, '焦作市', 410823, '武陟县', 113.38, 35.1), \
        (1595, 410000, '河南省', 410800, '焦作市', 410825, '温县', 113.08, 34.93), \
        (1596, 410000, '河南省', 410800, '焦作市', 410881, '济源市', 112.58, 35.07), \
        (1597, 410000, '河南省', 410800, '焦作市', 410882, '沁阳市', 112.93, 35.08), \
        (1598, 410000, '河南省', 410800, '焦作市', 410883, '孟州市', 112.78, 34.9), \
        (1599, 410000, '河南省', 410900, '濮阳市', 410901, '市辖区', 115.03, 35.77), \
        (1600, 410000, '河南省', 410900, '濮阳市', 410902, '华龙区', 115.07, 35.78), \
        (1601, 410000, '河南省', 410900, '濮阳市', 410922, '清丰县', 115.12, 35.9), \
        (1602, 410000, '河南省', 410900, '濮阳市', 410923, '南乐县', 115.2, 36.08), \
        (1603, 410000, '河南省', 410900, '濮阳市', 410926, '范县', 115.5, 35.87), \
        (1604, 410000, '河南省', 410900, '濮阳市', 410927, '台前县', 115.85, 36), \
        (1605, 410000, '河南省', 410900, '濮阳市', 410928, '濮阳县', 115.02, 35.7), \
        (1606, 410000, '河南省', 411000, '许昌市', 411001, '市辖区', 113.85, 34.03), \
        (1607, 410000, '河南省', 411000, '许昌市', 411002, '魏都区', 113.82, 34.03), \
        (1608, 410000, '河南省', 411000, '许昌市', 411023, '许昌县', 113.83, 34), \
        (1609, 410000, '河南省', 411000, '许昌市', 411024, '鄢陵县', 114.2, 34.1), \
        (1610, 410000, '河南省', 411000, '许昌市', 411025, '襄城县', 113.48, 33.85), \
        (1611, 410000, '河南省', 411000, '许昌市', 411081, '禹州市', 113.47, 34.17), \
        (1612, 410000, '河南省', 411000, '许昌市', 411082, '长葛市', 113.77, 34.22), \
        (1613, 410000, '河南省', 411100, '漯河市', 411101, '市辖区', 114.02, 33.58), \
        (1614, 410000, '河南省', 411100, '漯河市', 411102, '源汇区', 0, 0), \
        (1615, 410000, '河南省', 411100, '漯河市', 411103, '郾城区', 114, 33.58), \
        (1616, 410000, '河南省', 411100, '漯河市', 411104, '召陵区', 114.07, 33.57), \
        (1617, 410000, '河南省', 411100, '漯河市', 411121, '舞阳县', 113.6, 33.43), \
        (1618, 410000, '河南省', 411100, '漯河市', 411122, '临颍县', 113.93, 33.82), \
        (1619, 410000, '河南省', 411200, '三门峡市', 411201, '市辖区', 111.2, 34.78), \
        (1620, 410000, '河南省', 411200, '三门峡市', 411202, '湖滨区', 111.2, 34.78), \
        (1621, 410000, '河南省', 411200, '三门峡市', 411221, '渑池县', 111.75, 34.77), \
        (1622, 410000, '河南省', 411200, '三门峡市', 411222, '陕县', 111.08, 34.7), \
        (1623, 410000, '河南省', 411200, '三门峡市', 411224, '卢氏县', 111.05, 34.05), \
        (1624, 410000, '河南省', 411200, '三门峡市', 411281, '义马市', 111.87, 34.75), \
        (1625, 410000, '河南省', 411200, '三门峡市', 411282, '灵宝市', 110.87, 34.52), \
        (1626, 410000, '河南省', 411300, '南阳市', 411301, '市辖区', 112.52, 33), \
        (1627, 410000, '河南省', 411300, '南阳市', 411302, '宛城区', 112.55, 33.02), \
        (1628, 410000, '河南省', 411300, '南阳市', 411303, '卧龙区', 112.53, 32.98), \
        (1629, 410000, '河南省', 411300, '南阳市', 411321, '南召县', 112.43, 33.5), \
        (1630, 410000, '河南省', 411300, '南阳市', 411322, '方城县', 113, 33.27), \
        (1631, 410000, '河南省', 411300, '南阳市', 411323, '西峡县', 111.48, 33.28), \
        (1632, 410000, '河南省', 411300, '南阳市', 411324, '镇平县', 112.23, 33.03), \
        (1633, 410000, '河南省', 411300, '南阳市', 411325, '内乡县', 111.85, 33.05), \
        (1634, 410000, '河南省', 411300, '南阳市', 411326, '淅川县', 111.48, 33.13), \
        (1635, 410000, '河南省', 411300, '南阳市', 411327, '社旗县', 112.93, 33.05), \
        (1636, 410000, '河南省', 411300, '南阳市', 411328, '唐河县', 112.83, 32.7), \
        (1637, 410000, '河南省', 411300, '南阳市', 411329, '新野县', 112.35, 32.52), \
        (1638, 410000, '河南省', 411300, '南阳市', 411330, '桐柏县', 113.4, 32.37), \
        (1639, 410000, '河南省', 411300, '南阳市', 411381, '邓州市', 112.08, 32.68), \
        (1640, 410000, '河南省', 411400, '商丘市', 411401, '市辖区', 115.65, 34.45), \
        (1641, 410000, '河南省', 411400, '商丘市', 411402, '梁园区', 115.63, 34.45), \
        (1642, 410000, '河南省', 411400, '商丘市', 411403, '睢阳区', 115.63, 34.38), \
        (1643, 410000, '河南省', 411400, '商丘市', 411421, '民权县', 115.13, 34.65), \
        (1644, 410000, '河南省', 411400, '商丘市', 411422, '睢县', 115.07, 34.45), \
        (1645, 410000, '河南省', 411400, '商丘市', 411423, '宁陵县', 115.32, 34.45), \
        (1646, 410000, '河南省', 411400, '商丘市', 411424, '柘城县', 115.3, 34.07), \
        (1647, 410000, '河南省', 411400, '商丘市', 411425, '虞城县', 115.85, 34.4), \
        (1648, 410000, '河南省', 411400, '商丘市', 411426, '夏邑县', 116.13, 34.23), \
        (1649, 410000, '河南省', 411400, '商丘市', 411481, '永城市', 116.43, 33.92), \
        (1650, 410000, '河南省', 411500, '信阳市', 411501, '市辖区', 114.07, 32.13), \
        (1651, 410000, '河南省', 411500, '信阳市', 411502, '浉河区', 114.05, 32.12), \
        (1652, 410000, '河南省', 411500, '信阳市', 411503, '平桥区', 114.12, 32.1), \
        (1653, 410000, '河南省', 411500, '信阳市', 411521, '罗山县', 114.53, 32.2), \
        (1654, 410000, '河南省', 411500, '信阳市', 411522, '光山县', 114.9, 32.02), \
        (1655, 410000, '河南省', 411500, '信阳市', 411523, '新县', 114.87, 31.63), \
        (1656, 410000, '河南省', 411500, '信阳市', 411524, '商城县', 115.4, 31.8), \
        (1657, 410000, '河南省', 411500, '信阳市', 411525, '固始县', 115.68, 32.18), \
        (1658, 410000, '河南省', 411500, '信阳市', 411526, '潢川县', 115.03, 32.13), \
        (1659, 410000, '河南省', 411500, '信阳市', 411527, '淮滨县', 115.4, 32.43), \
        (1660, 410000, '河南省', 411500, '信阳市', 411528, '息县', 114.73, 32.35), \
        (1661, 410000, '河南省', 411600, '周口市', 411601, '市辖区', 114.65, 33.62), \
        (1662, 410000, '河南省', 411600, '周口市', 411602, '川汇区', 0, 0), \
        (1663, 410000, '河南省', 411600, '周口市', 411621, '扶沟县', 114.38, 34.07), \
        (1664, 410000, '河南省', 411600, '周口市', 411622, '西华县', 114.53, 33.8), \
        (1665, 410000, '河南省', 411600, '周口市', 411623, '商水县', 114.6, 33.53), \
        (1666, 410000, '河南省', 411600, '周口市', 411624, '沈丘县', 115.07, 33.4), \
        (1667, 410000, '河南省', 411600, '周口市', 411625, '郸城县', 115.2, 33.65), \
        (1668, 410000, '河南省', 411600, '周口市', 411626, '淮阳县', 114.88, 33.73), \
        (1669, 410000, '河南省', 411600, '周口市', 411627, '太康县', 114.85, 34.07), \
        (1670, 410000, '河南省', 411600, '周口市', 411628, '鹿邑县', 115.48, 33.87), \
        (1671, 410000, '河南省', 411600, '周口市', 411681, '项城市', 114.9, 33.45), \
        (1672, 410000, '河南省', 411700, '驻马店市', 411701, '市辖区', 114.02, 32.98), \
        (1673, 410000, '河南省', 411700, '驻马店市', 411702, '驿城区', 114.05, 32.97), \
        (1674, 410000, '河南省', 411700, '驻马店市', 411721, '西平县', 114.02, 33.38), \
        (1675, 410000, '河南省', 411700, '驻马店市', 411722, '上蔡县', 114.27, 33.27), \
        (1676, 410000, '河南省', 411700, '驻马店市', 411723, '平舆县', 114.63, 32.97), \
        (1677, 410000, '河南省', 411700, '驻马店市', 411724, '正阳县', 114.38, 32.6), \
        (1678, 410000, '河南省', 411700, '驻马店市', 411725, '确山县', 114.02, 32.8), \
        (1679, 410000, '河南省', 411700, '驻马店市', 411726, '泌阳县', 113.32, 32.72), \
        (1680, 410000, '河南省', 411700, '驻马店市', 411727, '汝南县', 114.35, 33), \
        (1681, 410000, '河南省', 411700, '驻马店市', 411728, '遂平县', 114, 33.15), \
        (1682, 410000, '河南省', 411700, '驻马店市', 411729, '新蔡县', 114.98, 32.75), \
        (1683, 420000, '湖北省', 420100, '武汉市', 420101, '市辖区', 114.3, 30.6), \
        (1684, 420000, '湖北省', 420100, '武汉市', 420102, '江岸区', 114.3, 30.6), \
        (1685, 420000, '湖北省', 420100, '武汉市', 420103, '江汉区', 114.27, 30.6), \
        (1686, 420000, '湖北省', 420100, '武汉市', 420104, '硚口区', 114.27, 30.57), \
        (1687, 420000, '湖北省', 420100, '武汉市', 420105, '汉阳区', 114.27, 30.55), \
        (1688, 420000, '湖北省', 420100, '武汉市', 420106, '武昌区', 114.3, 30.57), \
        (1689, 420000, '湖北省', 420100, '武汉市', 420107, '青山区', 114.38, 30.63), \
        (1690, 420000, '湖北省', 420100, '武汉市', 420111, '洪山区', 114.33, 30.5), \
        (1691, 420000, '湖北省', 420100, '武汉市', 420112, '东西湖区', 114.13, 30.62), \
        (1692, 420000, '湖北省', 420100, '武汉市', 420113, '汉南区', 114.08, 30.32), \
        (1693, 420000, '湖北省', 420100, '武汉市', 420114, '蔡甸区', 114.03, 30.58), \
        (1694, 420000, '湖北省', 420100, '武汉市', 420115, '江夏区', 114.32, 30.35), \
        (1695, 420000, '湖北省', 420100, '武汉市', 420116, '黄陂区', 114.37, 30.87), \
        (1696, 420000, '湖北省', 420100, '武汉市', 420117, '新洲区', 114.8, 30.85), \
        (1697, 420000, '湖北省', 420200, '黄石市', 420201, '市辖区', 115.03, 30.2), \
        (1698, 420000, '湖北省', 420200, '黄石市', 420202, '黄石港区', 115.07, 30.23), \
        (1699, 420000, '湖北省', 420200, '黄石市', 420203, '西塞山区', 115.12, 30.2), \
        (1700, 420000, '湖北省', 420200, '黄石市', 420204, '下陆区', 114.97, 30.18), \
        (1701, 420000, '湖北省', 420200, '黄石市', 420205, '铁山区', 114.9, 30.2), \
        (1702, 420000, '湖北省', 420200, '黄石市', 420222, '阳新县', 115.2, 29.85), \
        (1703, 420000, '湖北省', 420200, '黄石市', 420281, '大冶市', 114.97, 30.1), \
        (1704, 420000, '湖北省', 420300, '十堰市', 420301, '市辖区', 110.78, 32.65), \
        (1705, 420000, '湖北省', 420300, '十堰市', 420302, '茅箭区', 110.82, 32.6), \
        (1706, 420000, '湖北省', 420300, '十堰市', 420303, '张湾区', 110.78, 32.65), \
        (1707, 420000, '湖北省', 420300, '十堰市', 420321, '郧县', 110.82, 32.83), \
        (1708, 420000, '湖北省', 420300, '十堰市', 420322, '郧西县', 110.42, 33), \
        (1709, 420000, '湖北省', 420300, '十堰市', 420323, '竹山县', 110.23, 32.23), \
        (1710, 420000, '湖北省', 420300, '十堰市', 420324, '竹溪县', 109.72, 32.32), \
        (1711, 420000, '湖北省', 420300, '十堰市', 420325, '房县', 110.73, 32.07), \
        (1712, 420000, '湖北省', 420300, '十堰市', 420381, '丹江口市', 111.52, 32.55), \
        (1713, 420000, '湖北省', 420500, '宜昌市', 420501, '市辖区', 111.28, 30.7), \
        (1714, 420000, '湖北省', 420500, '宜昌市', 420502, '西陵区', 111.27, 30.7), \
        (1715, 420000, '湖北省', 420500, '宜昌市', 420503, '伍家岗区', 111.35, 30.65), \
        (1716, 420000, '湖北省', 420500, '宜昌市', 420504, '点军区', 111.27, 30.7), \
        (1717, 420000, '湖北省', 420500, '宜昌市', 420505, '猇亭区', 111.42, 30.53), \
        (1718, 420000, '湖北省', 420500, '宜昌市', 420506, '夷陵区', 111.32, 30.77), \
        (1719, 420000, '湖北省', 420500, '宜昌市', 420525, '远安县', 111.63, 31.07), \
        (1720, 420000, '湖北省', 420500, '宜昌市', 420526, '兴山县', 110.75, 31.35), \
        (1721, 420000, '湖北省', 420500, '宜昌市', 420527, '秭归县', 110.98, 30.83), \
        (1722, 420000, '湖北省', 420500, '宜昌市', 420528, '长阳土家族自治县', 111.18, 30.47), \
        (1723, 420000, '湖北省', 420500, '宜昌市', 420529, '五峰土家族自治县', 110.67, 30.2), \
        (1724, 420000, '湖北省', 420500, '宜昌市', 420581, '宜都市', 111.45, 30.4), \
        (1725, 420000, '湖北省', 420500, '宜昌市', 420582, '当阳市', 111.78, 30.82), \
        (1726, 420000, '湖北省', 420500, '宜昌市', 420583, '枝江市', 111.77, 30.43), \
        (1727, 420000, '湖北省', 420600, '襄樊市', 420601, '市辖区', 112.15, 32.02), \
        (1728, 420000, '湖北省', 420600, '襄樊市', 420602, '襄城区', 112.15, 32.02), \
        (1729, 420000, '湖北省', 420600, '襄樊市', 420606, '樊城区', 112.13, 32.03), \
        (1730, 420000, '湖北省', 420600, '襄樊市', 420607, '襄阳区', 112.2, 32.08), \
        (1731, 420000, '湖北省', 420600, '襄樊市', 420624, '南漳县', 111.83, 31.78), \
        (1732, 420000, '湖北省', 420600, '襄樊市', 420625, '谷城县', 111.65, 32.27), \
        (1733, 420000, '湖北省', 420600, '襄樊市', 420626, '保康县', 111.25, 31.88), \
        (1734, 420000, '湖北省', 420600, '襄樊市', 420682, '老河口市', 111.67, 32.38), \
        (1735, 420000, '湖北省', 420600, '襄樊市', 420683, '枣阳市', 112.75, 32.13), \
        (1736, 420000, '湖北省', 420600, '襄樊市', 420684, '宜城市', 112.25, 31.72), \
        (1737, 420000, '湖北省', 420700, '鄂州市', 420701, '市辖区', 114.88, 30.4), \
        (1738, 420000, '湖北省', 420700, '鄂州市', 420702, '梁子湖区', 114.67, 30.08), \
        (1739, 420000, '湖北省', 420700, '鄂州市', 420703, '华容区', 114.73, 30.53), \
        (1740, 420000, '湖北省', 420700, '鄂州市', 420704, '鄂城区', 114.88, 30.4), \
        (1741, 420000, '湖北省', 420800, '荆门市', 420801, '市辖区', 112.2, 31.03), \
        (1742, 420000, '湖北省', 420800, '荆门市', 420802, '东宝区', 112.2, 31.05), \
        (1743, 420000, '湖北省', 420800, '荆门市', 420804, '掇刀区', 112.2, 30.98), \
        (1744, 420000, '湖北省', 420800, '荆门市', 420821, '京山县', 113.1, 31.02), \
        (1745, 420000, '湖北省', 420800, '荆门市', 420822, '沙洋县', 112.58, 30.7), \
        (1746, 420000, '湖北省', 420800, '荆门市', 420881, '钟祥市', 112.58, 31.17), \
        (1747, 420000, '湖北省', 420900, '孝感市', 420901, '市辖区', 113.92, 30.93), \
        (1748, 420000, '湖北省', 420900, '孝感市', 420902, '孝南区', 113.92, 30.92), \
        (1749, 420000, '湖北省', 420900, '孝感市', 420921, '孝昌县', 113.97, 31.25), \
        (1750, 420000, '湖北省', 420900, '孝感市', 420922, '大悟县', 114.12, 31.57), \
        (1751, 420000, '湖北省', 420900, '孝感市', 420923, '云梦县', 113.75, 31.02), \
        (1752, 420000, '湖北省', 420900, '孝感市', 420981, '应城市', 113.57, 30.95), \
        (1753, 420000, '湖北省', 420900, '孝感市', 420982, '安陆市', 113.68, 31.27), \
        (1754, 420000, '湖北省', 420900, '孝感市', 420984, '汉川市', 113.83, 30.65), \
        (1755, 420000, '湖北省', 421000, '荆州市', 421001, '市辖区', 112.23, 30.33), \
        (1756, 420000, '湖北省', 421000, '荆州市', 421002, '沙市区', 112.25, 30.32), \
        (1757, 420000, '湖北省', 421000, '荆州市', 421003, '荆州区', 112.18, 30.35), \
        (1758, 420000, '湖北省', 421000, '荆州市', 421022, '公安县', 112.23, 30.07), \
        (1759, 420000, '湖北省', 421000, '荆州市', 421023, '监利县', 112.88, 29.82), \
        (1760, 420000, '湖北省', 421000, '荆州市', 421024, '江陵县', 112.42, 30.03), \
        (1761, 420000, '湖北省', 421000, '荆州市', 421081, '石首市', 112.4, 29.73), \
        (1762, 420000, '湖北省', 421000, '荆州市', 421083, '洪湖市', 113.45, 29.8), \
        (1763, 420000, '湖北省', 421000, '荆州市', 421087, '松滋市', 111.77, 30.18), \
        (1764, 420000, '湖北省', 421100, '黄冈市', 421101, '市辖区', 114.87, 30.45), \
        (1765, 420000, '湖北省', 421100, '黄冈市', 421102, '黄州区', 114.88, 30.43), \
        (1766, 420000, '湖北省', 421100, '黄冈市', 421121, '团风县', 114.87, 30.63), \
        (1767, 420000, '湖北省', 421100, '黄冈市', 421122, '红安县', 114.62, 31.28), \
        (1768, 420000, '湖北省', 421100, '黄冈市', 421123, '罗田县', 115.4, 30.78), \
        (1769, 420000, '湖北省', 421100, '黄冈市', 421124, '英山县', 115.67, 30.75), \
        (1770, 420000, '湖北省', 421100, '黄冈市', 421125, '浠水县', 115.27, 30.45), \
        (1771, 420000, '湖北省', 421100, '黄冈市', 421126, '蕲春县', 115.43, 30.23), \
        (1772, 420000, '湖北省', 421100, '黄冈市', 421127, '黄梅县', 115.93, 30.08), \
        (1773, 420000, '湖北省', 421100, '黄冈市', 421181, '麻城市', 115.03, 31.18), \
        (1774, 420000, '湖北省', 421100, '黄冈市', 421182, '武穴市', 115.55, 29.85), \
        (1775, 420000, '湖北省', 421200, '咸宁市', 421201, '市辖区', 114.32, 29.85), \
        (1776, 420000, '湖北省', 421200, '咸宁市', 421202, '咸安区', 114.3, 29.87), \
        (1777, 420000, '湖北省', 421200, '咸宁市', 421221, '嘉鱼县', 113.9, 29.98), \
        (1778, 420000, '湖北省', 421200, '咸宁市', 421222, '通城县', 113.82, 29.25), \
        (1779, 420000, '湖北省', 421200, '咸宁市', 421223, '崇阳县', 114.03, 29.55), \
        (1780, 420000, '湖北省', 421200, '咸宁市', 421224, '通山县', 114.52, 29.6), \
        (1781, 420000, '湖北省', 421200, '咸宁市', 421281, '赤壁市', 113.88, 29.72), \
        (1782, 420000, '湖北省', 421300, '随州市', 421301, '市辖区', 113.37, 31.72), \
        (1783, 420000, '湖北省', 421300, '随州市', 421302, '曾都区', 113.37, 31.72), \
        (1784, 420000, '湖北省', 421300, '随州市', 421381, '广水市', 113.82, 31.62),
        (1785, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422801, '恩施市', 109.47, 30.3), \
        (1786, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422802, '利川市', 108.93, 30.3), \
        (1787, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422822, '建始县', 109.73, 30.6), \
        (1788, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422823, '巴东县', 110.33, 31.05), \
        (1789, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422825, '宣恩县', 109.48, 29.98), \
        (1790, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422826, '咸丰县', 109.15, 29.68), \
        (1791, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422827, '来凤县', 109.4, 29.52), \
        (1792, 420000, '湖北省', 422800, '恩施土家族苗族自治', 422828, '鹤峰县', 110.03, 29.9), \
        (1793, 420000, '湖北省', 429000, '省直辖行政单位', 429004, '仙桃市', 0, 0), \
        (1794, 420000, '湖北省', 429000, '省直辖行政单位', 429005, '潜江市', 0, 0), \
        (1795, 420000, '湖北省', 429000, '省直辖行政单位', 429006, '天门市', 0, 0), \
        (1796, 420000, '湖北省', 429000, '省直辖行政单位', 429021, '神农架林区', 0, 0), \
        (1797, 430000, '湖南省', 430100, '长沙市', 430101, '市辖区', 112.93, 28.23), \
        (1798, 430000, '湖南省', 430100, '长沙市', 430102, '芙蓉区', 113.03, 28.18), \
        (1799, 430000, '湖南省', 430100, '长沙市', 430103, '天心区', 112.98, 28.12), \
        (1800, 430000, '湖南省', 430100, '长沙市', 430104, '岳麓区', 112.93, 28.23), \
        (1801, 430000, '湖南省', 430100, '长沙市', 430105, '开福区', 112.98, 28.25), \
        (1802, 430000, '湖南省', 430100, '长沙市', 430111, '雨花区', 113.03, 28.13), \
        (1803, 430000, '湖南省', 430100, '长沙市', 430121, '长沙县', 113.07, 28.25), \
        (1804, 430000, '湖南省', 430100, '长沙市', 430122, '望城县', 112.82, 28.37), \
        (1805, 430000, '湖南省', 430100, '长沙市', 430124, '宁乡县', 112.55, 28.25), \
        (1806, 430000, '湖南省', 430100, '长沙市', 430181, '浏阳市', 113.63, 28.15), \
        (1807, 430000, '湖南省', 430200, '株洲市', 430201, '市辖区', 113.13, 27.83), \
        (1808, 430000, '湖南省', 430200, '株洲市', 430202, '荷塘区', 113.17, 27.87), \
        (1809, 430000, '湖南省', 430200, '株洲市', 430203, '芦淞区', 113.15, 27.83), \
        (1810, 430000, '湖南省', 430200, '株洲市', 430204, '石峰区', 113.1, 27.87), \
        (1811, 430000, '湖南省', 430200, '株洲市', 430211, '天元区', 113.12, 27.83), \
        (1812, 430000, '湖南省', 430200, '株洲市', 430221, '株洲县', 113.13, 27.72), \
        (1813, 430000, '湖南省', 430200, '株洲市', 430223, '攸县', 113.33, 27), \
        (1814, 430000, '湖南省', 430200, '株洲市', 430224, '茶陵县', 113.53, 26.8), \
        (1815, 430000, '湖南省', 430200, '株洲市', 430225, '炎陵县', 113.77, 26.48), \
        (1816, 430000, '湖南省', 430200, '株洲市', 430281, '醴陵市', 113.48, 27.67), \
        (1817, 430000, '湖南省', 430300, '湘潭市', 430301, '市辖区', 112.93, 27.83), \
        (1818, 430000, '湖南省', 430300, '湘潭市', 430302, '雨湖区', 112.9, 27.87), \
        (1819, 430000, '湖南省', 430300, '湘潭市', 430304, '岳塘区', 112.95, 27.87), \
        (1820, 430000, '湖南省', 430300, '湘潭市', 430321, '湘潭县', 112.95, 27.78), \
        (1821, 430000, '湖南省', 430300, '湘潭市', 430381, '湘乡市', 112.53, 27.73), \
        (1822, 430000, '湖南省', 430300, '湘潭市', 430382, '韶山市', 112.52, 27.93), \
        (1823, 430000, '湖南省', 430400, '衡阳市', 430401, '市辖区', 112.57, 26.9), \
        (1824, 430000, '湖南省', 430400, '衡阳市', 430405, '珠晖区', 112.62, 26.9), \
        (1825, 430000, '湖南省', 430400, '衡阳市', 430406, '雁峰区', 112.6, 26.88), \
        (1826, 430000, '湖南省', 430400, '衡阳市', 430407, '石鼓区', 112.6, 26.9), \
        (1827, 430000, '湖南省', 430400, '衡阳市', 430408, '蒸湘区', 112.6, 26.9), \
        (1828, 430000, '湖南省', 430400, '衡阳市', 430412, '南岳区', 112.73, 27.25), \
        (1829, 430000, '湖南省', 430400, '衡阳市', 430421, '衡阳县', 112.37, 26.97), \
        (1830, 430000, '湖南省', 430400, '衡阳市', 430422, '衡南县', 112.67, 26.73), \
        (1831, 430000, '湖南省', 430400, '衡阳市', 430423, '衡山县', 112.87, 27.23), \
        (1832, 430000, '湖南省', 430400, '衡阳市', 430424, '衡东县', 112.95, 27.08), \
        (1833, 430000, '湖南省', 430400, '衡阳市', 430426, '祁东县', 112.12, 26.78), \
        (1834, 430000, '湖南省', 430400, '衡阳市', 430481, '耒阳市', 112.85, 26.42), \
        (1835, 430000, '湖南省', 430400, '衡阳市', 430482, '常宁市', 112.38, 26.42), \
        (1836, 430000, '湖南省', 430500, '邵阳市', 430501, '市辖区', 111.47, 27.25), \
        (1837, 430000, '湖南省', 430500, '邵阳市', 430502, '双清区', 111.47, 27.23), \
        (1838, 430000, '湖南省', 430500, '邵阳市', 430503, '大祥区', 111.45, 27.23), \
        (1839, 430000, '湖南省', 430500, '邵阳市', 430511, '北塔区', 111.45, 27.25), \
        (1840, 430000, '湖南省', 430500, '邵阳市', 430521, '邵东县', 111.75, 27.25), \
        (1841, 430000, '湖南省', 430500, '邵阳市', 430522, '新邵县', 111.45, 27.32), \
        (1842, 430000, '湖南省', 430500, '邵阳市', 430523, '邵阳县', 111.27, 27), \
        (1843, 430000, '湖南省', 430500, '邵阳市', 430524, '隆回县', 111.03, 27.12), \
        (1844, 430000, '湖南省', 430500, '邵阳市', 430525, '洞口县', 110.57, 27.05), \
        (1845, 430000, '湖南省', 430500, '邵阳市', 430527, '绥宁县', 110.15, 26.58), \
        (1846, 430000, '湖南省', 430500, '邵阳市', 430528, '新宁县', 110.85, 26.43), \
        (1847, 430000, '湖南省', 430500, '邵阳市', 430529, '城步苗族自治县', 110.32, 26.37), \
        (1848, 430000, '湖南省', 430500, '邵阳市', 430581, '武冈市', 110.63, 26.73), \
        (1849, 430000, '湖南省', 430600, '岳阳市', 430601, '市辖区', 113.12, 29.37), \
        (1850, 430000, '湖南省', 430600, '岳阳市', 430602, '岳阳楼区', 113.1, 29.37), \
        (1851, 430000, '湖南省', 430600, '岳阳市', 430603, '云溪区', 113.3, 29.47), \
        (1852, 430000, '湖南省', 430600, '岳阳市', 430611, '君山区', 113, 29.43), \
        (1853, 430000, '湖南省', 430600, '岳阳市', 430621, '岳阳县', 113.12, 29.15), \
        (1854, 430000, '湖南省', 430600, '岳阳市', 430623, '华容县', 112.57, 29.52), \
        (1855, 430000, '湖南省', 430600, '岳阳市', 430624, '湘阴县', 112.88, 28.68), \
        (1856, 430000, '湖南省', 430600, '岳阳市', 430626, '平江县', 113.58, 28.72), \
        (1857, 430000, '湖南省', 430600, '岳阳市', 430681, '汨罗市', 113.08, 28.8), \
        (1858, 430000, '湖南省', 430600, '岳阳市', 430682, '临湘市', 113.47, 29.48), \
        (1859, 430000, '湖南省', 430700, '常德市', 430701, '市辖区', 111.68, 29.05), \
        (1860, 430000, '湖南省', 430700, '常德市', 430702, '武陵区', 111.68, 29.03), \
        (1861, 430000, '湖南省', 430700, '常德市', 430703, '鼎城区', 111.68, 29.02), \
        (1862, 430000, '湖南省', 430700, '常德市', 430721, '安乡县', 112.17, 29.42), \
        (1863, 430000, '湖南省', 430700, '常德市', 430722, '汉寿县', 111.97, 28.9), \
        (1864, 430000, '湖南省', 430700, '常德市', 430723, '澧县', 111.75, 29.63), \
        (1865, 430000, '湖南省', 430700, '常德市', 430724, '临澧县', 111.65, 29.45), \
        (1866, 430000, '湖南省', 430700, '常德市', 430725, '桃源县', 111.48, 28.9), \
        (1867, 430000, '湖南省', 430700, '常德市', 430726, '石门县', 111.38, 29.58), \
        (1868, 430000, '湖南省', 430700, '常德市', 430781, '津市市', 111.88, 29.62), \
        (1869, 430000, '湖南省', 430800, '张家界市', 430801, '市辖区', 110.47, 29.13), \
        (1870, 430000, '湖南省', 430800, '张家界市', 430802, '永定区', 110.48, 29.13), \
        (1871, 430000, '湖南省', 430800, '张家界市', 430811, '武陵源区', 110.53, 29.35), \
        (1872, 430000, '湖南省', 430800, '张家界市', 430821, '慈利县', 111.12, 29.42), \
        (1873, 430000, '湖南省', 430800, '张家界市', 430822, '桑植县', 110.15, 29.4), \
        (1874, 430000, '湖南省', 430900, '益阳市', 430901, '市辖区', 112.32, 28.6), \
        (1875, 430000, '湖南省', 430900, '益阳市', 430902, '资阳区', 112.32, 28.6), \
        (1876, 430000, '湖南省', 430900, '益阳市', 430903, '赫山区', 112.37, 28.6), \
        (1877, 430000, '湖南省', 430900, '益阳市', 430921, '南县', 112.4, 29.38), \
        (1878, 430000, '湖南省', 430900, '益阳市', 430922, '桃江县', 112.12, 28.53), \
        (1879, 430000, '湖南省', 430900, '益阳市', 430923, '安化县', 111.22, 28.38), \
        (1880, 430000, '湖南省', 430900, '益阳市', 430981, '沅江市', 112.38, 28.85), \
        (1881, 430000, '湖南省', 431000, '郴州市', 431001, '市辖区', 113.02, 25.78), \
        (1882, 430000, '湖南省', 431000, '郴州市', 431002, '北湖区', 113.02, 25.8), \
        (1883, 430000, '湖南省', 431000, '郴州市', 431003, '苏仙区', 113.03, 25.8), \
        (1884, 430000, '湖南省', 431000, '郴州市', 431021, '桂阳县', 112.73, 25.73), \
        (1885, 430000, '湖南省', 431000, '郴州市', 431022, '宜章县', 112.95, 25.4), \
        (1886, 430000, '湖南省', 431000, '郴州市', 431023, '永兴县', 113.1, 26.13), \
        (1887, 430000, '湖南省', 431000, '郴州市', 431024, '嘉禾县', 112.37, 25.58), \
        (1888, 430000, '湖南省', 431000, '郴州市', 431025, '临武县', 112.55, 25.28), \
        (1889, 430000, '湖南省', 431000, '郴州市', 431026, '汝城县', 113.68, 25.55), \
        (1890, 430000, '湖南省', 431000, '郴州市', 431027, '桂东县', 113.93, 26.08), \
        (1891, 430000, '湖南省', 431000, '郴州市', 431028, '安仁县', 113.27, 26.7), \
        (1892, 430000, '湖南省', 431000, '郴州市', 431081, '资兴市', 113.23, 25.98), \
        (1893, 430000, '湖南省', 431100, '永州市', 431101, '市辖区', 111.62, 26.43), \
        (1894, 430000, '湖南省', 431100, '永州市', 431102, '零陵区', 0, 0), \
        (1895, 430000, '湖南省', 431100, '永州市', 431103, '冷水滩区', 111.6, 26.43), \
        (1896, 430000, '湖南省', 431100, '永州市', 431121, '祁阳县', 111.85, 26.58), \
        (1897, 430000, '湖南省', 431100, '永州市', 431122, '东安县', 111.28, 26.4), \
        (1898, 430000, '湖南省', 431100, '永州市', 431123, '双牌县', 111.65, 25.97), \
        (1899, 430000, '湖南省', 431100, '永州市', 431124, '道县', 111.58, 25.53), \
        (1900, 430000, '湖南省', 431100, '永州市', 431125, '江永县', 111.33, 25.28), \
        (1901, 430000, '湖南省', 431100, '永州市', 431126, '宁远县', 111.93, 25.6), \
        (1902, 430000, '湖南省', 431100, '永州市', 431127, '蓝山县', 112.18, 25.37), \
        (1903, 430000, '湖南省', 431100, '永州市', 431128, '新田县', 112.22, 25.92), \
        (1904, 430000, '湖南省', 431100, '永州市', 431129, '江华瑶族自治县', 111.58, 25.18), \
        (1905, 430000, '湖南省', 431200, '怀化市', 431201, '市辖区', 110, 27.57), \
        (1906, 430000, '湖南省', 431200, '怀化市', 431202, '鹤城区', 109.95, 27.55), \
        (1907, 430000, '湖南省', 431200, '怀化市', 431221, '中方县', 109.93, 27.4), \
        (1908, 430000, '湖南省', 431200, '怀化市', 431222, '沅陵县', 110.38, 28.47), \
        (1909, 430000, '湖南省', 431200, '怀化市', 431223, '辰溪县', 110.18, 28), \
        (1910, 430000, '湖南省', 431200, '怀化市', 431224, '溆浦县', 110.58, 27.92), \
        (1911, 430000, '湖南省', 431200, '怀化市', 431225, '会同县', 109.72, 26.87), \
        (1912, 430000, '湖南省', 431200, '怀化市', 431226, '麻阳苗族自治县', 109.8, 27.87), \
        (1913, 430000, '湖南省', 431200, '怀化市', 431227, '新晃侗族自治县', 109.17, 27.37), \
        (1914, 430000, '湖南省', 431200, '怀化市', 431228, '芷江侗族自治县', 109.68, 27.45), \
        (1915, 430000, '湖南省', 431200, '怀化市', 431229, '靖州苗族侗族自治县', 109.68, 26.58), \
        (1916, 430000, '湖南省', 431200, '怀化市', 431230, '通道侗族自治县', 109.78, 26.17), \
        (1917, 430000, '湖南省', 431200, '怀化市', 431281, '洪江市', 109.82, 27.2), \
        (1918, 430000, '湖南省', 431300, '娄底市', 431301, '市辖区', 112, 27.73), \
        (1919, 430000, '湖南省', 431300, '娄底市', 431302, '娄星区', 112, 27.73), \
        (1920, 430000, '湖南省', 431300, '娄底市', 431321, '双峰县', 112.2, 27.45), \
        (1921, 430000, '湖南省', 431300, '娄底市', 431322, '新化县', 111.3, 27.75), \
        (1922, 430000, '湖南省', 431300, '娄底市', 431381, '冷水江市', 111.43, 27.68), \
        (1923, 430000, '湖南省', 431300, '娄底市', 431382, '涟源市', 111.67, 27.7), \
        (1924, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433101, '吉首市', 109.73, 28.32), \
        (1925, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433122, '泸溪县', 110.22, 28.22), \
        (1926, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433123, '凤凰县', 109.6, 27.95), \
        (1927, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433124, '花垣县', 109.48, 28.58), \
        (1928, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433125, '保靖县', 109.65, 28.72), \
        (1929, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433126, '古丈县', 109.95, 28.62), \
        (1930, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433127, '永顺县', 109.85, 29), \
        (1931, 430000, '湖南省', 433100, '湘西土家族苗族自治', 433130, '龙山县', 109.43, 29.47), \
        (1932, 440000, '广东省', 440100, '广州市', 440101, '市辖区', 113.27, 23.13), \
        (1933, 440000, '广东省', 440100, '广州市', 440103, '荔湾区', 113.23, 23.13), \
        (1934, 440000, '广东省', 440100, '广州市', 440104, '越秀区', 113.27, 23.13), \
        (1935, 440000, '广东省', 440100, '广州市', 440105, '海珠区', 113.25, 23.1), \
        (1936, 440000, '广东省', 440100, '广州市', 440106, '天河区', 113.35, 23.12), \
        (1937, 440000, '广东省', 440100, '广州市', 440111, '白云区', 113.27, 23.17), \
        (1938, 440000, '广东省', 440100, '广州市', 440112, '黄埔区', 113.45, 23.1), \
        (1939, 440000, '广东省', 440100, '广州市', 440113, '番禺区', 113.35, 22.95), \
        (1940, 440000, '广东省', 440100, '广州市', 440114, '花都区', 113.22, 23.4), \
        (1941, 440000, '广东省', 440100, '广州市', 440115, '南沙区', 0, 0), \
        (1942, 440000, '广东省', 440100, '广州市', 440116, '萝岗区', 0, 0), \
        (1943, 440000, '广东省', 440100, '广州市', 440183, '增城市', 113.83, 23.3), \
        (1944, 440000, '广东省', 440100, '广州市', 440184, '从化市', 113.58, 23.55), \
        (1945, 440000, '广东省', 440200, '韶关市', 440201, '市辖区', 113.6, 24.82), \
        (1946, 440000, '广东省', 440200, '韶关市', 440203, '武江区', 113.57, 24.8), \
        (1947, 440000, '广东省', 440200, '韶关市', 440204, '浈江区', 113.6, 24.8), \
        (1948, 440000, '广东省', 440200, '韶关市', 440205, '曲江区', 113.6, 24.68), \
        (1949, 440000, '广东省', 440200, '韶关市', 440222, '始兴县', 114.07, 24.95), \
        (1950, 440000, '广东省', 440200, '韶关市', 440224, '仁化县', 113.75, 25.08), \
        (1951, 440000, '广东省', 440200, '韶关市', 440229, '翁源县', 114.13, 24.35), \
        (1952, 440000, '广东省', 440200, '韶关市', 440232, '乳源瑶族自治县', 113.27, 24.78), \
        (1953, 440000, '广东省', 440200, '韶关市', 440233, '新丰县', 114.2, 24.07), \
        (1954, 440000, '广东省', 440200, '韶关市', 440281, '乐昌市', 113.35, 25.13), \
        (1955, 440000, '广东省', 440200, '韶关市', 440282, '南雄市', 114.3, 25.12), \
        (1956, 440000, '广东省', 440300, '深圳市', 440301, '市辖区', 114.05, 22.55), \
        (1957, 440000, '广东省', 440300, '深圳市', 440303, '罗湖区', 114.12, 22.55), \
        (1958, 440000, '广东省', 440300, '深圳市', 440304, '福田区', 114.05, 22.53), \
        (1959, 440000, '广东省', 440300, '深圳市', 440305, '南山区', 113.92, 22.52), \
        (1960, 440000, '广东省', 440300, '深圳市', 440306, '宝安区', 113.9, 22.57), \
        (1961, 440000, '广东省', 440300, '深圳市', 440307, '龙岗区', 114.27, 22.73), \
        (1962, 440000, '广东省', 440300, '深圳市', 440308, '盐田区', 114.22, 22.55), \
        (1963, 440000, '广东省', 440400, '珠海市', 440401, '市辖区', 113.57, 22.27), \
        (1964, 440000, '广东省', 440400, '珠海市', 440402, '香洲区', 113.55, 22.27), \
        (1965, 440000, '广东省', 440400, '珠海市', 440403, '斗门区', 113.28, 22.22), \
        (1966, 440000, '广东省', 440400, '珠海市', 440404, '金湾区', 113.4, 22.07), \
        (1967, 440000, '广东省', 440500, '汕头市', 440501, '市辖区', 116.68, 23.35), \
        (1968, 440000, '广东省', 440500, '汕头市', 440507, '龙湖区', 116.72, 23.37), \
        (1969, 440000, '广东省', 440500, '汕头市', 440511, '金平区', 116.7, 23.37), \
        (1970, 440000, '广东省', 440500, '汕头市', 440512, '濠江区', 0, 0), \
        (1971, 440000, '广东省', 440500, '汕头市', 440513, '潮阳区', 116.6, 23.27), \
        (1972, 440000, '广东省', 440500, '汕头市', 440514, '潮南区', 116.43, 23.25), \
        (1973, 440000, '广东省', 440500, '汕头市', 440515, '澄海区', 116.77, 23.48), \
        (1974, 440000, '广东省', 440500, '汕头市', 440523, '南澳县', 117.02, 23.42), \
        (1975, 440000, '广东省', 440600, '佛山市', 440601, '市辖区', 113.12, 23.02), \
        (1976, 440000, '广东省', 440600, '佛山市', 440604, '禅城区', 0, 0), \
        (1977, 440000, '广东省', 440600, '佛山市', 440605, '南海区', 113.15, 23.03), \
        (1978, 440000, '广东省', 440600, '佛山市', 440606, '顺德区', 113.3, 22.8), \
        (1979, 440000, '广东省', 440600, '佛山市', 440607, '三水区', 112.87, 23.17), \
        (1980, 440000, '广东省', 440600, '佛山市', 440608, '高明区', 112.88, 22.9), \
        (1981, 440000, '广东省', 440700, '江门市', 440701, '市辖区', 113.08, 22.58), \
        (1982, 440000, '广东省', 440700, '江门市', 440703, '蓬江区', 0, 0), \
        (1983, 440000, '广东省', 440700, '江门市', 440704, '江海区', 0, 0), \
        (1984, 440000, '广东省', 440700, '江门市', 440705, '新会区', 113.03, 22.47), \
        (1985, 440000, '广东省', 440700, '江门市', 440781, '台山市', 112.78, 22.25), \
        (1986, 440000, '广东省', 440700, '江门市', 440783, '开平市', 112.67, 22.38), \
        (1987, 440000, '广东省', 440700, '江门市', 440784, '鹤山市', 112.97, 22.77), \
        (1988, 440000, '广东省', 440700, '江门市', 440785, '恩平市', 112.3, 22.18), \
        (1989, 440000, '广东省', 440800, '湛江市', 440801, '市辖区', 110.35, 21.27), \
        (1990, 440000, '广东省', 440800, '湛江市', 440802, '赤坎区', 110.37, 21.27), \
        (1991, 440000, '广东省', 440800, '湛江市', 440803, '霞山区', 110.4, 21.2), \
        (1992, 440000, '广东省', 440800, '湛江市', 440804, '坡头区', 110.47, 21.23), \
        (1993, 440000, '广东省', 440800, '湛江市', 440811, '麻章区', 110.32, 21.27), \
        (1994, 440000, '广东省', 440800, '湛江市', 440823, '遂溪县', 110.25, 21.38), \
        (1995, 440000, '广东省', 440800, '湛江市', 440825, '徐闻县', 110.17, 20.33), \
        (1996, 440000, '广东省', 440800, '湛江市', 440881, '廉江市', 110.27, 21.62), \
        (1997, 440000, '广东省', 440800, '湛江市', 440882, '雷州市', 110.08, 20.92), \
        (1998, 440000, '广东省', 440800, '湛江市', 440883, '吴川市', 110.77, 21.43), \
        (1999, 440000, '广东省', 440900, '茂名市', 440901, '市辖区', 110.92, 21.67), \
        (2000, 440000, '广东省', 440900, '茂名市', 440902, '茂南区', 110.92, 21.63), \
        (2001, 440000, '广东省', 440900, '茂名市', 440903, '茂港区', 111.02, 21.47), \
        (2002, 440000, '广东省', 440900, '茂名市', 440923, '电白县', 111, 21.5), \
        (2003, 440000, '广东省', 440900, '茂名市', 440981, '高州市', 110.85, 21.92), \
        (2004, 440000, '广东省', 440900, '茂名市', 440982, '化州市', 110.63, 21.67), \
        (2005, 440000, '广东省', 440900, '茂名市', 440983, '信宜市', 110.95, 22.35), \
        (2006, 440000, '广东省', 441200, '肇庆市', 441201, '市辖区', 112.47, 23.05), \
        (2007, 440000, '广东省', 441200, '肇庆市', 441202, '端州区', 112.48, 23.05), \
        (2008, 440000, '广东省', 441200, '肇庆市', 441203, '鼎湖区', 112.57, 23.17), \
        (2009, 440000, '广东省', 441200, '肇庆市', 441223, '广宁县', 112.43, 23.63), \
        (2010, 440000, '广东省', 441200, '肇庆市', 441224, '怀集县', 112.18, 23.92), \
        (2011, 440000, '广东省', 441200, '肇庆市', 441225, '封开县', 111.5, 23.43), \
        (2012, 440000, '广东省', 441200, '肇庆市', 441226, '德庆县', 111.77, 23.15), \
        (2013, 440000, '广东省', 441200, '肇庆市', 441283, '高要市', 112.45, 23.03), \
        (2014, 440000, '广东省', 441200, '肇庆市', 441284, '四会市', 112.68, 23.33), \
        (2015, 440000, '广东省', 441300, '惠州市', 441301, '市辖区', 114.42, 23.12), \
        (2016, 440000, '广东省', 441300, '惠州市', 441302, '惠城区', 114.4, 23.08), \
        (2017, 440000, '广东省', 441300, '惠州市', 441303, '惠阳区', 114.47, 22.8), \
        (2018, 440000, '广东省', 441300, '惠州市', 441322, '博罗县', 114.28, 23.18), \
        (2019, 440000, '广东省', 441300, '惠州市', 441323, '惠东县', 114.72, 22.98), \
        (2020, 440000, '广东省', 441300, '惠州市', 441324, '龙门县', 114.25, 23.73), \
        (2021, 440000, '广东省', 441400, '梅州市', 441401, '市辖区', 116.12, 24.28), \
        (2022, 440000, '广东省', 441400, '梅州市', 441402, '梅江区', 116.12, 24.32), \
        (2023, 440000, '广东省', 441400, '梅州市', 441421, '梅县', 116.05, 24.28), \
        (2024, 440000, '广东省', 441400, '梅州市', 441422, '大埔县', 116.7, 24.35), \
        (2025, 440000, '广东省', 441400, '梅州市', 441423, '丰顺县', 116.18, 23.77), \
        (2026, 440000, '广东省', 441400, '梅州市', 441424, '五华县', 115.77, 23.93), \
        (2027, 440000, '广东省', 441400, '梅州市', 441426, '平远县', 115.88, 24.57), \
        (2028, 440000, '广东省', 441400, '梅州市', 441427, '蕉岭县', 116.17, 24.67), \
        (2029, 440000, '广东省', 441400, '梅州市', 441481, '兴宁市', 115.73, 24.15), \
        (2030, 440000, '广东省', 441500, '汕尾市', 441501, '市辖区', 115.37, 22.78), \
        (2031, 440000, '广东省', 441500, '汕尾市', 441502, '城区', 0, 0), \
        (2032, 440000, '广东省', 441500, '汕尾市', 441521, '海丰县', 115.33, 22.97), \
        (2033, 440000, '广东省', 441500, '汕尾市', 441523, '陆河县', 115.65, 23.3), \
        (2034, 440000, '广东省', 441500, '汕尾市', 441581, '陆丰市', 115.65, 22.95), \
        (2035, 440000, '广东省', 441600, '河源市', 441601, '市辖区', 114.7, 23.73), \
        (2036, 440000, '广东省', 441600, '河源市', 441602, '源城区', 114.7, 23.73), \
        (2037, 440000, '广东省', 441600, '河源市', 441621, '紫金县', 115.18, 23.63), \
        (2038, 440000, '广东省', 441600, '河源市', 441622, '龙川县', 115.25, 24.1), \
        (2039, 440000, '广东省', 441600, '河源市', 441623, '连平县', 114.48, 24.37), \
        (2040, 440000, '广东省', 441600, '河源市', 441624, '和平县', 114.93, 24.45), \
        (2041, 440000, '广东省', 441600, '河源市', 441625, '东源县', 114.77, 23.82), \
        (2042, 440000, '广东省', 441700, '阳江市', 441701, '市辖区', 111.98, 21.87), \
        (2043, 440000, '广东省', 441700, '阳江市', 441702, '江城区', 111.95, 21.87), \
        (2044, 440000, '广东省', 441700, '阳江市', 441721, '阳西县', 111.62, 21.75), \
        (2045, 440000, '广东省', 441700, '阳江市', 441723, '阳东县', 112.02, 21.88), \
        (2046, 440000, '广东省', 441700, '阳江市', 441781, '阳春市', 111.78, 22.18), \
        (2047, 440000, '广东省', 441800, '清远市', 441801, '市辖区', 113.03, 23.7), \
        (2048, 440000, '广东省', 441800, '清远市', 441802, '清城区', 113.02, 23.7), \
        (2049, 440000, '广东省', 441800, '清远市', 441821, '佛冈县', 113.53, 23.88), \
        (2050, 440000, '广东省', 441800, '清远市', 441823, '阳山县', 112.63, 24.48), \
        (2051, 440000, '广东省', 441800, '清远市', 441825, '连山壮族瑶族自治县', 112.08, 24.57), \
        (2052, 440000, '广东省', 441800, '清远市', 441826, '连南瑶族自治县', 112.28, 24.72), \
        (2053, 440000, '广东省', 441800, '清远市', 441827, '清新县', 112.98, 23.73), \
        (2054, 440000, '广东省', 441800, '清远市', 441881, '英德市', 113.4, 24.18), \
        (2055, 440000, '广东省', 441800, '清远市', 441882, '连州市', 112.38, 24.78), \
        (2056, 440000, '广东', 441900, '广东省', 441900, '东莞市', 113.75, 23.05), \
        (2057, 440000, '广东', 442000, '广东省', 442000, '中山市', 113.38, 22.52), \
        (2058, 440000, '广东省', 445100, '潮州市', 445101, '市辖区', 116.62, 23.67), \
        (2059, 440000, '广东省', 445100, '潮州市', 445102, '湘桥区', 116.63, 23.68), \
        (2060, 440000, '广东省', 445100, '潮州市', 445121, '潮安县', 116.68, 23.45), \
        (2061, 440000, '广东省', 445100, '潮州市', 445122, '饶平县', 117, 23.67), \
        (2062, 440000, '广东省', 445200, '揭阳市', 445201, '市辖区', 116.37, 23.55), \
        (2063, 440000, '广东省', 445200, '揭阳市', 445202, '榕城区', 0, 0), \
        (2064, 440000, '广东省', 445200, '揭阳市', 445221, '揭东县', 116.42, 23.57), \
        (2065, 440000, '广东省', 445200, '揭阳市', 445222, '揭西县', 115.83, 23.43), \
        (2066, 440000, '广东省', 445200, '揭阳市', 445224, '惠来县', 116.28, 23.03), \
        (2067, 440000, '广东省', 445200, '揭阳市', 445281, '普宁市', 116.18, 23.3), \
        (2068, 440000, '广东省', 445300, '云浮市', 445301, '市辖区', 112.03, 22.92), \
        (2069, 440000, '广东省', 445300, '云浮市', 445302, '云城区', 112.03, 22.93), \
        (2070, 440000, '广东省', 445300, '云浮市', 445321, '新兴县', 112.23, 22.7), \
        (2071, 440000, '广东省', 445300, '云浮市', 445322, '郁南县', 111.53, 23.23), \
        (2072, 440000, '广东省', 445300, '云浮市', 445323, '云安县', 112, 23.08), \
        (2073, 440000, '广东省', 445300, '云浮市', 445381, '罗定市', 111.57, 22.77), \
        (2074, 450000, '广西壮', 450100, '南宁市', 450101, '市辖区', 108.37, 22.82), \
        (2075, 450000, '广西壮', 450100, '南宁市', 450102, '兴宁区', 108.38, 22.87), \
        (2076, 450000, '广西壮', 450100, '南宁市', 450103, '青秀区', 0, 0), \
        (2077, 450000, '广西壮', 450100, '南宁市', 450105, '江南区', 108.28, 22.78), \
        (2078, 450000, '广西壮', 450100, '南宁市', 450107, '西乡塘区', 108.3, 22.83), \
        (2079, 450000, '广西壮', 450100, '南宁市', 450108, '良庆区', 108.32, 22.77), \
        (2080, 450000, '广西壮', 450100, '南宁市', 450109, '邕宁区', 108.48, 22.75), \
        (2081, 450000, '广西壮', 450100, '南宁市', 450122, '武鸣县', 108.27, 23.17), \
        (2082, 450000, '广西壮', 450100, '南宁市', 450123, '隆安县', 107.68, 23.18), \
        (2083, 450000, '广西壮', 450100, '南宁市', 450124, '马山县', 108.17, 23.72), \
        (2084, 450000, '广西壮', 450100, '南宁市', 450125, '上林县', 108.6, 23.43), \
        (2085, 450000, '广西壮', 450100, '南宁市', 450126, '宾阳县', 108.8, 23.22), \
        (2086, 450000, '广西壮', 450100, '南宁市', 450127, '横县', 109.27, 22.68), \
        (2087, 450000, '广西壮', 450200, '柳州市', 450201, '市辖区', 109.42, 24.33), \
        (2088, 450000, '广西壮', 450200, '柳州市', 450202, '城中区', 0, 0), \
        (2089, 450000, '广西壮', 450200, '柳州市', 450203, '鱼峰区', 0, 0), \
        (2090, 450000, '广西壮', 450200, '柳州市', 450204, '柳南区', 109.38, 24.35), \
        (2091, 450000, '广西壮', 450200, '柳州市', 450205, '柳北区', 0, 0), \
        (2092, 450000, '广西壮', 450200, '柳州市', 450221, '柳江县', 109.33, 24.27), \
        (2093, 450000, '广西壮', 450200, '柳州市', 450222, '柳城县', 109.23, 24.65), \
        (2094, 450000, '广西壮', 450200, '柳州市', 450223, '鹿寨县', 109.73, 24.48), \
        (2095, 450000, '广西壮', 450200, '柳州市', 450224, '融安县', 109.4, 25.23), \
        (2096, 450000, '广西壮', 450200, '柳州市', 450225, '融水苗族自治县', 109.25, 25.07), \
        (2097, 450000, '广西壮', 450200, '柳州市', 450226, '三江侗族自治县', 109.6, 25.78), \
        (2098, 450000, '广西壮', 450300, '桂林市', 450301, '市辖区', 110.28, 25.28), \
        (2099, 450000, '广西壮', 450300, '桂林市', 450302, '秀峰区', 0, 0), \
        (2100, 450000, '广西壮', 450300, '桂林市', 450303, '叠彩区', 0, 0), \
        (2101, 450000, '广西壮', 450300, '桂林市', 450304, '象山区', 0, 0), \
        (2102, 450000, '广西壮', 450300, '桂林市', 450305, '七星区', 0, 0), \
        (2103, 450000, '广西壮', 450300, '桂林市', 450311, '雁山区', 0, 0), \
        (2104, 450000, '广西壮', 450300, '桂林市', 450321, '阳朔县', 110.48, 24.78), \
        (2105, 450000, '广西壮', 450300, '桂林市', 450322, '临桂县', 110.2, 25.23), \
        (2106, 450000, '广西壮', 450300, '桂林市', 450323, '灵川县', 110.32, 25.42), \
        (2107, 450000, '广西壮', 450300, '桂林市', 450324, '全州县', 111.07, 25.93), \
        (2108, 450000, '广西壮', 450300, '桂林市', 450325, '兴安县', 110.67, 25.62), \
        (2109, 450000, '广西壮', 450300, '桂林市', 450326, '永福县', 109.98, 24.98), \
        (2110, 450000, '广西壮', 450300, '桂林市', 450327, '灌阳县', 111.15, 25.48), \
        (2111, 450000, '广西壮', 450300, '桂林市', 450328, '龙胜各族自治县', 110, 25.8), \
        (2112, 450000, '广西壮', 450300, '桂林市', 450329, '资源县', 110.63, 26.03), \
        (2113, 450000, '广西壮', 450300, '桂林市', 450330, '平乐县', 110.63, 24.63), \
        (2114, 450000, '广西壮', 450300, '桂林市', 450331, '荔蒲县', 0, 0), \
        (2115, 450000, '广西壮', 450300, '桂林市', 450332, '恭城瑶族自治县', 110.83, 24.83), \
        (2116, 450000, '广西壮', 450400, '梧州市', 450401, '市辖区', 111.27, 23.48), \
        (2117, 450000, '广西壮', 450400, '梧州市', 450403, '万秀区', 0, 0), \
        (2118, 450000, '广西壮', 450400, '梧州市', 450404, '蝶山区', 0, 0), \
        (2119, 450000, '广西壮', 450400, '梧州市', 450405, '长洲区', 0, 0), \
        (2120, 450000, '广西壮', 450400, '梧州市', 450421, '苍梧县', 111.23, 23.42), \
        (2121, 450000, '广西壮', 450400, '梧州市', 450422, '藤县', 110.92, 23.38), \
        (2122, 450000, '广西壮', 450400, '梧州市', 450423, '蒙山县', 110.52, 24.2), \
        (2123, 450000, '广西壮', 450400, '梧州市', 450481, '岑溪市', 110.98, 22.92), \
        (2124, 450000, '广西壮', 450500, '北海市', 450501, '市辖区', 109.12, 21.48), \
        (2125, 450000, '广西壮', 450500, '北海市', 450502, '海城区', 0, 0), \
        (2126, 450000, '广西壮', 450500, '北海市', 450503, '银海区', 0, 0), \
        (2127, 450000, '广西壮', 450500, '北海市', 450512, '铁山港区', 109.43, 21.53), \
        (2128, 450000, '广西壮', 450500, '北海市', 450521, '合浦县', 109.2, 21.67), \
        (2129, 450000, '广西壮', 450600, '防城港市', 450601, '市辖区', 108.35, 21.7), \
        (2130, 450000, '广西壮', 450600, '防城港市', 450602, '港口区', 108.37, 21.65), \
        (2131, 450000, '广西壮', 450600, '防城港市', 450603, '防城区', 108.35, 21.77), \
        (2132, 450000, '广西壮', 450600, '防城港市', 450621, '上思县', 107.98, 22.15), \
        (2133, 450000, '广西壮', 450600, '防城港市', 450681, '东兴市', 107.97, 21.53), \
        (2134, 450000, '广西壮', 450700, '钦州市', 450701, '市辖区', 108.62, 21.95), \
        (2135, 450000, '广西壮', 450700, '钦州市', 450702, '钦南区', 0, 0), \
        (2136, 450000, '广西壮', 450700, '钦州市', 450703, '钦北区', 108.63, 21.98), \
        (2137, 450000, '广西壮', 450700, '钦州市', 450721, '灵山县', 109.3, 22.43), \
        (2138, 450000, '广西壮', 450700, '钦州市', 450722, '浦北县', 109.55, 22.27), \
        (2139, 450000, '广西壮', 450800, '贵港市', 450801, '市辖区', 109.6, 23.1), \
        (2140, 450000, '广西壮', 450800, '贵港市', 450802, '港北区', 0, 0), \
        (2141, 450000, '广西壮', 450800, '贵港市', 450803, '港南区', 0, 0), \
        (2142, 450000, '广西壮', 450800, '贵港市', 450804, '覃塘区', 109.42, 23.13), \
        (2143, 450000, '广西壮', 450800, '贵港市', 450821, '平南县', 110.38, 23.55), \
        (2144, 450000, '广西壮', 450800, '贵港市', 450881, '桂平市', 110.08, 23.4), \
        (2145, 450000, '广西壮', 450900, '玉林市', 450901, '市辖区', 110.17, 22.63), \
        (2146, 450000, '广西壮', 450900, '玉林市', 450902, '玉州区', 0, 0), \
        (2147, 450000, '广西壮', 450900, '玉林市', 450921, '容县', 110.55, 22.87), \
        (2148, 450000, '广西壮', 450900, '玉林市', 450922, '陆川县', 110.27, 22.33), \
        (2149, 450000, '广西壮', 450900, '玉林市', 450923, '博白县', 109.97, 22.28), \
        (2150, 450000, '广西壮', 450900, '玉林市', 450924, '兴业县', 109.87, 22.75), \
        (2151, 450000, '广西壮', 450900, '玉林市', 450981, '北流市', 110.35, 22.72), \
        (2152, 450000, '广西壮', 451000, '百色市', 451001, '市辖区', 106.62, 23.9), \
        (2153, 450000, '广西壮', 451000, '百色市', 451002, '右江区', 0, 0), \
        (2154, 450000, '广西壮', 451000, '百色市', 451021, '田阳县', 106.92, 23.73), \
        (2155, 450000, '广西壮', 451000, '百色市', 451022, '田东县', 107.12, 23.6), \
        (2156, 450000, '广西壮', 451000, '百色市', 451023, '平果县', 107.58, 23.32), \
        (2157, 450000, '广西壮', 451000, '百色市', 451024, '德保县', 106.62, 23.33), \
        (2158, 450000, '广西壮', 451000, '百色市', 451025, '靖西县', 106.42, 23.13), \
        (2159, 450000, '广西壮', 451000, '百色市', 451026, '那坡县', 105.83, 23.42), \
        (2160, 450000, '广西壮', 451000, '百色市', 451027, '凌云县', 106.57, 24.35), \
        (2161, 450000, '广西壮', 451000, '百色市', 451028, '乐业县', 106.55, 24.78), \
        (2162, 450000, '广西壮', 451000, '百色市', 451029, '田林县', 106.23, 24.3), \
        (2163, 450000, '广西壮', 451000, '百色市', 451030, '西林县', 105.1, 24.5), \
        (2164, 450000, '广西壮', 451000, '百色市', 451031, '隆林各族自治县', 105.33, 24.77), \
        (2165, 450000, '广西壮', 451100, '贺州市', 451101, '市辖区', 111.55, 24.42), \
        (2166, 450000, '广西壮', 451100, '贺州市', 451102, '八步区', 0, 0), \
        (2167, 450000, '广西壮', 451100, '贺州市', 451121, '昭平县', 110.8, 24.17), \
        (2168, 450000, '广西壮', 451100, '贺州市', 451122, '钟山县', 111.3, 24.53), \
        (2169, 450000, '广西壮', 451100, '贺州市', 451123, '富川瑶族自治县', 111.27, 24.83), \
        (2170, 450000, '广西壮', 451200, '河池市', 451201, '市辖区', 108.07, 24.7), \
        (2171, 450000, '广西壮', 451200, '河池市', 451202, '金城江区', 108.05, 24.7), \
        (2172, 450000, '广西壮', 451200, '河池市', 451221, '南丹县', 107.53, 24.98), \
        (2173, 450000, '广西壮', 451200, '河池市', 451222, '天峨县', 107.17, 25), \
        (2174, 450000, '广西壮', 451200, '河池市', 451223, '凤山县', 107.05, 24.55), \
        (2175, 450000, '广西壮', 451200, '河池市', 451224, '东兰县', 107.37, 24.52), \
        (2176, 450000, '广西壮', 451200, '河池市', 451225, '罗城仫佬族自治县', 108.9, 24.78), \
        (2177, 450000, '广西壮', 451200, '河池市', 451226, '环江毛南族自治县', 108.25, 24.83), \
        (2178, 450000, '广西壮', 451200, '河池市', 451227, '巴马瑶族自治县', 107.25, 24.15), \
        (2179, 450000, '广西壮', 451200, '河池市', 451228, '都安瑶族自治县', 108.1, 23.93), \
        (2180, 450000, '广西壮', 451200, '河池市', 451229, '大化瑶族自治县', 107.98, 23.73), \
        (2181, 450000, '广西壮', 451200, '河池市', 451281, '宜州市', 108.67, 24.5), \
        (2182, 450000, '广西壮', 451300, '来宾市', 451301, '市辖区', 109.23, 23.73), \
        (2183, 450000, '广西壮', 451300, '来宾市', 451302, '兴宾区', 0, 0), \
        (2184, 450000, '广西壮', 451300, '来宾市', 451321, '忻城县', 108.67, 24.07), \
        (2185, 450000, '广西壮', 451300, '来宾市', 451322, '象州县', 109.68, 23.97), \
        (2186, 450000, '广西壮', 451300, '来宾市', 451323, '武宣县', 109.67, 23.6), \
        (2187, 450000, '广西壮', 451300, '来宾市', 451324, '金秀瑶族自治县', 110.18, 24.13), \
        (2188, 450000, '广西壮', 451300, '来宾市', 451381, '合山市', 108.87, 23.82), \
        (2189, 450000, '广西壮', 451400, '崇左市', 451401, '市辖区', 107.37, 22.4), \
        (2190, 450000, '广西壮', 451400, '崇左市', 451402, '江洲区', 0, 0), \
        (2191, 450000, '广西壮', 451400, '崇左市', 451421, '扶绥县', 107.9, 22.63), \
        (2192, 450000, '广西壮', 451400, '崇左市', 451422, '宁明县', 107.07, 22.13), \
        (2193, 450000, '广西壮', 451400, '崇左市', 451423, '龙州县', 106.85, 22.35), \
        (2194, 450000, '广西壮', 451400, '崇左市', 451424, '大新县', 107.2, 22.83), \
        (2195, 450000, '广西壮', 451400, '崇左市', 451425, '天等县', 107.13, 23.08), \
        (2196, 450000, '广西壮', 451400, '崇左市', 451481, '凭祥市', 106.75, 22.12), \
        (2197, 460000, '海南省', 460100, '海口市', 460101, '市辖区', 110.32, 20.03), \
        (2198, 460000, '海南省', 460100, '海口市', 460105, '秀英区', 110.28, 20.02), \
        (2199, 460000, '海南省', 460100, '海口市', 460106, '龙华区', 110.3, 20.03), \
        (2200, 460000, '海南省', 460100, '海口市', 460107, '琼山区', 110.35, 20), \
        (2201, 460000, '海南省', 460100, '海口市', 460108, '美兰区', 110.37, 20.03), \
        (2202, 460000, '海南省', 460200, '三亚市', 460201, '市辖区', 109.5, 18.25), \
        (2203, 460000, '海南省', 469000, '省直辖县级行政单位', 469001, '五指山市', 0, 0), \
        (2204, 460000, '海南省', 469000, '省直辖县级行政单位', 469002, '琼海市', 0, 0), \
        (2205, 460000, '海南省', 469000, '省直辖县级行政单位', 469003, '儋州市', 0, 0), \
        (2206, 460000, '海南省', 469000, '省直辖县级行政单位', 469005, '文昌市', 0, 0), \
        (2207, 460000, '海南省', 469000, '省直辖县级行政单位', 469006, '万宁市', 0, 0), \
        (2208, 460000, '海南省', 469000, '省直辖县级行政单位', 469007, '东方市', 0, 0), \
        (2209, 460000, '海南省', 469000, '省直辖县级行政单位', 469025, '定安县', 0, 0), \
        (2210, 460000, '海南省', 469000, '省直辖县级行政单位', 469026, '屯昌县', 0, 0), \
        (2211, 460000, '海南省', 469000, '省直辖县级行政单位', 469027, '澄迈县', 0, 0), \
        (2212, 460000, '海南省', 469000, '省直辖县级行政单位', 469028, '临高县', 0, 0), \
        (2213, 460000, '海南省', 469000, '省直辖县级行政单位', 469030, '白沙黎族自治县', 0, 0), \
        (2214, 460000, '海南省', 469000, '省直辖县级行政单位', 469031, '昌江黎族自治县', 0, 0), \
        (2215, 460000, '海南省', 469000, '省直辖县级行政单位', 469033, '乐东黎族自治县', 0, 0), \
        (2216, 460000, '海南省', 469000, '省直辖县级行政单位', 469034, '陵水黎族自治县', 0, 0), \
        (2217, 460000, '海南省', 469000, '省直辖县级行政单位', 469035, '保亭黎族苗族自治县', 0, 0), \
        (2218, 460000, '海南省', 469000, '省直辖县级行政单位', 469036, '琼中黎族苗族自治县', 0, 0), \
        (2219, 460000, '海南省', 469000, '省直辖县级行政单位', 469037, '西沙群岛', 0, 0), \
        (2220, 460000, '海南省', 469000, '省直辖县级行政单位', 469038, '南沙群岛', 0, 0), \
        (2221, 460000, '海南省', 469000, '省直辖县级行政单位', 469039, '中沙群岛的岛礁及其海域', 0, 0), \
        (2222, 500000, '重庆市', 500100, '市辖区', 500101, '万州区', 108.4, 30.82), \
        (2223, 500000, '重庆市', 500100, '市辖区', 500102, '涪陵区', 107.4, 29.72), \
        (2224, 500000, '重庆市', 500100, '市辖区', 500103, '渝中区', 106.57, 29.55), \
        (2225, 500000, '重庆市', 500100, '市辖区', 500104, '大渡口区', 106.48, 29.48), \
        (2226, 500000, '重庆市', 500100, '市辖区', 500105, '江北区', 106.57, 29.6), \
        (2227, 500000, '重庆市', 500100, '市辖区', 500106, '沙坪坝区', 106.45, 29.53), \
        (2228, 500000, '重庆市', 500100, '市辖区', 500107, '九龙坡区', 106.5, 29.5), \
        (2229, 500000, '重庆市', 500100, '市辖区', 500108, '南岸区', 106.57, 29.52), \
        (2230, 500000, '重庆市', 500100, '市辖区', 500109, '北碚区', 106.4, 29.8), \
        (2231, 500000, '重庆市', 500100, '市辖区', 500110, '万盛区', 106.92, 28.97), \
        (2232, 500000, '重庆市', 500100, '市辖区', 500111, '双桥区', 105.78, 29.48), \
        (2233, 500000, '重庆市', 500100, '市辖区', 500112, '渝北区', 106.63, 29.72), \
        (2234, 500000, '重庆市', 500100, '市辖区', 500113, '巴南区', 106.52, 29.38), \
        (2235, 500000, '重庆市', 500100, '市辖区', 500114, '黔江区', 108.77, 29.53), \
        (2236, 500000, '重庆市', 500100, '市辖区', 500115, '长寿区', 107.08, 29.87), \
        (2237, 500000, '重庆市', 500100, '市辖区', 500116, '江津区', 0, 0), \
        (2238, 500000, '重庆市', 500100, '市辖区', 500117, '合川区', 0, 0), \
        (2239, 500000, '重庆市', 500100, '市辖区', 500118, '永川区', 0, 0), \
        (2240, 500000, '重庆市', 500100, '市辖区', 500119, '南川区', 0, 0), \
        (2241, 500000, '重庆市', 500200, '县', 500222, '綦江县', 106.65, 29.03), \
        (2242, 500000, '重庆市', 500200, '县', 500223, '潼南县', 105.83, 30.18), \
        (2243, 500000, '重庆市', 500200, '县', 500224, '铜梁县', 106.05, 29.85), \
        (2244, 500000, '重庆市', 500200, '县', 500225, '大足县', 105.72, 29.7), \
        (2245, 500000, '重庆市', 500200, '县', 500226, '荣昌县', 105.58, 29.4), \
        (2246, 500000, '重庆市', 500200, '县', 500227, '璧山县', 106.22, 29.6), \
        (2247, 500000, '重庆市', 500200, '县', 500228, '梁平县', 107.8, 30.68), \
        (2248, 500000, '重庆市', 500200, '县', 500229, '城口县', 108.67, 31.95), \
        (2249, 500000, '重庆市', 500200, '县', 500230, '丰都县', 107.73, 29.87), \
        (2250, 500000, '重庆市', 500200, '县', 500231, '垫江县', 107.35, 30.33), \
        (2251, 500000, '重庆市', 500200, '县', 500232, '武隆县', 107.75, 29.33), \
        (2252, 500000, '重庆市', 500200, '县', 500233, '忠县', 108.02, 30.3), \
        (2253, 500000, '重庆市', 500200, '县', 500234, '开县', 108.42, 31.18), \
        (2254, 500000, '重庆市', 500200, '县', 500235, '云阳县', 108.67, 30.95), \
        (2255, 500000, '重庆市', 500200, '县', 500236, '奉节县', 109.47, 31.02), \
        (2256, 500000, '重庆市', 500200, '县', 500237, '巫山县', 109.88, 31.08), \
        (2257, 500000, '重庆市', 500200, '县', 500238, '巫溪县', 109.63, 31.4), \
        (2258, 500000, '重庆市', 500200, '县', 500240, '石柱土家族自治县', 108.12, 30), \
        (2259, 500000, '重庆市', 500200, '县', 500241, '秀山土家族苗族自治县', 108.98, 28.45), \
        (2260, 500000, '重庆市', 500200, '县', 500242, '酉阳土家族苗族自治县', 108.77, 28.85), \
        (2261, 500000, '重庆市', 500200, '县', 500243, '彭水苗族土家族自治县', 108.17, 29.3), \
        (2262, 510000, '四川省', 510100, '成都市', 510101, '市辖区', 104.07, 30.67), \
        (2263, 510000, '四川省', 510100, '成都市', 510104, '锦江区', 104.08, 30.67), \
        (2264, 510000, '四川省', 510100, '成都市', 510105, '青羊区', 104.05, 30.68), \
        (2265, 510000, '四川省', 510100, '成都市', 510106, '金牛区', 104.05, 30.7), \
        (2266, 510000, '四川省', 510100, '成都市', 510107, '武侯区', 104.05, 30.65), \
        (2267, 510000, '四川省', 510100, '成都市', 510108, '成华区', 104.1, 30.67), \
        (2268, 510000, '四川省', 510100, '成都市', 510112, '龙泉驿区', 104.27, 30.57), \
        (2269, 510000, '四川省', 510100, '成都市', 510113, '青白江区', 104.23, 30.88), \
        (2270, 510000, '四川省', 510100, '成都市', 510114, '新都区', 104.15, 30.83), \
        (2271, 510000, '四川省', 510100, '成都市', 510115, '温江区', 103.83, 30.7), \
        (2272, 510000, '四川省', 510100, '成都市', 510121, '金堂县', 104.43, 30.85), \
        (2273, 510000, '四川省', 510100, '成都市', 510122, '双流县', 103.92, 30.58), \
        (2274, 510000, '四川省', 510100, '成都市', 510124, '郫县', 103.88, 30.82), \
        (2275, 510000, '四川省', 510100, '成都市', 510129, '大邑县', 103.52, 30.58), \
        (2276, 510000, '四川省', 510100, '成都市', 510131, '蒲江县', 103.5, 30.2), \
        (2277, 510000, '四川省', 510100, '成都市', 510132, '新津县', 103.82, 30.42), \
        (2278, 510000, '四川省', 510100, '成都市', 510181, '都江堰市', 103.62, 31), \
        (2279, 510000, '四川省', 510100, '成都市', 510182, '彭州市', 103.93, 30.98), \
        (2280, 510000, '四川省', 510100, '成都市', 510183, '邛崃市', 103.47, 30.42), \
        (2281, 510000, '四川省', 510100, '成都市', 510184, '崇州市', 103.67, 30.63), \
        (2282, 510000, '四川省', 510300, '自贡市', 510301, '市辖区', 104.78, 29.35), \
        (2283, 510000, '四川省', 510300, '自贡市', 510302, '自流井区', 104.77, 29.35), \
        (2284, 510000, '四川省', 510300, '自贡市', 510303, '贡井区', 104.72, 29.35), \
        (2285, 510000, '四川省', 510300, '自贡市', 510304, '大安区', 104.77, 29.37), \
        (2286, 510000, '四川省', 510300, '自贡市', 510311, '沿滩区', 104.87, 29.27), \
        (2287, 510000, '四川省', 510300, '自贡市', 510321, '荣县', 104.42, 29.47), \
        (2288, 510000, '四川省', 510300, '自贡市', 510322, '富顺县', 104.98, 29.18), \
        (2289, 510000, '四川省', 510400, '攀枝花市', 510401, '市辖区', 101.72, 26.58), \
        (2290, 510000, '四川省', 510400, '攀枝花市', 510402, '东区', 101.7, 26.55), \
        (2291, 510000, '四川省', 510400, '攀枝花市', 510403, '西区', 101.6, 26.6), \
        (2292, 510000, '四川省', 510400, '攀枝花市', 510411, '仁和区', 101.73, 26.5), \
        (2293, 510000, '四川省', 510400, '攀枝花市', 510421, '米易县', 102.12, 26.88), \
        (2294, 510000, '四川省', 510400, '攀枝花市', 510422, '盐边县', 101.85, 26.7), \
        (2295, 510000, '四川省', 510500, '泸州市', 510501, '市辖区', 105.43, 28.87), \
        (2296, 510000, '四川省', 510500, '泸州市', 510502, '江阳区', 105.45, 28.88), \
        (2297, 510000, '四川省', 510500, '泸州市', 510503, '纳溪区', 105.37, 28.77), \
        (2298, 510000, '四川省', 510500, '泸州市', 510504, '龙马潭区', 105.43, 28.9), \
        (2299, 510000, '四川省', 510500, '泸州市', 510521, '泸县', 105.38, 29.15), \
        (2300, 510000, '四川省', 510500, '泸州市', 510522, '合江县', 105.83, 28.82), \
        (2301, 510000, '四川省', 510500, '泸州市', 510524, '叙永县', 105.43, 28.17), \
        (2302, 510000, '四川省', 510500, '泸州市', 510525, '古蔺县', 105.82, 28.05), \
        (2303, 510000, '四川省', 510600, '德阳市', 510601, '市辖区', 104.38, 31.13), \
        (2304, 510000, '四川省', 510600, '德阳市', 510603, '旌阳区', 104.38, 31.13), \
        (2305, 510000, '四川省', 510600, '德阳市', 510623, '中江县', 104.68, 31.03), \
        (2306, 510000, '四川省', 510600, '德阳市', 510626, '罗江县', 104.5, 31.32), \
        (2307, 510000, '四川省', 510600, '德阳市', 510681, '广汉市', 104.28, 30.98), \
        (2308, 510000, '四川省', 510600, '德阳市', 510682, '什邡市', 104.17, 31.13), \
        (2309, 510000, '四川省', 510600, '德阳市', 510683, '绵竹市', 104.2, 31.35), \
        (2310, 510000, '四川省', 510700, '绵阳市', 510701, '市辖区', 104.73, 31.47), \
        (2311, 510000, '四川省', 510700, '绵阳市', 510703, '涪城区', 104.73, 31.47), \
        (2312, 510000, '四川省', 510700, '绵阳市', 510704, '游仙区', 104.75, 31.47), \
        (2313, 510000, '四川省', 510700, '绵阳市', 510722, '三台县', 105.08, 31.1), \
        (2314, 510000, '四川省', 510700, '绵阳市', 510723, '盐亭县', 105.38, 31.22), \
        (2315, 510000, '四川省', 510700, '绵阳市', 510724, '安县', 104.57, 31.53), \
        (2316, 510000, '四川省', 510700, '绵阳市', 510725, '梓潼县', 105.17, 31.63), \
        (2317, 510000, '四川省', 510700, '绵阳市', 510726, '北川羌族自治县', 104.45, 31.82), \
        (2318, 510000, '四川省', 510700, '绵阳市', 510727, '平武县', 104.53, 32.42), \
        (2319, 510000, '四川省', 510700, '绵阳市', 510781, '江油市', 104.75, 31.78), \
        (2320, 510000, '四川省', 510800, '广元市', 510801, '市辖区', 105.83, 32.43), \
        (2321, 510000, '四川省', 510800, '广元市', 510802, '市中区', 103.77, 29.57), \
        (2322, 510000, '四川省', 510800, '广元市', 510811, '元坝区', 105.97, 32.32), \
        (2323, 510000, '四川省', 510800, '广元市', 510812, '朝天区', 105.88, 32.65), \
        (2324, 510000, '四川省', 510800, '广元市', 510821, '旺苍县', 106.28, 32.23), \
        (2325, 510000, '四川省', 510800, '广元市', 510822, '青川县', 105.23, 32.58), \
        (2326, 510000, '四川省', 510800, '广元市', 510823, '剑阁县', 105.52, 32.28), \
        (2327, 510000, '四川省', 510800, '广元市', 510824, '苍溪县', 105.93, 31.73), \
        (2328, 510000, '四川省', 510900, '遂宁市', 510901, '市辖区', 105.57, 30.52), \
        (2329, 510000, '四川省', 510900, '遂宁市', 510903, '船山区', 105.57, 30.52), \
        (2330, 510000, '四川省', 510900, '遂宁市', 510904, '安居区', 105.45, 30.35), \
        (2331, 510000, '四川省', 510900, '遂宁市', 510921, '蓬溪县', 105.72, 30.78), \
        (2332, 510000, '四川省', 510900, '遂宁市', 510922, '射洪县', 105.38, 30.87), \
        (2333, 510000, '四川省', 510900, '遂宁市', 510923, '大英县', 105.25, 30.58), \
        (2334, 510000, '四川省', 511000, '内江市', 511001, '市辖区', 105.05, 29.58), \
        (2335, 510000, '四川省', 511000, '内江市', 511002, '市中区', 103.77, 29.57), \
        (2336, 510000, '四川省', 511000, '内江市', 511011, '东兴区', 105.07, 29.6), \
        (2337, 510000, '四川省', 511000, '内江市', 511024, '威远县', 104.67, 29.53), \
        (2338, 510000, '四川省', 511000, '内江市', 511025, '资中县', 104.85, 29.78), \
        (2339, 510000, '四川省', 511000, '内江市', 511028, '隆昌县', 0, 0), \
        (2340, 510000, '四川省', 511100, '乐山市', 511101, '市辖区', 103.77, 29.57), \
        (2341, 510000, '四川省', 511100, '乐山市', 511102, '市中区', 103.77, 29.57), \
        (2342, 510000, '四川省', 511100, '乐山市', 511111, '沙湾区', 103.55, 29.42), \
        (2343, 510000, '四川省', 511100, '乐山市', 511112, '五通桥区', 103.82, 29.4), \
        (2344, 510000, '四川省', 511100, '乐山市', 511113, '金口河区', 103.08, 29.25), \
        (2345, 510000, '四川省', 511100, '乐山市', 511123, '犍为县', 103.95, 29.22), \
        (2346, 510000, '四川省', 511100, '乐山市', 511124, '井研县', 104.07, 29.65), \
        (2347, 510000, '四川省', 511100, '乐山市', 511126, '夹江县', 103.57, 29.73), \
        (2348, 510000, '四川省', 511100, '乐山市', 511129, '沐川县', 103.9, 28.97), \
        (2349, 510000, '四川省', 511100, '乐山市', 511132, '峨边彝族自治县', 103.27, 29.23), \
        (2350, 510000, '四川省', 511100, '乐山市', 511133, '马边彝族自治县', 103.55, 28.83), \
        (2351, 510000, '四川省', 511100, '乐山市', 511181, '峨眉山市', 103.48, 29.6), \
        (2352, 510000, '四川省', 511300, '南充市', 511301, '市辖区', 106.08, 30.78), \
        (2353, 510000, '四川省', 511300, '南充市', 511302, '顺庆区', 106.08, 30.78), \
        (2354, 510000, '四川省', 511300, '南充市', 511303, '高坪区', 106.1, 30.77), \
        (2355, 510000, '四川省', 511300, '南充市', 511304, '嘉陵区', 106.05, 30.77), \
        (2356, 510000, '四川省', 511300, '南充市', 511321, '南部县', 106.07, 31.35), \
        (2357, 510000, '四川省', 511300, '南充市', 511322, '营山县', 106.57, 31.08), \
        (2358, 510000, '四川省', 511300, '南充市', 511323, '蓬安县', 106.42, 31.03), \
        (2359, 510000, '四川省', 511300, '南充市', 511324, '仪陇县', 106.28, 31.27), \
        (2360, 510000, '四川省', 511300, '南充市', 511325, '西充县', 105.88, 31), \
        (2361, 510000, '四川省', 511300, '南充市', 511381, '阆中市', 106, 31.55), \
        (2362, 510000, '四川省', 511400, '眉山市', 511401, '市辖区', 103.83, 30.05), \
        (2363, 510000, '四川省', 511400, '眉山市', 511402, '东坡区', 103.83, 30.05), \
        (2364, 510000, '四川省', 511400, '眉山市', 511421, '仁寿县', 104.15, 30), \
        (2365, 510000, '四川省', 511400, '眉山市', 511422, '彭山县', 103.87, 30.2), \
        (2366, 510000, '四川省', 511400, '眉山市', 511423, '洪雅县', 103.37, 29.92), \
        (2367, 510000, '四川省', 511400, '眉山市', 511424, '丹棱县', 103.52, 30.02), \
        (2368, 510000, '四川省', 511400, '眉山市', 511425, '青神县', 103.85, 29.83), \
        (2369, 510000, '四川省', 511500, '宜宾市', 511501, '市辖区', 104.62, 28.77), \
        (2370, 510000, '四川省', 511500, '宜宾市', 511502, '翠屏区', 104.62, 28.77), \
        (2371, 510000, '四川省', 511500, '宜宾市', 511521, '宜宾县', 104.55, 28.7), \
        (2372, 510000, '四川省', 511500, '宜宾市', 511522, '南溪县', 104.98, 28.85),
        (2373, 510000, '四川省', 511500, '宜宾市', 511523, '江安县', 105.07, 28.73), \
        (2374, 510000, '四川省', 511500, '宜宾市', 511524, '长宁县', 104.92, 28.58), \
        (2375, 510000, '四川省', 511500, '宜宾市', 511525, '高县', 104.52, 28.43), \
        (2376, 510000, '四川省', 511500, '宜宾市', 511526, '珙县', 104.72, 28.45), \
        (2377, 510000, '四川省', 511500, '宜宾市', 511527, '筠连县', 104.52, 28.17), \
        (2378, 510000, '四川省', 511500, '宜宾市', 511528, '兴文县', 105.23, 28.3), \
        (2379, 510000, '四川省', 511500, '宜宾市', 511529, '屏山县', 104.33, 28.83), \
        (2380, 510000, '四川省', 511600, '广安市', 511601, '市辖区', 106.63, 30.47), \
        (2381, 510000, '四川省', 511600, '广安市', 511602, '广安区', 0, 0), \
        (2382, 510000, '四川省', 511600, '广安市', 511621, '岳池县', 106.43, 30.55), \
        (2383, 510000, '四川省', 511600, '广安市', 511622, '武胜县', 106.28, 30.35), \
        (2384, 510000, '四川省', 511600, '广安市', 511623, '邻水县', 106.93, 30.33), \
        (2385, 510000, '四川省', 511600, '广安市', 511681, '华蓥市', 106.77, 30.38), \
        (2386, 510000, '四川省', 511700, '达州市', 511701, '市辖区', 107.5, 31.22), \
        (2387, 510000, '四川省', 511700, '达州市', 511702, '通川区', 107.48, 31.22), \
        (2388, 510000, '四川省', 511700, '达州市', 511721, '达县', 107.5, 31.2), \
        (2389, 510000, '四川省', 511700, '达州市', 511722, '宣汉县', 107.72, 31.35), \
        (2390, 510000, '四川省', 511700, '达州市', 511723, '开江县', 107.87, 31.08), \
        (2391, 510000, '四川省', 511700, '达州市', 511724, '大竹县', 107.2, 30.73), \
        (2392, 510000, '四川省', 511700, '达州市', 511725, '渠县', 106.97, 30.83), \
        (2393, 510000, '四川省', 511700, '达州市', 511781, '万源市', 108.03, 32.07), \
        (2394, 510000, '四川省', 511800, '雅安市', 511801, '市辖区', 103, 29.98), \
        (2395, 510000, '四川省', 511800, '雅安市', 511802, '雨城区', 103, 29.98), \
        (2396, 510000, '四川省', 511800, '雅安市', 511821, '名山县', 103.12, 30.08), \
        (2397, 510000, '四川省', 511800, '雅安市', 511822, '荥经县', 102.85, 29.8), \
        (2398, 510000, '四川省', 511800, '雅安市', 511823, '汉源县', 102.65, 29.35), \
        (2399, 510000, '四川省', 511800, '雅安市', 511824, '石棉县', 102.37, 29.23), \
        (2400, 510000, '四川省', 511800, '雅安市', 511825, '天全县', 102.75, 30.07), \
        (2401, 510000, '四川省', 511800, '雅安市', 511826, '芦山县', 102.92, 30.15), \
        (2402, 510000, '四川省', 511800, '雅安市', 511827, '宝兴县', 102.82, 30.37), \
        (2403, 510000, '四川省', 511900, '巴中市', 511901, '市辖区', 106.77, 31.85), \
        (2404, 510000, '四川省', 511900, '巴中市', 511902, '巴州区', 106.77, 31.85), \
        (2405, 510000, '四川省', 511900, '巴中市', 511921, '通江县', 107.23, 31.92), \
        (2406, 510000, '四川省', 511900, '巴中市', 511922, '南江县', 106.83, 32.35), \
        (2407, 510000, '四川省', 511900, '巴中市', 511923, '平昌县', 107.1, 31.57), \
        (2408, 510000, '四川省', 512000, '资阳市', 512001, '市辖区', 104.65, 30.12), \
        (2409, 510000, '四川省', 512000, '资阳市', 512002, '雁江区', 104.65, 30.12), \
        (2410, 510000, '四川省', 512000, '资阳市', 512021, '安岳县', 105.33, 30.1), \
        (2411, 510000, '四川省', 512000, '资阳市', 512022, '乐至县', 105.02, 30.28), \
        (2412, 510000, '四川省', 512000, '资阳市', 512081, '简阳市', 104.55, 30.4), \
        (2413, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513221, '汶川县', 103.58, 31.48), \
        (2414, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513222, '理县', 103.17, 31.43), \
        (2415, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513223, '茂县', 103.85, 31.68), \
        (2416, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513224, '松潘县', 103.6, 32.63), \
        (2417, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513225, '九寨沟县', 104.23, 33.27), \
        (2418, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513226, '金川县', 102.07, 31.48), \
        (2419, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513227, '小金县', 102.37, 31), \
        (2420, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513228, '黑水县', 102.98, 32.07), \
        (2421, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513229, '马尔康县', 102.22, 31.9), \
        (2422, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513230, '壤塘县', 100.98, 32.27), \
        (2423, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513231, '阿坝县', 101.7, 32.9), \
        (2424, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513232, '若尔盖县', 102.95, 33.58), \
        (2425, 510000, '四川省', 513200, '阿坝藏族羌族自治州', 513233, '红原县', 102.55, 32.8), \
        (2426, 510000, '四川省', 513300, '甘孜藏族自治州', 513321, '康定县', 101.97, 30.05), \
        (2427, 510000, '四川省', 513300, '甘孜藏族自治州', 513322, '泸定县', 102.23, 29.92), \
        (2428, 510000, '四川省', 513300, '甘孜藏族自治州', 513323, '丹巴县', 101.88, 30.88), \
        (2429, 510000, '四川省', 513300, '甘孜藏族自治州', 513324, '九龙县', 101.5, 29), \
        (2430, 510000, '四川省', 513300, '甘孜藏族自治州', 513325, '雅江县', 101.02, 30.03), \
        (2431, 510000, '四川省', 513300, '甘孜藏族自治州', 513326, '道孚县', 101.12, 30.98), \
        (2432, 510000, '四川省', 513300, '甘孜藏族自治州', 513327, '炉霍县', 100.68, 31.4), \
        (2433, 510000, '四川省', 513300, '甘孜藏族自治州', 513328, '甘孜县', 99.98, 31.62), \
        (2434, 510000, '四川省', 513300, '甘孜藏族自治州', 513329, '新龙县', 100.32, 30.95), \
        (2435, 510000, '四川省', 513300, '甘孜藏族自治州', 513330, '德格县', 98.58, 31.82), \
        (2436, 510000, '四川省', 513300, '甘孜藏族自治州', 513331, '白玉县', 98.83, 31.22), \
        (2437, 510000, '四川省', 513300, '甘孜藏族自治州', 513332, '石渠县', 98.1, 32.98), \
        (2438, 510000, '四川省', 513300, '甘孜藏族自治州', 513333, '色达县', 100.33, 32.27), \
        (2439, 510000, '四川省', 513300, '甘孜藏族自治州', 513334, '理塘县', 100.27, 30), \
        (2440, 510000, '四川省', 513300, '甘孜藏族自治州', 513335, '巴塘县', 99.1, 30), \
        (2441, 510000, '四川省', 513300, '甘孜藏族自治州', 513336, '乡城县', 99.8, 28.93), \
        (2442, 510000, '四川省', 513300, '甘孜藏族自治州', 513337, '稻城县', 100.3, 29.03), \
        (2443, 510000, '四川省', 513300, '甘孜藏族自治州', 513338, '得荣县', 99.28, 28.72), \
        (2444, 510000, '四川省', 513400, '凉山彝族自治州', 513401, '西昌市', 102.27, 27.9), \
        (2445, 510000, '四川省', 513400, '凉山彝族自治州', 513422, '木里藏族自治县', 101.28, 27.93), \
        (2446, 510000, '四川省', 513400, '凉山彝族自治州', 513423, '盐源县', 101.5, 27.43), \
        (2447, 510000, '四川省', 513400, '凉山彝族自治州', 513424, '德昌县', 102.18, 27.4), \
        (2448, 510000, '四川省', 513400, '凉山彝族自治州', 513425, '会理县', 102.25, 26.67), \
        (2449, 510000, '四川省', 513400, '凉山彝族自治州', 513426, '会东县', 102.58, 26.63), \
        (2450, 510000, '四川省', 513400, '凉山彝族自治州', 513427, '宁南县', 102.77, 27.07), \
        (2451, 510000, '四川省', 513400, '凉山彝族自治州', 513428, '普格县', 102.53, 27.38), \
        (2452, 510000, '四川省', 513400, '凉山彝族自治州', 513429, '布拖县', 102.82, 27.72), \
        (2453, 510000, '四川省', 513400, '凉山彝族自治州', 513430, '金阳县', 103.25, 27.7), \
        (2454, 510000, '四川省', 513400, '凉山彝族自治州', 513431, '昭觉县', 102.85, 28.02), \
        (2455, 510000, '四川省', 513400, '凉山彝族自治州', 513432, '喜德县', 102.42, 28.32), \
        (2456, 510000, '四川省', 513400, '凉山彝族自治州', 513433, '冕宁县', 102.17, 28.55), \
        (2457, 510000, '四川省', 513400, '凉山彝族自治州', 513434, '越西县', 102.52, 28.65), \
        (2458, 510000, '四川省', 513400, '凉山彝族自治州', 513435, '甘洛县', 102.77, 28.97), \
        (2459, 510000, '四川省', 513400, '凉山彝族自治州', 513436, '美姑县', 103.13, 28.33), \
        (2460, 510000, '四川省', 513400, '凉山彝族自治州', 513437, '雷波县', 103.57, 28.27), \
        (2461, 520000, '贵州省', 520100, '贵阳市', 520101, '市辖区', 106.63, 26.65), \
        (2462, 520000, '贵州省', 520100, '贵阳市', 520102, '南明区', 106.72, 26.57), \
        (2463, 520000, '贵州省', 520100, '贵阳市', 520103, '云岩区', 106.72, 26.62), \
        (2464, 520000, '贵州省', 520100, '贵阳市', 520111, '花溪区', 0, 0), \
        (2465, 520000, '贵州省', 520100, '贵阳市', 520112, '乌当区', 106.75, 26.63), \
        (2466, 520000, '贵州省', 520100, '贵阳市', 520113, '白云区', 106.65, 26.68), \
        (2467, 520000, '贵州省', 520100, '贵阳市', 520114, '小河区', 106.7, 26.53), \
        (2468, 520000, '贵州省', 520100, '贵阳市', 520121, '开阳县', 106.97, 27.07), \
        (2469, 520000, '贵州省', 520100, '贵阳市', 520122, '息烽县', 106.73, 27.1), \
        (2470, 520000, '贵州省', 520100, '贵阳市', 520123, '修文县', 106.58, 26.83), \
        (2471, 520000, '贵州省', 520100, '贵阳市', 520181, '清镇市', 106.47, 26.55), \
        (2472, 520000, '贵州省', 520200, '六盘水市', 520201, '钟山区', 104.83, 26.6), \
        (2473, 520000, '贵州省', 520200, '六盘水市', 520203, '六枝特区', 105.48, 26.22), \
        (2474, 520000, '贵州省', 520200, '六盘水市', 520221, '水城县', 104.95, 26.55), \
        (2475, 520000, '贵州省', 520200, '六盘水市', 520222, '盘县', 104.47, 25.72), \
        (2476, 520000, '贵州省', 520300, '遵义市', 520301, '市辖区', 106.92, 27.73), \
        (2477, 520000, '贵州省', 520300, '遵义市', 520302, '红花岗区', 106.92, 27.65), \
        (2478, 520000, '贵州省', 520300, '遵义市', 520303, '汇川区', 106.92, 27.73), \
        (2479, 520000, '贵州省', 520300, '遵义市', 520321, '遵义县', 106.83, 27.53), \
        (2480, 520000, '贵州省', 520300, '遵义市', 520322, '桐梓县', 106.82, 28.13), \
        (2481, 520000, '贵州省', 520300, '遵义市', 520323, '绥阳县', 107.18, 27.95), \
        (2482, 520000, '贵州省', 520300, '遵义市', 520324, '正安县', 107.43, 28.55), \
        (2483, 520000, '贵州省', 520300, '遵义市', 520325, '道真仡佬族苗族自治县', 107.6, 28.88), \
        (2484, 520000, '贵州省', 520300, '遵义市', 520326, '务川仡佬族苗族自治县', 107.88, 28.53), \
        (2485, 520000, '贵州省', 520300, '遵义市', 520327, '凤冈县', 107.72, 27.97), \
        (2486, 520000, '贵州省', 520300, '遵义市', 520328, '湄潭县', 107.48, 27.77), \
        (2487, 520000, '贵州省', 520300, '遵义市', 520329, '余庆县', 107.88, 27.22), \
        (2488, 520000, '贵州省', 520300, '遵义市', 520330, '习水县', 106.22, 28.32), \
        (2489, 520000, '贵州省', 520300, '遵义市', 520381, '赤水市', 105.7, 28.58), \
        (2490, 520000, '贵州省', 520300, '遵义市', 520382, '仁怀市', 106.42, 27.82), \
        (2491, 520000, '贵州省', 520400, '安顺市', 520401, '市辖区', 105.95, 26.25), \
        (2492, 520000, '贵州省', 520400, '安顺市', 520402, '西秀区', 105.92, 26.25), \
        (2493, 520000, '贵州省', 520400, '安顺市', 520421, '平坝县', 106.25, 26.42), \
        (2494, 520000, '贵州省', 520400, '安顺市', 520422, '普定县', 105.75, 26.32), \
        (2495, 520000, '贵州省', 520400, '安顺市', 520423, '镇宁布依族苗族自治县', 105.77, 26.07), \
        (2496, 520000, '贵州省', 520400, '安顺市', 520424, '关岭布依族苗族自治县', 105.62, 25.95), \
        (2497, 520000, '贵州省', 520400, '安顺市', 520425, '紫云苗族布依族自治县', 106.08, 25.75), \
        (2498, 520000, '贵州省', 522200, '铜仁地区', 522201, '铜仁市', 109.18, 27.72), \
        (2499, 520000, '贵州省', 522200, '铜仁地区', 522222, '江口县', 108.85, 27.7), \
        (2500, 520000, '贵州省', 522200, '铜仁地区', 522223, '玉屏侗族自治县', 108.92, 27.23), \
        (2501, 520000, '贵州省', 522200, '铜仁地区', 522224, '石阡县', 108.23, 27.52), \
        (2502, 520000, '贵州省', 522200, '铜仁地区', 522225, '思南县', 108.25, 27.93), \
        (2503, 520000, '贵州省', 522200, '铜仁地区', 522226, '印江土家族苗族自治县', 108.4, 28), \
        (2504, 520000, '贵州省', 522200, '铜仁地区', 522227, '德江县', 108.12, 28.27), \
        (2505, 520000, '贵州省', 522200, '铜仁地区', 522228, '沿河土家族自治县', 108.5, 28.57), \
        (2506, 520000, '贵州省', 522200, '铜仁地区', 522229, '松桃苗族自治县', 109.2, 28.17), \
        (2507, 520000, '贵州省', 522200, '铜仁地区', 522230, '万山特区', 109.2, 27.52), \
        (2508, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522301, '兴义市', 0, 0), \
        (2509, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522322, '兴仁县', 0, 0), \
        (2510, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522323, '普安县', 0, 0), \
        (2511, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522324, '晴隆县', 0, 0), \
        (2512, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522325, '贞丰县', 0, 0), \
        (2513, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522326, '望谟县', 0, 0), \
        (2514, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522327, '册亨县', 0, 0), \
        (2515, 520000, '贵州省', 522300, '黔西南布依族苗族自', 522328, '安龙县', 0, 0), \
        (2516, 520000, '贵州省', 522400, '毕节地区', 522401, '毕节市', 105.28, 27.3), \
        (2517, 520000, '贵州省', 522400, '毕节地区', 522422, '大方县', 105.6, 27.15), \
        (2518, 520000, '贵州省', 522400, '毕节地区', 522423, '黔西县', 106.03, 27.03), \
        (2519, 520000, '贵州省', 522400, '毕节地区', 522424, '金沙县', 106.22, 27.47), \
        (2520, 520000, '贵州省', 522400, '毕节地区', 522425, '织金县', 105.77, 26.67), \
        (2521, 520000, '贵州省', 522400, '毕节地区', 522426, '纳雍县', 105.38, 26.78), \
        (2522, 520000, '贵州省', 522400, '毕节地区', 522427, '威宁彝族回族苗族自治县', 0, 0), \
        (2523, 520000, '贵州省', 522400, '毕节地区', 522428, '赫章县', 104.72, 27.13), \
        (2524, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522601, '凯里市', 107.97, 26.58), \
        (2525, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522622, '黄平县', 107.9, 26.9), \
        (2526, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522623, '施秉县', 108.12, 27.03), \
        (2527, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522624, '三穗县', 108.68, 26.97), \
        (2528, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522625, '镇远县', 108.42, 27.05), \
        (2529, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522626, '岑巩县', 108.82, 27.18), \
        (2530, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522627, '天柱县', 109.2, 26.92), \
        (2531, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522628, '锦屏县', 109.2, 26.68), \
        (2532, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522629, '剑河县', 108.45, 26.73), \
        (2533, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522630, '台江县', 108.32, 26.67), \
        (2534, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522631, '黎平县', 109.13, 26.23), \
        (2535, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522632, '榕江县', 108.52, 25.93), \
        (2536, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522633, '从江县', 108.9, 25.75), \
        (2537, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522634, '雷山县', 108.07, 26.38), \
        (2538, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522635, '麻江县', 107.58, 26.5), \
        (2539, 520000, '贵州省', 522600, '黔东南苗族侗族自治', 522636, '丹寨县', 107.8, 26.2), \
        (2540, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522701, '都匀市', 107.52, 26.27), \
        (2541, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522702, '福泉市', 107.5, 26.7), \
        (2542, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522722, '荔波县', 107.88, 25.42), \
        (2543, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522723, '贵定县', 107.23, 26.58), \
        (2544, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522725, '瓮安县', 107.47, 27.07), \
        (2545, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522726, '独山县', 107.53, 25.83), \
        (2546, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522727, '平塘县', 107.32, 25.83), \
        (2547, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522728, '罗甸县', 106.75, 25.43), \
        (2548, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522729, '长顺县', 106.45, 26.03), \
        (2549, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522730, '龙里县', 106.97, 26.45), \
        (2550, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522731, '惠水县', 106.65, 26.13), \
        (2551, 520000, '贵州省', 522700, '黔南布依族苗族自治', 522732, '三都水族自治县', 107.87, 25.98), \
        (2552, 530000, '云南省', 530100, '昆明市', 530101, '市辖区', 102.72, 25.05), \
        (2553, 530000, '云南省', 530100, '昆明市', 530102, '五华区', 102.7, 25.05), \
        (2554, 530000, '云南省', 530100, '昆明市', 530103, '盘龙区', 102.72, 25.03), \
        (2555, 530000, '云南省', 530100, '昆明市', 530111, '官渡区', 102.75, 25.02), \
        (2556, 530000, '云南省', 530100, '昆明市', 530112, '西山区', 102.67, 25.03), \
        (2557, 530000, '云南省', 530100, '昆明市', 530113, '东川区', 103.18, 26.08), \
        (2558, 530000, '云南省', 530100, '昆明市', 530121, '呈贡县', 102.8, 24.88), \
        (2559, 530000, '云南省', 530100, '昆明市', 530122, '晋宁县', 102.6, 24.67), \
        (2560, 530000, '云南省', 530100, '昆明市', 530124, '富民县', 102.5, 25.22), \
        (2561, 530000, '云南省', 530100, '昆明市', 530125, '宜良县', 103.15, 24.92), \
        (2562, 530000, '云南省', 530100, '昆明市', 530126, '石林彝族自治县', 103.27, 24.77), \
        (2563, 530000, '云南省', 530100, '昆明市', 530127, '嵩明县', 103.03, 25.35), \
        (2564, 530000, '云南省', 530100, '昆明市', 530128, '禄劝彝族苗族自治县', 102.47, 25.55), \
        (2565, 530000, '云南省', 530100, '昆明市', 530129, '寻甸回族彝族自治县', 103.25, 25.57), \
        (2566, 530000, '云南省', 530100, '昆明市', 530181, '安宁市', 102.48, 24.92), \
        (2567, 530000, '云南省', 530300, '曲靖市', 530301, '市辖区', 103.8, 25.5), \
        (2568, 530000, '云南省', 530300, '曲靖市', 530302, '麒麟区', 103.8, 25.5), \
        (2569, 530000, '云南省', 530300, '曲靖市', 530321, '马龙县', 103.58, 25.43), \
        (2570, 530000, '云南省', 530300, '曲靖市', 530322, '陆良县', 103.67, 25.03), \
        (2571, 530000, '云南省', 530300, '曲靖市', 530323, '师宗县', 103.98, 24.83), \
        (2572, 530000, '云南省', 530300, '曲靖市', 530324, '罗平县', 104.3, 24.88), \
        (2573, 530000, '云南省', 530300, '曲靖市', 530325, '富源县', 104.25, 25.67), \
        (2574, 530000, '云南省', 530300, '曲靖市', 530326, '会泽县', 103.3, 26.42), \
        (2575, 530000, '云南省', 530300, '曲靖市', 530328, '沾益县', 103.82, 25.62), \
        (2576, 530000, '云南省', 530300, '曲靖市', 530381, '宣威市', 104.1, 26.22), \
        (2577, 530000, '云南省', 530400, '玉溪市', 530401, '市辖区', 102.55, 24.35), \
        (2578, 530000, '云南省', 530400, '玉溪市', 530402, '红塔区', 0, 0), \
        (2579, 530000, '云南省', 530400, '玉溪市', 530421, '江川县', 102.75, 24.28), \
        (2580, 530000, '云南省', 530400, '玉溪市', 530422, '澄江县', 102.92, 24.67), \
        (2581, 530000, '云南省', 530400, '玉溪市', 530423, '通海县', 102.75, 24.12), \
        (2582, 530000, '云南省', 530400, '玉溪市', 530424, '华宁县', 102.93, 24.2), \
        (2583, 530000, '云南省', 530400, '玉溪市', 530425, '易门县', 102.17, 24.67), \
        (2584, 530000, '云南省', 530400, '玉溪市', 530426, '峨山彝族自治县', 102.4, 24.18), \
        (2585, 530000, '云南省', 530400, '玉溪市', 530427, '新平彝族傣族自治县', 101.98, 24.07), \
        (2586, 530000, '云南省', 530400, '玉溪市', 530428, '元江哈尼族彝族傣族自治县', 0, 0), \
        (2587, 530000, '云南省', 530500, '保山市', 530501, '市辖区', 99.17, 25.12), \
        (2588, 530000, '云南省', 530500, '保山市', 530502, '隆阳区', 99.17, 25.12), \
        (2589, 530000, '云南省', 530500, '保山市', 530521, '施甸县', 99.18, 24.73), \
        (2590, 530000, '云南省', 530500, '保山市', 530522, '腾冲县', 98.5, 25.03), \
        (2591, 530000, '云南省', 530500, '保山市', 530523, '龙陵县', 98.68, 24.58), \
        (2592, 530000, '云南省', 530500, '保山市', 530524, '昌宁县', 99.6, 24.83), \
        (2593, 530000, '云南省', 530600, '昭通市', 530601, '市辖区', 103.72, 27.33), \
        (2594, 530000, '云南省', 530600, '昭通市', 530602, '昭阳区', 103.72, 27.33), \
        (2595, 530000, '云南省', 530600, '昭通市', 530621, '鲁甸县', 103.55, 27.2), \
        (2596, 530000, '云南省', 530600, '昭通市', 530622, '巧家县', 102.92, 26.92), \
        (2597, 530000, '云南省', 530600, '昭通市', 530623, '盐津县', 104.23, 28.12), \
        (2598, 530000, '云南省', 530600, '昭通市', 530624, '大关县', 103.88, 27.75), \
        (2599, 530000, '云南省', 530600, '昭通市', 530625, '永善县', 103.63, 28.23), \
        (2600, 530000, '云南省', 530600, '昭通市', 530626, '绥江县', 103.95, 28.6), \
        (2601, 530000, '云南省', 530600, '昭通市', 530627, '镇雄县', 104.87, 27.45), \
        (2602, 530000, '云南省', 530600, '昭通市', 530628, '彝良县', 104.05, 27.63), \
        (2603, 530000, '云南省', 530600, '昭通市', 530629, '威信县', 105.05, 27.85), \
        (2604, 530000, '云南省', 530600, '昭通市', 530630, '水富县', 104.4, 28.63), \
        (2605, 530000, '云南省', 530700, '丽江市', 530701, '市辖区', 100.23, 26.88), \
        (2606, 530000, '云南省', 530700, '丽江市', 530702, '古城区', 100.23, 26.88), \
        (2607, 530000, '云南省', 530700, '丽江市', 530721, '玉龙纳西族自治县', 100.23, 26.82), \
        (2608, 530000, '云南省', 530700, '丽江市', 530722, '永胜县', 100.75, 26.68), \
        (2609, 530000, '云南省', 530700, '丽江市', 530723, '华坪县', 101.27, 26.63), \
        (2610, 530000, '云南省', 530700, '丽江市', 530724, '宁蒗彝族自治县', 100.85, 27.28), \
        (2611, 530000, '云南省', 530800, '思茅市', 530801, '市辖区', 0, 0), \
        (2612, 530000, '云南省', 530800, '思茅市', 530802, '翠云区', 0, 0), \
        (2613, 530000, '云南省', 530800, '思茅市', 530821, '普洱哈尼族彝族自治县', 0, 0), \
        (2614, 530000, '云南省', 530800, '思茅市', 530822, '墨江哈尼族自治县', 0, 0), \
        (2615, 530000, '云南省', 530800, '思茅市', 530823, '景东彝族自治县', 0, 0), \
        (2616, 530000, '云南省', 530800, '思茅市', 530824, '景谷傣族彝族自治县', 0, 0), \
        (2617, 530000, '云南省', 530800, '思茅市', 530825, '镇沅彝族哈尼族拉祜族自治县', 0, 0), \
        (2618, 530000, '云南省', 530800, '思茅市', 530826, '江城哈尼族彝族自治县', 0, 0), \
        (2619, 530000, '云南省', 530800, '思茅市', 530827, '孟连傣族拉祜族佤族自治县', 0, 0), \
        (2620, 530000, '云南省', 530800, '思茅市', 530828, '澜沧拉祜族自治县', 0, 0), \
        (2621, 530000, '云南省', 530800, '思茅市', 530829, '西盟佤族自治县', 0, 0), \
        (2622, 530000, '云南省', 530900, '临沧市', 530901, '市辖区', 100.08, 23.88), \
        (2623, 530000, '云南省', 530900, '临沧市', 530902, '临翔区', 100.08, 23.88), \
        (2624, 530000, '云南省', 530900, '临沧市', 530921, '凤庆县', 99.92, 24.6), \
        (2625, 530000, '云南省', 530900, '临沧市', 530922, '云县', 100.13, 24.45), \
        (2626, 530000, '云南省', 530900, '临沧市', 530923, '永德县', 99.25, 24.03), \
        (2627, 530000, '云南省', 530900, '临沧市', 530924, '镇康县', 98.83, 23.78), \
        (2628, 530000, '云南省', 530900, '临沧市', 530925, '双江拉祜族佤族布朗族傣族自治县', 0, 0), \
        (2629, 530000, '云南省', 530900, '临沧市', 530926, '耿马傣族佤族自治县', 99.4, 23.55), \
        (2630, 530000, '云南省', 530900, '临沧市', 530927, '沧源佤族自治县', 99.25, 23.15), \
        (2631, 530000, '云南省', 532300, '楚雄彝族自治州', 532301, '楚雄市', 101.55, 25.03), \
        (2632, 530000, '云南省', 532300, '楚雄彝族自治州', 532322, '双柏县', 101.63, 24.7), \
        (2633, 530000, '云南省', 532300, '楚雄彝族自治州', 532323, '牟定县', 101.53, 25.32), \
        (2634, 530000, '云南省', 532300, '楚雄彝族自治州', 532324, '南华县', 101.27, 25.2), \
        (2635, 530000, '云南省', 532300, '楚雄彝族自治州', 532325, '姚安县', 101.23, 25.5), \
        (2636, 530000, '云南省', 532300, '楚雄彝族自治州', 532326, '大姚县', 101.32, 25.73), \
        (2637, 530000, '云南省', 532300, '楚雄彝族自治州', 532327, '永仁县', 101.67, 26.07), \
        (2638, 530000, '云南省', 532300, '楚雄彝族自治州', 532328, '元谋县', 101.88, 25.7), \
        (2639, 530000, '云南省', 532300, '楚雄彝族自治州', 532329, '武定县', 102.4, 25.53), \
        (2640, 530000, '云南省', 532300, '楚雄彝族自治州', 532331, '禄丰县', 102.08, 25.15), \
        (2641, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532501, '个旧市', 103.15, 23.37), \
        (2642, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532502, '开远市', 103.27, 23.72), \
        (2643, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532522, '蒙自县', 103.4, 23.37), \
        (2644, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532523, '屏边苗族自治县', 103.68, 22.98), \
        (2645, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532524, '建水县', 102.83, 23.62), \
        (2646, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532525, '石屏县', 102.5, 23.72), \
        (2647, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532526, '弥勒县', 103.43, 24.4), \
        (2648, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532527, '泸西县', 103.77, 24.53), \
        (2649, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532528, '元阳县', 102.83, 23.23), \
        (2650, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532529, '红河县', 102.42, 23.37), \
        (2651, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532530, '金平苗族瑶族傣族自治县', 0, 0), \
        (2652, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532531, '绿春县', 102.4, 23), \
        (2653, 530000, '云南省', 532500, '红河哈尼族彝族自治', 532532, '河口瑶族自治县', 103.97, 22.52), \
        (2654, 530000, '云南省', 532600, '文山壮族苗族自治州', 532621, '文山县', 104.25, 23.37), \
        (2655, 530000, '云南省', 532600, '文山壮族苗族自治州', 532622, '砚山县', 104.33, 23.62), \
        (2656, 530000, '云南省', 532600, '文山壮族苗族自治州', 532623, '西畴县', 104.67, 23.45), \
        (2657, 530000, '云南省', 532600, '文山壮族苗族自治州', 532624, '麻栗坡县', 104.7, 23.12), \
        (2658, 530000, '云南省', 532600, '文山壮族苗族自治州', 532625, '马关县', 104.4, 23.02), \
        (2659, 530000, '云南省', 532600, '文山壮族苗族自治州', 532626, '丘北县', 104.18, 24.05), \
        (2660, 530000, '云南省', 532600, '文山壮族苗族自治州', 532627, '广南县', 105.07, 24.05), \
        (2661, 530000, '云南省', 532600, '文山壮族苗族自治州', 532628, '富宁县', 105.62, 23.63), \
        (2662, 530000, '云南省', 532800, '西双版纳傣族自治州', 532801, '景洪市', 100.8, 22.02), \
        (2663, 530000, '云南省', 532800, '西双版纳傣族自治州', 532822, '勐海县', 100.45, 21.97), \
        (2664, 530000, '云南省', 532800, '西双版纳傣族自治州', 532823, '勐腊县', 101.57, 21.48), \
        (2665, 530000, '云南省', 532900, '大理白族自治州', 532901, '大理市', 100.23, 25.6), \
        (2666, 530000, '云南省', 532900, '大理白族自治州', 532922, '漾濞彝族自治县', 99.95, 25.67), \
        (2667, 530000, '云南省', 532900, '大理白族自治州', 532923, '祥云县', 100.55, 25.48), \
        (2668, 530000, '云南省', 532900, '大理白族自治州', 532924, '宾川县', 100.58, 25.83), \
        (2669, 530000, '云南省', 532900, '大理白族自治州', 532925, '弥渡县', 100.48, 25.35), \
        (2670, 530000, '云南省', 532900, '大理白族自治州', 532926, '南涧彝族自治县', 100.52, 25.05), \
        (2671, 530000, '云南省', 532900, '大理白族自治州', 532927, '巍山彝族回族自治县', 100.3, 25.23), \
        (2672, 530000, '云南省', 532900, '大理白族自治州', 532928, '永平县', 99.53, 25.47), \
        (2673, 530000, '云南省', 532900, '大理白族自治州', 532929, '云龙县', 99.37, 25.88), \
        (2674, 530000, '云南省', 532900, '大理白族自治州', 532930, '洱源县', 99.95, 26.12), \
        (2675, 530000, '云南省', 532900, '大理白族自治州', 532931, '剑川县', 99.9, 26.53), \
        (2676, 530000, '云南省', 532900, '大理白族自治州', 532932, '鹤庆县', 100.18, 26.57), \
        (2677, 530000, '云南省', 533100, '德宏傣族景颇族自治', 533102, '瑞丽市', 97.85, 24.02), \
        (2678, 530000, '云南省', 533100, '德宏傣族景颇族自治', 533103, '潞西市', 98.58, 24.43), \
        (2679, 530000, '云南省', 533100, '德宏傣族景颇族自治', 533122, '梁河县', 98.3, 24.82), \
        (2680, 530000, '云南省', 533100, '德宏傣族景颇族自治', 533123, '盈江县', 97.93, 24.72), \
        (2681, 530000, '云南省', 533100, '德宏傣族景颇族自治', 533124, '陇川县', 97.8, 24.2), \
        (2682, 530000, '云南省', 533300, '怒江傈僳族自治州', 533321, '泸水县', 98.85, 25.85), \
        (2683, 530000, '云南省', 533300, '怒江傈僳族自治州', 533323, '福贡县', 98.87, 26.9), \
        (2684, 530000, '云南省', 533300, '怒江傈僳族自治州', 533324, '贡山独龙族怒族自治县', 98.67, 27.73), \
        (2685, 530000, '云南省', 533300, '怒江傈僳族自治州', 533325, '兰坪白族普米族自治县', 99.42, 26.45), \
        (2686, 530000, '云南省', 533400, '迪庆藏族自治州', 533421, '香格里拉县', 99.7, 27.83), \
        (2687, 530000, '云南省', 533400, '迪庆藏族自治州', 533422, '德钦县', 98.92, 28.48), \
        (2688, 530000, '云南省', 533400, '迪庆藏族自治州', 533423, '维西傈僳族自治县', 99.28, 27.18), \
        (2689, 540000, '西藏自', 540100, '拉萨市', 540101, '市辖区', 91.13, 29.65), \
        (2690, 540000, '西藏自', 540100, '拉萨市', 540102, '城关区', 91.13, 29.65), \
        (2691, 540000, '西藏自', 540100, '拉萨市', 540121, '林周县', 91.25, 29.9), \
        (2692, 540000, '西藏自', 540100, '拉萨市', 540122, '当雄县', 91.1, 30.48), \
        (2693, 540000, '西藏自', 540100, '拉萨市', 540123, '尼木县', 90.15, 29.45), \
        (2694, 540000, '西藏自', 540100, '拉萨市', 540124, '曲水县', 90.73, 29.37), \
        (2695, 540000, '西藏自', 540100, '拉萨市', 540125, '堆龙德庆县', 91, 29.65), \
        (2696, 540000, '西藏自', 540100, '拉萨市', 540126, '达孜县', 91.35, 29.68), \
        (2697, 540000, '西藏自', 540100, '拉萨市', 540127, '墨竹工卡县', 91.73, 29.83), \
        (2698, 540000, '西藏自', 542100, '昌都地区', 542121, '昌都县', 97.18, 31.13), \
        (2699, 540000, '西藏自', 542100, '昌都地区', 542122, '江达县', 98.22, 31.5), \
        (2700, 540000, '西藏自', 542100, '昌都地区', 542123, '贡觉县', 98.27, 30.87), \
        (2701, 540000, '西藏自', 542100, '昌都地区', 542124, '类乌齐县', 96.6, 31.22), \
        (2702, 540000, '西藏自', 542100, '昌都地区', 542125, '丁青县', 95.6, 31.42), \
        (2703, 540000, '西藏自', 542100, '昌都地区', 542126, '察雅县', 97.57, 30.65), \
        (2704, 540000, '西藏自', 542100, '昌都地区', 542127, '八宿县', 96.92, 30.05), \
        (2705, 540000, '西藏自', 542100, '昌都地区', 542128, '左贡县', 97.85, 29.67), \
        (2706, 540000, '西藏自', 542100, '昌都地区', 542129, '芒康县', 98.6, 29.68), \
        (2707, 540000, '西藏自', 542100, '昌都地区', 542132, '洛隆县', 95.83, 30.75), \
        (2708, 540000, '西藏自', 542100, '昌都地区', 542133, '边坝县', 94.7, 30.93), \
        (2709, 540000, '西藏自', 542200, '山南地区', 542221, '乃东县', 91.77, 29.23), \
        (2710, 540000, '西藏自', 542200, '山南地区', 542222, '扎囊县', 91.33, 29.25), \
        (2711, 540000, '西藏自', 542200, '山南地区', 542223, '贡嘎县', 90.98, 29.3), \
        (2712, 540000, '西藏自', 542200, '山南地区', 542224, '桑日县', 92.02, 29.27), \
        (2713, 540000, '西藏自', 542200, '山南地区', 542225, '琼结县', 91.68, 29.03), \
        (2714, 540000, '西藏自', 542200, '山南地区', 542226, '曲松县', 92.2, 29.07), \
        (2715, 540000, '西藏自', 542200, '山南地区', 542227, '措美县', 91.43, 28.43), \
        (2716, 540000, '西藏自', 542200, '山南地区', 542228, '洛扎县', 90.87, 28.38), \
        (2717, 540000, '西藏自', 542200, '山南地区', 542229, '加查县', 92.58, 29.15), \
        (2718, 540000, '西藏自', 542200, '山南地区', 542231, '隆子县', 92.47, 28.42), \
        (2719, 540000, '西藏自', 542200, '山南地区', 542232, '错那县', 91.95, 28), \
        (2720, 540000, '西藏自', 542200, '山南地区', 542233, '浪卡子县', 90.4, 28.97), \
        (2721, 540000, '西藏自', 542300, '日喀则地区', 542301, '日喀则市', 88.88, 29.27), \
        (2722, 540000, '西藏自', 542300, '日喀则地区', 542322, '南木林县', 89.1, 29.68), \
        (2723, 540000, '西藏自', 542300, '日喀则地区', 542323, '江孜县', 89.6, 28.92), \
        (2724, 540000, '西藏自', 542300, '日喀则地区', 542324, '定日县', 87.12, 28.67), \
        (2725, 540000, '西藏自', 542300, '日喀则地区', 542325, '萨迦县', 88.02, 28.9), \
        (2726, 540000, '西藏自', 542300, '日喀则地区', 542326, '拉孜县', 87.63, 29.08), \
        (2727, 540000, '西藏自', 542300, '日喀则地区', 542327, '昂仁县', 87.23, 29.3), \
        (2728, 540000, '西藏自', 542300, '日喀则地区', 542328, '谢通门县', 88.27, 29.43), \
        (2729, 540000, '西藏自', 542300, '日喀则地区', 542329, '白朗县', 89.27, 29.12), \
        (2730, 540000, '西藏自', 542300, '日喀则地区', 542330, '仁布县', 89.83, 29.23), \
        (2731, 540000, '西藏自', 542300, '日喀则地区', 542331, '康马县', 89.68, 28.57), \
        (2732, 540000, '西藏自', 542300, '日喀则地区', 542332, '定结县', 87.77, 28.37), \
        (2733, 540000, '西藏自', 542300, '日喀则地区', 542333, '仲巴县', 84.03, 29.77), \
        (2734, 540000, '西藏自', 542300, '日喀则地区', 542334, '亚东县', 88.9, 27.48), \
        (2735, 540000, '西藏自', 542300, '日喀则地区', 542335, '吉隆县', 85.3, 28.85), \
        (2736, 540000, '西藏自', 542300, '日喀则地区', 542336, '聂拉木县', 85.98, 28.17), \
        (2737, 540000, '西藏自', 542300, '日喀则地区', 542337, '萨嘎县', 85.23, 29.33), \
        (2738, 540000, '西藏自', 542300, '日喀则地区', 542338, '岗巴县', 88.52, 28.28), \
        (2739, 540000, '西藏自', 542400, '那曲地区', 542421, '那曲县', 92.07, 31.48), \
        (2740, 540000, '西藏自', 542400, '那曲地区', 542422, '嘉黎县', 93.25, 30.65), \
        (2741, 540000, '西藏自', 542400, '那曲地区', 542423, '比如县', 93.68, 31.48), \
        (2742, 540000, '西藏自', 542400, '那曲地区', 542424, '聂荣县', 92.3, 32.12), \
        (2743, 540000, '西藏自', 542400, '那曲地区', 542425, '安多县', 91.68, 32.27), \
        (2744, 540000, '西藏自', 542400, '那曲地区', 542426, '申扎县', 88.7, 30.93), \
        (2745, 540000, '西藏自', 542400, '那曲地区', 542427, '索县', 93.78, 31.88), \
        (2746, 540000, '西藏自', 542400, '那曲地区', 542428, '班戈县', 90.02, 31.37), \
        (2747, 540000, '西藏自', 542400, '那曲地区', 542429, '巴青县', 94.03, 31.93), \
        (2748, 540000, '西藏自', 542400, '那曲地区', 542430, '尼玛县', 87.23, 31.78), \
        (2749, 540000, '西藏自', 542500, '阿里地区', 542521, '普兰县', 81.17, 30.3), \
        (2750, 540000, '西藏自', 542500, '阿里地区', 542522, '札达县', 79.8, 31.48), \
        (2751, 540000, '西藏自', 542500, '阿里地区', 542523, '噶尔县', 80.1, 32.5), \
        (2752, 540000, '西藏自', 542500, '阿里地区', 542524, '日土县', 79.72, 33.38), \
        (2753, 540000, '西藏自', 542500, '阿里地区', 542525, '革吉县', 81.12, 32.4), \
        (2754, 540000, '西藏自', 542500, '阿里地区', 542526, '改则县', 84.07, 32.3), \
        (2755, 540000, '西藏自', 542500, '阿里地区', 542527, '措勤县', 85.17, 31.02), \
        (2756, 540000, '西藏自', 542600, '林芝地区', 542621, '林芝县', 94.37, 29.68), \
        (2757, 540000, '西藏自', 542600, '林芝地区', 542622, '工布江达县', 93.25, 29.88), \
        (2758, 540000, '西藏自', 542600, '林芝地区', 542623, '米林县', 94.22, 29.22), \
        (2759, 540000, '西藏自', 542600, '林芝地区', 542624, '墨脱县', 95.33, 29.33), \
        (2760, 540000, '西藏自', 542600, '林芝地区', 542625, '波密县', 95.77, 29.87), \
        (2761, 540000, '西藏自', 542600, '林芝地区', 542626, '察隅县', 97.47, 28.67), \
        (2762, 540000, '西藏自', 542600, '林芝地区', 542627, '朗县', 93.07, 29.05), \
        (2763, 610000, '陕西省', 610100, '西安市', 610101, '市辖区', 108.93, 34.27), \
        (2764, 610000, '陕西省', 610100, '西安市', 610102, '新城区', 108.95, 34.27), \
        (2765, 610000, '陕西省', 610100, '西安市', 610103, '碑林区', 108.93, 34.23), \
        (2766, 610000, '陕西省', 610100, '西安市', 610104, '莲湖区', 108.93, 34.27), \
        (2767, 610000, '陕西省', 610100, '西安市', 610111, '灞桥区', 109.07, 34.27), \
        (2768, 610000, '陕西省', 610100, '西安市', 610112, '未央区', 108.93, 34.28), \
        (2769, 610000, '陕西省', 610100, '西安市', 610113, '雁塔区', 108.95, 34.22), \
        (2770, 610000, '陕西省', 610100, '西安市', 610114, '阎良区', 109.23, 34.65), \
        (2771, 610000, '陕西省', 610100, '西安市', 610115, '临潼区', 109.22, 34.37), \
        (2772, 610000, '陕西省', 610100, '西安市', 610116, '长安区', 108.93, 34.17), \
        (2773, 610000, '陕西省', 610100, '西安市', 610122, '蓝田县', 109.32, 34.15), \
        (2774, 610000, '陕西省', 610100, '西安市', 610124, '周至县', 108.2, 34.17), \
        (2775, 610000, '陕西省', 610100, '西安市', 610125, '户县', 108.6, 34.1), \
        (2776, 610000, '陕西省', 610100, '西安市', 610126, '高陵县', 109.08, 34.53), \
        (2777, 610000, '陕西省', 610200, '铜川市', 610201, '市辖区', 108.93, 34.9), \
        (2778, 610000, '陕西省', 610200, '铜川市', 610202, '王益区', 109.07, 35.07), \
        (2779, 610000, '陕西省', 610200, '铜川市', 610203, '印台区', 109.1, 35.1), \
        (2780, 610000, '陕西省', 610200, '铜川市', 610204, '耀州区', 108.98, 34.92), \
        (2781, 610000, '陕西省', 610200, '铜川市', 610222, '宜君县', 109.12, 35.4), \
        (2782, 610000, '陕西省', 610300, '宝鸡市', 610301, '市辖区', 107.13, 34.37), \
        (2783, 610000, '陕西省', 610300, '宝鸡市', 610302, '渭滨区', 107.15, 34.37), \
        (2784, 610000, '陕西省', 610300, '宝鸡市', 610303, '金台区', 107.13, 34.38), \
        (2785, 610000, '陕西省', 610300, '宝鸡市', 610304, '陈仓区', 107.37, 34.37), \
        (2786, 610000, '陕西省', 610300, '宝鸡市', 610322, '凤翔县', 107.38, 34.52), \
        (2787, 610000, '陕西省', 610300, '宝鸡市', 610323, '岐山县', 107.62, 34.45), \
        (2788, 610000, '陕西省', 610300, '宝鸡市', 610324, '扶风县', 107.87, 34.37), \
        (2789, 610000, '陕西省', 610300, '宝鸡市', 610326, '眉县', 107.75, 34.28), \
        (2790, 610000, '陕西省', 610300, '宝鸡市', 610327, '陇县', 106.85, 34.9), \
        (2791, 610000, '陕西省', 610300, '宝鸡市', 610328, '千阳县', 107.13, 34.65), \
        (2792, 610000, '陕西省', 610300, '宝鸡市', 610329, '麟游县', 107.78, 34.68), \
        (2793, 610000, '陕西省', 610300, '宝鸡市', 610330, '凤县', 106.52, 33.92), \
        (2794, 610000, '陕西省', 610300, '宝鸡市', 610331, '太白县', 107.32, 34.07), \
        (2795, 610000, '陕西省', 610400, '咸阳市', 610401, '市辖区', 108.7, 34.33), \
        (2796, 610000, '陕西省', 610400, '咸阳市', 610402, '秦都区', 108.72, 34.35), \
        (2797, 610000, '陕西省', 610400, '咸阳市', 610403, '杨凌区', 108.07, 34.28), \
        (2798, 610000, '陕西省', 610400, '咸阳市', 610404, '渭城区', 108.73, 34.33), \
        (2799, 610000, '陕西省', 610400, '咸阳市', 610422, '三原县', 108.93, 34.62), \
        (2800, 610000, '陕西省', 610400, '咸阳市', 610423, '泾阳县', 108.83, 34.53), \
        (2801, 610000, '陕西省', 610400, '咸阳市', 610424, '乾县', 108.23, 34.53), \
        (2802, 610000, '陕西省', 610400, '咸阳市', 610425, '礼泉县', 108.42, 34.48), \
        (2803, 610000, '陕西省', 610400, '咸阳市', 610426, '永寿县', 108.13, 34.7), \
        (2804, 610000, '陕西省', 610400, '咸阳市', 610427, '彬县', 108.08, 35.03), \
        (2805, 610000, '陕西省', 610400, '咸阳市', 610428, '长武县', 107.78, 35.2), \
        (2806, 610000, '陕西省', 610400, '咸阳市', 610429, '旬邑县', 108.33, 35.12), \
        (2807, 610000, '陕西省', 610400, '咸阳市', 610430, '淳化县', 108.58, 34.78), \
        (2808, 610000, '陕西省', 610400, '咸阳市', 610431, '武功县', 108.2, 34.27), \
        (2809, 610000, '陕西省', 610400, '咸阳市', 610481, '兴平市', 108.48, 34.3), \
        (2810, 610000, '陕西省', 610500, '渭南市', 610501, '市辖区', 109.5, 34.5), \
        (2811, 610000, '陕西省', 610500, '渭南市', 610502, '临渭区', 109.48, 34.5), \
        (2812, 610000, '陕西省', 610500, '渭南市', 610521, '华县', 109.77, 34.52), \
        (2813, 610000, '陕西省', 610500, '渭南市', 610522, '潼关县', 110.23, 34.55), \
        (2814, 610000, '陕西省', 610500, '渭南市', 610523, '大荔县', 109.93, 34.8), \
        (2815, 610000, '陕西省', 610500, '渭南市', 610524, '合阳县', 110.15, 35.23), \
        (2816, 610000, '陕西省', 610500, '渭南市', 610525, '澄城县', 109.93, 35.18), \
        (2817, 610000, '陕西省', 610500, '渭南市', 610526, '蒲城县', 109.58, 34.95), \
        (2818, 610000, '陕西省', 610500, '渭南市', 610527, '白水县', 109.58, 35.18), \
        (2819, 610000, '陕西省', 610500, '渭南市', 610528, '富平县', 109.18, 34.75), \
        (2820, 610000, '陕西省', 610500, '渭南市', 610581, '韩城市', 110.43, 35.48), \
        (2821, 610000, '陕西省', 610500, '渭南市', 610582, '华阴市', 110.08, 34.57), \
        (2822, 610000, '陕西省', 610600, '延安市', 610601, '市辖区', 109.48, 36.6), \
        (2823, 610000, '陕西省', 610600, '延安市', 610602, '宝塔区', 109.48, 36.6), \
        (2824, 610000, '陕西省', 610600, '延安市', 610621, '延长县', 110, 36.58), \
        (2825, 610000, '陕西省', 610600, '延安市', 610622, '延川县', 110.18, 36.88), \
        (2826, 610000, '陕西省', 610600, '延安市', 610623, '子长县', 109.67, 37.13), \
        (2827, 610000, '陕西省', 610600, '延安市', 610624, '安塞县', 109.32, 36.87), \
        (2828, 610000, '陕西省', 610600, '延安市', 610625, '志丹县', 108.77, 36.82), \
        (2829, 610000, '陕西省', 610600, '延安市', 610626, '吴起县', 0, 0), \
        (2830, 610000, '陕西省', 610600, '延安市', 610627, '甘泉县', 109.35, 36.28), \
        (2831, 610000, '陕西省', 610600, '延安市', 610628, '富县', 109.37, 35.98), \
        (2832, 610000, '陕西省', 610600, '延安市', 610629, '洛川县', 109.43, 35.77), \
        (2833, 610000, '陕西省', 610600, '延安市', 610630, '宜川县', 110.17, 36.05), \
        (2834, 610000, '陕西省', 610600, '延安市', 610631, '黄龙县', 109.83, 35.58), \
        (2835, 610000, '陕西省', 610600, '延安市', 610632, '黄陵县', 109.25, 35.58), \
        (2836, 610000, '陕西省', 610700, '汉中市', 610701, '市辖区', 107.02, 33.07), \
        (2837, 610000, '陕西省', 610700, '汉中市', 610702, '汉台区', 107.03, 33.07), \
        (2838, 610000, '陕西省', 610700, '汉中市', 610721, '南郑县', 106.93, 33), \
        (2839, 610000, '陕西省', 610700, '汉中市', 610722, '城固县', 107.33, 33.15), \
        (2840, 610000, '陕西省', 610700, '汉中市', 610723, '洋县', 107.55, 33.22), \
        (2841, 610000, '陕西省', 610700, '汉中市', 610724, '西乡县', 107.77, 32.98), \
        (2842, 610000, '陕西省', 610700, '汉中市', 610725, '勉县', 106.67, 33.15), \
        (2843, 610000, '陕西省', 610700, '汉中市', 610726, '宁强县', 106.25, 32.83), \
        (2844, 610000, '陕西省', 610700, '汉中市', 610727, '略阳县', 106.15, 33.33), \
        (2845, 610000, '陕西省', 610700, '汉中市', 610728, '镇巴县', 107.9, 32.53), \
        (2846, 610000, '陕西省', 610700, '汉中市', 610729, '留坝县', 106.92, 33.62), \
        (2847, 610000, '陕西省', 610700, '汉中市', 610730, '佛坪县', 107.98, 33.53), \
        (2848, 610000, '陕西省', 610800, '榆林市', 610801, '市辖区', 109.73, 38.28), \
        (2849, 610000, '陕西省', 610800, '榆林市', 610802, '榆阳区', 109.75, 38.28), \
        (2850, 610000, '陕西省', 610800, '榆林市', 610821, '神木县', 110.5, 38.83), \
        (2851, 610000, '陕西省', 610800, '榆林市', 610822, '府谷县', 111.07, 39.03), \
        (2852, 610000, '陕西省', 610800, '榆林市', 610823, '横山县', 109.28, 37.95), \
        (2853, 610000, '陕西省', 610800, '榆林市', 610824, '靖边县', 108.8, 37.6), \
        (2854, 610000, '陕西省', 610800, '榆林市', 610825, '定边县', 107.6, 37.58), \
        (2855, 610000, '陕西省', 610800, '榆林市', 610826, '绥德县', 110.25, 37.5), \
        (2856, 610000, '陕西省', 610800, '榆林市', 610827, '米脂县', 110.18, 37.75), \
        (2857, 610000, '陕西省', 610800, '榆林市', 610828, '佳县', 110.48, 38.02), \
        (2858, 610000, '陕西省', 610800, '榆林市', 610829, '吴堡县', 110.73, 37.45), \
        (2859, 610000, '陕西省', 610800, '榆林市', 610830, '清涧县', 110.12, 37.08), \
        (2860, 610000, '陕西省', 610800, '榆林市', 610831, '子洲县', 110.03, 37.62), \
        (2861, 610000, '陕西省', 610900, '安康市', 610901, '市辖区', 109.02, 32.68), \
        (2862, 610000, '陕西省', 610900, '安康市', 610902, '汉滨区', 109.02, 32.68), \
        (2863, 610000, '陕西省', 610900, '安康市', 610921, '汉阴县', 108.5, 32.9), \
        (2864, 610000, '陕西省', 610900, '安康市', 610922, '石泉县', 108.25, 33.05), \
        (2865, 610000, '陕西省', 610900, '安康市', 610923, '宁陕县', 108.32, 33.32), \
        (2866, 610000, '陕西省', 610900, '安康市', 610924, '紫阳县', 108.53, 32.52), \
        (2867, 610000, '陕西省', 610900, '安康市', 610925, '岚皋县', 108.9, 32.32), \
        (2868, 610000, '陕西省', 610900, '安康市', 610926, '平利县', 109.35, 32.4), \
        (2869, 610000, '陕西省', 610900, '安康市', 610927, '镇坪县', 109.52, 31.88), \
        (2870, 610000, '陕西省', 610900, '安康市', 610928, '旬阳县', 109.38, 32.83), \
        (2871, 610000, '陕西省', 610900, '安康市', 610929, '白河县', 110.1, 32.82), \
        (2872, 610000, '陕西省', 611000, '商洛市', 611001, '市辖区', 109.93, 33.87), \
        (2873, 610000, '陕西省', 611000, '商洛市', 611002, '商州区', 109.93, 33.87), \
        (2874, 610000, '陕西省', 611000, '商洛市', 611021, '洛南县', 110.13, 34.08), \
        (2875, 610000, '陕西省', 611000, '商洛市', 611022, '丹凤县', 110.33, 33.7), \
        (2876, 610000, '陕西省', 611000, '商洛市', 611023, '商南县', 110.88, 33.53), \
        (2877, 610000, '陕西省', 611000, '商洛市', 611024, '山阳县', 109.88, 33.53), \
        (2878, 610000, '陕西省', 611000, '商洛市', 611025, '镇安县', 109.15, 33.43), \
        (2879, 610000, '陕西省', 611000, '商洛市', 611026, '柞水县', 109.1, 33.68), \
        (2880, 620000, '甘肃省', 620100, '兰州市', 620101, '市辖区', 103.82, 36.07), \
        (2881, 620000, '甘肃省', 620100, '兰州市', 620102, '城关区', 103.83, 36.05), \
        (2882, 620000, '甘肃省', 620100, '兰州市', 620103, '七里河区', 0, 0), \
        (2883, 620000, '甘肃省', 620100, '兰州市', 620104, '西固区', 103.62, 36.1), \
        (2884, 620000, '甘肃省', 620100, '兰州市', 620105, '安宁区', 0, 0),
        (2885, 620000, '甘肃省', 620100, '兰州市', 620111, '红古区', 102.87, 36.33),
        (2886, 620000, '甘肃省', 620100, '兰州市', 620121, '永登县', 103.27, 36.73),
        (2887, 620000, '甘肃省', 620100, '兰州市', 620122, '皋兰县', 103.95, 36.33),
        (2888, 620000, '甘肃省', 620100, '兰州市', 620123, '榆中县', 104.12, 35.85),
        (2889, 620000, '甘肃省', 620200, '嘉峪关市', 620201, '市辖区', 98.27, 39.8),
        (2890, 620000, '甘肃省', 620300, '金昌市', 620301, '市辖区', 102.18, 38.5),
        (2891, 620000, '甘肃省', 620300, '金昌市', 620302, '金川区', 102.18, 38.5),
        (2892, 620000, '甘肃省', 620300, '金昌市', 620321, '永昌县', 101.97, 38.25),
        (2893, 620000, '甘肃省', 620400, '白银市', 620401, '市辖区', 104.18, 36.55),
        (2894, 620000, '甘肃省', 620400, '白银市', 620402, '白银区', 104.18, 36.55),
        (2895, 620000, '甘肃省', 620400, '白银市', 620403, '平川区', 104.83, 36.73),
        (2896, 620000, '甘肃省', 620400, '白银市', 620421, '靖远县', 104.68, 36.57),
        (2897, 620000, '甘肃省', 620400, '白银市', 620422, '会宁县', 105.05, 35.7),
        (2898, 620000, '甘肃省', 620400, '白银市', 620423, '景泰县', 104.07, 37.15),
        (2899, 620000, '甘肃省', 620500, '天水市', 620501, '市辖区', 105.72, 34.58),
        (2900, 620000, '甘肃省', 620500, '天水市', 620502, '秦城区', 0, 0),
        (2901, 620000, '甘肃省', 620500, '天水市', 620503, '北道区', 0, 0),
        (2902, 620000, '甘肃省', 620500, '天水市', 620521, '清水县', 106.13, 34.75),
        (2903, 620000, '甘肃省', 620500, '天水市', 620522, '秦安县', 105.67, 34.87),
        (2904, 620000, '甘肃省', 620500, '天水市', 620523, '甘谷县', 105.33, 34.73),
        (2905, 620000, '甘肃省', 620500, '天水市', 620524, '武山县', 104.88, 34.72),
        (2906, 620000, '甘肃省', 620500, '天水市', 620525, '张家川回族自治县', 106.22, 35),
        (2907, 620000, '甘肃省', 620600, '武威市', 620601, '市辖区', 102.63, 37.93),
        (2908, 620000, '甘肃省', 620600, '武威市', 620602, '凉州区', 102.63, 37.93),
        (2909, 620000, '甘肃省', 620600, '武威市', 620621, '民勤县', 103.08, 38.62),
        (2910, 620000, '甘肃省', 620600, '武威市', 620622, '古浪县', 102.88, 37.47),
        (2911, 620000, '甘肃省', 620600, '武威市', 620623, '天祝藏族自治县', 103.13, 36.98),
        (2912, 620000, '甘肃省', 620700, '张掖市', 620701, '市辖区', 100.45, 38.93),
        (2913, 620000, '甘肃省', 620700, '张掖市', 620702, '甘州区', 100.45, 38.93),
        (2914, 620000, '甘肃省', 620700, '张掖市', 620721, '肃南裕固族自治县', 99.62, 38.83),
        (2915, 620000, '甘肃省', 620700, '张掖市', 620722, '民乐县', 100.82, 38.43),
        (2916, 620000, '甘肃省', 620700, '张掖市', 620723, '临泽县', 100.17, 39.13),
        (2917, 620000, '甘肃省', 620700, '张掖市', 620724, '高台县', 99.82, 39.38),
        (2918, 620000, '甘肃省', 620700, '张掖市', 620725, '山丹县', 101.08, 38.78),
        (2919, 620000, '甘肃省', 620800, '平凉市', 620801, '市辖区', 106.67, 35.55),
        (2920, 620000, '甘肃省', 620800, '平凉市', 620802, '崆峒区', 106.67, 35.55),
        (2921, 620000, '甘肃省', 620800, '平凉市', 620821, '泾川县', 107.37, 35.33),
        (2922, 620000, '甘肃省', 620800, '平凉市', 620822, '灵台县', 107.62, 35.07),
        (2923, 620000, '甘肃省', 620800, '平凉市', 620823, '崇信县', 107.03, 35.3),
        (2924, 620000, '甘肃省', 620800, '平凉市', 620824, '华亭县', 106.65, 35.22),
        (2925, 620000, '甘肃省', 620800, '平凉市', 620825, '庄浪县', 106.05, 35.2),
        (2926, 620000, '甘肃省', 620800, '平凉市', 620826, '静宁县', 105.72, 35.52),
        (2927, 620000, '甘肃省', 620900, '酒泉市', 620901, '市辖区', 98.52, 39.75),
        (2928, 620000, '甘肃省', 620900, '酒泉市', 620902, '肃州区', 98.52, 39.75),
        (2929, 620000, '甘肃省', 620900, '酒泉市', 620921, '金塔县', 98.9, 39.98),
        (2930, 620000, '甘肃省', 620900, '酒泉市', 620922, '瓜州县', 0, 0),
        (2931, 620000, '甘肃省', 620900, '酒泉市', 620923, '肃北蒙古族自治县', 94.88, 39.52),
        (2932, 620000, '甘肃省', 620900, '酒泉市', 620924, '阿克塞哈萨克族自治县', 94.33, 39.63),
        (2933, 620000, '甘肃省', 620900, '酒泉市', 620981, '玉门市', 97.05, 40.28),
        (2934, 620000, '甘肃省', 620900, '酒泉市', 620982, '敦煌市', 94.67, 40.13),
        (2935, 620000, '甘肃省', 621000, '庆阳市', 621001, '市辖区', 107.63, 35.73),
        (2936, 620000, '甘肃省', 621000, '庆阳市', 621002, '西峰区', 107.63, 35.73),
        (2937, 620000, '甘肃省', 621000, '庆阳市', 621021, '庆城县', 107.88, 36),
        (2938, 620000, '甘肃省', 621000, '庆阳市', 621022, '环县', 107.3, 36.58),
        (2939, 620000, '甘肃省', 621000, '庆阳市', 621023, '华池县', 107.98, 36.47),
        (2940, 620000, '甘肃省', 621000, '庆阳市', 621024, '合水县', 108.02, 35.82),
        (2941, 620000, '甘肃省', 621000, '庆阳市', 621025, '正宁县', 108.37, 35.5),
        (2942, 620000, '甘肃省', 621000, '庆阳市', 621026, '宁县', 107.92, 35.5),
        (2943, 620000, '甘肃省', 621000, '庆阳市', 621027, '镇原县', 107.2, 35.68),
        (2944, 620000, '甘肃省', 621100, '定西市', 621101, '市辖区', 104.62, 35.58),
        (2945, 620000, '甘肃省', 621100, '定西市', 621102, '安定区', 104.62, 35.58),
        (2946, 620000, '甘肃省', 621100, '定西市', 621121, '通渭县', 105.25, 35.2),
        (2947, 620000, '甘肃省', 621100, '定西市', 621122, '陇西县', 104.63, 35),
        (2948, 620000, '甘肃省', 621100, '定西市', 621123, '渭源县', 104.22, 35.13),
        (2949, 620000, '甘肃省', 621100, '定西市', 621124, '临洮县', 103.87, 35.38),
        (2950, 620000, '甘肃省', 621100, '定西市', 621125, '漳县', 104.47, 34.85),
        (2951, 620000, '甘肃省', 621100, '定西市', 621126, '岷县', 104.03, 34.43),
        (2952, 620000, '甘肃省', 621200, '陇南市', 621201, '市辖区', 104.92, 33.4),
        (2953, 620000, '甘肃省', 621200, '陇南市', 621202, '武都区', 104.92, 33.4),
        (2954, 620000, '甘肃省', 621200, '陇南市', 621221, '成县', 105.72, 33.73),
        (2955, 620000, '甘肃省', 621200, '陇南市', 621222, '文县', 104.68, 32.95),
        (2956, 620000, '甘肃省', 621200, '陇南市', 621223, '宕昌县', 104.38, 34.05),
        (2957, 620000, '甘肃省', 621200, '陇南市', 621224, '康县', 105.6, 33.33),
        (2958, 620000, '甘肃省', 621200, '陇南市', 621225, '西和县', 105.3, 34.02),
        (2959, 620000, '甘肃省', 621200, '陇南市', 621226, '礼县', 105.17, 34.18),
        (2960, 620000, '甘肃省', 621200, '陇南市', 621227, '徽县', 106.08, 33.77),
        (2961, 620000, '甘肃省', 621200, '陇南市', 621228, '两当县', 106.3, 33.92),
        (2962, 620000, '甘肃省', 622900, '临夏回族自治州', 622901, '临夏市', 103.22, 35.6),
        (2963, 620000, '甘肃省', 622900, '临夏回族自治州', 622921, '临夏县', 103, 35.5),
        (2964, 620000, '甘肃省', 622900, '临夏回族自治州', 622922, '康乐县', 103.72, 35.37),
        (2965, 620000, '甘肃省', 622900, '临夏回族自治州', 622923, '永靖县', 103.32, 35.93),
        (2966, 620000, '甘肃省', 622900, '临夏回族自治州', 622924, '广河县', 103.58, 35.48),
        (2967, 620000, '甘肃省', 622900, '临夏回族自治州', 622925, '和政县', 103.35, 35.43),
        (2968, 620000, '甘肃省', 622900, '临夏回族自治州', 622926, '东乡族自治县', 103.4, 35.67),
        (2969, 620000, '甘肃省', 622900, '临夏回族自治州', 622927, '积石山保安族东乡族撒拉族自治县', 0, 0),
        (2970, 620000, '甘肃省', 623000, '甘南藏族自治州', 623001, '合作市', 102.92, 34.98),
        (2971, 620000, '甘肃省', 623000, '甘南藏族自治州', 623021, '临潭县', 103.35, 34.7),
        (2972, 620000, '甘肃省', 623000, '甘南藏族自治州', 623022, '卓尼县', 103.5, 34.58),
        (2973, 620000, '甘肃省', 623000, '甘南藏族自治州', 623023, '舟曲县', 104.37, 33.78),
        (2974, 620000, '甘肃省', 623000, '甘南藏族自治州', 623024, '迭部县', 103.22, 34.05),
        (2975, 620000, '甘肃省', 623000, '甘南藏族自治州', 623025, '玛曲县', 102.07, 34),
        (2976, 620000, '甘肃省', 623000, '甘南藏族自治州', 623026, '碌曲县', 102.48, 34.58),
        (2977, 620000, '甘肃省', 623000, '甘南藏族自治州', 623027, '夏河县', 102.52, 35.2),
        (2978, 630000, '青海省', 630100, '西宁市', 630101, '市辖区', 101.78, 36.62),
        (2979, 630000, '青海省', 630100, '西宁市', 630102, '城东区', 101.8, 36.62),
        (2980, 630000, '青海省', 630100, '西宁市', 630103, '城中区', 101.78, 36.62),
        (2981, 630000, '青海省', 630100, '西宁市', 630104, '城西区', 101.77, 36.62),
        (2982, 630000, '青海省', 630100, '西宁市', 630105, '城北区', 101.77, 36.67),
        (2983, 630000, '青海省', 630100, '西宁市', 630121, '大通回族土族自治县', 101.68, 36.93),
        (2984, 630000, '青海省', 630100, '西宁市', 630122, '湟中县', 101.57, 36.5),
        (2985, 630000, '青海省', 630100, '西宁市', 630123, '湟源县', 101.27, 36.68),
        (2986, 630000, '青海省', 632100, '海东地区', 632121, '平安县', 102.12, 36.5),
        (2987, 630000, '青海省', 632100, '海东地区', 632122, '民和回族土族自治县', 102.8, 36.33),
        (2988, 630000, '青海省', 632100, '海东地区', 632123, '乐都县', 102.4, 36.48),
        (2989, 630000, '青海省', 632100, '海东地区', 632126, '互助土族自治县', 101.95, 36.83),
        (2990, 630000, '青海省', 632100, '海东地区', 632127, '化隆回族自治县', 102.27, 36.1),
        (2991, 630000, '青海省', 632100, '海东地区', 632128, '循化撒拉族自治县', 102.48, 35.85),
        (2992, 630000, '青海省', 632200, '海北藏族自治州', 632221, '门源回族自治县', 101.62, 37.38),
        (2993, 630000, '青海省', 632200, '海北藏族自治州', 632222, '祁连县', 100.25, 38.18),
        (2994, 630000, '青海省', 632200, '海北藏族自治州', 632223, '海晏县', 100.98, 36.9),
        (2995, 630000, '青海省', 632200, '海北藏族自治州', 632224, '刚察县', 100.13, 37.33),
        (2996, 630000, '青海省', 632300, '黄南藏族自治州', 632321, '同仁县', 102.02, 35.52),
        (2997, 630000, '青海省', 632300, '黄南藏族自治州', 632322, '尖扎县', 102.03, 35.93),
        (2998, 630000, '青海省', 632300, '黄南藏族自治州', 632323, '泽库县', 101.47, 35.03),
        (2999, 630000, '青海省', 632300, '黄南藏族自治州', 632324, '河南蒙古族自治县', 101.6, 34.73),
        (3000, 630000, '青海省', 632500, '海南藏族自治州', 632521, '共和县', 100.62, 36.28),
        (3001, 630000, '青海省', 632500, '海南藏族自治州', 632522, '同德县', 100.57, 35.25),
        (3002, 630000, '青海省', 632500, '海南藏族自治州', 632523, '贵德县', 101.43, 36.05),
        (3003, 630000, '青海省', 632500, '海南藏族自治州', 632524, '兴海县', 99.98, 35.58),
        (3004, 630000, '青海省', 632500, '海南藏族自治州', 632525, '贵南县', 100.75, 35.58),
        (3005, 630000, '青海省', 632600, '果洛藏族自治州', 632621, '玛沁县', 100.23, 34.48),
        (3006, 630000, '青海省', 632600, '果洛藏族自治州', 632622, '班玛县', 100.73, 32.93),
        (3007, 630000, '青海省', 632600, '果洛藏族自治州', 632623, '甘德县', 99.9, 33.97),
        (3008, 630000, '青海省', 632600, '果洛藏族自治州', 632624, '达日县', 99.65, 33.75),
        (3009, 630000, '青海省', 632600, '果洛藏族自治州', 632625, '久治县', 101.48, 33.43),
        (3010, 630000, '青海省', 632600, '果洛藏族自治州', 632626, '玛多县', 98.18, 34.92),
        (3011, 630000, '青海省', 632700, '玉树藏族自治州', 632721, '玉树县', 97.02, 33),
        (3012, 630000, '青海省', 632700, '玉树藏族自治州', 632722, '杂多县', 95.3, 32.9),
        (3013, 630000, '青海省', 632700, '玉树藏族自治州', 632723, '称多县', 97.1, 33.37),
        (3014, 630000, '青海省', 632700, '玉树藏族自治州', 632724, '治多县', 95.62, 33.85),
        (3015, 630000, '青海省', 632700, '玉树藏族自治州', 632725, '囊谦县', 96.48, 32.2),
        (3016, 630000, '青海省', 632700, '玉树藏族自治州', 632726, '曲麻莱县', 95.8, 34.13),
        (3017, 630000, '青海省', 632800, '海西蒙古族藏族自治', 632801, '格尔木市', 94.9, 36.42),
        (3018, 630000, '青海省', 632800, '海西蒙古族藏族自治', 632802, '德令哈市', 97.37, 37.37),
        (3019, 630000, '青海省', 632800, '海西蒙古族藏族自治', 632821, '乌兰县', 98.48, 36.93),
        (3020, 630000, '青海省', 632800, '海西蒙古族藏族自治', 632822, '都兰县', 98.08, 36.3),
        (3021, 630000, '青海省', 632800, '海西蒙古族藏族自治', 632823, '天峻县', 99.02, 37.3),
        (3022, 640000, '宁夏回', 640100, '银川市', 640101, '市辖区', 106.28, 38.47),
        (3023, 640000, '宁夏回', 640100, '银川市', 640104, '兴庆区', 106.28, 38.48),
        (3024, 640000, '宁夏回', 640100, '银川市', 640105, '西夏区', 106.18, 38.48),
        (3025, 640000, '宁夏回', 640100, '银川市', 640106, '金凤区', 106.25, 38.47),
        (3026, 640000, '宁夏回', 640100, '银川市', 640121, '永宁县', 106.25, 38.28),
        (3027, 640000, '宁夏回', 640100, '银川市', 640122, '贺兰县', 106.35, 38.55),
        (3028, 640000, '宁夏回', 640100, '银川市', 640181, '灵武市', 106.33, 38.1),
        (3029, 640000, '宁夏回', 640200, '石嘴山市', 640201, '市辖区', 106.38, 39.02),
        (3030, 640000, '宁夏回', 640200, '石嘴山市', 640202, '大武口区', 106.38, 39.02),
        (3031, 640000, '宁夏回', 640200, '石嘴山市', 640205, '惠农区', 106.78, 39.25),
        (3032, 640000, '宁夏回', 640200, '石嘴山市', 640221, '平罗县', 106.53, 38.9),
        (3033, 640000, '宁夏回', 640300, '吴忠市', 640301, '市辖区', 106.2, 37.98),
        (3034, 640000, '宁夏回', 640300, '吴忠市', 640302, '利通区', 106.2, 37.98),
        (3035, 640000, '宁夏回', 640300, '吴忠市', 640323, '盐池县', 107.4, 37.78),
        (3036, 640000, '宁夏回', 640300, '吴忠市', 640324, '同心县', 105.92, 36.98),
        (3037, 640000, '宁夏回', 640300, '吴忠市', 640381, '青铜峡市', 106.07, 38.02),
        (3038, 640000, '宁夏回', 640400, '固原市', 640401, '市辖区', 106.28, 36),
        (3039, 640000, '宁夏回', 640400, '固原市', 640402, '原州区', 106.28, 36),
        (3040, 640000, '宁夏回', 640400, '固原市', 640422, '西吉县', 105.73, 35.97),
        (3041, 640000, '宁夏回', 640400, '固原市', 640423, '隆德县', 106.12, 35.62),
        (3042, 640000, '宁夏回', 640400, '固原市', 640424, '泾源县', 106.33, 35.48),
        (3043, 640000, '宁夏回', 640400, '固原市', 640425, '彭阳县', 106.63, 35.85),
        (3044, 640000, '宁夏回', 640500, '中卫市', 640501, '市辖区', 105.18, 37.52),
        (3045, 640000, '宁夏回', 640500, '中卫市', 640502, '沙坡头区', 105.18, 37.52),
        (3046, 640000, '宁夏回', 640500, '中卫市', 640521, '中宁县', 105.67, 37.48),
        (3047, 640000, '宁夏回', 640500, '中卫市', 640522, '海原县', 105.65, 36.57),
        (3048, 650000, '新疆自', 650100, '乌鲁木齐市', 650101, '市辖区', 87.62, 43.82),
        (3049, 650000, '新疆自', 650100, '乌鲁木齐市', 650102, '天山区', 87.65, 43.78),
        (3050, 650000, '新疆自', 650100, '乌鲁木齐市', 650103, '沙依巴克区', 87.6, 43.78),
        (3051, 650000, '新疆自', 650100, '乌鲁木齐市', 650104, '新市区', 87.6, 43.85),
        (3052, 650000, '新疆自', 650100, '乌鲁木齐市', 650105, '水磨沟区', 87.63, 43.83),
        (3053, 650000, '新疆自', 650100, '乌鲁木齐市', 650106, '头屯河区', 87.42, 43.87),
        (3054, 650000, '新疆自', 650100, '乌鲁木齐市', 650107, '达坂城区', 88.3, 43.35),
        (3055, 650000, '新疆自', 650100, '乌鲁木齐市', 650108, '东山区', 87.68, 43.95),
        (3056, 650000, '新疆自', 650100, '乌鲁木齐市', 650121, '乌鲁木齐县', 87.6, 43.8),
        (3057, 650000, '新疆自', 650200, '克拉玛依市', 650201, '市辖区', 84.87, 45.6),
        (3058, 650000, '新疆自', 650200, '克拉玛依市', 650202, '独山子区', 84.85, 44.32),
        (3059, 650000, '新疆自', 650200, '克拉玛依市', 650203, '克拉玛依区', 84.87, 45.6),
        (3060, 650000, '新疆自', 650200, '克拉玛依市', 650204, '白碱滩区', 85.13, 45.7),
        (3061, 650000, '新疆自', 650200, '克拉玛依市', 650205, '乌尔禾区', 85.68, 46.08),
        (3062, 650000, '新疆自', 652100, '吐鲁番地区', 652101, '吐鲁番市', 89.17, 42.95),
        (3063, 650000, '新疆自', 652100, '吐鲁番地区', 652122, '鄯善县', 90.22, 42.87),
        (3064, 650000, '新疆自', 652100, '吐鲁番地区', 652123, '托克逊县', 88.65, 42.78),
        (3065, 650000, '新疆自', 652200, '哈密地区', 652201, '哈密市', 93.52, 42.83),
        (3066, 650000, '新疆自', 652200, '哈密地区', 652222, '巴里坤哈萨克自治县', 0, 0),
        (3067, 650000, '新疆自', 652200, '哈密地区', 652223, '伊吾县', 94.7, 43.25),
        (3068, 650000, '新疆自', 652300, '昌吉回族自治州', 652301, '昌吉市', 87.3, 44.02),
        (3069, 650000, '新疆自', 652300, '昌吉回族自治州', 652302, '阜康市', 87.98, 44.15),
        (3070, 650000, '新疆自', 652300, '昌吉回族自治州', 652303, '米泉市', 87.65, 43.97),
        (3071, 650000, '新疆自', 652300, '昌吉回族自治州', 652323, '呼图壁县', 86.9, 44.18),
        (3072, 650000, '新疆自', 652300, '昌吉回族自治州', 652324, '玛纳斯县', 86.22, 44.3),
        (3073, 650000, '新疆自', 652300, '昌吉回族自治州', 652325, '奇台县', 89.58, 44.02),
        (3074, 650000, '新疆自', 652300, '昌吉回族自治州', 652327, '吉木萨尔县', 89.18, 44),
        (3075, 650000, '新疆自', 652300, '昌吉回族自治州', 652328, '木垒哈萨克自治县', 90.28, 43.83),
        (3076, 650000, '新疆自', 652700, '博尔塔拉蒙古自治州', 652701, '博乐市', 82.07, 44.9),
        (3077, 650000, '新疆自', 652700, '博尔塔拉蒙古自治州', 652722, '精河县', 82.88, 44.6),
        (3078, 650000, '新疆自', 652700, '博尔塔拉蒙古自治州', 652723, '温泉县', 81.03, 44.97),
        (3079, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652801, '库尔勒市', 86.15, 41.77),
        (3080, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652822, '轮台县', 84.27, 41.78),
        (3081, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652823, '尉犁县', 86.25, 41.33),
        (3082, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652824, '若羌县', 88.17, 39.02),
        (3083, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652825, '且末县', 85.53, 38.13),
        (3084, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652826, '焉耆回族自治县', 86.57, 42.07),
        (3085, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652827, '和静县', 86.4, 42.32),
        (3086, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652828, '和硕县', 86.87, 42.27),
        (3087, 650000, '新疆自', 652800, '巴音郭楞蒙古自治州', 652829, '博湖县', 86.63, 41.98),
        (3088, 650000, '新疆自', 652900, '阿克苏地区', 652901, '阿克苏市', 80.27, 41.17),
        (3089, 650000, '新疆自', 652900, '阿克苏地区', 652922, '温宿县', 80.23, 41.28),
        (3090, 650000, '新疆自', 652900, '阿克苏地区', 652923, '库车县', 82.97, 41.72),
        (3091, 650000, '新疆自', 652900, '阿克苏地区', 652924, '沙雅县', 82.78, 41.22),
        (3092, 650000, '新疆自', 652900, '阿克苏地区', 652925, '新和县', 82.6, 41.55),
        (3093, 650000, '新疆自', 652900, '阿克苏地区', 652926, '拜城县', 81.87, 41.8),
        (3094, 650000, '新疆自', 652900, '阿克苏地区', 652927, '乌什县', 79.23, 41.22),
        (3095, 650000, '新疆自', 652900, '阿克苏地区', 652928, '阿瓦提县', 80.38, 40.63),
        (3096, 650000, '新疆自', 652900, '阿克苏地区', 652929, '柯坪县', 79.05, 40.5),
        (3097, 650000, '新疆自', 653000, '克孜勒苏柯尔克孜自', 653001, '阿图什市', 0, 0),
        (3098, 650000, '新疆自', 653000, '克孜勒苏柯尔克孜自', 653022, '阿克陶县', 0, 0),
        (3099, 650000, '新疆自', 653000, '克孜勒苏柯尔克孜自', 653023, '阿合奇县', 0, 0),
        (3100, 650000, '新疆自', 653000, '克孜勒苏柯尔克孜自', 653024, '乌恰县', 0, 0),
        (3101, 650000, '新疆自', 653100, '喀什地区', 653101, '喀什市', 75.98, 39.47),
        (3102, 650000, '新疆自', 653100, '喀什地区', 653121, '疏附县', 75.85, 39.38),
        (3103, 650000, '新疆自', 653100, '喀什地区', 653122, '疏勒县', 76.05, 39.4),
        (3104, 650000, '新疆自', 653100, '喀什地区', 653123, '英吉沙县', 76.17, 38.93),
        (3105, 650000, '新疆自', 653100, '喀什地区', 653124, '泽普县', 77.27, 38.18),
        (3106, 650000, '新疆自', 653100, '喀什地区', 653125, '莎车县', 77.23, 38.42),
        (3107, 650000, '新疆自', 653100, '喀什地区', 653126, '叶城县', 77.42, 37.88),
        (3108, 650000, '新疆自', 653100, '喀什地区', 653127, '麦盖提县', 77.65, 38.9),
        (3109, 650000, '新疆自', 653100, '喀什地区', 653128, '岳普湖县', 76.77, 39.23),
        (3110, 650000, '新疆自', 653100, '喀什地区', 653129, '伽师县', 76.73, 39.5),
        (3111, 650000, '新疆自', 653100, '喀什地区', 653130, '巴楚县', 78.55, 39.78),
        (3112, 650000, '新疆自', 653100, '喀什地区', 653131, '塔什库尔干塔吉克自治县', 0, 0),
        (3113, 650000, '新疆自', 653200, '和田地区', 653201, '和田市', 79.92, 37.12),
        (3114, 650000, '新疆自', 653200, '和田地区', 653221, '和田县', 79.93, 37.1),
        (3115, 650000, '新疆自', 653200, '和田地区', 653222, '墨玉县', 79.73, 37.27),
        (3116, 650000, '新疆自', 653200, '和田地区', 653223, '皮山县', 78.28, 37.62),
        (3117, 650000, '新疆自', 653200, '和田地区', 653224, '洛浦县', 80.18, 37.07),
        (3118, 650000, '新疆自', 653200, '和田地区', 653225, '策勒县', 80.8, 37),
        (3119, 650000, '新疆自', 653200, '和田地区', 653226, '于田县', 81.67, 36.85),
        (3120, 650000, '新疆自', 653200, '和田地区', 653227, '民丰县', 82.68, 37.07),
        (3121, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654002, '伊宁市', 81.32, 43.92),
        (3122, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654003, '奎屯市', 84.9, 44.42),
        (3123, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654021, '伊宁县', 81.52, 43.98),
        (3124, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654022, '察布查尔锡伯自治县', 81.15, 43.83),
        (3125, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654023, '霍城县', 80.88, 44.05),
        (3126, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654024, '巩留县', 82.23, 43.48),
        (3127, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654025, '新源县', 83.25, 43.43),
        (3128, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654026, '昭苏县', 81.13, 43.15),
        (3129, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654027, '特克斯县', 81.83, 43.22),
        (3130, 650000, '新疆自', 654000, '伊犁哈萨克自治州', 654028, '尼勒克县', 82.5, 43.78),
        (3131, 650000, '新疆自', 654200, '塔城地区', 654201, '塔城市', 82.98, 46.75),
        (3132, 650000, '新疆自', 654200, '塔城地区', 654202, '乌苏市', 84.68, 44.43),
        (3133, 650000, '新疆自', 654200, '塔城地区', 654221, '额敏县', 83.63, 46.53),
        (3134, 650000, '新疆自', 654200, '塔城地区', 654223, '沙湾县', 85.62, 44.33),
        (3135, 650000, '新疆自', 654200, '塔城地区', 654224, '托里县', 83.6, 45.93),
        (3136, 650000, '新疆自', 654200, '塔城地区', 654225, '裕民县', 82.98, 46.2),
        (3137, 650000, '新疆自', 654200, '塔城地区', 654226, '和布克赛尔蒙古自治县', 85.72, 46.8),
        (3138, 650000, '新疆自', 654300, '阿勒泰地区', 654301, '阿勒泰市', 88.13, 47.85),
        (3139, 650000, '新疆自', 654300, '阿勒泰地区', 654321, '布尔津县', 86.85, 47.7),
        (3140, 650000, '新疆自', 654300, '阿勒泰地区', 654322, '富蕴县', 89.52, 47),
        (3141, 650000, '新疆自', 654300, '阿勒泰地区', 654323, '福海县', 87.5, 47.12),
        (3142, 650000, '新疆自', 654300, '阿勒泰地区', 654324, '哈巴河县', 86.42, 48.07),
        (3143, 650000, '新疆自', 654300, '阿勒泰地区', 654325, '青河县', 90.38, 46.67),
        (3144, 650000, '新疆自', 654300, '阿勒泰地区', 654326, '吉木乃县', 85.88, 47.43),
        (3145, 650000, '新疆自', 659000, '省直辖行政单位', 659001, '石河子市', 0, 0),
        (3146, 650000, '新疆自', 659000, '省直辖行政单位', 659002, '阿拉尔市', 0, 0),
        (3147, 650000, '新疆自', 659000, '省直辖行政单位', 659003, '图木舒克市', 0, 0),
        (3148, 650000, '新疆自', 659000, '省直辖行政单位', 659004, '五家渠市', 0, 0),
        (3149, 710000, '台湾', 710100, '台湾省', 710100, '台湾', 121.5, 25.03),
        (3150, 810000, '香港', 810100, '香港特别行政区', 810100, '香港', 114.08, 22.2),
        (3151, 820000, '澳门', 820100, '澳门特别行政区', 820100, '澳门', 113.33, 22.13),
    ]
    for i in arealist:
        updatadic = {}
        updatadic["provincecode"] = i[1]
        updatadic["provincevalue"] = i[2]
        updatadic["citycode"] = i[3]
        updatadic["cityvalue"] = i[4]
        updatadic["countycode"] = i[5]
        updatadic["countyvalue"] = i[6]
        updatadic["longitude"] = i[7]
        updatadic["latitude"] = i[8]
        if local_identity.objects.filter(**updatadic):
            # print("have")
            pass
        else:
            local_identity.objects.create(**updatadic)

