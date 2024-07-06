from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime, os
from django.http import HttpResponse
import datetime, json, simplejson
from .models import IssuesBreakdown
from CQM.models import CQMProject
from app01.models import UserInfo, ProjectinfoinDCT, Role
from django.db import transaction
from django.forms.models import model_to_dict

# Create your views here.
headermodel_IssuesBreakdown = {
    'Customer': 'Customer', 'Project': 'Project', 'FFRT Entry unclose issue': 'FFRT_Entry_unclose_issue',
    'SIT Exit unclose issue': 'SIT_Exit_unclose_issue', '1st FFRT': 'first_FFRT',
    '2nd FFRT': 'second_FFRT', '3rd FFRT': 'third_FFRT', '4th FFRT': 'fourth_FFRT',
    '5th FFRT': 'fifth_FFRT', '6th FFRT': 'sixth_FFRT', '分類': 'issue_def', 'Remark': 'Remark', 'FFRT': 'FFRT',
    'Defect ID': 'Defect_ID', 'Title': 'Title', 'Create date': 'Create_date', 'Update date': 'Update_date',
    'Status': 'Status',
    'Severity': 'Severity',
    'Category': 'Category', 'Component': 'Component', 'BIOS/KBC': 'BIOS_KBC', 'Comments': 'Comments',
    'Author': 'Author', 'Assign to': 'Assign_to', 'Description': 'Description', 'Reproduce steps': 'Reproduce_steps',
    'Age': 'Age',
}
headermodel_Category = {
    'NF_Uid': 'New found_Unidentified', 'NF_MW': 'New found_MWD', 'NF_N Im': 'New found_New Implement',
    'NF_Str': 'New found_Stress', 'RG F': 'Regression Fail',
    'UE': 'UE', 'AH': 'Adhoc', 'LateF': 'Late found',
}

from datetime import date, timedelta


def get_dates(start_date, end_date):
    dates = []

    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)

        # 将当前日期加上1天作为新的日期
        current_date += timedelta(days=1)

    return dates


