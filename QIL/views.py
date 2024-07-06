from django.shortcuts import render,redirect,HttpResponse
from QIL.forms import QIL_F
from QIL.models import QIL_M, QIL_Project, files_QIL
from LessonProjectME.models import TestProjectLL
import datetime, json
from django.views.decorators.csrf import csrf_exempt
from app01.models import ProjectinfoinDCT, UserInfo

# Create your views here.
@csrf_exempt
def QIL_add(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "QIL/Add"
    QIL_upload = QIL_F(request.POST)
    if request.method == "POST":
        QILlesson=QIL_F(request.POST)
        if 'Upload' in request.POST:
            # test = request.POST.get('test')
            # print(test)
            if QILlesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                Product = QILlesson.cleaned_data['Product']
                Customer = QILlesson.cleaned_data['Customer']
                QIL_No = QILlesson.cleaned_data['QIL_No']
                Issue_Description = QILlesson.cleaned_data['Issue_Description']
                Root_Cause = QILlesson.cleaned_data['Root_Cause']
                Status = QILlesson.cleaned_data['Status']
                Creator = QILlesson.cleaned_data['Creator']
                Created_On = QILlesson.cleaned_data['Created_On']
                file = request.FILES.getlist("myfiles", "")
                # print(file)
                QIL_No_check =QIL_M.objects.filter(QIL_No=QIL_No)

                # print (Object_check,Symptom_check)
                # if Object_check:
                #     #message = "Object '%s' already exists" % (Object)
                #     message_err=1
                #     return render(request, 'Lesson_upload.html',locals())
                # else:
                if QIL_No_check:
                    #message = "Symptom '%s' already exists" % (Symptom)
                    # message_err = 1
                    result = 1
                    return render(request, 'QIL/QIL_upload.html', locals())
                else:
                    # Photos=''
                    # for image in Photo:
                    #     # print (image.name)
                    #     if not Photos:
                    #         Photos='img/test/'+image.name
                    #     else:
                    #         Photos=Photos+','+'img/test/'+image.name
                    # print (Photos)
                    QIL = QIL_M()
                    QIL.Product = Product
                    QIL.Customer = Customer
                    QIL.QIL_No = QIL_No
                    QIL.Issue_Description = Issue_Description
                    QIL.Root_Cause = Root_Cause
                    QIL.Status = Status
                    QIL.QIL_No_check = QIL_No_check
                    QIL.Creator = Creator
                    QIL.Created_On = Created_On
                    # lesson.Photo=Photos
                    QIL.editor = request.session.get('user_name')
                    QIL.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    QIL.save()
                    for f in request.FILES.getlist('myfiles'):
                        # print(f)
                        empt = files_QIL()
                        # 增加其他字段应分别对应填写
                        empt.single = f
                        empt.files = f
                        empt.save()
                        QIL.files_QIL.add(empt)
                    result = 0
                    # message = "Upload '%s' Successfully" %(QIL_No)

                    # print (lessonlearn())
                    # print(lessonlearn(request.POST))
                    # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                    return render(request, 'QIL/QIL_upload.html', locals())
            else:
                cleanData = QILlesson.errors
                # print(lesson.errors)

    return render(request, 'QIL/QIL_upload.html', locals())

@csrf_exempt
def QIL_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "QIL/Edit"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "QIL_No": "435tyh", "Issue_Description": "weartsyd",
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
    for i in QIL_M.objects.all().values('Customer').distinct().order_by('Customer'):
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
                checkresult = QIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = QIL_M.objects.all()
            for i in checkresult:
                file_QILlist = []
                # print(i.file_P.all)
                for j in i.files_QIL.all():
                    file_QILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.QIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_QILlist},
                )
        if 'SAVE' in str(request.body):
            resdatas = json.loads(request.body)
            # print(resdatas)
            resdata = resdatas['rows']
            Customer = resdatas['Customer']
            # print(resdata)
            id = resdata['ID']
            updatadata = {
                "Product": resdata['Product'], "Customer": resdata['Customer'], "QIL_No": resdata['QIL_No'],
                "Issue_Description": resdata['Issue_Description'], "Root_Cause": resdata['Root_Cause'],
                "Status": resdata['Status'], "Creator": resdata['Creator'], "Created_On": resdata['Created_On'],
            }
            QIL_M.objects.filter(id=id).update(**updatadata)
            if Customer:
                checkresult = QIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = QIL_M.objects.all()
            for i in checkresult:
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.QIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
                     "Created_On": i.Created_On},
                )

        data = {
            'select': select,
            'content': mock_data,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'QIL/QIL_search.html', locals())

