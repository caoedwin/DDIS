
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import CDM
from .forms import CDMform
from django.views.decorators.csrf import csrf_exempt
import datetime,json,simplejson
from functools import reduce
from django.core import serializers
# import datetime,os
# from service.init_permission import init_permission
# from django.conf import settings
# Create your views here.
# from django.forms import forms
# from DjangoUeditor.forms import UEditorField

# from django.conf import settings

# class TestUEditorForm(forms.Form):
#     content = UEditorField('Solution/Action', width=800, height=500,
#                             toolbars="full", imagePath="upimg/", filePath="upfile/",
#                             upload_settings={"imageMaxSize": 1204000},
#                             settings={}, command=None#, blank=True
#                             )


@csrf_exempt
def CDM_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/CDM/Upload"
    CDMforms = CDMform(request.POST)
    CDM_lists = [{'Customer': '客户', 'Project': '专案', 'SKU_NO': '机台', 'A_cover_Material': 'A件',
                             'C_cover_Material': 'C件', 'D_cover_Material': 'D件'}]

    message_err = 0
    # print(request.POST,request.method)
    if request.method == "POST":
        # print(request.POST)
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            n=0

            for i in simplejson.loads(xlsxlist):
                n+=1
                CDM_dic = {}
                # print(i)
                # print (i['Customer'])
                check_dic = {'Customer': i['Customer'], 'Project': i['Project'], 'SKU_NO': i['SKU_NO'], 'A_cover_Material': i['A_cover_Material'],
                             'C_cover_Material': i['C_cover_Material'], 'D_cover_Material': i['D_cover_Material']}
                # print(check_dic)
                check_list = CDM.objects.filter(**check_dic)
                # print (check_list)
                if check_list:
                    err_ok = 1
                    CDM_dic['Customer']=i['Customer']
                    CDM_dic['Project'] = i['Project']
                    CDM_dic['SKU_NO'] = i['SKU_NO']
                    CDM_dic['A_cover_Material'] = i['A_cover_Material']
                    CDM_dic['C_cover_Material'] = i['C_cover_Material']
                    CDM_dic['D_cover_Material'] = i['D_cover_Material']
                    CDM_lists.append(CDM_dic)
                    continue
                else:
                    # print('save')
                    CDMmodule = CDM()
                    CDMmodule.Customer = i['Customer']
                    CDMmodule.Project = i['Project']
                    # CDMmodule.Phase = Phase
                    CDMmodule.SS_Data = i['SS_Data']
                    CDMmodule.A_cover_Material = i['A_cover_Material']
                    CDMmodule.C_cover_Material = i['C_cover_Material']
                    CDMmodule.D_cover_Material = i['D_cover_Material']
                    CDMmodule.SKU_NO = i['SKU_NO']
                    CDMmodule.Point1 = i['Point1']
                    CDMmodule.Point2 = i['Point2']
                    CDMmodule.Point3 = i['Point3']
                    CDMmodule.Point4 = i['Point4']
                    CDMmodule.Point5 = i['Point5']
                    CDMmodule.Point6 = i['Point6']
                    CDMmodule.Point7 = i['Point7']
                    # CDMmodule.Ave = i['Ave']
                    # Ave = CDMforms.cleaned_data['Ave']

                    CDMmodule.Ave = format((i['Point1']+ i['Point2'] + i['Point3'] + i['Point4'] + i['Point5'] + i['Point6'] + i['Point7']) / 7, '.2f')
                    # print ( format((i['Point1']+ i['Point2'] + i['Point3'] + i['Point4'] + i['Point5'] + i['Point6'] + i['Point7']) / 7, '.2f'))
                    CDMmodule.Conclusion = i['Conclusion']
                    CDMmodule.editor = request.session.get('user_name')
                    CDMmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    CDMmodule.save()
                    # print('ttt')
            # if not message_CDM:
            #     message_CDM = "Upload Successfully"
            # print(message_CDM)
            datajason={
                'err_ok':err_ok,
                'content': CDM_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")

        if 'Upload' in request.POST:
            # print('1')
            message_err=0
            if CDMforms.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                # print('t')
                Customer = CDMforms.cleaned_data['Customer']
                Project = CDMforms.cleaned_data['Project']
                # Phase = CDMforms.cleaned_data['Phase']
                SS_Data = CDMforms.cleaned_data['SS_Data']
                A_cover_Material = CDMforms.cleaned_data['A_cover_Material']
                C_cover_Material = CDMforms.cleaned_data['C_cover_Material']
                D_cover_Material = CDMforms.cleaned_data['D_cover_Material']
                SKU_NO = CDMforms.cleaned_data['SKU_NO']
                Point1 = CDMforms.cleaned_data['L1']
                Point2 = CDMforms.cleaned_data['L2']
                Point3 = CDMforms.cleaned_data['L3']
                Point4 = CDMforms.cleaned_data['L4']
                Point5 = CDMforms.cleaned_data['L5']
                Point6 = CDMforms.cleaned_data['L6']
                Point7 = CDMforms.cleaned_data['L7']
                # Ave = CDMforms.cleaned_data['Ave']
                # print(Point7)
                Ave = format((Point1+Point2+Point3+Point4+Point5+Point6+Point7)/7,'.2f')
                # print (Ave)
                Conclusion = CDMforms.cleaned_data['Conclusion']

                check_dic={'Customer':Customer,'Project':Project,'SKU_NO':SKU_NO,'A_cover_Material':A_cover_Material,
                           'C_cover_Material':C_cover_Material,'D_cover_Material':D_cover_Material}
                check_list = CDM.objects.filter(**check_dic)
                if check_list:
                    # message_CDM="%s %s %s (%s,%s) already exist in database, " \
                    #             "please choose Edit if you want to update" % (Customer,Project,SKU_NO,C_cover_Material,D_cover_Material)
                    message_err = 1
                    return render(request, 'CDM/CDM_upload.html', locals())
                else:
                    CDMmodule=CDM()
                    CDMmodule.Customer = Customer
                    CDMmodule.Project = Project
                    # CDMmodule.Phase = Phase
                    CDMmodule.SS_Data = SS_Data
                    CDMmodule.A_cover_Material = A_cover_Material
                    CDMmodule.C_cover_Material = C_cover_Material
                    CDMmodule.D_cover_Material = D_cover_Material
                    CDMmodule.SKU_NO = SKU_NO
                    CDMmodule.Point1 = Point1
                    CDMmodule.Point2 = Point2
                    CDMmodule.Point3 = Point3
                    CDMmodule.Point4 = Point4
                    CDMmodule.Point5 = Point5
                    CDMmodule.Point6 = Point6
                    CDMmodule.Point7 = Point7
                    CDMmodule.Ave=Ave
                    CDMmodule.Conclusion=Conclusion
                    CDMmodule.editor = request.session.get('user_name')
                    CDMmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # print('t')
                    CDMmodule.save()
                    message_CDM = "Upload Successfully"
                    # print(message_CDM)
                    return render(request, 'CDM/CDM_upload.html',
                                  {'weizhi': weizhi, 'Skin': Skin, 'CDMforms': CDMform(), 'message_CDM': message_CDM,
                                   'message_err': message_err})
            else:
                cleanData = CDMforms.errors
                # print (cleanData)
        return render(request, 'CDM/CDM_upload.html', {'weizhi':weizhi,'Skin':Skin,'CDMforms': CDMform(), 'message_err':message_err})

    return render(request, 'CDM/CDM_upload.html', locals())

@csrf_exempt
def CDM_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/CDM/Redit"
    # Customer_list=CDM.objects.all().values('Customer').distinct().order_by('Customer')
    # project_list = CDM.objects.all().values('Project').distinct().order_by('Project')
    # SKU_NO_list = CDM.objects.all().values('SKU_NO').distinct().order_by('SKU_NO')
    # C_cover_Material_list=CDM.objects.all().values('C_cover_Material').distinct().order_by('C_cover_Material')
    # D_cover_Material_list = CDM.objects.all().values('D_cover_Material').distinct().order_by('D_cover_Material')
    # if request.method == "POST":
    #     if 'Search' in request.POST:
    #         Customer = request.POST.get("Customer")
    #         Project = request.POST.get("Project")
    #         SKU_NO = request.POST.get("SKU_NO")
    #         C_cover_Material = request.POST.get("C_cover_Material")
    #         D_cover_Material = request.POST.get("D_cover_Material")
    #         dic = {}
    #         datalist=[]
    #         if Customer:
    #             dic['Customer']=Customer
    #         if Project:
    #             dic['Project'] = Project
    #         if SKU_NO:
    #             dic['SKU_NO'] = SKU_NO
    #         if C_cover_Material:
    #             dic['C_cover_Material'] = C_cover_Material
    #         if D_cover_Material:
    #             dic['D_cover_Material'] = D_cover_Material
    #         request.session['dic_CDM'] = dic
    #         if dic:
    #             CDM_list = CDM.objects.filter(**dic)
    #         else:
    #             CDM_list = CDM.objects.all()
    #         # print (dic)
    #         # print(CDM_list)
    #         # for i in CDM_list:
    #         #     datalist.append(i.toJSON())
    #         # dics = {"data": datalist}
    #         # print(dics)
    #         # CDM_jason={}
    #         # CDM_jason["data"]=list(CDM_list.values())
    #         # print(CDM_jason)
    #
    #
    #
    # else:
    #     dic=request.session.get('dic_CDM', None)
    #     if dic:
    #         CDM_list = CDM.objects.filter(**dic)
    #     else:
    #         CDM_list = CDM.objects.all()
    #
    #
    # # 1
    # # CDM_jason = {}
    # # datalist = serializers.serialize("json", CDM_list)
    # # CDM_jason["data"] = json.loads(datalist)
    # # 2
    # # CDM_jason = {}
    # # datalist = CDM_list.values()
    # # CDM_jason["data"] = list(datalist)
    # # 3
    # # list = []
    # # for province in CDM_list:
    # #     list.append([province.id, province.title])
    # # CDM_jason = {'data': list}
    # # print(CDM_jason)
    # # print (CDM_list.toJSON())
    # # print (CDM_list)
    # # print(CDM_list.values())
    # # print (CDM.objects.get(id=3).toJSON())
    mock_data = [

        ]
    selectItem = {

    }
    Customer_list = CDM.objects.all().values('Customer').distinct().order_by('Customer')
    # for i in Customer_list:
    #     projectlist = []
    #     for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
    #         projectlist.append(j['Project'])
    #     selectItem[i['Customer']] = projectlist
    for i in Customer_list:
        projectlist = {}
        for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            SKUlist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in CDM.objects.filter(**dic).values('SKU_NO').distinct().order_by('SKU_NO'):
                SKUlist.append(m['SKU_NO'])
            projectlist[(j['Project'])] = SKUlist
        selectItem[i['Customer']] = projectlist
    print(selectItem)
    others = {}
    SKU_list = []
    A_cover_list = []
    C_cover_list = []
    D_cover_list = []
    for i in CDM.objects.all().values('SKU_NO').distinct().order_by('SKU_NO'):
        SKU_list.append(i['SKU_NO'])
    others['SKU_list'] = SKU_list
    for i in CDM.objects.all().values('A_cover_Material').distinct().order_by('A_cover_Material'):
        A_cover_list.append(i['A_cover_Material'])
    others['A_cover_list'] = A_cover_list
    for i in CDM.objects.all().values('C_cover_Material').distinct().order_by('C_cover_Material'):
        C_cover_list.append(i['C_cover_Material'])
    others['C_cover_list'] = C_cover_list
    for i in CDM.objects.all().values('D_cover_Material').distinct().order_by('D_cover_Material'):
        D_cover_list.append(i['D_cover_Material'])
    others['D_cover_list'] = D_cover_list

    if request.method == "POST":
        # print(request.POST)
        if request.POST.get('isGetData') == 'first':
            for i in CDM.objects.all():
                # SS_Data_Show="/".join(i.SS_Data.split("-"))[2:]
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                     "A_cover":i.A_cover_Material,"C_cover":i.C_cover_Material,"D_cover":i.D_cover_Material,
                     "L1": i.Point1, "L2": i.Point2,"L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                     "L6": i.Point6,"L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,"SS_Data":i.SS_Data,
                     'Editor': i.editor, 'Edit_Time': i.edit_time}
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
            SKU_NO = request.POST.get("sku")
            A_cover_Material = request.POST.get("a_cover")
            C_cover_Material = request.POST.get("c_cover")
            D_cover_Material = request.POST.get("d_cover")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if SKU_NO:
                dic['SKU_NO'] = SKU_NO
            if A_cover_Material:
                dic['A_cover_Material'] = A_cover_Material
            if C_cover_Material:
                dic['C_cover_Material'] = C_cover_Material
            if D_cover_Material:
                dic['D_cover_Material'] = D_cover_Material

            request.session['dic_CDM'] = dic
            # print(dic)
            if dic:
                for i in CDM.objects.filter(**dic):
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover":i.A_cover_Material,"C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )
            else:
                for i in CDM.objects.all():
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover":i.A_cover_Material,"C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )

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
            A_cover_Material = request.POST.get('A_cover')
            C_cover_Material = request.POST.get('C_cover')
            D_cover_Material = request.POST.get('D_cover')
            SS = request.POST.get('SS_Data')
            # print(SS)
            Point1 = request.POST.get('L1')
            Point2 = request.POST.get('L2')
            Point3 = request.POST.get('L3')
            Point4 = request.POST.get('L4')
            Point5 = request.POST.get('L5')
            Point6 = request.POST.get('L6')
            Point7 = request.POST.get('L7')
            Ave = request.POST.get('Ave')
            Conclusion = request.POST.get('Conclusion')

            CDMmodule = CDM.objects.get(id=ID_num)
            # CDMmodule.Customer = Customer
            # CDMmodule.Project = Project
            # CDMmodule.Phase = Phase
            # CDMmodule.SKU_NO = SKU_NO
            CDMmodule.A_cover_Material = A_cover_Material
            CDMmodule.C_cover_Material = C_cover_Material
            CDMmodule.D_cover_Material = D_cover_Material
            CDMmodule.SS_Data = SS
            CDMmodule.Point1 = Point1
            CDMmodule.Point2 = Point2
            CDMmodule.Point3 = Point3
            CDMmodule.Point4 = Point4
            CDMmodule.Point5 = Point5
            CDMmodule.Point6 = Point6
            CDMmodule.Point7 = Point7
            CDMmodule.Ave = Ave
            CDMmodule.Conclusion = Conclusion
            CDMmodule.editor = request.session.get('user_name')
            CDMmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # print('t')
            CDMmodule.save()

            data = {
                "err_ok": "0",
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('isGetData') == 'edit':
            dic = request.session.get('dic_CDM', None)
            # print(dic)
            if dic:
                for i in CDM.objects.filter(**dic):
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover":i.A_cover_Material,"C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )
            else:
                for i in CDM.objects.all():
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover":i.A_cover_Material,"C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )
            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CDM/CDM_edit.html', locals())

