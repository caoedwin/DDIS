from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from django.http import HttpResponse
import datetime,json,simplejson
from .models import AutoItems, AutoResult, AutoProject
from CQM.models import CQM, CQMProject, CQM_history
from CQM.models import CQM as CQMtest
from app01.models import UserInfo, ProjectinfoinDCT
from django.db import transaction
from django.forms.models import model_to_dict
from django.db.models import Max,Min,Sum,Count,Q, Value, CharField


# Create your views here.

headermodel_auto = {
    'No.': 'Number', 'CG': 'Customer', 'VA/N-VA': 'ValueIf',
    'Base效益': 'BaseIncome',
    'Case ID': 'CaseID', 'Case Name': 'CaseName', 'Item': 'Item', '功能簡介': 'FunDescription',
    'Status': 'Status',
    # 'Owner': 'Owner', 'Comment': 'Comment',

}

headermodel_ProResult = {
    'No.': 'Number',
    # 'CG': 'Customer', 'VA/N-VA': 'ValueIf',
    # 'Base效益': 'BaseIncome',
    # 'Case ID': 'CaseID', 'Case Name': 'CaseName', 'Item': 'Item', '功能簡介': 'FunDescription',
    # 'Status': 'Status',
    # 'Owner': 'Owner', 'Comment': 'Comment',
    '備註': 'Comments', 'Cycles': 'Cycles',
}
@csrf_exempt
def AutoItem_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Automation效益/AutoItem_edit"
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
    selectCustomer = [
        # "A39", "C38(AIO)", "C38(NB)", "C85", "T88(AIO)",
    ]

    selectStatus = [
        "Ready", "Cancel", "Ongoing"
    ]



    for i in AutoItems.objects.all().values("Customer").distinct().order_by("Customer"):
        selectCustomer.append(i["Customer"])

    mock_data = [
        # {"id": "1", "Number": "Common-1", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": "0.5", "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "Status": "V", "FunctionInt": "硬盤，內存信息檢查，基本功能測試"},
    ]
    errMsg = ''  # 上傳errmsg
    errMsgNumber = ''
    canEdit = 1  # 增、刪、改、上傳


    if request.method=="POST":
        if request.POST:
            if request.POST.get('isGetData') == 'first':
                # mock_datalist = AutoItems.objects.all().annotate(type=Value('p', output_field=CharField(max_length=1)))
                #附加SQL查询，先以Customer，在一Number最后2位排序
                mock_datalist = AutoItems.objects.all().extra(select={'Lennum': "right(Number,2)"}).order_by("Customer","Lennum")
                for i in mock_datalist:
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                         "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment,
                         }
                    )
            if request.POST.get('isGetData') == 'SEARCH':
                ckeck_dic = {}
                Customer = request.POST.get('Customer')
                ValueIf = request.POST.get('VA_NVA')
                if Customer and Customer != "All":
                    ckeck_dic["Customer"] = Customer
                if ValueIf and ValueIf != "All":
                    ckeck_dic["ValueIf"] = ValueIf

                # mock_data
                if ckeck_dic:
                    mock_datalist = AutoItems.objects.filter(**ckeck_dic)
                else:
                    mock_datalist = AutoItems.objects.all()
                for i in mock_datalist:
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf, "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment,
                         }
                    )
            if request.POST.get('action') == 'addsubmit':
                add_dic = {
                    "Number": request.POST.get('Number'),
                    "Customer": request.POST.get('Customer'),
                    "ValueIf": request.POST.get('VA_NVA'),
                    "BaseIncome": request.POST.get('BaseBenfit'),
                    "CaseID": request.POST.get('CaseID'),
                    "CaseName": request.POST.get('CaseName'),
                    "Item": request.POST.get('Item'),
                    "Status": request.POST.get('Status'),
                    "FunDescription": request.POST.get('FunctionInt'),
                }
                # print(add_dic)
                if AutoItems.objects.filter(Number=request.POST.get('Number')).first():
                    errMsgNumber = "No.已经存在"
                else:
                    # print("create")
                    AutoItems.objects.create(**add_dic)


                # mock_data
                ckeck_dic = {}
                Customer = request.POST.get('CustomerSearch')
                ValueIf = request.POST.get('VA_NVASearch')
                if Customer and Customer != "All":
                    ckeck_dic["Customer"] = Customer
                if ValueIf and ValueIf != "All":
                    ckeck_dic["ValueIf"] = ValueIf

                # mock_data
                if ckeck_dic:
                    mock_datalist = AutoItems.objects.filter(**ckeck_dic)
                else:
                    mock_datalist = AutoItems.objects.all()
                for i in mock_datalist:
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf, "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment,
                         }
                    )
            if request.POST.get('action') == 'updateSubmit':
                add_dic = {
                    "Number": request.POST.get('Number'),
                    "Customer": request.POST.get('Customer'),
                    "ValueIf": request.POST.get('VA_NVA'),
                    "BaseIncome": request.POST.get('BaseBenfit'),
                    "CaseID": request.POST.get('CaseID'),
                    "CaseName": request.POST.get('CaseName'),
                    "Item": request.POST.get('Item'),
                    "Status": request.POST.get('Status'),
                    "FunDescription": request.POST.get('FunctionInt'),
                }
                # print(add_dic)
                # print(AutoItems.objects.filter(Number=request.POST.get('Number')).first().id,request.POST.get('id'),AutoItems.objects.filter(Number=request.POST.get('Number')).first().id != request.POST.get('id'))
                if AutoItems.objects.filter(Number=request.POST.get('Number')).first() and AutoItems.objects.filter(Number=request.POST.get('Number')).first().id != int(request.POST.get('id')):
                    errMsgNumber = "No.已经存在"
                else:
                    # print("create")
                    AutoItems.objects.filter(id=request.POST.get('id')).update(**add_dic)

                # mock_data
                ckeck_dic = {}
                Customer = request.POST.get('CustomerSearch')
                ValueIf = request.POST.get('VA_NVASearch')
                if Customer and Customer != "All":
                    ckeck_dic["Customer"] = Customer
                if ValueIf and ValueIf != "All":
                    ckeck_dic["ValueIf"] = ValueIf

                # mock_data
                if ckeck_dic:
                    mock_datalist = AutoItems.objects.filter(**ckeck_dic)
                else:
                    mock_datalist = AutoItems.objects.all()
                for i in mock_datalist:
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                         "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment,
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
                if 'ExcelData' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    ckeck_dic = {}
                    Customer = responseData['Customer']
                    if Customer and Customer != "All":
                        ckeck_dic['Customer'] = Customer
                    ValueIf = responseData['VA_NVA']
                    if ValueIf and ValueIf != "All":
                        ckeck_dic['ValueIf'] = ValueIf

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
                        # print(type(i), i)
                        rownum += 1
                        # print(rownum)
                        modeldata = {}
                        for key, value in i.items():
                            if key in headermodel_auto.keys():
                                modeldata[headermodel_auto[key]] = value
                        if 'Number' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，编号不能爲空
                                                                            """ % rownum
                            break
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
                        if 'ValueIf' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，VA/N-VA不能爲空
                                                                            """ % rownum
                            break
                        if 'BaseIncome' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Base效益不能爲空
                                                                            """ % rownum
                            break
                        if 'Item' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，Item不能爲空
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
                    # 让数据可以从有值更新为无值
                    AutoItemModelfiedlist = []
                    for i in AutoItems._meta.fields:
                        if i.name != 'id':
                            AutoItemModelfiedlist.append([i.name, i.get_internal_type()])
                    for i in uploadxlsxlist:
                        for j in AutoItemModelfiedlist:
                            if j[0] not in i.keys():
                                # print(j)
                                if j[1] == "DateField":
                                    i[j[0]] = None
                                else:
                                    i[j[0]] = ''
                    num1 = 0
                    if startupload:
                        for i in uploadxlsxlist:
                            num1 += 1
                            # print(num1)
                            # print(i)
                            # modeldata = {}
                            # for key, value in i.items():
                            #     if key in headermodel_Device.keys():
                            #         if headermodel_Device[key] == "Predict_return" or headermodel_Device[
                            #             key] == "Borrow_date" or headermodel_Device[key] == "Return_date":
                            #             print(value)
                            #             modeldata[headermodel_Device[key]] = value.split("/")[2] + "-" + \
                            #                                                        value.split("/")[0] + "-" + \
                            #                                                        value.split("/")[1]
                            #         else:
                            #             modeldata[headermodel_Device[key]] = value
                            Check_dic = {
                                'Number': i['Number'],
                            }
                            # print(modeldata)
                            # print(i)
                            # Check_dic_Gantt['Test_Start'] = None  # 日期格式为空NULL不能用空字符
                            if AutoItems.objects.filter(**Check_dic):  # 已经存在覆盖
                                AutoItems.objects.filter(
                                    **Check_dic).update(**i)
                            else:  # 新增
                                AutoItems.objects.create(**i)
                        errMsg = '上傳成功'

                    # mock_data
                    if ckeck_dic:
                        # print(checkAdaPow)
                        mock_datalist = AutoItems.objects.filter(**ckeck_dic)

                    else:
                        mock_datalist = AutoItems.objects.all()
                    for i in mock_datalist:
                        mock_data.append(
                            {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                             "BaseBenfit": i.BaseIncome,
                             "CaseID": i.CaseID,
                             "CaseName": i.CaseName,
                             "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                             "Owner": i.Owner, "Comment": i.Comment,
                             }
                        )
                    # print(mock_data)
                if 'MUTICANCEL' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    for i in responseData["params"]:
                        AutoItems.objects.filter(id=i).delete()

                    ckeck_dic = {}
                    Customer = responseData['Customer']
                    if Customer and Customer != "All":
                        ckeck_dic['Customer'] = Customer
                    ValueIf = responseData['VA_NVA']
                    if ValueIf and ValueIf != "All":
                        ckeck_dic['ValueIf'] = ValueIf

                    # mock_data
                    if ckeck_dic:
                        # print(checkAdaPow)
                        mock_datalist = AutoItems.objects.filter(**ckeck_dic)

                    else:
                        mock_datalist = AutoItems.objects.all()
                    for i in mock_datalist:
                        mock_data.append(
                            {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                             "BaseBenfit": i.BaseIncome,
                             "CaseID": i.CaseID,
                             "CaseName": i.CaseName,
                             "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                             "Owner": i.Owner, "Comment": i.Comment,
                             }
                        )
                    # print(mock_data)

        data = {
            'canEdit': canEdit,
            'selectCustomer': selectCustomer,
            'selectStatus': selectStatus,
            'content': mock_data,
            'errMsg': errMsg,
            'errMsgNumber': errMsgNumber,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'AutoResult/AutoItem_edit.html', locals())

@csrf_exempt
def AutoResult_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Automation效益/AutoResult_edit"



    # roles = []
    # onlineuser = request.session.get('account')
    # # print(UserInfo.objects.get(account=onlineuser))
    # for i in UserInfo.objects.get(account=onlineuser).role.all():
    #     roles.append(i.name)
    # # print(roles)
    # editPpriority = 100
    # for i in roles:
    #     if i == 'admin':
    #         editPpriority = 4
    #     elif 'PM' in i:
    #         if editPpriority != 4:
    #             editPpriority = 1
    #     elif 'RD' in i:
    #         if editPpriority != 4 and editPpriority != 1:
    #             editPpriority = 2
    #     elif 'DQA' in i:
    #         if 'DQA_SW' in i:
    #             if editPpriority != 4 and editPpriority != 1:
    #                 editPpriority = 5
    #         if 'DQA_ME' in i:
    #             if editPpriority != 4 and editPpriority != 1:
    #                 editPpriority = 6
    #         if 'DQA_INV' in i:
    #             if editPpriority != 4 and editPpriority != 1:
    #                 editPpriority = 4
    #     elif "JQE" in i:
    #         editPpriority = 3
    #     else:
    #         editPpriority = 0
    selectCustomer = {
        # "A39": [{"Project": "FAV10"}, {"Project": "GOG20"}, {"Project": "GOG21"}],
        # "C38(AIO)": [{"Project": "GOA30"}, {"Project": "GOC5051"}],
        # "C38(NB)": [{"Project": "GLMS1"}],
    }
    Customer_list = list(CQMProject.objects.all().values('Customer').distinct().order_by('Customer'))
    for i in list(AutoProject.objects.all().values('Customer').distinct().order_by('Customer')):
        if i not in Customer_list:
            Customer_list.append(i)
    for i in Customer_list:
        Customerlist = []
        for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('-Project'):
            Projectinfo = {}
            Projectinfo['value'] = j['Project']
            checkPro_dic = {"Customer": i['Customer'], "ComPrjCode": j['Project']}
            # print(ProjectinfoinDCT.objects.filter(**check_dic).first())
            if ProjectinfoinDCT.objects.filter(**checkPro_dic).first():
                Projectinfo['Year'] = ProjectinfoinDCT.objects.filter(**checkPro_dic).first().SS.split("/")[2][:4]
            else:
                Projectinfo['Year'] = ""
            Customerlist.append(Projectinfo)
        for j in AutoProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            Projectinfo['value'] = j['Project']
            Projectinfo['Year'] = AutoProject.objects.filter(Customer=i['Customer'],Project=j['Project']).first().Year
            Customerlist.append(Projectinfo)
        selectCustomer[i['Customer']] = Customerlist


    mock_data = [
        # {"id": "1", "Number": "110", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5, "ProjectData": 2,
        #  "CaseID": "PFA005_01", "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "Status": "使用", "FunctionInt": "硬盤，內存信息檢查，基本功能測試",
        #  "Comments": "11"},
        # {"id": "2", "Number": "112", "CG": "C38(AIO)", "VA_NVA": "NVA", "BaseBenfit": 0.5, "ProjectData": 0,
        #  "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test", "NPIBenfit": 0,
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": ""},
        # {"id": "3", "Number": "113", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5, "ProjectData": 3,
        #  "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": "22"},
        # {"id": "4", "Number": "114", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5, "ProjectData": 1,
        #  "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": ""},
    ]

    canEdit = 0
    if request.method == "POST":
        if request.POST:
            if request.POST.get('isGetData') == 'first':
                # mock_datalist = AutoItems.objects.all()
                # for i in mock_datalist:
                #     mock_data.append(
                #         {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                #          "BaseBenfit": i.BaseIncome,
                #          "CaseID": i.CaseID,
                #          "CaseName": i.CaseName,
                #          "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                #          "Owner": i.Owner, "Comment": i.Comment,
                #          }
                #     )
                pass
            if request.POST.get('isGetData') == 'SEARCH':
                Customer = request.POST.get('Customer')
                Project = request.POST.get('Project')
                Check_dic_Project = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'), }
                # Phase = request.POST.get('Phase')
                Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                current_user = request.session.get('user_name')
                if Projectinfo:
                    for k in Projectinfo.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
                ProjectinfoAuto = AutoProject.objects.filter(**Check_dic_Project).first()
                # current_user = request.session.get('user_name')
                if ProjectinfoAuto:
                    for k in ProjectinfoAuto.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
                # mock_datalist = AutoItems.objects.all()
                # mock_datalist = AutoItems.objects.exclude(Status="Ongoing")
                mock_datalist = AutoItems.objects.filter(Status__in=["Ready", "Cancel"])
                # print(mock_datalist)
                for i in mock_datalist:
                    ProjectData = 0
                    Comments = ""
                    # check_dic = {"Number": i.Number, "ProjectName": Project}
                    if "INV" in Project.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                            "Projectinfo": AutoProject.objects.filter(Project=Project).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                            "ProjectinfoCQM": CQMProject.objects.filter(Project=Project).first()}
                    if AutoResult.objects.filter(**check_dic):
                        if AutoResult.objects.filter(**check_dic).first().Cycles:
                            ProjectData = int(AutoResult.objects.filter(**check_dic).first().Cycles)
                        Comments = AutoResult.objects.filter(**check_dic).first().Comments
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                         "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment, "ProjectData": ProjectData,"Comments": Comments
                         }
                    )
            if request.POST.get('isGetData') == 'SAVE':
                Customer = request.POST.get('Customer')
                Project = request.POST.get('Project')
                Number = request.POST.get('rowIndex')
                ProjectData = request.POST.get('ProjectData')
                Comments = request.POST.get('Comments')
                # check_dic_Result = {"Number": Number, "ProjectName": Project}
                if "INV" in Project.upper():
                    check_dic_Result = {"AutoItem": AutoItems.objects.filter(Number=Number).first(),
                                        "Projectinfo": AutoProject.objects.filter(Project=Project).first()}
                else:
                    check_dic_Result = {"AutoItem": AutoItems.objects.filter(Number=Number).first(),
                                        "ProjectinfoCQM": CQMProject.objects.filter(Project=Project).first()}
                SSYear = ''
                for i in selectCustomer:
                    for j in selectCustomer[i]:
                        if j["value"] == Project:
                            SSYear = j["Year"]
                # print(check_dic_Result)
                if AutoResult.objects.filter(**check_dic_Result):
                    update_dic = {"ValueIf": AutoItems.objects.filter(Number=Number).first().ValueIf,
                                "Cycles": ProjectData, "Year": SSYear, "Comments": Comments,
                                  "editor": request.session.get('user_name'),
                                  "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                  }
                    AutoResult.objects.filter(**check_dic_Result).update(**update_dic)
                else:
                    creat_dic = {
                        "Number": Number, "ValueIf": AutoItems.objects.filter(Number=Number).first().ValueIf,
                                 "ProjectName": Project, "Year": SSYear, "Cycles": ProjectData, "Comments": Comments,
                                 "editor": request.session.get('user_name'),
                                 "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                 }
                    creat_dic.update(check_dic_Result)
                    # print(creat_dic)
                    AutoResult.objects.create(**creat_dic)

                Check_dic_Project = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'), }
                # Phase = request.POST.get('Phase')
                Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                current_user = request.session.get('user_name')
                if Projectinfo:
                    for k in Projectinfo.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
                ProjectinfoAuto = AutoProject.objects.filter(**Check_dic_Project).first()
                # current_user = request.session.get('user_name')
                if ProjectinfoAuto:
                    for k in ProjectinfoAuto.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
                # mock_datalist = AutoItems.objects.all()
                mock_datalist = AutoItems.objects.exclude(Status="Ongoing")
                for i in mock_datalist:
                    ProjectData = 0
                    Comments = ""
                    check_dic = {"Number": i.Number, "ProjectName": Project}
                    if AutoResult.objects.filter(**check_dic):
                        if AutoResult.objects.filter(**check_dic).first().Cycles:
                            ProjectData = int(AutoResult.objects.filter(**check_dic).first().Cycles)
                        Comments = AutoResult.objects.filter(**check_dic).first().Comments
                    mock_data.append(
                        {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                         "BaseBenfit": i.BaseIncome,
                         "CaseID": i.CaseID,
                         "CaseName": i.CaseName,
                         "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                         "Owner": i.Owner, "Comment": i.Comment, "ProjectData": ProjectData,"Comments": Comments
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
                if 'ExcelData' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    ckeck_dic = {}
                    Customer = responseData['customer']
                    if Customer and Customer != "All":
                        ckeck_dic['Customer'] = Customer
                    Project = responseData['project']
                    if Project and Project != "All":
                        ckeck_dic['Project'] = Project

                    if "INV" in Project.upper():
                        check_dic_Result = {
                            # "AutoItem": AutoItems.objects.filter(Number=Number).first(),
                                            "Projectinfo": AutoProject.objects.filter(Project=Project).first()}
                    else:
                        check_dic_Result = {
                            # "AutoItem": AutoItems.objects.filter(Number=Number).first(),
                                            "ProjectinfoCQM": CQMProject.objects.filter(Project=Project).first()}
                    SSYear = ''
                    for i in selectCustomer:
                        for j in selectCustomer[i]:
                            if j["value"] == Project:
                                SSYear = j["Year"]

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
                        # print(type(i), i)
                        rownum += 1
                        # print(rownum)
                        modeldata = {}
                        for key, value in i.items():
                            if key in headermodel_ProResult.keys():
                                modeldata[headermodel_ProResult[key]] = value
                        if 'Number' in modeldata.keys():
                            startupload = 1
                        else:
                            # canEdit = 0
                            startupload = 0
                            err_ok = 2
                            errMsg = err_msg = """
                                                        第"%s"條數據，编号不能爲空
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
                    # 让数据可以从有值更新为无值
                    AutoResultModelfiedlist = []
                    for i in AutoResult._meta.fields:
                        if i.name != 'id':
                            # print(i)
                            AutoResultModelfiedlist.append([i.name, i.get_internal_type()])
                    for i in uploadxlsxlist:
                        for j in AutoResultModelfiedlist:
                            if j[0] not in i.keys():
                                # print(j)
                                if j[1] == "DateField":
                                    i[j[0]] = None
                                else:
                                    i[j[0]] = ''
                    num1 = 0
                    if startupload:
                        for i in uploadxlsxlist:
                            if i["Cycles"] and i["Cycles"]!='0' or i["Comments"]:
                                num1 += 1
                                # print(num1)
                                # print(i)
                                # modeldata = {}
                                # for key, value in i.items():
                                #     if key in headermodel_Device.keys():
                                #         if headermodel_Device[key] == "Predict_return" or headermodel_Device[
                                #             key] == "Borrow_date" or headermodel_Device[key] == "Return_date":
                                #             print(value)
                                #             modeldata[headermodel_Device[key]] = value.split("/")[2] + "-" + \
                                #                                                        value.split("/")[0] + "-" + \
                                #                                                        value.split("/")[1]
                                #         else:
                                #             modeldata[headermodel_Device[key]] = value
                                check_dic_Result["AutoItem"] = AutoItems.objects.filter(Number=i["Number"]).first()
                                # print(modeldata)
                                # print(i)
                                # Check_dic_Gantt['Test_Start'] = None  # 日期格式为空NULL不能用空字符
                                if AutoResult.objects.filter(**check_dic_Result):  # 已经存在覆盖
                                    update_dic = {"ValueIf": AutoItems.objects.filter(Number=i["Number"]).first().ValueIf,
                                                  "Year": SSYear,
                                                  "Cycles": i["Cycles"], "Comments": i["Comments"],
                                                  "editor": request.session.get('user_name'),
                                                  "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                                  }
                                    # print(update_dic)
                                    AutoResult.objects.filter(
                                        **check_dic_Result).update(**update_dic)
                                else:  # 新增
                                    creat_dic = {
                                        "Number": i["Number"],
                                        "ValueIf": AutoItems.objects.filter(Number=i["Number"]).first().ValueIf,
                                        "ProjectName": Project, "Year": SSYear, "Cycles": i["Cycles"], "Comments": i["Comments"],
                                        "editor": request.session.get('user_name'),
                                        "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    }
                                    creat_dic.update(check_dic_Result)
                                    # print(creat_dic)
                                    AutoResult.objects.create(**creat_dic)
                        errMsg = '上傳成功'

                    # mock_data
                    # mock_datalist = AutoItems.objects.all()
                    mock_datalist = AutoItems.objects.exclude(Status="Ongoing")
                    for i in mock_datalist:
                        ProjectData = 0
                        Comments = ""
                        # check_dic = {"Number": i.Number, "ProjectName": Project}
                        if "INV" in Project.upper():
                            check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                         "Projectinfo": AutoProject.objects.filter(Project=Project).first()}
                        else:
                            check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                         "ProjectinfoCQM": CQMProject.objects.filter(Project=Project).first()}
                        # print(check_dic)
                        if AutoResult.objects.filter(**check_dic):
                            # print(AutoResult.objects.filter(**check_dic))
                            if AutoResult.objects.filter(**check_dic).first().Cycles:
                                ProjectData = int(AutoResult.objects.filter(**check_dic).first().Cycles)
                            Comments = AutoResult.objects.filter(**check_dic).first().Comments
                            # print(ProjectData, Comments)
                        mock_data.append(
                            {"id": i.id, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                             "BaseBenfit": i.BaseIncome,
                             "CaseID": i.CaseID,
                             "CaseName": i.CaseName,
                             "Item": i.Item, "Status": i.Status, "FunctionInt": i.FunDescription,
                             "Owner": i.Owner, "Comment": i.Comment, "ProjectData": ProjectData, "Comments": Comments
                             }
                        )

        data = {
            'canEdit': canEdit,
            'selectCustomer': selectCustomer,
            'content': mock_data,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'AutoResult/AutoResult_edit.html', locals())

