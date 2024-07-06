from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime, os

from .forms import ABODriverList
from .forms import ABOToolList
from .models import ABODriverList_M, ABOToolList_M
from CQM.models import CQMProject
from ABOProjectLessonL.models import ABOTestProjectLL
from app01.models import ProjectinfoinDCT, UserInfo
from LessonProjectME.models import TestProjectLL
# from .models import ABODriverList_M
# from .models import ABOToolList_M
from django.http import HttpResponse
import datetime, json, simplejson, requests, time
from requests_ntlm import HttpNtlmAuth


# Create your views here.
@csrf_exempt
def ABODriverList_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
        weizhi = "XQM/ABODriverList_upload"
    ABODriverList_M_lists = ABODriverList(request.POST)
    result = '00'
    Existlist = [{'Customer': 'Customer', 'Project': 'Project', 'Phase0': 'Phase',
                  'Name': 'Driver/Utility/Firmware/Application Name',
                  'Function': 'Function', 'Vendor': 'Vendor', 'Version': 'Version', 'Bios': 'Bios', 'Image': 'Image',
                  'Driver': 'Driver'}]
    ABODriverList_M_dic = {}
    result = 4

    if request.method == "POST":
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            n = 0

            for i in simplejson.loads(xlsxlist):
                n += 1
                # print(i)
                if 'Customer' in i.keys():
                    Customer = i['Customer']
                else:
                    Customer = ''
                if 'Project' in i.keys():
                    Project = i['Project']
                else:
                    Project = ''
                if 'Phase' in i.keys():
                    Phase0 = i['Phase']
                else:
                    Phase0 = ''
                if 'Driver/Utility/Firmware/Application Name' in i.keys():
                    Name = i['Driver/Utility/Firmware/Application Name']
                else:
                    Name = ''
                if 'Function' in i.keys():
                    Function = i['Function']
                else:
                    Function = ''
                if 'Vendor' in i.keys():
                    Vendor = i['Vendor']
                else:
                    Vendor = ''
                if 'Version' in i.keys():
                    Version = i['Version']
                else:
                    Version = ''
                if 'BIOS' in i.keys():
                    Bios = i['BIOS']
                else:
                    Bios = ''
                if 'Image' in i.keys():
                    Image = i['Image']
                else:
                    Image = ''
                if 'Driver' in i.keys():
                    Driver = i['Driver']
                else:
                    Driver = ''
                # print(len(Version))
                # print(Driver)
                check_dic = {'Customer': Customer, 'Project': Project, 'Phase0': Phase0, 'Name': Name,
                             'Function': Function, 'Vendor': Vendor, 'Version': Version, 'BIOS': Bios, 'Image': Image,
                             'Driver': Driver}
                check_list = ABODriverList_M.objects.filter(**check_dic)
                if check_list:
                    err_ok = 1
                    ABODriverList_M_dic['Customer'] = Customer
                    ABODriverList_M_dic['Project'] = Project
                    ABODriverList_M_dic['Phase0'] = Phase0
                    ABODriverList_M_dic['Name'] = Name
                    ABODriverList_M_dic['Function'] = Function
                    ABODriverList_M_dic['Vendor'] = Vendor
                    ABODriverList_M_dic['Version'] = Version
                    ABODriverList_M_dic['BIOS'] = Bios
                    ABODriverList_M_dic['Image'] = Image
                    ABODriverList_M_dic['Driver'] = Driver
                    Existlist.append(ABODriverList_M_dic)
                    continue
                else:
                    ABODriverList_Mmodule = ABODriverList_M()
                    ABODriverList_Mmodule.Customer = Customer
                    ABODriverList_Mmodule.Project = Project
                    ABODriverList_Mmodule.Phase0 = Phase0
                    ABODriverList_Mmodule.Name = Name
                    ABODriverList_Mmodule.Function = Function
                    ABODriverList_Mmodule.Vendor = Vendor
                    ABODriverList_Mmodule.Version = Version
                    ABODriverList_Mmodule.BIOS = Bios
                    ABODriverList_Mmodule.Image = Image
                    ABODriverList_Mmodule.Driver = Driver
                    ABODriverList_Mmodule.editor = request.session.get('user_name')
                    ABODriverList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ABODriverList_Mmodule.save()
            datajason = {
                'err_ok': err_ok,
                'content': Existlist
            }
            # print(datajason)
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if 'Upload' in request.POST:
            if ABODriverList_M_lists.is_valid():
                Customer = ABODriverList_M_lists.cleaned_data['Customer']
                Project = ABODriverList_M_lists.cleaned_data['Project']
                Phase0 = ABODriverList_M_lists.cleaned_data['Phase0']
                Name = ABODriverList_M_lists.cleaned_data['Name']
                Function = ABODriverList_M_lists.cleaned_data['Function']
                Vendor = ABODriverList_M_lists.cleaned_data['Vendor']
                Version = ABODriverList_M_lists.cleaned_data['Version']
                Bios = ABODriverList_M_lists.cleaned_data['Bios']
                Image = ABODriverList_M_lists.cleaned_data['Image']
                Driver = ABODriverList_M_lists.cleaned_data['Driver']

                check_dic = {'Customer': Customer, 'Project': Project, 'Phase0': Phase0, 'Name': Name,
                             'Function': Function,
                             'Vendor': Vendor, 'Version': Version, 'BIOS': Bios, 'Image': Image, 'Driver': Driver}
                if ABODriverList_M.objects.filter(**check_dic):
                    result = 1
                else:
                    ABODriverList_Mmodule = ABODriverList_M()
                    ABODriverList_Mmodule.Customer = Customer
                    ABODriverList_Mmodule.Project = Project
                    ABODriverList_Mmodule.Phase0 = Phase0
                    ABODriverList_Mmodule.Name = Name
                    ABODriverList_Mmodule.Function = Function
                    ABODriverList_Mmodule.Vendor = Vendor
                    ABODriverList_Mmodule.Version = Version
                    ABODriverList_Mmodule.BIOS = Bios
                    ABODriverList_Mmodule.Image = Image
                    ABODriverList_Mmodule.Driver = Driver
                    ABODriverList_Mmodule.editor = request.session.get('user_name')
                    ABODriverList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ABODriverList_Mmodule.save()
                    result = 0
            else:
                cleanData = ABODriverList_M_lists.errors
        ABODriverList_M_lists = ABODriverList()
        return render(request, 'DriverTool/ABODriverList_upload.html', locals())
    return render(request, 'ABODriverTool/ABODriverList_upload.html', locals())


