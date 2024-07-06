from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime,json,simplejson,requests,time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import KnowIssue_M
from .forms import KnowIssue_F
from app01.models import ProjectinfoinDCT
from app01.models import UserInfo
@csrf_exempt
def KnowIssue_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="KnowIssue/KnowIssue_upload"
    err_ok = 0  # excel上传1为重复

    result = 0  # 为1 forms 上传重复
    rpeatcontend = [
    ]

    KnowIssue = KnowIssue_F(request.POST)
    # print(request.method)
    if request.method == 'POST':
        # print(request.POST)
        if 'Upload' in request.POST.keys():
            if KnowIssue.is_valid():
                Customer = request.POST.get('Customer')
                Project_Code = request.POST.get('Project_Code')
                Platform = request.POST.get('Platform')
                Issue_NO = request.POST.get('Issue_NO')
                Issue_Title = request.POST.get('Issue_Title')
                Issue_Component = request.POST.get('Issue_Component')
                Detect_By_Case = request.POST.get('Detect_By_Case')
                Root_Cause = request.POST.get('Root_Cause')
                Issue_Status = request.POST.get('Issue_Status')
                PL = request.POST.get('PL')
                Editor = request.session.get('user_name')
                Edittime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Check_dic = {"Customer": Customer, "Project_Code": Project_Code, "Platform": Platform, "Issue_NO": Issue_NO,
                                "Issue_Title": Issue_Title
                             }
                Create_dic = {"Customer": Customer, "Project_Code": Project_Code, "Platform": Platform,
                             "Issue_NO": Issue_NO, "Issue_Title": Issue_Title, "Issue_Component": Issue_Component,
                              "Detect_By_Case": Detect_By_Case,
                              "Root_Cause": Root_Cause, "Issue_Status": Issue_Status, "PL": PL,
                              "Editor": Editor, "Edittime": Edittime
                             }
                if KnowIssue_M.objects.filter(**Check_dic).first():
                    UpdateResult = "数据已存在数据库中"
                    # print(UpdateResult)
                    rpeatcontend.append({})
                    # message_err=1
                    result = 1
                else:
                    KnowIssue_M.objects.create(**Create_dic)
                    result = 0
            else:
                cleandata=KnowIssue.errors
    print(locals())
    return render(request, 'KnowIssue/Known_Issue_upload.html', locals())

