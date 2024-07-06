from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from django.http import HttpResponse
import datetime,json,simplejson
from CQM.models import CQM, CQMProject, CQM_history
from .models import OBIDeviceResult, SeriesInfo, CategoryInfo
from app01.models import UserInfo, ProjectinfoinDCT
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Max,Min,Sum,Count,Q

# Create your views here.

headermodel_OBI = {
    'Customer': 'Customer', 'Project name': 'Project', 'Platform': 'Platform',
    'Series': 'Series',
    'Category': 'Category', 'Device No.': 'DeviceNo', 'P/N': 'PN', 'Device name': 'Devicename',
    'Test result': 'Testresult', 'FW version': 'FWversion', 'Software version': 'Softwareversion',
    'HW ID version': 'HWIDversion', 'Test Phase': 'TestPhase', 'Comments': 'Comments',

}

@csrf_exempt
def CQM_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/CQM_upload"
    # mock_data=[{"id":"1","Category":"USB 3.1 Gen2(沉版CH=0.36 , H=5.72, 9P, BlackTongue ,G/F , Black Ni)","Vendor":"ACON","SourcePriority":"M","CompalPN":"LTCX0093GB0","Status":"AP/AL","VendorPN":"XXX","Description":"CONN ACON GTRA0-9U1U91 9P H5.72 USB3.1","Qty":"2","Location":"JUSB2 & JUSB1","DataCodeB":"67","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"99","EMIB":"","RFB":"","DataCodeC":"1926","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":""},
    #            {"id": "2","Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)","Vendor": "HIGHSTAR","SourcePriority":"M","CompalPN": "LTCX0093HB0","Status": "AP/AL","VendorPN": "XXX", "Description": "S CONN HIGHSTAR UB11249-B200W-1H 24P H4.37 USB TYPE_C P0.25", "Qty": "2", "Location": "JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"94HK","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":"203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement 204869 The chip of HIGHSTAR DC-IN connector is skewed after DC-IN Jack strength test(X axis Drop,fail at axis +Y)"},
    #            {"id": "3", "Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)", "Vendor": "DEREN", "SourcePriority": "S1", "CompalPN": "LTCX0093IB0", "Status": "AP/AL","VendorPN": "XXX", "Description": "S CONN DEREN 560Q17-001H 24P H4.43 USB TYPE_C P0.25", "Qty": "2", "Location": "JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"DR1927Z","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":"203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement"},
    #            {"id":"4","Category":"USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)","Vendor":"LOTES","SourcePriority":"S2","CompalPN":"LTCX0094RB0","Status":"AP/AL","VendorPN":"XXX","Description":"S CONN LOTES AUSB0453-P103A11 24P H4.3 USB TYPE_C P0.25","Qty":"2","Location":"JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"N/A","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":""}]
    # selectItem = {"C38(NB)": [{"Project": "EL531", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                           {"Project": "EL532", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                           {"Project": "EL533", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                           {"Project": "EL534", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
    #               "C38(AIO)": [{"Project": "EL535", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                            {"Project": "EL536", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                            {"Project": "EL537", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                            {"Project": "EL538", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
    #               "A39": [{"Project": "EL531", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                       {"Project": "EL532", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                       {"Project": "EL533", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                       {"Project": "EL534", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
    #               "Other": [{"Project": "ELMV2", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                         {"Project": "ELMV3", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
    #                         {"Project": "ELMV4", "Phase": ["B(FVT)", "C(SIT)", "INV"]}]}
    # cc={"statu":1}
    # aa={"flag1":1}
    err_ok = 0#excel上传1为重复
    err_msg = ''
    result = 0#为1 forms 上传重复
    rpeatcontend = [
    ]


    # print(request.method)
    # print(request.POST)
    # print(request.GET)
    if request.method=="POST":
        # print(request.POST)
        canEdit = 0  # 机种权限 1有权限,前端是用的{{}}传值的，法国在上面，一进upload界面就提示没有权限
        if 'type' in request.POST:
            # print(request.POST.get('type'))
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            CQMList=[{'Customer':'Customer','Project':'Project','Phase':'Phase','Material_Group': 'Material_Group',
                     'Keyparts':'Keyparts','Character':'Character','PID':'PID',
                     'VID':'VID','HW':'HW','FW': 'FW','Supplier': 'Supplier','R1_PN_Description': 'R1_PN_Description','Compal_R1_PN': 'Compal_R1_PN','Compal_R3_PN': 'Compal_R3_PN',}]
            num = 1
            for i in simplejson.loads(xlsxlist):
                if num > 1:
                    break
                else:
                    if 'Customer' in i.keys():
                        Customer = i['Customer']
                    if 'Project' in i.keys():
                        Project = i['Project']
                    if 'Phase' in i.keys():
                        Phase = i['Phase']
                num+=1

            Check_dic_Project = {'Customer': Customer, 'Project': Project,}
            Check_dic_ProjectCQM = {'Customer': Customer, 'Project': Project, 'Phase': Phase,}
            # print(Check_dic_ProjectCQM)
            Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
            current_user = request.session.get('user_name')
            if Projectinfo:
                for k in Projectinfo.Owner.all():
                    # print(k.username,current_user)
                    # print(type(k.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
            # print(canEdit)
            if canEdit:
                #验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                rownum = 0
                startupload = 0
                for i in simplejson.loads(xlsxlist):
                    rownum += 1
                    # print(i)
                    # 同机种验证
                    if i['Project'] != Project:
                        # canEdit = 0
                        startupload = 0
                        err_ok = 2
                        err_msg = """
                    文件中包含多个机种，请检查确认，修改之后重新上传
                                        """
                        break

                    # 同Project,Phase验证，INV，OS refresh能多次上传
                    if 'Customer' in i.keys():
                        Customer = i['Customer']
                    if 'Project' in i.keys():
                        Project = i['Project']
                    if 'Phase' in i.keys():
                        Phase = i['Phase']
                    Check_dic_ProjectCQM = {'Customer': Customer, 'Project': Project, 'Phase': Phase, }

                    if Phase == "INV" or Phase == "OS refresh":
                        startupload = 1
                        pass
                    else:
                        if CQM.objects.filter(**Check_dic_ProjectCQM).first():
                            startupload = 0
                            err_ok = 2
                            err_msg = """
            同一个Project的同一个Phase，Excel上传只能使用一次
            %s-%s-%s 的数据已经存在。
                                """ % (Customer, Project, Phase)
                            break
                        else:
                            startupload = 1
                            pass
                    # Category验证，分客户别
                    if 'Customer' in i.keys():
                        if i["Customer"] == "C38(NB)":
                            CategoryCheckList = ['Active_Pen', 'Adapter', 'Battery', 'Camera', 'CPU', 'EMMC',
                                                 'Finger_Print', 'HDD',
                                                 'Keyboard', 'Memory', 'ODD', 'Panel', 'Power_Cord', 'Speaker', 'SSD',
                                                 'Touch_Pad', 'TPM',
                                                 'TCM', 'UFS', 'VRAM', 'VGA', 'WLAN', 'WWAN', 'Others', ]

                            if 'Material_Group' in i.keys():
                                if i['Material_Group'] not in CategoryCheckList:
                                    startupload = 0
                                    err_ok = 2
                                    err_msg = """
                                    第"%s"条数据的Material_Group(Category):  "%s" 不符合要求，请确认修改并重新上传。
                                    符合要求的Category列表：%s
                                    如需新增Category种类，请先联系管理者：June_Sun。
                                    """ % (rownum, i['Material_Group'], CategoryCheckList)
                                    break
                        if i["Customer"] == "C38(AIO)":
                            CategoryCheckList = ['Adapter', 'Camera', 'CPU', 'Fan',
                                                 'HDD',
                                                 'Keyboard', 'Panel', "MIC", "Mouse", 'ODD', 'Power_Cord', "Memory", 'Speaker', 'SSD',
                                                 "Stand", "Thermal module", 'VGA', 'VRAM', "Wireless KB/MS", 'WLAN+BT combo', 'Others', ]

                            if 'Material_Group' in i.keys():
                                if i['Material_Group'] not in CategoryCheckList:
                                    startupload = 0
                                    err_ok = 2
                                    err_msg = """
                                    第"%s"条数据的Material_Group(Category):  "%s" 不符合要求，请确认修改并重新上传。
                                    符合要求的Category列表：%s
                                    如需新增Category种类，请先联系管理者：Bruce_Shen。
                                    """ % (rownum, i['Material_Group'], CategoryCheckList)
                                    break
                    else:
                        startupload = 0
                        err_ok = 2
                        err_msg = """
                                    Customer不能爲空，請檢查第 "%s" 條數據的Customer
                                    """ % rownum
                        break
                    # 結果验证，不分客户别
                    ResultList = ["Qd", "Qd_L", "Qd_C", "T", "F", "DisQ", "Drpd", "No Build"]
                    if 'Reliability' in i.keys():
                        if i['Reliability'] not in ResultList:
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                        第"%s"条数据的Reliability: "%s" 不符合要求，请确认修改并重新上传。
                        符合要求的Reliability列表：%s
                        """ % (rownum, i['Reliability'], ResultList)
                            break
                    if 'Compatibility' in i.keys():
                        if i['Compatibility'] not in ResultList:
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                        第"%s"条数据的Compatibility: "%s" 不符合要求，请确认修改并重新上传。
                        符合要求的Compatibility列表：%s
                        """ % (rownum, i['Compatibility'], ResultList)
                            break
                    if 'Testresult' in i.keys():
                        if i['Testresult'] not in ResultList:
                            startupload = 0
                            err_ok = 2
                            err_msg = """
                        第"%s"条数据的Testresult: "%s" 不符合要求，请确认修改并重新上传。
                        符合要求的Testresult列表：%s
                        """ % (rownum, i['Testresult'], ResultList)
                            break

                if startupload:
                    for i in simplejson.loads(xlsxlist):

                        Check_dic = {"Projectinfo": Projectinfo,
                                     # 'Customer': i['Customer'], 'Project': i['Project'],
                                     # 'Phase': i['Phase'],
                                     # 'Material_Group': i['Material_Group'],
                                     # 'Keyparts': i['Keyparts'],
                                     # 'Character': i['Character'],
                                     # 'PID': i['PID'],
                                     # 'VID': i['VID'],
                                     # 'HW': i['HW'], 'FW': i['FW'],
                                     # 'Supplier': i['Supplier'],
                                     # 'R1_PN_Description': i['R1_PN_Description'],
                                     # 'Compal_R1_PN': i['Compal_R1_PN'],
                                     # 'Compal_R3_PN': i['Compal_R3_PN'],
                                     }
                        # print(Check_dic)
                        exsitdata={}
                        if 'Customer' in i.keys():
                            Check_dic['Customer'] = i['Customer']
                            exsitdata['Customer'] = i['Customer']
                        else:
                            exsitdata['Customer']=''
                        if 'Project' in i.keys():
                            Check_dic['Project'] = i['Project']
                            exsitdata['Project'] = i['Project']
                        else:
                            exsitdata['Project'] =''
                        if 'Phase' in i.keys():
                            Check_dic['Phase'] = i['Phase']
                            exsitdata['Phase'] = i['Phase']
                        else:
                            exsitdata['Phase'] =''
                        if 'Material_Group' in i.keys():
                            Check_dic['Material_Group'] = i['Material_Group']
                            exsitdata['Material_Group'] = i['Material_Group']
                        else:
                            exsitdata['Material_Group'] =''
                        if 'Keyparts' in i.keys():
                            Check_dic['Keyparts'] = i['Keyparts']
                            exsitdata['Keyparts'] = i['Keyparts']
                        else:
                            exsitdata['Keyparts'] =''
                        if 'Character' in i.keys():
                            Check_dic['Character'] = i['Character']
                            exsitdata['Character'] = i['Character']
                        else:
                            exsitdata['Character'] =''
                        if 'PID' in i.keys():
                            Check_dic['PID'] = i['PID']
                            exsitdata['PID'] = i['PID']
                        else:
                            exsitdata['PID'] =''
                        if 'VID' in i.keys():
                            Check_dic['VID'] = i['VID']
                            exsitdata['VID'] = i['VID']
                        else:
                            exsitdata['VID'] =''
                        if 'HW' in i.keys():
                            Check_dic['HW'] = i['HW']
                            exsitdata['HW'] = i['HW']
                        else:
                            exsitdata['HW'] =''
                        if 'FW' in i.keys():
                            Check_dic['FW'] = i['FW']
                            exsitdata['FW'] = i['FW']
                        else:
                            exsitdata['FW'] =''
                        if 'Supplier' in i.keys():
                            Check_dic['Supplier'] = i['Supplier']
                            exsitdata['Supplier'] = i['Supplier']
                        else:
                            exsitdata['Supplier'] =''
                        if 'R1_PN_Description' in i.keys():
                            Check_dic['R1_PN_Description'] = i['R1_PN_Description']
                            exsitdata['R1_PN_Description'] = i['R1_PN_Description']
                        else:
                            exsitdata['R1_PN_Description'] =''
                        if 'Compal_R1_PN' in i.keys():
                            Check_dic['Compal_R1_PN'] = i['Compal_R1_PN']
                            exsitdata['Compal_R1_PN'] = i['Compal_R1_PN']
                        else:
                            exsitdata['Compal_R1_PN'] =''
                        if 'Compal_R3_PN' in i.keys():
                            Check_dic['Compal_R3_PN'] = i['Compal_R3_PN']
                            exsitdata['Compal_R3_PN'] = i['Compal_R3_PN']
                        else:
                            exsitdata['Compal_R3_PN'] =''
                        if CQM.objects.filter(**Check_dic).first():#已存在的不覆盖，提示去edit修改,如果允许excel修改的话这里需要将CQM_history也记录下来
                            err_ok = 1
                            CQMList.append(exsitdata)
                        else:
                            updatedic = {}
                            updatedic['Projectinfo'] = Projectinfo
                            for j in i.keys():
                                if j == 'Comments':
                                    if i[j]:
                                        updatedic[j] = request.session.get('user_name') + '(%s)' % datetime.datetime.now().strftime(
                                            "%Y-%m-%d %H:%M:%S") + ":" + '\n' + i[j]

                                        # print(updatedic[j])
                                else:
                                    updatedic[j] = i[j]
                            updatedic['editor'] = request.session.get('user_name')
                            updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            CQM.objects.create(**updatedic)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": canEdit,
                'content': CQMList
            }
            # print(datajason)

            return HttpResponse(json.dumps(datajason), content_type="application/json")
    return render(request, 'CQM/CQM_upload.html', locals())