@csrf_exempt
def AutoResult_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Automation效益/AutoResult_search"

    mock_data = [
        # {"id": "1", "ProjectResult": [{"projectName": "EL4C2", "result": 20}, {"projectName": "EL4C4", "result": 30}, {"projectName": "EL4C5", "result": 40}], "Number": "110", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5,
        #  "SummaryBenfit": 26, "NPIBenfit": "10",
        #  "CaseID": "PFA005_01", "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "Status": "使用", "FunctionInt": "硬盤，內存信息檢查，基本功能測試",
        #  "Comments": "11"},
        # {"id": "2", "Number": "112", "CG": "C38(AIO)", "VA_NVA": "NVA", "BaseBenfit": 0.5, "ProjectData": 0,
        #  "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": ""},
        # {"id": "3", "ProjectResult": [{"projectName": "EL4C2", "result": 20}, {"projectName": "EL4C4", "result": 30}, {"projectName": "EL4C5", "result": 40}], "Number": "113", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5,
        #  "ProjectData": "", "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": "22"},
        # {"id": "4", "Number": "114", "CG": "C38(NB)", "VA_NVA": "VA", "BaseBenfit": 0.5, "ProjectData": 1,
        #  "CaseID": "PFA005_01",
        #  "CaseName": "Stress-Manual Power Management Cycles Test",
        #  "Item": "Battery life- Battery leackage(S3)", "FunctionInt": "硬盤，內存信息檢查，基本功能測試", "Comments": ""},
    ]

    selectCustomer = [
        "All",
        # "A39", "C38(NB)", "C38(AIO)"
    ]

    selectCustomerYear = {
        # "A39": [{"Project": "FAV10"}, {"Project": "GOG20"}, {"Project": "GOG21"}],
        # "C38(AIO)": [{"Project": "GOA30"}, {"Project": "GOC5051"}],
        # "C38(NB)": [{"Project": "GLMS1"}],
    }
    selectCustomerYearNPI = [
        # "GLMA0",
    ]
    Customer_list = list(CQMProject.objects.all().values('Customer').distinct().order_by('Customer'))
    for i in list(AutoProject.objects.all().values('Customer').distinct().order_by('Customer')):
        if i not in Customer_list:
            Customer_list.append(i)
    # print(Customer_list)
    for i in Customer_list:
        selectCustomer.append(i["Customer"])
    for i in Customer_list:
        Customerlist = []
        for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            selectCustomerYearNPI.append(j['Project'])
            Projectinfo = {}
            Projectinfo['Project'] = j['Project']
            checkPro_dic = {"Customer": i['Customer'], "ComPrjCode": j['Project']}
            # print(ProjectinfoinDCT.objects.filter(**check_dic).first())
            if ProjectinfoinDCT.objects.filter(**checkPro_dic).first():
                Projectinfo['Year'] = ProjectinfoinDCT.objects.filter(**checkPro_dic).first().SS.split("/")[2][:4]
            else:
                Projectinfo['Year'] = ""
            Customerlist.append(Projectinfo)
        for j in AutoProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            Projectinfo['Project'] = j['Project']
            Projectinfo['Year'] = AutoProject.objects.filter(Customer=i['Customer'], Project=j['Project']).first().Year
            Customerlist.append(Projectinfo)
        selectCustomerYear[i['Customer']] = Customerlist
    # print(selectCustomerYear)

    projectMsg = [
        # {"YEAR": 2010, "COMPRJCODE": "EL4C2", "PrjEngCode1": "", "PrjEngCode2": "", "PROJECT": "LENOVO", "SIZE": 12,
        #  "CPU": "INTEL",
        #  "PLATFORM": "", "VGA": "", "OSSUPPORT": "", "SS": "", "LD": "", "DQAPL": "", "TYPE": "INTEL",
        #  "PPA": "", "PQE": "", "id": 201467},
        # {"YEAR": 2013, "COMPRJCODE": "EL4C2", "PrjEngCode1": "", "PrjEngCode2": "", "PROJECT": "LENOVO", "SIZE": 12,
        #  "CPU": "INTEL",
        #  "PLATFORM": "", "VGA": "", "OSSUPPORT": "", "SS": "", "LD": "", "DQAPL": "", "TYPE": "INTEL",
        #  "PPA": "", "PQE": "", "id": 201468},
        # {"YEAR": 2014, "COMPRJCODE": "EL4C2", "PrjEngCode1": "", "PrjEngCode2": "", "PROJECT": "LENOVO", "SIZE": 12,
        #  "CPU": "INTEL",
        #  "PLATFORM": "", "VGA": "", "OSSUPPORT": "", "SS": "", "LD": "", "DQAPL": "", "TYPE": "INTEL",
        #  "PPA": "", "PQE": "", "id": 201469},
    ]

    canEdit = 1
    if request.method == "POST":
        if request.POST.get("isGetData") == "searchalert":
            Customer = request.POST.get('Customer')
            Year = request.POST.get('Year')
            Prolist = []
            if Customer != "All":#前端加了为空的判断,所以Customer不可能为空，并且el-option的value不能设为空
                if not Year:
                    for i in CQMProject.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                            "Project"):
                        Prolist.append(i["Project"])
                    for i in AutoProject.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                            "Project"):
                        Prolist.append(i["Project"])
                else:
                    for i in CQMProject.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                            "Project"):
                        for j in selectCustomerYear:
                            # print(j)
                            for k in selectCustomerYear[j]:
                                # print(k)
                                if i["Project"] == k["Project"]:
                                    if k["Year"] == Year:
                                        Prolist.append(i["Project"])
                    for i in AutoProject.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                            "Project"):
                        for j in selectCustomerYear:
                            for k in selectCustomerYear[j]:
                                if i["Project"] == k["Project"]:
                                    if k["Year"] == Year:
                                        Prolist.append(i["Project"])
            else:
                if not Year:
                    for i in CQMProject.objects.all().values("Project").distinct().order_by("Project"):
                        Prolist.append(i["Project"])
                    for i in AutoProject.objects.all().values("Project").distinct().order_by("Project"):
                        Prolist.append(i["Project"])
                else:
                    for i in CQMProject.objects.all().values("Project").distinct().order_by("Project"):
                        for j in selectCustomerYear:
                            for k in selectCustomerYear[j]:
                                if i["Project"] == k["Project"]:
                                    if k["Year"] == Year:
                                        Prolist.append(i["Project"])
                    for i in AutoProject.objects.all().values("Project").distinct().order_by("Project"):
                        for j in selectCustomerYear:
                            for k in selectCustomerYear[j]:
                                if i["Project"] == k["Project"]:
                                    if k["Year"] == Year:
                                        Prolist.append(i["Project"])
            # print(Prolist)
            for i in Prolist:
                # print(i)
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                    projectMsg.append({
                        "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().id,
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Year, "COMPRJCODE": i,
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().VGA,
                        "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().OSSupport,
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().LD,
                        "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPL,
                    })
                else:
                    # print(i)
                    projectMsg.append({
                        "id": "",
                        "YEAR": "", "COMPRJCODE": i,
                        "CUSPRJCODE": "",
                        "ProjectName": "",
                        "SIZE": "",
                        "CPU": "",
                        "PLATFORM": "",
                        "VGA": "",
                        "OSSUPPORT": "",
                        "Type": "",
                        "PPA": "",
                        "PQE": "",
                        "SS": "",
                        "LD": "",
                        "DQAPL": "",
                    })
            # print(projectMsg)
        if request.POST.get("action") == "getMsg":
            Customer = request.POST.get('customer')
            Year = request.POST.get('Year')
            Projectlist = request.POST.getlist("projectMsg", [])
            check_dic = {}

            # if Customer:
            #     check_dic["Customer"] = Customer
            # if Year:
            #     check_dic["Year"] = Year
            # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            # mock_datalist = AutoItems.objects.exclude(Status="Ongoing")
            mock_datalist = AutoItems.objects.filter(Status__in=["Ready", "Cancel"])
            for i in mock_datalist:
                SummaryBenfit = 0
                NPIBenfit = 0
                ProjectResult = []
                for j in Projectlist:
                    # check_dic["ProjectName"] = j
                    # check_dic["Number"] = i.Number
                    # # print(check_dic)
                    # AutoResult_Projectinfo = AutoResult.objects.filter(**check_dic).first()
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                            "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i.Number).first(),
                                            "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    AutoResult_Projectinfo = AutoResult.objects.filter(**check_dic).first()
                    # print(AutoResult_Projectinfo)
                    if AutoResult_Projectinfo:
                        # print(AutoResult_Projectinfo)
                        ProjectResult.append({"projectName": j, "result": AutoResult_Projectinfo.Cycles,
                                              "Comments": AutoResult_Projectinfo.Comments})
                    else:  # 占位，否则结果会错位
                        ProjectResult.append({"projectName": j, "result": '',
                                              "Comments": ''})
                SummaryProject = 0
                NPIProject = 0
                # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                for j in ProjectResult:
                    if j["result"]:
                        SummaryProject += float(j["result"])
                        # for m in list(AutoProject.objects.all().values('Project').distinct().order_by('Project')):
                        #     # print(m,j["projectName"])
                        #     if j["projectName"] not in m["Project"]:
                        #         NPIProject += float(j["result"])
                        # print(selectCustomerYearNPI)
                        if j["projectName"] in selectCustomerYearNPI:
                            NPIProject += float(j["result"])
                SummaryBenfit = SummaryProject * float(i.BaseIncome)
                NPIBenfit = NPIProject * float(i.BaseIncome)
                # print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                mock_data.append(
                    {"id": i.id, "ProjectResult": ProjectResult, "Number": i.Number, "CG": i.Customer, "VA_NVA": i.ValueIf,
                     "BaseBenfit": i.BaseIncome,
                     "SummaryBenfit": SummaryBenfit, "NPIBenfit": NPIBenfit,
                     "CaseID": i.CaseID, "CaseName": i.CaseName,
                     "Item": i.Item, "Status": i.Status, "Owner": i.Owner, "FunctionInt": i.FunDescription,
                     "Comments": i.Comment}
                )
        data = {
            "content": mock_data,
            "canEdit": canEdit,
            "projectMsg": projectMsg,
            "selectCustomer": selectCustomer,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'AutoResult/AutoResult_search.html', locals())