@csrf_exempt
def KnowIssue_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="KnowIssue/KnowIssue_search"
    mock_data = [
        # {"id": "1", "Customer": "C38A", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "aaaa"},
        # {"id": "2", "Customer": "C38N", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "bbbbb"},
        # {"id": "3", "Customer": "A39", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "cccccc"},
        # {"id": "4", "Customer": "C38A", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "ddddd"},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
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
    for i in KnowIssue_M.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    if request.method == 'POST':
        if request.POST.get("isGetData") == "SEARCHALERT":
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in KnowIssue_M.objects.filter(Customer=Customer).values("Project_Code").distinct().order_by(
                        "Project_Code"):
                    Prolist.append(i["Project_Code"])
            else:
                for i in KnowIssue_M.objects.all().values("Project_Code").distinct().order_by("Project_Code"):
                    Prolist.append(i["Project_Code"])
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
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
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
                            if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                PrjEngCode1 = Proinfo1.PrjEngCode1
                            else:
                                PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                            if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                PrjEngCode2 = Proinfo1.PrjEngCode2
                            else:
                                PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
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
                            if Proinfo1.Type == Proinfo2.Type:
                                Type = Proinfo1.Type
                            else:
                                Type = Proinfo1.Type + "/" + Proinfo2.Type
                            if Proinfo1.PPA == Proinfo2.PPA:
                                PPA = Proinfo1.PPA
                            else:
                                PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                            if Proinfo1.PQE == Proinfo2.PQE:
                                PQE = Proinfo1.PQE
                            else:
                                PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
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
                                "PrjEngCode1": PrjEngCode1,
                                "PrjEngCode2": PrjEngCode2,
                                "PROJECT": ProjectName,
                                "SIZE": Size,
                                "CPU": CPU,
                                "PLATFORM": Platform,
                                "VGA": VGA,
                                "OS SUPPORT": OSSupport,
                                "Type": Type,
                                "PPA": PPA,
                                "PQE": PQE,
                                "SS": SS,
                                "LD": LD,
                                "DQA PL": DQAPL,
                            })
                        else:
                            searchalert.append({
                                "id": "",
                                "YEAR": "", "COMPRJCODE": i,
                                "PrjEngCode1": "",
                                "PrjEngCode2": "",
                                "PROJECT": "",
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
                    else:
                        searchalert.append({
                            "YEAR": "", "COMPRJCODE": i,
                            "PrjEngCode1": "",
                            "PrjEngCode2": "",
                            "PROJECT": "",
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
        if request.POST.get("isGetData") == "SEARCH":
            Customer = request.POST.get('Customer')
            Project_Code = request.POST.get('COMPRJCODE')
            for i in KnowIssue_M.objects.filter(Customer=Customer, Project_Code=Project_Code):
                mock_data.append({
                    "id": i.id, "Customer": i.Customer, "Project_Code": i.Project_Code, "Platform": i.Platform, "Issue_NO": i.Issue_NO,
                     "Issue_Title": i.Issue_Title, "Issue_Component": i.Issue_Component, "Detect_By_Case": i.Detect_By_Case,
                    "Root_Cause": i.Root_Cause, "Issue_Status": i.Issue_Status, "PL": i.PL
                })

        data = {
            "content": mock_data,
            "select": selectItem,
            "sear": searchalert,
            "err_ok": "0",
            "canEdit": 1,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'KnowIssue/Known_Issue_search.html', locals())

@csrf_exempt
def KnowIssue_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="KnowIssue/KnowIssue_edit"
    mock_data = [
        # {"id": "1", "Customer": "C38A", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "aaaa"},
        # {"id": "2", "Customer": "C38N", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "bbbbb"},
        # {"id": "3", "Customer": "A39", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "cccccc"},
        # {"id": "4", "Customer": "C38A", "Project_Code": "TBD", "Platform": "FLY00", "TDMS_NO": "FLY00",
        #  "Issue_Title": "2020", "Root_Cause": "24", "Solution": "1", "PL": "ddddd"},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
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
    for i in KnowIssue_M.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    if request.method == 'POST':
        if request.POST.get("isGetData") == "SEARCHALERT":
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in KnowIssue_M.objects.filter(Customer=Customer).values("Project_Code").distinct().order_by(
                        "Project_Code"):
                    Prolist.append(i["Project_Code"])
            else:
                for i in KnowIssue_M.objects.all().values("Project_Code").distinct().order_by("Project_Code"):
                    Prolist.append(i["Project_Code"])
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
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
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
                            if Proinfo1.Type == Proinfo2.Type:
                                Type = Proinfo1.Type
                            else:
                                Type = Proinfo1.Type + "/" + Proinfo2.Type
                            if Proinfo1.PPA == Proinfo2.PPA:
                                PPA = Proinfo1.PPA
                            else:
                                PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                            if Proinfo1.PQE == Proinfo2.PQE:
                                PQE = Proinfo1.PQE
                            else:
                                PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
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
                                "Type": Type,
                                "PPA": PPA,
                                "PQE": PQE,
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
                                "Type": "",
                                "PPA": "",
                                "PQE": "",
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
        if request.POST.get("isGetData") == "SEARCH":
            Customer = request.POST.get('Customer')
            Project_Code = request.POST.get('COMPRJCODE')
            for i in KnowIssue_M.objects.filter(Customer=Customer, Project_Code=Project_Code):
                mock_data.append({
                    "id": i.id, "Customer": i.Customer, "Project_Code": i.Project_Code, "Platform": i.Platform, "Issue_NO": i.Issue_NO,
                     "Issue_Title": i.Issue_Title, "Issue_Component": i.Issue_Component, "Detect_By_Case": i.Detect_By_Case,
                    "Root_Cause": i.Root_Cause, "Issue_Status": i.Issue_Status, "PL": i.PL
                })
        if 'SAVE' in str(request.body):
            resdatas = json.loads(request.body)
            # print(resdatas)
            Customer = resdatas["Customer"]
            Project_Code = resdatas["Project"]
            id = resdatas["rows"]["id"]
            update_dic = {
                "Customer": resdatas["rows"]["Customer"], "Project_Code": resdatas["rows"]["Project_Code"],
                "Platform": resdatas["rows"]["Platform"], "Issue_NO": resdatas["rows"]["Issue_NO"],
                "Issue_Title": resdatas["rows"]["Issue_Title"], "Issue_Component": resdatas["rows"]["Issue_Component"],
                "Detect_By_Case": resdatas["rows"]["Detect_By_Case"], "Root_Cause": resdatas["rows"]["Root_Cause"],
                "Issue_Status": resdatas["rows"]["Issue_Status"], "PL": resdatas["rows"]["PL"],
                "Editor": request.session.get('user_name'), "Edittime": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            }
            KnowIssue_M.objects.filter(id=id).update(**update_dic)
            for i in KnowIssue_M.objects.filter(Customer=Customer, Project_Code=Project_Code):
                mock_data.append({
                    "id": i.id, "Customer": i.Customer, "Project_Code": i.Project_Code, "Platform": i.Platform, "Issue_NO": i.Issue_NO,
                     "Issue_Title": i.Issue_Title, "Issue_Component": i.Issue_Component, "Detect_By_Case": i.Detect_By_Case,
                    "Root_Cause": i.Root_Cause, "Issue_Status": i.Issue_Status, "PL": i.PL
                })


        data = {
            "content": mock_data,
            "select": selectItem,
            "sear": searchalert,
            "err_ok": "0",
            "canEdit": 1,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'KnowIssue/Known_Issue_edit.html', locals())