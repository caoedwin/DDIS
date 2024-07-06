from django.shortcuts import render,redirect
from .models import Bouncing_M
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from .forms import Bouncing
from .models import Bouncing_M,files_BM
from django.http import HttpResponse
import datetime,json,simplejson

# Create your views here.

@csrf_exempt
def bouncingtest_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/Buncing upload"
    buncing_upload = Bouncing(request.POST)
    Bouncing_M_lists = [{'Customer': '客户', 'Project': '专案','A_cover': 'A件',
                  'C_cover': 'C件', 'D_cover': 'D件','HS':'转轴',
                       'Torque':'扭力','Push':'推力','PV_L':'左峰值','PV_R':'右峰值','D_L':'Dur左','D_R':'Dur右'}]
    result='00'

    result = 4
    if request.method == "POST":
        # print(request.POST)
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            n = 0

            for i in simplejson.loads(xlsxlist):
                n += 1
                Bouncing_M_dic = {}
                # print(i)
                # print (i['Customer'])
                check_dic = {'Customer': i['Customer'], 'Project': i['Project'],'A_cover': i['A_cover_Material'],
                             'C_cover': i['C_cover_Material'], 'D_cover': i['D_cover_Material'],
                             'HS':i['Hinge supplier'],'Torque':i['Torque'],'Push':i['Push Force'],
                             'PV_L':i['Peak_Value_L'],'PV_R':i['Peak_Value_R'],'D_L':i['Distance_L'],'D_R':i['Distance_R']}
                # print(check_dic)
                check_list = Bouncing_M.objects.filter(**check_dic)
                # print (check_list)
                if check_list:
                    err_ok = 1
                    Bouncing_M_dic['Customer'] = i['Customer']
                    Bouncing_M_dic['Project'] = i['Project']
                    Bouncing_M_dic['A_cover'] = i['A_cover_Material']
                    Bouncing_M_dic['C_cover'] = i['C_cover_Material']
                    Bouncing_M_dic['D_cover'] = i['D_cover_Material']
                    Bouncing_M_dic['HS'] = i['Hinge supplier']
                    Bouncing_M_dic['Torque'] = i['Torque']
                    Bouncing_M_dic['Push'] = i['Push Force']
                    Bouncing_M_dic['PV_L'] = i['Peak_Value_L']
                    Bouncing_M_dic['PV_R'] = i['Peak_Value_R']
                    Bouncing_M_dic['D_L'] = i['Distance_L']
                    Bouncing_M_dic['D_R'] = i['Distance_R']
                    Bouncing_M_lists.append(Bouncing_M_dic)
                    continue
                else:
                    # print('save')
                    Bouncing_Mmodule = Bouncing_M()
                    Bouncing_Mmodule.Customer = i['Customer']
                    Bouncing_Mmodule.Project = i['Project']
                    # Bouncing_Mmodule.Phase = Phase
                    Bouncing_Mmodule.A_cover = i['A_cover_Material']
                    Bouncing_Mmodule.C_cover = i['C_cover_Material']
                    Bouncing_Mmodule.D_cover = i['D_cover_Material']
                    Bouncing_Mmodule.HS = i['Hinge supplier']
                    Bouncing_Mmodule.Torque = i['Torque']
                    Bouncing_Mmodule.Push = i['Push Force']
                    Bouncing_Mmodule.PV_L = i['Peak_Value_L']
                    Bouncing_Mmodule.PV_R = i['Peak_Value_R']
                    Bouncing_Mmodule.D_L = i['Distance_L']
                    Bouncing_Mmodule.D_R = i['Distance_R']
                    Bouncing_Mmodule.Conclusion = i['Conclusion']
                    Bouncing_Mmodule.editor = request.session.get('user_name')
                    Bouncing_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Bouncing_Mmodule.save()
                    # print('ttt')
            # if not message_Bouncing_M:
            #     message_Bouncing_M = "Upload Successfully"
            # print(message_Bouncing_M)
            datajason = {
                'err_ok': err_ok,
                'content': Bouncing_M_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if 'Upload' in request.POST:
            # print('1')

            if buncing_upload.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                # print('t')
                Customer = buncing_upload.cleaned_data['Customer']
                Project = buncing_upload.cleaned_data['Project']
                # Phase = buncing_upload.cleaned_data['Phase']
                A_cover = buncing_upload.cleaned_data['A_cover']
                C_cover = buncing_upload.cleaned_data['C_cover']
                D_cover = buncing_upload.cleaned_data['D_cover']
                HS = buncing_upload.cleaned_data['HS']
                Torque_min = request.POST.get('Torque_min')
                Torque_max = request.POST.get('Torque_max')
                # print(Torque_min)
                # print(Torque_max)
                Push_min = buncing_upload.cleaned_data['Push_min']
                Push_max = buncing_upload.cleaned_data['Push_max']
                PV_L_min = buncing_upload.cleaned_data['PV_L_min']
                PV_R_min = buncing_upload.cleaned_data['PV_R_min']
                PV_L_max = buncing_upload.cleaned_data['PV_L_max']
                PV_R_max = buncing_upload.cleaned_data['PV_R_max']
                D_L_min = buncing_upload.cleaned_data['D_L_min']
                D_R_min = buncing_upload.cleaned_data['D_R_min']
                D_L_max = buncing_upload.cleaned_data['D_L_max']
                D_R_max = buncing_upload.cleaned_data['D_R_max']
                Conclusion = request.POST.get('Conclusion')

                check_min_dic={'Customer':Customer,'Project':Project,'A_cover':A_cover,'C_cover':C_cover,'D_cover':D_cover,
                               'HS':HS,'Torque':Torque_min,'Push':Push_min,'PV_L':PV_L_min,'PV_R':PV_R_min,'D_L':D_L_min,'D_R':D_R_min}
                check_max_dic = {'Customer': Customer, 'Project': Project,'A_cover':A_cover, 'C_cover': C_cover, 'D_cover': D_cover,
                                 'HS': HS, 'Torque': Torque_max, 'Push': Push_max,'PV_L':PV_L_max,'PV_R':PV_R_max,'D_L':D_L_max,'D_R':D_R_max}
                check_min_list = Bouncing_M.objects.filter(**check_min_dic)
                check_max_list = Bouncing_M.objects.filter(**check_max_dic)
                if check_min_list or check_max_list:
                    # message_CDM="%s %s %s (%s,%s) already exist in database, " \
                    #             "please choose Edit if you want to update" % (Customer,Project,SKU_NO,C_cover_Material,D_cover_Material)
                    result = 1
                    return render(request, 'Bouncing/Bouncingtest_upload.html', locals())
                else:
                    Bouncing_Mmodule_min = Bouncing_M()
                    Bouncing_Mmodule_min.Customer = Customer
                    Bouncing_Mmodule_min.Project = Project
                    # Bouncing_Mmodule.Phase = Phase
                    Bouncing_Mmodule_min.A_cover = A_cover
                    Bouncing_Mmodule_min.C_cover = C_cover
                    Bouncing_Mmodule_min.D_cover = D_cover
                    Bouncing_Mmodule_min.HS = HS
                    Bouncing_Mmodule_min.Torque = Torque_min
                    Bouncing_Mmodule_min.Push = Push_min
                    Bouncing_Mmodule_min.PV_L = PV_L_min
                    Bouncing_Mmodule_min.PV_R = PV_R_min
                    Bouncing_Mmodule_min.D_L = D_L_min
                    Bouncing_Mmodule_min.D_R = D_R_min
                    Bouncing_Mmodule_min.Conclusion = Conclusion
                    Bouncing_Mmodule_min.editor = request.session.get('user_name')
                    Bouncing_Mmodule_min.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Bouncing_Mmodule_min.save()


                    Bouncing_Mmodule_max = Bouncing_M()
                    Bouncing_Mmodule_max.Customer = Customer
                    Bouncing_Mmodule_max.Project = Project
                    # Bouncing_Mmodule.Phase = Phase
                    Bouncing_Mmodule_max.A_cover = A_cover
                    Bouncing_Mmodule_max.C_cover = C_cover
                    Bouncing_Mmodule_max.D_cover = D_cover
                    Bouncing_Mmodule_max.HS = HS
                    Bouncing_Mmodule_max.Torque = Torque_max
                    Bouncing_Mmodule_max.Push = Push_max
                    Bouncing_Mmodule_max.PV_L = PV_L_max
                    Bouncing_Mmodule_max.PV_R = PV_R_max
                    Bouncing_Mmodule_max.D_L = D_L_max
                    Bouncing_Mmodule_max.D_R = D_R_max
                    Bouncing_Mmodule_max.Conclusion = Conclusion
                    Bouncing_Mmodule_max.editor = request.session.get('user_name')
                    Bouncing_Mmodule_max.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Bouncing_Mmodule_max.save()
                    message_CDM = "Upload Successfully"
                    result = 0
                    # print(request.FILES.getlist('myfiles'))
                    for f in request.FILES.getlist('myfiles'):
                        # print(f)
                        empt = files_BM()
                        # 增加其他字段应分别对应填写
                        empt.single = f
                        empt.files = f
                        empt.save()
                        Bouncing_Mmodule_min.files_B.add(empt)
                        Bouncing_Mmodule_max.files_B.add(empt)
                    # print(message_CDM)
                    return render(request, 'Bouncing/Bouncingtest_upload.html',
                                  {'weizhi': weizhi, 'Skin': Skin, 'buncing_upload': Bouncing(), 'message_CDM': message_CDM,
                                   'result': result})
            else:
                cleanData = buncing_upload.errors
                # print (cleanData)
        return render(request, 'Bouncing/Bouncingtest_upload.html', {'weizhi':weizhi,'Skin':Skin,'buncing_upload': Bouncing(), 'result':result})

    return render(request, 'Bouncing/Bouncingtest_upload.html', locals())
@csrf_exempt
def bouncingtest_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/Bouncing Edit"
    #Lesson_list=lesson_learn.objects.all()
    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (list.Object)
    #     for i in img:
    #         print (i.img)
    mock_data=[
               #  {"id":"123","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"1.0","D_R":"1.8","CON":"PICKUP PROJECT...."},
               # {"id":"124","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
               # {"id":"125","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
               # {"id":"126","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."}
    ]
    selectItem = {
        # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
        # "A39": ["FL531", "FL532", "FL533", "FL534"],
        # "C38(AIO)": ["FL535", "FL536", "FL537", "FL538"],
        # "Other": ["ELMV2", "ELMV3", "ELMV4"],
    }
    Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist

    others={}
    A_cover_list = []
    C_cover_list=[]
    D_cover_list=[]
    HS_list=[]
    Push_list=[]
    for i in Bouncing_M.objects.all().values('A_cover').distinct().order_by('A_cover'):
        A_cover_list.append(i['A_cover'])
    others['A_cover_list'] = A_cover_list
    for i in Bouncing_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
        C_cover_list.append(i['C_cover'])
    others['C_cover_list'] = C_cover_list
    for i in Bouncing_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
        D_cover_list.append(i['D_cover'])
    others['D_cover_list'] = D_cover_list
    for i in Bouncing_M.objects.all().values('HS').distinct().order_by('HS'):
        HS_list.append(i['HS'])
    others['HS_list'] = HS_list
    for i in Bouncing_M.objects.all().values('Push').distinct().order_by('Push'):
        Push_list.append(i['Push'])
    others['Push_list'] = Push_list

    # print (request.POST,request.method,request.POST.get('isGetData'))
    # print(request.method)
    if request.method == "POST" :
        # print(request.POST)
        if request.POST.get('isGetData')=='first':
            for i in Bouncing_M.objects.all():
                file_Blist=[]
                # print(i.file_B.all)
                for j in i.files_B.all():
                    file_Blist.append(str(j.files))

                mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,"C_cover": i.C_cover,
                                  "D_cover": i.D_cover, "Hinge_s": i.HS,
                                  "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                  "D_L": i.D_L,
                                  "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor, 'edit_time': i.edit_time}
                                 )


            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print (data)
            # if request.POST.get("msg") == "axios":
            #     data= {
            #         "err_ok":"0",
            #         #"content":upload
            #     }
            # print (json.dumps(data))
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            A_cover = request.POST.get("a_cover")
            C_cover = request.POST.get("c_cover")
            D_cover = request.POST.get("d_cover")
            HS=request.POST.get('hinge_s')
            Torque = request.POST.get('torque ')
            Push = request.POST.get('p_f ')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if A_cover:
                dic['A_cover'] = A_cover
            if C_cover:
                dic['C_cover'] = C_cover
            if D_cover:
                dic['D_cover'] = D_cover
            if HS:
                dic['HS'] = HS
            if Torque:
                dic['Torque'] = Torque
            if Push:
                dic['Push'] = Push
            request.session['dic_Bouncing'] = dic
            # print(dic)
            if dic:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            else:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            # Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
            # for i in Customer_list:
            #     projectlist=[]
            #     for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            #         projectlist.append(j['Project'])
            #     selectItem[i['Customer']]=projectlist

            # for i in Bouncing_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
            #     C_cover_list.append(i['C_cover'])
            # others['C_cover_list']=C_cover_list
            # for i in Bouncing_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
            #     D_cover_list.append(i['D_cover'])
            # others['D_cover_list']=D_cover_list
            # for i in Bouncing_M.objects.all().values('HS').distinct().order_by('HS'):
            #     HS_list.append(i['HS'])
            # others['HS_list']=HS_list
            # for i in Bouncing_M.objects.all().values('Push').distinct().order_by('Push'):
            #     Push_list.append(i['Push'])
            # others['Push_list']=Push_list
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('isGetData') == 'edit0':
            # print (request.POST)
            # print(request.POST.get('tempdata'))
            # Customer = request.POST.get('customer')
            # Project = request.POST.get('project')
            # Phase = buncing_upload.cleaned_data['Phase']
            ID_num = request.POST.get('id')
            A_cover = request.POST.get('A_cover')
            C_cover = request.POST.get('C_cover')
            D_cover = request.POST.get('D_cover')
            HS = request.POST.get('Hinge_s')
            Torque_min = request.POST.get('Torque')
            # print(Torque_min)
            # print(Torque_max)
            Push = request.POST.get('Push_F')
            PV_L = request.POST.get('PV_L')
            PV_R = request.POST.get('PV_R')
            D_L = request.POST.get('D_L')
            D_R = request.POST.get('D_R')
            Conclusion = request.POST.get('CON')

            Bouncing_Mmodule = Bouncing_M.objects.get(id=ID_num)
            # Bouncing_Mmodule.Customer = Customer
            # Bouncing_Mmodule.Project = Project
            # Bouncing_Mmodule.Phase = Phase
            Bouncing_Mmodule.A_cover = A_cover
            Bouncing_Mmodule.C_cover = C_cover
            Bouncing_Mmodule.D_cover = D_cover
            Bouncing_Mmodule.HS = HS
            Bouncing_Mmodule.Torque = Torque_min
            Bouncing_Mmodule.Push = Push
            Bouncing_Mmodule.PV_L = PV_L
            Bouncing_Mmodule.PV_R = PV_R
            Bouncing_Mmodule.D_L = D_L
            Bouncing_Mmodule.D_R = D_R
            Bouncing_Mmodule.Conclusion = Conclusion
            Bouncing_Mmodule.editor = request.session.get('user_name')
            Bouncing_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Bouncing_Mmodule.save()
            for f in request.FILES.getlist('file'):
                # print(f)
                empt = files_BM()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                Bouncing_Mmodule.files_B.add(empt)

            data = {
                "err_ok": "0",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('isGetData') == 'edit':
            dic = request.session.get('dic_Bouncing', None)
            if dic:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            else:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Bouncing/Bouncingtest_edit.html', locals())

def bouncingtest_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/Bouncing Search"
    #Lesson_list=lesson_learn.objects.all()
    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (list.Object)
    #     for i in img:
    #         print (i.img)
    mock_data = [
        #  {"id":"123","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"1.0","D_R":"1.8","CON":"PICKUP PROJECT...."},
        # {"id":"124","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
        # {"id":"125","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
        # {"id":"126","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."}
    ]
    selectItem = {
        # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
        # "A39": ["FL531", "FL532", "FL533", "FL534"],
        # "C38(AIO)": ["FL535", "FL536", "FL537", "FL538"],
        # "Other": ["ELMV2", "ELMV3", "ELMV4"],
    }
    Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    # print(selectItem)
    others = {}
    A_cover_list = []
    C_cover_list = []
    D_cover_list = []
    HS_list = []
    Push_list = []
    for i in Bouncing_M.objects.all().values('A_cover').distinct().order_by('A_cover'):
        A_cover_list.append(i['A_cover'])
    others['A_cover_list'] = A_cover_list
    for i in Bouncing_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
        C_cover_list.append(i['C_cover'])
    others['C_cover_list'] = C_cover_list
    for i in Bouncing_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
        D_cover_list.append(i['D_cover'])
    others['D_cover_list'] = D_cover_list
    for i in Bouncing_M.objects.all().values('HS').distinct().order_by('HS'):
        HS_list.append(i['HS'])
    others['HS_list'] = HS_list
    for i in Bouncing_M.objects.all().values('Push').distinct().order_by('Push'):
        Push_list.append(i['Push'])
    others['Push_list'] = Push_list
    # print(others)
    # print(request.POST,request.method)
    if request.method == "POST":

        if request.POST.get('isGetData') == 'first':
            for i in Bouncing_M.objects.all():
                file_Blist = []
                # print(i.file_B.all)
                for j in i.files_B.all():
                    file_Blist.append(str(j.files))

                mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                  "C_cover": i.C_cover,
                                  "D_cover": i.D_cover, "Hinge_s": i.HS,
                                  "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                  "D_L": i.D_L,
                                  "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                  'edit_time': i.edit_time}
                                 )

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print (data)
            # if request.POST.get("msg") == "axios":
            #     data= {
            #         "err_ok":"0",
            #         #"content":upload
            #     }
            # print (json.dumps(data))
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            A_cover = request.POST.get("a_cover")
            C_cover = request.POST.get("c_cover")
            D_cover = request.POST.get("d_cover")
            HS = request.POST.get('hinge_s')
            Torque = request.POST.get('torque ')
            Push = request.POST.get('p_f ')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if A_cover:
                dic['A_cover'] = A_cover
            if C_cover:
                dic['C_cover'] = C_cover
            if D_cover:
                dic['D_cover'] = D_cover
            if HS:
                dic['HS'] = HS
            if Torque:
                dic['Torque'] = Torque
            if Push:
                dic['Push'] = Push
            # request.session['dic_Bouncing'] = dic
            # print(dic)
            if dic:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            else:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
            for i in Customer_list:
                projectlist = []
                for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                        'Project'):
                    projectlist.append(j['Project'])
                selectItem[i['Customer']] = projectlist

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Bouncing/Bouncingtest.html', locals())