@csrf_exempt
def ABODriverList_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/ABODriverList_edit"
    # status='0'
    mock_data = [
        # {'id': 1, "Name": "Intel Serial I/O driver", "Function": "I/O", "Vendor": "Intel","Version": "Inbox","Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 2, "Name": "Intel WinPE Serial I/O driver", "Function": "I/O", "Vendor": "Intel","Version": "30.100.1727.1", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 3, "Name": "Intel Chipset driver", "Function": "Chipset", "Vendor": "Intel","Version": "10.1.17809.8096(DM:10.1.15.5)", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 4, "Name": "Intel Rapid Storage Technology driver", "Function": "IRST", "Vendor": "Intel","Version": "17.0.0.1072", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 5, "Name": "Intel WinRE Rapid Storage TechnologyO driver", "Function": "IRST", "Vendor": "Intel","Version": "17.0.0.1072", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 6, "Name": "Intel Management Engine Interface driver", "Function": "MEI", "Vendor": "Intel","Version": "1851.12.0.1193(CSME:12.0.23.1311)", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 7, "Name": "Intel Dynamic Platform Thermal driver", "Function": "DPTF", "Vendor": "Intel","Version": "8.5.10103.7263", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"},
        #          {'id': 8, "Name": "Intel Dynamic Platform Thermal Framework driver", "Function": "ISST", "Vendor": "Intel","Version": "10.23.0.2241", "Project": "EL451_S540-14IWL", "Driver": "V1.11", "Image": "v25 GML"}
    ]
    selectItem = {
        # "C38(NB)": [{"Project": "EL531", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL532", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL533", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL534", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "C38(AIO)": [{"Project": "EL535", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL536", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL537", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL538", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "A39": [{"Project": "EL531", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL532", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL533", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL534", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "Other": [{"Project": "ELMV2", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                     {"Project": "ELMV3", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                     {"Project": "ELMV4", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}]
    }

    dr = [
        # {"Driver": "v0.8"}, {"Driver": "v1.0"}, {"Driver": "v1.11"}
    ]
    image = [
        # {"Image": "v24.1 GMl"}, {"Image": "v22.0 GMl"}
    ]
    canEdit = 0

    for i in ABODriverList_M.objects.all().values('Customer').distinct().order_by('Customer'):
        Customerlist = []
        # print(type(i))
        for j in ABODriverList_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectlist = {}

            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            Phaselist = []
            for l in ABODriverList_M.objects.filter(**dic).values('Phase0').distinct().order_by('Phase0'):
                Phaselist.append(l['Phase0'])
            Projectlist['Project'] = j["Project"]
            Projectlist['Phase0'] = Phaselist
            Customerlist.append(Projectlist)
        selectItem[i['Customer']] = Customerlist

    if request.method == "POST":

        # print(request.POST, request.method)
        # print(request.body)
        # print(type(request.body),type(request.POST))
        # responseData = json.loads(request.body)
        # print(responseData)
        # if request.POST.get('isGetData') == 'first':

        # test = request.POST
        # for i in test:
        #     print(test[i])
        if request.POST.get('isGetData') == 'PHASE':
            dic_phase = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),
                         'Phase0': request.POST.get('Phase')}
            # print(dic_phase)
            for i in ABODriverList_M.objects.filter(**dic_phase).values('Driver').distinct().order_by('Driver'):
                # print(i)
                dr.append({'Driver': i['Driver']})
            for i in ABODriverList_M.objects.filter(**dic_phase).values('Image').distinct().order_by('Image'):
                # print(i)
                image.append({'Image': i['Image']})
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            Driver = request.POST.get('Driver')
            Image = request.POST.get('Image')
            check_Owner_dic = {"Customer": Customer, "Project": Project}
            Projectinfo_CQM = ABOTestProjectLL.objects.filter(**check_Owner_dic)
            Projectinfo_LL = TestProjectLL.objects.filter(**check_Owner_dic)
            current_user = request.session.get('user_name')
            if Projectinfo_CQM:
                for i in Projectinfo_CQM:
                    for k in i.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
            if canEdit == 0 and Projectinfo_LL:
                for i in Projectinfo_LL:
                    for k in i.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            if Driver:
                dic['Driver'] = Driver
                # print(Driver,len(Driver))
            if Image:
                dic['Image'] = Image
            for i in ABODriverList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
                                  "Version": i.Version, "Project": i.Project, "Bios": i.BIOS, "Driver": i.Driver,
                                  "Image": i.Image, 'Customer': i.Customer, 'Phase': i.Phase0, })

        if request.POST.get('isGetData') == 'SAVE':
            # print(request.POST)
            id = request.POST.get('rows[id]')
            ABODriverList_Mmodule = ABODriverList_M.objects.get(id=id)
            ABODriverList_Mmodule.Customer = request.POST.get('rows[Customer]')
            ABODriverList_Mmodule.Project = request.POST.get('rows[Project]')
            ABODriverList_Mmodule.Phase0 = request.POST.get('rows[Phase]')
            ABODriverList_Mmodule.Name = request.POST.get('rows[Name]')
            ABODriverList_Mmodule.Function = request.POST.get('rows[Function0]')
            ABODriverList_Mmodule.Vendor = request.POST.get('rows[Vendor]')
            ABODriverList_Mmodule.Version = request.POST.get('rows[Version]')
            ABODriverList_Mmodule.BIOS = request.POST.get('rows[Bios]')
            ABODriverList_Mmodule.Image = request.POST.get('rows[Image]')
            ABODriverList_Mmodule.Driver = request.POST.get('rows[Driver]')
            ABODriverList_Mmodule.editor = request.session.get('user_name')
            ABODriverList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ABODriverList_Mmodule.save()

            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            Driver = request.POST.get('Driver')
            Image = request.POST.get('Image')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            if Driver:
                dic['Driver'] = Driver
            if Image:
                dic['Image'] = Image
            for i in ABODriverList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
                                  "Version": i.Version, "Project": i.Project, "Bios": i.BIOS, "Driver": i.Driver,
                                  "Image": i.Image,
                                  'Customer': i.Customer, 'Phase': i.Phase0, })
        if request.POST.get('isGetData') == 'DELETE':
            # print(request.POST)
            id = request.POST.get('id')
            ABODriverList_Mmodule = ABODriverList_M.objects.get(id=id)
            ABODriverList_Mmodule.delete()
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            Driver = request.POST.get('Driver')
            Image = request.POST.get('Image')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            if Driver:
                dic['Driver'] = Driver
            if Image:
                dic['Image'] = Image
            for i in ABODriverList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
                                  "Version": i.Version, "Project": i.Project, "Bios": i.BIOS, "Driver": i.Driver,
                                  "Image": i.Image,
                                  'Customer': i.Customer, 'Phase': i.Phase0, })
        if 'MUTICANCEL' in str(request.body):
            responseData = json.loads(request.body)
            # print(responseData)
            for i in responseData['params']:
                ABODriverList_M.objects.get(id=i).delete()
            Customer = responseData['Customer']
            Project = responseData['Project']
            Phase = responseData['Phase']
            Driver = responseData['Driver']
            Image = responseData['Image']
            # print(Customer,Project)
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            if Driver:
                dic['Driver'] = Driver
            if Image:
                dic['Image'] = Image
            # print(dic)
            for i in ABODriverList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
                                  "Version": i.Version, "Project": i.Project, "Bios": i.BIOS, "Driver": i.Driver,
                                  "Image": i.Image,
                                  'Customer': i.Customer, 'Phase': i.Phase0, })
            # status='1'
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "selectedDriver": dr,
            "selectedImage": image,
            "canEdit": canEdit,
            # "status":status
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ABODriverTool/ABODriverList_edit.html', locals())


