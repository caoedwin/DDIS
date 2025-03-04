from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime,json,simplejson,requests,time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from app01.models import UserInfo
from django.db.models import F
from django.db.models.functions import ExtractYear
# Create your views here.
@csrf_exempt
def SpecDownload_summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="SpecDownload/SpecDownload_Summary"
    selectOptions=[
        # [{
        #     "label":"C38(NB)",
        #     "value":"C38(NB)",
        # },{
        #     "label":"C38(AIO)",
        #     "value":"C38(AIO)",
        # },{
        #     "label":"A39",
        #     "value":"A39",
        # },{
        #     "label":"AIO(T88)",
        #     "value":"AIO(T88)",
        # }],[{"categoty": "HW"},
        #  {"categoty": "SW"},
        #  ],
        # [{"fc": "xxxx"},
        #  {"fc": "xx"},
        #  {"fc": "cccc"}],
    ]
    mock_data=[
        # {"id":"1","Customer":"C38(NB)","Category":"wsx","Fc":"6yjumjh","Case_name":"umjnyj","Version":"1.0", "file":""},
        # {"id":"2","Customer":"A39","Category":"wef","Fc":"5yuymjh","Case_name":"","Version":"2.0"},
        # {"id":"3","Customer":"C38(AIO)","Category":"zdfre","Fc":"juyjye","Case_name":"tyjth","Version":"13.1"},
        # {"id":"4","Customer":"A39","Category":"wergtrbfvd","Fc":"eyrujyjh","Case_name":"ytjujhhty","Version":"11.0"},
        # {"id":"5","Customer":"AIO(T88)","Category":"fdvfbtgrf","Fc":"rgthyhgb","Case_name":"tyjmhn","Version":"5.3"}
    ]
    duplicate_check = 0
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
    Customerlist = []
    for i in SpecDownload.objects.all().values("Customer").distinct().order_by("Customer"):
        Customerlist.append({"label": i["Customer"], "value": i["Customer"]})
    selectOptions.append(Customerlist)
    Categorylist = []
    for i in SpecDownload.objects.all().values("Category").distinct().order_by("Category"):
        Categorylist.append({"categoty": i["Category"]})
    selectOptions.append(Categorylist)
    Functionnlist = []
    for i in SpecDownload.objects.all().values("Functionn").distinct().order_by("Functionn"):
        Functionnlist.append({"fc": i["Functionn"]})
    selectOptions.append(Functionnlist)
    if request.method == 'POST':
        if request.POST.get("action") == "submit":
            Customersearch = request.POST.get("searchCustomer")
            Categorysearch = request.POST.get("searchCategory")
            Functionnsearch = request.POST.get("searchFC")

            fileList = request.FILES.getlist("fileList", "")
            Customer = request.POST.get("Customer")
            Category = request.POST.get("Category")
            Functionn = request.POST.get("Functionn")
            Case_name = request.POST.get("Case_name")
            Version = request.POST.get("Version")
            checkSpecdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name,
                         "Version": Version, }

            if SpecDownload.objects.filter(**checkSpecdic):
                duplicate_check = 1
            else:
                # Createdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name, "Version": Version,}
                # SpecDownload.objects.create(**Createdic)
                SpecDownloads = SpecDownload()
                SpecDownloads.Customer = Customer
                SpecDownloads.Category = Category
                SpecDownloads.Functionn =Functionn
                SpecDownloads.Case_name = Case_name
                SpecDownloads.Version = Version
                SpecDownloads.editor = request.session.get('account')
                SpecDownloads.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                SpecDownloads.save()
                if fileList:
                    for f in fileList:
                        # print(f)
                        empt = files_SpecD()
                        # 增加其他字段应分别对应填写
                        empt.single = f
                        empt.files = f
                        empt.save()
                        SpecDownloads.files_Spec.add(empt)
            if Customersearch and Categorysearch and Functionnsearch:
                searchdic = {"Customer": Customersearch, "Category": Categorysearch, "Functionn": Functionnsearch,}
                for i in SpecDownload.objects.filter(**searchdic):
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            selectOptions = []
            Customerlist = []
            for i in SpecDownload.objects.all().values("Customer").distinct().order_by("Customer"):
                Customerlist.append({"label": i["Customer"], "value": i["Customer"]})
            selectOptions.append(Customerlist)
            Categorylist = []
            for i in SpecDownload.objects.all().values("Category").distinct().order_by("Category"):
                Categorylist.append({"categoty": i["Category"]})
            selectOptions.append(Categorylist)
            Functionnlist = []
            for i in SpecDownload.objects.all().values("Functionn").distinct().order_by("Functionn"):
                Functionnlist.append({"fc": i["Functionn"]})
            selectOptions.append(Functionnlist)
        if request.POST.get("isGetData") == "Search":
            Customer = request.POST.get("Customer")
            Category = request.POST.get("Category")
            Functionn = request.POST.get("Function")
            checkSpecdic = {"Customer": Customer, "Category":Category, "Functionn":Functionn}
            for i in SpecDownload.objects.filter(**checkSpecdic):
                filelist = []
                for h in i.files_Spec.all():
                    filelist.append("/media/" + str(h.files))
                mock_data.append({
                    "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                    "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                })
        if request.POST.get("action") == "edit":
            Customersearch = request.POST.get("showCustomer")
            Categorysearch = request.POST.get("showCategory")
            Functionnsearch = request.POST.get("showFunction")
            # print(Customersearch, Categorysearch, Functionnsearch)

            # fileList = request.FILES.getlist("fileList", "")
            Customer = request.POST.get("Customer")
            Category = request.POST.get("category")
            Functionn = request.POST.get("Fc")
            Case_name = request.POST.get("Case_name")
            Version = request.POST.get("Version")
            editor = request.session.get('account')
            id = request.POST.get("ID")
            updateSpecdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name,
                            "Version": Version, "editor": editor}
            SpecDownload.objects.filter(id=id).update(**updateSpecdic)
            if Customersearch and Categorysearch and Functionnsearch:
                searchdic = {"Customer": Customersearch, "Category": Categorysearch, "Functionn": Functionnsearch,}
                for i in SpecDownload.objects.filter(**searchdic):
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            selectOptions = []
            Customerlist = []
            for i in SpecDownload.objects.all().values("Customer").distinct().order_by("Customer"):
                Customerlist.append({"label": i["Customer"], "value": i["Customer"]})
            selectOptions.append(Customerlist)
            Categorylist = []
            for i in SpecDownload.objects.all().values("Category").distinct().order_by("Category"):
                Categorylist.append({"categoty": i["Category"]})
            selectOptions.append(Categorylist)
            Functionnlist = []
            for i in SpecDownload.objects.all().values("Functionn").distinct().order_by("Functionn"):
                Functionnlist.append({"fc": i["Functionn"]})
            selectOptions.append(Functionnlist)
        if request.POST.get("action") == "DELETE":
            Customersearch = request.POST.get("showCustomer")
            Categorysearch = request.POST.get("showCategory")
            Functionnsearch = request.POST.get("showFunction")

            id = request.POST.get("ID")

            SpecDownload.objects.get(id=id).files_Spec.all().delete()#多对多时可以先删除母表里的数据，一对多是不行？
            SpecDownload.objects.get(id=id).delete()
            # instance = #你获取的需要修改的那条记录，确保能够用instance.字段名能够获取到你保存的相对路径
            # sender = #你要修改的图片字段所在的类
            # file_delete(sender, instance, **kwargs)

            if Customersearch and Categorysearch and Functionnsearch:
                searchdic = {"Customer": Customersearch, "Category": Categorysearch, "Functionn": Functionnsearch, }
                for i in SpecDownload.objects.filter(**searchdic):
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn,
                        "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn,
                        "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist, "Ownerflag": 1 if request.session.get('account') == i.editor else 0
                    })
            selectOptions = []
            Customerlist = []
            for i in SpecDownload.objects.all().values("Customer").distinct().order_by("Customer"):
                Customerlist.append({"label": i["Customer"], "value": i["Customer"]})
            selectOptions.append(Customerlist)
            Categorylist = []
            for i in SpecDownload.objects.all().values("Category").distinct().order_by("Category"):
                Categorylist.append({"categoty": i["Category"]})
            selectOptions.append(Categorylist)
            Functionnlist = []
            for i in SpecDownload.objects.all().values("Functionn").distinct().order_by("Functionn"):
                Functionnlist.append({"fc": i["Functionn"]})
            selectOptions.append(Functionnlist)
        data = {
            "selectOptions": selectOptions,
            "content": mock_data,
            "duplicate_check": duplicate_check,
            "canEdit": canEdit,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'SpecDownload/SpecDwonload_Summary.html', locals())

