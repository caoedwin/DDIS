from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os,simplejson
from .forms import package0
from .models import Package_M,files_PM
from django.http import HttpResponse
import json
# class TestUEditorForm(forms.Form):
#     content = UEditorField('Solution/Action', width=800, height=500,
#                             toolbars="full", imagePath="upimg/", filePath="upfile/",
#                             upload_settings={"imageMaxSize": 1204000},
#                             settings={}, command=None#, blank=True
#                             )


@csrf_exempt

def Package_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Package G-value record /Upload"
    package_upload=package0(request.POST)
    # for list in Lesson_list:
    #     img=list.file.all()
    #     print (list.Object)
    #     for i in img:
    #         print (i.img)
    Package_M_lists = [{'Customer': '客户', 'Project': '专案','Pattern':'包装方式'}]
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
                Package_M_dic = {}
                # print(i)
                # print (i['Customer'])
                check_dic = {'Customer': i['Customer'], 'Project': i['Project'],'Pattern': i['Pattern']}
                # print(check_dic)
                check_list = Package_M.objects.filter(**check_dic)
                # print (check_list)
                if check_list:
                    err_ok = 1
                    Package_M_dic['Customer'] = i['Customer']
                    Package_M_dic['Project'] = i['Project']
                    Package_M_dic['Pattern'] = i['Pattern']
                    # print(Package_M_dic)
                    Package_M_lists.append(Package_M_dic)
                    # print(Package_M_lists)
                    # continue
                else:
                    # print(i['Pattern'])
                    Package_Mmodule = Package_M()
                    Package_Mmodule.Customer = i['Customer']
                    Package_Mmodule.Project = i['Project']
                    Package_Mmodule.Phase = 'C(SIT)'
                    Package_Mmodule.Degree = i['angle']
                    Package_Mmodule.Duan = i['short']#biaoqian
                    Package_Mmodule.Zhong = i['middle']
                    Package_Mmodule.Chang = i['long']
                    Package_Mmodule.Left = i['left']
                    Package_Mmodule.Right = i['right']
                    Package_Mmodule.Top = i['top']
                    Package_Mmodule.Bottom = i['bottom']
                    Package_Mmodule.Zheng = i['front']
                    Package_Mmodule.Fan = i['behind']
                    Package_Mmodule.Pattern = i['Pattern']
                    Package_Mmodule.Conclusion = i['Conclusion']
                    Package_Mmodule.editor = request.session.get('user_name')
                    Package_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Package_Mmodule.save()
                    # print('ttt')
            # if not message_Package_M:
            #     message_Package_M = "Upload Successfully"
            # print(message_Package_M)
            datajason = {
                'err_ok': err_ok,
                'content': Package_M_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if 'Upload' in request.POST:
            # print('1')
            if package_upload.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                # print(package_upload.cleaned_data)
                Customer = package_upload.cleaned_data['Customer']
                Project = package_upload.cleaned_data['Project']
                # print(Customer,Project)
                Phase = package_upload.cleaned_data['Phase']
                Degree = package_upload.cleaned_data['degree']
                Duan = package_upload.cleaned_data['duan']
                Zhong = package_upload.cleaned_data['zhong']
                Chang = package_upload.cleaned_data['chang']
                Left = package_upload.cleaned_data['left']
                # print(Torque_min)
                # print(Torque_max)
                Right = package_upload.cleaned_data['right']
                Top = package_upload.cleaned_data['top']
                Bottom = package_upload.cleaned_data['bottom']
                Zheng = package_upload.cleaned_data['zheng']
                Fan = package_upload.cleaned_data['fan']
                Pattern = package_upload.cleaned_data['Pattern']
                Conclusion = request.POST.get('Conclusion')
                file = request.FILES.getlist("myfiles", "")


                check_dic = {'Customer': Customer, 'Project': Project, 'Pattern': Pattern}
                check_list = Package_M.objects.filter(**check_dic)
                if check_list:
                    # message_CDM="%s %s %s (%s,%s) already exist in database, " \
                    #             "please choose Edit if you want to update" % (Customer,Project,SKU_NO,C_cover_Material,D_cover_Material)
                    result = 1
                    return render(request, 'Package/Package_upload.html', locals())
                else:
                    Package_Mmodule = Package_M()
                    Package_Mmodule.Customer = Customer
                    Package_Mmodule.Project = Project
                    Package_Mmodule.Phase = Phase
                    Package_Mmodule.Degree = Degree
                    Package_Mmodule.Duan = Duan
                    Package_Mmodule.Zhong = Zhong
                    Package_Mmodule.Chang = Chang
                    Package_Mmodule.Left = Left
                    Package_Mmodule.Right = Right
                    Package_Mmodule.Top = Top
                    Package_Mmodule.Bottom = Bottom
                    Package_Mmodule.Zheng = Zheng
                    Package_Mmodule.Fan = Fan
                    Package_Mmodule.Pattern = Pattern
                    Package_Mmodule.Conclusion = Conclusion
                    Package_Mmodule.editor = request.session.get('user_name')
                    Package_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Package_Mmodule.save()
                    # print (request.FILES.getlist('myfiles'))
                    for f in request.FILES.getlist('myfiles'):
                        # print(f)
                        empt = files_PM()
                        # 增加其他字段应分别对应填写
                        empt.single = f
                        empt.files = f
                        empt.save()
                        Package_Mmodule.files_P.add(empt)

                    result = 0
                    # print()
                    return render(request, 'Package/Package_upload.html',
                                  {'weizhi': weizhi, 'Skin': Skin, 'package_upload': package0(),
                                   'result': result})
            else:
                cleanData = Package_upload.errors
                # print (cleanData)
        return render(request, 'Package/Package_upload.html',
                      {'weizhi': weizhi, 'Skin': Skin, 'package_upload': package0(), 'result': result})

    return render(request, 'Package/Package_upload.html', locals())
@csrf_exempt
def package_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Package G-value record /Edit"
    mock_data = [
        # {"Project": "DLME1", "angle": "23.53", "short": "33.62", "middle": "33.66", "long": "77.84", "left": "41.63","right": "84.37", "top": "44.58", "bottom": "36.22", "front": "262.69", "behind": "225.27", "Remark": "有second battery設計，D件會比較薄弱，造成整體結構比較弱，has risk。"},
        ]
    selectItem = {
                  # "C38(NB)": ["EL531", "EL532", "EL533", "EL534"],
                  # "A39": ["FL531", "FL532", "FL533", "FL534"],
                  # "C38(AIO)": ["FL535", "FL536", "FL537", "FL538"],
                  # "Other": ["ELMV2", "ELMV3", "ELMV4"],
                  }
    Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    others = {}
    Patternlist = []
    for i in Package_M.objects.all().values('Pattern').distinct().order_by('Pattern'):
        Patternlist.append(i['Pattern'])
    others['Pattern'] = Patternlist
    if request.method == "POST":
        if request.POST.get('isGetData')=='first':
            for i in Package_M.objects.all():
                file_Plist=[]
                # print(i.file_P.all)
                for j in i.files_P.all():
                    file_Plist.append(str(j.files))
                    # print(j.img)
                # print(file_P)
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                     "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                     "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                     "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                     "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                     'Edit_Time': i.edit_time}
                                 )
                # print(mock_data)

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            Pattern = request.POST.get("pattern")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Pattern:
                dic['Pattern'] = Pattern

            request.session['dic_Package'] = dic
            # print(dic)
            if dic:
                for i in Package_M.objects.filter(**dic):
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            else:
                for i in Package_M.objects.all():
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
            for i in Customer_list:
                projectlist=[]
                for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
                    projectlist.append(j['Project'])
                selectItem[i['Customer']]=projectlist

            # for i in Package_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
            #     C_cover_list.append(i['C_cover'])
            # others['C_cover_list']=C_cover_list
            # for i in Package_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
            #     D_cover_list.append(i['D_cover'])
            # others['D_cover_list']=D_cover_list
            # for i in Package_M.objects.all().values('HS').distinct().order_by('HS'):
            #     HS_list.append(i['HS'])
            # others['HS_list']=HS_list
            # for i in Package_M.objects.all().values('Push').distinct().order_by('Push'):
            #     Push_list.append(i['Push'])
            # others['Push_list']=Push_list
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('isGetData') == 'edit0':
            # print (request.POST)
            # print(request.POST.get('tempdata'))
            # Customer = request.POST.get('customer')
            # Project = request.POST.get('project')
            # Phase = buncing_upload.cleaned_data['Phase']
            ID_num = request.POST.get('id')
            Degree = request.POST.get('angle')
            Duan = request.POST.get('short')
            Zhong = request.POST.get('middle')
            Chang = request.POST.get('long')
            Left = request.POST.get('left')
            Right = request.POST.get('right')
            Top = request.POST.get('top')
            Bottom = request.POST.get('bottom')
            Zheng = request.POST.get('front')
            Fan = request.POST.get('behind')
            Pattern = request.POST.get('Pattern')
            Conclusion = request.POST.get('Remark')
            # file=request.files.get('file')
            # print (file)

            Package_Mmodule = Package_M.objects.get(id=ID_num)
            # Package_Mmodule.Customer = Customer
            # Package_Mmodule.Project = Project
            # Package_Mmodule.Phase = Phase
            Package_Mmodule.Degree = Degree
            Package_Mmodule.Duan = Duan
            Package_Mmodule.Zhong = Zhong
            Package_Mmodule.Chang = Chang
            Package_Mmodule.Left = Left
            Package_Mmodule.Right = Right
            Package_Mmodule.Top = Top
            Package_Mmodule.Bottom = Bottom
            Package_Mmodule.Zheng = Zheng
            Package_Mmodule.Fan = Fan
            Package_Mmodule.Pattern = Pattern
            Package_Mmodule.Conclusion = Conclusion
            Package_Mmodule.editor = request.session.get('user_name')
            Package_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Package_Mmodule.save()
            # print(request.FILES.getlist('file'))
            for f in request.FILES.getlist('file'):
                # print(f)
                empt = files_PM()
                # 增加其他字段应分别对应填写
                empt.single = f
                empt.files = f
                empt.save()
                Package_Mmodule.files_P.add(empt)

            data = {
                "err_ok": "0",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('isGetData') == 'edit':
            dic = request.session.get('dic_Package', None)
            if dic:
                for i in Package_M.objects.filter(**dic):
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            else:
                for i in Package_M.objects.all():
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'Package/package_edit.html', locals())