@csrf_exempt
def CDM_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/CDM/Search"
    mock_data = [

    ]
    selectItem = {

    }
    Customer_list = CDM.objects.all().values('Customer').distinct().order_by('Customer')
    # for i in Customer_list:
    #     projectlist = []
    #     for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
    #         projectlist.append(j['Project'])
    #     selectItem[i['Customer']] = projectlist
    for i in Customer_list:
        projectlist = {}
        for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            SKUlist = []
            dic={'Customer':i['Customer'],'Project':j['Project']}
            for m in CDM.objects.filter(**dic).values('SKU_NO').distinct().order_by('SKU_NO'):
                SKUlist.append(m['SKU_NO'])
            projectlist[(j['Project'])]=SKUlist
        selectItem[i['Customer']] = projectlist

    # print(selectItem)
    others = {}
    SKU_list = []
    A_cover_list = []
    C_cover_list = []
    D_cover_list = []
    for i in CDM.objects.all().values('SKU_NO').distinct().order_by('SKU_NO'):
        SKU_list.append(i['SKU_NO'])
    others['SKU_list'] = SKU_list
    for i in CDM.objects.all().values('A_cover_Material').distinct().order_by('A_cover_Material'):
        A_cover_list.append(i['A_cover_Material'])
    others['A_cover_list'] = A_cover_list
    for i in CDM.objects.all().values('C_cover_Material').distinct().order_by('C_cover_Material'):
        C_cover_list.append(i['C_cover_Material'])
    others['C_cover_list'] = C_cover_list
    for i in CDM.objects.all().values('D_cover_Material').distinct().order_by('D_cover_Material'):
        D_cover_list.append(i['D_cover_Material'])
    others['D_cover_list'] = D_cover_list
    # print (request.POST)
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            for i in CDM.objects.all():
                # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                     "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                     "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                     "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion, "SS_Data": i.SS_Data,
                     'Editor': i.editor, 'Edit_Time': i.edit_time}
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
            SKU_NO = request.POST.get("sku")
            A_cover_Material = request.POST.get("a_cover")
            C_cover_Material = request.POST.get("c_cover")
            D_cover_Material = request.POST.get("d_cover")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if SKU_NO:
                dic['SKU_NO'] = SKU_NO
            if A_cover_Material:
                dic['A_cover_Material'] = A_cover_Material
            if C_cover_Material:
                dic['C_cover_Material'] = C_cover_Material
            if D_cover_Material:
                dic['D_cover_Material'] = D_cover_Material

            # request.session['dic_CDM'] = dic
            # print(dic)
            if dic:
                for i in CDM.objects.filter(**dic):
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )
            else:
                for i in CDM.objects.all():
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CDM/CDM_search.html', locals())