@csrf_exempt
def ManagementSop_summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="SpecDownload/SpecDownload_Summary"
    selectOptions=[
        # [{
        #     "label":"C38(NB)",
        #     "value":"C38(NB)",
        # },{
        #     "label":"C38(AIO)",
        #     "value":"C38(AIO)",
        # },{
        #     "label":"A39",
        #     "value":"A39",
        # },{
        #     "label":"AIO(T88)",
        #     "value":"AIO(T88)",
        # }],[{"categoty": "HW"},
        #  {"categoty": "SW"},
        #  ],
        # [{"fc": "xxxx"},
        #  {"fc": "xx"},
        #  {"fc": "cccc"}],
    ]
    mock_data=[
        # {"id":"1","Customer":"C38(NB)","Category":"wsx","Fc":"6yjumjh","Case_name":"umjnyj","Version":"1.0", "file":""},
        # {"id":"2","Customer":"A39","Category":"wef","Fc":"5yuymjh","Case_name":"","Version":"2.0"},
        # {"id":"3","Customer":"C38(AIO)","Category":"zdfre","Fc":"juyjye","Case_name":"tyjth","Version":"13.1"},
        # {"id":"4","Customer":"A39","Category":"wergtrbfvd","Fc":"eyrujyjh","Case_name":"ytjujhhty","Version":"11.0"},
        # {"id":"5","Customer":"AIO(T88)","Category":"fdvfbtgrf","Fc":"rgthyhgb","Case_name":"tyjmhn","Version":"5.3"}
    ]
    mock_data = [
        # {"id": "1", "No": "1", "Title": "PCQAU實驗室設備管理規範", "Description": "實驗室設備管理標準化文件", "Version": "V00",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},

    ]

    mock_data1 = [
        # {"id": "1", "No": "2", "Title": "設備申購作業", "Description": "實驗室設備申購作業流程指導說明", "Version": "V1.0",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},
        # {"id": "2", "No": "3", "Title": "設備配件安裝維修", "Description": "實驗室設備配件安裝維修流程說明", "Version": "V1.0",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 0},

    ]

    mock_data2 = [
        # {"id": "1", "No": "4", "Title": "衝擊試驗機", "Description": "4 in 1 報告：規格定義/驗收報告/驗收標準/保養模版", "Version": "V1.0",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},
        # {"id": "2", "No": "5", "Title": "", "Description": "設備標準作業指導書SOP", "Version": "V1.1",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 0},
        # {"id": "3", "No": "6", "Title": "震動試驗機", "Description": "4 in 1 報告：規格定義/驗收報告/驗收標準/保養模版", "Version": "V1.0",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},
        # {"id": "4", "No": "7", "Title": "", "Description": "設備標準作業指導書SOP", "Version": "V1.2",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 0},
        # {"id": "5", "No": "8", "Title": "跌落試驗機", "Description": "4 in 1 報告：規格定義/驗收報告/驗收標準/保養模版", "Version": "V1.0",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},
        # {"id": "6", "No": "9", "Title": "", "Description": "設備標準作業指導書SOP", "Version": "V1.2",
        #  "Upload_Date": "2025/1/18", "file": "", "Ownerflag": 1},
    ]

    errMessage = ""
    addPermission = 0  # 1:可新增 0:不可新增
    deletePermission = 0  # 1:可刪除 0:不可刪除
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    # print(roles)
    editPpriority = 100
    for i in roles:
        if 'DQA_LNV_ManSop_Admin' in i:
            addPermission, deletePermission = 1, 1
        # elif 'PM' in i:
        #     if editPpriority != 4:
        #         editPpriority = 1
        # elif 'RD' in i:
        #     if editPpriority != 4 and editPpriority != 1:
        #         editPpriority = 2
    if request.method == 'POST':
        if request.POST:
            if request.POST.get("isGetData") == "first":
                pass
            if request.POST.get("action") == "submit1":
                fileList = request.FILES.getlist("fileList", "")
                Num = request.POST.get("No")
                Title = request.POST.get("Title")
                Description = request.POST.get("Description")
                Version = request.POST.get("Version")

                if ManagementSopRoom.objects.filter(Num=Num):
                    errMessage = "No号重复"
                else:
                    # Createdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name, "Version": Version,}
                    # SpecDownload.objects.create(**Createdic)
                    ManagementSopRooms = ManagementSopRoom()
                    ManagementSopRooms.Num = Num
                    ManagementSopRooms.Title = Title
                    ManagementSopRooms.Description = Description
                    ManagementSopRooms.Version = Version
                    ManagementSopRooms.editor = request.session.get('account')
                    ManagementSopRooms.edit_time = datetime.datetime.now().strftime("%Y-%m-%d")
                    ManagementSopRooms.save()
                    if fileList:
                        for f in fileList:
                            # print(f)
                            empt = files_SopRom()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            ManagementSopRooms.files_Spec.add(empt)
            if request.POST.get("action") == "submit2":
                fileList = request.FILES.getlist("fileList", "")
                Num = request.POST.get("No")
                Title = request.POST.get("Title")
                Description = request.POST.get("Description")
                Version = request.POST.get("Version")

                if ManagementSopProcess.objects.filter(Num=Num):
                    errMessage = "No号重复"
                else:
                    # Createdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name, "Version": Version,}
                    # SpecDownload.objects.create(**Createdic)
                    ManagementSopProcesss = ManagementSopProcess()
                    ManagementSopProcesss.Num = Num
                    ManagementSopProcesss.Title = Title
                    ManagementSopProcesss.Description = Description
                    ManagementSopProcesss.Version = Version
                    ManagementSopProcesss.editor = request.session.get('account')
                    ManagementSopProcesss.edit_time = datetime.datetime.now().strftime("%Y-%m-%d")
                    ManagementSopProcesss.save()
                    if fileList:
                        for f in fileList:
                            # print(f)
                            empt = files_SopProcess()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            ManagementSopProcesss.files_Spec.add(empt)
            if request.POST.get("action") == "submit3":
                fileList = request.FILES.getlist("fileList", "")
                Num = request.POST.get("No")
                Title = request.POST.get("Title")
                Description = request.POST.get("Description")
                Version = request.POST.get("Version")

                if ManagementSopDevice.objects.filter(Num=Num):
                    errMessage = "No号重复"
                else:
                    # Createdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name, "Version": Version,}
                    # SpecDownload.objects.create(**Createdic)
                    ManagementSopDevices = ManagementSopDevice()
                    ManagementSopDevices.Num = Num
                    ManagementSopDevices.Title = Title
                    ManagementSopDevices.Description = Description
                    ManagementSopDevices.Version = Version
                    ManagementSopDevices.editor = request.session.get('account')
                    ManagementSopDevices.edit_time = datetime.datetime.now().strftime("%Y-%m-%d")
                    ManagementSopDevices.save()
                    if fileList:
                        for f in fileList:
                            # print(f)
                            empt = files_SopDevice()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            ManagementSopDevices.files_Spec.add(empt)
        else:
            try:
                request.body
                # print(request.body)
            except:
                # print('1')
                pass
            else:
                # print('2')
                if 'delete1' in str(request.body):
                    responseData = json.loads(request.body)
                    for i in responseData['params']:
                        # print(i)
                        ManagementSopRoom.objects.get(id=i).files_Spec.all().delete()#删除实体文件 model中的files_SopRom_delete方法
                        ManagementSopRoom.objects.get(id=i).delete()
                if 'delete2' in str(request.body):
                    responseData = json.loads(request.body)
                    for i in responseData['params']:
                        # print(i)
                        ManagementSopProcess.objects.get(id=i).files_Spec.all().delete()#删除实体文件 model中的files_SopRom_delete方法
                        ManagementSopProcess.objects.get(id=i).delete()
                if 'delete3' in str(request.body):
                    responseData = json.loads(request.body)
                    for i in responseData['params']:
                        # print(i)
                        ManagementSopDevice.objects.get(id=i).files_Spec.all().delete()#删除实体文件 model中的files_SopRom_delete方法
                        ManagementSopDevice.objects.get(id=i).delete()
        # mock_data
        for i in ManagementSopRoom.objects.all().order_by(F('Num')):#.desc()從大到小
            filelist = []
            for h in i.files_Spec.all():
                filelist.append("/media/" + str(h.files))
            mock_data.append({
                "id": i.id, "No": i.Num, "Title": i.Title, "Description": i.Description,
                "Version": i.Version,
                "Upload_Date": i.edit_time, "file": filelist,
                "Ownerflag": 1 if request.session.get('account') == i.editor else 0,
                "editor": i.editor
            })
        for i in ManagementSopProcess.objects.all().order_by(F('Num')):
            filelist = []
            for h in i.files_Spec.all():
                filelist.append("/media/" + str(h.files))
            mock_data1.append({
                "id": i.id, "No": i.Num, "Title": i.Title, "Description": i.Description,
                "Version": i.Version,
                "Upload_Date": i.edit_time, "file": filelist,
                "Ownerflag": 1 if request.session.get('account') == i.editor else 0,
                "editor": i.editor
            })
        for i in ManagementSopDevice.objects.all().order_by(F('Num')):
            filelist = []
            for h in i.files_Spec.all():
                filelist.append("/media/" + str(h.files))
            mock_data2.append({
                "id": i.id, "No": i.Num, "Title": i.Title, "Description": i.Description,
                "Version": i.Version,
                "Upload_Date": i.edit_time, "file": filelist,
                "Ownerflag": 1 if request.session.get('account') == i.editor else 0,
                "editor": i.editor
            })
        data = {
            "content": mock_data,
            "content1": mock_data1,
            "content2": mock_data2,
            "errMessage": errMessage,
            "addPermission": addPermission,
            "deletePermission": deletePermission,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'SpecDownload/ManagementSop_Summary.html', locals())
