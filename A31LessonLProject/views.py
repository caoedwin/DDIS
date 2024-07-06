from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from .models import A31lessonlearn_Project, A31TestProjectLL, A31lesson_learn, A31Imgs, A31files
from app01.models import ProjectinfoinDCT, UserInfo
from django.views.decorators.csrf import csrf_exempt
from .forms import A31lessonlearn as lessonlearn
# from TestPlanME.models import TestProjectME
import datetime, os

import datetime, json


# Create your views here.
@csrf_exempt
def A31Lesson_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Upload"
    message = ''
    message_err = 0
    # form=TestUEditorForm()
    lesson_form = lessonlearn(request.POST)
    if request.method == "POST":
        lesson = lessonlearn(request.POST)
        # test = request.POST.get('test')
        # print(test)
        if lesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
            Category = lesson.cleaned_data['Category']
            Object = lesson.cleaned_data['Object']
            Symptom = lesson.cleaned_data['Symptom']
            Reproduce_Steps = lesson.cleaned_data['Reproduce_Steps']
            Root_Cause = lesson.cleaned_data['Root_Cause']
            Comments = lesson.cleaned_data['Solution']
            Action = lesson.cleaned_data['Action']
            Status = lesson.cleaned_data['Status']
            # print(Comments)
            Photo = request.FILES.getlist("myfiles", "")
            print(Photo)
            Object_check = A31lesson_learn.objects.filter(Object=Object)
            Symptom_check = A31lesson_learn.objects.filter(Symptom=Symptom)
            # print (Object_check,Symptom_check)
            # if Object_check:
            #     #message = "Object '%s' already exists" % (Object)
            #     message_err=1
            #     return render(request, 'Lesson_upload.html',locals())
            # else:
            if Symptom_check:
                # message = "Symptom '%s' already exists" % (Symptom)
                message_err = 2
                return render(request, 'Lesson_upload.html', locals())
            else:
                # Photos=''
                # for image in Photo:
                #     # print (image.name)
                #     if not Photos:
                #         Photos='img/test/'+image.name
                #     else:
                #         Photos=Photos+','+'img/test/'+image.name
                # print (Photos)
                lesson = A31lesson_learn()
                lesson.Category = Category
                lesson.Object = Object
                lesson.Symptom = Symptom
                lesson.Reproduce_Steps = Reproduce_Steps
                lesson.Root_Cause = Root_Cause
                lesson.Solution = Comments
                lesson.Action = Action
                lesson.Status = Status
                # lesson.Photo=Photos
                lesson.editor = request.session.get('user_name')
                lesson.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lesson.save()
                # print(request.FILES.getlist('myfiles'),request.POST.get('myfiles'))
                # print(request.FILES)
                for f in request.FILES.getlist('myfiles'):
                    # print(f)
                    empt = A31Imgs()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.img = f
                    empt.save()
                    lesson.Photo.add(empt)
                for f in request.FILES.getlist('myvideos'):
                    # print(f)
                    empt = A31files()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.files = f
                    empt.save()
                    lesson.video.add(empt)
                message = "Upload '%s' Successfully" % (Object)

                # print (lessonlearn())
                # print(lessonlearn(request.POST))
                # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                return render(request, 'Lesson_upload.html', locals())
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    # print (locals())
    return render(request, 'A31LessonLProject/Lesson_upload.html',
                  locals())  # {'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})


