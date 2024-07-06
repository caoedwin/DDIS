from django.shortcuts import render,redirect,HttpResponse
from .models import UserInfo,lesson_learn,Imgs,files,ProjectinfoinDCT
from django.views.decorators.csrf import csrf_exempt
from Bouncing.models import Bouncing_M
from Package.models import Package_M
from CDM.models import CDM
from TestPlanME.models import TestProjectME,TestItemME,TestPlanME
from LessonProjectME.models import lessonlearn_Project
from DriverTool.models import DriverList_M,ToolList_M
from MQM.models import MQM
from TestPlanSW.models import TestProjectSW
from CQM.models import CQMProject, CQM, CQM_history
import datetime,os
from service.init_permission import init_permission
from django.conf import settings
# Create your views here.
from django.forms import forms
from DjangoUeditor.forms import UEditorField
from .forms import lessonlearn
from django.conf import settings
import datetime,json,requests,time
from requests_ntlm import HttpNtlmAuth
# from app01.templatetags.custom_tag import *

# class TestUEditorForm(forms.Form):
#     content = UEditorField('Solution/Action', width=800, height=500,
#                             toolbars="full", imagePath="upimg/", filePath="upfile/",
#                             upload_settings={"imageMaxSize": 1204000},
#                             settings={}, command=None#, blank=True
#                             )
# import logging
#
# logger = logging.getLogger('Django')
# logger.debug('Debug')
# logger.info('Info')
# logger.warning('Warning')
# logger.error('Error')
# logger.critical('Critical')

def ImportProjectinfoFromDCT():
    ProjectNameList = []
    for i in Package_M.objects.all().values('Project').distinct():
        # print(i['Project'])
        ProjectNameList.append(i['Project'])
    for i in Bouncing_M.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in CDM.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in DriverList_M.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in ToolList_M.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in MQM.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in TestProjectME.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in TestProjectSW.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    for i in CQMProject.objects.all().values('Project').distinct():
        ProjectNameList.append(i['Project'])
    # print(ProjectNameList)
    ProjectNameList = list(set(ProjectNameList))
    print(ProjectNameList)
    sameandlocal=[]
    samePrj=[]
    nosamePjr = []
    for i in ProjectNameList:
        project = "ProjectCode=" + i
        url = r'http://192.168.1.10/dct/api/ClientSvc/getProjectInfo'
        requests.adapters.DEFAULT_RETRIES = 1
        # s = requests.session()
        # s.keep_alive = False  # 关闭多余连接
        # getTestSpec=requests.get(url)
        headers = {'Connection': 'close'}
        try:
            r = requests.get(url, headers=headers)
            getTestSpec = requests.get(url, project)
            # print (getTestSpec.url)
        except:
            # time.sleep(0.1)
            print("Can't connect to DCT Sercer")
            return 0
        targetURL = getTestSpec.url
        # url=r"http://127.0.0.1"

        url.split('\n')[0]
        # print url
        # 输入用户名和密码python requests实现windows身份验证登录
        try:
            getTestSpec = requests.get(targetURL, auth=HttpNtlmAuth('DCT\\administrator', 'DQA3`2018'))
        except:
            # time.sleep(0.1)
            print("try request agian")
            return 0

        # print 1
        # print getTestSpec.url
        newstr = getTestSpec.text.replace('<br>', '')
        # print (newstr)
        newstr1 = newstr.replace('":"', '*!')
        # print(newstr1)
        newstr2 = newstr1.replace('","', '!*')
        # print(newstr2)
        newstr3 = newstr2.replace('{"', '/!')
        # print(newstr3)
        newstr4 = newstr3.replace('"  }', '!/')
        # print(newstr4)
        newstr5 = newstr4.replace('"', '')
        # print(newstr5)
        newstr6 = newstr5.replace('*!', '":"')
        # print(newstr6)
        newstr7 = newstr6.replace('!*', '","')
        # print(newstr7)
        newstr8 = newstr7.replace('/!', '{"')
        # print(newstr8)
        newstr9 = newstr8.replace('!/', '"}')
        # print(newstr9)
        if not ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
            # print(json.loads(newstr))
            if json.loads(newstr9)['ComPrjCode']:
                samePrj.append(i)
                localPrjCre = {"Year": json.loads(newstr9)['Year'],
                               "ComPrjCode": json.loads(newstr9)['ComPrjCode'],
                               "CusPrjCode": json.loads(newstr9)['CusPrjCode'],
                               "ProjectName": json.loads(newstr9)['ProjectName'],
                               "Size": json.loads(newstr9)['Size'], "CPU": json.loads(newstr9)['CPU'],
                               "Platform": json.loads(newstr9)['Platform'],
                               "VGA": json.loads(newstr9)['VGA'],
                               "OSSupport": json.loads(newstr9)['OSSupport'],
                               "SS": json.loads(newstr9)['SS'],
                               "LD": json.loads(newstr9)['LD'], "DQAPL": json.loads(newstr9)['DQAPL']}
                ProjectinfoinDCT.objects.create(**localPrjCre)
            else:
                nosamePjr.append(i)
        else:
            sameandlocal.append(i)
            if json.loads(newstr9)['ComPrjCode']:
                localPrjUpdate = {"Year": json.loads(newstr9)['Year'],
                               "ComPrjCode": json.loads(newstr9)['ComPrjCode'],
                               "CusPrjCode": json.loads(newstr9)['CusPrjCode'],
                               "ProjectName": json.loads(newstr9)['ProjectName'],
                               "Size": json.loads(newstr9)['Size'], "CPU": json.loads(newstr9)['CPU'],
                               "Platform": json.loads(newstr9)['Platform'],
                               "VGA": json.loads(newstr9)['VGA'],
                               "OSSupport": json.loads(newstr9)['OSSupport'],
                               "SS": json.loads(newstr9)['SS'],
                               "LD": json.loads(newstr9)['LD'], "DQAPL": json.loads(newstr9)['DQAPL']}
                ProjectinfoinDCT.objects.filter(ComPrjCode=i).update(**localPrjUpdate)


    print(sameandlocal)
    print(samePrj)
    print(nosamePjr)
    return 1