@csrf_exempt
def ABODriverList_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/ABODriverList_search"

    mock_data = [
        # {"Name": "Intel Serial I/O driver", "Function": "I/O", "Vendor": "Intel", "Version": "Inbox","Project": "EL451_S540-14IWL", "Driver": "v1.11", "Image": "v25 GM1"},
        #          {"Name": "Intel WinPE Serial I/O driver", "Function": "I/O", "Vendor": "Intel","Version": "30.100.1727.1", "Project": "EL451_S540-14IWL", "Driver": "v1.11", "Image": "v25 GM1"},
        #          {"Name": "Intel Chipset driver", "Function": "Chipset", "Vendor": "Intel","Version": "10.1.17809.8096(DM:10.1.15.5)", "Project": "EL451_S540-14IWL", "Driver": "v1.11","Image": "v25 GM1"},
        #          {"Name": "Intel Rapid Storage Technology driver", "Function": "IRST", "Vendor": "Intel","Version": "17.0.0.1072", "Project": "EL451_S540-14IWL", "Driver": "v1.11", "Image": "v25 GM1"},
        #          {"Name": "Intel WinRE Rapid Storage Technology driver", "Function": "IRST", "Vendor": "Intel","Version": "17.0.0.1072", "Project": "EL451_S540-14IWL", "Driver": "v1.11", "Image": "v25 GM1"},
        #          {"Name": "Intel Management Engine Interface driver", "Function": "MEI", "Vendor": "Intel","Version": "1851.12.0.1193", "Project": "EL451_S540-14IWL", "Driver": "v1.11","Image": "v25 GM1"},
        #          {"Name": "Intel Dynamic Platform Thermal Framework driver", "Function": "DPTF", "Vendor": "Intel","Version": "8.5.10103.7263", "Project": "EL451_S540-14IWL", "Driver": "v1.11","Image": "v25 GM1"}
    ]

    selectItem = {
        # "C38(NB)":[{"Project":"EL531", "Phase0":["B(FVT)","C(SIT)","INV"]},{"Project":"EL532","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL533","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL534","Phase0":["B(FVT)","C(SIT)","INV"]}],
        #           "C38(AIO)":[{"Project":"EL535", "Phase0":["B(FVT)","C(SIT)","INV"]},{"Project":"EL536","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL537","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL538","Phase0":["B(FVT)","C(SIT)","INV"]}],
        #           "A39": [{"Project":"EL531", "Phase0":["B(FVT)","C(SIT)","INV"]},{"Project":"EL532","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL533","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"EL534","Phase0":["B(FVT)","C(SIT)","INV"]}],
        #           "Other":[{"Project":"ELMV2", "Phase0":["B(FVT)","C(SIT)","INV"]},{"Project":"ELMV3","Phase0":["B(FVT)","C(SIT)","INV"]}, {"Project":"ELMV4","Phase0":["B(FVT)","C(SIT)","INV"]}]
    }
    sear = []
    # dr=[{"Driver":"v0.8"},{"Driver":"v1.0"},{"Driver":"v1.11"}],
    dr = [
        # {"Driver":"v0.8"},{"Driver":"v1.0"},{"Driver":"v1.11"}
    ]
    image = [
        # {"Image":"v24.1 GMl"},{"Image":"v22.0 GMl"}
    ]
    for i in ABODriverList_M.objects.all().values('Customer').distinct().order_by('Customer'):
        Customerlist = []
        # print(type(i))
        for j in ABODriverList_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectlist = {}

            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            Phaselist = []
            for l in ABODriverList_M.objects.filter(**dic).values('Phase0').distinct().order_by('Phase0'):
                Phaselist.append(l['Phase0'])
            Projectlist['Project'] = j["Project"]
            Projectlist['Phase0'] = Phaselist
            Customerlist.append(Projectlist)
        selectItem[i['Customer']] = Customerlist
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if 'admin' in i:
            # editPpriority = 4
            canExport = 1
        # elif 'DQA' in i and 'edit' in i:
        #     canExport = 1
    if request.method == "POST":
        # if request.POST.get("isGetData")=="PHASE":
        #     dic_phase = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Project'),
        #                  'Phase0': request.POST.get('Phase')}
        #     # print(dic_phase)
        #     for i in ABODriverList_M.objects.filter(**dic_phase).values('Driver').distinct().order_by('Driver'):
        #         # print(i)
        #         dr.append({'Driver': i['Driver']})
        #     for i in ABODriverList_M.objects.filter(**dic_phase).values('Image').distinct().order_by('Image'):
        #         # print(i)
        #         image.append({'Image': i['Image']})
        if request.POST.get('isGetData') == 'SEARCHALERT':
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in ABODriverList_M.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append(i["Project"])
            else:
                for i in ABODriverList_M.objects.all().values("Project").distinct().order_by("Project"):
                    Prolist.append(i["Project"])
            for i in Prolist:
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
                    sear.append({
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Year, "COMPRJCODE": i,
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().VGA,
                        "OS SUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().OSSupport,
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().LD,
                        "DQA PL": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPL,
                    })
                else:
                    sear.append({
                        "YEAR": "", "COMPRJCODE": i,
                        "CUSPRJCODE": "",
                        "ProjectName": "",
                        "SIZE": "",
                        "CPU": "",
                        "PLATFORM": "",
                        "VGA": "",
                        "OS SUPPORT": "",
                        "Type": "",
                        "PPA": "",
                        "PQE": "",
                        "SS": "",
                        "LD": "",
                        "DQA PL": "",
                    })
            # print(sear)
        if request.POST.get('isGetData') == 'clickdetail':
            print(request.POST)
            Customer = request.POST.get('Customer')
            Project = request.POST.get('row.COMPRJCODE')
            Phase = request.POST.get('Phase')
            Driver = request.POST.get('Driver')
            Image = request.POST.get('Image')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            if Driver:
                dic['Driver'] = Driver
            if Image:
                dic['Image'] = Image
            for i in ABODriverList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
                                  "Version": i.Version, "Project": i.Project, "Bios": i.BIOS, "Driver": i.Driver,
                                  "Image": i.Image,
                                  'Customer': i.Customer, 'Phase': i.Phase0, })
        # if request.POST.get('isGetData') == 'SEARCH':
        #     Customer = request.POST.get('Customer')
        #     Project = request.POST.get('Project')
        #     Phase = request.POST.get('Phase')
        #     Driver = request.POST.get('Driver')
        #     Image = request.POST.get('Image')
        #     dic = {}
        #     if Customer:
        #         dic['Customer'] = Customer
        #     if Project:
        #         dic['Project'] = Project
        #     if Phase:
        #         dic['Phase0'] = Phase
        #     if Driver:
        #         dic['Driver'] = Driver
        #     if Image:
        #         dic['Image'] = Image
        #     for i in ABODriverList_M.objects.filter(**dic):
        #         mock_data.append({'id': i.id, "Name": i.Name, "Function0": i.Function, "Vendor": i.Vendor,
        #                           "Version": i.Version, "Project": i.Project, "Driver": i.Driver, "Image": i.Image,
        #                           'Customer': i.Customer, 'Phase': i.Phase0, })

        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            # "select0":selectList,
            "sear": sear,
            "selectedDriver": dr,
            "selectedImage": image,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'ABODriverTool/ABODriverList_search.html', locals())


