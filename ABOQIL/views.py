from django.shortcuts import render, redirect, HttpResponse
from ABOQIL.forms import ABOQIL_F
from ABOQIL.models import ABOQIL_M, ABOQIL_Project, files_ABOQIL
from ABOProjectLessonL.models import ABOTestProjectLL
import datetime, json
from django.views.decorators.csrf import csrf_exempt
from app01.models import ProjectinfoinDCT, UserInfo


# Create your views here.
@csrf_exempt
def ABOQIL_add(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "ABOQIL/Add"
    ABOQIL_upload = ABOQIL_F(request.POST)
    if request.method == "POST":
        ABOQILlesson = ABOQIL_F(request.POST)
        if 'Upload' in request.POST:
            # test = request.POST.get('test')
            # print(test)
            if ABOQILlesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                # print(ABOQILlesson.cleaned_data)
                Product = ABOQILlesson.cleaned_data['Product']
                Customer = ABOQILlesson.cleaned_data['Customer']
                QIL_No = ABOQILlesson.cleaned_data['QIL_No']
                Issue_Description = ABOQILlesson.cleaned_data['Issue_Description']
                Root_Cause = ABOQILlesson.cleaned_data['Root_Cause']
                Status = ABOQILlesson.cleaned_data['Status']
                Creator = ABOQILlesson.cleaned_data['Creator']
                Created_On = ABOQILlesson.cleaned_data['Created_On']
                file = request.FILES.getlist("myfiles", "")
                # print(file)
                ABOQIL_No_check = ABOQIL_M.objects.filter(ABOQIL_No=QIL_No)

                # print (Object_check,Symptom_check)
                # if Object_check:
                #     #message = "Object '%s' already exists" % (Object)
                #     message_err=1
                #     return render(request, 'Lesson_upload.html',locals())
                # else:
                if ABOQIL_No_check:
                    # message = "Symptom '%s' already exists" % (Symptom)
                    # message_err = 1
                    result = 1
                    return render(request, 'ABOQIL/ABOQIL_upload.html', locals())
                else:
                    # Photos=''
                    # for image in Photo:
                    #     # print (image.name)
                    #     if not Photos:
                    #         Photos='img/test/'+image.name
                    #     else:
                    #         Photos=Photos+','+'img/test/'+image.name
                    # print (Photos)
                    ABOQIL = ABOQIL_M()
                    ABOQIL.Product = Product
                    ABOQIL.Customer = Customer
                    ABOQIL.ABOQIL_No = QIL_No
                    ABOQIL.Issue_Description = Issue_Description
                    ABOQIL.Root_Cause = Root_Cause
                    ABOQIL.Status = Status
                    ABOQIL.ABOQIL_No_check = ABOQIL_No_check
                    ABOQIL.Creator = Creator
                    ABOQIL.Created_On = Created_On
                    # lesson.Photo=Photos
                    ABOQIL.editor = request.session.get('user_name')
                    ABOQIL.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ABOQIL.save()
                    for f in request.FILES.getlist('myfiles'):
                        # print(f)
                        empt = files_ABOQIL()
                        # 增加其他字段应分别对应填写
                        empt.single = f
                        empt.files = f
                        empt.save()
                        ABOQIL.files_ABOQIL.add(empt)
                    result = 0
                    # message = "Upload '%s' Successfully" %(ABOQIL_No)

                    # print (lessonlearn())
                    # print(lessonlearn(request.POST))
                    # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                    return render(request, 'ABOQIL/ABOQIL_upload.html', locals())
            else:
                cleanData = ABOQILlesson.errors
                # print(lesson.errors)

    return render(request, 'ABOQIL/ABOQIL_upload.html', locals())


@csrf_exempt
def ABOQIL_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "ABOQIL/Edit"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "ABOQIL_No": "435tyh", "Issue_Description": "weartsyd",
        #  "Root_Cause": "rydtufjkg", "Status": "rtsyduj", "Creator": "", "Created_On": "2020.3.4"},
    ]
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if i == 'admin':
            # editPpriority = 4
            canExport = 1
        elif i == 'DQA_director':
            canExport = 1
    for i in ABOQIL_M.objects.all().values('Customer').distinct().order_by('Customer'):
        select.append(i['Customer'])
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get('isGetData') == 'first':
            data = {
                'select': select
            }
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            # print(Customer)
            if Customer:
                checkresult = ABOQIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = ABOQIL_M.objects.all()
            for i in checkresult:
                file_ABOQILlist = []
                # print(i.file_P.all)
                for j in i.files_ABOQIL.all():
                    file_ABOQILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.ABOQIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status,
                     "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_ABOQILlist},
                )
        if 'SAVE' in str(request.body):
            resdatas = json.loads(request.body)
            # print(resdatas)
            resdata = resdatas['rows']
            Customer = resdatas['Customer']
            # print(resdata)
            id = resdata['ID']
            updatadata = {
                "Product": resdata['Product'], "Customer": resdata['Customer'], "ABOQIL_No": resdata['ABOQIL_No'],
                "Issue_Description": resdata['Issue_Description'], "Root_Cause": resdata['Root_Cause'],
                "Status": resdata['Status'], "Creator": resdata['Creator'], "Created_On": resdata['Created_On'],
            }
            ABOQIL_M.objects.filter(id=id).update(**updatadata)
            if Customer:
                checkresult = ABOQIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = ABOQIL_M.objects.all()
            for i in checkresult:
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.ABOQIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status,
                     "Creator": i.Creator,
                     "Created_On": i.Created_On},
                )

        data = {
            'select': select,
            'content': mock_data,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'ABOQIL/ABOQIL_search.html', locals())