@csrf_exempt
def Package_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Package G-value record /Search"
    mock_data = [

        ]
    selectItem = {

    }
    Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    others = {}
    Patternlist = []
    for i in Package_M.objects.all().values('Pattern').distinct().order_by('Pattern'):
        Patternlist.append(i['Pattern'])
    others['Pattern'] = Patternlist
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            for i in Package_M.objects.all():
                file_Plist = []
                # print(i.file_P.all)
                for j in i.files_P.all():
                    file_Plist.append(str(j.files))
                    # print(j.img)
                # print(file_P)
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                     "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                     "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                     "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                     "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                     'Edit_Time': i.edit_time}
                )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            Pattern = request.POST.get("pattern")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Pattern:
                dic['Pattern'] = Pattern

            # request.session['dic_Package'] = dic
            # print(dic)
            if dic:
                for i in Package_M.objects.filter(**dic):
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            else:
                for i in Package_M.objects.all():
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
            for i in Customer_list:
                projectlist = []
                for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                        'Project'):
                    projectlist.append(j['Project'])
                selectItem[i['Customer']] = projectlist

            # for i in Package_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
            #     C_cover_list.append(i['C_cover'])
            # others['C_cover_list']=C_cover_list
            # for i in Package_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
            #     D_cover_list.append(i['D_cover'])
            # others['D_cover_list']=D_cover_list
            # for i in Package_M.objects.all().values('HS').distinct().order_by('HS'):
            #     HS_list.append(i['HS'])
            # others['HS_list']=HS_list
            # for i in Package_M.objects.all().values('Push').distinct().order_by('Push'):
            #     Push_list.append(i['Push'])
            # others['Push_list']=Push_list
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request,'Package/Package_search.html',locals())