@csrf_exempt
def ABOToolList_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/ABOToolList_upload"
    ABOToolList_upload = ABOToolList(request.POST)
    ABOToolList_M_lists = [{'Customer': 'Customer', 'Project': 'Project',
                         'Phase0': 'Phase', 'Vendor': 'Vendor', 'Version': 'Version',
                         'ToolName': 'ToolName', 'TestCase': 'TestCase'}]
    result = '00'
    ABOToolList_M_dic = {}
    result = 4
    if request.method == "POST":
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            n = 0

            for i in simplejson.loads(xlsxlist):
                n += 1
                if 'Customer' in i.keys():
                    Customer = i['Customer']
                else:
                    Customer = ''
                if 'Project' in i.keys():
                    Project = i['Project']
                else:
                    Project = ''
                if 'Phase' in i.keys():
                    Phase0 = i['Phase']
                else:
                    Phase0 = ''
                if 'Vendor' in i.keys():
                    Vendor = i['Vendor']
                else:
                    Vendor = ''
                if 'Version' in i.keys():
                    Version = i['Version']
                else:
                    Version = ''
                if 'ToolName' in i.keys():
                    ToolName = i['ToolName']
                else:
                    ToolName = ''
                if 'TestCase' in i.keys():
                    TestCase = i['TestCase']
                else:
                    TestCase = ''
                # print(len(Version))
                check_dic = {'Customer': Customer, 'Project': Project,
                             'Phase0': Phase0, 'Vendor': Vendor,
                             'Version': Version, 'ToolName': ToolName, 'TestCase': TestCase}
                check_list = ABOToolList_M.objects.filter(**check_dic)
                if check_list:
                    err_ok = 1
                    ABOToolList_M_dic['Customer'] = Customer
                    ABOToolList_M_dic['Project'] = Project
                    ABOToolList_M_dic['Phase0'] = Phase0
                    ABOToolList_M_dic['Vendor'] = Vendor
                    ABOToolList_M_dic['Version'] = Version
                    ABOToolList_M_dic['ToolName'] = ToolName
                    ABOToolList_M_dic['TestCase'] = TestCase
                    ABOToolList_M_lists.append(ABOToolList_M_dic)
                    continue
                else:
                    ABOToolList_Mmodule = ABOToolList_M()
                    ABOToolList_Mmodule.Customer = Customer
                    ABOToolList_Mmodule.Project = Project
                    ABOToolList_Mmodule.Phase0 = Phase0
                    ABOToolList_Mmodule.Vendor = Vendor
                    ABOToolList_Mmodule.Version = Version
                    ABOToolList_Mmodule.ToolName = ToolName
                    ABOToolList_Mmodule.TestCase = TestCase
                    ABOToolList_Mmodule.editor = request.session.get('user_name')
                    ABOToolList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ABOToolList_Mmodule.save()
            datajason = {
                'err_ok': err_ok,
                'content': ABOToolList_M_lists
            }
            return HttpResponse(json.dumps(datajason), content_type="application/json")
        if 'Upload' in request.POST:
            if ABOToolList_upload.is_valid():  # 必须要先验证否则提示object错误没有attribute 'cleaned_data'
                Customer = ABOToolList_upload.cleaned_data['Customer']
                Project = ABOToolList_upload.cleaned_data['Project']
                Phase0 = ABOToolList_upload.cleaned_data['Phase0']
                Vendor = ABOToolList_upload.cleaned_data['Vendor']
                Version = ABOToolList_upload.cleaned_data['Version']
                ToolName = ABOToolList_upload.cleaned_data['ToolName']
                TestCase = ABOToolList_upload.cleaned_data['TestCase']
                check_dic = {'Customer': Customer, 'Project': Project, 'Phase0': Phase0, 'Vendor': Vendor,
                             'Version': Version, 'ToolName': ToolName, 'TestCase': TestCase}
                if ABOToolList_M.objects.filter(**check_dic):
                    result = 1
                else:
                    ABOToolList_Mmodule = ABOToolList_M()
                    ABOToolList_Mmodule.Customer = Customer
                    ABOToolList_Mmodule.Project = Project
                    ABOToolList_Mmodule.Phase0 = Phase0
                    ABOToolList_Mmodule.Vendor = Vendor
                    ABOToolList_Mmodule.Version = Version
                    ABOToolList_Mmodule.ToolName = ToolName
                    ABOToolList_Mmodule.TestCase = TestCase
                    ABOToolList_Mmodule.editor = request.session.get('user_name')
                    ABOToolList_Mmodule.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ABOToolList_Mmodule.save()
                    message_CDM = "Upload Successfully"
                    result = 0
                return render(request, 'ABODriverTool/ABOToolList_upload.html',
                              {'weizhi': weizhi, 'Skin': Skin, 'ABOToolList_upload': ABOToolList(),
                               'result': result})
            else:
                cleanData = ABOToolList_upload.errors
        return render(request, 'ABODriverTool/ABOToolList_upload.html',
                      {'weizhi': weizhi, 'Skin': Skin, 'ABOToolList_upload': ABOToolList(), 'result': result})

    return render(request, 'ABODriverTool/ABOToolList_upload.html', locals())