@csrf_exempt
def QIL_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "QIL/Edit"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "QIL_No": "435tyh", "Issue_Description": "weartsyd",
        #  "Root_Cause": "rydtufjkg", "Status": "rtsyduj", "Creator": "", "Created_On": "2020.3.4"},
    ]
    for i in QIL_M.objects.all().values('Customer').distinct().order_by('Customer'):
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
                checkresult = QIL_M.objects.filter(Customer=Customer)
            else:
                checkresult = QIL_M.objects.all()
            for i in checkresult:
                file_QILlist = []
                # print(i.file_P.all)
                for j in i.files_QIL.all():
                    file_QILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.QIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_QILlist},
                )
        if request.POST.get('isGetData') == 'SAVE':
            # print('1')
            id = request.POST.get('ID')
            searchcustomer = request.POST.get('serchCategory')
            filelist = request.FILES.getlist("fileList", "")
            updatadata = {
                        "Product": request.POST.get('Product'), "Customer": request.POST.get('Customer'), "QIL_No": request.POST.get('QIL_No'),
                        "Issue_Description": request.POST.get('Issue_Description'), "Root_Cause": request.POST.get('Root_Cause'),
                        "Status": request.POST.get('Status'), "Creator": request.POST.get('Creator'), "Created_On": request.POST.get('Created_On'),
                    }
            QIL_M.objects.filter(id=id).update(**updatadata)
            if filelist:
                for f in filelist:
                    # print(f)
                    empt = files_QIL()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.files = f
                    empt.save()
                    QIL_M.objects.get(id=id).files_QIL.add(empt)
            if searchcustomer:
                checkresult = QIL_M.objects.filter(Customer=searchcustomer)
            else:
                checkresult = QIL_M.objects.all()
            for i in checkresult:
                file_QILlist = []
                # print(i.file_P.all)
                for j in i.files_QIL.all():
                    file_QILlist.append("/media/" + str(j.files))
                # print(i)
                mock_data.append(
                    {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.QIL_No,
                     "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
                     "Created_On": i.Created_On, "file": file_QILlist},
                )
        # if 'SAVE' in str(request.body):
        #     resdatas = json.loads(request.body)
        #     # print(resdatas)
        #     resdata = resdatas['rows']
        #     Customer = resdatas['Customer']
        #     # print(resdata)
        #     id = resdata['ID']
        #     updatadata = {
        #         "Product": resdata['Product'], "Customer": resdata['Customer'], "QIL_No": resdata['QIL_No'],
        #         "Issue_Description": resdata['Issue_Description'], "Root_Cause": resdata['Root_Cause'],
        #         "Status": resdata['Status'], "Creator": resdata['Creator'], "Created_On": resdata['Created_On'],
        #     }
        #     QIL_M.objects.filter(id=id).update(**updatadata)
        #     if Customer:
        #         checkresult = QIL_M.objects.filter(Customer=Customer)
        #     else:
        #         checkresult = QIL_M.objects.all()
        #     for i in checkresult:
        #         file_QILlist = []
        #         # print(i.file_P.all)
        #         for j in i.files_QIL.all():
        #             file_QILlist.append("/media/" + str(j.files))
        #         # print(i)
        #         mock_data.append(
        #             {"ID": i.id, "Product": i.Product, "Customer": i.Customer, "QIL_No": i.QIL_No,
        #              "Issue_Description": i.Issue_Description, "Root_Cause": i.Root_Cause, "Status": i.Status, "Creator": i.Creator,
        #              "Created_On": i.Created_On, "file": file_QILlist},
        #         )

        data = {
            'select': select,
            'content': mock_data
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'QIL/QIL_edit.html', locals())

