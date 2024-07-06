from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
import datetime,os
from django.http import HttpResponse
import datetime,json,simplejson
from .models import LowLightList
from CQM.models import CQMProject
from app01.models import UserInfo, ProjectinfoinDCT, Role
from django.db import transaction
from django.forms.models import model_to_dict
# Create your views here.
@csrf_exempt
def LowLightList_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "Reliability Test Data/LowLight_edit"
    ProjectCodeOption = {
        # "C38(NB)": [{"Projectcode": "ILYE3"},
        #             {"Projectcode": "JLV31"},
        #             {"Projectcode": "FLV34"},
        #             {"Projectcode": "GLSM1"}],
        # "C38(AIO)": [{"Projectcode": "ILYE3"},
        #              {"Projectcode": "JLV31"},
        #              {"Projectcode": "FLV34"},
        #              {"Projectcode": "GLSM1"}],
        # "C85": [{"Projectcode": "ILYE3"},
        #         {"Projectcode": "JLV31"},
        #         {"Projectcode": "FLV34"},
        #         {"Projectcode": "GLSM1"}],
        # "T88(AIO)": [{"Projectcode": "ILYE3"},
        #              {"Projectcode": "JLV31"},
        #              {"Projectcode": "FLV34"},
        #              {"Projectcode": "GLSM1"}],
    }


    mock_data = [
        # {"id": 1, "Customer": "C38(NB)", "ProjectcodeCompal": "ILYE3", "ProjectcodeCustomer": "Y580S-16IRH",
        #  "Lowlight_item": "Thermal and power setting frozen too late", "Root_cause": "For EOY10 SDV phase test",
        #  "LD": "Jazz_Lin", "Owner": "", "Mitigation_plan": "",
        #  },
        # {"id": 2, "Customer": "C38(NB)", "ProjectcodeCompal": "ILYE3", "ProjectcodeCustomer": "Y580S-16IRH",
        #  "Lowlight_item": "Thermal and power setting frozen too late", "Root_cause": "For EOY10 SDV phase test",
        #  "LD": "Jazz_Lin", "Owner": "", "Mitigation_plan": "",
        #  },
    ]

    errMsg = ''

    uploadpermission = 0  # 1:能编辑 0:不能编辑


    roles = []
    onlineuser = request.session.get('account')
    # print(UserInfo.objects.get(account=onlineuser))
    for i in UserInfo.objects.get(account=onlineuser).role.all():
        roles.append(i.name)
    # print(roles)
    editPpriority = 0
    for i in roles:
        if 'DQA_SW' in i or 'admin' == i:
            editPpriority = 1
        elif 'LD' in i:
            if editPpriority != 1:
                editPpriority = 2
        elif 'RD' in i:
            if editPpriority != 1 and editPpriority != 2:
                editPpriority = 3


    # print(request.POST)
    # print(request.body)
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            for i in CQMProject.objects.all().values("Customer").distinct():
                Projectcode_list = []
                for j in CQMProject.objects.filter(Customer=i['Customer']):
                    Projectcode_list.append({"Projectcode": j.Project})
                ProjectCodeOption[i['Customer']] = Projectcode_list

        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            check_LowL_dic = {"Customer": Customer}
            ProjectCompal = request.POST.get('ProjectcodeCompal')
            if ProjectCompal:
                check_LowL_dic["ProjectCompal"] = ProjectCompal
                if editPpriority == 1:

                    # print(check_LowL_dic)
                    check_Owner_dic = {"Customer": Customer, "Project": ProjectCompal}
                    Projectinfo = CQMProject.objects.filter(**check_Owner_dic).first()
                    current_user = request.session.get('user_name')
                    if Projectinfo:
                        for k in Projectinfo.Owner.all():
                            # print(k.username)
                            if k.username == current_user:
                                uploadpermission = 1
                                break
                    if not uploadpermission:
                        editPpriority = 0
            else:
                editPpriority = 0

            for i in LowLightList.objects.filter(**check_LowL_dic):
                mock_data.append(
                    {
                        "id": i.id, "Customer": i.Customer, "ProjectcodeCompal": i.ProjectCompal,
                        "ProjectcodeCustomer": ProjectinfoinDCT.objects.filter(ComPrjCode=i.ProjectCompal).first().PrjEngCode2 if ProjectinfoinDCT.objects.filter(ComPrjCode=i.ProjectCompal) else "DCT Web上没有此Project的信息",
                        "Lowlight_item": i.Lowlight_item,
                        "Root_cause": i.Root_Cause,
                        "LD": i.LD, "Owner": i.Owner, "Mitigation_plan": i.Mitigation_plan,
                        "editor": i.editor, "edit_time": str(i.edit_time),
                    }
                )
        if request.POST.get('action') == 'onSubmit':
            Customer = request.POST.get('Customer')
            ProjectCompal = request.POST.get('ProjectcodeCompal')
            Lowlight_item = request.POST.get('Lowlight_item')
            Root_cause = request.POST.get('Root_cause')
            LD = request.POST.get('LD')
            Owner = request.POST.get('Owner')
            Mitigation_plan = request.POST.get('Mitigation_plan')
            upload_LowL_dic = {
                "Customer": Customer, "ProjectCompal": ProjectCompal, "Lowlight_item": Lowlight_item, "Root_Cause": Root_cause, "LD": LD,
                "Owner": Owner, "Mitigation_plan": Mitigation_plan,
                "editor": request.session.get('account'), "edit_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            check_LowL_dic = {
                "Customer": Customer, "ProjectCompal": ProjectCompal, "Lowlight_item": Lowlight_item,
            }

            searchCustomer = request.POST.get('searchCustomer')
            searchProjectcodeCompal = request.POST.get('searchProjectcodeCompal')
            list_LowL_dic = {'Customer': searchCustomer, 'ProjectCompal': searchProjectcodeCompal}

            if ProjectCompal != searchProjectcodeCompal or Customer != searchCustomer:
                errMsg = "填写的客户别和机种名与当前的不符"
            elif LowLightList.objects.filter(**check_LowL_dic):
                errMsg = "%s,%s,%s:已存在该项目" % (Customer, ProjectCompal, Lowlight_item)
            else:
                LowLightList.objects.create(**upload_LowL_dic)

            for i in LowLightList.objects.filter(**list_LowL_dic):
                mock_data.append(
                    {
                        "id": i.id, "Customer": i.Customer, "ProjectcodeCompal": i.ProjectCompal,
                        "ProjectcodeCustomer": ProjectinfoinDCT.objects.filter(
                            ComPrjCode=i.ProjectCompal).first().PrjEngCode2 if ProjectinfoinDCT.objects.filter(
                            ComPrjCode=i.ProjectCompal) else "DCT Web上没有此Project的信息",
                        "Lowlight_item": i.Lowlight_item,
                        "Root_cause": i.Root_Cause,
                        "LD": i.LD, "Owner": i.Owner, "Mitigation_plan": i.Mitigation_plan,
                        "editor": i.editor, "edit_time": str(i.edit_time),
                    }
                )
        if request.POST.get('action') == 'onSubmit1':
            id = request.POST.get('ID')
            Lowlight_item = request.POST.get('Lowlight_item')
            Root_cause = request.POST.get('Root_cause')
            LD = request.POST.get('LD')
            Owner = request.POST.get('Owner')
            Mitigation_plan = request.POST.get('Mitigation_plan')
            upload_LowL_dic = {}
            if Lowlight_item:
                upload_LowL_dic['Lowlight_item'] = Lowlight_item
            if Root_cause:
                upload_LowL_dic['Root_Cause'] = Root_cause
            if LD:
                upload_LowL_dic['LD'] = LD
            if Owner:
                upload_LowL_dic['Owner'] = Owner
            if Mitigation_plan:
                upload_LowL_dic['Mitigation_plan'] = Mitigation_plan
            # print(upload_LowL_dic,id)
            if upload_LowL_dic:
                LowLightList.objects.filter(id=id).update(**upload_LowL_dic)

            searchCustomer = request.POST.get('searchCustomer')
            searchProjectcodeCompal = request.POST.get('searchProjectcodeCompal')
            list_LowL_dic = {'Customer': searchCustomer, 'ProjectCompal': searchProjectcodeCompal}
            for i in LowLightList.objects.filter(**list_LowL_dic):
                mock_data.append(
                    {
                        "id": i.id, "Customer": i.Customer, "ProjectcodeCompal": i.ProjectCompal,
                        "ProjectcodeCustomer": ProjectinfoinDCT.objects.filter(
                            ComPrjCode=i.ProjectCompal).first().PrjEngCode2 if ProjectinfoinDCT.objects.filter(
                            ComPrjCode=i.ProjectCompal) else "DCT Web上没有此Project的信息",
                        "Lowlight_item": i.Lowlight_item,
                        "Root_cause": i.Root_Cause,
                        "LD": i.LD, "Owner": i.Owner, "Mitigation_plan": i.Mitigation_plan,
                        "editor": i.editor, "edit_time": str(i.edit_time),
                    }
                )
        editpermission = editPpriority
        data = {
            "errMsg": errMsg,
            "ProjectCodeOption": ProjectCodeOption,
            "content": mock_data,
            "uploadpermission": uploadpermission,
            "editpermission": editpermission,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'LowLightList/LowLightList_edit.html', locals())