@csrf_exempt
def ABOToolList_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/ABOToolList_edit"
    mock_data = [
        # {'id':1,"ToolName":"STPM","TestCase":"Stress","Vendor":"Compal initernal","Project":"EL451_S540-14IWL","Version":"V2.5.0.0"},
        #        {'id':2,"ToolName": "3DMark11", "TestCase": "Stress", "Vendor": "FutureMark", "Project": "EL451_S540-14IWL", "Version": "v1.0.132"},
        #        {'id':3,"ToolName": "3DMark", "TestCase": "Stress Performance", "Vendor": "FutureMark", "Project": "EL451_S540-14IWL", "Version": "v2.8.6546"},
        #        {'id':4,"ToolName": "Bench loop", "TestCase": "Stress", "Vendor": "", "Project": "EL451_S540-14IWL", "Version": "v1.2.6"},
        #        {'id':5,"ToolName": "BurnInTest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL", "Version": "V8.1.1022.0"},
        #        {'id':6,"ToolName": "STPM_ThermalCherk(C38)", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL", "Version": "v1.6.1.0"},
        #        {'id':7,"ToolName": "Pwrtest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL", "Version": "v10586_TH2"},
        #        {'id':8,"ToolName": "PingTest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL", "Version": "v3.6.7.11"},
        #        {'id':9,"ToolName": "EC Tool", "TestCase": "N/A", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v08.00e"}
    ]
    selectItem = {
        # "C38(NB)": [{"Project": "EL531", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL532", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL533", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                       {"Project": "EL534", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "C38(AIO)": [{"Project": "EL535", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL536", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL537", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                        {"Project": "EL538", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "A39": [{"Project": "EL531", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL532", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL533", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                   {"Project": "EL534", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}],
        #           "Other": [{"Project": "ELMV2", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                     {"Project": "ELMV3", "Phase0": ["B(FVT)", "C(SIT)", "INV"]},
        #                     {"Project": "ELMV4", "Phase0": ["B(FVT)", "C(SIT)", "INV"]}]
    }
    canEdit = 0
    for i in ABOToolList_M.objects.all().values('Customer').distinct().order_by('Customer'):
        Customerlist = []
        # print(type(i))
        for j in ABOToolList_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectlist = {}

            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            Phaselist = []
            for l in ABOToolList_M.objects.filter(**dic).values('Phase0').distinct().order_by('Phase0'):
                Phaselist.append(l['Phase0'])
            Projectlist['Project'] = j["Project"]
            Projectlist['Phase0'] = Phaselist
            Customerlist.append(Projectlist)
        selectItem[i['Customer']] = Customerlist
    if request.method == "POST":
        # print (request.POST,request.method)
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            check_Owner_dic = {"Customer": Customer, "Project": Project}
            Projectinfo_CQM = ABOTestProjectLL.objects.filter(**check_Owner_dic)
            Projectinfo_LL = TestProjectLL.objects.filter(**check_Owner_dic)
            current_user = request.session.get('user_name')
            if Projectinfo_CQM:
                for i in Projectinfo_CQM:
                    for k in i.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break
            if canEdit == 0 and Projectinfo_LL:
                for i in Projectinfo_LL:
                    for k in i.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if k.username == current_user:
                            canEdit = 1
                            break

            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            for i in ABOToolList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, 'ToolName': i.ToolName, 'TestCase': i.TestCase, 'Vendor': i.Vendor,
                                  'Project': i.Project, 'Version': i.Version, 'Customer': i.Customer,
                                  'Phase': i.Phase0})
        if request.POST.get('isGetData') == 'SAVE':
            # print(request.POST)
            id = request.POST.get('rows[id]')
            editdata = ABOToolList_M.objects.get(id=id)
            # editdata.Customer=request.POST.get('row[Customer]')
            editdata.Project = request.POST.get('rows[Project]')
            editdata.Phase0 = request.POST.get('rows[Phase]')
            editdata.ToolName = request.POST.get('rows[ToolName]')
            editdata.TestCase = request.POST.get('rows[TestCase]')
            editdata.Vendor = request.POST.get('rows[Vendor]')
            editdata.Version = request.POST.get('rows[Version]')
            editdata.editor = request.session.get('user_name')
            editdata.edit_time = datetime.datetime.now().strftime("%Y-%m-d %H:%M:%S")
            editdata.save()

            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            for i in ABOToolList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, 'ToolName': i.ToolName, 'TestCase': i.TestCase, 'Vendor': i.Vendor,
                                  'Project': i.Project, 'Version': i.Version, 'Customer': i.Customer,
                                  'Phase': i.Phase0})
        if request.POST.get('isGetData') == "DELETE":
            # print(request.POST)
            # print(request.POST.get('id'))
            ABOToolList_M.objects.get(id=request.POST.get('id')).delete()

            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            for i in ABOToolList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, 'ToolName': i.ToolName, 'TestCase': i.TestCase, 'Vendor': i.Vendor,
                                  'Project': i.Project, 'Version': i.Version, 'Customer': i.Customer,
                                  'Phase': i.Phase0})
        if 'MUTICANCEL' in str(request.body):
            responseData = json.loads(request.body)
            # print(responseData)
            for i in responseData['params']:
                ABOToolList_M.objects.get(id=i).delete()
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            for i in ABOToolList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, 'ToolName': i.ToolName, 'TestCase': i.TestCase, 'Vendor': i.Vendor,
                                  'Project': i.Project, 'Version': i.Version, 'Customer': i.Customer,
                                  'Phase': i.Phase0})

        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "canEdit": canEdit,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ABODriverTool/ABOToolList_edit.html', locals())