@csrf_exempt
def Package_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Package G-value record /Search"
    mock_data = [

        ]
    selectItem = {

    }
    Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        projectlist = []
        for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            projectlist.append(j['Project'])
        selectItem[i['Customer']] = projectlist
    others = {}
    Patternlist = []
    for i in Package_M.objects.all().values('Pattern').distinct().order_by('Pattern'):
        Patternlist.append(i['Pattern'])
    others['Pattern'] = Patternlist
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            for i in Package_M.objects.all():
                file_Plist = []
                # print(i.file_P.all)
                for j in i.files_P.all():
                    file_Plist.append(str(j.files))
                    # print(j.img)
                # print(file_P)
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                     "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                     "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                     "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                     "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                     'Edit_Time': i.edit_time}
                )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            # print(data)
            return HttpResponse(json.dumps(data), content_type="application/json")
        if not request.POST.get('isGetData'):
            Customer = request.POST.get("customer")
            Project = request.POST.get("project")
            Pattern = request.POST.get("pattern")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Pattern:
                dic['Pattern'] = Pattern

            # request.session['dic_Package'] = dic
            # print(dic)
            if dic:
                for i in Package_M.objects.filter(**dic):
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            else:
                for i in Package_M.objects.all():
                    file_Plist = []
                    # print(i.file_P.all)
                    for j in i.files_P.all():
                        file_Plist.append(str(j.files))
                        # print(j.img)
                    # print(file_P)
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "Pattern": i.Pattern,
                         "angle": i.Degree, "short": i.Duan, "middle": i.Zhong,
                         "long": i.Chang, "left": i.Left, "right": i.Right, "top": i.Top,
                         "bottom": i.Bottom, "front": i.Zheng, "behind": i.Fan,
                         "Remark": i.Conclusion, "file_P": file_Plist, 'Editor': i.editor,
                         'Edit_Time': i.edit_time}
                    )
            Customer_list = Package_M.objects.all().values('Customer').distinct().order_by('Customer')
            for i in Customer_list:
                projectlist = []
                for j in Package_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by(
                        'Project'):
                    projectlist.append(j['Project'])
                selectItem[i['Customer']] = projectlist

            # for i in Package_M.objects.all().values('C_cover').distinct().order_by('C_cover'):
            #     C_cover_list.append(i['C_cover'])
            # others['C_cover_list']=C_cover_list
            # for i in Package_M.objects.all().values('D_cover').distinct().order_by('D_cover'):
            #     D_cover_list.append(i['D_cover'])
            # others['D_cover_list']=D_cover_list
            # for i in Package_M.objects.all().values('HS').distinct().order_by('HS'):
            #     HS_list.append(i['HS'])
            # others['HS_list']=HS_list
            # for i in Package_M.objects.all().values('Push').distinct().order_by('Push'):
            #     Push_list.append(i['Push'])
            # others['Push_list']=Push_list
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request,'Package/Package_export.html',locals())