@csrf_exempt
def login(request):
    # 不允许重复登录
    if request.session.get('is_login', None):
        return redirect('/index/')
    # print(request.method)
    # print('test')

    if request.method == "POST":
        # login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        # if login_form.is_valid():
        Account = request.POST.get('inputEmail')
        Password = request.POST.get('inputPassword')
        user_obj = UserInfo.objects.filter(account=Account, password=Password).first()
        # print (Account)
        # print (Password)
        # print (user_obj)
        # t= UserInfo.objects.get(account=Account)
        user = UserInfo.objects.filter(account=Account).first()
        # print(type(user),type(user_obj))
        if user:

            # print (user.password)
            if user.password == Password:
                # 往session字典内写入用户状态和数据,你完全可以往里面写任何数据，不仅仅限于用户相关！
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.username
                request.session['account'] = Account
                # request.session['Skin'] = "/static/src/blue.jpg"
                request.session.set_expiry(12*60*60)
                # print('11')
                Skin = request.COOKIES.get('Skin_raw')
                # print(Skin)
                if not Skin:
                    Skin = "/static/src/blue.jpg"
                # print(Skin)
                # print('21')
                init_permission(request, user_obj)  # 调用init_permission，初始化权限
                # print('21')
                # print(settings.MEDIA_ROOT,settings.MEDIA_URL)
                return redirect('/index/')
            else:
                message = "密码不正确！"
        else:
            message = "用户不存在！"
        return render(request, 'login.html', locals())


    return render(request, 'login.html', locals())

def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # Skin = request.COOKIES.get('Skin_raw')
    # # print(Skin)
    # if not Skin:
    #     Skin = "/static/src/blue.jpg"
    # weizhi="Home/Dashboard"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    # print (permission_url)
    # L_R_data_object=lesson_learn.objects.all().order_by('edit_time')
    # # print(type(L_R_data_object.first().edit_time))
    # # print(L_R_data_object.last().edit_time)
    # time_first=L_R_data_object.first().edit_time
    # L_R_data_first=datetime.datetime.strptime(str(time_first)[0:10],'%Y-%m-%d')
    # time_last = L_R_data_object.last().edit_time
    # L_R_data_last = datetime.datetime.strptime(str(time_last)[0:10], '%Y-%m-%d')
    # # print(type(L_R_data_first))
    # L_R_data = (L_R_data_last-L_R_data_first).days/365
    # L_R_data=format(L_R_data,'.2f')
    L_R_data = lesson_learn.objects.filter(Category="Reliability").values('Symptom').count()
    L_C_data = lesson_learn.objects.filter(Category="Compatibility").values('Symptom').count()
    R_P_data=Package_M.objects.all().values('Project').distinct().count()
    R_B_data=Bouncing_M.objects.all().values('Project').distinct().count()
    R_C_data=CDM.objects.all().values('Project').distinct().count()
    T_M_Project=TestProjectME.objects.all().values('Project').distinct().count()
    X_D_DriverList=DriverList_M.objects.all().values('Project').distinct().count()
    X_D_ToolList=ToolList_M.objects.all().values('Project').distinct().count()
    X_M_Project=MQM.objects.all().values('Project').distinct().count()
    T_S_Project=TestProjectSW.objects.all().values('Project').distinct().count()
    X_C_data = CQMProject.objects.all().values('Project').distinct().count()
    # for i in TestProjectME.objects.all().values('Customer', 'Project', 'Phase').distinct():
    #     print(i)
    T_M_Items=TestItemME.objects.all().count()
    # importPrjResult = ImportProjectinfoFromDCT()
    print(request.POST)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Reliability":
            #cookie
            # Redirect = redirect('/Lesson_search/')
            # Reliabilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Reliabilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    if request.method == "POST":
        if request.POST.get("isGetData") == "Compatibility":
            #cookie
            # Redirect = redirect('/Lesson_search/')
            # Compatibilityv = request.POST.get('isGetData')
            # Redirect.set_cookie('cookieSWME', Compatibilityv, 3600 * 24 )
            # return Redirect#这里虽然返回了Redirect的路径，但是由于时axios传输，返回页面没有用，到那时必须要加，不然cookie设置不成功。
            request.session['sessionSWME'] = request.POST.get('isGetData')
            request.session.set_expiry(12 * 60 * 60)
    return render(request, 'index.html', locals())