@csrf_exempt
def AutoResult_summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Automation效益/AutoResult_summary"

    ItemSummary = AutoItems.objects.all().count()

    CategoryData = ["NPI", "Total"]
    VAData = [0, 0]
    NVAData = [0, 0]
    VA_NVA = [
        {
            "name": "VA",
            "type": "bar",
            "stack": "status",
            "barMaxWidth": 50,
            "data": VAData
        },
        {
            "name": "N-VA",
            "type": "bar",
            "stack": "status",
            "barMaxWidth": 50,
            "data": NVAData
        },
    ]

    selectCustomerYear = {
        # "A39": [{"Project": "FAV10"}, {"Project": "GOG20"}, {"Project": "GOG21"}],
        # "C38(AIO)": [{"Project": "GOA30"}, {"Project": "GOC5051"}],
        # "C38(NB)": [{"Project": "GLMS1"}],
    }
    selectCustomerYearNPI = [
        # "GLMA0",
    ]
    Customer_list = list(CQMProject.objects.all().values('Customer').distinct().order_by('Customer'))
    for i in list(AutoProject.objects.all().values('Customer').distinct().order_by('Customer')):
        if i not in Customer_list:
            Customer_list.append(i)
    # print(Customer_list)

    for i in Customer_list:
        Customerlist = []
        for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            selectCustomerYearNPI.append(j['Project'])
            Projectinfo = {}
            Projectinfo['Project'] = j['Project']
            checkPro_dic = {"Customer": i['Customer'], "ComPrjCode": j['Project']}
            # print(ProjectinfoinDCT.objects.filter(**check_dic).first())
            if ProjectinfoinDCT.objects.filter(**checkPro_dic).first():
                Projectinfo['Year'] = ProjectinfoinDCT.objects.filter(**checkPro_dic).first().SS.split("/")[2][:4]
            else:
                Projectinfo['Year'] = ""
            Customerlist.append(Projectinfo)
        for j in AutoProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            Projectinfo['Project'] = j['Project']
            Projectinfo['Year'] = AutoProject.objects.filter(Customer=i['Customer'], Project=j['Project']).first().Year
            Customerlist.append(Projectinfo)
        selectCustomerYear[i['Customer']] = Customerlist

    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(CQMtest.objects.all().count())
            Year = request.POST.get("Year")
            if not Year:
                Year = str(datetime.datetime.now().year)
            VAitems = list(AutoItems.objects.filter(ValueIf="VA").values("Number").distinct())
            NVAitems = list(AutoItems.objects.filter(ValueIf="N-VA").values("Number").distinct())
            Projectlist_Total = []
            for i in selectCustomerYear:
                for j in selectCustomerYear[i]:
                    if j["Year"] == Year:
                        Projectlist_Total.append(j["Project"])
            VAData_Total = 0
            for i in VAitems:
                for j in Projectlist_Total:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        VAData_Total += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            NVAData_Total = 0
            for i in NVAitems:
                for j in Projectlist_Total:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        NVAData_Total += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            Projectlist_NPI = []
            for i in CQMProject.objects.all().values('Project').distinct().order_by('Project'):
                # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first())
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                    if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS.split("/")[2][:4] == Year:
                        Projectlist_NPI.append(i["Project"])
            VAData_NPI = 0
            for i in VAitems:
                for j in Projectlist_NPI:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        VAData_NPI += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            NVAData_NPI = 0
            for i in NVAitems:
                for j in Projectlist_NPI:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        NVAData_NPI += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            VAData = [VAData_NPI, VAData_Total]
            NVAData = [NVAData_NPI, NVAData_Total]
            VA_NVA = [
                {
                    "name": "VA",
                    "type": "bar",
                    "stack": "status",
                    "barMaxWidth": 50,
                    "data": VAData
                },
                {
                    "name": "N-VA",
                    "type": "bar",
                    "stack": "status",
                    "barMaxWidth": 50,
                    "data": NVAData
                },
            ]
        if request.POST.get("isGetData") == "Search":
            Year = request.POST.get("Year")
            if not Year:
                Year = str(datetime.datetime.now().year)
            VAitems = list(AutoItems.objects.filter(ValueIf="VA").values("Number").distinct())
            NVAitems = list(AutoItems.objects.filter(ValueIf="N-VA").values("Number").distinct())
            Projectlist_Total = []
            for i in selectCustomerYear:
                for j in selectCustomerYear[i]:
                    if j["Year"] == Year:
                        Projectlist_Total.append(j["Project"])
            VAData_Total = 0
            for i in VAitems:
                for j in Projectlist_Total:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                            "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                            "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        VAData_Total += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles)*float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            NVAData_Total = 0
            for i in NVAitems:
                for j in Projectlist_Total:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        NVAData_Total += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            Projectlist_NPI = []
            for i in CQMProject.objects.all().values('Project').distinct().order_by('Project'):
                # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first())
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                    if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS.split("/")[2][:4] == Year:
                        Projectlist_NPI.append(i["Project"])
            VAData_NPI = 0
            for i in VAitems:
                for j in Projectlist_NPI:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        VAData_NPI += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            NVAData_NPI = 0
            for i in NVAitems:
                for j in Projectlist_NPI:
                    if "INV" in j.upper():
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "Projectinfo": AutoProject.objects.filter(Project=j).first()}
                    else:
                        check_dic = {"AutoItem": AutoItems.objects.filter(Number=i["Number"]).first(),
                                     "ProjectinfoCQM": CQMProject.objects.filter(Project=j).first()}
                    if AutoResult.objects.filter(**check_dic).first():
                        NVAData_NPI += float(
                            AutoResult.objects.filter(**check_dic).first().Cycles) * float(
                            AutoItems.objects.filter(Number=i["Number"]).first().BaseIncome)
            VAData = [VAData_NPI, VAData_Total]
            NVAData = [NVAData_NPI, NVAData_Total]
            VA_NVA = [
                {
                    "name": "VA",
                    "type": "bar",
                    "stack": "status",
                    "barMaxWidth": 50,
                    "data": VAData
                },
                {
                    "name": "N-VA",
                    "type": "bar",
                    "stack": "status",
                    "barMaxWidth": 50,
                    "data": NVAData
                },
            ]


        data = {
            'ItemSummary': ItemSummary,
            'CategoryData': CategoryData,
            'VA_NVA': VA_NVA,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'AutoResult/AutoResult_summary.html', locals())