@csrf_exempt
def IssuesBreakdown_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DDIS/IssuesBreakdown_edit"
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
        # {"id": 1, "Project": "FLMA0", "FFRT_Entry_unclose_issue": "67", "SIT_Exit_unclose_issue": "41",
        #  "first_FFRT": "2023-12-05~2023-12-18", "second_FFRT": "2023-12-19~2023-12-25",
        #  "third_FFRT": "2023-12-19~2023-12-25", "fourth_FFRT": "", "fifth_FFRT": "",
        #  "sixth_FFRT": "", "issue_def": "New found_Unidentified", "Remark": "Copilot PCR new feature issue",
        #  "FFRT": "FFRT1", "Defect_ID": "398743",
        #  "Title": "[S590-14&16IRU_SIT_UMA] Copilot PCR, Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl (F/R: 2/2u, 4/4c)",
        #  "Create_date": "2023-12-20", "Update_date": "2023-12-25", "Status": "Postpone",
        #  "Severity": "3", "Category": "OS", "Component": "OS",
        #  "BIOS_KBC": "PFCN08WW", "Comments": "", "Author": "Vickie_Wang@compal.com",
        #  "Assign_to": "liulan4", "Description": "Test configuration: Image: V8"
        #                                         "OS: Win11 23H2 build 22631.2715"
        #                                         "Driver: V1.00"
        #                                         "BIOS/EC: PFCN08WW/PFEC08WW, 2023/12/14"
        #                                         "Edge: V120.0.2210.77"
        #                                         "Detect by:"
        #                                         "Ad-hoc"
        #                                         "Fail scope:"
        #                                         "Tested unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "Failed unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "F/R: 2/2u, 4/4c"
        #                                         "Observed symptom:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl"
        #                                         "Error code/ message:"
        #                                         "None"
        #                                         "Expected behavior:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press once Right Ctrl."
        #                                         "How to recover:"
        #                                         "None.",
        #  "Reproduce_steps": "",
        #  "Age": "4",
        #
        #  },
        # {"id": 2, "Project": "FLMA0", "FFRT_Entry_unclose_issue": "67", "SIT_Exit_unclose_issue": "41",
        #  "first_FFRT": "2023-12-05~2023-12-18", "second_FFRT": "2023-12-19~2023-12-25",
        #  "third_FFRT": "2023-12-19~2023-12-25", "fourth_FFRT": "", "fifth_FFRT": "",
        #  "sixth_FFRT": "", "issue_def": "New found_Unidentified", "Remark": "Copilot PCR new feature issue",
        #  "FFRT": "FFRT1", "Defect_ID": "398744",
        #  "Title": "[S590-14&16IRU_SIT_UMA] Copilot PCR, Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl (F/R: 2/2u, 4/4c)",
        #  "Create_date": "2023-12-20", "Update_date": "2023-12-25", "Status": "Postpone",
        #  "Severity": "3", "Category": "OS", "Component": "OS",
        #  "BIOS_KBC": "PFCN08WW", "Comments": "", "Author": "Vickie_Wang@compal.com",
        #  "Assign_to": "liulan4", "Description": "Test configuration: Image: V8"
        #                                         "OS: Win11 23H2 build 22631.2715"
        #                                         "Driver: V1.00"
        #                                         "BIOS/EC: PFCN08WW/PFEC08WW, 2023/12/14"
        #                                         "Edge: V120.0.2210.77"
        #                                         "Detect by:"
        #                                         "Ad-hoc"
        #                                         "Fail scope:"
        #                                         "Tested unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "Failed unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "F/R: 2/2u, 4/4c"
        #                                         "Observed symptom:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl"
        #                                         "Error code/ message:"
        #                                         "None"
        #                                         "Expected behavior:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press once Right Ctrl."
        #                                         "How to recover:"
        #                                         "None.",
        #  "Reproduce_steps": "",
        #  "Age": "4",
        #
        #  },
        # {"id": 3, "Project": "FLMA0", "FFRT_Entry_unclose_issue": "67", "SIT_Exit_unclose_issue": "41",
        #  "first_FFRT": "2023-12-05~2023-12-18", "second_FFRT": "2023-12-19~2023-12-25",
        #  "third_FFRT": "2023-12-19~2023-12-25", "fourth_FFRT": "", "fifth_FFRT": "",
        #  "sixth_FFRT": "", "issue_def": "New found_Unidentified", "Remark": "Copilot PCR new feature issue",
        #  "FFRT": "FFRT1", "Defect_ID": "398745",
        #  "Title": "[S590-14&16IRU_SIT_UMA] Copilot PCR, Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl (F/R: 2/2u, 4/4c)",
        #  "Create_date": "2023-12-20", "Update_date": "2023-12-25", "Status": "Postpone",
        #  "Severity": "3", "Category": "OS", "Component": "OS",
        #  "BIOS_KBC": "PFCN08WW", "Comments": "", "Author": "Vickie_Wang@compal.com",
        #  "Assign_to": "liulan4", "Description": "Test configuration: Image: V8"
        #                                         "OS: Win11 23H2 build 22631.2715"
        #                                         "Driver: V1.00"
        #                                         "BIOS/EC: PFCN08WW/PFEC08WW, 2023/12/14"
        #                                         "Edge: V120.0.2210.77"
        #                                         "Detect by:"
        #                                         "Ad-hoc"
        #                                         "Fail scope:"
        #                                         "Tested unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "Failed unit: 2units(14-I7U16WFS05#38, 16-I5U08WFS02#02)"
        #                                         "F/R: 2/2u, 4/4c"
        #                                         "Observed symptom:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press twice Right Ctrl"
        #                                         "Error code/ message:"
        #                                         "None"
        #                                         "Expected behavior:"
        #                                         "Press Right Ctrl(Copilot Key) to launch Copilot window, then enter/resume MS/S4 or launch other windows, close Copilot window need press once Right Ctrl."
        #                                         "How to recover:"
        #                                         "None.",
        #  "Reproduce_steps": "",
        #  "Age": "4",

        # },
    ]

    errMsg = ''

    deletepermission = 0  # 1:能删除

    err_msg = ''

    canEdit = 0  # 1:能编辑 0:不能编辑

    # roles = []
    # onlineuser = request.session.get('account')
    # # print(UserInfo.objects.get(account=onlineuser))
    # for i in UserInfo.objects.get(account=onlineuser).role.all():
    #     roles.append(i.name)
    # # print(roles)
    # editPpriority = 0
    # for i in roles:
    #     if 'DQA_SW' in i or 'admin' == i:
    #         editPpriority = 1
    #     elif 'LD' in i:
    #         if editPpriority != 1:
    #             editPpriority = 2
    #     elif 'RD' in i:
    #         if editPpriority != 1 and editPpriority != 2:
    #             editPpriority = 3

    # print(request.POST)
    # print(request.body)
    if request.method == "POST":
        canEdit = 0
        if request.POST.get('isGetData') == 'first':
            for i in CQMProject.objects.all().values("Customer").distinct():
                Projectcode_list = []
                for j in CQMProject.objects.filter(Customer=i['Customer']):
                    Projectcode_list.append({"Projectcode": j.Project})
                ProjectCodeOption[i['Customer']] = Projectcode_list

        if request.POST.get('isGetData') == 'SEARCH':
            Check_dic_Project = {'Customer': request.POST.get('Customer'), 'Project': request.POST.get('Projectcode'), }
            Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
            current_user = request.session.get('user_name')
            if Projectinfo:
                for k in Projectinfo.Owner.all():
                    # print(k.username,current_user)
                    # print(type(i.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
            # mock_data
            for i in IssuesBreakdown.objects.filter(**Check_dic_Project):
                # print(i)
                mock_data.append(
                    {
                        "id": i.id, "Customer": i.Customer, "Project": i.Project,
                        "FFRT_Entry_unclose_issue": i.FFRT_Entry_unclose_issue,
                        "SIT_Exit_unclose_issue": i.SIT_Exit_unclose_issue,
                        "first_FFRT": i.first_FFRT,
                        "second_FFRT": i.second_FFRT,
                        "third_FFRT": i.third_FFRT,
                        "fourth_FFRT": i.fourth_FFRT,
                        "fifth_FFRT": i.fifth_FFRT,
                        "sixth_FFRT": i.sixth_FFRT,
                        "issue_def": i.issue_def,
                        "Remark": i.Remark,
                        "FFRT": i.FFRT,
                        "Defect_ID": i.Defect_ID,
                        "Title": i.Title,
                        "Create_date": str(i.Create_date) if i.Create_date else '',
                        "Update_date": str(i.Update_date) if i.Update_date else '',
                        "Status": i.Status, "Severity": i.Severity,
                        "Category": i.Category,
                        "Component": i.Component,
                        "BIOS_KBC": i.BIOS_KBC,
                        "Comments": i.Comments,
                        "Author": i.Author, "Assign_to": i.Assign_to, "Description": i.Description,
                        "Reproduce_steps": i.Reproduce_steps,
                        "Age": i.Age
                    }
                )
        else:
            try:
                request.body
            except:
                pass
            else:
                if 'MUTIDELETE' in str(request.body):
                    responseData = json.loads(request.body)
                    CustomerSearch = responseData['Customer']
                    ProjectSearch = responseData['Projectcode']

                    Check_dic_Project = {'Customer': CustomerSearch, 'Project': ProjectSearch, }
                    Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                    # print(Projectinfo)
                    current_user = request.session.get('user_name')
                    if Projectinfo:
                        for k in Projectinfo.Owner.all():
                            # print(k.username,current_user)
                            # print(type(k.username),type(current_user))
                            if k.username == current_user:
                                canEdit = 1
                                break

                    del_dic_IssueBreakdown = {'Customer': CustomerSearch, 'Project': ProjectSearch}
                    # print(dic_Project)

                    if IssuesBreakdown.objects.filter(**del_dic_IssueBreakdown):
                        # print(1)
                        IssuesBreakdown.objects.filter(**del_dic_IssueBreakdown).delete()

                if 'upload' in str(request.body):

                    responseData = json.loads(request.body)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    CustomerSearch = responseData['Customer']
                    ProjectSearch = responseData['Projectcode']

                    xlsxlist = json.loads(responseData['ExcelData'])
                    # print(xlsxlist)
                    # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                    Check_dic_Project = {'Customer': CustomerSearch, 'Project': ProjectSearch, }
                    # print(Check_dic_ProjectCQM)
                    Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                    # print(Projectinfo)
                    current_user = request.session.get('user_name')
                    if Projectinfo:
                        for k in Projectinfo.Owner.all():
                            # print(k.username,current_user)
                            # print(type(k.username),type(current_user))
                            if k.username == current_user:
                                canEdit = 1
                                break
                    # print(canEdit)
                    if canEdit:
                        rownum = 0
                        startupload = 0
                        # print(xlsxlist)
                        create_list = []
                        for i in xlsxlist:
                            # print(type(i),i)
                            rownum += 1
                            modeldata = {"Customer": CustomerSearch}
                            for key, value in i.items():
                                if key in headermodel_IssuesBreakdown.keys():
                                    # print(headermodel_IssuesBreakdown[key],value)
                                    modeldata[headermodel_IssuesBreakdown[key]] = value
                            # print(modeldata)
                            if 'Project' in modeldata.keys():
                                if ProjectSearch == modeldata['Project']:
                                    startupload = 1
                                else:
                                    startupload = 0
                                    err_msg = """
                                        第"%s"條數據，Project与搜索的机种名不一致
                                                            """ % rownum
                                    break
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，Project不能爲空
                                                            """ % rownum
                                break
                            if 'FFRT_Entry_unclose_issue' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，FFRT_Entry_unclose_issue不能爲空
                                                            """ % rownum
                                break
                            if 'SIT_Exit_unclose_issue' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，SIT_Exit_unclose_issue不能爲空
                                                            """ % rownum
                                break
                            if 'issue_def' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，分類不能爲空
                                                            """ % rownum
                                break
                            if 'FFRT' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，FFRT不能爲空
                                                            """ % rownum
                                break
                            if 'Create_date' in modeldata.keys():
                                try:
                                    # 将字符串转换为日期对象
                                    date = datetime.datetime.strptime(modeldata['Create_date'].replace('/', '-'),
                                                                      '%Y-%m-%d')
                                    # print(date)
                                    # return True
                                    startupload = 1
                                except Exception as e:
                                    # return False
                                    print(e)
                                    startupload = 0
                                    err_msg = """
                                                                                                        第"%s"條數據，Create_date日期格式不对（YYYY-MM-DD）
                                                                                                                            """ % rownum
                                    break
                            else:
                                # canEdit = 0
                                startupload = 0
                                err_msg = """
                                        第"%s"條數據，Create_date不能爲空
                                                            """ % rownum
                                break
                            if 'Update_date' in modeldata.keys():
                                try:
                                    # 将字符串转换为日期对象
                                    date = datetime.datetime.strptime(modeldata['Update_date'].replace('/', '-'),
                                                                      '%Y-%m-%d')
                                    # return True
                                    startupload = 1
                                except Exception as e:
                                    # return False
                                    print(e)
                                    startupload = 0
                                    err_msg = """
                                                                        第"%s"條數據，Update_date日期格式不对（YYYY-MM-DD）
                                                                                            """ % rownum
                                    break
                            if 'first_FFRT' in modeldata.keys() or 'second_FFRT' in modeldata.keys() or 'third_FFRT' in modeldata.keys() or 'fourth_FFRT' in modeldata.keys() or 'fifth_FFRT' in modeldata.keys() or 'sixth_FFRT' in modeldata.keys():
                                try:
                                    # 将字符串转换为日期对象
                                    if 'first_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['first_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['first_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                        # print(date_start, date_end)
                                    if 'second_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['second_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['second_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                    if 'third_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['third_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['third_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                    if 'fourth_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['fourth_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['fourth_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                    if 'fifth_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['fifth_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['fifth_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                    if 'sixth_FFRT' in modeldata.keys():
                                        date_start = datetime.datetime.strptime(
                                            modeldata['sixth_FFRT'].split("~")[0].replace('/', '-'), '%Y-%m-%d')
                                        date_end = datetime.datetime.strptime(
                                            modeldata['sixth_FFRT'].split("~")[1].replace('/', '-'), '%Y-%m-%d')
                                    # return True
                                    startupload = 1
                                except Exception as e:
                                    # return False
                                    print(e)
                                    startupload = 0
                                    err_msg = """
                                                                                                        第"%s"條數據，schedule格式不对（YYYY-MM-DD~YYYY-MM-DD）
                                                                                                                            """ % rownum
                                    break
                            create_list.append(IssuesBreakdown(**modeldata))  # object(**dict)
                        # print(err_msg, startupload)
                        # print(create_list,)
                        if startupload:
                            try:
                                with transaction.atomic():
                                    IssuesBreakdown.objects.bulk_create(create_list)
                                    update_list = []
                            except Exception as e:
                                # alert = '此数据正被其他使用者编辑中...'
                                alert = str(e)
                                print(alert)

                    # print('IssuesBreakdown')
                    # mock_data
                    for i in IssuesBreakdown.objects.filter(**Check_dic_Project):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "Customer": i.Customer, "Project": i.Project,
                                "FFRT_Entry_unclose_issue": i.FFRT_Entry_unclose_issue,
                                "SIT_Exit_unclose_issue": i.SIT_Exit_unclose_issue,
                                "first_FFRT": i.first_FFRT,
                                "second_FFRT": i.second_FFRT,
                                "third_FFRT": i.third_FFRT,
                                "fourth_FFRT": i.fourth_FFRT,
                                "fifth_FFRT": i.fifth_FFRT,
                                "sixth_FFRT": i.sixth_FFRT,
                                "issue_def": i.issue_def,
                                "Remark": i.Remark,
                                "FFRT": i.FFRT,
                                "Defect_ID": i.Defect_ID,
                                "Title": i.Title,
                                "Create_date": str(i.Create_date) if i.Create_date else '',
                                "Update_date": str(i.Update_date) if i.Update_date else '',
                                "Status": i.Status, "Severity": i.Severity,
                                "Category": i.Category,
                                "Component": i.Component,
                                "BIOS_KBC": i.BIOS_KBC,
                                "Comments": i.Comments,
                                "Author": i.Author, "Assign_to": i.Assign_to, "Description": i.Description,
                                "Reproduce_steps": i.Reproduce_steps,
                                "Age": i.Age
                            }
                        )
        data = {
            "errMsg": err_msg,
            "ProjectCodeOption": ProjectCodeOption,
            "content": mock_data,
            "permission": canEdit,

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'IssuesBreakdown/IssuesBreakdown_Edit.html', locals())


@csrf_exempt
def IssuesBreakdown_Summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DDIS/IssuesBreakdown_edit"
    labelname = ""
    propName = ""

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
    for i in IssuesBreakdown.objects.all().values("Customer").distinct():
        Projectlist = []
        for j in IssuesBreakdown.objects.filter(Customer=i["Customer"]).values("Project").distinct():
            Projectlist.append({"Projectcode": j["Project"]})
        ProjectCodeOption[i['Customer']] = Projectlist

    # 表格數據
    mock_data1 = [
        # {"id": 1, "Project": "LD", "S590_Intel_IRU_1416": "Gary_Sun"},
        # {"id": 2, "Project": "TL", "S590_Intel_IRU_1416": "Sarah_Zhu"},
        # {"id": 3, "Project": "1st FFRT", "S590_Intel_IRU_1416": "2023/12/5 ~ 2023/12/18"},
        # {"id": 4, "Project": "2nd FFRT", "S590_Intel_IRU_1416": "2023/12/16~ 2023/12/20"},
    ]
    mock_data2 = [
        # {"id": 1, "FFRT": "FFRT1", "Date": "2023/12/7", "New_Implement": 1, "Stress": 2,
        #  "Unidentified": 4, "MWD": 1, "Regression_Fail": 1, "UE": 0, "Adhoc": 1, "Late_found": 0},
        # {"id": 2, "FFRT": "FFRT1", "Date": "2023/12/7", "New_Implement": 1, "Stress": 2,
        #  "Unidentified": 4, "MWD": 1, "Regression_Fail": 1, "UE": 0, "Adhoc": 1, "Late_found": 0},
        # {"id": 3, "FFRT": "FFRT1", "Date": "2023/12/7", "New_Implement": 1, "Stress": 2,
        #  "Unidentified": 4, "MWD": 1, "Regression_Fail": 1, "UE": 0, "Adhoc": 1, "Late_found": 0},
        # {"id": 4, "FFRT": "FFRT1", "Date": "2023/12/7", "New_Implement": 1, "Stress": 2,
        #  "Unidentified": 4, "MWD": 1, "Regression_Fail": 1, "UE": 0, "Adhoc": 1, "Late_found": 0},
        # {"id": 5, "FFRT": "Total", "Date": 35, "New_Implement": 14, "Stress": 5,
        #  "Unidentified": 4, "MWD": 1, "Regression_Fail": 2, "UE": 7, "Adhoc": 2, "Late_found": 0},
        # {"id": 6, "FFRT": "Total", "Date": 35, "New_Implement": 24, "Stress": 24,
        #  "Unidentified": 24, "MWD": 24, "Regression_Fail": 2, "UE": 7, "Adhoc": 2, "Late_found": 0},
    ]

    keyparts_key = ['NewF', 'RG F', 'UE', 'AH', 'LateF', 'NF_Uid', 'NF_MW', 'NF_N Im', 'NF_Str']

    Category_Option = [

        # {"value": 234, "name": 'NewF'},
        # {"value": 234, "name": 'RG F'},
        # {"value": 135, "name": 'UE'},
        # {"value": 1548, "name": 'AH'},
        # {"value": 1548, "name": 'LateF'},

    ]

    NewF_Option = [

        # {"value": 335, "name": 'NF_Uid'},
        # {"value": 310, "name": 'NF_MW'},
        # {"value": 234, "name": 'NF_N Im'},
        # {"value": 135, "name": 'NF_Str'},

    ]

    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            pass
        if request.POST.get('isGetData') == 'SEARCH':
            Customer = request.POST.get('Customer')
            Projectcode = request.POST.get('Projectcode')
            # mock_data1
            LD_Character = "DCT 没有该机种的ProjectInfo"
            TL_Character = "DCT 没有该机种的ProjectInfo"
            if ProjectinfoinDCT.objects.filter(
                    ComPrjCode=Projectcode):
                LD_Character = ProjectinfoinDCT.objects.filter(
                    ComPrjCode=Projectcode).first().LD
                TL_Character = ProjectinfoinDCT.objects.filter(
                    ComPrjCode=Projectcode).first().DQAPL
            elif len(Projectcode) >= 5:
                LD_Character = ProjectinfoinDCT.objects.filter(
                    ComPrjCode=Projectcode[:5]).first().LD
                TL_Character = ProjectinfoinDCT.objects.filter(
                    ComPrjCode=Projectcode[:5]).first().DQAPL
            mock_data1.append({"id": 1, "Project": "LD", Projectcode: LD_Character})
            mock_data1.append({"id": 2, "Project": "TL", Projectcode: TL_Character})
            FFRT_Date = []
            # IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("first_FFRT").distinct()[0]前提是所有的first_FFRT等6个日期范围所有数据都一样
            dic_search_IssuesB = {"Customer": Customer, "Project": Projectcode}
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("first_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("first_FFRT").distinct()[0][
                    "first_FFRT"]:
                    mock_data1.append({"id": 3, "Project": "1st FFRT",
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("first_FFRT").distinct()[0][
                                           "first_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT1", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("first_FFRT").distinct()[0]["first_FFRT"]))
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("second_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("second_FFRT").distinct()[0][
                    "second_FFRT"]:
                    mock_data1.append({"id": 4, "Project": "2nd FFRT",
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("second_FFRT").distinct()[0][
                                           "second_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT2", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("second_FFRT").distinct()[0]["second_FFRT"]))
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("third_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("third_FFRT").distinct()[0][
                    "third_FFRT"]:
                    mock_data1.append({"id": 5, "Project": '3rd FFRT',
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("third_FFRT").distinct()[0][
                                           "third_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT3", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("third_FFRT").distinct()[0]["third_FFRT"]))
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fourth_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fourth_FFRT").distinct()[0][
                    "fourth_FFRT"]:
                    mock_data1.append({"id": 6, "Project": '4th FFRT',
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fourth_FFRT").distinct()[0][
                                           "fourth_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT4", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fourth_FFRT").distinct()[0]["fourth_FFRT"]))
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fifth_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fifth_FFRT").distinct()[0][
                    "fifth_FFRT"]:
                    mock_data1.append({"id": 7, "Project": '5th FFRT',
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fifth_FFRT").distinct()[0][
                                           "fifth_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT5", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("fifth_FFRT").distinct()[0]["fifth_FFRT"]))
            if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("sixth_FFRT").distinct():
                if IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("sixth_FFRT").distinct()[0][
                    "sixth_FFRT"]:
                    mock_data1.append({"id": 8, "Project": '6th FFRT',
                                       Projectcode: IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("sixth_FFRT").distinct()[0][
                                           "sixth_FFRT"]})
                    FFRT_Date.append(
                        ("FFRT6", IssuesBreakdown.objects.filter(**dic_search_IssuesB).values("sixth_FFRT").distinct()[0]["sixth_FFRT"]))

            # mock_data2
            id_num = 1
            for i in FFRT_Date:
                # print(i, i[1], type(i[1]))
                start_date = datetime.datetime.strptime(i[1].replace(" ", "").split("~")[0].replace('/', '-'),
                                                        "%Y-%m-%d")
                end_date = datetime.datetime.strptime(i[1].replace(" ", "").split("~")[1].replace('/', '-'), "%Y-%m-%d")
                result = get_dates(start_date, end_date)
                FFRTnum = i[0]
                for j in result:
                    if IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                      FFRT=FFRTnum, Create_date=j).count():
                        mock_data2.append(
                            {"id": id_num, "FFRT": FFRTnum, "Date": str(j.strftime("%Y-%m-%d")),
                             "New_Implement": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                             Project=Projectcode,
                                                                             FFRT=FFRTnum, Create_date=j,
                                                                             issue_def="New found_New Implement").count(),
                             "Stress": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                      Project=Projectcode,
                                                                      FFRT=FFRTnum, Create_date=j,
                                                                      issue_def='New found_Stress').count(),
                             "Unidentified": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                            Project=Projectcode,
                                                                            FFRT=FFRTnum,
                                                                            Create_date=j,
                                                                            issue_def='New found_Unidentified').count(),
                             "MWD": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                   FFRT=FFRTnum, Create_date=j,
                                                                   issue_def='New found_MWD').count(),
                             "Regression_Fail": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                               Project=Projectcode,
                                                                               FFRT=FFRTnum,
                                                                               Create_date=j,
                                                                               issue_def='Regression Fail').count(),
                             "UE": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                  FFRT=FFRTnum, Create_date=j,
                                                                  issue_def='UE').count(),
                             "Adhoc": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                     Project=Projectcode,
                                                                     FFRT=FFRTnum, Create_date=j,
                                                                     issue_def='Adhoc').count(),
                             "Late_found": IssuesBreakdown.objects.filter(Customer=Customer,
                                                                          Project=Projectcode,
                                                                          FFRT=FFRTnum,
                                                                          Create_date=j,
                                                                          issue_def='Late found').count()})
                        id_num += 1
            # mock_data2 Total
            NewF_total = IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                        issue_def="New found_New Implement").count() + IssuesBreakdown.objects.filter(
                Customer=Customer, Project=Projectcode,
                issue_def='New found_Stress').count() + IssuesBreakdown.objects.filter(Customer=Customer,
                                                                                       Project=Projectcode,
                                                                                       issue_def='New found_Unidentified').count() + IssuesBreakdown.objects.filter(
                Customer=Customer, Project=Projectcode,
                issue_def='New found_MWD').count()
            mock_data2.append({"id": id_num + 1, "FFRT": "Total",
                               "Date": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode).count(),
                               "New_Implement": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                               issue_def="New found_New Implement").count(),
                               "Stress": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                        issue_def='New found_Stress').count(),
                               "Unidentified": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                              issue_def='New found_Unidentified').count(),
                               "MWD": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                     issue_def='New found_MWD').count(),
                               "Regression_Fail": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                                 issue_def='Regression Fail').count(),
                               "UE": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                    issue_def='UE').count(),
                               "Adhoc": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                       issue_def='Adhoc').count(),
                               "Late_found": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                            issue_def='Late found').count()})
            mock_data2.append({"id": id_num + 1, "FFRT": "Total",
                               "Date": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode).count(),
                               "New_Implement": NewF_total,
                               "Stress": NewF_total,
                               "Unidentified": NewF_total,
                               "MWD": NewF_total,
                               "Regression_Fail": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                                 issue_def='Regression Fail').count(),
                               "UE": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                    issue_def='UE').count(),
                               "Adhoc": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                       issue_def='Adhoc').count(),
                               "Late_found": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                                            issue_def='Late found').count()})
            # Category_Option
            Category_Option.append(
                {"value": NewF_total, "name": 'NewF'},
            )
            Category_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='Regression Fail').count(), "name": 'RG F'},
            )
            Category_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='UE').count(), "name": 'UE'},
            )
            Category_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='Adhoc').count(), "name": 'AH'},
            )
            Category_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='Late found').count(), "name": 'LateF'},
            )
            # NewF_Option
            NewF_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='New found_Unidentified').count(), "name": 'NF_Uid'},
            )
            NewF_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='New found_MWD').count(), "name": 'NF_MW'},
            )
            NewF_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def="New found_New Implement").count(),
                 "name": 'NF_N Im'},
            )
            NewF_Option.append(
                {"value": IssuesBreakdown.objects.filter(Customer=Customer, Project=Projectcode,
                                                         issue_def='New found_Stress').count(), "name": 'NF_Str'},
            )
            labelname = propName = Projectcode

        data = {
            "labelname": labelname,
            "propName": propName,
            "content1": mock_data1,
            "content2": mock_data2,
            "Keyparts_key": keyparts_key,
            "Category_Option": Category_Option,
            "NewF_Option": NewF_Option,
            "ProjectCodeOption": ProjectCodeOption,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'IssuesBreakdown/IssuesBreakdown_Summary.html', locals())