@csrf_exempt
def ABOQIL_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "ABOQIL/Edit"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "ABOQIL_No": "435tyh", "Issue_Description": "weartsyd",
        #  "Root_Cause": "rydtufjkg", "Status": "rtsyduj", "Creator": "", "Created_On": "2020.3.4"},
    ]
    for i in ABOQIL_M.objects.all().values('Customer').distinct().order_by('Customer'):
        select.append(i['Customer'])
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get('isGetData') == 'first':
            data = {
                'select': select
            }
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            # print(Customer)
            if Customer:
                checkresult = ABOQIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = ABOQIL_M.objects.all()
            for i in checkresult:
                file_ABOQILlist = []
                # print(i.file_P.all)
                for j in i.files_ABOQIL.all():
                    file_ABOQILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.ABOQIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status,
                     "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_ABOQILlist},
                )
        if request.POST.get('isGetData') == 'SAVE':
            # print('1')
            id = request.POST.get('ID')
            searchcustomer = request.POST.get('serchCategory')
            filelist = request.FILES.getlist("fileList", "")
            updatadata = {
                "Product": request.POST.get('Product'), "Customer": request.POST.get('Customer'),
                "ABOQIL_No": request.POST.get('QIL_No'),
                "Issue_Description": request.POST.get('Issue_Description'),
                "Root_Cause": request.POST.get('Root_Cause'),
                "Status": request.POST.get('Status'), "Creator": request.POST.get('Creator'),
                "Created_On": request.POST.get('Created_On'),
            }
            ABOQIL_M.objects.filter(id=id).update(**updatadata)
            if filelist:
                for f in filelist:
                    # print(f)
                    empt = files_ABOQIL()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.files = f
                    empt.save()
                    ABOQIL_M.objects.get(id=id).files_ABOQIL.add(empt)
            if searchcustomer:
                checkresult = ABOQIL_M.objects.filter(Customer=searchcustomer)
            else:
                checkresult = ABOQIL_M.objects.all()
            for i in checkresult:
                file_ABOQILlist = []
                # print(i.file_P.all)
                for j in i.files_ABOQIL.all():
                    file_ABOQILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.ABOQIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status,
                     "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_ABOQILlist},
                )
        # if 'SAVE' in str(request.body):
        #     resdatas = json.loads(request.body)
        #     # print(resdatas)
        #     resdata = resdatas['rows']
        #     Customer = resdatas['Customer']
        #     # print(resdata)
        #     id = resdata['ID']
        #     updatadata = {
        #         "Product": resdata['Product'], "Customer": resdata['Customer'], "ABOQIL_No": resdata['ABOQIL_No'],
        #         "Issue_Description": resdata['Issue_Description'], "Root_Cause": resdata['Root_Cause'],
        #         "Status": resdata['Status'], "Creator": resdata['Creator'], "Created_On": resdata['Created_On'],
        #     }
        #     ABOQIL_M.objects.filter(id=id).update(**updatadata)
        #     if Customer:
        #         checkresult = ABOQIL_M.objects.filter(Customer=Customer)
        #     else:
        #         checkresult = ABOQIL_M.objects.all()
        #     for i in checkresult:
        #         file_ABOQILlist = []
        #         # print(i.file_P.all)
        #         for j in i.files_ABOQIL.all():
        #             file_ABOQILlist.append("/media/" + str(j.files))
        #         # print(i)
        #         mock_data.append(
        #             {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "ABOQIL_No": i.ABOQIL_No,
        #              "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
        #              "Created_On": i.Created_On, "file": file_ABOQILlist},
        #         )

        data = {
            'select': select,
            'content': mock_data
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'ABOQIL/ABOQIL_edit.html', locals())