@csrf_exempt
def CDM_export(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/CDM/Search"
    mock_data = [

    ]
    selectItem = {

    }
    Customer_list = CDM.objects.all().values('Customer').distinct().order_by('Customer')
    # for i in Customer_list:
    #     projectlist = []
    #     for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
    #         projectlist.append(j['Project'])
    #     selectItem[i['Customer']] = projectlist
    for i in Customer_list:
        projectlist = {}
        for j in CDM.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            SKUlist = []
            dic={'Customer':i['Customer'],'Project':j['Project']}
            for m in CDM.objects.filter(**dic).values('SKU_NO').distinct().order_by('SKU_NO'):
                SKUlist.append(m['SKU_NO'])
            projectlist[(j['Project'])]=SKUlist
        selectItem[i['Customer']] = projectlist

    # print(selectItem)
    others = {}
    SKU_list = []
    A_cover_list = []
    C_cover_list = []
    D_cover_list = []
    for i in CDM.objects.all().values('SKU_NO').distinct().order_by('SKU_NO'):
        SKU_list.append(i['SKU_NO'])
    others['SKU_list'] = SKU_list
    for i in CDM.objects.all().values('A_cover_Material').distinct().order_by('A_cover_Material'):
        A_cover_list.append(i['A_cover_Material'])
    others['A_cover_list'] = A_cover_list
    for i in CDM.objects.all().values('C_cover_Material').distinct().order_by('C_cover_Material'):
        C_cover_list.append(i['C_cover_Material'])
    others['C_cover_list'] = C_cover_list
    for i in CDM.objects.all().values('D_cover_Material').distinct().order_by('D_cover_Material'):
        D_cover_list.append(i['D_cover_Material'])
    others['D_cover_list'] = D_cover_list
    # print (request.POST)
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            for i in CDM.objects.all():
                # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                mock_data.append(
                    {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                     "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                     "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                     "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion, "SS_Data": i.SS_Data,
                     'Editor': i.editor, 'Edit_Time': i.edit_time}
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
            SKU_NO = request.POST.get("sku")
            A_cover_Material = request.POST.get("a_cover")
            C_cover_Material = request.POST.get("c_cover")
            D_cover_Material = request.POST.get("d_cover")

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if SKU_NO:
                dic['SKU_NO'] = SKU_NO
            if A_cover_Material:
                dic['A_cover_Material'] = A_cover_Material
            if C_cover_Material:
                dic['C_cover_Material'] = C_cover_Material
            if D_cover_Material:
                dic['D_cover_Material'] = D_cover_Material

            # request.session['dic_CDM'] = dic
            # print(dic)
            if dic:
                for i in CDM.objects.filter(**dic):
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )
            else:
                for i in CDM.objects.all():
                    # SS_Data_Show = "/".join(i.SS_Data.split("-"))[2:]
                    mock_data.append(
                        {"id": i.id, 'Customer': i.Customer, 'Project': i.Project, "SKU": i.SKU_NO,
                         "A_cover": i.A_cover_Material, "C_cover": i.C_cover_Material, "D_cover": i.D_cover_Material,
                         "L1": i.Point1, "L2": i.Point2, "L3": i.Point3, "L4": i.Point4, "L5": i.Point5,
                         "L6": i.Point6, "L7": i.Point7, "Ave": i.Ave, "Conclusion": i.Conclusion,
                         "SS_Data": i.SS_Data,
                         'Editor': i.editor, 'Edit_Time': i.edit_time}
                    )

            data = {
                "err_ok": "0",
                "content": mock_data,
                "select": selectItem,
                "others": others
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CDM/CDM_export.html', locals())

@csrf_exempt
def CDM_update(request,id):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi="Reliability Test Data/CDM/Redit/%s" % id
    CDM_formdefault = CDM.objects.get(id=id)
    CDMforms = CDMform(request.POST)
    # print(request.POST)
    if request.method == "POST":
        if CDMforms.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
            Customer = CDMforms.cleaned_data['Customer']
            Project = CDMforms.cleaned_data['Project']
            # Phase = CDMforms.cleaned_data['Phase']
            SS_Data = CDMforms.cleaned_data['SS_Data']
            C_cover_Material = CDMforms.cleaned_data['C_cover_Material']
            D_cover_Material = CDMforms.cleaned_data['D_cover_Material']
            SKU_NO = CDMforms.cleaned_data['SKU_NO']
            Point1 = CDMforms.cleaned_data['L1']
            Point2 = CDMforms.cleaned_data['L2']
            Point3 = CDMforms.cleaned_data['L3']
            Point4 = CDMforms.cleaned_data['L4']
            Point5 = CDMforms.cleaned_data['L5']
            Point6 = CDMforms.cleaned_data['L6']
            Point7 = CDMforms.cleaned_data['L7']
            Ave = CDMforms.cleaned_data['Ave']
            Conclusion = CDMforms.cleaned_data['Conclusion']


            CDM_formdefault.Customer = Customer
            CDM_formdefault.Project = Project
            # CDMmodule.Phase = Phase
            CDM_formdefault.SS_Data = SS_Data
            CDM_formdefault.C_cover_Material = C_cover_Material
            CDM_formdefault.D_cover_Material = D_cover_Material
            CDM_formdefault.SKU_NO = SKU_NO
            CDM_formdefault.Point1 = Point1
            CDM_formdefault.Point2 = Point2
            CDM_formdefault.Point3 = Point3
            CDM_formdefault.Point4 = Point4
            CDM_formdefault.Point5 = Point5
            CDM_formdefault.Point6 = Point6
            CDM_formdefault.Point7 = Point7
            CDM_formdefault.Ave = Ave
            CDM_formdefault.Conclusion = Conclusion
            CDM_formdefault.editor = request.session.get('user_name')
            CDM_formdefault.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            CDM_formdefault.save()
            return redirect('/CDM/CDM-edit/')
        else:
            cleanData = CDMforms.errors
    else:
        values = {'Customer': CDM_formdefault.Customer, 'Project': CDM_formdefault.Project,
                  'SKU_NO': CDM_formdefault.SKU_NO, 'SS_Data': CDM_formdefault.SS_Data, 'C_cover_Material': CDM_formdefault.C_cover_Material,
                  'D_cover_Material': CDM_formdefault.D_cover_Material,'L1': CDM_formdefault.Point1,'L2': CDM_formdefault.Point2,
                  'L3': CDM_formdefault.Point3,'L4': CDM_formdefault.Point4,'L5': CDM_formdefault.Point5,'L6': CDM_formdefault.Point6,
                  'L7': CDM_formdefault.Point7,'Ave': CDM_formdefault.Ave,'Conclusion': CDM_formdefault.Conclusion}
        CDMforms = CDMform(values)
    return render(request, 'CDM/CDM_update.html', locals())