@csrf_exempt
def OBIDeviceResult_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "OBIDeviceResult/edit"

    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5,3", "Category": "Cabel&Adapter", "Device_No": "21830", "PN": "4Y50Q64661",
        #  "Device_Name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "Qd_C", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
        # {"id": "2", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5, 3", "Category": "Cabel&Adapter", "Device_No": "21831", "PN": "4Y50Q64661",
        #  "Device_Name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "Qd_C", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
        # {"id": "3", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5, 3", "Category": "Cabel&Adapter", "Device_No": "21830", "PN": "4Y50Q64661",
        #  "Device_Name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "Qd_C", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39"
    ]

    selectProjectName = [
        # {"value": "GLA34"}, {"value": "FLMA0"}, {"value": "FLMS0"}
    ]

    sectionPlatform = [
        # "Intel Tiger lake-C", "Intel Ice lake", "AMD Lucienne",
    ]

    selectPN = [
        # {"value": "4Y50U45359"}, {"value": "GY50X79384"}, {"value": "4Y40Z48977"}
    ]


    sectionSeries = [
            # "SMB", "Consumer 7,9,5,3",
        ]

    sectionCategory = [
        # "SMB", "Consumer 7,9,5,3",
    ]


    canEdit = 0  # 编辑机种的权限
    errMsg = '上傳成功'#excel 上傳
    errMsgNumber = ''#add

    for i in CQMProject.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    for i in CQMProject.objects.all().values("Project").distinct().order_by("Project"):
        selectProjectName.append({"value": i["Project"]})
    for i in ProjectinfoinDCT.objects.all().values("Platform").distinct().order_by("Platform"):
        sectionPlatform.append(i["Platform"])
    for i in OBIDeviceResult.objects.all().values("PN").distinct().order_by("PN"):
        selectPN.append({"value": i["PN"]})

    for i in SeriesInfo.objects.all().values("Series").distinct().order_by("Series"):
        sectionSeries.append(i["Series"])
    for i in CategoryInfo.objects.all().values("Category").distinct().order_by("Category"):
        sectionCategory.append(i["Category"])

    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    # print(roles)
    editPpriority = 100
    for i in roles:
        if i == 'admin':
            editPpriority = 4
        elif 'PM' in i:
            if editPpriority != 4:
                editPpriority = 1
        elif 'RD' in i:
            if editPpriority != 4 and editPpriority != 1:
                editPpriority = 2
        elif 'DQA' in i:
            if 'DQA_SW' in i:
                if editPpriority != 4 and editPpriority != 1:
                    editPpriority = 5
            if 'DQA_ME' in i:
                if editPpriority != 4 and editPpriority != 1:
                    editPpriority = 6
            if 'DQA_INV' in i:
                if editPpriority != 4 and editPpriority != 1:
                    editPpriority = 4
        elif "JQE" in i:
            editPpriority = 3
        else:
            editPpriority = 0
    cc = {"statu": editPpriority}
    # print(editPpriority)
    alert=0
    # print(request.POST)
    # print(request.body)
    if request.method == "POST":
        if request.POST:
            if request.POST.get('isGetData') == 'SEARCH':
                current_user = request.session.get('user_name')
                if request.POST.get('ProjectName') and request.POST.get('Customer'):
                    Projectinfo = CQMProject.objects.filter(Project=request.POST.get('ProjectName')).first()
                    if Projectinfo.Customer == request.POST.get('Customer'):
                        for k in Projectinfo.Owner.all():
                            # print(i.username,current_user)
                            # print(type(i.username),type(current_user))
                            if k.username == current_user:
                                canEdit = 1
                                break

                check_dic = {}
                Customer = request.POST.get('Customer')
                ProjectName = request.POST.get('ProjectName')
                Platform = request.POST.get('Platform')
                PN = request.POST.get('PN')
                if Customer:
                    check_dic['Customer'] = Customer
                if ProjectName:
                    check_dic['Project'] = ProjectName
                if Platform:
                    check_dic['Platform'] = Platform
                if PN:
                    check_dic['PN'] = PN
                # print(check_dic)
                if check_dic:
                    check_Result = OBIDeviceResult.objects.filter(**check_dic)
                else:
                    check_Result = OBIDeviceResult.objects.all()
                for i in check_Result:
                    mock_data.append({"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
             "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
             "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
             "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion, "Test_Phase": i.TestPhase, "Comments": i.Comments},)
                # print(mock_data)
            if request.POST.get('action') == 'submit':
                adddic = {"Customer": request.POST.get('Customer'), "Project": request.POST.get('ProjectName'),
                          "Platform": request.POST.get('Platform'),"Series": request.POST.get('Series'),
                          "Category": request.POST.get('Category'), "DeviceNo": request.POST.get('DeviceNo'),
                          "PN": request.POST.get('PN'),"Devicename": request.POST.get('DeviceName'),
                          "Testresult": request.POST.get('TestResult'), "FWversion": request.POST.get('FWVer'),
                          "Softwareversion": request.POST.get('SoftwareVer'), "HWIDversion": request.POST.get('HWID_ver'),
                          "TestPhase": request.POST.get('TestPhase'), "Comments": request.POST.get('Comments'),
                          "editor": request.session.get('user_name'),
                          "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          }
                adddiccheck = {"Project": request.POST.get('ProjectName'),
                          "DeviceNo": request.POST.get('DeviceNo'),
                          }
                if request.POST.get('ProjectName') == request.POST.get('ProjectNameSearch'):
                    if OBIDeviceResult.objects.filter(**adddiccheck):
                        errMsgNumber = "機種：%s，DeviceNo：%s 數據已經存在" % (request.POST.get('ProjectName'), request.POST.get('DeviceNo'))
                    else:
                        OBIDeviceResult.objects.create(**adddic)
                else:
                    errMsgNumber = "機種名稱不對"

                #mock_data
                check_dic = {}
                Customer = request.POST.get('CustomerSearch')
                ProjectName = request.POST.get('ProjectNameSearch')
                Platform = request.POST.get('PlatformSearch')
                PN = request.POST.get('PNSearch')
                if Customer:
                    check_dic['Customer'] = Customer
                if ProjectName:
                    check_dic['Project'] = ProjectName
                if Platform:
                    check_dic['Platform'] = Platform
                if PN:
                    check_dic['PN'] = PN
                # print(check_dic)
                if check_dic:
                    check_Result = OBIDeviceResult.objects.filter(**check_dic)
                else:
                    check_Result = OBIDeviceResult.objects.all()
                for i in check_Result:
                    mock_data.append({"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
             "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
             "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
             "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion, "Test_Phase": i.TestPhase, "Comments": i.Comments},)
                # print(mock_data)
            if request.POST.get('action') == 'SAVE':
                updatedic = {"Customer": request.POST.get('Customer'), "Project": request.POST.get('ProjectName'),
                          "Platform": request.POST.get('Platform'), "Series": request.POST.get('Series'),
                          "Category": request.POST.get('Category'), "DeviceNo": request.POST.get('DeviceNo'),
                          "PN": request.POST.get('PN'), "Devicename": request.POST.get('DeviceName'),
                          "Testresult": request.POST.get('TestResult'), "FWversion": request.POST.get('FWVer'),
                          "Softwareversion": request.POST.get('SoftwareVer'),
                          "HWIDversion": request.POST.get('HWID_ver'),
                          "TestPhase": request.POST.get('TestPhase'), "Comments": request.POST.get('Comments'),
                          "editor": request.session.get('user_name'), "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }


                OBIDeviceResult.objects.filter(id=request.POST.get('id')).update(**updatedic)
                # mock_data
                check_dic = {}
                Customer = request.POST.get('CustomerSearch')
                ProjectName = request.POST.get('ProjectNameSearch')
                Platform = request.POST.get('PlatformSearch')
                PN = request.POST.get('PNSearch')
                if Customer:
                    check_dic['Customer'] = Customer
                if ProjectName:
                    check_dic['Project'] = ProjectName
                if Platform:
                    check_dic['Platform'] = Platform
                if PN:
                    check_dic['PN'] = PN
                # print(check_dic)
                if check_dic:
                    check_Result = OBIDeviceResult.objects.filter(**check_dic)
                else:
                    check_Result = OBIDeviceResult.objects.all()
                for i in check_Result:
                    mock_data.append(
                        {"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
                         "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
                         "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
                         "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion, "Test_Phase": i.TestPhase,
                         "Comments": i.Comments}, )
                # print(mock_data)

        else:
            try:
                request.body
                # print(request.body)
            except:
                # print('1')
                pass
            else:
                # print('2')
                if 'MUTICANCEL' in str(request.body):
                    # print("1", request.POST.getlist['params'])
                    responseData = json.loads(request.body)
                    # print(responseData)
                    for i in responseData['params']:
                        # for j in CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)):
                        #     print(j)
                        # CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)).delete()
                        OBIDeviceResult.objects.get(id=i).delete()

                    Customer = responseData['Customer']
                    ProjectName = responseData['ProjectName']
                    Platform = responseData['Platform']
                    PN = responseData['PN']
                    check_dic = {}
                    if Customer:
                        check_dic['Customer'] = Customer
                    if ProjectName:
                        check_dic['Project'] = ProjectName
                    if Platform:
                        check_dic['Platform'] = Platform
                    if PN:
                        check_dic['PN'] = PN
                    # print(check_dic)
                    if check_dic:
                        check_Result = OBIDeviceResult.objects.filter(**check_dic)
                    else:
                        check_Result = OBIDeviceResult.objects.all()
                    for i in check_Result:
                        mock_data.append(
                            {"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
                             "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
                             "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
                             "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion, "Test_Phase": i.TestPhase,
                             "Comments": i.Comments}, )
                    # print(mock_data)
                if 'ExcelData' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    checkOBI = {}
                    Customer = responseData['Customer']
                    if Customer and Customer != "All":
                        checkOBI['Customer'] = Customer
                    ProjectName = responseData['ProjectName']
                    if ProjectName and ProjectName != "All":
                        checkOBI['Project'] = ProjectName
                    Platform = responseData['Platform']
                    if Platform and Platform != "All":
                        checkOBI['Platform'] = Platform
                    PN = responseData['PN']
                    if PN and PN != "All":
                        checkOBI['PN'] = PN

                    xlsxlist = json.loads(responseData['ExcelData'])
                    # Adapterlist = [
                    #     {
                    #         'Number': '編號', }
                    # ]
                    rownum = 0
                    startupload = 0
                    # print(xlsxlist)
                    uploadxlsxlist = []
                    for i in xlsxlist:
                        # print(type(i),i)
                        rownum += 1
                        # print(rownum)
                        modeldata = {}
                        for key, value in i.items():
                            if key in headermodel_OBI.keys():
                                modeldata[headermodel_OBI[key]] = value
                        # print(modeldata)
                        if 'Customer' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，客戶別不能爲空
                                                                            """ % rownum
                            break
                        if 'Project' in modeldata.keys():
                            if ProjectName == modeldata['Project']:
                                startupload = 1
                            else:
                                startupload = 0
                                err_ok = 2
                                errMsg = err_msg = """
                                                        第"%s"條數據，Project与选择 的机种名不一致
                                                                            """ % rownum
                                break
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Project不能爲空
                                                                            """ % rownum
                            break
                        if 'Platform' in modeldata.keys():
                            if modeldata['Platform'] not in sectionPlatform:
                                # print(modeldata['Platform'])
                                startupload = 0
                                err_ok = 2
                                errMsg = err_msg = """
                                                        第"%s"條數據，Platform不在维护列表里，请到DCT添加该Platform
                                                                            """ % rownum
                                break
                            else:
                                startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Platform不能爲空
                                                                            """ % rownum
                            break
                        if 'Series' in modeldata.keys():
                            Serieslist = []
                            for i in SeriesInfo.objects.all().values('Series').distinct().order_by('Series'):
                                Serieslist.append(i['Series'])
                            if modeldata['Series'] not in Serieslist:
                                startupload = 0
                                err_ok = 2
                                errMsg = err_msg = """
                                                        第"%s"條數據，Series不在维护列表里
                                                                            """ % rownum
                                break
                            else:
                                startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Series不能爲空
                                                                            """ % rownum
                            break
                        if 'Category' in modeldata.keys():
                            Categorylist = []
                            for i in CategoryInfo.objects.all().values('Category').distinct().order_by('Category'):
                                Categorylist.append(i['Category'])
                            if modeldata['Category'] not in Categorylist:
                                startupload = 0
                                err_ok = 2
                                errMsg = err_msg = """
                                                        第"%s"條數據，Category不在维护列表里
                                                                            """ % rownum
                                break
                            else:
                                startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Category不能爲空
                                                                            """ % rownum
                            break
                        if 'DeviceNo' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，DeviceNo不能爲空
                                                                            """ % rownum
                            break
                        if 'PN' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，PN不能爲空
                                                                            """ % rownum
                            break
                        if 'Devicename' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Devicename不能爲空
                                                                            """ % rownum
                            break
                        if 'TestPhase' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，TestPhase不能爲空
                                                                            """ % rownum
                            break

                        # if 'Pchsdate' in modeldata.keys():
                        #     # modeldata['Pchsdate'] = modeldata['Pchsdate'].replace('/', '-')
                        #     # print(len(modeldata['Pchsdate'].split('-')))
                        #     if len(modeldata['Pchsdate']) >= 8 and len(modeldata['Pchsdate']) <= 10:
                        #         # modeldata['Pchsdate'].replace('/', '-')
                        #         # print(modeldata['Pchsdate'].replace('/', '-'))
                        #         modeldata['Pchsdate'] = modeldata['Pchsdate'].replace('/', '-')
                        #         modeldata['Pchsdate'] = modeldata['Pchsdate'].replace('.', '-')
                        #         # print(modeldata['Pchsdate'])
                        #         startupload = 1
                        #     else:
                        #         # canEdit = 0
                        #         startupload = 0
                        #         err_ok = 2
                        #         errMsg = err_msg = """
                        #                                     第"%s"條數據，購買時間格式不對，請確認是否是文字格式YYYY-MM-DD
                        #                                                         """ % rownum
                        #         break
                        # else:
                        #     modeldata['Pchsdate'] = None  # 日期爲空

                        uploadxlsxlist.append(modeldata)
                    # print(startupload)
                    #让数据可以从有值更新为无值
                    DevieModelfiedlist = []
                    for i in OBIDeviceResult._meta.fields:
                        if i.name != 'id':
                            DevieModelfiedlist.append([i.name,i.get_internal_type()])
                    for i in uploadxlsxlist:
                        for j in DevieModelfiedlist:
                            if j[0] not in i.keys():
                                # print(j)
                                if j[1] == "DateField":
                                    i[j[0]] = None
                                else:
                                    i[j[0]] = ''
                    num1 = 0
                    if startupload:
                        # print(uploadxlsxlist)
                        for i in uploadxlsxlist:
                            num1 += 1
                            # print(num1)
                            # print(i)
                            # modeldata = {}
                            # for key, value in i.items():
                            #     if key in headermodel_OBI.keys():
                            #         if headermodel_OBI[key] == "Predict_return" or headermodel_OBI[
                            #             key] == "Borrow_date" or headermodel_OBI[key] == "Return_date":
                            #             print(value)
                            #             modeldata[headermodel_OBI[key]] = value.split("/")[2] + "-" + \
                            #                                                        value.split("/")[0] + "-" + \
                            #                                                        value.split("/")[1]
                            #         else:
                            #             modeldata[headermodel_OBI[key]] = value
                            Check_dic = {
                                'Project': i['Project'],
                                'DeviceNo': i['DeviceNo'],
                            }
                            i['editor'] = request.session.get('user_name')
                            i['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # print(modeldata)
                            # print(i)
                            # Check_dic_Gantt['Test_Start'] = None  # 日期格式为空NULL不能用空字符
                            if OBIDeviceResult.objects.filter(**Check_dic):#已经存在覆盖
                                OBIDeviceResult.objects.filter(
                                    **Check_dic).update(**i)
                            else:#新增
                                OBIDeviceResult.objects.create(**i)
                        errMsg = '上傳成功'

                    # mock_data
                    if checkOBI:
                        check_Result = OBIDeviceResult.objects.filter(**checkOBI)
                    else:
                        check_Result = OBIDeviceResult.objects.all()
                    for i in check_Result:
                        mock_data.append(
                            {"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
                             "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
                             "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
                             "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion, "Test_Phase": i.TestPhase,
                             "Comments": i.Comments}, )
                    for i in OBIDeviceResult.objects.all().values("PN").distinct().order_by("PN"):
                        selectPN.append({"value": i["PN"]})
                    # print(mock_data)
        aa = {"flag": alert}
        data = {
            "content": mock_data,
            "select": selectItem,
            "selectProjectName": selectProjectName,
            "selectPN": selectPN,
            "canEdit": canEdit,
            "sectionPlatform": sectionPlatform,
            "sectionSeries": sectionSeries,
            "sectionCategory": sectionCategory,
            "errMsg": errMsg,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'OBIDeviceResult/OBIDeviceResult_edit.html', locals())

@csrf_exempt
def OBIDeviceResult_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "OBIDeviceResult/search"
    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5,3", "Category": "Cabel&Adapter", "Device_No": "21830", "PN": "4Y50Q64661",
        #  "Device_name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "F", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
        # {"id": "2", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5, 3", "Category": "Cabel&Adapter", "Device_No": "21831", "PN": "4Y50Q64661",
        #  "Device_name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "Qd_C", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
        # {"id": "3", "Customer": "C38(NB)", "Project_Name": "GLV34", "Platform": "AMD Cezanne-H",
        #  "Series": "Consumer 7,9,5, 3", "Category": "Cabel&Adapter", "Device_No": "21830", "PN": "4Y50Q64661",
        #  "Device_name": "Lenovo Fingerprint Biometric USB Mouse", "Test_Result": "Qd_C", "FW_Ver": "",
        #  "Software_Ver": "", "HW_ID_ver": "", "Test_Phase": "SIT", "Comments": "實物P/N為: 4Y40X49493, 與LNV確認是同一產品."},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39"
    ]

    selectProjectName = [
        # {"value": "GLA34"}, {"value": "FLMA0"}, {"value": "FLMS0"}
    ]

    sectionPlatform = [
        # "Intel Tiger lake-C", "Intel Ice lake", "AMD Lucienne",
    ]

    selectPN = [
        # {"value": "4Y50U45359"}, {"value": "GY50X79384"}, {"value": "4Y40Z48977"}
    ]

    for i in CQMProject.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    for i in OBIDeviceResult.objects.all().values("Project").distinct().order_by("Project"):
        selectProjectName.append({"value": i["Project"]})
    for i in OBIDeviceResult.objects.all().values("Platform").distinct().order_by("Platform"):
        sectionPlatform.append(i["Platform"])
    for i in OBIDeviceResult.objects.all().values("PN").distinct().order_by("PN"):
        selectPN.append({"value": i["PN"]})

    canEdit = 0  # export權限
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if 'admin' in i:
            # editPpriority = 4
            canEdit = 1

    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            pass
        if request.POST.get('isGetData') == 'SEARCH':
            check_dic = {}
            Customer = request.POST.get('Customer')
            ProjectName = request.POST.get('ProjectName')
            Platform = request.POST.get('Platform')
            PN = request.POST.get('PN')
            if Customer and Customer != "All":
                check_dic['Customer'] = Customer
            if ProjectName and ProjectName != "All":
                check_dic['Project'] = ProjectName
            if Platform and Platform != "All":
                check_dic['Platform'] = Platform
            if PN:
                check_dic['PN'] = PN
            # print(check_dic)
            if check_dic:
                check_Result = OBIDeviceResult.objects.filter(**check_dic)
            else:
                check_Result = OBIDeviceResult.objects.all()
            for i in check_Result:
                mock_data.append({"id": i.id, "Customer": i.Customer, "Project_Name": i.Project, "Platform": i.Platform,
                                  "Series": i.Series, "Category": i.Category, "Device_No": i.DeviceNo, "PN": i.PN,
                                  "Device_Name": i.Devicename, "Test_Result": i.Testresult, "FW_Ver": i.FWversion,
                                  "Software_Ver": i.Softwareversion, "HW_ID_ver": i.HWIDversion,
                                  "Test_Phase": i.TestPhase, "Comments": i.Comments}, )
            # print(mock_data)
        data = {
            "content": mock_data,
            "select": selectItem,
            "selectProjectName": selectProjectName,
            "selectPN": selectPN,
            "canEdit": canEdit,
            "sectionPlatform": sectionPlatform,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'OBIDeviceResult/OBIDeviceResult_search.html', locals())


@csrf_exempt
def OBIDeviceResult_options(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "OBIDeviceResult/ptions"
    mock_data = [
        # {"id": "1", "Category": "Keyboard"},
        # {"id": "2", "Category": "Cabel&Adapter"},
    ]

    mock_data1 = [
        # {"id": "1", "Series": "SMB"},
        # {"id": "2", "Series": "SMB"},
    ]

    sectionCategory = [
        # "Keyboard", "Cabel&Adapter", "Dock",
    ]


    sectionSeries = [
        # "SMB", "Consumer 7,9,5,3",
    ]


    canEdit = 1
    err_MSG = ''
    if request.method == "POST":
        if request.POST:
            if request.POST.get('isGetData') == 'first':
                for i in CategoryInfo.objects.all().values("Category").distinct().order_by("Category"):
                    sectionCategory.append(i["Category"])
                for i in SeriesInfo.objects.all().values("Series").distinct().order_by("Series"):
                    sectionSeries.append(i["Series"])
                for i in CategoryInfo.objects.all():
                    mock_data.append({"id": i.id, "Category": i.Category,
                                      "editor": i.editor, "edit_time": i.edit_time, })
                for i in SeriesInfo.objects.all():
                    mock_data1.append({"id": i.id, "Series": i.Series,
                                      "editor": i.editor, "edit_time": i.edit_time, })
            if request.POST.get('isGetData') == 'SearchCategory':
                Category = request.POST.get('Category')
                check_dic={'Category': Category}
                if Category == "All" or not Category:
                    Category_QuerySet = CategoryInfo.objects.all()
                else:
                    Category_QuerySet = CategoryInfo.objects.filter(**check_dic)
                for i in Category_QuerySet:
                    mock_data.append({"id": i.id, "Category": i.Category,
                                      "editor": i.editor, "edit_time": i.edit_time, })
            if request.POST.get('action') == 'addSubmitCategory':
                Category = request.POST.get('Category')
                add_dic = {"Category": Category,
                           "editor": request.session.get('user_name'),
                           "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if CategoryInfo.objects.filter(Category=Category):
                    err_MSG = """ %s已经存在
                    """%Category
                else:
                    CategoryInfo.objects.create(**add_dic)

                CategorySearch = request.POST.get('CategorySearch')
                check_dic = {"Category": CategorySearch}
                if CategorySearch == "All" or not CategorySearch:
                    Category_QuerySet = CategoryInfo.objects.all()
                else:
                    Category_QuerySet = CategoryInfo.objects.filter(**check_dic)
                for i in Category_QuerySet:
                    mock_data.append({"id": i.id, "Category": i.Category,
                                      "editor": i.editor, "edit_time": i.edit_time, })
                for i in CategoryInfo.objects.all().values("Category").distinct().order_by("Category"):
                    sectionCategory.append(i["Category"])
            if request.POST.get('action') == 'editSubmitCategory':
                editid1 = request.POST.get('editid1')
                Category = request.POST.get('Category')
                update_dic = {"Category": Category,
                           "editor": request.session.get('user_name'),
                           "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if CategoryInfo.objects.filter(Category=Category):
                    err_MSG = """ %s已经存在
                                """ % Category
                else:
                    CategoryInfo.objects.filter(id=editid1).update(**update_dic)

                CategorySearch = request.POST.get('CategorySearch')
                check_dic = {"Category": CategorySearch}
                if CategorySearch == "All" or not CategorySearch:
                    Category_QuerySet = CategoryInfo.objects.all()
                else:
                    Category_QuerySet = CategoryInfo.objects.filter(**check_dic)
                for i in Category_QuerySet:
                    mock_data.append({"id": i.id, "Category": i.Category,
                                      "editor": i.editor, "edit_time": i.edit_time, })
                for i in CategoryInfo.objects.all().values("Category").distinct().order_by("Category"):
                    sectionCategory.append(i["Category"])

            if request.POST.get('isGetData') == 'SearchSeries':
                check_dic={}
                Series = request.POST.get('Series')
                check_dic = {"Series": Series}
                if Series == "All" or not Series:
                    Series_QuerySet = SeriesInfo.objects.all()
                else:
                    Series_QuerySet = SeriesInfo.objects.filter(**check_dic)
                for i in Series_QuerySet:
                    mock_data1.append({"id": i.id, "Series": i.Series,
                                       "editor": i.editor, "edit_time": i.edit_time, })
            if request.POST.get('action') == 'addSubmitSeries':
                Series = request.POST.get('Series')
                add_dic = {"Series": Series,
                           "editor": request.session.get('user_name'),
                           "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if SeriesInfo.objects.filter(Series=Series):
                    err_MSG = """ %s已经存在
                    """ % Series
                else:
                    SeriesInfo.objects.create(**add_dic)

                SeriesSearch = request.POST.get('SeriesSearch')
                check_dic = {"Series": SeriesSearch}
                if SeriesSearch == "All" or not SeriesSearch:
                    Series_QuerySet = SeriesInfo.objects.all()
                else:
                    Series_QuerySet = SeriesInfo.objects.filter(**check_dic)
                for i in Series_QuerySet:
                    mock_data1.append({"id": i.id, "Series": i.Series,
                                      "editor": i.editor, "edit_time": i.edit_time, })

                for i in SeriesInfo.objects.all().values("Series").distinct().order_by("Series"):
                    sectionSeries.append(i["Series"])
            if request.POST.get('action') == 'editSubmitSeries':
                editid = request.POST.get('editid2')
                Series = request.POST.get('Series')
                add_dic = {"Series": Series,
                           "editor": request.session.get('user_name'),
                           "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                if SeriesInfo.objects.filter(Series=Series):
                    err_MSG = """ %s已经存在
                    """ % Series
                else:
                    SeriesInfo.objects.filter(id=editid).update(**add_dic)

                SeriesSearch = request.POST.get('SeriesSearch')
                check_dic = {"Series": SeriesSearch}
                if SeriesSearch == "All" or not SeriesSearch:
                    Series_QuerySet = SeriesInfo.objects.all()
                else:
                    Series_QuerySet = SeriesInfo.objects.filter(**check_dic)
                for i in Series_QuerySet:
                    mock_data1.append({"id": i.id, "Series": i.Series,
                                      "editor": i.editor, "edit_time": i.edit_time, })

                for i in SeriesInfo.objects.all().values("Series").distinct().order_by("Series"):
                    sectionSeries.append(i["Series"])
        else:
            try:
                request.body
                # print(request.body)
            except:
                # print('1')
                pass
            else:
                # print('2')
                if 'DeleteSeries' in str(request.body):
                    # print("1", request.POST.getlist['params'])
                    responseData = json.loads(request.body)
                    # print(responseData)
                    for i in responseData['DeleteId']:
                        # for j in CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)):
                        #     print(j)
                        # CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)).delete()
                        SeriesInfo.objects.get(id=i).delete()

                    SeriesSearch = responseData['Series_search']
                    check_dic = {"Series": SeriesSearch}
                    if SeriesSearch == "All" or not SeriesSearch:
                        Series_QuerySet = SeriesInfo.objects.all()
                    else:
                        Series_QuerySet = SeriesInfo.objects.filter(**check_dic)
                    for i in Series_QuerySet:
                        mock_data1.append({"id": i.id, "Series": i.Series,
                                           "editor": i.editor, "edit_time": i.edit_time, })

                    for i in SeriesInfo.objects.all().values("Series").distinct().order_by("Series"):
                        sectionSeries.append(i["Series"])
                if 'DeleteCategory' in str(request.body):
                    # print("1", request.POST.getlist['params'])
                    responseData = json.loads(request.body)
                    # print(responseData)
                    for i in responseData['DeleteId']:
                        # for j in CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)):
                        #     print(j)
                        # CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)).delete()
                        CategoryInfo.objects.get(id=i).delete()

                    CategorySearch = responseData['Category_search']
                    check_dic = {"Category": CategorySearch}
                    if CategorySearch == "All" or not CategorySearch:
                        Category_QuerySet = CategoryInfo.objects.all()
                    else:
                        Category_QuerySet = CategoryInfo.objects.filter(**check_dic)
                    for i in Category_QuerySet:
                        mock_data.append({"id": i.id, "Category": i.Category,
                                          "editor": i.editor, "edit_time": i.edit_time, })
                    for i in CategoryInfo.objects.all().values("Category").distinct().order_by("Category"):
                        sectionCategory.append(i["Category"])

        data = {
            "canEdit": canEdit,
            "err_MSG": err_MSG,
            "content": mock_data,
            "content1": mock_data1,
            "sectionCategory": sectionCategory,
            "sectionSeries": sectionSeries,
        }
        # print(json.dumps(data), type(json.dumps(data)))
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'OBIDeviceResult/OBIDeviceResult_options.html', locals())