def FilesDownload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Home/FilesDownload"
    permission_url = request.session.get(settings.SESSION_PERMISSION_URL_KEY)
    data = {}
    if request.method == "GET":
        # print(request.GET)
        if request.GET.get("action") == "first":
            importPrjResult = ImportProjectinfoFromDCT()
            if importPrjResult:
                data['result'] = 1
            else:
                data['result'] = 0
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'FilesDownload.html', locals())

@csrf_exempt
def logout(request):
    # print('t')
    # print (request.session.get('is_login', None))
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        # print('logout')
        return redirect("/login/")
    #flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("/login/")

@csrf_exempt
def Change_Password(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    # print (request.method)
    if request.method == "POST":
        OldPassword=request.POST.get('OldPassword')
        Password = request.POST.get('Password')
        Passwordc = request.POST.get('Confirm')
        user=request.session.get('user_name')
        userpass=UserInfo.objects.get(username=user).password
        # print(OldPassword,userpass)
        if OldPassword==userpass:
            if Password==Passwordc:
                # print(request.session.get('user_name', None))
                updatep = UserInfo.objects.filter(username=request.session.get('user_name', None))
                # print (updatep)
                # for e in updatep:
                #    print (e.password)
                updatep.update(password=Password)
                request.session.flush()
                return redirect("/login/")
            else:
                message="Password is not same"
                return render(request, 'changepassword.html', locals())
        else:
            message = "Incorrect Password"
            return render(request, 'changepassword.html', locals())
    return render(request, 'changepassword.html', locals())

@csrf_exempt
def Change_Skin(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    # print(request.method)
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    # print(Skin)
    weizhi = "Change Skin"
    Render = render(request, 'ChangeSkin.html', locals())
    Redirect=redirect('/Change_Skin/')
    if request.method == "POST":

        if 'blue' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/blue.jpg", 3600 * 24 * 30 * 12)
        if 'kiwi' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/kiwi.jpg", 3600 * 24 * 30 * 12)
        if 'sunny' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/sunny.jpg",3600*24*30*12)
        if 'yellow' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/yellow.jpg",3600*24*30*12)
        if 'chrome' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/chrome.jpg",3600*24*30*12)
        if 'ocean' in request.POST:
            Skinv = request.POST.get('Skin')
            Redirect.set_cookie('Skin_raw', "/static/src/ocean.jpg",3600*24*30*12)
        return Redirect
            # return redirect('/index/')
    # return redirect('/index/')
    # print(Skin)
    return Render


@csrf_exempt
def Lesson_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Lesson-Learn/Reliability/Upload"
    message=''
    message_err=0
    # form=TestUEditorForm()
    lesson_form=lessonlearn(request.POST)
    if request.method == "POST":
        lesson=lessonlearn(request.POST)
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
            # print(Comments)
            Photo = request.FILES.getlist("myfiles", "")
            print(Photo)
            Object_check =lesson_learn.objects.filter(Object=Object)
            Symptom_check=lesson_learn.objects.filter(Symptom=Symptom)
            # print (Object_check,Symptom_check)
            # if Object_check:
            #     #message = "Object '%s' already exists" % (Object)
            #     message_err=1
            #     return render(request, 'Lesson_upload.html',locals())
            # else:
            if Symptom_check:
                #message = "Symptom '%s' already exists" % (Symptom)
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
                lesson=lesson_learn()
                lesson.Category = Category
                lesson.Object=Object
                lesson.Symptom=Symptom
                lesson.Reproduce_Steps = Reproduce_Steps
                lesson.Root_Cause = Root_Cause
                lesson.Solution=Comments
                lesson.Action = Action
                # lesson.Photo=Photos
                lesson.editor=request.session.get('user_name')
                lesson.edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                lesson.save()
                # print(request.FILES.getlist('myfiles'),request.POST.get('myfiles'))
                # print(request.FILES)
                for f in request.FILES.getlist('myfiles'):
                    # print(f)
                    empt = Imgs()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.img = f
                    empt.save()
                    lesson.Photo.add(empt)
                for f in request.FILES.getlist('myvideos'):
                    # print(f)
                    empt = files()
                    # 增加其他字段应分别对应填写
                    empt.single = f
                    empt.files = f
                    empt.save()
                    lesson.video.add(empt)
                message="Upload '%s' Successfully" %(Object)

                # print (lessonlearn())
                # print(lessonlearn(request.POST))
                # return render(request, 'Lesson_upload.html', {'weizhi':weizhi,'Skin':Skin,'lesson_form':lessonlearn(),'message':message,'message_err':message_err})
                return render(request, 'Lesson_upload.html', locals())
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    # print (locals())
    return render(request, 'Lesson_upload.html',locals())#{'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})

@csrf_exempt
def Lesson_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Lesson-Learn/Reliability/Redit"
    Lesson_list=lesson_learn.objects.all()
    return render(request, 'Lesson_edit.html', locals())

def Lesson_update(request,id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Lesson-Learn/Reliability/Redit/%s" % id
    message = ''
    # form=TestUEditorForm()
    lesson_formdefault = lesson_learn.objects.get(id=id)
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
            # lesson = lesson_learn()
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
            if choose=="删除原图片":
                lesson_formdefault.Photo.clear()
            for f in request.FILES.getlist('myfiles'):
                # print(f)
                empt = Imgs()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.img = f
                empt.save()
                lesson_formdefault.Photo.add(empt)
                # lesson_formdefault.Photo.remove()
            if choosev=="删除原视频":
                lesson_formdefault.video.clear()
            for f in request.FILES.getlist('myvideos'):
                # print(f)
                empt = files()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                lesson_formdefault.video.add(empt)
                # lesson_formdefault.video.remove()
            id=id
            message_redit = "Redit '%s' Successfully" % (id)
            # print (lessonlearn())
            # print(lessonlearn(request.POST))
            # return render(request, 'Lesson_update.html',locals())
            return redirect('/Lesson_edit/')
        else:
            cleanData = lesson.errors
            # print(lesson.errors)
    else:
        values = {'Object': lesson_formdefault.Object, 'Symptom': lesson_formdefault.Symptom, 'Root_Cause': lesson_formdefault.Root_Cause, 'Solution': lesson_formdefault.Solution, 'Action': lesson_formdefault.Action}
        lesson_form = lessonlearn(values)
    # print (locals())
    # print(settings.BASE_DIR,settings.STATICFILES_DIRS)
    return render(request, 'Lesson_update.html',
                  locals())  # {'weizhi':weizhi,'Skin':Skin,'lesson_form':lesson_form,'message':message})
    # return render(request, 'Lesson_update.html', locals())

@csrf_exempt
def Lesson_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # Categoryfromcookie = request.COOKIES.get('cookieSWME')#cookie也是可以的，但是每次设置cookie时都要返回redirect，如果要返回Jason给axios，就没法用了
    Categoryfromcookie = request.session.get('sessionSWME')
    print(Categoryfromcookie)
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Lesson-Learn/Reliability/Search"
    # Lesson_list=lesson_learn.objects.all()
    Lesson_list = lesson_learn.objects.filter(Category=Categoryfromcookie)
    selectCategory = [
        # {"Category": "SW"},
        # {"Category": "ME"}
    ]
    # print(request.method)
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            # print(request.POST.get("isGetData"), '111')
            Categorylist = lesson_learn.objects.all().values("Category").distinct().order_by("-Category")
            for i in Categorylist:
                selectCategory.append({"Category": i["Category"]})

            data = {
                'addselect': selectCategory,
            }
            # print(updateData)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get("isGetData") == "Search":
            Category = request.POST.get("Category")
            if Category:
                # print(Category)
                Check_dic = {"Category": Category}
                Lesson_list = lesson_learn.objects.filter(**Check_dic)
                # print(Lesson_list)

            else:
                Lesson_list = lesson_learn.objects.all()
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
    return render(request, 'Lesson_search.html', locals())

def Lesson_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Lesson-Learn/Reliability/Search"
    Lesson_list=lesson_learn.objects.all()

    return render(request, 'Lesson_export.html', locals())



def ttt(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="/ttt"

    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (img)
    #     for i in img:
    #         print (i.img)
    return render(request, 'ttt.html', locals())