@csrf_exempt
def ABOToolList_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "XQM/ABOToolList_search"
    mock_data = [
        # {"ToolName": "STPM", "TestCase": "Stress", "Vendor": "Compal initernal", "Project": "EL451_S540-14IWL","Version": "V2.5.0.0"},
        #          {"ToolName": "3DMark11", "TestCase": "Stress", "Vendor": "FutureMark", "Project": "EL451_S540-14IWL","Version": "v1.0.132"},
        #          {"ToolName": "3DMark", "TestCase": "Stress Performance", "Vendor": "FutureMark","Project": "EL451_S540-14IWL", "Version": "v2.8.6546"},
        #          {"ToolName": "Bench loop", "TestCase": "Stress", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v1.2.6"},
        #          {"ToolName": "BurnInTest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "V8.1.1022.0"},
        #          {"ToolName": "STPM_ThermalCherk(C38)", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v1.6.1.0"},
        #          {"ToolName": "Pwrtest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v10586_TH2"},
        #          {"ToolName": "PingTest", "TestCase": "", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v3.6.7.11"},
        #          {"ToolName": "EC Tool", "TestCase": "N/A", "Vendor": "", "Project": "EL451_S540-14IWL","Version": "v08.00e"}
    ]
    sear = []
    selectItem = {
        # "C38(NB)":["EL531", "EL532", "EL533", "EL534"],"C38(AIO)":["FL535", "FL536", "FL537", "FL538"],"A39":["FL531", "FL532", "FL533", "FL534"],"Other":["ELMV2", "ELMV3", "ELMV4"]
    }
    for i in ABOToolList_M.objects.all().values('Customer').distinct().order_by('Customer'):
        Customerlist = []
        # print(type(i))
        for j in ABOToolList_M.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectlist = {}

            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            Phaselist = []
            for l in ABOToolList_M.objects.filter(**dic).values('Phase0').distinct().order_by('Phase0'):
                Phaselist.append(l['Phase0'])
            Projectlist['Project'] = j["Project"]
            Projectlist['Phase0'] = Phaselist
            Customerlist.append(Projectlist)
        selectItem[i['Customer']] = Customerlist
    canExport = 0
    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    for i in roles:
        if 'admin' in i:
            # editPpriority = 4
            canExport = 1
        elif 'DQA' in i:
            canExport = 1
    if request.method == "POST":
        if request.POST.get('isGetData') == 'SEARCHALERT':
            Customer = request.POST.get('Customer')
            Prolist = []
            if Customer:
                for i in ABOToolList_M.objects.filter(Customer=Customer).values("Project").distinct().order_by("Project"):
                    Prolist.append(i["Project"])
            else:
                for i in ABOToolList_M.objects.all().values("Project").distinct().order_by("Project"):
                    Prolist.append(i["Project"])
            for i in Prolist:
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i).first():
                    sear.append({
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Year, "COMPRJCODE": i,
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().VGA,
                        "OS SUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().OSSupport,
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().PQE,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().LD,
                        "DQA PL": ProjectinfoinDCT.objects.filter(ComPrjCode=i).first().DQAPL,
                    })
                else:
                    sear.append({
                        "YEAR": "", "COMPRJCODE": i,
                        "CUSPRJCODE": "",
                        "ProjectName": "",
                        "SIZE": "",
                        "CPU": "",
                        "PLATFORM": "",
                        "VGA": "",
                        "OS SUPPORT": "",
                        "Type": "",
                        "PPA": "",
                        "PQE": "",
                        "SS": "",
                        "LD": "",
                        "DQA PL": "",
                    })
            # print(sear)
        if request.POST.get('isGetData') == 'clickdetail':
            Customer = request.POST.get('Customer')
            Project = request.POST.get('row.COMPRJCODE')
            Phase = request.POST.get('Phase')
            dic = {}
            if Customer:
                dic['Customer'] = Customer
            if Project:
                dic['Project'] = Project
            if Phase:
                dic['Phase0'] = Phase
            for i in ABOToolList_M.objects.filter(**dic):
                mock_data.append({'id': i.id, 'ToolName': i.ToolName, 'TestCase': i.TestCase, 'Vendor': i.Vendor,
                                  'Project': i.Project, 'Version': i.Version, 'Customer': i.Customer,
                                  'Phase': i.Phase0})
        # if request.POST.get('isGetData')=='SEARCH':
        #     Customer=request.POST.get('Customer')
        #     Project=request.POST.get('Project')
        #     Phase=request.POST.get('Phase')
        #     dic = {}
        #     if Customer:
        #         dic['Customer'] = Customer
        #     if Project:
        #         dic['Project'] = Project
        #     if Phase:
        #         dic['Phase0'] = Phase
        #     for i in ABOToolList_M.objects.filter(**dic):
        #         mock_data.append({'id':i.id,'ToolName':i.ToolName,'TestCase':i.TestCase,'Vendor':i.Vendor,
        #                           'Project':i.Project,'Version':i.Version,'Customer':i.Customer,'Phase':i.Phase0})
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "sear": sear,
            'canExport': canExport,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ABODriverTool/ABOToolList_search.html', locals())
