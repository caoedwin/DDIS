from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import datetime,json,simplejson,requests,time
from .forms import INVGantt_F
from .models import INVGantt
from app01.models import ProjectinfoinDCT
from django.db.models import Max,Min,Sum,Count,Q
from django.db.models.functions import ExtractYear
# Create your views here.
@csrf_exempt
def INVGantt_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="INVGantt/INVGantt_upload"
    repeatcontend = [
    ]
    err_ok = 0  # excel上传1为重复
    canEdit = 0
    result = 0  # 为1 forms 上传重复
    INVGantt_F_list = INVGantt_F(request.POST)
    if request.method == 'POST':
        canEdit = 1  # 机种权限 1有权限,前端是用的{{}}传值的，法国在上面，一进upload界面就提示没有权限
        if 'Upload' in request.POST.keys():
            # print(request.POST)
            if INVGantt_F_list.is_valid():
                # print("yes")
                Check_dic = {
                              'Customer': request.POST.get('Customer'),
                                'INV_Number': request.POST.get('INV_Number'),
                              'INV_Model': request.POST.get('INV_Model'),
                              'Project_Name': request.POST.get('Project_Name'),
                              # 'Year': request.POST.get('Year'), 'Unit_Qty': request.POST.get('Unit_Qty'),
                              # 'TP_Kinds': request.POST.get('TP_Kinds'),
                              # 'Qualify_Cycles': request.POST.get('Qualify_Cycles'),
                              'Status': request.POST.get('Status'),
                              'TP_Cat': request.POST.get('TP_Cat'),
                              'Trial_Run_Type': request.POST.get('Trial_Run_Type'),
                              'TP_Vendor': request.POST.get('TP_Vendor'),
                              'TP_Key_Parameter': request.POST.get('TP_Key_Parameter'),
                              'Lenovo_TP_PN': request.POST.get('Lenovo_TP_PN'),
                              'Compal_TP_PN': request.POST.get('Compal_TP_PN'),

                             }
                # if request.POST.get('Customer'):
                #     Check_dic['Customer'] = request.POST.get('Customer')
                # if request.POST.get('INV_Number'):
                #     Check_dic['INV_Number'] = request.POST.get('INV_Number')
                # if request.POST.get('INV_Model'):
                #     Check_dic['INV_Model'] = request.POST.get('INV_Model')
                # if request.POST.get('Project_Name'):
                #     Check_dic['Project_Name'] = request.POST.get('Project_Name')
                # if request.POST.get('TP_Cat'):
                #     Check_dic['TP_Cat'] = request.POST.get('TP_Cat')
                # if request.POST.get('Trial_Run_Type'):
                #     Check_dic['Trial_Run_Type'] = request.POST.get('Trial_Run_Type')
                # if request.POST.get('TP_Vendor'):
                #     Check_dic['TP_Vendor'] = request.POST.get('TP_Vendor')
                # if request.POST.get('TP_Key_Parameter'):
                #     Check_dic['TP_Key_Parameter'] = request.POST.get('TP_Key_Parameter')
                # if request.POST.get('Lenovo_TP_PN'):
                #     Check_dic['Lenovo_TP_PN'] = request.POST.get('Lenovo_TP_PN')
                # if request.POST.get('Compal_TP_PN'):
                #     Check_dic['Compal_TP_PN'] = request.POST.get('Compal_TP_PN')


                Create_dic = {
                              'Customer': request.POST.get('Customer'), 'INV_Number': request.POST.get('INV_Number'),
                              'INV_Model': request.POST.get('INV_Model'),
                              'Project_Name': request.POST.get('Project_Name'),
                              'Year': request.POST.get('Year'), 'Unit_Qty': request.POST.get('Unit_Qty'),
                              'TP_Kinds': request.POST.get('TP_Kinds'),
                              'Qualify_Cycles': request.POST.get('Qualify_Cycles'),
                              'Status': request.POST.get('Status'), 'TP_Cat': request.POST.get('TP_Cat'),
                              'Trial_Run_Type': request.POST.get('Trial_Run_Type'),
                              'TP_Vendor': request.POST.get('TP_Vendor'),
                              'TP_Key_Parameter': request.POST.get('TP_Key_Parameter'),
                              'Lenovo_TP_PN': request.POST.get('Lenovo_TP_PN'),
                              'Compal_TP_PN': request.POST.get('Compal_TP_PN'),
                              'Issue_Link': request.POST.get('Issue_Link'),
                              'Remark': request.POST.get('Remark'), 'Attend_Time': request.POST.get('Attend_Time'),
                              'Get_INV': request.POST.get('Get_INV'), 'Month': request.POST.get('Month'),
                              'Test_Start': request.POST.get('Test_Start'),
                              'Test_End': request.POST.get('Test_End'),
                              'Editor': request.session.get('user_name'),
                              'Edittime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                # print(Create_dic)

                if INVGantt.objects.filter(**Check_dic).first():
                    UpdateResult = "数据已存在数据库中"
                    # print(UpdateResult)
                    repeatcontend.append({})
                    # message_err=1
                    result = 1
                else:
                    # print("Create")
                    INVGantt.objects.create(**Create_dic)
            else:
                # print("no")
                cleandata = INVGantt_F_list.errors
                # print(cleandata)
        if 'type' in request.POST:

            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))

            INVGanttList = [{
                'Customer': 'Customer', 'INV_Number': 'INV_Number', 'INV_Model': 'INV_Model', 'Project_Name': 'Project_Name',
                'Unit_Origin': 'Unit_Origin',
                 # 'Year': 'Year', 'Unit_Qty': 'Unit_Qty', 'TP_Kinds': 'TP_Kinds', 'Qualify_Cycles': 'Qualify_Cycles',
                 # 'Status': 'Status',
                 'TP_Cat': 'TP_Cat', 'Trial_Run_Type': 'Trial_Run_Type', 'TP_Vendor': 'TP_Vendor',
                 'TP_Key_Parameter': 'TP_Key_Parameter', 'Lenovo_TP_PN': 'Lenovo_TP_PN', 'Compal_TP_PN': 'Compal_TP_PN',
                 # 'Issue_Link': 'Issue_Link', 'Remark': 'Remark',
                 # 'Attend_Time': 'Attend_Time', 'Get_INV': 'Get_INV', 'Month': 'Month', 'Test_Start': 'Test_Start', 'Test_End': 'Test_End',
                 }]
            for i in simplejson.loads(xlsxlist):
                # print(i)
                Check_dic_Gantt = {}
                if 'Customer' in i.keys():
                    Customer = i['Customer']
                    Check_dic_Gantt['Customer'] = Customer
                else:
                    Check_dic_Gantt['Customer'] = ''#空字符搜索与没有此关键字的搜索结果完全不一样，并且数据库中这些字段都是字符型数据
                # if 'INV_Number' in i.keys():
                #     INV_Number = i['INV_Number']
                #     Check_dic_Gantt['INV_Number'] = INV_Number
                # else:
                #     Check_dic_Gantt['INV_Number'] = ''
                if 'INV_Model' in i.keys():
                    INV_Model = i['INV_Model']
                    Check_dic_Gantt['INV_Model'] = INV_Model
                else:
                    Check_dic_Gantt['INV_Model'] = ''
                if 'Project_Name' in i.keys():
                    Project_Name = i['Project_Name']
                    Check_dic_Gantt['Project_Name'] = Project_Name
                else:
                    Check_dic_Gantt['Project_Name'] = ''
                if 'Unit_Origin' in i.keys():
                    Unit_Origin = i['Unit_Origin']
                    Check_dic_Gantt['Unit_Origin'] = Unit_Origin
                else:
                    Check_dic_Gantt['Unit_Origin'] = ''
                if 'Qualify_Cycles' in i.keys():
                    Qualify_Cycles = i['Qualify_Cycles']
                    Check_dic_Gantt['Qualify_Cycles'] = Qualify_Cycles
                else:
                    Check_dic_Gantt['Qualify_Cycles'] = ''
                # if 'Status' in i.keys():
                #     Statuss = i['Status']
                #     Check_dic_Gantt['Status'] = Statuss
                # else:
                #     Check_dic_Gantt['Status'] = ''
                if 'TP_Cat' in i.keys():
                    TP_Cat = i['TP_Cat']
                    Check_dic_Gantt['TP_Cat'] = TP_Cat
                else:
                    Check_dic_Gantt['TP_Cat'] = ''
                if 'Trial_Run_Type' in i.keys():
                    Trial_Run_Type = i['Trial_Run_Type']
                    Check_dic_Gantt['Trial_Run_Type'] = Trial_Run_Type
                else:
                    Check_dic_Gantt['Trial_Run_Type'] = ''
                if 'TP_Vendor' in i.keys():
                    TP_Vendor = i['TP_Vendor']
                    Check_dic_Gantt['TP_Vendor'] = TP_Vendor
                else:
                    Check_dic_Gantt['TP_Vendor'] = ''
                if 'TP_Key_Parameter' in i.keys():
                    TP_Key_Parameter = i['TP_Key_Parameter']
                    Check_dic_Gantt['TP_Key_Parameter'] = TP_Key_Parameter
                else:
                    Check_dic_Gantt['TP_Key_Parameter'] = ''
                if 'Lenovo_TP_PN' in i.keys():
                    Lenovo_TP_PN = i['Lenovo_TP_PN']
                    Check_dic_Gantt['Lenovo_TP_PN'] = Lenovo_TP_PN
                else:
                    Check_dic_Gantt['Lenovo_TP_PN'] = ''
                if 'Compal_TP_PN' in i.keys():
                    Compal_TP_PN = i['Compal_TP_PN']
                    Check_dic_Gantt['Compal_TP_PN'] = Compal_TP_PN
                else:
                    Check_dic_Gantt['Compal_TP_PN'] = ''
                if 'Test_Start' in i.keys():
                    Test_Start = i['Test_Start']
                    Check_dic_Gantt['Test_Start'] = Test_Start
                else:
                    Check_dic_Gantt['Test_Start'] = None#日期格式为空NULL不能用空字符
                if 'Test_End' in i.keys():
                    Test_End = i['Test_End']
                    Check_dic_Gantt['Test_End'] = Test_End
                else:
                    Check_dic_Gantt['Test_End'] = None

                if INVGantt.objects.filter(**Check_dic_Gantt).first():
                    # err_ok = 1
                    INVGanttList.append(Check_dic_Gantt)
                    Update_dic_Gantt = {}
                    for j in i.keys():
                        Update_dic_Gantt[j] = i[j]
                    Update_dic_Gantt['Editor'] = request.session.get('user_name')
                    Update_dic_Gantt['Edittime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # print(Update_dic_Gantt)
                    if INVGantt.objects.filter(**Check_dic_Gantt):
                        INVGantt.objects.filter(**Check_dic_Gantt).update(**Update_dic_Gantt)
                else:
                    Create_dic_Gantt = {}
                    for j in i.keys():
                        Create_dic_Gantt[j] = i[j]
                    Create_dic_Gantt['Editor'] = request.session.get('user_name')
                    Create_dic_Gantt['Edittime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # print(Create_dic_Gantt)
                    INVGantt.objects.create(**Create_dic_Gantt)
            # print(INVGanttList)
            datajason = {
                'err_ok': err_ok,
                "canEdit": 1,#用的xlsx_pop.js如果不反悔caneEdit,不会出现山川成功弹框和重复数据的弹框
                # 'content': INVGanttList
            }
            # print(datajason)

            return HttpResponse(json.dumps(datajason), content_type="application/json")
    return render(request, 'INVGantt/INVGantt_upload.html', locals())

@csrf_exempt
def INVGantt_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="INVGantt/INVGantt_search"
    selectItem = {
        # "C38(NB)": [{"Project": "EL531", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL532", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL533", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]},
        #             {"Project": "EL534", "CompalPN": ["LTCX0093GB0", "LTCX0093HB0", "LTCX0093IB0", "LTCX0094RB0"]}],
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
    selectCategory = [
        # "adapter", "Battery", "Finger Print"
    ]

    selectStatus = [
        # "Pass", "Fail", "Testing"
    ]

    selectLenovo_TP_PN = [
        # "SSA1B09974", "SSA1B09975", "SM30N76643"
    ]

    selectCompal_TP_PN = [
        # "DD900017P50", "SKM1A25395", "PK05400A800"
    ]
    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "INV_Number": "TBD", "INV_Model": "FLY00", "Project_Name": "FLY00",
        #           "Year": "2020", "Unit_Qty": "24", "TP_Kinds": "1", "Qualify_Cycles": "", "Status": "Planning",
        #           "TP_Cat": "CPU", "Trial_Run_Type": "New Source","TP_Vendor": "Intel",
        #           "TP_Key_Parameter": "I7-10870H 2.2G/8C/16M Match to G1B,G1R,G2R,G3R VGA", "Lenovo_TP_PN": "SSA1B09975",
        #           "Compal_TP_PN": "","Issue_Link": "", "Remark": "", "Attend_Time": "1", "Get_INV": "",
        #           "Month": "","Test_Start":"","Test_End":""},
        ]
    for i in INVGantt.objects.all().values('Customer').distinct().order_by('Customer'):
        # print(i)
        Project = []
        for j in INVGantt.objects.filter(Customer=i['Customer']).values('INV_Model').distinct().order_by('INV_Model'):
            # CompalPNlist=[]
            # for k in CQM.objects.filter(Customer=i['Customer'],Project=j['Project']).values('CompalPN').distinct().order_by('CompalPN'):
            #     CompalPNlist.append(k['CompalPN'])
            Project.append({"Project": j['INV_Model'],})#"CompalPN":CompalPNlist})
        selectItem[i['Customer']] = Project
    for i in INVGantt.objects.all().values('TP_Cat').distinct().order_by('TP_Cat'):
        selectCategory.append(i['TP_Cat'])
    for i in INVGantt.objects.all().values('Status').distinct().order_by('Status'):
        selectStatus.append(i['Status'])
    for i in INVGantt.objects.all().values('Lenovo_TP_PN').distinct().order_by('Lenovo_TP_PN'):
        selectLenovo_TP_PN.append(i['Lenovo_TP_PN'])
    for i in INVGantt.objects.all().values('Compal_TP_PN').distinct().order_by('Compal_TP_PN'):
        selectCompal_TP_PN.append(i['Compal_TP_PN'])
    if request.method == 'POST':
        # print(request,type(request),request.POST)
        if request.POST.get('isGetData') == 'SEARCH':
            check_dic = {}
            if request.POST.get('Customer'):
                check_dic['Customer'] = request.POST.get('Customer')
            if request.POST.get('Project'):
                check_dic['INV_Model'] = request.POST.get('Project')
            if request.POST.get('Category'):
                check_dic['TP_Cat'] = request.POST.get('Category')
            if request.POST.get('Status'):
                check_dic['Status'] = request.POST.get('Status')
            if request.POST.get('Lenovo_TP_PN'):
                check_dic['Lenovo_TP_PN'] = request.POST.get('Lenovo_TP_PN')
            if request.POST.get('Compal_TP_PN'):
                check_dic['Compal_TP_PN'] = request.POST.get('Compal_TP_PN')
            for i in INVGantt.objects.filter(**check_dic):
                # print(i.Test_Start, str(i.Test_End), str(i.Edittime))
                mock_data.append({"id":i.id, "Customer": i.Customer, 'INV_Number':i.INV_Number, "INV_Model":i.INV_Model, "Project_Name":i.Project_Name, "Unit_Origin":i.Unit_Origin, "Year":i.Year,
                                  "Unit_Qty":i.Unit_Qty, "TP_Kinds":i.TP_Kinds, "Qualify_Cycles":i.Qualify_Cycles, "Status":i.Status,
                                  "TP_Cat":i.TP_Cat, "Trial_Run_Type":i.Trial_Run_Type, "TP_Vendor":i.TP_Vendor, "TP_Key_Parameter":i.TP_Key_Parameter,
                                  "Lenovo_TP_PN":i.Lenovo_TP_PN,"Compal_TP_PN":i.Compal_TP_PN, "Issue_Link":i.Issue_Link,
                                  "Remark":i.Remark, "Attend_Time":i.Attend_Time, "Get_INV":i.Get_INV, "Month":i.Month,
                                  "Test_Start":str(i.Test_Start), "Test_End":str(i.Test_End),
                                  "Editor":i.Editor, "Edittime":str(i.Edittime), })
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,

            "selectStatus": selectStatus,
            # "selectCompal_R3_PN":selectCompal_R3_PN,
            "selectCategory": selectCategory,
            "selectLenovo_TP_PN": selectLenovo_TP_PN,
            "selectCompal_TP_PN": selectCompal_TP_PN
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'INVGantt/INVGantt_search.html', locals())

@csrf_exempt
def INVGantt_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="INVGantt/INVGantt_edit"
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
    mock_data = [
        # {"id": "1", "Customer": "C38(NB)", "INV_Number": "TBD", "INV_Model": "FLY00", "Project_Name": "FLY00",
        #           "Year": "2020", "Unit_Qty": "24", "TP_Kinds": "1", "Qualify_Cycles": "", "Status": "Planning",
        #           "TP_Cat": "CPU", "Trial_Run_Type": "New Source","TP_Vendor": "Intel",
        #           "TP_Key_Parameter": "I7-10870H 2.2G/8C/16M Match to G1B,G1R,G2R,G3R VGA", "Lenovo_TP_PN": "SSA1B09975",
        #           "Compal_TP_PN": "","Issue_Link": "", "Remark": "", "Attend_Time": "1", "Get_INV": "",
        #           "Month": "","Test_Start":"","Test_End":""},
        ]
    aa = {"flag": 0}  # 弹窗1为此提案数据被编辑
    cc = {"statu": 4}  # 角色权限
    for i in INVGantt.objects.all().values('Customer').distinct().order_by('Customer'):
        # # print(i)
        # Project = []
        # for j in CQMProject.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
        #     Project.append({"Project": j['Project']})
        selectItem.append(i['Customer'])
    # print(selectItem)
    roles = []
    onlineuser = request.session.get('account')
    if request.method == 'POST':
        if request.POST.get('isGetData') == "SEARCHALERT":
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in INVGantt.objects.filter(Customer=Customer).values("INV_Model").distinct().order_by(
                        "INV_Model"):
                    Prolist.append(i["INV_Model"])
            else:
                for i in INVGantt.objects.all().values("INV_Model").distinct().order_by("INV_Model"):
                    Prolist.append(i["INV_Model"])
            # print(Prolist)
            for i in Prolist:
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
                    searchalert.append({
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Year, "COMPRJCODE": i,
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().VGA,
                        "OS SUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().OSSupport,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().LD,
                        "DQA PL": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPL,
                    })
                else:
                    # print(len(i))
                    if len(i) > 5:
                        # print(i['Project'],i['Project'][0:5],i['Project'][0:3],i['Project'][5:])
                        Prostr1 = i[0:5]
                        Prostr2 = i[0:3] + i[5:]
                        Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                        Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                        if Proinfo1 and Proinfo2:
                            if Proinfo1.Year == Proinfo2.Year:
                                Year = Proinfo1.Year
                            else:
                                Year = Proinfo1.Year + "/" + Proinfo2.Year
                            if Proinfo1.CusPrjCode == Proinfo2.CusPrjCode:
                                CusPrjCode = Proinfo1.CusPrjCode
                            else:
                                CusPrjCode = Proinfo1.CusPrjCode + "/" + Proinfo2.CusPrjCode
                            if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                ProjectName = Proinfo1.ProjectName
                            else:
                                ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                            if Proinfo1.Size == Proinfo2.Size:
                                Size = Proinfo1.Size
                            else:
                                Size = Proinfo1.Size + "/" + Proinfo2.Size
                            if Proinfo1.CPU == Proinfo2.CPU:
                                CPU = Proinfo1.CPU
                            else:
                                CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                            if Proinfo1.Platform == Proinfo2.Platform:
                                Platform = Proinfo1.Platform
                            else:
                                Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                            if Proinfo1.VGA == Proinfo2.VGA:
                                VGA = Proinfo1.VGA
                            else:
                                VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                            if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                OSSupport = Proinfo1.OSSupport
                            else:
                                OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                            if Proinfo1.SS == Proinfo2.SS:
                                SS = Proinfo1.SS
                            else:
                                SS = Proinfo1.SS + "/" + Proinfo2.SS
                            if Proinfo1.LD == Proinfo2.LD:
                                LD = Proinfo1.LD
                            else:
                                LD = Proinfo1.LD + "/" + Proinfo2.LD
                            if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                DQAPL = Proinfo1.DQAPL
                            else:
                                DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                            searchalert.append({
                                "id": Proinfo1.id,
                                "YEAR": Year,
                                "COMPRJCODE": i,
                                "CUSPRJCODE": CusPrjCode,
                                "PROJECT": ProjectName,
                                "SIZE": Size,
                                "CPU": CPU,
                                "PLATFORM": Platform,
                                "VGA": VGA,
                                "OSSUPPORT": OSSupport,
                                "SS": SS,
                                "LD": LD,
                                "DQAPL": DQAPL,
                            })
                        else:
                            searchalert.append({
                                "id": "",
                                "YEAR": "", "COMPRJCODE": i,
                                "CUSPRJCODE": "",
                                "ProjectName": "",
                                "SIZE": "",
                                "CPU": "",
                                "PLATFORM": "",
                                "VGA": "",
                                "OSSUPPORT": "",
                                "SS": "",
                                "LD": "",
                                "DQAPL": "",
                            })
                    else:
                        searchalert.append({
                            "YEAR": "", "COMPRJCODE": i,
                            "CUSPRJCODE": "",
                            "ProjectName": "",
                            "SIZE": "",
                            "CPU": "",
                            "PLATFORM": "",
                            "VGA": "",
                            "OS SUPPORT": "",
                            "SS": "",
                            "LD": "",
                            "DQA PL": "",
                        })
            # print(sear)
        if request.POST.get('isGetData') == 'SEARCH':
            Check_dic_Project = {'Customer': request.POST.get('Customer'), 'INV_Model': request.POST.get('COMPRJCODE'),}

            Customer=request.POST.get('Customer')
            INV_Model=request.POST.get('COMPRJCODE')
            check_dic = {}
            #Customer,Project不能为空，最好前端加判断
            if Customer:
                check_dic['Customer'] = Customer
            if INV_Model:
                check_dic['INV_Model'] = INV_Model

            # print(check_dic)
            for i in INVGantt.objects.filter(**check_dic):
                # print(i.Test_Start, str(i.Test_End), str(i.Edittime))
                mock_data.append({"id":i.id, "Customer": i.Customer, 'INV_Number':i.INV_Number, "INV_Model":i.INV_Model, "Project_Name":i.Project_Name, "Unit_Origin":i.Unit_Origin,
                                  "Year":i.Year,"Unit_Qty":i.Unit_Qty, "TP_Kinds":i.TP_Kinds, "Qualify_Cycles":i.Qualify_Cycles, "Status":i.Status,
                                  "TP_Cat":i.TP_Cat, "Trial_Run_Type":i.Trial_Run_Type, "TP_Vendor":i.TP_Vendor, "TP_Key_Parameter":i.TP_Key_Parameter,
                                  "Lenovo_TP_PN":i.Lenovo_TP_PN,"Compal_TP_PN":i.Compal_TP_PN, "Issue_Link":i.Issue_Link,
                                  "Remark":i.Remark, "Attend_Time":i.Attend_Time, "Get_INV":i.Get_INV, "Month":i.Month,
                                  "Test_Start":str(i.Test_Start), "Test_End":str(i.Test_End),
                                  "Editor":i.Editor, "Edittime":str(i.Edittime), })
            # print(mock_data)
        if 'SAVE' in str(request.body):
            resdatas=json.loads(request.body)
            # print(resdatas)
            resdata = resdatas['rows']
            Customer = resdatas['Customer']
            INV_Model = resdatas['Project']
            # print (resdata)
            # print(resdata['Comments'])

            Update_dic_Gantt = {}
            for j in resdata.keys():#前提是前端的关键字和数据库的一样
                Update_dic_Gantt[j] = resdata[j]
            Update_dic_Gantt['Editor'] = request.session.get('user_name')
            Update_dic_Gantt['Edittime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(Update_dic_Gantt)
            INVGantt.objects.filter(id=resdata['id']).update(**Update_dic_Gantt)
            check_dic = {}
            if Customer:
                check_dic['Customer'] = Customer
            if INV_Model:
                check_dic['INV_Model'] = INV_Model

            for i in INVGantt.objects.filter(**check_dic):
                mock_data.append(
                    {"id": i.id, "Customer": i.Customer, 'INV_Number': i.INV_Number, "INV_Model": i.INV_Model,
                     "Project_Name": i.Project_Name, "Unit_Origin": i.Unit_Origin, "Year": i.Year,
                     "Unit_Qty": i.Unit_Qty, "TP_Kinds": i.TP_Kinds, "Qualify_Cycles": i.Qualify_Cycles,
                     "Status": i.Status,
                     "TP_Cat": i.TP_Cat, "Trial_Run_Type": i.Trial_Run_Type, "TP_Vendor": i.TP_Vendor,
                     "TP_Key_Parameter": i.TP_Key_Parameter,
                     "Lenovo_TP_PN": i.Lenovo_TP_PN, "Compal_TP_PN": i.Compal_TP_PN, "Issue_Link": i.Issue_Link,
                     "Remark": i.Remark, "Attend_Time": i.Attend_Time, "Get_INV": i.Get_INV, "Month": i.Month,
                     "Test_Start": str(i.Test_Start), "Test_End": str(i.Test_End),
                     "Editor": i.Editor, "Edittime": str(i.Edittime), })
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            # "canEdit": canEdit,
            "orr": cc,
            "orn": aa,
            # "history": history,
            "sear": searchalert,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'INVGantt/INVGantt_edit.html', locals())

@csrf_exempt
def INVGantt_summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="INVGantt/INVGantt_summary"

    mock_data = [

    ]

    mock_data1 = [
        # {"Customer": "A39", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "0",
        #  "Total": "0"},
        # {"Customer": "C38N", "Pass": "111", "Fail": "13", "Ongoing": "6", "Planning": "56",
        #  "Total": "186"},
        # {"Customer": "C38A", "Pass": "93", "Fail": "18", "Ongoing": "10", "Planning": "14",
        #  "Total": "135"},
        # # {"Customer": "A39", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "0",
        # #  "Total": "0"},
    ]

    mock_data2 = [
        # {"Month": "Jan", "A39": "0", "C38N": "16", "C38A": "10", "Total": "26"},
        # {"Month": "Feb", "A39": "6", "C38N": "6", "C38A": "4", "Total": "10"},
        # {"Month": "Mar", "A39": "32", "C38N": "32", "C38A": "20", "Total": "52"},
        # {"Month": "Apr", "A39": "28", "C38N": "28", "C38A": "23", "Total": "51"},
        # {"Month": "May", "A39": "29", "C38N": "29", "C38A": "23", "Total": "42"},
        # {"Month": "Jun", "A39": "19", "C38N": "19", "C38A": "13", "Total": "64"}
    ]

    mock_data3 = [
        # {"Project": "DLMVA", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "ELMV2", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "ELIC1", "Pass": "13", "Fail": "1", "Ongoing": "0", "Planning": "2", "Total": "16"},
        # {"Project": "ELAV4V5", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "2", "Total": "3"},
        # {"Project": "ELMEA", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "1", "Total": "1"},
        # {"Project": "EL531", "Pass": "3", "Fail": "1", "Ongoing": "1", "Planning": "0", "Total": "5"},
        # {"Project": "EL4C2", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "EL452", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "EL432532", "Pass": "13", "Fail": "1", "Ongoing": "0", "Planning": "2", "Total": "16"},
        # {"Project": "FLPR5R7", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "2", "Total": "3"},
        # {"Project": "FLZ04", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "1", "Total": "1"},
        # {"Project": "EL4C4", "Pass": "3", "Fail": "1", "Ongoing": "1", "Planning": "0", "Total": "5"}
    ]

    mock_data4 = [
        # {"KeyPart": "CPU", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"KeyPart": "HDD", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"KeyPart": "SSHD", "Pass": "13", "Fail": "1", "Ongoing": "0", "Planning": "2", "Total": "16"},
        # {"KeyPart": "SSD", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "2", "Total": "3"},
        # {"KeyPart": "ODD", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "1", "Total": "1"},
        # {"KeyPart": "RAM", "Pass": "3", "Fail": "1", "Ongoing": "1", "Planning": "0", "Total": "5"},
    ]

    mock_data5 = [
        # {"Project": "CIZS1S2", "Jan": "1", "Feb": "0", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
        # {"Project": "DTZS1S2", "Jan": "1", "Feb": "0", "Mar": "0", "Apr": "0", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
        # {"Project": "DLMV2", "Jan": "13", "Feb": "1", "Mar": "0", "Apr": "2", "May": "16", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
        # {"Project": "DLME1", "Jan": "1", "Feb": "0", "Mar": "0", "Apr": "2", "May": "3", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
        # {"Project": "DLAE1", "Jan": "0", "Feb": "0", "Mar": "0", "Apr": "1", "May": "1", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
        # {"Project": "DLMV3", "Jan": "3", "Feb": "1", "Mar": "1", "Apr": "0", "May": "5", "Jun": "1", "Jul": "0", "Aug": "0", "Sep": "0", "Oct": "1", "Nov": "0", "Dec": "0", "By_Project_Total_Qty": "1"},
    ]

    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]

    INV_data = {
                # "Customer_key": ['C38A', 'C38N', 'A39'],#search1
                # "Month_key": ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],#search2
                # "INV_Project_key": ['DLMVA', 'ELMV2', 'ELIC1', 'ELAV4V5', 'ELMEA', 'EL531', 'EL4C2',
                #                     'EL452', 'EL432532', 'FLPR5R7', 'FLZ04', 'EL4C4', 'DLMVA', 'ELMV2', 'ELIC1', 'ELAV4V5', 'ELMEA', 'EL531', 'EL4C2',
                #                     'EL452', 'EL432532', 'FLPR5R7', 'FLZ04', 'EL4C4'],#search3

                # "Category_key": ['CPU', 'SSHD', 'ODD', 'Panel', 'Battery', 'Keyboard']#search4
                }
    INV_Customer = [
        # {
        #     "name": "Pass",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth":50,
        #     "data": [120,130,140]#对应机种顺序
        # },
        # {
        #     "name": "Fail",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125]  # 对应机种顺序
        # },
        # {
        #     "name": "Ongoing",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100]  # 对应机种顺序
        # },
        # {
        #     "name": "Planning",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [88, 0, 38]  # 对应机种顺序
        # },
    ]#search1

    INV_Month = [
        # {
        #     "name": "C38A",
        #     "type": "bar",
        #     "stack": "month",
        #     "barMaxWidth":50,
        #     "data": [120, 30, 140, 34, 56, 67, 120, 30, 140, 34, 56, 67]#对应机种顺序
        # },
        # {
        #     "name": "C38N",
        #     "type": "bar",
        #     "stack": "month",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 88, 99, 23, 100, 110, 125, 88, 99, 23]  # 对应机种顺序
        # },
        # {
        #     "name": "A39",
        #     "type": "bar",
        #     "stack": "month",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100, 23, 0, 56, 56, 67, 100, 23, 0, 56]  # 对应机种顺序
        # }
    ]#search2

    INV_Project = [
        # {
        #     "name": "Pass",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth":50,
        #     "data": [120, 130, 140, 45, 56, 23, 120, 130, 140, 45, 56, 23]#对应机种顺序
        # },
        # {
        #     "name": "Fail",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 101, 23, 0, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
        # {
        #     "name": "Ongoing",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100, 12, 44, 55, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
        # {
        #     "name": "Planning",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [88, 0, 38, 33, 12, 90, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
    ]#search3

    AIO_Project = [
        # {
        #     "name": "Pass",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth":50,
        #     "data": [120, 130, 140, 45, 56, 23, 120, 130, 140, 45, 56, 23]#对应机种顺序
        # },
        # {
        #     "name": "Fail",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 101, 23, 0, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
        # {
        #     "name": "Ongoing",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100, 12, 44, 55, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
        # {
        #     "name": "Planning",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [88, 0, 38, 33, 12, 90, 120, 130, 140, 45, 56, 23]  # 对应机种顺序
        # },
    ]

    INV_Category = [
        # {
        #     "name": "Pass",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth":50,
        #     "data": [120, 130, 140, 45, 56, 23]#对应机种顺序
        # },
        # {
        #     "name": "Fail",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 101, 23, 0]  # 对应机种顺序
        # },
        # {
        #     "name": "Ongoing",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100, 12, 44, 55]  # 对应机种顺序
        # },
        # {
        #     "name": "Planning",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [88, 0, 38, 33, 12, 90]  # 对应机种顺序
        # },
    ]#search4

    for i in INVGantt.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])

    if request.method == 'POST':
        if request.POST.get("isGetData") == "first":
            Year = str(datetime.datetime.now().year)
            # print(Year)
            # Search1 default
            Customer_key = []
            Customerlist = INVGantt.objects.all().values("Customer").distinct().order_by("Customer")

            for i in Customerlist:
                Customer_key.append(i["Customer"])
            INV_data["Customer_key"] = Customer_key
            if Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                # print(Test_Endperiod)
                for i in Customerlist:
                    PassNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    #Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                    PlanningNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Planning").count()
                    mock_data1.append({"Customer": i["Customer"], "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                 Test_Start__range=Test_Endperiod).count()
                # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                # print(i["Customer"], PassNo)
                FailNo = INVGantt.objects.filter(Status="Fail", Test_Start__range=Test_Endperiod).count()
                OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                    Test_Start__range=Test_Endperiod).count()
                # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                PlanningNo = INVGantt.objects.filter(Status="Planning").count()
                mock_data1.append(
                    {"Customer": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                     "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in INV_data["Customer_key"]:
                    for k in mock_data1:
                        if k["Customer"] == j:
                            datalist.append(k[i])
                INV_Customer.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth":50,
                        "data": datalist#对应机种顺序
                    },
                )

            #Search2 default
            # Year = request.POST.get("Date")  # Search2里面Year不能为空，为空就没有数据
            Mounthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            if Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                for i in Mounthlist:
                    data2dict = {"Month": i}
                    for j in selectItem:
                        data2dict[j] = INVGantt.objects.filter(Customer=j, Month=i,
                                                               Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    data2dict["Total"] = INVGantt.objects.filter(Month=i,
                                                                                Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    mock_data2.append(data2dict)
                data2dict = {"Month": "Total"}
                for j in selectItem:
                    data2dict[j] = INVGantt.objects.filter(Customer=j, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                data2dict["Total"] = INVGantt.objects.filter(Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                mock_data2.append(data2dict)

                INV_data["Month_key"] = Mounthlist
                for i in selectItem:
                    datalist = []
                    for j in INV_data["Month_key"]:
                        for k in mock_data2:
                            if k["Month"] == j:
                                datalist.append(k[i])
                    INV_Month.append({
                        "name": i,
                        "type": "bar",
                        "stack": "month",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    })

            # Search3 default
            Customer = "C38(NB)"
            # Year = request.POST.get("Date")
            if Customer:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    Projectlist = []
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                    for i in Projectlist:
                        PassNo = INVGantt.objects.filter(Project_Name=i,
                                                         Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail",
                                                         Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(Project_Name=i, Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                        PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning").count()
                        mock_data3.append(
                            {"Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                             "Planning": PlanningNo,
                             "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                    PlanningNo = INVGantt.objects.filter(Customer=Customer, Status="Planning").count()
                    mock_data3.append({"Project": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                INV_data["INV_Project_key"] = Projectlist
                for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                    datalist = []
                    for j in INV_data["INV_Project_key"]:
                        for k in mock_data3:
                            if k["Project"] == j:
                                datalist.append(k[i])
                    INV_Project.append(
                        {
                            "name": i,
                            "type": "bar",
                            "stack": "status",
                            "barMaxWidth": 50,
                            "data": datalist  # 对应机种顺序
                        },
                    )

            # Search4 default
            # Year = request.POST.get("Date")
            if Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                KeyparList = []
                for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values("TP_Cat").distinct().order_by(
                        "TP_Cat"):
                    KeyparList.append(i["TP_Cat"])
                for i in KeyparList:
                    PassNo = INVGantt.objects.filter(TP_Cat=i,
                                                     Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                    PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning").count()
                    mock_data4.append(
                        {"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                         "Planning": PlanningNo,
                         "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                 Test_Start__range=Test_Endperiod).count()
                # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                # print(i["Customer"], PassNo)
                FailNo = INVGantt.objects.filter(Status="Fail",
                                                 Test_Start__range=Test_Endperiod).count()
                OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                    Test_Start__range=Test_Endperiod).count()
                # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                PlanningNo = INVGantt.objects.filter(Status="Planning").count()
                mock_data4.append({"KeyPart": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                   "Planning": PlanningNo,
                                   "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            INV_data["Category_key"] = KeyparList
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in INV_data["Category_key"]:
                    for k in mock_data4:
                        if k["KeyPart"] == j:
                            datalist.append(k[i])
                INV_Category.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )

            # Search5 default
            Customer = "C38(NB)"
            # Year = request.POST.get("Date")
            if Customer and Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                Projectlist = []
                for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                        "Project_Name").distinct().order_by("Project_Name"):
                    Projectlist.append(i["Project_Name"])
                Mounthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for i in Projectlist:
                    data5dict = {"Project": i}
                    for j in Mounthlist:
                        data5dict[j] = INVGantt.objects.filter(Customer=Customer, Project_Name=i, Month=j,
                                                               Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    # 要除去Planning的，因为Planing的月份为空
                    data5dict["By_Project_Total_Qty"] = INVGantt.objects.filter(Customer=Customer, Project_Name=i,
                                                                                Test_Start__range=Test_Endperiod).exclude(
                        Status="Planning").count()
                    mock_data5.append(data5dict)
                data5dict = {"Project": "By month total Qty"}
                for j in Mounthlist:
                    data5dict[j] = INVGantt.objects.filter(Customer=Customer, Month=j, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                # 要除去Planning的，因为Planing的月份为空
                data5dict["By_Project_Total_Qty"] = INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).exclude(
                    Status="Planning").count()
                mock_data5.append(data5dict)

        if request.POST.get("isGetData") == "SEARCH1":
            Year = request.POST.get("Date")
            Customer_key = []
            Customerlist = INVGantt.objects.all().values("Customer").distinct().order_by("Customer")

            for i in Customerlist:
                Customer_key.append(i["Customer"])
            INV_data["Customer_key"] = Customer_key
            if Year:
                if Year == str(datetime.datetime.now().year):#如果时当年，算上没有schedule的Planning
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    # print(Test_Endperiod)
                    for i in Customerlist:
                        PassNo = INVGantt.objects.filter(Customer=i["Customer"],
                                                         Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Fail",
                                                         Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                        PlanningNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Planning").count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status="Planning").count())
                        mock_data1.append(
                            {"Customer": i["Customer"], "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                             "Planning": PlanningNo,
                             "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Status="Fail", Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                    PlanningNo = INVGantt.objects.filter(Status="Planning").count()
                    mock_data1.append({"Customer": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                else:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    # print(Test_Endperiod)
                    for i in Customerlist:
                        PassNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Fail", Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Testing", 'Pending'], Test_Start__range=Test_Endperiod).count()
                        PlanningNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Planning", Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status="Planning").count())
                        mock_data1.append({"Customer": i["Customer"], "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Status="Fail", Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'], Test_Start__range=Test_Endperiod).count()
                    PlanningNo = INVGantt.objects.filter(Status="Planning", Test_Start__range=Test_Endperiod).count()
                    mock_data1.append({"Customer": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            else:
                for i in Customerlist:
                    PassNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass']).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Fail").count()
                    OngoingNo = INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Testing", 'Pending'],).count()
                    PlanningNo = INVGantt.objects.filter(Customer=i["Customer"], Status="Planning").count()
                    mock_data1.append({"Customer": i["Customer"], "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                                   "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass']).count()
                # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                # print(i["Customer"], PassNo)
                FailNo = INVGantt.objects.filter(Status="Fail").count()
                OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'], ).count()
                PlanningNo = INVGantt.objects.filter(Status="Planning").count()
                mock_data1.append({"Customer": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                   "Planning": PlanningNo,
                                   "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in INV_data["Customer_key"]:
                    for k in mock_data1:
                        if k["Customer"] == j:
                            datalist.append(k[i])
                INV_Customer.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth":50,
                        "data": datalist#对应机种顺序
                    },
                )
        if request.POST.get("isGetData") == "SEARCH2":
            Year = request.POST.get("Date")#Search2里面Year不能为空，为空就没有数据
            Mounthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            if Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                for i in Mounthlist:
                    data2dict = {"Month": i}
                    for j in selectItem:
                        data2dict[j] = INVGantt.objects.filter(Customer=j, Month=i, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                        # print(data2dict,"1")
                    data2dict["Total"] = INVGantt.objects.filter(Month=i, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    # print(data2dict,"2")
                    mock_data2.append(data2dict)
                data2dict = {"Month": "Total"}
                for j in selectItem:
                    data2dict[j] = INVGantt.objects.filter(Customer=j, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                data2dict["Total"] = INVGantt.objects.filter(Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                # print(data2dict,"3")
                mock_data2.append(data2dict)

                INV_data["Month_key"] = Mounthlist
                for i in selectItem:
                    datalist = []
                    for j in INV_data["Month_key"]:
                        for k in mock_data2:
                            if k["Month"] == j:
                                datalist.append(k[i])
                    INV_Month.append({
                            "name": i,
                            "type": "bar",
                            "stack": "month",
                            "barMaxWidth":50,
                            "data": datalist#对应机种顺序
                        })
        if request.POST.get("isGetData") == "SEARCH3":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Date")
            if Customer:
                if Year:
                    if Year == str(datetime.datetime.now().year):  # 如果时当年，算上没有schedule的Planning
                        Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                        Projectlist = []
                        for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                                "Project_Name").distinct().order_by("Project_Name"):
                            Projectlist.append(i["Project_Name"])
                        for i in Projectlist:
                            PassNo = INVGantt.objects.filter(Project_Name=i,
                                                             Status__in=["Pass", 'Conditional Pass'],
                                                             Test_Start__range=Test_Endperiod).count()
                            # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                            # print(i["Customer"], PassNo)
                            FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail",
                                                             Test_Start__range=Test_Endperiod).count()
                            OngoingNo = INVGantt.objects.filter(Project_Name=i, Status__in=["Testing", 'Pending'],
                                                                Test_Start__range=Test_Endperiod).count()
                            # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                            PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning").count()
                            mock_data3.append(
                                {"Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                 "Planning": PlanningNo,
                                 "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                        PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail",
                                                         Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                        PlanningNo = INVGantt.objects.filter(Customer=Customer, Status="Planning").count()
                        mock_data3.append({"Project": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Planning": PlanningNo,
                                           "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    else:
                        Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                        Projectlist = []
                        for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                                "Project_Name").distinct().order_by("Project_Name"):
                            Projectlist.append(i["Project_Name"])
                        for i in Projectlist:
                            PassNo = INVGantt.objects.filter(Project_Name=i,
                                                             Status__in=["Pass", 'Conditional Pass'],
                                                             Test_Start__range=Test_Endperiod).count()
                            # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                            # print(i["Customer"], PassNo)
                            FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail",
                                                             Test_Start__range=Test_Endperiod).count()
                            OngoingNo = INVGantt.objects.filter(Project_Name=i, Status__in=["Testing", 'Pending'],
                                                                Test_Start__range=Test_Endperiod).count()
                            PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning",
                                                                 Test_Start__range=Test_Endperiod).count()
                            mock_data3.append(
                                {"Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                 "Planning": PlanningNo,
                                 "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                        PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail", Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        PlanningNo = INVGantt.objects.filter(Customer=Customer, Status="Planning", Test_Start__range=Test_Endperiod).count()
                        mock_data3.append({"Project": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Planning": PlanningNo,
                                           "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                else:
                    Projectlist = []
                    for i in INVGantt.objects.filter(Customer=Customer).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                    for i in Projectlist:
                        PassNo = INVGantt.objects.filter(Project_Name=i,
                                                         Status__in=["Pass", 'Conditional Pass'],
                                                         ).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail",
                                                         ).count()
                        OngoingNo = INVGantt.objects.filter(Project_Name=i, Status__in=["Testing", 'Pending'],
                                                            ).count()
                        PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning",
                                                             ).count()
                        mock_data3.append(
                            {"Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                             "Planning": PlanningNo,
                             "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'],
                                                     ).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail", ).count()
                    OngoingNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Testing", 'Pending'],
                                                        ).count()
                    PlanningNo = INVGantt.objects.filter(Customer=Customer, Status="Planning", ).count()
                    mock_data3.append({"Project": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                INV_data["INV_Project_key"] = Projectlist
                for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                    datalist = []
                    for j in INV_data["INV_Project_key"]:
                        for k in mock_data3:
                            if k["Project"] == j:
                                datalist.append(k[i])
                    INV_Project.append(
                        {
                            "name": i,
                            "type": "bar",
                            "stack": "status",
                            "barMaxWidth": 50,
                            "data": datalist  # 对应机种顺序
                        },
                    )
        if request.POST.get("isGetData") == "SEARCH4":
            Year = request.POST.get("Date")
            if Year:
                if Year == str(datetime.datetime.now().year):  # 如果时当年，算上没有schedule的Planning
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    KeyparList = []
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values(
                            "TP_Cat").distinct().order_by("TP_Cat"):
                        KeyparList.append(i["TP_Cat"])
                    for i in KeyparList:
                        PassNo = INVGantt.objects.filter(TP_Cat=i,
                                                         Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail",
                                                         Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                        PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning").count()
                        mock_data4.append(
                            {"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                             "Planning": PlanningNo,
                             "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    # Planning状态的没有schedule日期，不能把Test_Start__range作为搜索条件，需要加到当年的里面去
                    PlanningNo = INVGantt.objects.filter(Status="Planning").count()
                    mock_data4.append({"KeyPart": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                else:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    KeyparList = []
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values("TP_Cat").distinct().order_by("TP_Cat"):
                        KeyparList.append(i["TP_Cat"])
                    for i in KeyparList:
                        PassNo = INVGantt.objects.filter(TP_Cat=i,
                                                         Status__in=["Pass", 'Conditional Pass'],
                                                         Test_Start__range=Test_Endperiod).count()
                        # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                        # print(i["Customer"], PassNo)
                        FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail",
                                                         Test_Start__range=Test_Endperiod).count()
                        OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending'],
                                                            Test_Start__range=Test_Endperiod).count()
                        PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning",
                                                             Test_Start__range=Test_Endperiod).count()
                        mock_data4.append(
                            {"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                             "Planning": PlanningNo,
                             "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                        Test_Start__range=Test_Endperiod).count()
                    PlanningNo = INVGantt.objects.filter(Status="Planning",
                                                         Test_Start__range=Test_Endperiod).count()
                    mock_data4.append({"KeyPart": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                       "Planning": PlanningNo,
                                       "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            else:
                KeyparList = []
                for i in INVGantt.objects.all().values("TP_Cat").distinct().order_by(
                        "TP_Cat"):
                    KeyparList.append(i["TP_Cat"])
                for i in KeyparList:
                    PassNo = INVGantt.objects.filter(TP_Cat=i,
                                                     Status__in=["Pass", 'Conditional Pass'],
                                                     ).count()
                    # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                    # print(i["Customer"], PassNo)
                    FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail",
                                                     ).count()
                    OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending'],
                                                        ).count()
                    PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning",
                                                         ).count()
                    mock_data4.append(
                        {"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                         "Planning": PlanningNo,
                         "Total": PassNo + FailNo + OngoingNo + PlanningNo})
                PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                 ).count()
                # print(INVGantt.objects.filter(Customer=i["Customer"], Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod))
                # print(i["Customer"], PassNo)
                FailNo = INVGantt.objects.filter(Status="Fail",
                                                 ).count()
                OngoingNo = INVGantt.objects.filter(Status__in=["Testing", 'Pending'],
                                                    ).count()
                PlanningNo = INVGantt.objects.filter(Status="Planning",
                                                     ).count()
                mock_data4.append({"KeyPart": "Total", "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                   "Planning": PlanningNo,
                                   "Total": PassNo + FailNo + OngoingNo + PlanningNo})
            INV_data["Category_key"] = KeyparList
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in INV_data["Category_key"]:
                    for k in mock_data4:
                        if k["KeyPart"] == j:
                            datalist.append(k[i])
                INV_Category.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )
        if request.POST.get("isGetData") == "SEARCH5":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Date")
            if Customer and Year:
                Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                Projectlist = []
                for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                        "Project_Name").distinct().order_by("Project_Name"):
                    Projectlist.append(i["Project_Name"])
                Mounthlist = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                for i in Projectlist:
                    data5dict = {"Project": i}
                    for j in Mounthlist:
                        data5dict[j] = INVGantt.objects.filter(Customer=Customer, Project_Name=i, Month=j, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    # 要除去Planning的，因为Planing的月份为空
                    data5dict["By_Project_Total_Qty"] = INVGantt.objects.filter(Customer=Customer, Project_Name=i, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                    mock_data5.append(data5dict)
                data5dict = {"Project": "By month total Qty"}
                for j in Mounthlist:
                    data5dict[j] = INVGantt.objects.filter(Customer=Customer, Month=j, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                # 要除去Planning的，因为Planing的月份为空
                data5dict["By_Project_Total_Qty"] = INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).exclude(Status="Planning").count()
                mock_data5.append(data5dict)



        data = {
            # "err_ok": "0",
            "select": selectItem,
            "content1": mock_data1,#search1
            "content2": mock_data2,#search2
            "content3": mock_data3,#search3
            "content4": mock_data4,#search4
            "content5": mock_data5,#search5
            'INV_data': INV_data,#search1,2,3,4,5
            "INV_Customer": INV_Customer,#search1
            "INV_Month": INV_Month,#search2
            "INV_Project": INV_Project,#search3
            # "AIO_Project": AIO_Project,
            "INV_Category": INV_Category,#search4

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'INVGantt/INVGantt_summary.html', locals())

@csrf_exempt
def INVGantt_top(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="INVGantt/INVGantt_top"

    mock_data1 = [
        # {"Project": "DLMVA", "Standard_test_time": "1", "Retest_time": "0", "Total_Attend_time": "0", "Total": "1"},
        # {"Project": "ELMV2", "Standard_test_time": "1", "Retest_time": "0", "Total_Attend_time": "0", "Total": "1"},
        # {"Project": "ELIC1", "Standard_test_time": "13", "Retest_time": "1", "Total_Attend_time": "0", "Total": "16"},
        # {"Project": "ELAV4V5", "Standard_test_time": "1", "Retest_time": "0", "Total_Attend_time": "0", "Total": "3"},
        # {"Project": "ELMEA", "Standard_test_time": "0", "Retest_time": "0", "Total_Attend_time": "0", "Total": "1"},
        # {"Project": "EL531", "Standard_test_time": "3", "Retest_time": "1", "Total_Attend_time": "1", "Total": "5"},
    ]

    mock_data2 = [
        # {"KeyPart": "SSD", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "RAM", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Panel", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "HDD", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "EE", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "ME", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Package", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Camera", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "VRAM", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "CPU", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
    ]

    mock_data3 = [
        # {"KeyPart": "SSD", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "RAM", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Panel", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "HDD", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "EE", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "ME", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Package", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "Camera", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "VRAM", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
        # {"KeyPart": "CPU", "Pass": "0", "Fail": "16", "Ongoing": "10", "Total": "26"},
    ]

    mock_data4 = [
        # {"Project": "DLMVA", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "ELMV2", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "ELIC1", "Pass": "13", "Fail": "1", "Ongoing": "0", "Planning": "2", "Total": "16"},
        # {"Project": "ELAV4V5", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "2", "Total": "3"},
        # {"Project": "ELMEA", "Pass": "0", "Fail": "0", "Ongoing": "0", "Planning": "1", "Total": "1"},
        # {"Project": "EL531", "Pass": "3", "Fail": "1", "Ongoing": "1", "Planning": "0", "Total": "5"},
        # {"Project": "EL4C2", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "EL452", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "0", "Total": "1"},
        # {"Project": "EL432532", "Pass": "13", "Fail": "1", "Ongoing": "0", "Planning": "2", "Total": "16"},
        # {"Project": "FLPR5R7", "Pass": "1", "Fail": "0", "Ongoing": "0", "Planning": "2", "Total": "3"},
    ]

    mock_data5 = [
        # {"Year": "Y2017", "PASS": "691", "FAIL": "94", "Total": "785", "Failure": "14%"},
        # {"Year": "Y2018", "PASS": "584", "FAIL": "96", "Total": "680", "Failure": "16%"},
        # {"Year": "Y2019", "PASS": "926", "FAIL": "173", "Total": "1099", "Failure": "19%"},
        # {"Year": "Y2020", "PASS": "204", "FAIL": "31", "Total": "245", "Failure": "15%"},
    ]

    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]

    Top10 = {
        # "Customer_key": ['DLMVA', 'ELMV2', 'ELIC1', 'ELAV4V5', 'ELMEA', 'EL531'],
        # "Keyparts_key": ['SSD', 'RAM', 'Panel', 'HDD', 'EE', 'ME', 'Package', 'Camera', 'VRAM', 'CPU']
        # "Failed_Keyparts_key": ['SSD', 'RAM', 'Panel', 'HDD', 'EE', 'ME', 'Package', 'Camera', 'VRAM', 'CPU'],
        # "Project_key": ['DLMVA', 'ELMV2', 'ELIC1', 'ELAV4V5', 'ELMEA', 'EL531', 'EL4C2', 'EL452', 'EL432532',
        #                 'FLPR5R7'],
        # "Quantity_key": ['Y2017', 'Y2018', 'Y2019', 'Y2020'],
    }
    Execution_Project = [
        # {
        #     "name": "Standard_test_time",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [120, 130, 140, 120, 130, 140]  # 对应机种顺序
        # },
        # {
        #     "name": "Retest_time",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 100, 110, 125]  # 对应机种顺序
        # },
    ]

    Keyparts = [

        # {"value": 335, "name": 'SSD'},
        # {"value": 310, "name": 'RAM'},
        # {"value": 234, "name": 'Panel'},
        # {"value": 135, "name": 'HDD'},
        # {"value": 1548, "name": 'EE'},
        # {"value": 335, "name": 'ME'},
        # {"value": 310, "name": 'Package'},
        # {"value": 234, "name": 'Camera'},
        # {"value": 135, "name": 'VRAM'},
        # {"value": 1548, "name": 'CPU'},

    ]

    Failed_Keyparts = [

        # {"value": 335, "name": 'SSD'},
        # {"value": 310, "name": 'RAM'},
        # {"value": 234, "name": 'Panel'},
        # {"value": 135, "name": 'HDD'},
        # {"value": 1548, "name": 'EE'},
        # {"value": 335, "name": 'ME'},
        # {"value": 310, "name": 'Package'},
        # {"value": 234, "name": 'Camera'},
        # {"value": 135, "name": 'VRAM'},
        # {"value": 1548, "name": 'CPU'},

    ]

    Test_Status = [
        # {
        #     "name": "Pass",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [120, 130, 140, 45, 56, 23, 120, 130, 140, 45]  # 对应机种顺序
        # },
        # {
        #     "name": "Fail",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 101, 23, 0, 120, 130, 140, 45]  # 对应机种顺序
        # },
        # {
        #     "name": "Ongoing",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [56, 67, 100, 12, 44, 55, 120, 130, 140, 45]  # 对应机种顺序
        # },
        # {
        #     "name": "Planning",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [88, 0, 38, 33, 12, 90, 120, 130, 140, 45]  # 对应机种顺序
        # },
    ]

    INV_Quantity = [
        # {
        #     "name": "PASS",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [120, 130, 140, 45]  # 对应机种顺序
        # },
        # {
        #     "name": "FAIL",
        #     "type": "bar",
        #     "stack": "status",
        #     "barMaxWidth": 50,
        #     "data": [100, 110, 125, 101]  # 对应机种顺序
        # },
    ]

    for i in INVGantt.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])

    if request.method == 'POST':
        if request.POST.get("isGetData") == "first":
            # Search1 default
            Customer = "All"
            Year = str(datetime.datetime.now().year)
            Projectlist = []

            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.all().values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            mock_data1_all = []
            for i in Projectlist:
                Standardtime = \
                INVGantt.objects.filter(Project_Name=i, Qualify_Cycles="New-Qualify").aggregate(Sum("Attend_Time"))[
                    "Attend_Time__sum"]
                Retesttime = \
                INVGantt.objects.filter(Project_Name=i, Qualify_Cycles="Re-Qualify").aggregate(Sum("Attend_Time"))[
                    "Attend_Time__sum"]
                if Standardtime:
                    Standardtime = round(float(Standardtime), 0)
                else:
                    Standardtime = 0
                if Retesttime:
                    Retesttime = round(float(Retesttime), 0)
                else:
                    Retesttime = 0
                Totaltime = Standardtime + Retesttime
                Total = INVGantt.objects.filter(Project_Name=i).exclude(Status="Planning").count()
                mock_data1_all.append({"Project": i, "Standard_test_time": Standardtime, "Retest_time": Retesttime,
                                       "Total_Attend_time": Totaltime, "Total": Total})
            mock_data1_all.sort(key=lambda x: x["Total_Attend_time"], reverse=True)
            number1 = 1
            for i in mock_data1_all:
                if number1 > 10:
                    break
                else:
                    mock_data1.append(i)
                    number1 += 1
            Projecttopkey = []
            for i in mock_data1:
                Projecttopkey.append(i["Project"])
            Top10["Customer_key"] = Projecttopkey
            for i in ["Standard_test_time", "Retest_time"]:
                datalist = []
                for j in Top10["Customer_key"]:
                    for k in mock_data1:
                        if k["Project"] == j:
                            datalist.append(k[i])
                Execution_Project.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )

            # Search2 default
            # Customer = request.POST.get("Customer")
            # Year = request.POST.get("Date")
            keypartlist = []
            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                            "TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values(
                            "TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
                else:
                    for i in INVGantt.objects.all().values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
            mock_data2_all = []
            mock_data3_all = []
            if Customer != "All":  # 因为不同Customer之间keypart名称有重复的，而Project_name没有重复的，所以不能像search1一样
                for i in keypartlist:
                    PassNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i,
                                                     Status__in=["Pass", 'Conditional Pass']).count()
                    FailNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status="Fail").count()
                    OngoingNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i,
                                                        Status__in=["Testing", 'Pending']).count()
                    PlanningNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status="Planning").count()
                    mock_data2_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
                    mock_data3_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
            else:
                for i in keypartlist:
                    PassNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Pass", 'Conditional Pass']).count()
                    FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail").count()
                    OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending']).count()
                    PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning").count()
                    mock_data2_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
                    mock_data3_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})

            mock_data2_all.sort(key=lambda x: x['Total'], reverse=True)
            mock_data3_all.sort(key=lambda x: x['Fail'], reverse=True)
            numberkeypart_Total = 1
            for i in mock_data2_all:
                if numberkeypart_Total > 10:
                    break
                else:
                    mock_data2.append(i)
                    numberkeypart_Total += 1
            keypart_Totalkey = []
            for i in mock_data2:
                keypart_Totalkey.append(i["KeyPart"])
                Keyparts.append({"value": i["Total"], "name": i["KeyPart"]})
            Top10["Keyparts_key"] = keypart_Totalkey

            numberkeypart_Fail = 1
            for i in mock_data3_all:
                if numberkeypart_Fail > 10:
                    break
                else:
                    mock_data3.append(i)
                    numberkeypart_Fail += 1
            keypart_Failkey = []
            for i in mock_data3:
                keypart_Failkey.append(i["KeyPart"])
                Failed_Keyparts.append({"value": i["Fail"], "name": i["KeyPart"]})
            Top10["Failed_Keyparts_key"] = keypart_Failkey

            # Search3 default
            # Customer = request.POST.get("Customer")
            # Year = request.POST.get("Date")
            # 虽然也要统计Planning的状态，但是时通过计算这一年的机种的所有状态，而不是直接通过Test_start+status统计
            Projectlist = []
            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.all().values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            mock_data4_all = []
            for i in Projectlist:
                PassNo = INVGantt.objects.filter(Project_Name=i,
                                                 Status__in=["Pass", 'Conditional Pass']).count()
                FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail").count()
                OngoingNo = INVGantt.objects.filter(Project_Name=i,
                                                    Status__in=["Testing", 'Pending']).count()
                PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning").count()
                mock_data4_all.append({
                    "Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                    # "Total": PassNo + FailNo + OngoingNo + PlanningNo
                    "Total": OngoingNo + PlanningNo
                })
            mock_data4_all.sort(key=lambda x: x["Total"], reverse=True)
            Projnumber = 1
            Projkey = []
            for i in mock_data4_all:
                if Projnumber > 10:
                    break
                else:
                    mock_data4.append(i)
                    Projkey.append(i["Project"])
                    Projnumber += 1
            Top10["Project_key"] = Projkey
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in Top10["Project_key"]:
                    for k in mock_data4:
                        if k["Project"] == j:
                            datalist.append(k[i])
                Test_Status.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )

            # Search4 default
            # Customer = request.POST.get("Customer")
            if Customer != "All":
                yearlist1 = INVGantt.objects.filter(Customer=Customer).annotate(TestEndYear=ExtractYear("Test_End"))
            else:
                yearlist1 = INVGantt.objects.all().annotate(TestEndYear=ExtractYear("Test_End"))
            # print(yearlist1,"1")
            # for i in yearlist1:
            #     print(i.Test_End, i.TestEndYear)
            Yearqura = yearlist1.values('TestEndYear').annotate(dcount=Count('TestEndYear'))
            # print(Yearqura)
            Yearlist = []
            for i in Yearqura:
                if i["TestEndYear"]:
                    Yearlist.append(i["TestEndYear"])
            # print(Yearlist)
            if Customer != "All":
                for i in Yearlist:
                    Test_Endperiod = [str(i) + "-01-01", str(i) + "-12-31"]
                    PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail",
                                                     Test_Start__range=Test_Endperiod).count()
                    # print(round(FailNo / PassNo, 2),format(round(FailNo / PassNo, 2), '.2%'))
                    if PassNo:
                        Failure = format(round(FailNo / PassNo, 2), '.0%')
                    else:
                        Failure = format(round(0), '.0%')
                    mock_data5.append(
                        {"Year": "Y" + str(i), "PASS": PassNo, "FAIL": FailNo, "Total": PassNo + FailNo,
                         "Failure": Failure})
            else:
                for i in Yearlist:
                    Test_Endperiod = [str(i) + "-01-01", str(i) + "-12-31"]
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    FailNo = INVGantt.objects.filter(Status="Fail", Test_Start__range=Test_Endperiod).count()
                    # print(round(FailNo / PassNo, 2),format(round(FailNo / PassNo, 2), '.2%'))
                    if PassNo:
                        Failure = format(round(FailNo / PassNo, 2), '.0%')
                    else:
                        Failure = format(round(0), '.0%')
                    mock_data5.append(
                        {"Year": "Y" + str(i), "PASS": PassNo, "FAIL": FailNo, "Total": PassNo + FailNo,
                         "Failure": Failure})
            Top10["Quantity_key"] = Yearlist
            for i in ["PASS", "FAIL"]:
                datalist = []
                for j in Top10["Quantity_key"]:
                    for k in mock_data5:
                        if k["Year"] == "Y" + str(j):
                            datalist.append(k[i])
                INV_Quantity.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )

        if request.POST.get("isGetData") == "SEARCH1":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Date")
            Projectlist = []
            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values("Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values("Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.all().values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            mock_data1_all = []
            for i in Projectlist:
                Standardtime = INVGantt.objects.filter(Project_Name=i, Qualify_Cycles="New-Qualify").aggregate(Sum("Attend_Time"))["Attend_Time__sum"]
                Retesttime = INVGantt.objects.filter(Project_Name=i, Qualify_Cycles="Re-Qualify").aggregate(Sum("Attend_Time"))[
                    "Attend_Time__sum"]
                if Standardtime:
                    Standardtime = round(float(Standardtime), 0)
                else:
                    Standardtime = 0
                if Retesttime:
                    Retesttime = round(float(Retesttime), 0)
                else:
                    Retesttime = 0
                Totaltime = Standardtime + Retesttime
                Total = INVGantt.objects.filter(Project_Name=i).exclude(Status="Planning").count()
                mock_data1_all.append({"Project": i, "Standard_test_time": Standardtime, "Retest_time": Retesttime,
                                       "Total_Attend_time": Totaltime, "Total": Total})
            mock_data1_all.sort(key=lambda x: x["Total_Attend_time"], reverse=True)
            number1 = 1
            for i in mock_data1_all:
                if number1 > 10:
                    break
                else:
                    mock_data1.append(i)
                    number1 += 1
            Projecttopkey = []
            for i in mock_data1:
                Projecttopkey.append(i["Project"])
            Top10["Customer_key"] = Projecttopkey
            for i in ["Standard_test_time", "Retest_time"]:
                datalist = []
                for j in Top10["Customer_key"]:
                    for k in mock_data1:
                        if k["Project"] == j:
                            datalist.append(k[i])
                Execution_Project.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth":50,
                        "data": datalist#对应机种顺序
                    },
                )
        if request.POST.get("isGetData") == "SEARCH2":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Date")
            keypartlist = []
            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer, Test_Start__range=Test_Endperiod).values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
                else:
                    for i in INVGantt.objects.all().values("TP_Cat").distinct().order_by("TP_Cat"):
                        keypartlist.append(i["TP_Cat"])
            mock_data2_all = []
            mock_data3_all = []
            if Customer != "All":#因为不同Customer之间keypart名称有重复的，而Project_name没有重复的，所以不能像search1一样
                for i in keypartlist:
                    PassNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status__in=["Pass", 'Conditional Pass']).count()
                    FailNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status="Fail").count()
                    OngoingNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status__in=["Testing", 'Pending']).count()
                    # PlanningNo = INVGantt.objects.filter(Customer=Customer, TP_Cat=i, Status="Planning").count()
                    mock_data2_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
                    mock_data3_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
            else:
                for i in keypartlist:
                    PassNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Pass", 'Conditional Pass']).count()
                    FailNo = INVGantt.objects.filter(TP_Cat=i, Status="Fail").count()
                    OngoingNo = INVGantt.objects.filter(TP_Cat=i, Status__in=["Testing", 'Pending']).count()
                    # PlanningNo = INVGantt.objects.filter(TP_Cat=i, Status="Planning").count()
                    mock_data2_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})
                    mock_data3_all.append({"KeyPart": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo,
                                           "Total": PassNo + FailNo + OngoingNo})

            mock_data2_all.sort(key=lambda x: x['Total'], reverse=True)
            mock_data3_all.sort(key=lambda x: x['Fail'], reverse=True)
            numberkeypart_Total = 1
            for i in mock_data2_all:
                if numberkeypart_Total > 10:
                    break
                else:
                    mock_data2.append(i)
                    numberkeypart_Total += 1
            keypart_Totalkey = []
            for i in mock_data2:
                keypart_Totalkey.append(i["KeyPart"])
                Keyparts.append({"value": i["Total"], "name": i["KeyPart"]})
            Top10["Keyparts_key"] = keypart_Totalkey

            numberkeypart_Fail = 1
            for i in mock_data3_all:
                if numberkeypart_Fail > 10:
                    break
                else:
                    mock_data3.append(i)
                    numberkeypart_Fail += 1
            keypart_Failkey = []
            for i in mock_data3:
                keypart_Failkey.append(i["KeyPart"])
                Failed_Keyparts.append({"value": i["Fail"], "name": i["KeyPart"]})
            Top10["Failed_Keyparts_key"] = keypart_Failkey
        if request.POST.get("isGetData") == "SEARCH3":
            Customer = request.POST.get("Customer")
            Year = request.POST.get("Date")
            Projectlist = []
            # 虽然也要统计Planning的状态，但是时通过计算这一年的机种的所有状态，而不是直接通过Test_start+status统计
            if Customer != "All":
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Customer=Customer,Test_Start__range=Test_Endperiod).values("Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.filter(Customer=Customer).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            else:
                if Year:
                    Test_Endperiod = [Year + "-01-01", Year + "-12-31"]
                    for i in INVGantt.objects.filter(Test_Start__range=Test_Endperiod).values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
                else:
                    for i in INVGantt.objects.all().values(
                            "Project_Name").distinct().order_by("Project_Name"):
                        Projectlist.append(i["Project_Name"])
            mock_data4_all = []
            for i in Projectlist:
                PassNo = INVGantt.objects.filter(Project_Name=i,
                                                 Status__in=["Pass", 'Conditional Pass']).count()
                FailNo = INVGantt.objects.filter(Project_Name=i, Status="Fail").count()
                OngoingNo = INVGantt.objects.filter(Project_Name=i,
                                                    Status__in=["Testing", 'Pending']).count()
                PlanningNo = INVGantt.objects.filter(Project_Name=i, Status="Planning").count()
                mock_data4_all.append({
                                        "Project": i, "Pass": PassNo, "Fail": FailNo, "Ongoing": OngoingNo, "Planning": PlanningNo,
                                       # "Total": PassNo + FailNo + OngoingNo + PlanningNo
                                        "Total": OngoingNo + PlanningNo
                                       })
            mock_data4_all.sort(key=lambda x: x["Total"], reverse=True)
            Projnumber = 1
            Projkey = []
            for i in mock_data4_all:
                if Projnumber > 10:
                    break
                else:
                    mock_data4.append(i)
                    Projkey.append(i["Project"])
                    Projnumber += 1
            Top10["Project_key"] = Projkey
            for i in ["Pass", "Fail", "Ongoing", "Planning"]:
                datalist = []
                for j in Top10["Project_key"]:
                    for k in mock_data4:
                        if k["Project"] == j:
                            datalist.append(k[i])
                Test_Status.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth":50,
                        "data": datalist#对应机种顺序
                    },
                )
        if request.POST.get("isGetData") == "SEARCH4":
            Customer = request.POST.get("Customer")
            if Customer != "All":
                yearlist1 = INVGantt.objects.filter(Customer=Customer).annotate(TestEndYear=ExtractYear("Test_End"))
            else:
                yearlist1 = INVGantt.objects.all().annotate(TestEndYear=ExtractYear("Test_End"))
            # print(yearlist1,"1")
            # for i in yearlist1:
            #     print(i.Test_End, i.TestEndYear)
            Yearqura = yearlist1.values('TestEndYear').annotate(dcount=Count('TestEndYear'))
            # print(Yearqura)
            Yearlist = []
            for i in Yearqura:
                if i["TestEndYear"]:
                    Yearlist.append(i["TestEndYear"])
            # print(Yearlist)
            if Customer != "All":
                for i in Yearlist:
                    Test_Endperiod = [str(i) + "-01-01", str(i) + "-12-31"]
                    PassNo = INVGantt.objects.filter(Customer=Customer, Status__in=["Pass", 'Conditional Pass'], Test_Start__range=Test_Endperiod).count()
                    FailNo = INVGantt.objects.filter(Customer=Customer, Status="Fail", Test_Start__range=Test_Endperiod).count()
                    # print(round(FailNo / PassNo, 2),format(round(FailNo / PassNo, 2), '.2%'))
                    if PassNo:
                        Failure = format(round(FailNo / PassNo, 2), '.0%')
                    else:
                        Failure = format(round(0), '.0%')
                    mock_data5.append({"Year": "Y" + str(i), "PASS": PassNo, "FAIL": FailNo, "Total": PassNo + FailNo, "Failure": Failure})
            else:
                for i in Yearlist:
                    Test_Endperiod = [str(i) + "-01-01", str(i) + "-12-31"]
                    PassNo = INVGantt.objects.filter(Status__in=["Pass", 'Conditional Pass'],
                                                     Test_Start__range=Test_Endperiod).count()
                    FailNo = INVGantt.objects.filter(Status="Fail", Test_Start__range=Test_Endperiod).count()
                    # print(round(FailNo / PassNo, 2),format(round(FailNo / PassNo, 2), '.2%'))
                    if PassNo:
                        Failure = format(round(FailNo / PassNo, 2), '.0%')
                    else:
                        Failure = format(round(0), '.0%')
                    mock_data5.append(
                        {"Year": "Y" + str(i), "PASS": PassNo, "FAIL": FailNo, "Total": PassNo + FailNo,
                         "Failure": Failure})
            Top10["Quantity_key"] = Yearlist
            for i in ["PASS", "FAIL"]:
                datalist = []
                for j in Top10["Quantity_key"]:
                    for k in mock_data5:
                        if k["Year"] == "Y" + str(j):
                            datalist.append(k[i])
                INV_Quantity.append(
                    {
                        "name": i,
                        "type": "bar",
                        "stack": "status",
                        "barMaxWidth": 50,
                        "data": datalist  # 对应机种顺序
                    },
                )

        data = {
            "err_ok": "0",
            "content1": mock_data1,
            "content2": mock_data2,
            "content3": mock_data3,
            "content4": mock_data4,
            "content5": mock_data5,
            "select": selectItem,
            'Top10': Top10,
            "Execution_Project": Execution_Project,
            "Test_Status": Test_Status,
            "INV_Quantity": INV_Quantity,
            "Failed_Keyparts": Failed_Keyparts,
            "Keyparts": Keyparts,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'INVGantt/INVGantt_top.html', locals())

from rest_framework.viewsets import ModelViewSet
from .serializers import *

class INVGantView(ModelViewSet):
    # queryset是一个查询数据的查询集，存储这所有的数据库查询之后的数据
    queryset = INVGantt.objects.all()
    serializer_class = INVGantserilizer
    # serializer_class用来指定在当前的视图里面进行　序列化与反序列时使用的序列化器（串行器）

from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
@csrf_exempt
def INVGantViewre(request):
    if request.method == "GET":
        invgant = INVGantt.objects.all()
        checklist = {}
        print(request.GET)
        if request.GET.get("Project_Name"):
            checklist['Project_Name'] =request.GET.get("Project_Name")
        if checklist:
            invgant = INVGantt.objects.filter(**checklist)
        ser = INVGantserilizer(instance=invgant, many=True)
        jsondata = JSONRenderer().render(ser.data)
        return HttpResponse(jsondata, content_type='application/json', status=200)