@csrf_exempt
def QIL_projectresult(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "QIL/ProjectResult"
    canEdit = 0
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "QIL_No": "435tyh", "Issue_Description": "weartsyd",
        #  "Root_Cause": "rydtufjkg", "Status": "rtsyduj", "Result": "sdfgh", "Comments": "wergthygrf", "Creator": "",
        #  "Created_On": "2020.3.4"},
        # {"ID": "2", "Product": "wrgtrb", "Customer": "3454tyhy", "QIL_No": "htgr", "Issue_Description": "erytiu",
        #  "Root_Cause": "rtsyhdujf", "Status": "wertgh", "Result": "aregstd", "Comments": "ngfxb", "Creator": "",
        #  "Created_On": "2001.10.7"},
    ]
    selectItem = {
        # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
        # "C38(AIO)": ["EL535", "EL536", "EL537", "EL538"],
        # "A39": ["EL531", "EL532", "EL533", "EL534"],
        # "Other": ["ELMV2", "ELMV3", "ELMV4"]
    }


    for i in TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer'):
        projectlist = []
        for j in TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
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
                Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
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
                    QILlist = []
                    for i in QIL_M.objects.all():#for i in QIL_M.objects.filter(Customer=Customer)每个机种只创建本客户别的issue
                        QILlist.append(i.id)
                    # print (Lessonlist)
                    existQIL = []
                    for i in Projectinfos.qil_project_set.all():
                        # print(i)
                        existQIL.append(i.QIL.id)
                    # print(existlesson)
                    for i in QILlist:
                        if i in existQIL:
                            continue
                        else:
                            QIL_Project.objects.create(QIL=QIL_M.objects.get(id=i),
                                                      Projectinfo=TestProjectLL.objects.filter(**dic_Project).first())
                if Projectinfos.qil_project_set.all():
                    for i in Projectinfos.qil_project_set.all().order_by('id'):
                        QILProjectinfo = {}
                        QILProjectinfo['ID'] = i.id
                        QILProjectinfo['Product'] = i.QIL.Product
                        QILProjectinfo['Customer'] = i.QIL.Customer
                        QILProjectinfo['QIL_No'] = i.QIL.QIL_No
                        QILProjectinfo['Issue_Description'] = i.QIL.Issue_Description
                        QILProjectinfo['Root_Cause'] = i.QIL.Root_Cause
                        QILProjectinfo['Status'] = i.QIL.Status
                        QILProjectinfo['Creator'] = i.QIL.Creator
                        QILProjectinfo['Created_On'] = i.QIL.Created_On
                        filelist = []
                        for j in i.QIL.files_QIL.all():
                            filelist.append("/media/" + str(j.files))
                        QILProjectinfo['file'] = filelist
                        QILProjectinfo['Result'] = i.result
                        QILProjectinfo['Comments'] = i.Comment
                        mock_data.append(QILProjectinfo)
        if 'SAVE' in str(request.body):
            resdatas = json.loads(request.body)
            Customer = resdatas["Customer"]
            Project = resdatas["Project"]
            rows = resdatas["rows"]
            # print(rows)
            id = rows["ID"]
            dic_Project = {'Customer': Customer, 'Project': Project}
            Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
            try:
                editplan = QIL_Project.objects.filter(id=id).first()
                # print(type(editplan), editplan.QIL.QIL_No, rows["Result"])
                editplan.result = rows["Result"]
                editplan.Comment = rows["Comments"]
                editplan.editor = request.session.get('user_name')
                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                editplan.save()
                Content = "保存成功"
            except:
                msg = 401
                Content = "保存失败,请检查网络并重新尝试保存"
            if Projectinfos.qil_project_set.all():
                for i in Projectinfos.qil_project_set.all().order_by('id'):
                    QILProjectinfo = {}
                    QILProjectinfo['ID'] = i.id
                    QILProjectinfo['Product'] = i.QIL.Product
                    QILProjectinfo['Customer'] = i.QIL.Customer
                    QILProjectinfo['QIL_No'] = i.QIL.QIL_No
                    QILProjectinfo['Issue_Description'] = i.QIL.Issue_Description
                    QILProjectinfo['Root_Cause'] = i.QIL.Root_Cause
                    QILProjectinfo['Status'] = i.QIL.Status
                    QILProjectinfo['Creator'] = i.QIL.Creator
                    QILProjectinfo['Created_On'] = i.QIL.Created_On
                    filelist = []
                    for j in i.QIL.files_QIL.all():
                        filelist.append("/media/" + str(j.files))
                    QILProjectinfo['file'] = filelist
                    QILProjectinfo['Result'] = i.result
                    QILProjectinfo['Comments'] = i.Comment
                    mock_data.append(QILProjectinfo)
        data = {
            "err_ok": "0",
            "canEdit": canEdit,
            "content": mock_data,
            "select": selectItem,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'QIL/QIL_ProjectResult.html', locals())

