from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from django.http import HttpResponse
import datetime,json,simplejson
from MQM.models import MQM
from app01.models import UserInfo, ProjectinfoinDCT
from django.db import transaction
from .forms import MQM_F

# Create your views here.
@csrf_exempt
def MQM_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/MQM_upload"
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
    MQM_upload=MQM_F(request.POST)
    # print(request.method)
    if request.method=="POST":
        # print(request.POST)
        if 'Upload' in request.POST.keys():
            if MQM_upload.is_valid():
                message_err=0
                # print('2')
                Check_dic = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),
                              'Category': request.POST.get('Category'), 'Name': request.POST.get('Name'), 'Vendor': request.POST.get('Vendor'),
                              'SourcePriority': request.POST.get('SourcePriority'),
                              'CompalPN': request.POST.get('CompalPN'),
                              'VendorPN': request.POST.get('VendorPN'), 'Status': request.POST.get('Status'),
                              'Description': request.POST.get('Description'), 'Qty': request.POST.get('Qty'),
                              'Location': request.POST.get('Location'),
                              # 'B_DQA_DataCode': request.POST.get('DataCodeB'),
                              # 'B_DQA_Reliability': request.POST.get('ReliabilityB'),
                              # 'B_DQA_Compatibility': request.POST.get('CompatibilityB'),
                              # 'B_DQA_Result': request.POST.get('ResultforB'), 'B_RD_ESD': request.POST.get('ESDB'),
                              # 'B_RD_EMI': request.POST.get('EMIB'), 'B_RD_RF': request.POST.get('RFB'),
                              # 'C_DQA_DataCode': request.POST.get('DataCodeC'),
                              # 'C_DQA_Reliability': request.POST.get('ReliabilityC'),
                              # 'C_DQA_Compatibility': request.POST.get('CompatibilityC'),
                              # 'C_DQA_Result': request.POST.get('ResultforC'),
                              # 'C_RD_ESD': request.POST.get('ESDC'), 'C_RD_EMI': request.POST.get('EMIC'),
                              # 'C_RD_RF': request.POST.get('RFC'), 'Control_run': request.POST.get('Controlrun'),
                              # 'Comments': request.POST.get('Comments')
                             }
                if request.POST.get('Comments'):
                    Comments = request.session.get('user_name') +  '(%s)' % datetime.datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S") + ":" + '\n' + request.POST.get('Comments')
                else:
                    Comments = ""

                Create_dic={'Customer':request.POST.get('Customer'), 'Project':request.POST.get('Project'),
                            'Category':request.POST.get('Category').upper(), 'Name': request.POST.get('Name'), 'Vendor':request.POST.get('Vendor'),
                            'SourcePriority':request.POST.get('SourcePriority'),'CompalPN':request.POST.get('CompalPN'),
                            'VendorPN':request.POST.get('VendorPN'), 'Status':request.POST.get('Status'),
                            'Description':request.POST.get('Description'),'Qty':request.POST.get('Qty'),
                            'Location':request.POST.get('Location'), 'B_DQA_DataCode':request.POST.get('DataCodeB'),
                            'B_DQA_Reliability':request.POST.get('ReliabilityB'),'B_DQA_Compatibility':request.POST.get('CompatibilityB'),
                            'B_DQA_Result':request.POST.get('ResultforB'),'B_RD_ESD':request.POST.get('ESDB'),
                            'B_RD_EMI':request.POST.get('EMIB'),'B_RD_RF':request.POST.get('RFB'),
                            'C_DQA_DataCode': request.POST.get('DataCodeC'),
                            'C_DQA_Reliability': request.POST.get('ReliabilityC'),
                            'C_DQA_Compatibility': request.POST.get('CompatibilityC'),
                            'C_DQA_Result': request.POST.get('ResultforC'),
                            'C_RD_ESD': request.POST.get('ESDC'), 'C_RD_EMI': request.POST.get('EMIC'),
                            'C_RD_RF': request.POST.get('RFC'),
                            'INV_DQA_DataCode': request.POST.get('DataCodeINV'),
                            'INV_DQA_Reliability': request.POST.get('ReliabilityINV'),
                            'INV_DQA_Compatibility': request.POST.get('CompatibilityINV'),
                            'INV_DQA_Result': request.POST.get('ResultforINV'),
                            'INV_RD_ESD': request.POST.get('ESDINV'), 'INV_RD_EMI': request.POST.get('EMIINV'),
                            'INV_RD_RF': request.POST.get('RFINV'),
                            'Control_run':request.POST.get('Controlrun'),
                            'Comments':Comments,'editor':request.session.get('user_name'),
                            'edit_time':datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                # print(Create_dic)
                if MQM.objects.filter(**Check_dic).first():
                    UpdateResult="数据已存在数据库中"
                    print(UpdateResult)
                    message_err=1
                else:
                    MQM.objects.create(**Create_dic)
            else:
                cleandata=MQM_upload.errors
        if 'type' in request.POST:
            err_ok=0
            err_msg = ''
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            MQMList=[{'Customer':'Customer','Project':'Project','Category':'Category','Vendor': 'Vendor',
                     'SourcePriority':'SourcePriority','CompalPN':'CompalPN','VendorPN':'VendorPN',
                     'Status':'Status','Description':'Description','Location': 'Location',}]

            num = 1
            for i in simplejson.loads(xlsxlist):
                if num > 1:
                    break
                else:
                    if 'Customer' in i.keys():
                        Customer = i['Customer']
                    if 'Project' in i.keys():
                        Project = i['Project']
                num += 1

            rownum = 0
            startupload = 0
            for i in simplejson.loads(xlsxlist):
                rownum += 1
                # print(i)
                # 同机种验证
                # print(Project, i['Project'])
                if i['Project'] != Project:
                    startupload = 0
                    err_ok = 2
                    err_msg = """
            文件中包含多个机种，请检查确认，修改之后重新上传
                                """
                    break
                #同Project验证，不能多次上传
                if 'Customer' in i.keys():
                    Customer = i['Customer']
                if 'Project' in i.keys():
                    Project = i['Project']
                Check_dic_ProjectCQM = {'Customer': Customer, 'Project': Project, }
                if MQM.objects.filter(**Check_dic_ProjectCQM).first():
                    startupload = 0
                    err_ok = 2
                    err_msg = """
            同一个Project，Excel上传只能使用一次
            %s-%s 的数据已经存在。
                                """ % (Customer, Project,)
                    break
                else:
                    startupload = 1
                    pass

            if startupload:
                for i in simplejson.loads(xlsxlist):
                    Check_dic = {
                        # 'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),
                        #          'Category': request.POST.get('Category'), 'Vendor': request.POST.get('Vendor'),
                        #          'SourcePriority': request.POST.get('SourcePriority'),
                        #          'CompalPN': request.POST.get('CompalPN'),
                        #          'VendorPN': request.POST.get('VendorPN'), 'Status': request.POST.get('Status'),
                        #          'Description': request.POST.get('Description'), 'Qty': request.POST.get('Qty'),
                        #          'Location': request.POST.get('Location'),
                                 }
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
                    if 'Category' in i.keys():
                        Check_dic['Category'] = i['Category'].upper()
                        exsitdata['Category'] = i['Category'].upper()
                    else:
                        exsitdata['Category'] =''
                    if 'Name' in i.keys():
                        Check_dic['Name'] = i['Name']
                        exsitdata['Name'] = i['Name']
                    else:
                        exsitdata['Name'] =''
                    if 'Vendor' in i.keys():
                        Check_dic['Vendor'] = i['Vendor']
                        exsitdata['Vendor'] = i['Vendor']
                    else:
                        exsitdata['Vendor'] =''
                    if 'SourcePriority' in i.keys():
                        Check_dic['SourcePriority'] = i['SourcePriority']
                        exsitdata['SourcePriority'] = i['SourcePriority']
                    else:
                        exsitdata['SourcePriority'] =''
                    if 'CompalPN' in i.keys():
                        Check_dic['CompalPN'] = i['CompalPN']
                        exsitdata['CompalPN'] = i['CompalPN']
                    else:
                        exsitdata['CompalPN'] =''
                    if 'VendorPN' in i.keys():
                        Check_dic['VendorPN'] = i['VendorPN']
                        exsitdata['VendorPN'] = i['VendorPN']
                    else:
                        exsitdata['VendorPN'] =''
                    if 'Status' in i.keys():
                        Check_dic['Status'] = i['Status']
                        exsitdata['Status'] = i['Status']
                    else:
                        exsitdata['Status'] =''
                    if 'Description' in i.keys():
                        Check_dic['Description'] = i['Description']
                        exsitdata['Description'] = i['Description']
                    else:
                        exsitdata['Description'] =''
                    if 'Qty' in i.keys():
                        Check_dic['Qty'] = i['Qty']
                        exsitdata['Qty'] = i['Qty']
                    else:
                        exsitdata['Qty'] =''
                    if 'Location' in i.keys():
                        Check_dic['Location'] = i['Location']
                        exsitdata['Location'] = i['Location']
                    else:
                        exsitdata['Location'] =''
                    if MQM.objects.filter(**Check_dic).first():#已存在的不覆盖，提示去edit修改
                        err_ok=1
                        MQMList.append(exsitdata)
                    else:
                        updatedic = {}
                        for j in i.keys():
                            if j == 'Comments':
                                if i[j]:
                                    updatedic[j] = request.session.get('user_name') + '(%s)' % datetime.datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S") + ":" + '\n' + i[j]

                                    # print(updatedic[j])
                            elif j =="Category":
                                updatedic[j] = i[j].upper()
                            else:
                                updatedic[j] = i[j]
                        updatedic['editor'] = request.session.get('user_name')
                        updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        MQM.objects.create(**updatedic)
            datajason = {
                'err_ok': err_ok,
                "err_msg": err_msg,
                "canEdit": 1,
                'content': MQMList
            }
            print(datajason)

            return HttpResponse(json.dumps(datajason), content_type="application/json")
    return render(request, 'MQM/MQM_upload.html', locals())

@csrf_exempt
def MQM_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/MQM_edit"
    mock_data=[
        # {"id":"1","Category":"USB 3.1 Gen2(沉版CH=0.36 , H=5.72, 9P, BlackTongue ,G/F , Black Ni)","Vendor":"ACON","SourcePriority":"M","CompalPN":"LTCX0093GB0","Status":"AP/AL","VendorPN":"XXX","Description":"CONN ACON GTRA0-9U1U91 9P H5.72 USB3.1","Qty":"2","Location":"JUSB2 & JUSB1","DataCodeB":"67","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"99","EMIB":"","RFB":"","DataCodeC":"1926","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":""},
        #        {"id": "2","Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)","Vendor": "HIGHSTAR","SourcePriority":"M","CompalPN": "LTCX0093HB0","Status": "AP/AL","VendorPN": "XXX", "Description": "S CONN HIGHSTAR UB11249-B200W-1H 24P H4.37 USB TYPE_C P0.25", "Qty": "2", "Location": "JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"94HK","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":"203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement 204869 The chip of HIGHSTAR DC-IN connector is skewed after DC-IN Jack strength test(X axis Drop,fail at axis +Y)"},
        #        {"id": "3", "Category": "USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)", "Vendor": "DEREN", "SourcePriority": "S1", "CompalPN": "LTCX0093IB0", "Status": "AP/AL","VendorPN": "XXX", "Description": "S CONN DEREN 560Q17-001H 24P H4.43 USB TYPE_C P0.25", "Qty": "2", "Location": "JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"DR1927Z","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":"203374 USB Type-C port eject force not meet spec(spec:0.8kg~2kg)after Operating Force Measurement"},
        #        {"id":"4","Category":"USB Type-C (AVAP)(CH=-1.15 , H=4.43 , 30u'Gold ,Black Tongue , Black Ni)","Vendor":"LOTES","SourcePriority":"S2","CompalPN":"LTCX0094RB0","Status":"AP/AL","VendorPN":"XXX","Description":"S CONN LOTES AUSB0453-P103A11 24P H4.3 USB TYPE_C P0.25","Qty":"2","Location":"JTYPEC1 & JTYPEC2","DataCodeB":"","ReliabilityB":"","CompatibilityB":"","ResultforB":"0","ESDB":"","EMIB":"","RFB":"","DataCodeC":"N/A","ReliabilityC":"","CompatibilityC":"","ResultforC":"0","ESDC":"","EMIC":"","RFC":"","Controlrun":"","Comments":""}
    ]
    selectItem = {
                # "C38(NB)": [{"Project": "EL531", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #               {"Project": "EL532", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #               {"Project": "EL533", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #               {"Project": "EL534", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
                #   "C38(AIO)": [{"Project": "EL535", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #                {"Project": "EL536", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #                {"Project": "EL537", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #                {"Project": "EL538", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
                #   "A39": [{"Project": "EL531", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #           {"Project": "EL532", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #           {"Project": "EL533", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #           {"Project": "EL534", "Phase": ["B(FVT)", "C(SIT)", "INV"]}],
                #   "Other": [{"Project": "ELMV2", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #             {"Project": "ELMV3", "Phase": ["B(FVT)", "C(SIT)", "INV"]},
                #             {"Project": "ELMV4", "Phase": ["B(FVT)", "C(SIT)", "INV"]}]
    }
    # editPpriority={
    #     # "statu":1
    #     }
    # alert={
    #     # "flag1":1
    # }
    for i in MQM.objects.all().values('Customer').distinct().order_by('Customer'):
        # print(i)
        Project = []
        for j in MQM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Project.append({"Project": j['Project']})
        selectItem[i['Customer']] = Project
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    # print(roles)
    editPpriority = 100
    for i in roles:
        if i == 'admin' or ('DQA_SW' in str(roles) and 'DQA_ME' in str(roles)):
            editPpriority = 4
        elif 'PM' in i:
            if editPpriority != 4:
                editPpriority = 3
        elif 'RD' in i:
            if editPpriority != 4 and editPpriority != 3:
                editPpriority = 2
        elif 'DQA' in i:
            if 'DQA_SW' in i:
                if editPpriority != 4 and editPpriority != 3:
                    editPpriority = 5
            if 'DQA_ME' in i:
                if editPpriority != 4 and editPpriority != 3:
                    editPpriority = 6
            if 'DQA_INV' in i:
                if editPpriority != 4 and editPpriority != 3:
                    editPpriority = 7
        else:
            editPpriority = 0
    # print(editPpriority)
    alert=0

    if request.method=="POST":
        # print(request.method,request.body)

        # print (request.POST)
        # if request.POST.get('isGetData')=='first':
        #     for i in MQM.objects.all().values('Customer').distinct().order_by('Customer'):
        #         # print(i)
        #         Project=[]
        #         for j in MQM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
        #             Project.append({"Project":j['Project']})
        #         selectItem[i['Customer']]=Project
            # print(selectItem)
        if request.POST.get('isGetData') == 'SEARCH':
            Customer=request.POST.get('Customer')
            Project=request.POST.get('Project')
            check_dic = {}
            if Customer:
                check_dic['Customer']=Customer
            if Project:
                check_dic['Project']=Project
            # print(check_dic)
            for i in MQM.objects.filter(**check_dic):
                mock_data.append({"id":i.id, 'Project':i.Project, "Category":i.Category, "Name":i.Name, "Vendor":i.Vendor, "SourcePriority":i.SourcePriority,
                                  "CompalPN":i.CompalPN, "Status":i.Status, "VendorPN":i.VendorPN, "Description":i.Description,
                                  "Qty":i.Qty, "Location":i.Location, "DataCodeB":i.B_DQA_DataCode, "ReliabilityB":i.B_DQA_Reliability,
                                  "CompatibilityB":i.B_DQA_Compatibility,"ResultforB":i.B_DQA_Result, "ESDB":i.B_RD_ESD,
                                  "EMIB":i.B_RD_EMI, "RFB":i.B_RD_RF, "DataCodeC":i.C_DQA_DataCode, "ReliabilityC":i.C_DQA_Reliability,
                                  "CompatibilityC":i.C_DQA_Compatibility, "ResultforC":i.C_DQA_Result, "ESDC":i.C_RD_ESD,
                                  "EMIC":i.C_RD_EMI, "RFC":i.C_RD_RF, "DataCodeINV":i.INV_DQA_DataCode, "ReliabilityINV":i.INV_DQA_Reliability,
                                  "CompatibilityINV":i.INV_DQA_Compatibility, "ResultforINV":i.INV_DQA_Result, "ESDINV":i.INV_RD_ESD,
                                  "EMIINV":i.INV_RD_EMI, "RFINV":i.INV_RD_RF,"Controlrun":i.Control_run, "Comments":i.Comments})
            # print(mock_data)
        if 'SAVE' in str(request.body):
            resdatas=json.loads(request.body)
            # print(resdatas)
            resdata=resdatas['rows']
            Customer=resdatas['Customer']
            Project=resdatas['Project']
            # print (resdata)
            # print(resdata['Comments'])
            if resdata['Comments']:
                if 'Comment' in resdata.keys():
                    Coments=resdata['Comments']+'\n'+request.session.get('user_name')+'(%s)'%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":"+"\n"+resdata['Comment']
                else:
                    Coments=resdata['Comments']
            else:
                if 'Comment' in resdata.keys():
                    Coments=request.session.get('user_name')+'(%s)'%datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+":"+"\n"+resdata['Comment']
                else:
                    Coments=''
            update_dic={'Project':resdata['Project'], 'Category':resdata['Category'], 'Name':resdata['Name'], 'Vendor':resdata['Vendor'],'SourcePriority':resdata['SourcePriority'],
                        'CompalPN':resdata['CompalPN'], 'VendorPN':resdata['VendorPN'], 'Status':resdata['Status'],
                        'Description':resdata['Description'], 'Qty':resdata['Qty'], 'Location':resdata['Location'],
                        'B_DQA_DataCode':resdata['DataCodeB'], 'B_DQA_Reliability':resdata['ReliabilityB'],
                        'B_DQA_Compatibility':resdata['CompatibilityB'], 'B_DQA_Result':resdata['ResultforB'],
                        'B_RD_ESD':resdata['ESDB'], 'B_RD_EMI':resdata['EMIB'], 'B_RD_RF':resdata['RFB'],'C_DQA_DataCode':resdata['DataCodeC'],
                        'C_DQA_Reliability':resdata['ReliabilityC'],'C_DQA_Compatibility':resdata['CompatibilityC'],'C_DQA_Result':resdata['ResultforC'],
                        'C_RD_ESD':resdata['ESDC'], 'C_RD_EMI':resdata['EMIC'], 'C_RD_RF':resdata['RFC'],'INV_DQA_DataCode':resdata['DataCodeINV'],
                        'INV_DQA_Reliability':resdata['ReliabilityINV'],'INV_DQA_Compatibility':resdata['CompatibilityINV'],'INV_DQA_Result':resdata['ResultforINV'],
                        'INV_RD_ESD':resdata['ESDINV'], 'INV_RD_EMI':resdata['EMIINV'], 'INV_RD_RF':resdata['RFINV'], 'Control_run':resdata['Controlrun'],
                        'Comments':Coments,'editor':request.session.get('user_name'),'edit_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            try:
                with transaction.atomic():
                    updateMQM=MQM.objects.filter(id=resdata['id']).update(**update_dic)
                    alert=0
            except:
                alert='此数据正被其他使用者编辑中...'
            check_dic = {}
            if Customer:
                check_dic['Customer'] = Customer
            if Project:
                check_dic['Project'] = Project
            # if check_dic:
            for i in MQM.objects.filter(**check_dic):
                mock_data.append(
                    {"id": i.id, 'Project': i.Project, "Category": i.Category, "Name": i.Name, "Vendor": i.Vendor,
                     "SourcePriority": i.SourcePriority,
                     "CompalPN": i.CompalPN, "Status": i.Status, "VendorPN": i.VendorPN, "Description": i.Description,
                     "Qty": i.Qty, "Location": i.Location, "DataCodeB": i.B_DQA_DataCode,
                     "ReliabilityB": i.B_DQA_Reliability,
                     "CompatibilityB": i.B_DQA_Compatibility, "ResultforB": i.B_DQA_Result, "ESDB": i.B_RD_ESD,
                     "EMIB": i.B_RD_EMI, "RFB": i.B_RD_RF, "DataCodeC": i.C_DQA_DataCode,
                     "ReliabilityC": i.C_DQA_Reliability,
                     "CompatibilityC": i.C_DQA_Compatibility, "ResultforC": i.C_DQA_Result, "ESDC": i.C_RD_ESD,
                     "EMIC": i.C_RD_EMI, "RFC": i.C_RD_RF, "DataCodeINV": i.INV_DQA_DataCode,
                     "ReliabilityINV": i.INV_DQA_Reliability,
                     "CompatibilityINV": i.INV_DQA_Compatibility, "ResultforINV": i.INV_DQA_Result,
                     "ESDINV": i.INV_RD_ESD,
                     "EMIINV": i.INV_RD_EMI, "RFINV": i.INV_RD_RF, "Controlrun": i.Control_run, "Comments": i.Comments})
            # else:
            #     for i in MQM.objects.all():
            #         mock_data.append(
            #             {"id": i.id, "Category": i.Category, "Vendor": i.Vendor, "SourcePriority": i.SourcePriority,
            #              "CompalPN": i.CompalPN, "Status": i.Status, "VendorPN": i.VendorPN,
            #              "Description": i.Description,
            #              "Qty": i.Qty, "Location": i.Location, "DataCodeB": i.B_DQA_DataCode,
            #              "ReliabilityB": i.B_DQA_Reliability,
            #              "CompatibilityB": i.B_DQA_Compatibility, "ResultforB": i.B_DQA_Result, "ESDB": i.B_RD_ESD,
            #              "EMIB": i.B_RD_EMI, "RFB": i.B_RD_RF, "DataCodeC": i.C_DQA_DataCode,
            #              "ReliabilityC": i.C_DQA_Reliability,
            #              "CompatibilityC": i.C_DQA_Compatibility, "ResultforC": i.C_DQA_Result, "ESDC": i.C_RD_ESD,
            #              "EMIC": i.C_RD_EMI, "RFC": i.C_RD_RF, "Controlrun": i.Control_run, "Comments": i.Comments})
        if 'MUTIDELETE' in str(request.body):
            responseData = json.loads(request.body)
            # print(responseData['params'])
            for i in responseData['params']:
                # print(i,MQM.objects.filter(id=i))
                MQM.objects.get(id=i).delete()
            Customer = responseData['Customer']
            Project = responseData['Project']
            # print(Customer,Project)
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            for i in MQM.objects.filter(**dic):
                mock_data.append(
                    {"id": i.id, 'Project': i.Project, "Category": i.Category, "Name": i.Name, "Vendor": i.Vendor,
                     "SourcePriority": i.SourcePriority,
                     "CompalPN": i.CompalPN, "Status": i.Status, "VendorPN": i.VendorPN, "Description": i.Description,
                     "Qty": i.Qty, "Location": i.Location, "DataCodeB": i.B_DQA_DataCode,
                     "ReliabilityB": i.B_DQA_Reliability,
                     "CompatibilityB": i.B_DQA_Compatibility, "ResultforB": i.B_DQA_Result, "ESDB": i.B_RD_ESD,
                     "EMIB": i.B_RD_EMI, "RFB": i.B_RD_RF, "DataCodeC": i.C_DQA_DataCode,
                     "ReliabilityC": i.C_DQA_Reliability,
                     "CompatibilityC": i.C_DQA_Compatibility, "ResultforC": i.C_DQA_Result, "ESDC": i.C_RD_ESD,
                     "EMIC": i.C_RD_EMI, "RFC": i.C_RD_RF, "DataCodeINV": i.INV_DQA_DataCode,
                     "ReliabilityINV": i.INV_DQA_Reliability,
                     "CompatibilityINV": i.INV_DQA_Compatibility, "ResultforINV": i.INV_DQA_Result,
                     "ESDINV": i.INV_RD_ESD,
                     "EMIINV": i.INV_RD_EMI, "RFINV": i.INV_RD_RF, "Controlrun": i.Control_run, "Comments": i.Comments})
            # status='1'

        data={
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "orr": editPpriority,
            "orn": alert
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'MQM/MQM_edit.html', locals())

@csrf_exempt
def MQM_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/MQM_search"
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
    lo = [
        # {"Location": "JUSB2 & JUSB1"}, {"Location": "JTYPEC1 & JTYPEC2"}, {"Location": "JTYPEC1 & JTYPEC2"}
    ]
    selectCategory=[
        # {'Category':0}
    ]

    canExport = 0
    canShow = 1
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if 'admin' in i:
            # editPpriority = 4
            canExport = 1
        if 'RD' in i:
            # editPpriority = 4
            canShow = 0
        # elif 'PM' in i:
        #     if editPpriority != 4:
        #         editPpriority = 1
        # elif 'RD' in i:
        #     if editPpriority != 4 and editPpriority != 1:
        #         editPpriority = 2
        # elif 'DQA' in i:
        #     canExport = 1
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
    for i in MQM.objects.all().values('Customer').distinct().order_by('Customer'):
        # print(i)
        Project = []
        for j in MQM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('-Project'):
            CompalPNlist=[]
            for k in MQM.objects.filter(Customer=i['Customer'],Project=j['Project']).values('CompalPN').distinct().order_by('CompalPN'):
                CompalPNlist.append(k['CompalPN'])
            Project.append({"Project": j['Project'],"CompalPN":CompalPNlist})
        Category = []
        for j in MQM.objects.filter(Customer=i['Customer']).values('Category').distinct().order_by(
                'Category'):
            # CompalPNlist=[]
            # for k in CQM.objects.filter(Customer=i['Customer'],Project=j['Project']).values('CompalPN').distinct().order_by('CompalPN'):
            #     CompalPNlist.append(k['CompalPN'])
            Category.append({"Category": j['Category'], })  # "CompalPN":CompalPNlist})
        selectItem[i['Customer']] = {"Project": Project, "Category": Category}
    for i in MQM.objects.all().values('Category').distinct().order_by('Category'):
        selectCategory.append({'Category':i['Category']})
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    print(request.POST)
    if request.method == "POST":
        if request.POST.get('isGetdata') == 'lo':
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            CompalPN = request.POST.get('CompalPN')
            check_dic={}
            check_dic['Customer'] = Customer
            check_dic['Project'] = Project
            check_dic['CompalPN'] = CompalPN
            for i in MQM.objects.filter(**check_dic).values("Location").distinct().order_by('Location'):
                lo.append({"Location":i['Location']})
            # print(lo)
            return HttpResponse(json.dumps({"selectedLocation":lo}), content_type="application/json")

        if request.POST.get('isGetData') == 'SEARCH':
            check_dic={}
            Customer=request.POST.get('Customer')
            Project=request.POST.get('Project')
            # CompalPN=request.POST.get('CompalPN')
            # Location = request.POST.get('Location')
            Category = request.POST.get('Category')
            if Customer:
                check_dic['Customer'] = Customer
            if Project:
                check_dic['Project'] = Project
            # if CompalPN:
            #     check_dic['CompalPN'] = CompalPN
            # if Location:
            #     check_dic['Location'] = Location
            if Category:
                check_dic['Category'] = Category
            # if check_dic:
            for i in MQM.objects.filter(**check_dic):
                mock_data.append(
                    {"id": i.id, 'Project': i.Project, "Category": i.Category, "Name": i.Name, "Vendor": i.Vendor,
                     "SourcePriority": i.SourcePriority,
                     "CompalPN": i.CompalPN, "Status": i.Status, "VendorPN": i.VendorPN, "Description": i.Description,
                     "Qty": i.Qty, "Location": i.Location, "DataCodeB": i.B_DQA_DataCode,
                     "ReliabilityB": i.B_DQA_Reliability,
                     "CompatibilityB": i.B_DQA_Compatibility, "ResultforB": i.B_DQA_Result, "ESDB": i.B_RD_ESD,
                     "EMIB": i.B_RD_EMI, "RFB": i.B_RD_RF, "DataCodeC": i.C_DQA_DataCode,
                     "ReliabilityC": i.C_DQA_Reliability,
                     "CompatibilityC": i.C_DQA_Compatibility, "ResultforC": i.C_DQA_Result, "ESDC": i.C_RD_ESD,
                     "EMIC": i.C_RD_EMI, "RFC": i.C_RD_RF, "DataCodeINV": i.INV_DQA_DataCode,
                     "ReliabilityINV": i.INV_DQA_Reliability,
                     "CompatibilityINV": i.INV_DQA_Compatibility, "ResultforINV": i.INV_DQA_Result,
                     "ESDINV": i.INV_RD_ESD,
                     "EMIINV": i.INV_RD_EMI, "RFINV": i.INV_RD_RF, "Controlrun": i.Control_run, "Comments": i.Comments})
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            'canExport': canExport,
            'canShow': canShow,
            'addselect': selectCategory,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'MQM/MQM_search.html', locals())