@csrf_exempt
def A31Lesson_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Redit"
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
    form = {
        # "Category": "SW",
        # "Object": "Design",
        # "Symptom": "asdfghjghtjymk,jkjh",
        # "Reproduce_Steps": "esyrtduyfukigliukyjtyt",
        # "Root_Cause": "esrdtgfjyhjjhgryter",
        # "Solution": "esrthdyhyjytrwetgrthyjtyrhtjyjyrghthygr",
        # "Action": "grhdtgyjhygrhtjthyrthygrzhh"
        # # "photo":[{name: 'food.jpeg', url: '/static/images/spec.png'},
        # #           {name: 'food2.jpeg', url: '/static/images/spec.png'}]
    }
    fileListO = [
        # {'name': 'Screenshot_15.png', 'url': '/media/img/test/Screenshot_15.png'}
    ]
    # print(request.POST)
    Categorylist = A31lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    Lesson_list = A31lesson_learn.objects.all()
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = A31lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = A31lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Status": i.Status,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "alertID":
            id = request.POST.get('ID')
            if id:
                editlesson = A31lesson_learn.objects.get(id=id)
                form["Category"] = editlesson.Category
                form["Object"] = editlesson.Object
                form["Symptom"] = editlesson.Symptom
                form["Reproduce_Steps"] = editlesson.Reproduce_Steps
                form["Root_Cause"] = editlesson.Root_Cause
                form["Solution"] = editlesson.Solution
                form["Action"] = editlesson.Action
                form["Status"] = editlesson.Status
                # print(len(editlesson.Photo.all()),len(editlesson.video.all()))
                for i in editlesson.Photo.all():
                    # print(i.img,type(i.img),)
                    # print(i.img.name)
                    fileListO.append({'name': '', 'url': '/media/' + i.img.name})

                for i in editlesson.video.all():
                    fileListO.append({'name': '', 'url': '/media/' + i.files.name})
            data = {
                'form': form,
                'fileListO': fileListO
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("action") == "submit":
            serchCategory = request.POST.get("serchCategory")
            editID = request.POST.get('id')
            # print(serchCategory, request.POST.get('Category'))
            Photolist = request.FILES.getlist("fileList", "")
            # print(Photolist,editID)
            if editID:
                # print("1")
                editlesson = A31lesson_learn.objects.get(id=editID)
                editlesson.Category = request.POST.get('Category')
                editlesson.Object = request.POST.get('Object')
                editlesson.Symptom = request.POST.get('Symptom')
                editlesson.Reproduce_Steps = request.POST.get('Reproduce_Steps')
                editlesson.Root_Cause = request.POST.get('Root_Cause')
                editlesson.Solution = request.POST.get('Solution')
                editlesson.Action = request.POST.get('Action')
                editlesson.Status = request.POST.get('Status')
                # lesson.Photo=Photos
                editlesson.editor = request.session.get('user_name')
                editlesson.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                editlesson.save()
                if Photolist:
                    for f in Photolist:
                        # print(f)
                        if f.name.split(".")[1] == "mp4" or f.name.split(".")[1] == "AVI" or f.name.split(".")[
                            1] == "mov" or f.name.split(".")[1] == "rmvb":
                            empt = A31files()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            editlesson.video.add(empt)
                        else:
                            empt = A31Imgs()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.img = f
                            empt.save()
                            editlesson.Photo.add(empt)
            if serchCategory:
                # print(Category)
                Check_dic = {"Category": serchCategory}
                Lesson_list = A31lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = A31lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Status": i.Status,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)

            # fileList = [{name: 'food.jpeg', url: '/static/images/spec.png'},
            #             {name: 'food2.jpeg', url: '/static/images/spec.png'}]
            data = {
                #     'fileList': fileList
                'addselect': selectCategory,
                'content': mock_data,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'A31LessonLProject/Lesson_edit.html', locals())


def A31Lesson_update(request, id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Redit/%s" % id
    message = ''
    # form=TestUEditorForm()
    lesson_formdefault = A31lesson_learn.objects.get(id=id)
    # print(lesson_formdefault)
    # print(request.POST)
    lesson_form = lessonlearn(request.POST)

    if request.method == "POST":
        lesson = lessonlearn(request.POST)
        if lesson.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
            Object = lesson.cleaned_data['Object']
            Symptom = lesson.cleaned_data['Symptom']
            Root_Cause = lesson.cleaned_data['Root_Cause']
            # print(Root_Cause)
            Comments = lesson.cleaned_data['Solution']
            Action = lesson.cleaned_data['Action']
            choose = request.POST.get('choose')
            choosev = request.POST.get('choosev')
            # print(choose)
            # print(Root_Cause,Comments)
            Photo = request.FILES.getlist("myfiles", "")
            # lesson = A31lesson_learn()
            # print(lesson_formdefault)
            # print (lesson)
            lesson_formdefault.Object = Object
            lesson_formdefault.Symptom = Symptom
            lesson_formdefault.Root_Cause = Root_Cause
            lesson_formdefault.Solution = Comments
            lesson_formdefault.Action = Action
            # lesson.Photo=Photos
            lesson_formdefault.editor = request.session.get('user_name')
            lesson_formdefault.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            lesson_formdefault.save()
            if choose == "删除原图片":
                lesson_formdefault.Photo.clear()
            for f in request.FILES.getlist('myfiles'):
                # print(f)
                empt = A31Imgs()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.img = f
                empt.save()
                lesson_formdefault.Photo.add(empt)
                # lesson_formdefault.Photo.remove()
            if choosev == "删除原视频":
                lesson_formdefault.video.clear()
            for f in request.FILES.getlist('myvideos'):
                # print(f)
                empt = A31files()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                lesson_formdefault.video.add(empt)
                # lesson_formdefault.video.remove()
            id = id
            message_redit = "Redit '%s' Successfully" % (id)
            # print (lessonlearn())
            # print(lessonlearn(request.POST))
            # return render(request, 'Lesson_update.html',locals())
            return redirect('/Lesson_edit/')
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    else:
        values = {'Object': lesson_formdefault.Object, 'Symptom': lesson_formdefault.Symptom,
                  'Root_Cause': lesson_formdefault.Root_Cause, 'Solution': lesson_formdefault.Solution,
                  'Action': lesson_formdefault.Action}
        lesson_form = lessonlearn(values)
    # print (locals())
    # print(settings.BASE_DIR,settings.STATICFILES_DIRS)
    return render(request, 'A31LessonLProject/Lesson_update.html',
                  locals())  # {'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})
    # return render(request, 'Lesson_update.html', locals())


@csrf_exempt
def A31Lesson_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # Categoryfromcookie = request.COOKIES.get('cookieSWME')#cookie也是可以的，但是每次设置cookie时都要返回redirect，如果要返回Jason给axios，就没法用了
    Categoryfromcookie = request.session.get('sessionSWME')
    print(Categoryfromcookie)
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Search"
    # Lesson_list=A31lesson_learn.objects.all()
    Lesson_list = A31lesson_learn.objects.filter(Category=Categoryfromcookie)
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
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
    Categorylist = A31lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("isGetData"), '111')
            if Categoryfromcookie:
                for i in Lesson_list:
                    Photolist = []
                    filelist = []
                    for h in i.Photo.all():
                        # print(str(h.img).split("."))
                        if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                            Photolist.append("/media/" + str(h.img))
                        else:
                            filelist.append("/media/" + str(h.img))
                    Videolist = []
                    for h in i.video.all():
                        Videolist.append("/media/" + str(h.files))
                    # print(Photolist)
                    mock_data.append(
                        {
                            "id": i.id,
                            "Category": i.Category,
                            "Object": i.Object,
                            "Symptom": i.Symptom,
                            "Reproduce_Steps": i.Reproduce_Steps,
                            "Root_Cause": i.Root_Cause,
                            "Solution": i.Solution,
                            "Action": i.Action,
                            "Status": i.Status,
                            "Photo": Photolist,
                            "file": filelist,
                            "Video": Videolist,
                            "editor": i.editor,
                            "edit_time": i.edit_time,
                        },
                    )
                request.session['sessionSWME'] = None

            data = {
                'addselect': selectCategory,
                'content': mock_data,
                "canEdit": canEdit,
                'canExport': canExport,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = A31lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = A31lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Status": i.Status,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
                "canEdit": canEdit,
                'canExport': canExport,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        # Lesson_list_dic = []
        # for i in Lesson_list:
        #     Photolist = []
        #     for j in i.Photo.all():
        #         Photolist.append("/media/"+str(j.img))
        #     videolist = []
        #     for j in i.video.all():
        #         videolist.append("/media/"+str(j.files))
        #     Lesson_list_dic.append({"id":i.id, "Category":i.Category, "Object":i.Object, "Symptom":i.Symptom, "Reproduce_Steps":i.Reproduce_Steps,
        #                             "Root_Cause":i.Root_Cause, "Solution":i.Solution, "Action":i.Action, "Photo":Photolist, "video":videolist, "edit_time":i.edit_time,})
        #         # data = {
        #         #     'Lesson_list': Lesson_list_dic,
        # }
        # return HttpResponse(json.dumps(data), content_type="application/json")
        # print(locals())
    return render(request, 'A31LessonLProject/Lesson_search.html', locals())


@csrf_exempt
def A31Lesson_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Search"
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    mock_data = [
        # {"id": "1", "Category": "SW", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
        # {"id": "2", "Category": "ME", "Object": "Design", "Symptom": "", "Reproduce_Steps": "",
        #  "Root_Cause": "",
        #  "Solution": "", "Action": "", "Photo": "", "Video": "", "editor": "", "edit_time": ""},
    ]
    # print(request.method)
    Categorylist = A31lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
    for i in Categorylist:
        selectCategory.append({"Category": i["Category"]})
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("isGetData"), '111')
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = A31lesson_learn.objects.filter(**Check_dic)
            else:
                Lesson_list = A31lesson_learn.objects.all()
            for i in Lesson_list:
                Photolist = []
                filelist = []
                for h in i.Photo.all():
                    # print(str(h.img).split("."))
                    if str(h.img).split(".")[1] == "jpg" or str(h.img).split(".")[1] == "png":
                        Photolist.append("/media/" + str(h.img))
                    else:
                        filelist.append("/media/" + str(h.img))
                Videolist = []
                for h in i.video.all():
                    Videolist.append("/media/" + str(h.files))
                # print(Photolist)
                mock_data.append(
                    {
                        "id": i.id,
                        "Category": i.Category,
                        "Object": i.Object,
                        "Symptom": i.Symptom,
                        "Reproduce_Steps": i.Reproduce_Steps,
                        "Root_Cause": i.Root_Cause,
                        "Solution": i.Solution,
                        "Action": i.Action,
                        "Photo": Photolist,
                        "file": filelist,
                        "Video": Videolist,
                        "editor": i.editor,
                        "edit_time": i.edit_time,
                    },
                )
            # print(mock_data)
            data = {
                'addselect': selectCategory,
                'content': mock_data,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        # Lesson_list_dic = []
        # for i in Lesson_list:
        #     Photolist = []
        #     for j in i.Photo.all():
        #         Photolist.append("/media/"+str(j.img))
        #     videolist = []
        #     for j in i.video.all():
        #         videolist.append("/media/"+str(j.files))
        #     Lesson_list_dic.append({"id":i.id, "Category":i.Category, "Object":i.Object, "Symptom":i.Symptom, "Reproduce_Steps":i.Reproduce_Steps,
        #                             "Root_Cause":i.Root_Cause, "Solution":i.Solution, "Action":i.Action, "Photo":Photolist, "video":videolist, "edit_time":i.edit_time,})
        #         # data = {
        #         #     'Lesson_list': Lesson_list_dic,
        # }
        # return HttpResponse(json.dumps(data), content_type="application/json")
        # print(locals())

    return render(request, 'A31LessonLProject/Lesson_export.html', locals())


def A31Lesson_project(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "LessonProjectME/Edit"
    Lesson_list = A31lesson_learn.objects.all()
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
    Customer_list = A31TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in A31TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                'Project'):
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
    Categorylist = A31lesson_learn.objects.all().values("Category").distinct().order_by("Category")
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
            Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
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
                for i in A31lesson_learn.objects.filter(Status="active"):
                    Lessonlist.append(i.id)
                # print (Lessonlist)
                existlesson = []
                # print(Projectinfos.a31lessonlearn_project_set)
                for i in Projectinfos.a31lessonlearn_project_set.all():
                    # print(i)
                    existlesson.append(i.lesson.id)
                # print(existlesson)
                for i in Lessonlist:
                    if i in existlesson:
                        continue
                    else:
                        A31lessonlearn_Project.objects.create(lesson=A31lesson_learn.objects.get(id=i),
                                                              Projectinfo=A31TestProjectLL.objects.filter(
                                                                  **dic_Project).first())
            if Category:
                if Projectinfos.a31lessonlearn_project_set.filter(lesson__Category=Category):
                    for i in Projectinfos.a31lessonlearn_project_set.filter(lesson__Category=Category).order_by('id'):
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
                if Projectinfos.a31lessonlearn_project_set.all():
                    for i in Projectinfos.a31lessonlearn_project_set.all().order_by('id'):
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

            Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
            # learninfo = A31lesson_learn.objects.get(id=request.POST.get("lesson_id"))
            # editplan = A31lessonlearn_Project.objects.filter(lesson=learninfo, Projectinfo=Projectinfos).first()
            try:
                editplan = A31lessonlearn_Project.objects.filter(id=request.POST.get("lesson_id")).first()
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
            Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
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
                Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
                for i in Projectinfos.a31lessonlearn_project_set.filter(lesson__Category=Category).order_by('id'):
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
                Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
                for i in Projectinfos.a31lessonlearn_project_set.all().order_by('id'):
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

    return render(request, 'A31LessonLProject/Lesson_result.html', locals())


def A31Lesson_project_Search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "LessonProjectME/ProjectResult"
    Lesson_list = A31lesson_learn.objects.all()
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
    Customer_list = A31TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in A31TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                'Project'):
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
    Customer_list = A31TestProjectLL.objects.all().values('Customer').distinct().order_by('Customer')
    Categorylist = A31lesson_learn.objects.all().values("Category").distinct().order_by("Category")
    for i in Categorylist:
        selectCategory.append({"Category": i['Category']})

    # for i in Customer_list:
    #     Customerlist = []
    #     for j in A31TestProjectLL.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
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
            if Customer != "ALL":  # 前端加了为空的判断,所以Customer不可能为空，并且el-option的value不能设为空
                for i in A31TestProjectLL.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append(i["Project"])
            else:
                for i in A31TestProjectLL.objects.all().values("Project").distinct().order_by("Project"):
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
                for i in A31lesson_learn.objects.filter(Category=Category):
                    projectresult = []
                    for j in Projectlist:
                        print(j)
                        dic_Project = {'Customer': Customer, 'Project': j}
                        Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
                        A31lessonlearn_Projectinfo = A31lessonlearn_Project.objects.filter(lesson=i.id,
                                                                                           Projectinfo=Projectinfos).first()
                        if A31lessonlearn_Projectinfo:
                            # print(type(A31lessonlearn_Project.objects.filter(lesson=i.id,
                            #                                Projectinfo=Projectinfos)),type(A31lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                            projectresult.append({"projectname": j, "result": A31lessonlearn_Projectinfo.result,
                                                  "comment": A31lessonlearn_Projectinfo.Comment})
                        else:  # 占位，否则结果会错位
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
                for i in A31lesson_learn.objects.all():
                    projectresult = []
                    for j in Projectlist:
                        # print(j)
                        dic_Project = {'Customer': Customer, 'Project': j}
                        Projectinfos = A31TestProjectLL.objects.filter(**dic_Project).first()
                        A31lessonlearn_Projectinfo = A31lessonlearn_Project.objects.filter(lesson=i.id,
                                                                                           Projectinfo=Projectinfos).first()
                        if A31lessonlearn_Projectinfo:

                            # print(type(A31lessonlearn_Project.objects.filter(lesson=i.id,
                            #                                Projectinfo=Projectinfos)),type(A31lessonlearn_Project.objects.filter(lesson=i.id,Projectinfo=Projectinfos).first()))
                            projectresult.append({"projectname": j, "result": A31lessonlearn_Projectinfo.result,
                                                  "comment": A31lessonlearn_Projectinfo.Comment})
                        else:  # 占位，否则结果会错位
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

    return render(request, 'A31LessonLProject/Lesson_result_search.html', locals())
