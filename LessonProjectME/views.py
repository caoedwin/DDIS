from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from .models import lessonlearn_Project,TestProjectLL, UserInfo
from app01.models import lesson_learn,ProjectinfoinDCT

# from TestPlanME.models import TestProjectME
import datetime,os

import datetime,json
# Create your views here.
def Lesson_project(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="LessonProjectME/Edit"
    Lesson_list=lesson_learn.objects.all()
    canEdit = 0
    msg = 400
    mock_data = [
        # {
        #     "len_id": 100,
        #     "object": "elmv2",
        #     "symptom": "symptom1",
        #     "root_cause": "root_cause1",
        #     "solution": "solution1",
        #     "action": "action1",
        #     "photo": [imgSrcBase + "123456.png", imgSrcBase + "1234567.png"],
        #     "result": "Pass",
        #     "comment": "action=get&csrfmiddle",
        #     "canEdit": 1,
        # },
        ]
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    combine = {
        # "C38(NB)": [{"project": "ELMV2", "phase": [0, 1, 2, 3]}, {"project": "FLY00", "phase": [2, 3]},
        #             {"project": "ELZP5", "phase": [1]}, {"project": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"project": "FLMS0", "phase": [1, 2, 3]}, {"project": "FLMS1", "phase": [1, 2, 3]},
        #              {"project": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"project": "DLAE1", "phase": [1, 2, 3]}, {"project": "DLAE2", "phase": [1, 2, 3]},
        #         {"project": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"project": "OTHER", "phase": [1, 2, 3]}]
    }
    Customer_list = TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            # dic = {'Customer': i['Customer'], 'Project': j['Project']}
            # for m in TestProjectME.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):
            #
            #     if m['Phase'] == "B(FVT)":
            #         PhaseValue = 0
            #     if m['Phase'] == "C(SIT)":
            #         PhaseValue = 1
            #     if m['Phase'] == "INV":
            #         PhaseValue = 2
            #     if m['Phase'] == "Others":
            #         PhaseValue = 3
            #     phaselist.append
            # Projectinfo['phase'] = phaselist(PhaseValue)
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print(combine)
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    # print(str(request.body, encoding='utf-8'))
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("Category")
    for i in Categorylist:
        selectCategory.append({"Category": i['Category']})

    if request.method == "GET":
        if request.GET.get("action") == "get":
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
                'addselect': selectCategory,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        if request.GET.get("action") == "search":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Category = request.GET.get('Category')
            # Phase = request.GET.get('phase')
            # # print(type(Phase))
            # if Phase == '0':
            #     Phase = 'B(FVT)'
            # if Phase == '1':
            #     Phase = 'C(SIT)'
            # if Phase == '2':
            #     Phase = 'INV'
            # if Phase == '3':
            #     Phase = 'Others'


            dic_Project = {'Customer': Customer, 'Project': Project}

            # print(dic_Project)
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
                Lessonlist = []
                for i in lesson_learn.objects.filter(Status="active"):
                    Lessonlist.append(i.id)
                # print (Lessonlist)
                existlesson = []
                # print(Projectinfos.lessonlearn_project_set)
                for i in Projectinfos.lessonlearn_project_set.all():
                    # print(i)
                    existlesson.append(i.lesson.id)
                # print(existlesson)
                for i in Lessonlist:
                    if i in existlesson:
                        continue
                    else:
                        lessonlearn_Project.objects.create(lesson=lesson_learn.objects.get(id=i),
                                                  Projectinfo=TestProjectLL.objects.filter(**dic_Project).first())
            if Category:
                if Projectinfos.lessonlearn_project_set.filter(lesson__Category=Category):
                    for i in Projectinfos.lessonlearn_project_set.filter(lesson__Category=Category).order_by('id'):
                        LessonProjectinfo = {}
                        LessonProjectinfo['len_id'] = i.id
                        LessonProjectinfo['Category'] = i.lesson.Category
                        LessonProjectinfo['object'] = i.lesson.Object
                        LessonProjectinfo['symptom'] = i.lesson.Symptom
                        LessonProjectinfo['Reproduce_Steps'] = i.lesson.Reproduce_Steps
                        LessonProjectinfo['root_cause'] = i.lesson.Root_Cause
                        LessonProjectinfo['solution'] = i.lesson.Solution
                        LessonProjectinfo['action'] = i.lesson.Action
                        Photolist = []
                        filelist = []
                        # print(i.file_B.all)
                        for j in i.lesson.Photo.all():
                            if str(j.img).split(".")[1] == "jpg" or str(j.img).split(".")[1] == "png":
                                Photolist.append("/media/" + str(j.img))
                            else:
                                filelist.append("/media/" + str(j.img))
                        LessonProjectinfo['photo'] = Photolist
                        LessonProjectinfo['file'] = filelist
                        LessonProjectinfo['result'] = i.result
                        LessonProjectinfo['comment'] = i.Comment
                        mock_data.append(LessonProjectinfo)
            else:
                if Projectinfos.lessonlearn_project_set.all():
                    for i in Projectinfos.lessonlearn_project_set.all().order_by('id'):
                        LessonProjectinfo = {}
                        LessonProjectinfo['len_id'] = i.id
                        LessonProjectinfo['Category'] = i.lesson.Category
                        LessonProjectinfo['object'] = i.lesson.Object
                        LessonProjectinfo['symptom'] = i.lesson.Symptom
                        LessonProjectinfo['Reproduce_Steps'] = i.lesson.Reproduce_Steps
                        LessonProjectinfo['root_cause'] = i.lesson.Root_Cause
                        LessonProjectinfo['solution'] = i.lesson.Solution
                        LessonProjectinfo['action'] = i.lesson.Action
                        Photolist = []
                        filelist = []
                        # print(i.file_B.all)
                        for j in i.lesson.Photo.all():
                            if str(j.img).split(".")[1] == "jpg" or str(j.img).split(".")[1] == "png":
                                Photolist.append("/media/" + str(j.img))
                            else:
                                filelist.append("/media/" + str(j.img))
                        LessonProjectinfo['photo'] = Photolist
                        LessonProjectinfo['file'] = filelist
                        LessonProjectinfo['result'] = i.result
                        LessonProjectinfo['comment'] = i.Comment
                        mock_data.append(LessonProjectinfo)
            # print (mock_data)
            updateData = {
                'msg': msg,
                'canEdit': canEdit,
                "content": mock_data,
                "selectMsg": combine,
                'addselect': selectCategory,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")

    if request.method == "POST":
        # str(request.body, encoding='utf-8')
        # print (str(request.body, encoding='utf-8'))
        # print(json.loads(request.body))
        # responseData = json.loads(request.body)
        # print(responseData)
        # print(request.body)

        if request.POST.get("PostKey") == "Edit":
            # print(request.POST)
            dic_Project = {'Customer': request.POST.get("customer"),
                           'Project': request.POST.get("project")}
            Category = request.POST.get("Category")

            Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
            # learninfo = lesson_learn.objects.get(id=request.POST.get("lesson_id"))
            # editplan = lessonlearn_Project.objects.filter(lesson=learninfo, Projectinfo=Projectinfos).first()
            try:
                editplan = lessonlearn_Project.objects.filter(id=request.POST.get("lesson_id")).first()
                # print(type(editplan))
                editplan.result = request.POST.get("result")
                editplan.Comment = request.POST.get("comment")
                editplan.editor = request.session.get('user_name')
                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                editplan.save()
                Content = "保存成功"
            except:
                msg = 401
                Content = "保存失败,请检查网络并重新尝试保存"

            # print(dic_Project)
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
            if Category:
                Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
                for i in Projectinfos.lessonlearn_project_set.filter(lesson__Category=Category).order_by('id'):
                    LessonProjectinfo = {}
                    LessonProjectinfo['len_id'] = i.id
                    LessonProjectinfo['Category'] = i.lesson.Category
                    LessonProjectinfo['object'] = i.lesson.Object
                    LessonProjectinfo['symptom'] = i.lesson.Symptom
                    LessonProjectinfo['Reproduce_Steps'] = i.lesson.Reproduce_Steps
                    LessonProjectinfo['root_cause'] = i.lesson.Root_Cause
                    LessonProjectinfo['solution'] = i.lesson.Solution
                    LessonProjectinfo['action'] = i.lesson.Action
                    Photolist = []
                    filelist = []
                    # print(i.file_B.all)
                    for j in i.lesson.Photo.all():
                        if str(j.img).split(".")[1] == "jpg" or str(j.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(j.img))
                        else:
                            filelist.append("/media/" + str(j.img))
                    LessonProjectinfo['photo'] = Photolist
                    LessonProjectinfo['file'] = filelist
                    LessonProjectinfo['result'] = i.result
                    LessonProjectinfo['comment'] = i.Comment
                    mock_data.append(LessonProjectinfo)
            else:
                Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
                for i in Projectinfos.lessonlearn_project_set.all().order_by('id'):
                    LessonProjectinfo = {}
                    LessonProjectinfo['len_id'] = i.id
                    LessonProjectinfo['Category'] = i.lesson.Category
                    LessonProjectinfo['object'] = i.lesson.Object
                    LessonProjectinfo['symptom'] = i.lesson.Symptom
                    LessonProjectinfo['Reproduce_Steps'] = i.lesson.Reproduce_Steps
                    LessonProjectinfo['root_cause'] = i.lesson.Root_Cause
                    LessonProjectinfo['solution'] = i.lesson.Solution
                    LessonProjectinfo['action'] = i.lesson.Action
                    Photolist = []
                    filelist = []
                    # print(i.file_B.all)
                    for j in i.lesson.Photo.all():
                        if str(j.img).split(".")[1] == "jpg" or str(j.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(j.img))
                        else:
                            filelist.append("/media/" + str(j.img))
                    LessonProjectinfo['photo'] = Photolist
                    LessonProjectinfo['file'] = filelist
                    LessonProjectinfo['result'] = i.result
                    LessonProjectinfo['comment'] = i.Comment
                    mock_data.append(LessonProjectinfo)
            # print (mock_data)
            updateData = {
                'msg': msg,
                'canEdit': canEdit,
                "content": Content,
                # "MockData": mock_data,
                "selectMsg": combine,
                'addselect': selectCategory,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")

    return render(request, 'LessonProjectME/Lesson_result.html', locals())

def Lesson_project_Search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="LessonProjectME/ProjectResult"
    Lesson_list=lesson_learn.objects.all()
    mock_data = [
    ]
    projectMsg = [
        # {"YEAR": 2010, "COMPRJCODE": "EL4C2", "CUSPRJCODE": "TAURUS", "PROJECT": "LENOVO", "SIZE": 12, "CPU": "INTEL",
        #  "id": 201467},
        # {"YEAR": 2013, "COMPRJCODE": "EL4C4", "CUSPRJCODE": "TAURUS", "PROJECT": "LENOVO", "SIZE": 12,
        #  "CPU": "INTEL", "id": 201487},
        # {"YEAR": 2014, "COMPRJCODE": "EL4C5", "CUSPRJCODE": "TAURUS", "PROJECT": "LENOVO", "SIZE": 12,
        #  "CPU": "INTEL", "id": 201407},
    ]
    allResult = {
        'msg': 400,
        'content': projectMsg,
    }
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    combine = {
        # "C38(NB)": [{"project": "ELMV2", "phase": [0, 1, 2, 3]}, {"project": "FLY00", "phase": [2, 3]},
        #             {"project": "ELZP5", "phase": [1]}, {"project": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"project": "FLMS0", "phase": [1, 2, 3]}, {"project": "FLMS1", "phase": [1, 2, 3]},
        #              {"project": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"project": "DLAE1", "phase": [1, 2, 3]}, {"project": "DLAE2", "phase": [1, 2, 3]},
        #         {"project": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"project": "OTHER", "phase": [1, 2, 3]}]
    }
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
    Customer_list = TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            # dic = {'Customer': i['Customer'], 'Project': j['Project']}
            # for m in TestProjectME.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):
            #
            #     if m['Phase'] == "B(FVT)":
            #         PhaseValue = 0
            #     if m['Phase'] == "C(SIT)":
            #         PhaseValue = 1
            #     if m['Phase'] == "INV":
            #         PhaseValue = 2
            #     if m['Phase'] == "Others":
            #         PhaseValue = 3
            #     phaselist.append
            # Projectinfo['phase'] = phaselist(PhaseValue)
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    Customer_list = TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')
    Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("Category")
    for i in Categorylist:
        selectCategory.append({"Category": i['Category']})

    # for i in Customer_list:
    #     Customerlist = []
    #     for j in TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
    #         Projectinfo = {}
    #         phaselist = []
    #         # dic = {'Customer': i['Customer'], 'Project': j['Project']}
    #         # for m in TestProjectME.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):
    #         #
    #         #     if m['Phase'] == "B(FVT)":
    #         #         PhaseValue = 0
    #         #     if m['Phase'] == "C(SIT)":
    #         #         PhaseValue = 1
    #         #     if m['Phase'] == "INV":
    #         #         PhaseValue = 2
    #         #     if m['Phase'] == "Others":
    #         #         PhaseValue = 3
    #         #     phaselist.append(PhaseValue)
    #         # Projectinfo['phase'] = phaselist
    #         Projectinfo['project'] = j['Project']
    #         Customerlist.append(Projectinfo)
    #     combine[i['Customer']] = Customerlist
    # print(combine)
    # print(request.method)
    # print(request.GET)
    # print(request.POST,request.GET)
    # print(str(request.body, encoding='utf-8'))

    if request.method == "GET":
        if request.GET.get("action") == "get":
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
                'addselect': selectCategory,
                'canExport': canExport,

            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        if request.GET.get("action") == "search":
            Customer = request.GET.get('customer')
            Prolist = []
            if Customer != "ALL":#前端加了为空的判断,所以Customer不可能为空，并且el-option的value不能设为空
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
            # print(projectMsg)
            data = {
                'msg': 400,
            'content': projectMsg,
            'addselect': selectCategory,
                "selectMsg": combine,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == "POST":
        if request.POST.get("action") == "getMsg":
            Customer = request.POST.get('customer')
            Projectlist = request.POST.getlist("projectMsg", [])
            print(Projectlist)
            Category = request.POST.get('Category')
            if Category:
                for i in lesson_learn.objects.filter(Category=Category):
                    projectresult = []
                    for j in Projectlist:
                        print(j)
                        dic_Project = {'Customer': Customer, 'Project': j}
                        Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
                        lessonlearn_Projectinfo = lessonlearn_Project.objects.filter(lesson=i.id,
                                                                                     Projectinfo=Projectinfos).first()
                        if lessonlearn_Projectinfo:
                            # print(type(lessonlearn_Project.objects.filter(lesson=i.id,
                            #                                Projectinfo=Projectinfos)),type(lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                            projectresult.append({"projectname": j, "result": lessonlearn_Projectinfo.result,
                                                  "comment": lessonlearn_Projectinfo.Comment})
                        else:#占位，否则结果会错位
                            projectresult.append({"projectname": j, "result": '',
                                                  "comment": ''})
                    # print(projectresult)
                    Photolist = []
                    filelist = []
                    for h in i.Photo.all():
                        if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(h.img))
                        else:
                            filelist.append("/media/" + str(h.img))
                    # print(Photolist)
                    mock_data.append(
                        {
                            "len_id": i.id,
                            "Category": i.Category,
                            "object": i.Object,
                            "symptom": i.Symptom,
                            "Reproduce_Steps": i.Reproduce_Steps,
                            "root_cause": i.Root_Cause,
                            "solution": i.Solution,
                            "action": i.Action,
                            "photo": Photolist,
                            "file": filelist,
                            "project": projectresult,
                        },
                    )
            else:
                for i in lesson_learn.objects.all():
                    projectresult = []
                    for j in Projectlist:
                        # print(j)
                        dic_Project = {'Customer': Customer, 'Project': j}
                        Projectinfos = TestProjectLL.objects.filter(**dic_Project).first()
                        lessonlearn_Projectinfo = lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()
                        if lessonlearn_Projectinfo:

                        # print(type(lessonlearn_Project.objects.filter(lesson=i.id,
                        #                                Projectinfo=Projectinfos)),type(lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                            projectresult.append({"projectname": j, "result": lessonlearn_Projectinfo.result, "comment": lessonlearn_Projectinfo.Comment})
                        else:#占位，否则结果会错位
                            projectresult.append({"projectname": j, "result": '',
                                                  "comment": ''})
                    # print(projectresult)
                    Photolist = []
                    filelist = []
                    for h in i.Photo.all():
                        if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(h.img))
                        else:
                            filelist.append("/media/" + str(h.img))
                    # print(Photolist)
                    mock_data.append(
                        {
                            "len_id": i.id,
                            "Category": i.Category,
                            "object": i.Object,
                            "symptom": i.Symptom,
                            "Reproduce_Steps": i.Reproduce_Steps,
                            "root_cause": i.Root_Cause,
                            "solution": i.Solution,
                            "action": i.Action,
                            "photo": Photolist,
                            "file": filelist,
                            "project": projectresult,
                        },
                    )
            print(mock_data)


            # print (mock_data)
            updateData = {
                'msg': 400,
                'content': mock_data,
                'addselect': selectCategory,
                "selectMsg": combine,
                'canExport': canExport,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")



    return render(request, 'LessonProjectME/Lesson_result_search.html', locals())