@csrf_exempt
def ABOQIL_projectresult(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "ABOQIL/ProjectResult"
    canEdit = 0
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "ABOQIL_No": "435tyh", "Issue_Description": "weartsyd",
        #  "Root_Cause": "rydtufjkg", "Status": "rtsyduj", "Result": "sdfgh", "Comments": "wergthygrf", "Creator": "",
        #  "Created_On": "2020.3.4"},
        # {"ID": "2", "Product": "wrgtrb", "Customer": "3454tyhy", "ABOQIL_No": "htgr", "Issue_Description": "erytiu",
        #  "Root_Cause": "rtsyhdujf", "Status": "wertgh", "Result": "aregstd", "Comments": "ngfxb", "Creator": "",
        #  "Created_On": "2001.10.7"},
    ]
    selectItem = {
        # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
        # "C38(AIO)": ["EL535", "EL536", "EL537", "EL538"],
        # "A39": ["EL531", "EL532", "EL533", "EL534"],
        # "Other": ["ELMV2", "ELMV3", "ELMV4"]
    }

    for i in ABOTestProjectLL.objects.all().values('Customer').distinct().order_by('Customer'):
        projectlist = []
        for j in ABOTestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get('isGetData') == 'first':
            data = {
                'selectItem': selectItem
            }
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            dic_Project = {'Customer': Customer, 'Project': Project}

            # print(dic_Project)
            if Project and Customer:
                Projectinfos = ABOTestProjectLL.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                canEdit = 0
                current_user = request.session.get('user_name')
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                # print(canEdit)
                if canEdit:
                    ABOQILlist = []
                    for i in ABOQIL_M.objects.all():  # for i in ABOQIL_M.objects.filter(Customer=Customer)每个机种只创建本客户别的issue
                        ABOQILlist.append(i.id)
                    # print (Lessonlist)
                    existABOQIL = []
                    for i in Projectinfos.aboqil_project_set.all():
                        # print(i)
                        existABOQIL.append(i.ABOQIL.id)
                    # print(existlesson)
                    for i in ABOQILlist:
                        if i in existABOQIL:
                            continue
                        else:
                            ABOQIL_Project.objects.create(ABOQIL=ABOQIL_M.objects.get(id=i),
                                                          Projectinfo=ABOTestProjectLL.objects.filter(
                                                              **dic_Project).first())
                if Projectinfos.aboqil_project_set.all():
                    for i in Projectinfos.aboqil_project_set.all().order_by('id'):
                        ABOQILProjectinfo = {}
                        ABOQILProjectinfo['ID'] = i.id
                        ABOQILProjectinfo['Product'] = i.ABOQIL.Product
                        ABOQILProjectinfo['Customer'] = i.ABOQIL.Customer
                        ABOQILProjectinfo['QIL_No'] = i.ABOQIL.ABOQIL_No
                        ABOQILProjectinfo['Issue_Description'] = i.ABOQIL.Issue_Description
                        ABOQILProjectinfo['Root_Cause'] = i.ABOQIL.Root_Cause
                        ABOQILProjectinfo['Status'] = i.ABOQIL.Status
                        ABOQILProjectinfo['Creator'] = i.ABOQIL.Creator
                        ABOQILProjectinfo['Created_On'] = i.ABOQIL.Created_On
                        filelist = []
                        for j in i.ABOQIL.files_ABOQIL.all():
                            filelist.append("/media/" + str(j.files))
                        ABOQILProjectinfo['file'] = filelist
                        ABOQILProjectinfo['Result'] = i.result
                        ABOQILProjectinfo['Comments'] = i.Comment
                        mock_data.append(ABOQILProjectinfo)
        if 'SAVE' in str(request.body):
            resdatas = json.loads(request.body)
            Customer = resdatas["Customer"]
            Project = resdatas["Project"]
            rows = resdatas["rows"]
            # print(rows)
            id = rows["ID"]
            dic_Project = {'Customer': Customer, 'Project': Project}
            Projectinfos = ABOTestProjectLL.objects.filter(**dic_Project).first()
            try:
                editplan = ABOQIL_Project.objects.filter(id=id).first()
                # print(type(editplan), editplan.ABOQIL.ABOQIL_No, rows["Result"])
                editplan.result = rows["Result"]
                editplan.Comment = rows["Comments"]
                editplan.editor = request.session.get('user_name')
                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                editplan.save()
                Content = "保存成功"
            except:
                msg = 401
                Content = "保存失败,请检查网络并重新尝试保存"
            if Projectinfos.aboqil_project_set.all():
                for i in Projectinfos.aboqil_project_set.all().order_by('id'):
                    ABOQILProjectinfo = {}
                    ABOQILProjectinfo['ID'] = i.id
                    ABOQILProjectinfo['Product'] = i.ABOQIL.Product
                    ABOQILProjectinfo['Customer'] = i.ABOQIL.Customer
                    ABOQILProjectinfo['QIL_No'] = i.ABOQIL.ABOQIL_No
                    ABOQILProjectinfo['Issue_Description'] = i.ABOQIL.Issue_Description
                    ABOQILProjectinfo['Root_Cause'] = i.ABOQIL.Root_Cause
                    ABOQILProjectinfo['Status'] = i.ABOQIL.Status
                    ABOQILProjectinfo['Creator'] = i.ABOQIL.Creator
                    ABOQILProjectinfo['Created_On'] = i.ABOQIL.Created_On
                    filelist = []
                    for j in i.ABOQIL.files_ABOQIL.all():
                        filelist.append("/media/" + str(j.files))
                    ABOQILProjectinfo['file'] = filelist
                    ABOQILProjectinfo['Result'] = i.result
                    ABOQILProjectinfo['Comments'] = i.Comment
                    mock_data.append(ABOQILProjectinfo)
        data = {
            "err_ok": "0",
            "canEdit": canEdit,
            "content": mock_data,
            "select": selectItem,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'ABOQIL/ABOQIL_ProjectResult.html', locals())