@csrf_exempt
def QIL_searchbyproject(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "QIL/SearchByProject"
    select = []
    mock_data = [
        # {"ID": "1", "Product": "sdfg", "Customer": "tr", "QIL_No": "435tyh", "Issue_Description": "weartsyd","Root_Cause": "rydtufjkg", "Status": "rtsyduj",
        #  "Project": [{"projectName": "FL4C4", "result": "580","comment": "580"}, {"projectName": "FL4E1", "result": "155","comment": "580"},
        #             {"projectName": "FL5C1", "result": "60","comment": "580"}, {"projectName": "EL445", "result": "61","comment": "580"}],
        #  "Creator": "", "Created_On": "2020.3.4"},
        # {"ID": "2", "Product": "wrgtrb", "Customer": "3454tyhy", "QIL_No": "htgr", "Issue_Description": "erytiu","Root_Cause": "rtsyhdujf", "Status": "wertgh",
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
    for i in TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer'):
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
                for i in TestProjectLL.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append(i["Project"])
            else:
                for i in TestProjectLL.objects.all().values("Project").distinct().order_by("Project"):
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

            for i in QIL_M.objects.all():
                projectresult = []
                for j in Projectlist:
                    # print(j)
                    if Customer:
                        dic_Project = {'Customer': Customer, 'Project': j}
                    else:
                        dic_Project = {'Project': j}
                    Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
                    QIL_Projectinfo = QIL_Project.objects.filter(QIL=i.id, Projectinfo=Projectinfos).first()
                    if QIL_Projectinfo:

                    # print(type(lessonlearn_Project.objects.filter(lesson=i.id,
                    #                                Projectinfo=Projectinfos)),type(lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                        projectresult.append({"projectName": j, "result": QIL_Projectinfo.result, "comment": QIL_Projectinfo.Comment})
                    else:  # 占位，否则结果会错位
                        projectresult.append({"projectname": j, "result": '',
                                              "comment": ''})
                # print(projectresult)
                filelist = []
                for j in i.files_QIL.all():
                    filelist.append("/media/" + str(j.files))

                mock_data.append(
                    {
                        "ID": i.id,
                        "Product": i.Product,
                        "Customer": i.Customer,
                        "QIL_No": i.QIL_No,
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


    return render(request, 'QIL/QIL_searchbyproject.html', locals())