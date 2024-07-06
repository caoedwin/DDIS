from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from django.http import HttpResponse
import datetime,json,simplejson
from CQM.models import CQM, CQMProject, CQM_history
from app01.models import UserInfo, ProjectinfoinDCT, Role
from django.db import transaction
from .forms import CQM_F
from django.forms.models import model_to_dict


headermodel_CQM = {
    'Customer':'Customer','Project':'Project','Phase':'Phase',
                      'Material_Group': 'Material_Group',
                     'Keyparts':'Keyparts','Character':'Character','PID':'PID',
                     'VID':'VID','HW':'HW','FW': 'FW','Supplier': 'Supplier','R1_PN_Description': 'R1_PN_Description',
                      'Compal_R1_PN': 'Compal_R1_PN','Compal_R3_PN': 'Compal_R3_PN',
                      'Reliability': 'Reliability','Compatibility': 'Compatibility',
                      'Testresult': 'Testresult','ESD': 'ESD',
                      'EMI': 'EMI','RF': 'RF',
                      'PMsummary': 'PMsummary','Controlrun': 'Controlrun',
                      'Comments': 'Comments',

}
# Create your views here.
@csrf_exempt
def CQM_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/CQM_upload"
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

    CQM_M_lists = CQM_F(request.POST)
    # print(request.method)
    # print(request.POST)
    # print(request.POST.keys())
    # print('Upload' in request.POST.keys())
    # print(request.GET)
    if request.method=="POST":
        # print(request.POST)
        canEdit = 0  # 机种权限 1有权限,前端是用的{{}}传值的，法国在上面，一进upload界面就提示没有权限
        if 'Upload' in request.POST.keys():
            if CQM_M_lists.is_valid():

                # print('2')
                # if request.POST.get('Phase') == 'FVT' or request.POST.get('Phase') == 'SIT':
                #     Phase = 'NPI'
                # elif request.POST.get('Phase') == 'OOC':
                #     Phase = 'OOC'
                # elif request.POST.get('Phase') == 'INV':
                #     Phase = 'INV'
                # else:
                #     Phase = 'OS refresh'
                Check_dic_Project = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),}
                Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                current_user = request.session.get('user_name')
                if Projectinfo:
                    for k in Projectinfo.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
                if canEdit:
                    Check_dic = {"Projectinfo":Projectinfo,
                                  'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),'Phase': request.POST.get('Phase'),
                                  'Material_Group': request.POST.get('Material_Group'), 'Keyparts': request.POST.get('Keyparts'), 'Character': request.POST.get('Character'),
                                  'PID': request.POST.get('PID'),
                                  'VID': request.POST.get('VID'),
                                  'HW': request.POST.get('HW'), 'FW': request.POST.get('FW'),
                                  'Supplier': request.POST.get('Supplier'), 'R1_PN_Description': request.POST.get('R1_PN_Description'),
                                  'Compal_R1_PN': request.POST.get('Compal_R1_PN'),
                                  'Compal_R3_PN': request.POST.get('Compal_R3_PN'),

                                 }
                    if request.POST.get('Comments'):
                        Comments = request.session.get('user_name') +  '(%s)' % datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S") + ":" + '\n' + request.POST.get('Comments')
                    else:
                        Comments = ''

                    Create_dic={"Projectinfo":Projectinfo,
                                  'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),'Phase': request.POST.get('Phase'),
                                  'Material_Group': request.POST.get('Material_Group'), 'Keyparts': request.POST.get('Keyparts'), 'Character': request.POST.get('Character'),
                                  'PID': request.POST.get('PID'),
                                  'VID': request.POST.get('VID'),
                                  'HW': request.POST.get('HW'), 'FW': request.POST.get('FW'),
                                  'Supplier': request.POST.get('Supplier'), 'R1_PN_Description': request.POST.get('R1_PN_Description'),
                                  'Compal_R1_PN': request.POST.get('Compal_R1_PN'),
                                  'Compal_R3_PN': request.POST.get('Compal_R3_PN'),
                                'Reliability':request.POST.get('Reliability'),'Compatibility':request.POST.get('Compatibility'),
                                'Testresult':request.POST.get('Testresult'),'ESD':request.POST.get('ESD'),
                                'EMI':request.POST.get('EMI'),'RF':request.POST.get('RF'),
                                'PMsummary': request.POST.get('PMsummary'),
                                'Controlrun':request.POST.get('Controlrun'),
                                'Comments':Comments,'editor':request.session.get('user_name'),
                                'edit_time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                    # print(Create_dic)
                    if Projectinfo:
                        if CQM.objects.filter(**Check_dic).first():
                            UpdateResult="数据已存在数据库中"
                            # print(UpdateResult)
                            rpeatcontend.append({})
                            # message_err=1
                            result = 1
                        else:
                            print(Create_dic)
                            CQM.objects.create(**Create_dic)
            else:
                cleandata=CQM_M_lists.errors
        if 'type' in request.POST:
            # print(request.POST.get('type'))
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            CQMList=[{'Customer':'Customer','Project':'Project','Phase':'Phase',
                     #  'Material_Group': 'Material_Group',
                     # 'Keyparts':'Keyparts','Character':'Character','PID':'PID',
                     # 'VID':'VID','HW':'HW','FW': 'FW','Supplier': 'Supplier','R1_PN_Description': 'R1_PN_Description',
                      'Compal_R1_PN': 'Compal_R1_PN','Compal_R3_PN': 'Compal_R3_PN',}]
            uploadsuccess = [{'Customer':'Customer','Project':'Project','Phase':'Phase',
                     #  'Material_Group': 'Material_Group',
                     # 'Keyparts':'Keyparts','Character':'Character','PID':'PID',
                     # 'VID':'VID','HW':'HW','FW': 'FW','Supplier': 'Supplier','R1_PN_Description': 'R1_PN_Description',
                      'Compal_R1_PN': 'Compal_R1_PN','Compal_R3_PN': 'Compal_R3_PN',}]
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
            # print(Projectinfo)
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
                uploadxlsxlist = []
                for i in simplejson.loads(xlsxlist):
                    modeldata = {}
                    for key, value in i.items():
                        if key in headermodel_CQM.keys():
                            modeldata[headermodel_CQM[key]] = value
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

                    if Phase.upper() == "INV" or Phase.upper() == "OS refresh".upper():
                        startupload = 1
                        pass
                    else:
                        startupload = 1
            #         else:
            #             if CQM.objects.filter(**Check_dic_ProjectCQM).first():
            #                 startupload = 0
            #                 err_ok = 2
            #                 err_msg = """
            # 同一个Project的同一个Phase，Excel上传只能使用一次
            # %s-%s-%s 的数据已经存在。
            #                     """ % (Customer, Project, Phase)
            #                 break
            #             else:
            #                 startupload = 1
            #                 pass
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
                    uploadxlsxlist.append(modeldata)
                CQMModelfiedlist = []
                for i in CQM._meta.fields:
                    if i.name != 'id' and i.name != 'Projectinfo':
                        CQMModelfiedlist.append([i.name, i.get_internal_type()])
                for i in uploadxlsxlist:
                    for j in CQMModelfiedlist:
                        if j[0] not in i.keys():
                            # print(j)
                            if j[1] == "DateField":
                                i[j[0]] = None
                            else:
                                i[j[0]] = ''

                if startupload:
                    for i in uploadxlsxlist:

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
                        # if 'Material_Group' in i.keys():
                        #     Check_dic['Material_Group'] = i['Material_Group']
                        #     exsitdata['Material_Group'] = i['Material_Group']
                        # else:
                        #     exsitdata['Material_Group'] =''
                        # if 'Keyparts' in i.keys():
                        #     Check_dic['Keyparts'] = i['Keyparts']
                        #     exsitdata['Keyparts'] = i['Keyparts']
                        # else:
                        #     exsitdata['Keyparts'] =''
                        # if 'Character' in i.keys():
                        #     Check_dic['Character'] = i['Character']
                        #     exsitdata['Character'] = i['Character']
                        # else:
                        #     exsitdata['Character'] =''
                        # if 'PID' in i.keys():
                        #     Check_dic['PID'] = i['PID']
                        #     exsitdata['PID'] = i['PID']
                        # else:
                        #     exsitdata['PID'] =''
                        # if 'VID' in i.keys():
                        #     Check_dic['VID'] = i['VID']
                        #     exsitdata['VID'] = i['VID']
                        # else:
                        #     exsitdata['VID'] =''
                        # if 'HW' in i.keys():
                        #     Check_dic['HW'] = i['HW']
                        #     exsitdata['HW'] = i['HW']
                        # else:
                        #     exsitdata['HW'] =''
                        # if 'FW' in i.keys():
                        #     Check_dic['FW'] = i['FW']
                        #     exsitdata['FW'] = i['FW']
                        # else:
                        #     exsitdata['FW'] =''
                        if 'Supplier' in i.keys():
                            Check_dic['Supplier'] = i['Supplier']
                            exsitdata['Supplier'] = i['Supplier']
                        else:
                            exsitdata['Supplier'] =''
                        # if 'R1_PN_Description' in i.keys():
                        #     Check_dic['R1_PN_Description'] = i['R1_PN_Description']
                        #     exsitdata['R1_PN_Description'] = i['R1_PN_Description']
                        # else:
                        #     exsitdata['R1_PN_Description'] =''
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


                            # updatedic = {}
                            # updatedic['Projectinfo'] = Projectinfo
                            # for j in i.keys():
                            #     if j == 'Comments':
                            #         if i[j]:
                            #             updatedic[j] = request.session.get(
                            #                 'user_name') + '(%s)' % datetime.datetime.now().strftime(
                            #                 "%Y-%m-%d %H:%M:%S") + ":" + '\n' + i[j]
                            #
                            #             # print(updatedic[j])
                            #     else:
                            #         updatedic[j] = i[j]
                            # updatedic['editor'] = request.session.get('user_name')
                            # updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            #
                            # # 对应角色值伤上传对应的结果
                            # roles = []
                            # onlineuser = request.session.get('account')
                            # # print(UserInfo.objects.get(account=onlineuser))
                            # for m in UserInfo.objects.get(account=onlineuser).role.all():
                            #     roles.append(m.name)
                            # # print(roles)
                            # editPpriority = 100
                            # for m in roles:
                            #     if m == 'admin':
                            #         # del updatedic['Reliability']
                            #         # del updatedic['Compatibility']
                            #         # del updatedic['Testresult']
                            #         # del updatedic['ESD']
                            #         # del updatedic['EMI']
                            #         # del updatedic['RF']
                            #         # del updatedic['Controlrun']
                            #         # del updatedic['PMsummary']
                            #
                            #         updatedic.pop("Reliability", '404')
                            #         updatedic.pop("Compatibility", '404')
                            #         updatedic.pop("Testresult", '404')
                            #         updatedic.pop("ESD", '404')
                            #         updatedic.pop("EMI", '404')
                            #         updatedic.pop("RF", '404')
                            #         updatedic.pop("Controlrun", '404')
                            #         updatedic.pop("PMsummary", '404')
                            #     elif 'PM' in m:
                            #         # del updatedic['Reliability']
                            #         # del updatedic['Compatibility']
                            #         # del updatedic['Testresult']
                            #         # del updatedic['ESD']
                            #         # del updatedic['EMI']
                            #         # del updatedic['RF']
                            #         # del updatedic['Controlrun']
                            #         # # del updatedic['PMsummary']
                            #
                            #         updatedic.pop("Reliability", '404')
                            #         updatedic.pop("Compatibility", '404')
                            #         updatedic.pop("Testresult", '404')
                            #         updatedic.pop("ESD", '404')
                            #         updatedic.pop("EMI", '404')
                            #         updatedic.pop("RF", '404')
                            #         updatedic.pop("Controlrun", '404')
                            #         # updatedic.pop("PMsummary", '404')
                            #     elif 'RD' in m:
                            #         # del updatedic['Reliability']
                            #         # del updatedic['Compatibility']
                            #         # del updatedic['Testresult']
                            #         # # del updatedic['ESD']
                            #         # # del updatedic['EMI']
                            #         # # del updatedic['RF']
                            #         # del updatedic['Controlrun']
                            #         # del updatedic['PMsummary']
                            #
                            #         updatedic.pop("Reliability", '404')
                            #         updatedic.pop("Compatibility", '404')
                            #         updatedic.pop("Testresult", '404')
                            #         # updatedic.pop("ESD", '404')
                            #         # updatedic.pop("EMI", '404')
                            #         # updatedic.pop("RF", '404')
                            #         updatedic.pop("Controlrun", '404')
                            #         updatedic.pop("PMsummary", '404')
                            #     elif 'DQA' in m:
                            #         if 'DQA_SW' in m:
                            #             # del updatedic['Reliability']
                            #             # # del updatedic['Compatibility']
                            #             # del updatedic['Testresult']
                            #             # del updatedic['ESD']
                            #             # del updatedic['EMI']
                            #             # del updatedic['RF']
                            #             # del updatedic['Controlrun']
                            #             # del updatedic['PMsummary']
                            #             # break#防止一个人多个角色，del如果本来就没有会报错
                            #
                            #             updatedic.pop("Reliability", '404')
                            #             # updatedic.pop("Compatibility", '404')
                            #             updatedic.pop("Testresult", '404')
                            #             updatedic.pop("ESD", '404')
                            #             updatedic.pop("EMI", '404')
                            #             updatedic.pop("RF", '404')
                            #             updatedic.pop("Controlrun", '404')
                            #             updatedic.pop("PMsummary", '404')
                            #         if 'DQA_ME' in m:
                            #             # # del updatedic['Reliability']
                            #             # del updatedic['Compatibility']
                            #             # del updatedic['Testresult']
                            #             # del updatedic['ESD']
                            #             # del updatedic['EMI']
                            #             # del updatedic['RF']
                            #             # del updatedic['Controlrun']
                            #             # del updatedic['PMsummary']
                            #             # break#防止一个人多个角色，del如果本来就没有会报错
                            #
                            #             # updatedic.pop("Reliability", '404')
                            #             updatedic.pop("Compatibility", '404')
                            #             updatedic.pop("Testresult", '404')
                            #             updatedic.pop("ESD", '404')
                            #             updatedic.pop("EMI", '404')
                            #             updatedic.pop("RF", '404')
                            #             updatedic.pop("Controlrun", '404')
                            #             updatedic.pop("PMsummary", '404')
                            #
                            #
                            # #存为历史
                            # Changecontent = ""
                            # Changeto = ""
                            # datadic = model_to_dict(CQM.objects.filter(**Check_dic).first())
                            # # print(datadic)
                            # for m in updatedic.keys():  # 前提是前端的关键字和数据库的一样
                            #     if m == "edit_time" or m == "editor":
                            #         continue
                            #     else:
                            #         if updatedic[m] == datadic[m]:
                            #             continue
                            #         else:
                            #             if not datadic[m]:
                            #                 datadic[m] = ''
                            #             if Changecontent:
                            #                 Changecontent = Changecontent + '\n' + m + ":" + datadic[m]
                            #             else:
                            #                 Changecontent = m + ":" + datadic[m]
                            #             if Changeto:
                            #                 Changeto = Changeto + '\n' + m + ":" + updatedic[m]
                            #             else:
                            #                 Changeto = m + ":" + updatedic[m]
                            # # print(Changecontent)
                            # # print(Changeto)
                            # update_dic_his = {"Changeid": CQM.objects.filter(**Check_dic).first(),
                            #                   "Changecontent": Changecontent,
                            #                   "Changeto": Changeto, "Changeowner": request.session.get('user_name'),
                            #                   "Change_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                            #
                            # CQM.objects.filter(**Check_dic).first().update(**updatedic)
                            # CQM_history.objects.create(**update_dic_his)
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
                            # print(updatedic)
                            CQM.objects.create(**updatedic)
                            uploadsuccess.append(Check_dic)
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
def CQM_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/CQM_edit"
    mock_data = [
        # {"id": "1", "Project": "EL451_S540-14IWL", "Material_Group": "CPU", "Keyparts": "Whiskylake",
        #           "Character": "Intel i3-8145U 2.1G/2C/4M", "PID": "", "VID": "", "HW": "", "FW": "",
        #           "Supplier": "Intel", "R1_PN_Description": "S IC FJ8068404064702 QQK9 W0 2.1G BGA",
        #           "Compal_R1_PN": "SA0000C6R20", "Compal_R3_PN": "SA0000C6R30", "Phase": "FVT", "Reliability": "Qd",
        #           "Compatibility": "DisQ", "Testresult": "T", "PMsummary": "", "Controlrun": "", "Comments": ""},
        #          {"id": "2", "Project": "EL451_S540-14IWL", "Material_Group": "CPU", "Keyparts": "Whiskylake",
        #           "Character": "Intel i5-8265U 1.6G/4C/6M", "PID": "", "VID": "", "HW": "", "FW": "",
        #           "Supplier": "Intel", "R1_PN_Description": "S IC FJ8068404064604 QQTG W0 1.6G BGA",
        #           "Compal_R1_PN": "SA0000C6Q20", "Compal_R3_PN": "SA0000C6Q30", "Phase": "SIT", "Reliability": "F",
        #           "Compatibility": "No Build", "Testresult": "F", "ESD": "", "EMI": "", "RF": "", "PMsummary": "",
        #           "Controlrun": "", "Comments": ""},
        #          {"id": "3", "Project": "EL451", "Material_Group": "CPU", "Keyparts": "Whiskylake",
        #           "Character": "Intel i7-8565U 1.8G/4C/8M", "PID": "", "VID": "", "HW": "", "FW": "",
        #           "Supplier": "Intel", "R1_PN_Description": "S IC FJ8068404064403 QQK6 W0 1.8G BGA",
        #           "Compal_R1_PN": "SA0000C6P20", "Compal_R3_PN": "SA0000C6P30", "Phase": "FVT",
        #           "Reliability": "No Build", "Compatibility": "F", "Testresult": "No Build", "ESD": "", "EMI": "",
        #           "RF": "", "PMsummary": "", "Controlrun": "", "Comments": ""},
        #          {"id": "4", "Project": "EL451-14IWL", "Material_Group": "CPU", "Keyparts": "Pentium", "Character": "",
        #           "PID": "", "VID": "", "HW": "", "FW": "", "Supplier": "Intel", "R1_PN_Description": "",
        #           "Compal_R1_PN": "", "Compal_R3_PN": "", "Phase": "INV", "Reliability": "Drpd",
        #           "Compatibility": "No Build", "Testresult": "DisQ", "ESD": "", "EMI": "", "RF": "", "PMsummary": "",
        #           "Controlrun": "", "Comments": "", "osrefresh": ""},
        #          {"id": "5", "Project": "", "Material_Group": "CPU", "Keyparts": "SMB0 I3", "Character": "", "PID": "",
        #           "VID": "", "HW": "", "FW": "", "Supplier": "Intel", "R1_PN_Description": "", "Compal_R1_PN": "",
        #           "Compal_R3_PN": "", "Phase": "OOC", "Reliability": "DisQ", "Compatibility": "DisQ",
        #           "Testresult": "DisQ", "ESD": "", "EMI": "", "RF": "", "PMsummary": "", "Controlrun": "",
        #           "Comments": ""}
    ]
    selectItem = [
        # "C38(NB)","C38(AIO)","A39","Other"
    ]
    searchalert = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMS0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "IdeaPad5 14IIL05 Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "Intel",
        #  "PLATFORM": "Intel Ice Lake-U", "VGA": "NV N175-G3 NV N175-G5 UMA", "OS SUPPORT": "WIN10 19H2",
        #  "SS": "2020-01-17", "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    history = [
        # {"oldContent": "xxxxxxxxxx", "newContent": "xx", "changeOwner": "LUX", "changeTime": "2020/4/20"},
        #        {"oldContent": "xxxxxxxx", "newdContent": "xxxx", "changeOwner": "LUX", "changeTime": "2020/4/11"},
        #        {"oldContent": "xxx", "newContent": "xxxxxxx", "changeOwner": "LUX", "changeTime": "2020/4/04"},
        #        {"oldContent": "x", "newContent": "xxxxxxx", "changeOwner": "LUX", "changeTime": "2020/4/10"}
    ]
    canEdit = 0#编辑机种的权限
    aa = {"flag": 0}#弹窗1为此提案数据被编辑
    cc = {"statu": 4}#角色权限
    for i in CQMProject.objects.all().values('Customer').distinct().order_by('Customer'):
        # # print(i)
        # Project = []
        # for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
        #     Project.append({"Project": j['Project']})
        selectItem.append(i['Customer'])
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
        if request.POST.get('isGetData') == 'SEARCH':
            Check_dic_Project = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('COMPRJCODE'),}
            Phase = request.POST.get('Phase')
            Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
            current_user = request.session.get('user_name')
            if Projectinfo:
                for k in Projectinfo.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
            Customer=request.POST.get('Customer')
            Project=request.POST.get('COMPRJCODE')
            check_dic = {}
            #Customer,Project不能为空，最好前端加判断
            if Customer:
                check_dic['Customer'] = Customer
            if Project:
                check_dic['Project'] = Project
            if Phase:
                check_dic['Phase'] = Phase
            check_dic['Projectinfo'] = Projectinfo
            # print(check_dic)
            for i in CQM.objects.filter(**check_dic):
                mock_data.append({"id":i.id, "Customer": i.Customer, 'Project':i.Project, "Phase":i.Phase, "Material_Group":i.Material_Group, "Keyparts":i.Keyparts,
                                  "Character":i.Character, "PID":i.PID, "VID":i.VID, "HW":i.HW,
                                  "FW":i.FW, "Supplier":i.Supplier, "R1_PN_Description":i.R1_PN_Description, "Compal_R1_PN":i.Compal_R1_PN,
                                  "Compal_R3_PN":i.Compal_R3_PN,"Reliability":i.Reliability, "Compatibility":i.Compatibility,
                                  "Testresult":i.Testresult, "ESD":i.ESD, "EMI":i.EMI, "RF":i.RF,
                                  "PMsummary":i.PMsummary, "Controlrun":i.Controlrun, "Comments":i.Comments,
                                  "editor":i.editor, "edit_time":i.edit_time, })
            # print(mock_data)
        if request.POST.get('isGetData') == "SEARCHALERT":
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in CQMProject.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append(i["Project"])
            else:
                for i in CQMProject.objects.all().values("Project").distinct().order_by("Project"):
                    Prolist.append(i["Project"])
            for i in Prolist:
                for j in CQM.objects.filter(Project=i).values('Phase').distinct().order_by("Phase"):
                    if ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
                        searchalert.append({
                            "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Year, "COMPRJCODE": i,"Phase":j["Phase"],
                            "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode1,
                            "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode2,
                            "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().ProjectName,
                            "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Size,
                            "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().CPU,
                            "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Platform,
                            "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().VGA,
                            "OS SUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().OSSupport,
                            "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                            "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                            "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
                            "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().SS,
                            "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().LD,
                            "DQA PL": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPL,
                        })
                    else:
                        searchalert.append({
                            "YEAR": "", "COMPRJCODE": i,"Phase":j["Phase"],
                            "CUSPRJCODE": "",
                            "ProjectName": "",
                            "SIZE": "",
                            "CPU": "",
                            "PLATFORM": "",
                            "VGA": "",
                            "OS SUPPORT": "",
                            "Type": "",
                            "PPA": "",
                            "PQE": "",
                            "SS": "",
                            "LD": "",
                            "DQA PL": "",
                        })
            # print(sear)
        if 'SAVE' in str(request.body):
            resdatas=json.loads(request.body)
            # print(resdatas)
            resdata = resdatas['rows']
            Customer = resdatas['Customer']
            Project = resdatas['Project']
            Phase = resdatas['Phase']
            # print (resdata)
            # print(resdata['Comments'])
            if resdata['Comments']:
                if 'Comment' in resdata.keys():
                    Coments = resdata['Comments']+'\n'+request.session.get('user_name')+'(%s)'%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":"+"\n"+resdata['Comment']
                else:
                    Coments = resdata['Comments']
            else:
                if 'Comment' in resdata.keys():
                    Coments=request.session.get('user_name')+'(%s)' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":"+"\n"+resdata['Comment']
                else:
                    Coments=''
            update_dic = {'Project': resdata['Project'], 'Phase': resdata['Phase'], 'Material_Group': resdata['Material_Group'], 'Keyparts': resdata['Keyparts'],
                        'Character':resdata['Character'], 'PID': resdata['PID'], 'VID':resdata['VID'],
                        'HW':resdata['HW'], 'FW':resdata['FW'], 'Supplier':resdata['Supplier'],
                        'R1_PN_Description':resdata['R1_PN_Description'], 'Compal_R1_PN':resdata['Compal_R1_PN'],
                        'Compal_R3_PN':resdata['Compal_R3_PN'], 'Reliability':resdata['Reliability'],
                        'Compatibility':resdata['Compatibility'], 'Testresult':resdata['Testresult'], 'ESD': resdata['ESD'], 'EMI':resdata['EMI'],
                        'RF':resdata['RF'], 'PMsummary':resdata['PMsummary'],'Controlrun':resdata['Controlrun'],
                        'Comments': Coments, 'editor': request.session.get('user_name'), 'edit_time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            Changecontent = ""
            Changeto = ""
            datadic = model_to_dict(CQM.objects.filter(id=resdata['id']).first())
            # print(datadic)
            for i in update_dic.keys():#前提是前端的关键字和数据库的一样
                if i == "edit_time" or i == "editor":
                    continue
                else:
                    if update_dic[i] == datadic[i]:
                        continue
                    else:
                        if not datadic[i]:
                            datadic[i] = ''
                        if Changecontent:
                            Changecontent = Changecontent + '\n' + i + ":" + datadic[i]
                        else:
                            Changecontent = i + ":" + datadic[i]
                        if Changeto:
                            Changeto = Changeto + '\n' + i + ":" + update_dic[i]
                        else:
                            Changeto = i + ":" + update_dic[i]
            # print(Changecontent)
            # print(Changeto)
            update_dic_his = {"Changeid": CQM.objects.filter(id=resdata['id']).first(), "Changecontent": Changecontent,
                              "Changeto": Changeto, "Changeowner": request.session.get('user_name'), "Change_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            try:
                with transaction.atomic():
                    updateCQM=CQM.objects.filter(id=resdata['id']).update(**update_dic)
                    # print(updateCQM)
                    if updateCQM:
                        CQM_history.objects.create(**update_dic_his)
                    alert=0
            except:
                alert='此数据正被其他使用者编辑中...'
            check_dic = {}
            check_dic_Pro = {}
            if Customer:
                check_dic['Customer'] = Customer
                check_dic_Pro['Customer'] = Customer
            if Project:
                check_dic['Project'] = Project
                check_dic_Pro['Project'] = Project
            if Phase:
                check_dic['Phase'] = Phase

            # if check_dic:
            check_dic['Projectinfo'] = CQMProject.objects.filter(**check_dic_Pro).first()
            for i in CQM.objects.filter(**check_dic):
                mock_data.append({"id": i.id, "Customer": i.Customer, 'Project': i.Project, "Phase": i.Phase,
                                  "Material_Group": i.Material_Group, "Keyparts": i.Keyparts,
                                  "Character": i.Character, "PID": i.PID, "VID": i.VID, "HW": i.HW,
                                  "FW": i.FW, "Supplier": i.Supplier, "R1_PN_Description": i.R1_PN_Description,
                                  "Compal_R1_PN": i.Compal_R1_PN,
                                  "Compal_R3_PN": i.Compal_R3_PN, "Reliability": i.Reliability,
                                  "Compatibility": i.Compatibility,
                                  "Testresult": i.Testresult, "ESD": i.ESD, "EMI": i.EMI, "RF": i.RF,
                                  "PMsummary": i.PMsummary, "Controlrun": i.Controlrun, "Comments": i.Comments,
                                  "editor": i.editor, "edit_time": i.edit_time, })
        if 'history' in str(request.body):
            resdatas = json.loads(request.body)
            # print(resdatas["id"])
            for i in CQM_history.objects.filter(Changeid=CQM.objects.get(id=resdatas["id"])):
                # print (i.Changeid)
                history.append({"oldContent": i.Changecontent, "newContent": i.Changeto, "changeOwner": i.Changeowner, "changeTime": i.Change_time})
        if 'MUTIDELETE' in str(request.body):
            responseData = json.loads(request.body)
            # print(responseData)
            for i in responseData['params']:
                # for j in CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)):
                #     print(j)
                CQM_history.objects.filter(Changeid=CQM.objects.get(id=i)).delete()
                CQM.objects.get(id=i).delete()
            Customer = responseData['Customer']
            Project = responseData['COMPRJCODE']
            Phase = responseData['Phase']

            # print(Customer,Project)
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase'] = Phase

            for i in CQM.objects.filter(**dic):
                mock_data.append({"id": i.id, "Customer": i.Customer, 'Project': i.Project, "Phase": i.Phase,
                                  "Material_Group": i.Material_Group, "Keyparts": i.Keyparts,
                                  "Character": i.Character, "PID": i.PID, "VID": i.VID, "HW": i.HW,
                                  "FW": i.FW, "Supplier": i.Supplier, "R1_PN_Description": i.R1_PN_Description,
                                  "Compal_R1_PN": i.Compal_R1_PN,
                                  "Compal_R3_PN": i.Compal_R3_PN, "Reliability": i.Reliability,
                                  "Compatibility": i.Compatibility,
                                  "Testresult": i.Testresult, "ESD": i.ESD, "EMI": i.EMI, "RF": i.RF,
                                  "PMsummary": i.PMsummary, "Controlrun": i.Controlrun, "Comments": i.Comments,
                                  "editor": i.editor, "edit_time": i.edit_time, })
            # status='1'
        aa = {"flag": alert}
        data={
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "canEdit": canEdit,
            "orr": cc,
            "orn": aa,
            "history": history,
            "sear": searchalert
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CQM/CQM_edit.html', locals())

@csrf_exempt
def CQM_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/CQM_search"
    mock_data = [
        # {"id": "1", "Category": "USB 3.1 Gen2(沉版CH=0.36 , H=5.72, 9P, BlackTongue ,G/F , Black Ni)", "Vendor": "ACON",
        #  "SourcePriority": "M", "CompalPN": "LTCX0093GB0", "Status": "AP/AL", "VendorPN": "XXX",
        #  "Description": "CONN ACON GTRA0-9U1U91 9P H5.72 USB3.1", "Qty": "2", "Location": "JUSB2 & JUSB1",
        #  "DataCodeB": "", "ReliabilityB": "", "CompatibilityB": "", "ResultforB": "0", "ESDB": "", "EMIB": "",
        #  "RFB": "", "DataCodeC": "1926", "ReliabilityC": "", "CompatibilityC": "", "ResultforC": "0", "ESDC": "",
        #  "EMIC": "", "RFC": "", "Controlrun": "", "Comments": ""},
        # {"id": "2", "Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)",
        #  "Vendor": "HIGHSTAR", "SourcePriority": "M", "CompalPN": "LTCX0093HB0", "Status": "AP/AL", "VendorPN": "XXX",
        #  "Description": "S CONN HIGHSTAR UB11249-B200W-1H 24P H4.37 USB TYPE_C P0.25", "Qty": "2",
        #  "Location": "JTYPEC1 & JTYPEC2", "DataCodeB": "", "ReliabilityB": "", "CompatibilityB": "", "ResultforB": "0",
        #  "ESDB": "", "EMIB": "", "RFB": "", "DataCodeC": "94HK", "ReliabilityC": "", "CompatibilityC": "",
        #  "ResultforC": "0", "ESDC": "", "EMIC": "", "RFC": "", "Controlrun": "",
        #  "Comments": "203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement 204869 The chip of HIGHSTAR DC-IN connector is skewed after DC-IN Jack strength test(X axis Drop,fail at axis +Y)"},
        # {"id": "3", "Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)",
        #  "Vendor": "DEREN", "SourcePriority": "S1", "CompalPN": "LTCX0093IB0", "Status": "AP/AL", "VendorPN": "XXX",
        #  "Description": "S CONN DEREN 560Q17-001H 24P H4.43 USB TYPE_C P0.25", "Qty": "2",
        #  "Location": "JTYPEC1 & JTYPEC2", "DataCodeB": "", "ReliabilityB": "", "CompatibilityB": "", "ResultforB": "0",
        #  "ESDB": "", "EMIB": "", "RFB": "", "DataCodeC": "DR1927Z", "ReliabilityC": "", "CompatibilityC": "",
        #  "ResultforC": "0", "ESDC": "", "EMIC": "", "RFC": "", "Controlrun": "",
        #  "Comments": "203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement"},
        # {"id": "4", "Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)",
        #  "Vendor": "LOTES", "SourcePriority": "S2", "CompalPN": "LTCX0094RB0", "Status": "AP/AL", "VendorPN": "XXX",
        #  "Description": "S CONN LOTES AUSB0453-P103A11 24P H4.3 USB TYPE_C P0.25", "Qty": "2",
        #  "Location": "JTYPEC1 & JTYPEC2", "DataCodeB": "", "ReliabilityB": "", "CompatibilityB": "", "ResultforB": "0",
        #  "ESDB": "", "EMIB": "", "RFB": "", "DataCodeC": "N/A", "ReliabilityC": "", "CompatibilityC": "",
        #  "ResultforC": "0", "ESDC": "", "EMIC": "", "RFC": "", "Controlrun": "", "Comments": ""}
        ]
    selectItem = {
        # "C38(NB)": {"Project": [{"Project": "EL531", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL532", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL533", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL534", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]}],
        #             "Category": [{"Category": "WWAN",},{"Category": "WLAN"}]},
        # "C38(AIO)": [{"Project": "EL535", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #              {"Project": "EL536", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #              {"Project": "EL537", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #              {"Project": "EL538", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]}],
        # "A39": [{"Project": "EL531", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #         {"Project": "EL532", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #         {"Project": "EL533", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #         {"Project": "EL534", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]}],
        # "Other": [{"Project": "ELMV2", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #           {"Project": "ELMV3", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #           {"Project": "ELMV4", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]}]
    }
    selectCategory = []
    selectCompal_R1_PN = [
        # "SA0000C6R20", "SA0000C6Q20", "SA0000C6P20"#下拉数据格式
        # {"value": "SA0000C6R20"}#输入+下拉+匹配的数据格式
    ]
    selectCompal_R3_PN = [
        # "SA0000C6R30", "SA0000C6Q30", "SA0000C6P30"#下拉数据格式
        # {"value": "SA0000C6R20"}#输入+下拉+匹配的数据格式
    ]
    history = [
        # {"oldContent": "xxxxxxxxxx", "newContent": "xx", "changeOwner": "LUX", "changeTime": "2020/4/20"},
        #        {"oldContent": "xxxxxxxx", "newdContent": "xxxx", "changeOwner": "LUX", "changeTime": "2020/4/11"},
        #        {"oldContent": "xxx", "newContent": "xxxxxxx", "changeOwner": "LUX", "changeTime": "2020/4/04"},
        #        {"oldContent": "x", "newContent": "xxxxxxx", "changeOwner": "LUX", "changeTime": "2020/4/10"}
               ]
    for i in CQMProject.objects.all().values('Customer').distinct().order_by('Customer'):
        # print(i)
        Project = []
        for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('-Project'):
            # CompalPNlist=[]
            # for k in CQM.objects.filter(Customer=i['Customer'],Project=j['Project']).values('CompalPN').distinct().order_by('CompalPN'):
            #     CompalPNlist.append(k['CompalPN'])
            Project.append({"Project": j['Project'],})#"CompalPN":CompalPNlist})

        Category = []
        for j in CQM.objects.filter(Customer=i['Customer']).values('Material_Group').distinct().order_by('Material_Group'):
            # CompalPNlist=[]
            # for k in CQM.objects.filter(Customer=i['Customer'],Project=j['Project']).values('CompalPN').distinct().order_by('CompalPN'):
            #     CompalPNlist.append(k['CompalPN'])
            Category.append({"Category": j['Material_Group'], })  # "CompalPN":CompalPNlist})
        selectItem[i['Customer']] = {"Project": Project, "Category": Category}
    for i in CQM.objects.all().values('Compal_R1_PN').distinct().order_by('Compal_R1_PN'):
        if i['Compal_R1_PN']:
            selectCompal_R1_PN.append({"value": i['Compal_R1_PN']})
        else:#null
            selectCompal_R1_PN.append({"value": ''})
    for i in CQM.objects.all().values('Compal_R3_PN').distinct().order_by('Compal_R3_PN'):
        if i['Compal_R3_PN']:
            selectCompal_R3_PN.append({"value": i['Compal_R3_PN']})
        else:  # null
            selectCompal_R3_PN.append({"value": ''})
    # for i in CQM.objects.all().values('Material_Group').distinct().order_by('Material_Group'):
    #     selectCategory.append(i['Material_Group'])
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
        # elif 'DQA' in i and 'edit' in i:
        #     canExport = 1
    # print(request.POST)
    if request.method == "POST":
        if request.POST.get('isGetData') == 'SEARCH':
            check_dic={}
            check_dic_Pro = {}
            Customer=request.POST.get('Customer')
            Project=request.POST.get('Project')
            # print(Customer, Project)
            Category = request.POST.get('Category')
            Compal_R1_PN = request.POST.get('Compal_R1_PN')
            Compal_R3_PN = request.POST.get('Compal_R3_PN')
            if Customer:
                check_dic['Customer'] = Customer
                check_dic_Pro['Customer'] = Customer
            if Project:
                check_dic['Project'] = Project
                check_dic_Pro['Project'] = Project
            if Category:
                check_dic['Material_Group'] = Category
            if Compal_R1_PN:
                check_dic['Compal_R1_PN'] = Compal_R1_PN
            if Compal_R3_PN:
                check_dic['Compal_R3_PN'] = Compal_R3_PN
            # Projectinfo = CQMProject.objects.filter(**check_dic_Pro).first()
            # if Customer and Project:
            #     check_dic['Projectinfo'] = Projectinfo
            # print(check_dic_Pro)
            # print(check_dic)
            # if check_dic:
            if CQM.objects.filter(**check_dic):
                for i in CQM.objects.filter(**check_dic):
                    print(i.Projectinfo, i.Customer,i.Project)
                    mock_data.append({"id": i.id, "Customer": i.Customer, 'Project': i.Project, "Phase": i.Phase,
                                      "Material_Group": i.Material_Group, "Keyparts": i.Keyparts,
                                      "Character": i.Character, "PID": i.PID, "VID": i.VID, "HW": i.HW,
                                      "FW": i.FW, "Supplier": i.Supplier, "R1_PN_Description": i.R1_PN_Description,
                                      "Compal_R1_PN": i.Compal_R1_PN,
                                      "Compal_R3_PN": i.Compal_R3_PN, "Reliability": i.Reliability,
                                      "Compatibility": i.Compatibility,
                                      "Testresult": i.Testresult, "ESD": i.ESD, "EMI": i.EMI, "RF": i.RF,
                                      "PMsummary": i.PMsummary, "Controlrun": i.Controlrun, "Comments": i.Comments,
                                      "editor": i.editor, "edit_time": i.edit_time, })
        if 'history' in str(request.body):
            resdatas = json.loads(request.body)
            # print(resdatas["id"])
            for i in CQM_history.objects.filter(Changeid=CQM.objects.get(id=resdatas["id"])):
                # print (i.Changeid)
                history.append({"oldContent": i.Changecontent, "newContent": i.Changeto, "changeOwner": i.Changeowner, "changeTime": i.Change_time})
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "history": history,
            "selectCompal_R1_PN":selectCompal_R1_PN,
            "selectCompal_R3_PN":selectCompal_R3_PN,
            "selectCategory":selectCategory,
            'canExport': canExport,
        }
        # print(json.dumps(data), type(json.dumps(data)))
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CQM/CQM_search.html', locals())


# 3
from rest_framework.renderers import JSONRenderer
from .serializers import *
from rest_framework import HTTP_HEADER_ENCODING, exceptions
import base64
import binascii
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.authentication import BaseAuthentication,get_authorization_header #  导入认证类
from rest_framework.exceptions import AuthenticationFailed # 用于抛出错误信息
from app01.models import UserInfo # 导入用户信息表

class MyAuth(BaseAuthentication):
  def authenticate(self, request):
    # """自定义的认证类中必须有此方法以及如下的判断和两个返回值"""
    # # 1. 获取token
    # # print(request,1)
    # # print(request.query_params,2)
    # token = request.query_params.get('token')
    # # print(token)
    # # 2. 判断是否成功获取token
    # if not token:
    #   raise AuthenticationFailed("缺少token")
    # # 3. 判断token是否合法
    # try:
    #   user_obj = UserInfo.objects.filter(token=token).first()
    # except Exception:
    #   raise AuthenticationFailed("token不合法")
    # # 4. 判断token在数据库中是否存在
    # if not user_obj:
    #   raise AuthenticationFailed("token不存在")
    # # 5. 认证通过
    # return (user_obj, token)	# 两个值user_obj赋值给了request.user；token赋值给了request.auth
    # # 注意，权限组件会用到这两个返回值

    # print(request.query_params)
    # username = request.data.get('username', '')
    # password = request.data.get('password', '')
    username = request.query_params.get('username', '')
    password = request.query_params.get('password', '')
    token = request.query_params.get('token', '')
    # print(token)
    # print(username, password)
    # if request.session.get('is_login', None):
    #     # print('1',request.session.get('account'))
    #     user_obj = UserInfo.objects.filter(account=request.session.get('account')).first()
    # else:
    #     user_obj = UserInfo.objects.filter(account=username, password=password).first()
    group = Role.objects.filter(name="API_CQM").first()
    user_obj = None
    if UserInfo.objects.filter(account=username, password=password).first():
        groups = UserInfo.objects.filter(account=username, password=password).first().role.all()
        # print(groups)
        if group in groups:
            user_obj = UserInfo.objects.filter(account=username, password=password).first()
    # print(user_obj)
    if user_obj:
        pass
    else:
        raise AuthenticationFailed("账户密码不正确")
    return (user_obj, token)# 必须要返回两个值，两个值user_obj赋值给了request.user；token赋值给了request.auth



  # #   auth自带的BasicAuthentication
  # """
  #     HTTP Basic authentication against username/password.
  #     """
  # www_authenticate_realm = 'api'
  #
  # def authenticate(self, request):
  #     """
  #     Returns a `User` if a correct username and password have been supplied
  #     using HTTP Basic authentication.  Otherwise returns `None`.
  #     """
  #     auth = get_authorization_header(request).split()
  #     print(auth)
  #
  #     if not auth or auth[0].lower() != b'basic':
  #         return None
  #
  #     if len(auth) == 1:
  #         msg = _('Invalid basic header. No credentials provided.')
  #         raise exceptions.AuthenticationFailed(msg)
  #     elif len(auth) > 2:
  #         msg = _('Invalid basic header. Credentials string should not contain spaces.')
  #         raise exceptions.AuthenticationFailed(msg)
  #
  #     try:
  #         auth_parts = base64.b64decode(auth[1]).decode(HTTP_HEADER_ENCODING).partition(':')
  #         print(auth_parts,base64)
  #     except (TypeError, UnicodeDecodeError, binascii.Error):
  #         msg = _('Invalid basic header. Credentials not correctly base64 encoded.')
  #         raise exceptions.AuthenticationFailed(msg)
  #
  #     userid, password = auth_parts[0], auth_parts[2]
  #     return self.authenticate_credentials(userid, password, request)
  #
  # def authenticate_credentials(self, userid, password, request=None):
  #     """
  #     Authenticate the userid and password against username and password
  #     with optional request for context.
  #     """
  #     credentials = {
  #         get_user_model().USERNAME_FIELD: userid,
  #         'password': password
  #     }
  #     print(credentials)
  #     user = authenticate(request=request, **credentials)
  #     print(user)
  #
  #     if user is None:
  #         raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
  #
  #     if not user.is_active:
  #         raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
  #
  #     return (user, None)
  #
  # def authenticate_header(self, request):
  #     return 'Basic realm="%s"' % self.www_authenticate_realm
from rest_framework.views import APIView
from rest_framework.response import Response
import uuid
class LoginView(APIView):

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user_obj = UserInfo.objects.filter(account= username, password = password).first()
        if user_obj:
            user_obj.token = uuid.uuid4()
            user_obj.save()
            return Response(user_obj.token)
        else:
            return Response('the username or password was wrong')

# 游客只读，登录用户只读，只有登录用户属于 管理员 分组，才可以增删改
from .permissions import MyPermission
class CQMSeriView(APIView):
    authentication_classes = [MyAuth]	# 局部认证(全局在setting里面设置),不写默认用全局（全局需要用DRF写用户的注册登陆接口，可以另外创建一个用于DRF的用户module）
    permission_classes = [MyPermission]  # 局部配置(全局在setting里面设置),不写默认用全局（全局需要用DRF写用户的注册登陆接口，可以另外创建一个用于DRF的用户module）
    # 所有用户都可以访问
    # def get(self, request, *args, **kwargs):
    #     return APIResponse(0, '自定义读 OK')
    #
    # # 必须是 自定义“管理员”分组 下的用户
    # def post(self, request, *args, **kwargs):
    #     return APIResponse(0, '自定义写 OK')
    def get(self, request):
        # print(request.GET)
        # cqm = CQM.objects.all()
        # print(2 ,request.auth)
        cqm = []
        checklist = {}
        if request.GET.get("Customer"):
            checklist['Customer'] = request.GET.get("Customer")
        if request.GET.get("Project"):
            checklist['Project'] = request.GET.get("Project")
        if request.GET.get("Phase"):
            checklist['Phase'] = request.GET.get("Phase")
        if request.GET.get("Compal_R1_PN"):
            checklist['Compal_R1_PN'] = request.GET.get("Compal_R1_PN")
        if request.GET.get("Compal_R3_PN"):
            checklist['Compal_R3_PN'] = request.GET.get("Compal_R3_PN")
        if checklist:
            cqm = CQM.objects.filter(**checklist)
        ser = CQMserilizer(instance=cqm, many=True)
        jsondata = JSONRenderer().render(ser.data)
        return HttpResponse(jsondata, content_type='application/json', status=200)
        # return Response('测试认证组件')