@csrf_exempt
def ABOQIL_searchbyproject(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "ABOQIL/SearchByProject"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "ABOQIL_No": "435tyh", "Issue_Description": "weartsyd","Root_Cause": "rydtufjkg", "Status": "rtsyduj",
        #  "Project": [{"projectName": "FL4C4", "result": "580","comment": "580"}, {"projectName": "FL4E1", "result": "155","comment": "580"},
        #             {"projectName": "FL5C1", "result": "60","comment": "580"}, {"projectName": "EL445", "result": "61","comment": "580"}],
        #  "Creator": "", "Created_On": "2020.3.4"},
        # {"ID": "2", "Product": "wrgtrb", "Customer": "3454tyhy", "ABOQIL_No": "htgr", "Issue_Description": "erytiu","Root_Cause": "rtsyhdujf", "Status": "wertgh",
        #  "Project": [{"projectName": "FL4C4", "result": "580","comment": "580"}, {"projectName": "FL4E1", "result": "155","comment": "580"},
        #             {"projectName": "FL5C1", "result": "60","comment": "580"}, {"projectName": "EL445", "result": "61","comment": "580"}],
        #  "Creator": "", "Created_On": "2001.10.7"},
    ]
    projectMsg = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus","PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD","PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青","DQA PL": "张亚萍"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMS0", "CUSPRJCODE": "Taurus","PROJECT": "IdeaPad5 14IIL05 Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "Intel","PLATFORM": "Intel Ice Lake-U", "VGA": "NV N175-G3 NV N175-G5 UMA", "OS SUPPORT": "WIN10 19H2","SS": "2020-01-17", "LD": "王青", "DQA PL": "张亚萍"},
    ]
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if i == 'admin':
            # editPpriority = 4
            canExport = 1
        elif i == 'DQA_director':
            canExport = 1
    for i in ABOTestProjectLL.objects.all().values('Customer').distinct().order_by('Customer'):
        select.append(i['Customer'])
    if request.method == "POST":
        # print(request.POST)
        if request.POST.get('isGetData') == 'first':
            data = {
                'select': select
            }
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in ABOTestProjectLL.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append(i["Project"])
            else:
                for i in ABOTestProjectLL.objects.all().values("Project").distinct().order_by("Project"):
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
        if request.POST.get("action") == "getMsg":
            Customer = request.POST.get('customer')
            Projectlist = request.POST.getlist("projectMsg", [])

            for i in ABOQIL_M.objects.all():
                projectresult = []
                for j in Projectlist:
                    # print(j)
                    if Customer:
                        dic_Project = {'Customer': Customer, 'Project': j}
                    else:
                        dic_Project = {'Project': j}
                    Projectinfos = ABOTestProjectLL.objects.filter(**dic_Project).first()
                    ABOQIL_Projectinfo = ABOQIL_Project.objects.filter(ABOQIL=i.id, Projectinfo=Projectinfos).first()
                    if ABOQIL_Projectinfo:

                        # print(type(lessonlearn_Project.objects.filter(lesson=i.id,
                        #                                Projectinfo=Projectinfos)),type(lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                        projectresult.append({"projectName": j, "result": ABOQIL_Projectinfo.result,
                                              "comment": ABOQIL_Projectinfo.Comment})
                    else:  # 占位，否则结果会错位
                        projectresult.append({"projectname": j, "result": '',
                                              "comment": ''})
                # print(projectresult)
                filelist = []
                for j in i.files_ABOQIL.all():
                    filelist.append("/media/" + str(j.files))

                mock_data.append(
                    {
                        "ID": i.id,
                        "Product": i.Product,
                        "Customer": i.Customer,
                        "QIL_No": i.ABOQIL_No,
                        "Issue_Description": i.Issue_Description,
                        "Root_Cause": i.Root_Cause,
                        "Status": i.Status,
                        "Creator": i.Creator,
                        "Created_On": i.Created_On,
                        "file": filelist,
                        "Project": projectresult,
                    },
                )

        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": select,
            "searchalert": projectMsg,
            'canExport': canExport,
        }

        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'ABOQIL/ABOQIL_searchbyproject.html', locals())
