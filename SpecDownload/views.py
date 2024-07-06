from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime,json,simplejson,requests,time
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import files_SpecD, SpecDownload
from app01.models import UserInfo
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
                SpecDownloads.editor = request.session.get('user_name')
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
                        "Version": i.Version, "file": filelist
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist
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
                    "Version": i.Version, "file": filelist
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
            id = request.POST.get("ID")
            updateSpecdic = {"Customer": Customer, "Category": Category, "Functionn": Functionn, "Case_name": Case_name,
                            "Version": Version, }
            SpecDownload.objects.filter(id=id).update(**updateSpecdic)
            if Customersearch and Categorysearch and Functionnsearch:
                searchdic = {"Customer": Customersearch, "Category": Categorysearch, "Functionn": Functionnsearch,}
                for i in SpecDownload.objects.filter(**searchdic):
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn, "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist
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
                        "Version": i.Version, "file": filelist
                    })
            else:
                for i in SpecDownload.objects.all():
                    filelist = []
                    for h in i.files_Spec.all():
                        filelist.append("/media/" + str(h.files))
                    mock_data.append({
                        "id": i.id, "Customer": i.Customer, "Category": i.Category, "Fc": i.Functionn,
                        "Case_name": i.Case_name,
                        "Version": i.Version, "file": filelist
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