def bouncingtest_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/Bouncing Export"
    #Lesson_list=lesson_learn.objects.all()
    # for list in Lesson_list:
    #     img=list.Photo.all()
    #     print (list.Object)
    #     for i in img:
    #         print (i.img)
    mock_data = [
        #  {"id":"123","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"1.0","D_R":"1.8","CON":"PICKUP PROJECT...."},
        # {"id":"124","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
        # {"id":"125","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."},
        # {"id":"126","C_cover":"Mg_AL","D_cover":"Mg_AL","Hinge_s":"LH","Torque":"Max","Push_F":"160","PV_L":"9.9","PV_R":"10","D_L":"3.6","D_R":"3.6","CON":"PICKUP PROJECT...."}
    ]
    selectItem = {
        # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
        # "A39": ["FL531", "FL532", "FL533", "FL534"],
        # "C38(AIO)": ["FL535", "FL536", "FL537", "FL538"],
        # "Other": ["ELMV2", "ELMV3", "ELMV4"],
    }
    Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    # print(selectItem)
    others = {}
    A_cover_list = []
    C_cover_list = []
    D_cover_list = []
    HS_list = []
    Push_list = []
    for i in Bouncing_M.objects.all().values('A_cover').distinct().order_by('A_cover'):
        A_cover_list.append(i['A_cover'])
    others['A_cover_list'] = A_cover_list
    for i in Bouncing_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
        C_cover_list.append(i['C_cover'])
    others['C_cover_list'] = C_cover_list
    for i in Bouncing_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
        D_cover_list.append(i['D_cover'])
    others['D_cover_list'] = D_cover_list
    for i in Bouncing_M.objects.all().values('HS').distinct().order_by('HS'):
        HS_list.append(i['HS'])
    others['HS_list'] = HS_list
    for i in Bouncing_M.objects.all().values('Push').distinct().order_by('Push'):
        Push_list.append(i['Push'])
    others['Push_list'] = Push_list
    # print(others)
    # print(request.POST,request.method)
    if request.method == "POST":

        if request.POST.get('isGetData') == 'first':
            for i in Bouncing_M.objects.all():
                file_Blist = []
                # print(i.file_B.all)
                for j in i.files_B.all():
                    file_Blist.append(str(j.files))
                print (file_Blist)

                mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                  "C_cover": i.C_cover,
                                  "D_cover": i.D_cover, "Hinge_s": i.HS,
                                  "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                  "D_L": i.D_L,
                                  "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                  'edit_time': i.edit_time}
                                 )

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print (data)
            # if request.POST.get("msg") == "axios":
            #     data= {
            #         "err_ok":"0",
            #         #"content":upload
            #     }
            # print (json.dumps(data))
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            A_cover = request.POST.get("a_cover")
            C_cover = request.POST.get("c_cover")
            D_cover = request.POST.get("d_cover")
            HS = request.POST.get('hinge_s')
            Torque = request.POST.get('torque ')
            Push = request.POST.get('p_f ')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if A_cover:
                dic['A_cover'] = A_cover
            if C_cover:
                dic['C_cover'] = C_cover
            if D_cover:
                dic['D_cover'] = D_cover
            if HS:
                dic['HS'] = HS
            if Torque:
                dic['Torque'] = Torque
            if Push:
                dic['Push'] = Push
            # request.session['dic_Bouncing'] = dic
            # print(dic)
            if dic:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            else:
                for i in Bouncing_M.objects.all():
                    file_Blist = []
                    # print(i.file_B.all)
                    for j in i.files_B.all():
                        file_Blist.append(str(j.files))

                    mock_data.append({"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "A_cover": i.A_cover,
                                      "C_cover": i.C_cover,
                                      "D_cover": i.D_cover, "Hinge_s": i.HS,
                                      "Torque": i.Torque, "Push_F": i.Push, "PV_L": i.PV_L, "PV_R": i.PV_R,
                                      "D_L": i.D_L,
                                      "D_R": i.D_R, "CON": i.Conclusion, "file_B": file_Blist, 'editor': i.editor,
                                      'edit_time': i.edit_time}
                                     )
            Customer_list = Bouncing_M.objects.all().values('Customer').distinct().order_by('Customer')
            for i in Customer_list:
                projectlist = []
                for j in Bouncing_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                        'Project'):
                    projectlist.append(j['Project'])
                selectItem[i['Customer']] = projectlist

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'Bouncing/Bouncingtest_export.html', locals())