from django.shortcuts import render
from django.shortcuts import render,redirect
from django.conf import settings
from django.http import HttpResponse
from TestPlanME.models import TestPlanME,TestProjectME,TestItemME
from TestPlanSW.models import TestPlanSW,TestProjectSW,TestItemSW,RetestItemSW,FFRTByRD, TestProjectSWAIO, TestPlanSWAIO
from app01.models import UserInfo, ProjectinfoinDCT
import datetime,json,simplejson
from django.db.models import Max,Min,Sum,Count,Q
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def TestPlanSW_summary(request):
    if not request.session.get('is_login', None):

        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Summary"
    mock_data = [
        # {"Project": "FLMS0", "CaseLibrarytime": "1050", "ProjectBasetime": "0", "Timew/Comfig": "0", "SKUQ": "0",
        #  "Config-Automationtime": "0", "Config-Leveragetime": "0", "Config-Smarttime": "0", "Attendtime-Optimize": "0",
        #  "Config-Retesttime": "0", "H/C": "0", "H/C+OT": "0"},
        # {"Summary": "Base time",
        #  "Project": [{"projectName": "FL4C4", "Code": "2142"}, {"projectName": "FL4E1", "Code": "219"},
        #              {"projectName": "FL5C1", "Code": "242"}, {"projectName": "EL445", "Code": "239"}]},
        # {"Summary": "Feature Support",
        #  "Project": [{"projectName": "FL4C4", "Code": "651"}, {"projectName": "FL4E1", "Code": "121"},
        #              {"projectName": "FL5C1", "Code": "56"}, {"projectName": "EL445", "Code": "90"}]},
        # {"Summary": "Time w/Config-follow matrix(6SKU)",
        #  "Project": [{"projectName": "FL4C4", "Code": "2361"}, {"projectName": "FL4E1", "Code": "272"},
        #              {"projectName": "FL5C1", "Code": "142"}, {"projectName": "EL445", "Code": "179"}]},
        # {"Summary": "Config-Automation time",
        #  "Project": [{"projectName": "FL4C4", "Code": "97"}, {"projectName": "FL4E1", "Code": "0"},
        #              {"projectName": "FL5C1", "Code": "0"}, {"projectName": "EL445", "Code": "5"}]},
        # {"Summary": "Config-Leverage time",
        #  "Project": [{"projectName": "FL4C4", "Code": "0"}, {"projectName": "FL4E1", "Code": "0"},
        #              {"projectName": "FL5C1", "Code": "0"}, {"projectName": "EL445", "Code": "0"}]},
        # {"Summary": "Config-Smart time",
        #  "Project": [{"projectName": "FL4C4", "Code": "0"}, {"projectName": "FL4E1", "Code": "0"},
        #              {"projectName": "FL5C1", "Code": "0"}, {"projectName": "EL445", "Code": "0"}]},
        # {"Summary": "Attend time-Optimize",
        #  "Project": [{"projectName": "FL4C4", "Code": "2263"}, {"projectName": "FL4E1", "Code": "272"},
        #              {"projectName": "FL5C1", "Code": "142"}, {"projectName": "EL445", "Code": "174"}]},
        # {"Summary": "Config-Retest time",
        #  "Project": [{"projectName": "FL4C4", "Code": "580"}, {"projectName": "FL4E1", "Code": "155"},
        #              {"projectName": "FL5C1", "Code": "60"}, {"projectName": "EL445", "Code": "61"}]},
    ]
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]
    searchalert = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMS0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "IdeaPad5 14IIL05 Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "Intel",
        #  "PLATFORM": "Intel Ice Lake-U", "VGA": "NV N175-G3 NV N175-G5 UMA", "OS SUPPORT": "WIN10 19H2",
        #  "SS": "2020-01-17", "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    proinfomation = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    Sums = {
            # "Time_value": [1527, 1483, 344, 1971, 2103, 1493, 1000],
            # "Time_key": ["FVT Config-Retest time", "SIT Config-Retest time", "FFRT Config-Retest time",
            #              "FVT Attend Time", "SIT Attend Time", "FFRT 1st Attend Time", "FFRT 2nd Attend Time"],
            # "Quantity_top6_value": [1, 1, 1, 2, 3, 4],
            # 'Quantity_top6_key': ['EC Team', 'RF', 'EMI', 'SW Team', 'SA Team', 'Thermal Team']
            }
    canEdit = 0
    rdchangelist=[
        # {"Functionteam":"EC Team","Quantity":"1"},
        #           {"Functionteam":"RF","Quantity":"1"},
        #           {"Functionteam":"EMI","Quantity":"1"},
        #           {"Functionteam":"SW Team","Quantity":"2"},
        #           {"Functionteam":"SA Team","Quantity":"3"},
        #           {"Functionteam":"Thermal Team","Quantity":"4"}
                  ]
    Top10={
           #  "Execution_key":['xxxxx','xxxxx','x','xx','x','x','xx','x','xxx','cvc'],
           # "Normal_value": [3, 6, 6, 7, 8, 9, 14, 24, 33, 47],
           # "Regression_key": ['cccc', 'ccc', 'c', 'c', 'cc', 'c', 'ccc', 'c', 'ccc', 'cvc'],
           # "Regression_value": [1, 3, 6, 7, 7, 9, 16, 25, 39, 42],
           }
    Execution_Top10 = [
        # {
        #     "name": "B(FVT)",
        #     "type": "bar",
        #     "stack": "总量",
        #     "data": [220,230,240,250,260,270,280,290,300,310]#对应机种顺序
        # },
        # {
        #     "name": "C(SIT)",
        #     "type": "bar",
        #     "stack": "总量",
        #     "data": [220, 230, 240, 250, 260, 270, 280, 290, 300, 310]  # 对应机种顺序
        # },
    ]
    Regression_Top10 = [
        # {
        #     "name": "B(FVT)",
        #     "type": "bar",
        #     "stack": "总量",
        #     "data": [220, 230, 240, 250, 260, 270, 280, 290, 0, 310]  # 对应机种顺序
        # },
        # {
        #     "name": "C(SIT)",
        #     "type": "bar",
        #     "stack": "总量",
        #     "data": [220, 230, 240, 250, 260, 270, 280, null, 300, 310]  # 对应机种顺序
        # },
    ]
    for i in TestProjectSW.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    for i in TestProjectSWAIO.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
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
    # print(request.method,request.POST, request.GET, 'yyy')
    # print(request.body)
    # print(request.POST)
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            Customer = "C38(NB)"
            defaultproject = TestProjectSW.objects.filter(Customer=Customer).values("Project").distinct().order_by("-ScheduleBegin")
            defaultprojectlist = []
            counter = 0
            for i in defaultproject:
                # print(i)
                if counter < 10:
                    if (i["Project"] not in defaultprojectlist):
                        defaultprojectlist.append(i["Project"])
                        counter += 1
                else:
                    break

            # print(counter, defaultprojectlist)

            Projectlist = []
            for i in defaultprojectlist:
                # print(i)
                for j in TestProjectSW.objects.filter(Customer=Customer, Project=i):
                    Projectlist.append({"name": i, "value": j.Phase})
            # print(Projectlist)

            #之后的跟getMsg里面的一样
            Project_basetime = []
            Project_FS = []
            Project_TCM = []
            Project_CAT = []
            Project_CLT = []
            Project_CST = []
            Project_ATO = []
            Project_CRT = []
            for i in Projectlist:
                Project = i["name"]
                Phase = i["value"]
                check_dic_Pro = {"Customer": Customer, "Project": Project, "Phase": Phase}
                if TestProjectSW.objects.filter(**check_dic_Pro).first():
                    check_dic = {"Customer": Customer, "Phase": Phase,
                                 "Projectinfo": TestProjectSW.objects.filter(**check_dic_Pro).first()}
                    CodeBS = 0
                    CodeFS = 0
                    CodeTCM = 0
                    CodeCAT = 0
                    CodeCLT = 0
                    CodeCST = 0
                    CodeATO = 0
                    CodeCRT = 0
                    HC = 0
                    HCO = 0
                    SKUQ = 0
                    if TestPlanSW.objects.filter(**check_dic):
                        # print(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTime")))
                        CodeBS = round(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTime"))["BaseTime__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTime"))["BaseTime__sum"] else 0

                        CodeFS = round(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                               "BaseTimeSupport__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                            "BaseTimeSupport__sum"] else 0

                        CodeTCM = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                "TimewConfigFollowmatrix__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                            "TimewConfigFollowmatrix__sum"] else 0
                        Projectinfos = TestProjectSW.objects.filter(**check_dic_Pro).first()
                        SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                                   Projectinfos.SKU5,
                                   Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                                   Projectinfos.SKU10,
                                   Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                                   Projectinfos.SKU15,
                                   Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                                   Projectinfos.SKU20,
                                   Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                                   Projectinfos.SKU25,
                                   Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                                   Projectinfos.SKU30,
                                   Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                                   Projectinfos.SKU35,
                                   Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                                   Projectinfos.SKU40,
                                   ]

                        for j in SKUlist:
                            if j:
                                SKUQ += 1

                        CodeCAT = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigAutomationTime"))[
                                "ConfigAutomationTime__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigAutomationTime"))[
                            "ConfigAutomationTime__sum"] else 0

                        CodeCLT = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigLeverageTime"))[
                                "ConfigLeverageTime__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigLeverageTime"))[
                            "ConfigLeverageTime__sum"] else 0

                        CodeCST = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigSmartTime"))[
                                "ConfigSmartTime__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigSmartTime"))[
                            "ConfigSmartTime__sum"] else 0

                        CodeATO = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("AttendTimeOptimize"))[
                                "AttendTimeOptimize__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("AttendTimeOptimize"))[
                            "AttendTimeOptimize__sum"] else 0

                        CodeCRT = round(
                            TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigRetestTime"))[
                                "ConfigRetestTime__sum"] / 60, 0) if TestPlanSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigRetestTime"))[
                            "ConfigRetestTime__sum"] else 0


                        HC = 0 if not TestProjectSW.objects.filter(**check_dic_Pro).first().Full_Function_Duration else round(CodeATO / 6 / TestProjectSW.objects.filter(
                                **check_dic_Pro).first().Full_Function_Duration, 2)
                        HCO = round(HC * 6 / 7, 2)
                        print(i["name"],HCO)
                        # mock_data.append(
                        #     {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS, "ProjectBasetime": CodeFS,
                        #      "Timew/Comfig": CodeTCM,
                        #      "SKUQ": SKUQ,
                        #      "Config-Automationtime": CodeCAT, "Config-Leveragetime": CodeCLT, "Config-Smarttime": CodeCST,
                        #      "Attendtime-Optimize": CodeATO,
                        #      "Config-Retesttime": CodeCRT, "H/C": HC, "H/C+OT": HCO})
                    CodeBS_R = 0
                    CodeFS_R = 0
                    CodeTCM_R = 0
                    CodeCAT_R = 0
                    CodeCLT_R = 0
                    CodeCST_R = 0
                    CodeATO_R = 0
                    CodeCRT_R = 0
                    HC_R = 0
                    HCO_R = 0
                    if RetestItemSW.objects.filter(**check_dic):

                        CodeBS_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTime"))[
                                "BaseTime__sum"] / 60,
                            0) if RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTime"))["BaseTime__sum"] else 0

                        CodeFS_R = round(RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                             "BaseTimeSupport__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                            "BaseTimeSupport__sum"] else 0

                        CodeTCM_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                "TimewConfigFollowmatrix__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                            "TimewConfigFollowmatrix__sum"] else 0


                        CodeCAT_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigAutomationTime"))[
                                "ConfigAutomationTime__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigAutomationTime"))[
                            "ConfigAutomationTime__sum"] else 0

                        CodeCLT_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigLeverageTime"))[
                                "ConfigLeverageTime__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigLeverageTime"))[
                            "ConfigLeverageTime__sum"] else 0

                        CodeCST_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigSmartTime"))[
                                "ConfigSmartTime__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigSmartTime"))[
                            "ConfigSmartTime__sum"] else 0

                        CodeATO_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("AttendTimeOptimize"))[
                                "AttendTimeOptimize__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("AttendTimeOptimize"))[
                            "AttendTimeOptimize__sum"] else 0

                        CodeCRT_R = round(
                            RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigRetestTime"))[
                                "ConfigRetestTime__sum"] / 60, 0) if RetestItemSW.objects.filter(**check_dic).aggregate(
                                Sum("ConfigRetestTime"))[
                            "ConfigRetestTime__sum"] else 0


                        HC_R = 0 if not TestProjectSW.objects.filter(**check_dic_Pro).first().Full_Function_Duration else round(CodeATO_R / 6 / TestProjectSW.objects.filter(
                                **check_dic_Pro).first().Full_Function_Duration, 2)
                        HCO_R = round(HC_R * 6 / 7, 2)
                        print(i["name"], HCO)
                    mock_data.append(
                        {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS + CodeBS_R,
                         "ProjectBasetime": CodeFS + CodeFS_R,
                         "Timew/Comfig": CodeTCM + CodeTCM_R,
                         "SKUQ": SKUQ,
                         "Config-Automationtime": CodeCAT + CodeCAT_R, "Config-Leveragetime": CodeCLT + CodeCLT_R,
                         "Config-Smarttime": CodeCST + CodeCST_R,
                         "Attendtime-Optimize": CodeATO + CodeATO_R,
                         "Config-Retesttime": CodeCRT + CodeCRT_R, "H/C": round(HC + HC_R, 2), "H/C+OT": round(HCO + HCO_R, 2),
                         "ATO/TCM": 0 if (CodeTCM + CodeTCM_R) == 0 else round((CodeATO + CodeATO_R) / (CodeTCM + CodeTCM_R), 2)
                         })
            print(datetime.datetime.now(), "表格")
            # Project top 10
            Projectlist_top = []
            Phaselist_top = []
            Projectlist_top_normal = {}
            Projectlist_top_retest = {}
            for i in Projectlist:
                Projectlist_top.append(i["name"])
                Phaselist_top.append(i["value"])
            # print(Projectlist_top)
            Projectlist_top = list(set(Projectlist_top))
            Phaselist_top = list(set(Phaselist_top))
            # print(Phaselist_top)
            Phasesortorder = {'B(FVT)': 0, 'C(SIT)': 1, 'SIT2': 2, 'GSKU': 3, 'FFRT': 4, 'FFRT2': 5, 'FFRT3': 6,
                              'FFRT4': 7,
                              'FFRT5': 8, 'FFRT6': 9, 'Wave': 10, 'Wave2': 11, 'Wave3': 12, 'Wave4': 13,
                              'Wave5': 14, 'OOC': 15, 'OOC2': 16, 'OOC3': 17, 'OOC4': 18, 'OOC5': 19, 'OOC6': 20,
                              'Others': 21}
            # print(Projectlist_top)
            Phaselist_top.sort(key=lambda x: Phasesortorder[x])
            # print(Phaselist_top)
            for i in Projectlist_top:
                ProjecttotalATO = 0.00
                ProjecttotalRe = 0.00
                datainphase_normal = {}
                datainphase_retest = {}
                for j in mock_data:  # 尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                    if j["Project"] == i:
                        ProjecttotalATO += j["Attendtime-Optimize"] + j["Config-Retesttime"]
                        datainphase_normal[j['Phase']] = j["Attendtime-Optimize"] + j["Config-Retesttime"]
                        if j['Phase'] in ["FFRT2", "FFRT3", "FFRT4", "FFRT5", "FFRT6", "FFRT7", "FFRT8"]:
                            ProjecttotalRe += j["Config-Retesttime"] + j["Attendtime-Optimize"]
                            datainphase_retest[j['Phase']] = j["Config-Retesttime"] + j["Attendtime-Optimize"]
                        else:
                            ProjecttotalRe += j["Config-Retesttime"]
                            datainphase_retest[j['Phase']] = j["Config-Retesttime"]
                Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]

            # reverse为True从大到小
            top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1][0], reverse=True)
            top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1][0], reverse=True)

            # reverse为False从小到大
            # top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1], reverse=False)
            # top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1], reverse=False)
            # print(top_normal)
            # print(top_retest)
            if len(top_retest) > 10:  # 超过10个取最大的10个
                # 从大到小时取前十个
                top_normal_new = top_normal[:10]
                top_retest_new = top_retest[:10]
                # 从小到大时取最后十个
                # top_normal_new = top_normal[-10:]
                # top_retest_new = top_retest[-10:]
            else:
                top_normal_new = top_normal
                top_retest_new = top_retest
            # print(top_normal_new)
            # print(top_retest_new)
            Normal_key = []
            Normal_value = []
            for i in top_normal_new:
                Normal_key.append(i[0])
                # Normal_value.append(i[1])
            Top10["Execution_key"] = Normal_key
            # Top10["Normal_value"] = Normal_value#Value其实都不需要了，换成data了
            Regression_key = []
            Regression_value = []
            for i in top_retest_new:
                Regression_key.append(i[0])
                # Regression_value.append(i[1])
            Top10["Regression_key"] = Regression_key
            # Top10["Regression_value"] = Regression_value#Value其实都不需要了，换成data了
            print(datetime.datetime.now(), "图表1")
            for i in Phaselist_top:
                data_Phase_E = []
                for j in top_normal_new:
                    if i in j[1][1].keys():
                        data_Phase_E.append(j[1][1][i])
                    else:
                        data_Phase_E.append('null')
                Execution_Top10.append({
                    "name": i,
                    "type": "bar",
                    "stack": "总量",
                    "barMaxWidth": 50,
                    "data": data_Phase_E
                })
                data_Phase_R = []
                for j in top_retest_new:
                    if i in j[1][1].keys():
                        data_Phase_R.append(j[1][1][i])
                    else:
                        data_Phase_R.append('null')
                Regression_Top10.append({
                    "name": i,
                    "type": "bar",
                    "stack": "总量",
                    "barMaxWidth": 50,
                    "data": data_Phase_R
                })
            print(datetime.datetime.now(), "图表2")

        if request.POST.get("isGetData") == "SEARCHALERT":
            Customer = request.POST.get("Customer")
            timerange = request.POST.getlist("Date", [])
            # print(timerange)
            # print(not timerange[0])
            Prolist = []
            # print(Customer)
            if Customer == "C38(AIO)" or Customer == "T88(AIO)":
                if not timerange[0]:
                    # 应该是统计只要某机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                    if Customer:
                        # for i in TestProjectSW.objects.filter(Customer=Customer).values("Project", "Phase").distinct().order_by(
                        #         "Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSWAIO.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                                "Project"):
                            # print(i)
                            for j in TestProjectSWAIO.objects.filter(Customer=Customer, Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    else:
                        # for i in TestProjectSW.objects.all().values("Project", "Phase").distinct().order_by("Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSWAIO.objects.all().values("Project").distinct().order_by("Project"):
                            for j in TestProjectSWAIO.objects.filter(Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    # print(Prolist)
                    for i in Prolist:
                        # print(i)
                        if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                            # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                            searchalert.append({
                                "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                                "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                                "COMPRJCODE": i["Project"],
                                "PHASE": i["Phase"],
                                "PrjEngCode1": ProjectinfoinDCT.objects.filter(
                                    ComPrjCode=i["Project"]).first().PrjEngCode1,
                                "PrjEngCode2": ProjectinfoinDCT.objects.filter(
                                    ComPrjCode=i["Project"]).first().PrjEngCode2,
                                "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                                "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                                "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                                "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                                "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                                "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                                "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                                "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                                "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                                "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                                "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                                "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                            })
                        else:
                            # print(i)
                            if len(i['Project']) > 5:
                                # print(i)
                                Prostr1 = i['Project'][0:5]
                                Prostr2 = i['Project'][0:3] + i['Project'][5:]
                                Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                                Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()

                                if Proinfo1 and Proinfo2:
                                    if Proinfo1.Year == Proinfo2.Year:
                                        Year = Proinfo1.Year
                                    else:
                                        Year = Proinfo1.Year + "/" + Proinfo2.Year
                                    if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1
                                    else:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                                    if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2
                                    else:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                                    if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                        ProjectName = Proinfo1.ProjectName
                                    else:
                                        ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                                    if Proinfo1.Size == Proinfo2.Size:
                                        Size = Proinfo1.Size
                                    else:
                                        Size = Proinfo1.Size + "/" + Proinfo2.Size
                                    if Proinfo1.CPU == Proinfo2.CPU:
                                        CPU = Proinfo1.CPU
                                    else:
                                        CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                                    if Proinfo1.Platform == Proinfo2.Platform:
                                        Platform = Proinfo1.Platform
                                    else:
                                        Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                                    if Proinfo1.VGA == Proinfo2.VGA:
                                        VGA = Proinfo1.VGA
                                    else:
                                        VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                                    if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                        OSSupport = Proinfo1.OSSupport
                                    else:
                                        OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                                    if Proinfo1.Type == Proinfo2.Type:
                                        Type = Proinfo1.Type
                                    else:
                                        Type = Proinfo1.Type + "/" + Proinfo2.Type
                                    if Proinfo1.PPA == Proinfo2.PPA:
                                        PPA = Proinfo1.PPA
                                    else:
                                        PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                                    if Proinfo1.PQE == Proinfo2.PQE:
                                        PQE = Proinfo1.PQE
                                    else:
                                        PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                                    if Proinfo1.SS == Proinfo2.SS:
                                        SS = Proinfo1.SS
                                    else:
                                        SS = Proinfo1.SS + "/" + Proinfo2.SS
                                    if Proinfo1.LD == Proinfo2.LD:
                                        LD = Proinfo1.LD
                                    else:
                                        LD = Proinfo1.LD + "/" + Proinfo2.LD
                                    if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                        DQAPL = Proinfo1.DQAPL
                                    else:
                                        DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                                    searchalert.append({
                                        "id": Proinfo1.id,
                                        "YEAR": Year,
                                        "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": PrjEngCode1,
                                        "PrjEngCode2": PrjEngCode2,
                                        "PROJECT": ProjectName,
                                        "SIZE": Size,
                                        "CPU": CPU,
                                        "PLATFORM": Platform,
                                        "VGA": VGA,
                                        "OSSUPPORT": OSSupport,
                                        "Type": Type,
                                        "PPA": PPA,
                                        "PQE": PQE,
                                        "SS": SS,
                                        "LD": LD,
                                        "DQAPL": DQAPL,
                                    })
                                else:
                                    searchalert.append({
                                        "id": "",
                                        "YEAR": "", "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": "",
                                        "PrjEngCode2": "",
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
                            else:
                                searchalert.append({
                                    "id": "",
                                    "YEAR": "", "COMPRJCODE": i["Project"],
                                    "PHASE": i["Phase"],
                                    "PrjEngCode1": "",
                                    "PrjEngCode2": "",
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
                else:
                    # 应该是统计只要某 机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                    if Customer:
                        # for i in TestProjectSW.objects.filter(Customer=Customer).filter(ScheduleBegin__range=timerange).values("Project", "Phase").distinct().order_by(
                        #         "Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSWAIO.objects.filter(Customer=Customer).filter(ScheduleBegin__range=timerange).values(
                                "Project").distinct().order_by(
                            "Project"):
                            for j in TestProjectSWAIO.objects.filter(Customer=Customer, Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    else:
                        # for i in TestProjectSW.objects.filter(ScheduleBegin__range=timerange).values("Project", "Phase").distinct().order_by("Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSWAIO.objects.filter(ScheduleBegin__range=timerange).values(
                                "Project").distinct().order_by(
                            "Project"):
                            for j in TestProjectSWAIO.objects.filter(Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})

                    # print(Prolist)
                    for i in Prolist:
                        # print(i)
                        if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                            # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                            searchalert.append({
                                "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                                "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                                "COMPRJCODE": i["Project"],
                                "PHASE": i["Phase"],
                                "PrjEngCode1": ProjectinfoinDCT.objects.filter(
                                    ComPrjCode=i["Project"]).first().PrjEngCode1,
                                "PrjEngCode2": ProjectinfoinDCT.objects.filter(
                                    ComPrjCode=i["Project"]).first().PrjEngCode2,
                                "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                                "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                                "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                                "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                                "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                                "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                                "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                                "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                                "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                                "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                                "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                                "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                            })
                        else:
                            # print(i)
                            if len(i['Project']) > 5:
                                Prostr1 = i['Project'][0:5]
                                Prostr2 = i['Project'][0:3] + i['Project'][5:]
                                Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                                Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                                if Proinfo1 and Proinfo2:
                                    if Proinfo1.Year == Proinfo2.Year:
                                        Year = Proinfo1.Year
                                    else:
                                        Year = Proinfo1.Year + "/" + Proinfo2.Year
                                    if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1
                                    else:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                                    if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2
                                    else:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                                    if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                        ProjectName = Proinfo1.ProjectName
                                    else:
                                        ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                                    if Proinfo1.Size == Proinfo2.Size:
                                        Size = Proinfo1.Size
                                    else:
                                        Size = Proinfo1.Size + "/" + Proinfo2.Size
                                    if Proinfo1.CPU == Proinfo2.CPU:
                                        CPU = Proinfo1.CPU
                                    else:
                                        CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                                    if Proinfo1.Platform == Proinfo2.Platform:
                                        Platform = Proinfo1.Platform
                                    else:
                                        Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                                    if Proinfo1.VGA == Proinfo2.VGA:
                                        VGA = Proinfo1.VGA
                                    else:
                                        VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                                    if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                        OSSupport = Proinfo1.OSSupport
                                    else:
                                        OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                                    if Proinfo1.Type == Proinfo2.Type:
                                        Type = Proinfo1.Type
                                    else:
                                        Type = Proinfo1.Type + "/" + Proinfo2.Type
                                    if Proinfo1.PPA == Proinfo2.PPA:
                                        PPA = Proinfo1.PPA
                                    else:
                                        PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                                    if Proinfo1.PQE == Proinfo2.PQE:
                                        PQE = Proinfo1.PQE
                                    else:
                                        PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                                    if Proinfo1.SS == Proinfo2.SS:
                                        SS = Proinfo1.SS
                                    else:
                                        SS = Proinfo1.SS + "/" + Proinfo2.SS
                                    if Proinfo1.LD == Proinfo2.LD:
                                        LD = Proinfo1.LD
                                    else:
                                        LD = Proinfo1.LD + "/" + Proinfo2.LD
                                    if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                        DQAPL = Proinfo1.DQAPL
                                    else:
                                        DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                                    searchalert.append({
                                        "id": Proinfo1.id,
                                        "YEAR": Year,
                                        "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": PrjEngCode1,
                                        "PrjEngCode2": PrjEngCode2,
                                        "PROJECT": ProjectName,
                                        "SIZE": Size,
                                        "CPU": CPU,
                                        "PLATFORM": Platform,
                                        "VGA": VGA,
                                        "OSSUPPORT": OSSupport,
                                        "Type": Type,
                                        "PPA": PPA,
                                        "PQE": PQE,
                                        "SS": SS,
                                        "LD": LD,
                                        "DQAPL": DQAPL,
                                    })
                                else:
                                    searchalert.append({
                                        "id": "",
                                        "YEAR": "", "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": "",
                                        "PrjEngCode2": "",
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
                            else:
                                searchalert.append({
                                    "id": "",
                                    "YEAR": "", "COMPRJCODE": i["Project"],
                                    "PHASE": i["Phase"],
                                    "PrjEngCode1": "",
                                    "PrjEngCode2": "",
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
            else:
                if not timerange[0]:
                    # 应该是统计只要某机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                    if Customer:
                        # for i in TestProjectSW.objects.filter(Customer=Customer).values("Project", "Phase").distinct().order_by(
                        #         "Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSW.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                                "Project"):
                            # print(i)
                            for j in TestProjectSW.objects.filter(Customer=Customer, Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    else:
                        # for i in TestProjectSW.objects.all().values("Project", "Phase").distinct().order_by("Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSW.objects.all().values("Project").distinct().order_by("Project"):
                            for j in TestProjectSW.objects.filter(Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    # print(Prolist)
                    for i in Prolist:
                        # print(i)
                        if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                            # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                            searchalert.append({
                                "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                                "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                                "COMPRJCODE": i["Project"],
                                "PHASE": i["Phase"],
                                "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode1,
                                "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode2,
                                "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                                "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                                "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                                "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                                "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                                "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                                "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                                "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                                "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                                "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                                "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                                "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                            })
                        else:
                            # print(i)
                            if len(i['Project']) > 5:
                                # print(i)
                                Prostr1 = i['Project'][0:5]
                                Prostr2 = i['Project'][0:3] + i['Project'][5:]
                                Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                                Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()

                                if Proinfo1 and Proinfo2:
                                    if Proinfo1.Year == Proinfo2.Year:
                                        Year = Proinfo1.Year
                                    else:
                                        Year = Proinfo1.Year + "/" + Proinfo2.Year
                                    if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1
                                    else:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                                    if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2
                                    else:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                                    if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                        ProjectName = Proinfo1.ProjectName
                                    else:
                                        ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                                    if Proinfo1.Size == Proinfo2.Size:
                                        Size = Proinfo1.Size
                                    else:
                                        Size = Proinfo1.Size + "/" + Proinfo2.Size
                                    if Proinfo1.CPU == Proinfo2.CPU:
                                        CPU = Proinfo1.CPU
                                    else:
                                        CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                                    if Proinfo1.Platform == Proinfo2.Platform:
                                        Platform = Proinfo1.Platform
                                    else:
                                        Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                                    if Proinfo1.VGA == Proinfo2.VGA:
                                        VGA = Proinfo1.VGA
                                    else:
                                        VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                                    if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                        OSSupport = Proinfo1.OSSupport
                                    else:
                                        OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                                    if Proinfo1.Type == Proinfo2.Type:
                                        Type = Proinfo1.Type
                                    else:
                                        Type = Proinfo1.Type + "/" + Proinfo2.Type
                                    if Proinfo1.PPA == Proinfo2.PPA:
                                        PPA = Proinfo1.PPA
                                    else:
                                        PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                                    if Proinfo1.PQE == Proinfo2.PQE:
                                        PQE = Proinfo1.PQE
                                    else:
                                        PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                                    if Proinfo1.SS == Proinfo2.SS:
                                        SS = Proinfo1.SS
                                    else:
                                        SS = Proinfo1.SS + "/" + Proinfo2.SS
                                    if Proinfo1.LD == Proinfo2.LD:
                                        LD = Proinfo1.LD
                                    else:
                                        LD = Proinfo1.LD + "/" + Proinfo2.LD
                                    if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                        DQAPL = Proinfo1.DQAPL
                                    else:
                                        DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                                    searchalert.append({
                                        "id": Proinfo1.id,
                                        "YEAR": Year,
                                        "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": PrjEngCode1,
                                        "PrjEngCode2": PrjEngCode2,
                                        "PROJECT": ProjectName,
                                        "SIZE": Size,
                                        "CPU": CPU,
                                        "PLATFORM": Platform,
                                        "VGA": VGA,
                                        "OSSUPPORT": OSSupport,
                                        "Type": Type,
                                        "PPA": PPA,
                                        "PQE": PQE,
                                        "SS": SS,
                                        "LD": LD,
                                        "DQAPL": DQAPL,
                                    })
                                else:
                                    searchalert.append({
                                        "id": "",
                                        "YEAR": "", "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": "",
                                        "PrjEngCode2": "",
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
                            else:
                                searchalert.append({
                                    "id": "",
                                    "YEAR": "", "COMPRJCODE": i["Project"],
                                    "PHASE": i["Phase"],
                                    "PrjEngCode1": "",
                                    "PrjEngCode2": "",
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
                else:
                    # 应该是统计只要某 机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                    if Customer:
                        # for i in TestProjectSW.objects.filter(Customer=Customer).filter(ScheduleBegin__range=timerange).values("Project", "Phase").distinct().order_by(
                        #         "Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSW.objects.filter(Customer=Customer).filter(ScheduleBegin__range=timerange).values(
                                "Project").distinct().order_by(
                            "Project"):
                            for j in TestProjectSW.objects.filter(Customer=Customer, Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                    else:
                        # for i in TestProjectSW.objects.filter(ScheduleBegin__range=timerange).values("Project", "Phase").distinct().order_by("Project"):
                        #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                        for i in TestProjectSW.objects.filter(ScheduleBegin__range=timerange).values(
                                "Project").distinct().order_by(
                                "Project"):
                            for j in TestProjectSW.objects.filter(Project=i["Project"]):
                                Prolist.append({"Project": i["Project"], "Phase": j.Phase})

                    # print(Prolist)
                    for i in Prolist:
                        # print(i)
                        if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                            # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                            searchalert.append({
                                "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                                "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                                "COMPRJCODE": i["Project"],
                                "PHASE": i["Phase"],
                                "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode1,
                                "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode2,
                                "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                                "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                                "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                                "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                                "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                                "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                                "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                                "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                                "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                                "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                                "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                                "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                            })
                        else:
                            # print(i)
                            if len(i['Project']) > 5:
                                Prostr1 = i['Project'][0:5]
                                Prostr2 = i['Project'][0:3]+i['Project'][5:]
                                Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                                Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                                if Proinfo1 and Proinfo2:
                                    if Proinfo1.Year == Proinfo2.Year:
                                        Year = Proinfo1.Year
                                    else:
                                        Year = Proinfo1.Year + "/" + Proinfo2.Year
                                    if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1
                                    else:
                                        PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                                    if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2
                                    else:
                                        PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                                    if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                        ProjectName = Proinfo1.ProjectName
                                    else:
                                        ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                                    if Proinfo1.Size == Proinfo2.Size:
                                        Size = Proinfo1.Size
                                    else:
                                        Size = Proinfo1.Size + "/" + Proinfo2.Size
                                    if Proinfo1.CPU == Proinfo2.CPU:
                                        CPU = Proinfo1.CPU
                                    else:
                                        CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                                    if Proinfo1.Platform == Proinfo2.Platform:
                                        Platform = Proinfo1.Platform
                                    else:
                                        Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                                    if Proinfo1.VGA == Proinfo2.VGA:
                                        VGA = Proinfo1.VGA
                                    else:
                                        VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                                    if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                        OSSupport = Proinfo1.OSSupport
                                    else:
                                        OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                                    if Proinfo1.Type == Proinfo2.Type:
                                        Type = Proinfo1.Type
                                    else:
                                        Type = Proinfo1.Type + "/" + Proinfo2.Type
                                    if Proinfo1.PPA == Proinfo2.PPA:
                                        PPA = Proinfo1.PPA
                                    else:
                                        PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                                    if Proinfo1.PQE == Proinfo2.PQE:
                                        PQE = Proinfo1.PQE
                                    else:
                                        PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                                    if Proinfo1.SS == Proinfo2.SS:
                                        SS = Proinfo1.SS
                                    else:
                                        SS = Proinfo1.SS + "/" + Proinfo2.SS
                                    if Proinfo1.LD == Proinfo2.LD:
                                        LD = Proinfo1.LD
                                    else:
                                        LD = Proinfo1.LD + "/" + Proinfo2.LD
                                    if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                        DQAPL = Proinfo1.DQAPL
                                    else:
                                        DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                                    searchalert.append({
                                        "id": Proinfo1.id,
                                        "YEAR": Year,
                                        "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": PrjEngCode1,
                                        "PrjEngCode2": PrjEngCode2,
                                        "PROJECT": ProjectName,
                                        "SIZE": Size,
                                        "CPU": CPU,
                                        "PLATFORM": Platform,
                                        "VGA": VGA,
                                        "OSSUPPORT": OSSupport,
                                        "Type": Type,
                                        "PPA": PPA,
                                        "PQE": PQE,
                                        "SS": SS,
                                        "LD": LD,
                                        "DQAPL": DQAPL,
                                    })
                                else:
                                    searchalert.append({
                                        "id": "",
                                        "YEAR": "", "COMPRJCODE": i["Project"],
                                        "PHASE": i["Phase"],
                                        "PrjEngCode1": "",
                                        "PrjEngCode2": "",
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
                            else:
                                searchalert.append({
                                    "id": "",
                                    "YEAR": "", "COMPRJCODE": i["Project"],
                                    "PHASE": i["Phase"],
                                    "PrjEngCode1": "",
                                    "PrjEngCode2": "",
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

        if 'getMsg' in str(request.body):#前端穿Jason数据
            getdata = json.loads(request.body)
            # print(getdata)
            print(datetime.datetime.now())
            Customer = getdata['customer']
            Projectlist = getdata["searchalert"]
            # print(Projectlist)
            if Customer == "C38(AIO)" or Customer == "T88(AIO)":
                Project_basetime = []
                Project_FS = []
                Project_TCM = []
                Project_CAT = []
                Project_CLT = []
                Project_CST = []
                Project_ATO = []
                Project_CRT = []
                for i in Projectlist:
                    Project = i["name"]
                    Phase = i["value"]
                    check_dic_Pro = {"Customer": Customer, "Project": Project, "Phase": Phase}
                    if TestProjectSWAIO.objects.filter(**check_dic_Pro).first():
                        check_dic = {"Customer": Customer, "Phase": Phase,
                                     "Projectinfo": TestProjectSWAIO.objects.filter(**check_dic_Pro).first()}
                        check_dic_BS = {"Customer": Customer, "Phase": Phase,
                                        "Projectinfo": TestProjectSWAIO.objects.filter(**check_dic_Pro).first(),
                                        "Owner__contains": "DQA"}
                        CodeBS = 0
                        CodeFS = 0
                        CodeTCM = 0
                        CodeCAT = 0
                        CodeCLT = 0
                        CodeCST = 0
                        CodeATO = 0
                        CodeCRT = 0
                        HC = 0
                        HCO = 0
                        SKUQ = 0
                        if TestPlanSWAIO.objects.filter(**check_dic):
                            # print(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTime")))

                            if TestPlanSWAIO.objects.filter(**check_dic_BS).aggregate(Sum("AT_AttendTime"))["AT_AttendTime__sum"]:
                                CodeBS = round(
                                    TestPlanSWAIO.objects.filter(**check_dic_BS).aggregate(Sum("AT_AttendTime"))[
                                        "AT_AttendTime__sum"] / 60,
                                    0)
                            else:
                                CodeBS = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(Sum("Basetimesupport"))[
                                "Basetimesupport__sum"]:
                                CodeFS = round(TestPlanSWAIO.objects.filter(**check_dic).aggregate(Sum("Basetimesupport"))[
                                                   "Basetimesupport__sum"] / 60, 0)
                            else:
                                CodeFS = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(Sum("Configalltesttime"))[
                                "Configalltesttime__sum"]:
                                CodeTCM = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(Sum("Configalltesttime"))[
                                        "Configalltesttime__sum"] / 60, 0)
                            else:
                                CodeTCM = 0
                            Projectinfos = TestProjectSWAIO.objects.filter(**check_dic_Pro).first()
                            SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                                       Projectinfos.SKU5,
                                       Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                                       Projectinfos.SKU10,
                                       Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                                       Projectinfos.SKU15,
                                       Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                                       Projectinfos.SKU20,]
                            SKUQ = 0
                            for j in SKUlist:
                                if j:
                                    SKUQ += 1
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigAutomationtime"))[
                                "ConfigAutomationtime__sum"]:
                                CodeCAT = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigAutomationtime"))[
                                        "ConfigAutomationtime__sum"] / 60, 0)
                            else:
                                CodeCAT = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigLeveragetime"))[
                                "ConfigLeveragetime__sum"]:
                                CodeCLT = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigLeveragetime"))[
                                        "ConfigLeveragetime__sum"] / 60, 0)
                            else:
                                CodeCLT = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigSmarttime"))[
                                "ConfigSmarttime__sum"]:
                                CodeCST = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigSmarttime"))[
                                        "ConfigSmarttime__sum"] / 60, 0)
                            else:
                                CodeCST = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                    Sum("AttendtimeOptimize"))[
                                "AttendtimeOptimize__sum"]:
                                CodeATO = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                        Sum("AttendtimeOptimize"))[
                                        "AttendtimeOptimize__sum"] / 60, 0)
                            else:
                                CodeATO = 0
                            if TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigRetesttime"))[
                                "ConfigRetesttime__sum"]:
                                CodeCRT = round(
                                    TestPlanSWAIO.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigRetesttime"))[
                                        "ConfigRetesttime__sum"] / 60, 0)
                            else:
                                CodeCRT = 0

                            if not TestProjectSWAIO.objects.filter(**check_dic_Pro).first().Full_Function_Duration:
                                HC = 0

                            else:
                                HC = round(CodeATO / 6 / TestProjectSWAIO.objects.filter(
                                    **check_dic_Pro).first().Full_Function_Duration, 2)
                            HCO = round(HC * 6 / 7, 2)
                            # mock_data.append(
                            #     {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS, "ProjectBasetime": CodeFS,
                            #      "Timew/Comfig": CodeTCM,
                            #      "SKUQ": SKUQ,
                            #      "Config-Automationtime": CodeCAT, "Config-Leveragetime": CodeCLT, "Config-Smarttime": CodeCST,
                            #      "Attendtime-Optimize": CodeATO,
                            #      "Config-Retesttime": CodeCRT, "H/C": HC, "H/C+OT": HCO})

                        mock_data.append(
                            {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS,
                             "ProjectBasetime": CodeFS,
                             "Timew/Comfig": CodeTCM,
                             "SKUQ": SKUQ,
                             "Config-Automationtime": CodeCAT, "Config-Leveragetime": CodeCLT,
                             "Config-Smarttime": CodeCST,
                             "Attendtime-Optimize": CodeATO,
                             "Config-Retesttime": CodeCRT, "H/C": round(HC, 2),
                             "H/C+OT": round(HCO, 2),
                             "ATO/TCM": 0 if CodeTCM == 0 else round(CodeATO / CodeTCM, 2)})
                print(datetime.datetime.now(), "表格")
                # Project top 10
                Projectlist_top = []
                Phaselist_top = []
                Projectlist_top_normal = {}
                Projectlist_top_retest = {}
                for i in Projectlist:
                    Projectlist_top.append(i["name"])
                    Phaselist_top.append(i["value"])
                # print(Projectlist_top)
                Projectlist_top = list(set(Projectlist_top))
                Phaselist_top = list(set(Phaselist_top))
                Phasesortorder = {'B(SDV)': 0, 'C(SIT)': 1, 'Wave2': 2, 'Wave3': 3, 'EELP+': 4, 'OOC': 5, 'OOC2': 6, 'OOC3': 7, }
                # print(Projectlist_top)
                Phaselist_top.sort(key=lambda x: Phasesortorder[x])
                # print(Phaselist_top)
                for i in Projectlist_top:
                    ProjecttotalATO = 0.00
                    ProjecttotalRe = 0.00
                    datainphase_normal = {}
                    datainphase_retest = {}
                    for j in mock_data:  # 尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            ProjecttotalATO += j["Attendtime-Optimize"] + j["Config-Retesttime"]
                            datainphase_normal[j['Phase']] = j["Attendtime-Optimize"] + j["Config-Retesttime"]
                            if j['Phase'] in ["FFRT2", "FFRT3", "FFRT4", "FFRT5", "FFRT6", "FFRT7", "FFRT8"]:
                                ProjecttotalRe += j["Config-Retesttime"] + j["Attendtime-Optimize"]
                                datainphase_retest[j['Phase']] = j["Config-Retesttime"] + j["Attendtime-Optimize"]
                            else:
                                ProjecttotalRe += j["Config-Retesttime"]
                                datainphase_retest[j['Phase']] = j["Config-Retesttime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]

                # reverse为True从大到小
                top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1][0], reverse=True)
                top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1][0], reverse=True)

                # reverse为False从小到大
                # top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1], reverse=False)
                # top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1], reverse=False)
                # print(top_normal)
                # print(top_retest)
                if len(top_retest) > 10:  # 超过10个取最大的10个
                    # 从大到小时取前十个
                    top_normal_new = top_normal[:10]
                    top_retest_new = top_retest[:10]
                    # 从小到大时取最后十个
                    # top_normal_new = top_normal[-10:]
                    # top_retest_new = top_retest[-10:]
                else:
                    top_normal_new = top_normal
                    top_retest_new = top_retest
                # print(top_normal_new)
                # print(top_retest_new)
                Normal_key = []
                Normal_value = []
                for i in top_normal_new:
                    Normal_key.append(i[0])
                    # Normal_value.append(i[1])
                Top10["Execution_key"] = Normal_key
                # Top10["Normal_value"] = Normal_value#Value其实都不需要了，换成data了
                Regression_key = []
                Regression_value = []
                for i in top_retest_new:
                    Regression_key.append(i[0])
                    # Regression_value.append(i[1])
                Top10["Regression_key"] = Regression_key
                # Top10["Regression_value"] = Regression_value#Value其实都不需要了，换成data了
                print(datetime.datetime.now(), "图表1")
                for i in Phaselist_top:
                    data_Phase_E = []
                    for j in top_normal_new:
                        if i in j[1][1].keys():
                            data_Phase_E.append(j[1][1][i])
                        else:
                            data_Phase_E.append('null')
                    Execution_Top10.append({
                        "name": i,
                        "type": "bar",
                        "stack": "总量",
                        "barMaxWidth": 50,
                        "data": data_Phase_E
                    })
                    data_Phase_R = []
                    for j in top_retest_new:
                        if i in j[1][1].keys():
                            data_Phase_R.append(j[1][1][i])
                        else:
                            data_Phase_R.append('null')
                    Regression_Top10.append({
                        "name": i,
                        "type": "bar",
                        "stack": "总量",
                        "barMaxWidth": 50,
                        "data": data_Phase_R
                    })
                print(datetime.datetime.now(), "图表2")
                # print(Top10)
            else:
                Project_basetime = []
                Project_FS = []
                Project_TCM = []
                Project_CAT = []
                Project_CLT = []
                Project_CST = []
                Project_ATO = []
                Project_CRT = []
                # print(Projectlist)
                for i in Projectlist:
                    Project = i["name"]
                    Phase = i["value"]
                    check_dic_Pro = {"Customer": Customer, "Project": Project, "Phase": Phase}
                    # print(check_dic_Pro)
                    if TestProjectSW.objects.filter(**check_dic_Pro).first():
                        check_dic = {"Customer": Customer, "Phase": Phase,
                                     "Projectinfo": TestProjectSW.objects.filter(**check_dic_Pro).first()}
                        check_dic_BS = {"Customer": Customer, "Phase": Phase,
                                     "Projectinfo": TestProjectSW.objects.filter(**check_dic_Pro).first(), "Owner__contains": "DQA"}
                        CodeBS = 0
                        CodeFS = 0
                        CodeTCM = 0
                        CodeCAT = 0
                        CodeCLT = 0
                        CodeCST = 0
                        CodeATO = 0
                        CodeCRT = 0
                        HC = 0
                        HCO = 0
                        SKUQ = 0
                        # print(check_dic)
                        # print(check_dic_BS)
                        if TestPlanSW.objects.filter(**check_dic):
                            # print(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTime")))
                            print(1)
                            if TestPlanSW.objects.filter(**check_dic_BS).aggregate(Sum("BaseTime"))["BaseTime__sum"]:
                                CodeBS = round(
                                    TestPlanSW.objects.filter(**check_dic_BS).aggregate(Sum("BaseTime"))["BaseTime__sum"] / 60,
                                    0)
                            else:
                                CodeBS = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                "BaseTimeSupport__sum"]:
                                CodeFS = round(TestPlanSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                                   "BaseTimeSupport__sum"] / 60, 0)
                            else:
                                CodeFS = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                "TimewConfigFollowmatrix__sum"]:
                                CodeTCM = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                        "TimewConfigFollowmatrix__sum"] / 60, 0)
                            else:
                                CodeTCM = 0
                            Projectinfos = TestProjectSW.objects.filter(**check_dic_Pro).first()
                            SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                                       Projectinfos.SKU5,
                                       Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                                       Projectinfos.SKU10,
                                       Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                                       Projectinfos.SKU15,
                                       Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                                       Projectinfos.SKU20,
                                       Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                                       Projectinfos.SKU25,
                                       Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                                       Projectinfos.SKU30,
                                       Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                                       Projectinfos.SKU35,
                                       Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                                       Projectinfos.SKU40,
                                       ]
                            SKUQ = 0
                            for j in SKUlist:
                                if j:
                                    SKUQ += 1
                            if TestPlanSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigAutomationTime"))[
                                "ConfigAutomationTime__sum"]:
                                CodeCAT = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigAutomationTime"))[
                                        "ConfigAutomationTime__sum"] / 60, 0)
                            else:
                                CodeCAT = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigLeverageTime"))[
                                "ConfigLeverageTime__sum"]:
                                CodeCLT = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigLeverageTime"))[
                                        "ConfigLeverageTime__sum"] / 60, 0)
                            else:
                                CodeCLT = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigSmartTime"))[
                                "ConfigSmartTime__sum"]:
                                CodeCST = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigSmartTime"))[
                                        "ConfigSmartTime__sum"] / 60, 0)
                            else:
                                CodeCST = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(
                                    Sum("AttendTimeOptimize"))[
                                "AttendTimeOptimize__sum"]:
                                CodeATO = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(
                                        Sum("AttendTimeOptimize"))[
                                        "AttendTimeOptimize__sum"] / 60, 0)
                            else:
                                CodeATO = 0
                            if TestPlanSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigRetestTime"))[
                                "ConfigRetestTime__sum"]:
                                CodeCRT = round(
                                    TestPlanSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigRetestTime"))[
                                        "ConfigRetestTime__sum"] / 60, 0)
                            else:
                                CodeCRT = 0

                            if not TestProjectSW.objects.filter(**check_dic_Pro).first().Full_Function_Duration:
                                HC = 0

                            else:
                                HC = round(CodeATO / 6 / TestProjectSW.objects.filter(
                                    **check_dic_Pro).first().Full_Function_Duration, 2)
                            HCO = round(HC * 6 / 7, 2)
                            # mock_data.append(
                            #     {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS, "ProjectBasetime": CodeFS,
                            #      "Timew/Comfig": CodeTCM,
                            #      "SKUQ": SKUQ,
                            #      "Config-Automationtime": CodeCAT, "Config-Leveragetime": CodeCLT, "Config-Smarttime": CodeCST,
                            #      "Attendtime-Optimize": CodeATO,
                            #      "Config-Retesttime": CodeCRT, "H/C": HC, "H/C+OT": HCO})
                        CodeBS_R = 0
                        CodeFS_R = 0
                        CodeTCM_R = 0
                        CodeCAT_R = 0
                        CodeCLT_R = 0
                        CodeCST_R = 0
                        CodeATO_R = 0
                        CodeCRT_R = 0
                        HC_R = 0
                        HCO_R = 0
                        if RetestItemSW.objects.filter(**check_dic):
                            print(2)
                            if RetestItemSW.objects.filter(**check_dic_BS).aggregate(Sum("BaseTime"))["BaseTime__sum"]:
                                CodeBS_R = round(
                                    RetestItemSW.objects.filter(**check_dic_BS).aggregate(Sum("BaseTime"))["BaseTime__sum"] / 60,
                                    0)
                            else:
                                CodeBS_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                "BaseTimeSupport__sum"]:
                                CodeFS_R = round(RetestItemSW.objects.filter(**check_dic).aggregate(Sum("BaseTimeSupport"))[
                                                   "BaseTimeSupport__sum"] / 60, 0)
                            else:
                                CodeFS_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                "TimewConfigFollowmatrix__sum"]:
                                CodeTCM_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(Sum("TimewConfigFollowmatrix"))[
                                        "TimewConfigFollowmatrix__sum"] / 60, 0)
                            else:
                                CodeTCM_R = 0

                            if RetestItemSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigAutomationTime"))[
                                "ConfigAutomationTime__sum"]:
                                CodeCAT_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigAutomationTime"))[
                                        "ConfigAutomationTime__sum"] / 60, 0)
                            else:
                                CodeCAT_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigLeverageTime"))[
                                "ConfigLeverageTime__sum"]:
                                CodeCLT_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigLeverageTime"))[
                                        "ConfigLeverageTime__sum"] / 60, 0)
                            else:
                                CodeCLT_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigSmartTime"))[
                                "ConfigSmartTime__sum"]:
                                CodeCST_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigSmartTime"))[
                                        "ConfigSmartTime__sum"] / 60, 0)
                            else:
                                CodeCST_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(
                                    Sum("AttendTimeOptimize"))[
                                "AttendTimeOptimize__sum"]:
                                CodeATO_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(
                                        Sum("AttendTimeOptimize"))[
                                        "AttendTimeOptimize__sum"] / 60, 0)
                            else:
                                CodeATO_R = 0
                            if RetestItemSW.objects.filter(**check_dic).aggregate(
                                    Sum("ConfigRetestTime"))[
                                "ConfigRetestTime__sum"]:
                                CodeCRT_R = round(
                                    RetestItemSW.objects.filter(**check_dic).aggregate(
                                        Sum("ConfigRetestTime"))[
                                        "ConfigRetestTime__sum"] / 60, 0)
                            else:
                                CodeCRT_R = 0

                            if not TestProjectSW.objects.filter(**check_dic_Pro).first().Full_Function_Duration:
                                HC_R = 0

                            else:
                                HC_R = round(CodeATO_R / 6 / TestProjectSW.objects.filter(
                                    **check_dic_Pro).first().Full_Function_Duration, 2)
                            HCO_R = round(HC_R * 6 / 7, 2)
                        mock_data.append(
                            {"Project": i["name"], "Phase": i["value"], "CaseLibrarytime": CodeBS+CodeBS_R, "ProjectBasetime": CodeFS+CodeFS_R,
                             "Timew/Comfig": CodeTCM+CodeTCM_R,
                             "SKUQ": SKUQ,
                             "Config-Automationtime": CodeCAT+CodeCAT_R, "Config-Leveragetime": CodeCLT+CodeCLT_R, "Config-Smarttime": CodeCST+CodeCST_R,
                             "Attendtime-Optimize": CodeATO+CodeATO_R,
                             "Config-Retesttime": CodeCRT+CodeCRT_R, "H/C": round(HC+HC_R, 2), "H/C+OT": round(HCO+HCO_R, 2),
                             "ATO/TCM": 0 if (CodeTCM + CodeTCM_R) == 0 else round((CodeATO + CodeATO_R) / (CodeTCM + CodeTCM_R), 2)})
                print(datetime.datetime.now(),"表格")
                #Project top 10
                Projectlist_top = []
                Phaselist_top = []
                Projectlist_top_normal = {}
                Projectlist_top_retest = {}
                for i in Projectlist:
                    Projectlist_top.append(i["name"])
                    Phaselist_top.append(i["value"])
                # print(Projectlist_top)
                Projectlist_top = list(set(Projectlist_top))
                Phaselist_top = list(set(Phaselist_top))
                Phasesortorder = {'B(FVT)': 0, 'C(SIT)': 1, 'SIT2': 2, 'GSKU': 3, 'FFRT': 4, 'FFRT2': 5, 'FFRT3': 6, 'FFRT4': 7,
                                  'FFRT5': 8, 'FFRT6': 9, 'Wave': 10, 'Wave2': 11, 'Wave3': 12, 'Wave4': 13,
                                  'Wave5': 14, 'OOC': 15, 'OOC2': 16, 'OOC3': 17, 'OOC4': 18, 'OOC5': 19, 'OOC6': 20,
                                  'Others': 21}
                # print(Projectlist_top)
                Phaselist_top.sort(key=lambda x: Phasesortorder[x])
                for i in Projectlist_top:
                    ProjecttotalATO = 0.00
                    ProjecttotalRe = 0.00
                    datainphase_normal = {}
                    datainphase_retest = {}
                    for j in mock_data:#尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            ProjecttotalATO += j["Attendtime-Optimize"] + j["Config-Retesttime"]
                            datainphase_normal[j['Phase']] = j["Attendtime-Optimize"] + j["Config-Retesttime"]
                            if j['Phase'] in ["FFRT2", "FFRT3", "FFRT4", "FFRT5", "FFRT6", "FFRT7", "FFRT8"]:
                                ProjecttotalRe += j["Config-Retesttime"] + j["Attendtime-Optimize"]
                                datainphase_retest[j['Phase']] = j["Config-Retesttime"] + j["Attendtime-Optimize"]
                            else:
                                ProjecttotalRe += j["Config-Retesttime"]
                                datainphase_retest[j['Phase']] = j["Config-Retesttime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]
                # print(Projectlist_top_normal)
                # print(Projectlist_top_retest)
                # reverse为True从大到小
                top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1][0], reverse=True)
                top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1][0], reverse=True)



                # reverse为False从小到大
                # top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1], reverse=False)
                # top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1], reverse=False)
                # print(top_normal)
                # print(top_retest)
                if len(top_retest) > 10:#超过10个取最大的10个
                    #从大到小时取前十个
                    top_normal_new = top_normal[:10]
                    top_retest_new = top_retest[:10]
                    #从小到大时取最后十个
                    # top_normal_new = top_normal[-10:]
                    # top_retest_new = top_retest[-10:]
                else:
                    top_normal_new = top_normal
                    top_retest_new = top_retest
                # print(top_normal_new)
                # print(top_retest_new)
                Normal_key = []
                Normal_value = []
                for i in top_normal_new:
                    Normal_key.append(i[0])
                    # Normal_value.append(i[1])
                Top10["Execution_key"] = Normal_key
                # Top10["Normal_value"] = Normal_value#Value其实都不需要了，换成data了
                Regression_key = []
                Regression_value = []
                for i in top_retest_new:
                    Regression_key.append(i[0])
                    # Regression_value.append(i[1])
                Top10["Regression_key"] = Regression_key
                # Top10["Regression_value"] = Regression_value#Value其实都不需要了，换成data了
                print(datetime.datetime.now(), "图表1")
                for i in Phaselist_top:
                    data_Phase_E = []
                    for j in top_normal_new:
                        if i in j[1][1].keys():
                            data_Phase_E.append(j[1][1][i])
                        else:
                            data_Phase_E.append('null')
                    Execution_Top10.append({
                        "name": i,
                        "type": "bar",
                        "stack": "总量",
                        "barMaxWidth": 50,
                        "data": data_Phase_E
                    })
                    data_Phase_R = []
                    for j in top_retest_new:
                        if i in j[1][1].keys():
                            data_Phase_R.append(j[1][1][i])
                        else:
                            data_Phase_R.append('null')
                    Regression_Top10.append({
                        "name": i,
                        "type": "bar",
                        "stack": "总量",
                        "barMaxWidth": 50,
                        "data": data_Phase_R
                    })
                print(datetime.datetime.now(), "图表2")
                # print(Top10)
        data = {
            "err_ok": "0",
            "content": mock_data,
            "select": selectItem,
            "sear": searchalert,
            "rdchangelist": rdchangelist,
            "canEdit": canEdit,
            "proinfomation": proinfomation,
            'Sum': Sums,
            'Top10': Top10,
            "Execution_Top10": Execution_Top10,
            "Regression_Top10": Regression_Top10,
            'canExport': canExport,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'TestPlanSW/TestPlanSW_Summary.html', locals())

def TestPlanSW_Edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Edit"
    # MockData = [
    #             # {"caseid": "Basic", "contents": [
    #             #     {"id": 20191210, "caseid": "BFA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "unattendedtime": 695,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191211, "caseid": "BFA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 400, "unattendedtime": 400,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191212, "caseid": "BFA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 500, "unattendedtime": 500,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191213, "caseid": "BFA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 600, "unattendedtime": 600,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191214, "caseid": "BFA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 700, "unattendedtime": 700,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191215, "caseid": "BFA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 800, "unattendedtime": 800,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Interaction", "contents": [
    #             #     {"id": 20191216, "caseid": "IAA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 10,
    #             #      "unattendedtime": 10, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191217, "caseid": "IAA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 20,
    #             #      "unattendedtime": 20, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191218, "caseid": "IAA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 30,
    #             #      "unattendedtime": 30, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191219, "caseid": "IAA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 40,
    #             #      "unattendedtime": 40, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191220, "caseid": "IAA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 50,
    #             #      "unattendedtime": 50, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191221, "caseid": "IAA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 60,
    #             #      "unattendedtime": 60, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Connectivity", "contents": [
    #             #     {"id": 20191222, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191223, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191224, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191225, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191226, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191227, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Process and Stroage", "contents": [
    #             #     {"id": 20191228, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191229, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191230, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191231, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191232, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191233, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Performance", "contents": [
    #             #     {"id": 20191234, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191235, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191236, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191237, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191238, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191239, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game Test", "contents": [
    #             #     {"id": 20191240, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191241, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191242, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191243, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191244, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191245, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Stress", "contents": [
    #             #     {"id": 20191246, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191247, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191248, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191249, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191250, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191251, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Application", "contents": [
    #             #     {"id": 20191252, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191253, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191254, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191255, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191256, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191257, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Compal internal", "contents": [
    #             #     {"id": 20191258, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191259, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191260, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191261, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191262, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191263, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game unique", "contents": [
    #             #     {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Linux and DOS", "contents": [
    #             #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Accessories", "contents": [
    #             #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Gaming Unique", "contents": [
    #             #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             ]
    # newMockData = [
    #                #  {"caseid": "Game unique", "contents": [
    #                #      {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #  ]},
    #                # {"caseid": "Linux and DOS", "contents": [
    #                #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Accessories", "contents": [
    #                #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Gaming Unique", "contents": [
    #                #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                ]
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "testitem":"","version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
    ]
    title = [
             # {"caseid": "Basic", 'hasChildren': 'true'},
             # {"caseid": "Interaction", 'hasChildren': 'true'},
             # {"caseid": "Connectivity", 'hasChildren': 'true'},
             # {"caseid": "Process and Stroage", 'hasChildren': 'true'},
             # {"caseid": "Performance", 'hasChildren': 'true'},
             # {"caseid": "Game Test", 'hasChildren': 'true'},
             # {"caseid": "Stress", 'hasChildren': 'true'},
             # {"caseid": "Application", 'hasChildren': 'true'},
             # {"caseid": "Compal internal", 'hasChildren': 'true'},
             # {"caseid": "Game unique", 'hasChildren': 'true'},
             # {"caseid": "Linux and DOS", 'hasChildren': 'true'},
             # {"caseid": "Accessories", 'hasChildren': 'true'},
             # {"caseid": "Gaming Unique", 'hasChildren': 'true'},
             ]
    SKU = [
           # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
           # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
           # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
           # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
           # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
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
    Customer_list = TestProjectSW.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSW.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSW.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(FVT)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "SIT2":
                    PhaseValue = 2
                if m['Phase'] == "GSKU":
                    PhaseValue = 3
                if m['Phase'] == "Wave":
                    PhaseValue = 4
                if m['Phase'] == "Wave2":
                    PhaseValue = 5
                if m['Phase'] == "Wave3":
                    PhaseValue = 6
                if m['Phase'] == "Wave4":
                    PhaseValue = 7
                if m['Phase'] == "Wave5":
                    PhaseValue = 8
                if m['Phase'] == "OOC":
                    PhaseValue = 9
                if m['Phase'] == "OOC2":
                    PhaseValue = 10
                if m['Phase'] == "OOC3":
                    PhaseValue = 11
                if m['Phase'] == "OOC4":
                    PhaseValue = 12
                if m['Phase'] == "OOC5":
                    PhaseValue = 13
                if m['Phase'] == "OOC6":
                    PhaseValue = 14
                if m['Phase'] == "FFRT":
                    PhaseValue = 15
                if m['Phase'] == "FFRT2":
                    PhaseValue = 16
                if m['Phase'] == "FFRT3":
                    PhaseValue = 17
                if m['Phase'] == "FFRT4":
                    PhaseValue = 18
                if m['Phase'] == "FFRT5":
                    PhaseValue = 19
                if m['Phase'] == "FFRT6":
                    PhaseValue = 20
                if m['Phase'] == "Others":
                    PhaseValue = 21
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print (request.method)
    # print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            return HttpResponse(json.dumps(combine), content_type="application/json")
        elif request.GET.get("action") == "getCategory":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            # print(type(Phase))
            PhaseinItem = []
            if Phase == '0':
                Phase = 'B(FVT)'
                PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                PhaseinItem = ['Others']

            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # func = lambda z: dict([(x, y) for y, x in z.items()])

            # dic_ProjectSum = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # ProjectSum = TestProjectSW.objects.filter(**dic_ProjectSum).first()
            # # print(ProjectSum)
            # Retestitems = RetestItemSW.objects.filter(Projectinfo=ProjectSum).first()
            # # print(Retestitems)
            # # , Owner__contains="DQA"
            # basetimesum = TestPlanSW.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").values('Category2').annotate(
            #     Sum('BaseTime')).order_by('Category2')
            # print(TestPlanSW.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").values('Category2').distinct().count())


            if TestItemSW.objects.count()>0:
                for h in PhaseinItem:
                    # dic_Item = {'Customer': Customer, 'Phase': h}
                    # for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
                    #     title.append({"caseid": i['Category2']})
                    dic_ItemP = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
                    # dic_Item = {'Customer': Customer, 'Projectinfo': TestProjectSW.objects.filter(**dic_ItemP).first(), 'Phase': Phase}
                    dic_Item = {'Projectinfo': TestProjectSW.objects.filter(**dic_ItemP).first()}
                    if TestPlanSW.objects.filter(**dic_Item):
                        for i in TestPlanSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
                            title.append({"caseid": i['Category2']})
                            # print(TestPlanSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2').count())
                    if RetestItemSW.objects.filter(**dic_Item):
                        for i in RetestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
                            title.append({"caseid": i['Category2']})
                # print(title)
                seen = set()
                new_l = []
                for d in title:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        new_l.append(d)
                title = new_l
                # print(title)
            if not title:
                for h in PhaseinItem:
                    dic_Item = {'Customer': Customer, 'Phase': h}
                    for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
                        title.append({"caseid": i['Category2']})
            # if 'FFRT' in Phase:
            #     title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
            # print (title)
            # if TestPlanSW.objects.filter(Projectinfo=Projectinfos).first():
            #     for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
            #         title.append({"caseid": i['Category2']})
            # if RetestItemSW.objects.filter(**dic_Project).first():
            #     title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
            # # print (title)
            updateData = {
                "MockData": title,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        # elif request.GET.get("action") == "search":
        #     # if request.GET.get("customer") == "C38(NB)":
        #         Customer = request.GET.get('customer')
        #         Project = request.GET.get('project')
        #         Phase = request.GET.get('phase')
        #         # print(type(Phase))
        #         if Phase == '0':
        #             Phase = 'B(FVT)'
        #         if Phase == '1':
        #             Phase = 'C(SIT)'
        #         if Phase == '2':
        #             Phase = 'FFRT'
        #         if Phase == '3':
        #             Phase = 'Others'
        #         dic_Item=     {'Customer': Customer, 'Phase': Phase}
        #         dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #         # print(dic_Project)
        #         Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
        #         # print(Projectinfos.Owner.all())
        #         # print(Projectinfos)
        #         canEdit = 0
        #         current_user = request.session.get('user_name')
        #         if Projectinfos:
        #             for i in Projectinfos.Owner.all():
        #                 # print(i.username,current_user)
        #                 # print(type(i.username),type(current_user))
        #                 if i.username == current_user:
        #                     canEdit = 1
        #                     break
        #             SKUlist=[Projectinfos.SKU1,Projectinfos.SKU2,Projectinfos.SKU3,Projectinfos.SKU4,Projectinfos.SKU5,
        #                       Projectinfos.SKU6,Projectinfos.SKU7,Projectinfos.SKU8,Projectinfos.SKU9,Projectinfos.SKU10,
        #                       Projectinfos.SKU11,Projectinfos.SKU12,Projectinfos.SKU13,Projectinfos.SKU14,Projectinfos.SKU15,
        #                       Projectinfos.SKU16,Projectinfos.SKU17,Projectinfos.SKU18,Projectinfos.SKU19,Projectinfos.SKU20]
        #             n=1
        #             for i in SKUlist:
        #                 if i:
        #                     SKUno='SKU%s'%n
        #                     SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
        #                     n+=1
        #         # print(SKU)
        #         if canEdit:
        #             itemlist = []
        #             for i in TestItemSW.objects.filter(Customer=Customer,Phase=Phase):
        #                 itemlist.append(i.id)
        #             # print (itemlist,'yyy')
        #             existitem = []
        #             for i in Projectinfos.testplansw_set.all():
        #                 existitem.append(i.Items.id)
        #             # print(existitem)
        #             for i in itemlist:
        #                 if i in existitem:
        #                     continue
        #                 else:
        #                     # print(TestProjectSW.objects.filter(**dic_Project).first())
        #                     TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),
        #                                               Projectinfo=TestProjectSW.objects.filter(**dic_Project).first())
        #             # print (TestItemSW.objects.all().values('Category2').distinct().count())
        #         m=0
        #         for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct():
        #             # print(type(i),i)
        #             title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
        #             m+=1
        #         dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #         if RetestItemSW.objects.filter(**dic_Project).first():
        #             title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
        #         # print(title)
        #
        #
        #         updateData = {
        #             "MockData": title,
        #             "SKU": SKU,
        #             "selectMsg": combine,
        #             "canEdit": canEdit
        #         }
        #         return HttpResponse(json.dumps(updateData), content_type="application/json")

        elif request.GET.get("action") == "getContent":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category2=request.GET.get('category')
            # print(Category2)
            # print(Phase, type(Phase))
            #Search的时候不需要知道Items是link那个Item的，读的都是TestPlan里面的测试当下的Item信息，并且创建时可能就没有Link case（比如测试当下的版本不是上传时的最新版本，因为现在只有excel才能创建PLan）
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
            # print(Category2)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [
                    Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20,
                            Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                            Projectinfos.SKU25,
                            Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                            Projectinfos.SKU30,
                            Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                            Projectinfos.SKU35,
                            Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                            Projectinfos.SKU40,
                           ]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1
            # print(SKU)
            # print(type(Phase))
            # if canEdit:
            #     itemlist = []
            #     for i in TestItemSW.objects.filter(Customer=Customer, Phase=Phase):
            #         itemlist.append(i.id)
            #     # print (itemlist,'yyy')
            #     existitem = []
            #     for i in Projectinfos.testplansw_set.all():
            #         existitem.append(i.Items.id)
            #     # print(existitem)
            #     for i in itemlist:
            #         if i in existitem:
            #             continue
            #         else:
            #             # print(TestProjectSW.objects.filter(**dic_Project).first())
            #             TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),Projectinfo=TestProjectSW.objects.filter(**dic_Project).first(),
            #             Customer=TestItemSW.objects.get(id=i).Customer, Phase=TestItemSW.objects.get(id=i).Phase,
            #             ItemNo_d=TestItemSW.objects.get(id=i).ItemNo_d, Item_d=TestItemSW.objects.get(id=i).Item_d,
            #             TestItems=TestItemSW.objects.get(id=i).TestItems, Category=TestItemSW.objects.get(id=i).Category,
            #             Category2=TestItemSW.objects.get(id=i).Category2, Version=TestItemSW.objects.get(id=i).Version,
            #             ReleaseDate=TestItemSW.objects.get(id=i).ReleaseDate, Owner=TestItemSW.objects.get(id=i).Owner,
            #             Priority=TestItemSW.objects.get(id=i).Priority, TDMSTotalTime=TestItemSW.objects.get(id=i).TDMSTotalTime,
            #             BaseTime=TestItemSW.objects.get(id=i).BaseTime, TDMSUnattendedTime=TestItemSW.objects.get(id=i).TDMSUnattendedTime,
            #             BaseAotomationTime1SKU=TestItemSW.objects.get(id=i).BaseAotomationTime1SKU, Chramshell=TestItemSW.objects.get(id=i).Chramshell,
            #             ConvertibaleNBMode=TestItemSW.objects.get(id=i).ConvertibaleNBMode, ConvertibaleYogaPadMode=TestItemSW.objects.get(id=i).ConvertibaleYogaPadMode,
            #             DetachablePadMode=TestItemSW.objects.get(id=i).DetachablePadMode, DetachableWDockmode=TestItemSW.objects.get(id=i).DetachableWDockmode,
            #             PhaseFVT=TestItemSW.objects.get(id=i).PhaseFVT, PhaseSIT=TestItemSW.objects.get(id=i).PhaseSIT,
            #             PhaseFFRT=TestItemSW.objects.get(id=i).PhaseFFRT, Coverage=TestItemSW.objects.get(id=i).Coverage,
            #             editor=request.session.get('user_name'),edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            # print(request.GET)
            # print(request.GET.get("category"))

            if request.GET.get("category") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":
                RetestItemSWinfo=RetestItemSW.objects.filter(**dic_Project)
                # print('Retest')
                # print(RetestItemSWinfo)
                if RetestItemSWinfo:
                    for i in RetestItemSWinfo:
                        planOptimize=[]
                        SKUlist_R = {
                                    "SKU1":i.SKU1, "SKU2":i.SKU2, "SKU3":i.SKU3, "SKU4":i.SKU4,"SKU5":i.SKU5,
                                   "SKU6":i.SKU6, "SKU7":i.SKU7, "SKU8":i.SKU8, "SKU9":i.SKU9,"SKU10":i.SKU10,
                                   "SKU11":i.SKU11, "SKU12":i.SKU12,"SKU13": i.SKU13, "SKU14":i.SKU14,"SKU15":i.SKU15,
                                   "SKU16":i.SKU16, "SKU17":i.SKU17, "SKU18":i.SKU18, "SKU19":i.SKU19,"SKU20":i.SKU20,
                            "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24, "SKU25": i.SKU25,
                            "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29, "SKU30": i.SKU30,
                            "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34, "SKU35": i.SKU35,
                            "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39, "SKU40": i.SKU40,
                        }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_R.keys():
                                    planOptimize.append(SKUlist_R[j["skuNo"]])
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS':i.BaseTimeSupport,'TFC':i.TimewConfigFollowmatrix,'conAtime':i.ConfigAutomationTime,'conLtime':i.ConfigLeverageTime,
                                'conSitemInAll':i.ConfigSmartItemPer,'conStime':i.ConfigSmartTime,'proTS':i.ProjectTestSKUOptimize,'ATO':i.AttendTimeOptimize
                            })
                    # print(newContents)
            else:
                # print('Others')
                # Iteminfos = TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category2': Category2, "Projectinfo": Projectinfos}
                if Projectinfos:
                    x = 0

                    for i in TestPlanSW.objects.filter(**dicPlan):
                        x += 1
                        # print(i,type(i))
                        # print(i.id)
                        planOptimize = []
                        SKUlist_T = {
                            "SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                     "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                            "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24, "SKU25": i.SKU25,
                            "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29, "SKU30": i.SKU30,
                            "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34, "SKU35": i.SKU35,
                            "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39, "SKU40": i.SKU40,
                        }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_T.keys():
                                planOptimize.append(SKUlist_T[j["skuNo"]])
                        # print(planOptimize)
                        # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                        newContents.append(
                            {  # item
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT,
                                'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                # plan
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize,
                                'CRC': i.ConfigRetestCycle, 'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })
                    # print(newContents)
                    # print(x)
            # print(newContents)
            updateData = {
                "content": newContents,
                "SKU": SKU,
                "canEdit": canEdit
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")

        elif request.GET.get("action") == "DeleteAll":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category2=request.GET.get('category')
            # print(Category2)
            # print(Phase, type(Phase))
            #Search的时候不需要知道Items是link那个Item的，读的都是TestPlan里面的测试当下的Item信息，并且创建时可能就没有Link case（比如测试当下的版本不是上传时的最新版本，因为现在只有excel才能创建PLan）
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
            # print(Category2)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            # Delete TestPlan&RetestItemSW
            if Projectinfos:
                Deldic = {'Customer': Customer, 'Phase': Phase, "Projectinfo": Projectinfos}
                if TestPlanSW.objects.filter(**Deldic):
                    # print(1)
                    TestPlanSW.objects.filter(**Deldic).delete()
                if RetestItemSW.objects.filter(**Deldic):
                    # print(2)
                    RetestItemSW.objects.filter(**Deldic).delete()
            # Searchs
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [
                    Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20,
                            Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                            Projectinfos.SKU25,
                            Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                            Projectinfos.SKU30,
                            Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                            Projectinfos.SKU35,
                            Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                            Projectinfos.SKU40,
                           ]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1
            # print(SKU)
            # print(type(Phase))
            # if canEdit:
            #     itemlist = []
            #     for i in TestItemSW.objects.filter(Customer=Customer, Phase=Phase):
            #         itemlist.append(i.id)
            #     # print (itemlist,'yyy')
            #     existitem = []
            #     for i in Projectinfos.testplansw_set.all():
            #         existitem.append(i.Items.id)
            #     # print(existitem)
            #     for i in itemlist:
            #         if i in existitem:
            #             continue
            #         else:
            #             # print(TestProjectSW.objects.filter(**dic_Project).first())
            #             TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),Projectinfo=TestProjectSW.objects.filter(**dic_Project).first(),
            #             Customer=TestItemSW.objects.get(id=i).Customer, Phase=TestItemSW.objects.get(id=i).Phase,
            #             ItemNo_d=TestItemSW.objects.get(id=i).ItemNo_d, Item_d=TestItemSW.objects.get(id=i).Item_d,
            #             TestItems=TestItemSW.objects.get(id=i).TestItems, Category=TestItemSW.objects.get(id=i).Category,
            #             Category2=TestItemSW.objects.get(id=i).Category2, Version=TestItemSW.objects.get(id=i).Version,
            #             ReleaseDate=TestItemSW.objects.get(id=i).ReleaseDate, Owner=TestItemSW.objects.get(id=i).Owner,
            #             Priority=TestItemSW.objects.get(id=i).Priority, TDMSTotalTime=TestItemSW.objects.get(id=i).TDMSTotalTime,
            #             BaseTime=TestItemSW.objects.get(id=i).BaseTime, TDMSUnattendedTime=TestItemSW.objects.get(id=i).TDMSUnattendedTime,
            #             BaseAotomationTime1SKU=TestItemSW.objects.get(id=i).BaseAotomationTime1SKU, Chramshell=TestItemSW.objects.get(id=i).Chramshell,
            #             ConvertibaleNBMode=TestItemSW.objects.get(id=i).ConvertibaleNBMode, ConvertibaleYogaPadMode=TestItemSW.objects.get(id=i).ConvertibaleYogaPadMode,
            #             DetachablePadMode=TestItemSW.objects.get(id=i).DetachablePadMode, DetachableWDockmode=TestItemSW.objects.get(id=i).DetachableWDockmode,
            #             PhaseFVT=TestItemSW.objects.get(id=i).PhaseFVT, PhaseSIT=TestItemSW.objects.get(id=i).PhaseSIT,
            #             PhaseFFRT=TestItemSW.objects.get(id=i).PhaseFFRT, Coverage=TestItemSW.objects.get(id=i).Coverage,
            #             editor=request.session.get('user_name'),edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            # print(request.GET)
            # print(request.GET.get("category"))

            if request.GET.get("category") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":
                RetestItemSWinfo=RetestItemSW.objects.filter(**dic_Project)
                # print('Retest')
                # print(RetestItemSWinfo)
                if RetestItemSWinfo:
                    for i in RetestItemSWinfo:
                        planOptimize=[]
                        SKUlist_R = {
                                    "SKU1":i.SKU1, "SKU2":i.SKU2, "SKU3":i.SKU3, "SKU4":i.SKU4,"SKU5":i.SKU5,
                                   "SKU6":i.SKU6, "SKU7":i.SKU7, "SKU8":i.SKU8, "SKU9":i.SKU9,"SKU10":i.SKU10,
                                   "SKU11":i.SKU11, "SKU12":i.SKU12,"SKU13": i.SKU13, "SKU14":i.SKU14,"SKU15":i.SKU15,
                                   "SKU16":i.SKU16, "SKU17":i.SKU17, "SKU18":i.SKU18, "SKU19":i.SKU19,"SKU20":i.SKU20,
                            "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24, "SKU25": i.SKU25,
                            "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29, "SKU30": i.SKU30,
                            "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34, "SKU35": i.SKU35,
                            "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39, "SKU40": i.SKU40,
                        }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_R.keys():
                                    planOptimize.append(SKUlist_R[j["skuNo"]])
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS':i.BaseTimeSupport,'TFC':i.TimewConfigFollowmatrix,'conAtime':i.ConfigAutomationTime,'conLtime':i.ConfigLeverageTime,
                                'conSitemInAll':i.ConfigSmartItemPer,'conStime':i.ConfigSmartTime,'proTS':i.ProjectTestSKUOptimize,'ATO':i.AttendTimeOptimize
                            })
                    # print(newContents)
            else:
                # print('Others')
                # Iteminfos = TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category2': Category2, "Projectinfo": Projectinfos}
                if Projectinfos:
                    x = 0

                    for i in TestPlanSW.objects.filter(**dicPlan):
                        x += 1
                        # print(i,type(i))
                        # print(i.id)
                        planOptimize = []
                        SKUlist_T = {
                            "SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                     "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                            "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24, "SKU25": i.SKU25,
                            "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29, "SKU30": i.SKU30,
                            "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34, "SKU35": i.SKU35,
                            "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39, "SKU40": i.SKU40,
                        }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_T.keys():
                                planOptimize.append(SKUlist_T[j["skuNo"]])
                        # print(planOptimize)
                        # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                        newContents.append(
                            {  # item
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT,
                                'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                # plan
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize,
                                'CRC': i.ConfigRetestCycle, 'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })
                    # print(newContents)
                    # print(x)
            # print(newContents)
            updateData = {
                "content": newContents,
                "SKU": SKU,
                "canEdit": canEdit
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")

    if request.method == "POST":
        # print(request.POST)
        # print(request.body)
        if request.POST.get('action')=='edit':
            # print(request.POST)
            updatedate = {
                # 'FeatureSupport': request.POST.get('FS'), "BaseTimeSupport": request.POST.get('BTS'),
                #           "TE": request.POST.get('TE'),"Schedule": request.POST.get('schedule'),"ProjectTestSKUfollowMatrix":request.POST.get('starttime'),
                #           "TimewConfigFollowmatrix":request.POST.get('TFC'),"ConfigAutomationItem":request.POST.get('conAitem'),
                #           "ConfigAutomationTime":request.POST.get('CAT'),"ConfigLeverageItem":request.POST.get('conLitem'),
                #           "ConfigLeverageTime":request.POST.get('CLT'),"CommentsLeverage":request.POST.get('comments1'),
                #           "ConfigSmartItem":request.POST.get('conSitem'),"ConfigSmartItemPer":request.POST.get(''),
                          }
            Customer = request.POST.get('customer')
            Project = request.POST.get('project')
            Phase = request.POST.get('phase')
            # print(type(Phase))
            #edit时也不需要知道Items是link那个Item的，直接通过id查找的
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
            # update 直接找到这条的ID就可以了，他的关联的Test Item是不会变的。
            # for h in PhaseinItem:
            #     dic_Item = {'Customer': Customer, 'Phase': h}
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(float('1.1'))
            #print(float('NULL'))
            # print(float(''))#hui baocuo
            if 'FS' in request.POST.keys():
                updatedate['FeatureSupport']=request.POST.get('FS')
            if 'BTS' in request.POST.keys():
                if request.POST.get('BTS'):
                    updatedate['BaseTimeSupport'] = float(request.POST.get('BTS'))
                else:
                    updatedate['BaseTimeSupport']=None
            if 'TE' in request.POST.keys():
                updatedate['TE'] = request.POST.get('TE')
            if 'schedule' in request.POST.keys():
                updatedate['Schedule'] = request.POST.get('schedule')
            if 'starttime' in request.POST.keys():
                if request.POST.get('starttime'):
                    updatedate['ProjectTestSKUfollowMatrix'] = float(request.POST.get('starttime'))
                else:
                    updatedate['ProjectTestSKUfollowMatrix'] =None
            if 'TFC' in request.POST.keys():
                if request.POST.get('TFC'):
                    updatedate['TimewConfigFollowmatrix'] = float(request.POST.get('TFC'))
                else:
                    updatedate['TimewConfigFollowmatrix']=None
            if 'conAitem' in request.POST.keys():
                updatedate['ConfigAutomationItem'] = request.POST.get('conAitem')
            if 'CAT' in request.POST.keys():
                if request.POST.get('CAT'):
                    updatedate['ConfigAutomationTime'] = float(request.POST.get('CAT'))
                else:
                    updatedate['ConfigAutomationTime']=None
            if 'conLitem' in request.POST.keys():
                updatedate['ConfigLeverageItem'] = request.POST.get('conLitem')
            if 'CLT' in request.POST.keys():
                if request.POST.get('CLT'):
                    updatedate['ConfigLeverageTime'] = float(request.POST.get('CLT'))
                else:
                    updatedate['ConfigLeverageTime']=None
            if 'comments1' in request.POST.keys():
                updatedate['CommentsLeverage'] = request.POST.get('comments1')
            if 'conSitem' in request.POST.keys():
                updatedate['ConfigSmartItem'] = request.POST.get('conSitem')
            if 'conSitemInAll' in request.POST.keys():
                if request.POST.get('conSitemInAll'):
                    updatedate['ConfigSmartItemPer'] = float(request.POST.get('conSitemInAll'))
                else:
                    updatedate['ConfigSmartItemPer']=None
            if 'CST' in request.POST.keys():
                if request.POST.get('CST'):
                    print(request.POST.get('CST'))
                    print(float(request.POST.get('CST')))
                    updatedate['ConfigSmartTime'] = float(request.POST.get('CST'))
                else:
                    updatedate['ConfigSmartTime']=None
            if 'comments2' in request.POST.keys():
                updatedate['CommentsSmart'] = request.POST.get('comments2')
            if 'proTS' in request.POST.keys():
                if request.POST.get('proTS'):
                    updatedate['ProjectTestSKUOptimize'] = float(request.POST.get('proTS'))
                else:
                    updatedate['ProjectTestSKUOptimize']=None
            if 'ATO' in request.POST.keys():
                if request.POST.get('ATO'):
                    updatedate['AttendTimeOptimize'] = float(request.POST.get('ATO'))
                else:
                    updatedate['AttendTimeOptimize']=None
            if 'CRC' in request.POST.keys():
                if request.POST.get('CRC'):
                    updatedate['ConfigRetestCycle'] = float(request.POST.get('CRC'))
                else:
                    updatedate['ConfigRetestCycle']=None
            if 'CRS' in request.POST.keys():
                if request.POST.get('CRS'):
                    updatedate['ConfigRetestSKU'] = float(request.POST.get('CRS'))
                else:
                    updatedate['ConfigRetestSKU']=None
            if 'CRT' in request.POST.keys():
                if request.POST.get('CRT'):
                    updatedate['ConfigRetestTime'] = float(request.POST.get('CRT'))
                else:
                    updatedate['ConfigRetestTime'] =None
            updatedate['editor'] = request.session.get('user_name')
            updatedate['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 'planOptimize' in request.POST.keys():
                # print('ppp')
                planOptimize = request.POST.getlist('planOptimize',[])
            # print(planOptimize,'111')

            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(dic_Project)
            # print (Projectinfos)
            if Projectinfos:
                SKUlist = [
                        Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20,
                        Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                        Projectinfos.SKU25,
                        Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                        Projectinfos.SKU30,
                        Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                        Projectinfos.SKU35,
                        Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                        Projectinfos.SKU40,
                           ]
                # print(SKUlist)
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1

            x=0
            # print(SKU)
            for k in SKU:
                updatedate[k["skuNo"]] = planOptimize[x]
                x+=1
            print((updatedate))


            Category2 = request.POST.get('category')
            if Category2 == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":

                RetestItemSW.objects.filter(id=request.POST.get('ID')).update(**updatedate)
            else:
                TestPlanSW.objects.filter(id=request.POST.get('ID')).update(**updatedate)
            return HttpResponse(json.dumps({'editResult':1}), content_type="application/json")
        # print(request.body)        # print(json.loads(request.body))

        #excel

        # responseData = json.loads(request.body)
        # if 'ExcelData' in responseData.keys():
        if request.POST.get('action')=='submitFFRTData':
            # print(request.POST)
            submitResult = 0

            Phase = request.POST.get('Phase')
            # print(Phase)
            #submitFFRTData时也不需要link case，因为肯定只有FFRT，2，3，4，5，6才有这个，并且都是加到Other这个catogory的
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
                # PhaseinItem = ['Others']
            # submit目前只有FFRT会有新增，其他的不会有，所以值加到RetestItemSW里面，他没有关联TestItem
            # for h in PhaseinItem:
            #     dic_Item = {'Customer': Customer, 'Phase': h}
            projctcheck = {'Customer': request.POST.get('customer'), 'Project': request.POST.get('project'),'Phase':Phase}
            Reitemcheck = {'Customer': request.POST.get('customer'), 'Project': request.POST.get('project'),'Phase':Phase,
                           'ItemNo_d': request.POST.get('caseid'), 'Item_d': request.POST.get('casename'),
                           'TestItems':request.POST.get('testitem')}
            # print(projctcheck)
            # print(Reitemcheck)
            if RetestItemSW.objects.filter(**Reitemcheck).first():
                print(Reitemcheck,'exist')
            else:
                adddic = {}
                adddic['Customer'] = request.POST.get('customer')
                adddic['Phase'] = Phase
                adddic['Project'] = request.POST.get('project')
                adddic['ItemNo_d'] = request.POST.get('caseid')
                adddic['Item_d'] = request.POST.get('casename')
                adddic['TestItems'] = request.POST.get('testitem')
                adddic['Category'] = "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"
                adddic['Category2'] = "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"
                adddic['Version'] = request.POST.get('version')
                adddic['ReleaseDate'] = request.POST.get('releasedate')
                adddic['Owner'] = request.POST.get('owner')
                adddic['Priority'] = request.POST.get('priority')
                if request.POST.get('basetime'):
                    adddic['BaseTime'] = float(request.POST.get('basetime'))
                if request.POST.get('unattendedtime'):
                    adddic['TDMSUnattendedTime'] = float(request.POST.get('unattendedtime'))
                if request.POST.get('basetimeA'):
                    adddic['BaseAotomationTime1SKU'] = float(request.POST.get('basetimeA'))
                adddic['Chramshell'] = request.POST.get('chramshell')
                adddic['ConvertibaleNBMode'] = request.POST.get('cover_NB')
                adddic['ConvertibaleYogaPadMode'] = request.POST.get('cover_Yoga')
                adddic['DetachablePadMode'] = request.POST.get('detach_Pad')
                adddic['DetachableWDockmode'] = request.POST.get('detach_W')
                adddic['PhaseFFRT'] = request.POST.get('PhaseF')
                # adddic['Coverage'] = request.POST.get('')
                # print(projctcheck)
                adddic['Projectinfo'] = TestProjectSW.objects.get(**projctcheck)
                adddic['FeatureSupport'] = request.POST.get('FS')
                if request.POST.get('BTS'):
                    adddic['BaseTimeSupport'] = float(request.POST.get('BTS'))
                adddic['TE'] = request.POST.get('TE')
                adddic['Schedule'] = request.POST.get('schedule')
                if request.POST.get('starttime'):
                    adddic['ProjectTestSKUfollowMatrix'] = float(request.POST.get('starttime'))
                if request.POST.get('TFC'):
                    adddic['TimewConfigFollowmatrix'] = float(request.POST.get('TFC'))
                adddic['ConfigAutomationItem'] = request.POST.get('conAitem')
                if request.POST.get('CAT'):
                    adddic['ConfigAutomationTime'] = float(request.POST.get('CAT'))
                adddic['ConfigLeverageItem'] = request.POST.get('conLitem')
                if request.POST.get('CLT'):
                    adddic['ConfigLeverageTime'] = float(request.POST.get('CLT'))
                adddic['CommentsLeverage'] = request.POST.get('comments1')
                adddic['ConfigSmartItem'] = request.POST.get('conSitem')
                if request.POST.get('conSitemInAll'):
                    adddic['ConfigSmartItemPer'] = float(request.POST.get('conSitemInAll'))
                if request.POST.get('CST'):
                    adddic['ConfigSmartTime'] = float(request.POST.get('CST'))
                adddic['CommentsSmart'] = request.POST.get('comments2')
                if request.POST.get('proTS'):
                    adddic['ProjectTestSKUOptimize'] = float(request.POST.get('proTS'))
                if request.POST.get('ATO'):
                    adddic['AttendTimeOptimize'] = float(request.POST.get('ATO'))
                if request.POST.get('CRC'):
                    adddic['ConfigRetestCycle'] = float(request.POST.get('CRC'))
                if request.POST.get('CRS'):
                    adddic['ConfigRetestSKU'] = float(request.POST.get('CRS'))
                if request.POST.get('CRT'):
                    adddic['ConfigRetestTime'] = float(request.POST.get('CRT'))
                planOptimize = request.POST.getlist('planOptimize',[])
                k=1
                # print(planOptimize)
                for m in planOptimize:
                    key = "SKU%s" % k
                    # print(key)
                    adddic[key]=m
                    # print(m)
                    # print(adddic[key])
                    k+=1
                adddic['editor'] = request.session.get('user_name')
                adddic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # print(adddic)
                # print(updatedic)
                # for m in updatedic:
                #     print (m,type(updatedic[m]))
                # print(adddic)
                RetestItemSW.objects.create(**adddic)
                submitResult=1
                # print(submitResult)
            return HttpResponse(json.dumps({'submitResult':submitResult}), content_type="application/json")
        if 'ExcelData' in str(request.body):
            responseData = json.loads(request.body)
            xlsxlist = json.loads(responseData['ExcelData'])
            if responseData:
                # print(responseData)
                check_dic_list = []
                check_list_list = []
                Phase = str(responseData['phase'])
                # print(Phase, type(Phase))
                if Phase == '0':
                    Phase = 'B(FVT)'
                    # PhaseinItem = ['B(FVT)']
                if Phase == '1':
                    Phase = 'C(SIT)'
                    # PhaseinItem = ['C(SIT)']
                if Phase == '2':
                    Phase = 'SIT2'
                    # PhaseinItem = ['C(SIT)']
                if Phase == '3':
                    Phase = 'GSKU'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '4':
                    Phase = 'Wave'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '5':
                    Phase = 'Wave2'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '6':
                    Phase = 'Wave3'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '7':
                    Phase = 'Wave4'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '8':
                    Phase = 'Wave5'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '9':
                    Phase = 'OOC'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '10':
                    Phase = 'OOC2'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '11':
                    Phase = 'OOC3'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '12':
                    Phase = 'OOC4'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '13':
                    Phase = 'OOC5'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '14':
                    Phase = 'OOC6'
                    # PhaseinItem = ['C(SIT)', 'FFRT']
                if Phase == '15':
                    Phase = 'FFRT'
                    # PhaseinItem = ['FFRT']
                if Phase == '16':
                    Phase = 'FFRT2'
                    # PhaseinItem = ['FFRT']
                if Phase == '17':
                    Phase = 'FFRT3'
                    # PhaseinItem = ['FFRT']
                if Phase == '18':
                    Phase = 'FFRT4'
                    # PhaseinItem = ['FFRT']
                if Phase == '19':
                    Phase = 'FFRT5'
                    # PhaseinItem = ['FFRT']
                if Phase == '20':
                    Phase = 'FFRT6'
                    # PhaseinItem = ['FFRT']
                if Phase == '21':
                    Phase = 'Others'
                    # PhaseinItem = ['Others']
                # print(Phase)
                dic_Project = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(dic_Project)
                item_nodata = [{'Customer':'Customer','Phase':'Phase','ItemNo_d': 'Case_ID', 'Item_d': 'Case_Name','TestItems':'Test_Items'}]
                item_changeddata = [{'Customer':'Customer','Phase':'Phase','ItemNo_d': 'Case_ID', 'Item_d': 'Case_Name','TestItems':'Test_Items'}]
                num = 0
                for i in xlsxlist:
                    # print(i)
                    num+=1
                    # print(num)
                    #RetestFFRT
                    if 'Category2' in i.keys():#转换的文档中最后会多一些空值
                        # print(i['Category2'])
                        ##FFRT,2,3,4,5,6才会有,存到RetestItem表里
                        if i['Category2']== "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":#也不需要link case
                            # print('Others')
                            # print(i['ItemNo_d'], i['Item_d'], i['TestItems'])

                            if 'ItemNo_d' in i.keys() and 'Item_d' in i.keys() and 'TestItems' in i.keys():

                                # print('yeah')
                                check_dicRetestplan= {'Customer':responseData['customer'], 'Project':responseData['project'],
                                  'Phase':Phase,'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems'],
                                                      'Projectinfo':TestProjectSW.objects.get(**dic_Project)}

                                # print(check_dicRetestplan)

                                editplan = RetestItemSW.objects.filter(**check_dicRetestplan).first()

                                # print(type(editplan),editplan)
                                # edit
                                if editplan:#如果重复测试同一个case，excel上传时只能将其中某一项（如TestItem）改下名（如加-1），如果不这样，excel上传时就不能修改，只能新增。
                                    print('edit in others category')

                                    if 'Category' in i.keys():
                                        editplan.Category = i['Category']
                                    if 'Category2' in i.keys():
                                        editplan.Category2 = i['Category2']
                                    if 'Version' in i.keys():
                                        editplan.Version = i['Version']
                                    if 'ReleaseDate' in i.keys():
                                        editplan.ReleaseDate = i['ReleaseDate']
                                    if 'Owner' in i.keys():
                                        editplan.Owner = i['Owner']
                                    if 'Priority' in i.keys():
                                        editplan.Priority = i['Priority']
                                    if 'TDMSsTotalTime' in i.keys():
                                        if i['TDMSTotalTime']:
                                            editplan.TDMSTotalTime = float(i['TDMSTotalTime'])
                                        else:
                                            editplan.TDMSTotalTime = 0
                                    else:
                                        editplan.TDMSTotalTime = None
                                    if 'BaseTime' in i.keys():
                                        # print(i['BaseTime'])
                                        if i['BaseTime']:
                                            editplan.BaseTime = float(i['BaseTime'])
                                        else:
                                            editplan.BaseTime = 0
                                    else:
                                        editplan.BaseTime = 0
                                    if 'TDMSUnattendedTime' in i.keys():
                                        if i['TDMSUnattendedTime']:
                                            editplan.TDMSUnattendedTime = float(i['TDMSUnattendedTime'])
                                        else:
                                            editplan.TDMSUnattendedTime = 0
                                    else:
                                        editplan.TDMSUnattendedTime =None
                                    if 'BaseAotomationTime1SKU' in i.keys():
                                        if i['BaseAotomationTime1SKU']:
                                            editplan.BaseAotomationTime1SKU = float(i['BaseAotomationTime1SKU'])
                                        else:
                                            editplan.BaseAotomationTime1SKU = 0
                                    else:
                                        editplan.BaseAotomationTime1SKU = None
                                    if 'Chramshell' in i.keys():
                                        editplan.Chramshell = i['Chramshell']
                                    if 'ConvertibaleNBMode' in i.keys():
                                        editplan.ConvertibaleNBMode = i['ConvertibaleNBMode']
                                    if 'ConvertibaleYogaPadMode' in i.keys():
                                        editplan.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                                    if 'DetachablePadMode' in i.keys():
                                        editplan.DetachablePadMode = i['DetachablePadMode']
                                    if 'DetachableWDockmode' in i.keys():
                                        editplan.DetachableWDockmode = i['DetachableWDockmode']
                                    if 'PhaseFVT' in i.keys():
                                        editplan.PhaseFVT = i['PhaseFVT']
                                    if 'PhaseSIT' in i.keys():
                                        editplan.PhaseSIT = i['PhaseSIT']
                                    if 'PhaseFFRT' in i.keys():
                                        editplan.PhaseFFRT = i['PhaseFFRT']
                                    if 'Coverage' in i.keys():
                                        editplan.Coverage = i['Coverage']

                                    if 'FeatureSupport' in i.keys():
                                        editplan.FeatureSupport = i['FeatureSupport']
                                    if 'BaseTimeSupport' in i.keys():
                                        if i['BaseTimeSupport']:
                                            editplan.BaseTimeSupport = float(i['BaseTimeSupport'])
                                    else:
                                        editplan.BaseTimeSupport = None
                                    if 'TE' in i.keys():
                                        editplan.TE = i['TE']
                                    if 'Schedule' in i.keys():
                                        editplan.Schedule = i['Schedule']
                                    if 'ProjectTestSKUfollowMatrix' in i.keys():
                                        if i['ProjectTestSKUfollowMatrix']:
                                            editplan.ProjectTestSKUfollowMatrix = float(i['ProjectTestSKUfollowMatrix'])
                                    else:
                                        editplan.ProjectTestSKUfollowMatrix =None
                                    if 'TimewConfigFollowmatrix' in i.keys():
                                        if i['TimewConfigFollowmatrix']:
                                            editplan.TimewConfigFollowmatrix = float(i['TimewConfigFollowmatrix'])
                                    else:
                                        editplan.TimewConfigFollowmatrix = None
                                    if 'ConfigAutomationItem' in i.keys():
                                        editplan.ConfigAutomationItem = i['ConfigAutomationItem']
                                    if 'ConfigAutomationTime' in i.keys():
                                        if i['ConfigAutomationTime']:
                                            editplan.ConfigAutomationTime = float(i['ConfigAutomationTime'])
                                    else:
                                        editplan.ConfigAutomationTime = None
                                    if 'ConfigLeverageItem' in i.keys():
                                        editplan.ConfigLeverageItem = i['ConfigLeverageItem']
                                    if 'ConfigLeverageTime' in i.keys():
                                        if i['ConfigLeverageTime']:
                                            editplan.ConfigLeverageTime = float(i['ConfigLeverageTime'])
                                    else:
                                        editplan.ConfigLeverageTime =None
                                    if 'CommentsLeverage' in i.keys():
                                        editplan.CommentsLeverage = i['CommentsLeverage']
                                    if 'ConfigSmartItem' in i.keys():
                                        editplan.ConfigSmartItem = i['ConfigSmartItem']
                                    if 'ConfigSmartItemPer' in i.keys():
                                        if i['ConfigSmartItemPer']:
                                            editplan.ConfigSmartItemPer = float(i['ConfigSmartItemPer'])
                                    else:
                                        editplan.ConfigSmartItemPer =None
                                    if 'ConfigSmartTime' in i.keys():
                                        if i['ConfigSmartTime']:
                                            editplan.ConfigSmartTime = float(i['ConfigSmartTime'])
                                    else:
                                        editplan.ConfigSmartTime =None
                                    if 'CommentsSmart' in i.keys():
                                        editplan.CommentsSmart = i['CommentsSmart']
                                    if 'ProjectTestSKUOptimize' in i.keys():
                                        if i['ProjectTestSKUOptimize']:
                                            editplan.ProjectTestSKUOptimize = float(i['ProjectTestSKUOptimize'])
                                    else:
                                        editplan.ProjectTestSKUOptimize =None
                                    if 'AttendTimeOptimize' in i.keys():
                                        if i['AttendTimeOptimize']:
                                            editplan.AttendTimeOptimize = float(i['AttendTimeOptimize'])
                                    else:
                                        editplan.AttendTimeOptimize =None
                                    if 'SKU1' in i.keys():
                                        editplan.SKU1 = i['SKU1'].upper
                                    if 'SKU2' in i.keys():
                                        editplan.SKU2 = i['SKU2'].upper
                                    if 'SKU3' in i.keys():
                                        editplan.SKU3 = i['SKU3'].upper
                                    if 'SKU4' in i.keys():
                                        editplan.SKU4 = i['SKU4'].upper
                                    if 'SKU5' in i.keys():
                                        editplan.SKU5 = i['SKU5'].upper
                                    if 'SKU6' in i.keys():
                                        editplan.SKU6 = i['SKU6'].upper
                                    if 'SKU7' in i.keys():
                                        editplan.SKU7 = i['SKU7'].upper
                                    if 'SKU8' in i.keys():
                                        editplan.SKU8 = i['SKU8'].upper
                                    if 'SKU9' in i.keys():
                                        editplan.SKU9 = i['SKU9'].upper
                                    if 'SKU10' in i.keys():
                                        editplan.SKU10 = i['SKU10'].upper
                                    if 'SKU11' in i.keys():
                                        editplan.SKU11 = i['SKU11'].upper
                                    if 'SKU12' in i.keys():
                                        editplan.SKU12 = i['SKU12'].upper
                                    if 'SKU13' in i.keys():
                                        editplan.SKU13 = i['SKU13'].upper
                                    if 'SKU14' in i.keys():
                                        editplan.SKU14 = i['SKU14'].upper
                                    if 'SKU15' in i.keys():
                                        editplan.SKU15 = i['SKU15'].upper
                                    if 'SKU16' in i.keys():
                                        editplan.SKU16 = i['SKU16'].upper
                                    if 'SKU17' in i.keys():
                                        editplan.SKU17 = i['SKU17'].upper
                                    if 'SKU18' in i.keys():
                                        editplan.SKU18 = i['SKU18'].upper
                                    if 'SKU19' in i.keys():
                                        editplan.SKU19 = i['SKU19'].upper
                                    if 'SKU20' in i.keys():
                                        editplan.SKU20 = i['SKU20'].upper
                                    if 'SKU21' in i.keys():
                                        editplan.SKU21 = i['SKU21'].upper
                                    if 'SKU22' in i.keys():
                                        editplan.SKU22 = i['SKU22'].upper
                                    if 'SKU23' in i.keys():
                                        editplan.SKU23 = i['SKU23'].upper
                                    if 'SKU24' in i.keys():
                                        editplan.SKU24 = i['SKU24'].upper
                                    if 'SKU25' in i.keys():
                                        editplan.SKU25 = i['SKU25'].upper
                                    if 'SKU26' in i.keys():
                                        editplan.SKU26 = i['SKU26'].upper
                                    if 'SKU27' in i.keys():
                                        editplan.SKU27 = i['SKU27'].upper
                                    if 'SKU28' in i.keys():
                                        editplan.SKU28 = i['SKU28'].upper
                                    if 'SKU29' in i.keys():
                                        editplan.SKU29 = i['SKU29'].upper
                                    if 'SKU30' in i.keys():
                                        editplan.SKU30 = i['SKU30'].upper
                                    if 'SKU31' in i.keys():
                                        editplan.SKU31 = i['SKU31'].upper
                                    if 'SKU32' in i.keys():
                                        editplan.SKU32 = i['SKU32'].upper
                                    if 'SKU33' in i.keys():
                                        editplan.SKU33 = i['SKU33'].upper
                                    if 'SKU34' in i.keys():
                                        editplan.SKU34 = i['SKU34'].upper
                                    if 'SKU35' in i.keys():
                                        editplan.SKU35 = i['SKU35'].upper
                                    if 'SKU36' in i.keys():
                                        editplan.SKU36 = i['SKU36'].upper
                                    if 'SKU37' in i.keys():
                                        editplan.SKU37 = i['SKU37'].upper
                                    if 'SKU38' in i.keys():
                                        editplan.SKU38 = i['SKU38'].upper
                                    if 'SKU39' in i.keys():
                                        editplan.SKU39 = i['SKU39'].upper
                                    if 'SKU40' in i.keys():
                                        editplan.SKU40 = i['SKU40'].upper
                                    if 'ConfigRetestCycle' in i.keys():
                                        if i['ConfigRetestCycle']:
                                            editplan.ConfigRetestCycle = float(i['ConfigRetestCycle'])
                                    else:
                                        editplan.ConfigRetestCycle =None
                                    if 'ConfigRetestSKU' in i.keys():
                                        if i['ConfigRetestSKU']:
                                            editplan.ConfigRetestSKU = float(i['ConfigRetestSKU'])
                                    else:
                                        editplan.ConfigRetestSKU = None
                                    if 'ConfigRetestTime' in i.keys():
                                        if i['ConfigRetestTime']:
                                            editplan.ConfigRetestTime = float(i['ConfigRetestTime'])
                                    else:
                                        editplan.ConfigRetestTime =None
                                    editplan.editor = request.session.get('user_name')
                                    editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    editplan.save()
                                #create
                                else:
                                    print('create on others category')
                                    updatedic={}
                                    # 由于需要转成float,所以即使excel中的key与models中的一样也不能用如下方式
                                    # for j in i.keys():
                                    #     updatedic[j]=i[j]
                                    updatedic['Project']=responseData['project']
                                    updatedic['Projectinfo']=TestProjectSW.objects.get(**dic_Project)
                                    updatedic['editor']=request.session.get('user_name')
                                    updatedic['edit_time']= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                                    updatedic["Customer"] = responseData['customer']
                                    updatedic["Phase"] = Phase
                                    updatedic["Project"] = responseData['project']
                                    updatedic["ItemNo_d"] = i['ItemNo_d']
                                    updatedic["Item_d"] = i['Item_d']
                                    #因为如上几项在other中是新增，并且可能重复存在，所以需要
                                    if 'TestItems' in i.keys():
                                        updatedic["TestItems"] = i['TestItems']
                                    if 'Category' in i.keys():
                                        updatedic["Category"] = i['Category']
                                    if 'Category2' in i.keys():
                                        updatedic["Category2"] = i['Category2']
                                    if 'Version' in i.keys():
                                        updatedic["Version"] = i['Version']
                                    if 'ReleaseDate' in i.keys():
                                        updatedic["ReleaseDate"] = i['ReleaseDate']
                                    if 'Owner' in i.keys():
                                        updatedic["Owner"] = i['Owner']
                                    if 'Priority' in i.keys():
                                        updatedic["Priority"] = i['Priority']
                                    if 'TDMSsTotalTime' in i.keys():
                                        if i['TDMSTotalTime']:
                                            updatedic["TDMSTotalTime"] = float(i['TDMSTotalTime'])
                                    else:
                                        updatedic["TDMSTotalTime"] = None
                                    # if 'BaseTime' in i.keys():
                                    #     if i['BaseTime']:
                                    #         updatedic["BaseTime"] = float(i['BaseTime'])
                                    # else:
                                    #     updatedic["BaseTime"] =None
                                    if 'BaseTime' in i.keys():
                                        # print(i['BaseTime'])
                                        if i['BaseTime']:
                                            updatedic["BaseTime"] = float(i['BaseTime'])
                                        else:
                                            updatedic["BaseTime"] = 0
                                    else:
                                        updatedic["BaseTime"] = 0
                                    if 'TDMSUnattendedTime' in i.keys():
                                        if i['TDMSUnattendedTime']:
                                            updatedic["TDMSUnattendedTime"] = float(i['TDMSUnattendedTime'])
                                    else:
                                        updatedic["TDMSUnattendedTime"] =None
                                    if 'BaseAotomationTime1SKU' in i.keys():
                                        if i['BaseAotomationTime1SKU']:
                                            updatedic["BaseAotomationTime1SKU"] = float(i['BaseAotomationTime1SKU'])
                                    else:
                                        updatedic["BaseAotomationTime1SKU"] = None
                                    if 'Chramshell' in i.keys():
                                        updatedic["Chramshell"] = i['Chramshell']
                                    if 'ConvertibaleNBMode' in i.keys():
                                        updatedic["ConvertibaleNBMode"] = i['ConvertibaleNBMode']
                                    if 'ConvertibaleYogaPadMode' in i.keys():
                                        updatedic["ConvertibaleYogaPadMode"] = i['ConvertibaleYogaPadMode']
                                    if 'DetachablePadMode' in i.keys():
                                        updatedic["DetachablePadMode"] = i['DetachablePadMode']
                                    if 'DetachableWDockmode' in i.keys():
                                        updatedic["DetachableWDockmode"] = i['DetachableWDockmode']
                                    if 'PhaseFVT' in i.keys():
                                        updatedic["PhaseFVT"] = i['PhaseFVT']
                                    if 'PhaseSIT' in i.keys():
                                        updatedic["PhaseSIT"] = i['PhaseSIT']
                                    if 'PhaseFFRT' in i.keys():
                                        updatedic["PhaseFFRT"] = i['PhaseFFRT']
                                    if 'Coverage' in i.keys():
                                        updatedic["Coverage"] = i['Coverage']

                                    if 'FeatureSupport' in i.keys():
                                        updatedic["FeatureSupport"] = i['FeatureSupport']
                                    if 'BaseTimeSupport' in i.keys():
                                        if i['BaseTimeSupport']:
                                            updatedic["BaseTimeSupport"] = float(i['BaseTimeSupport'])
                                    else:
                                        updatedic["BaseTimeSupport"] = None
                                    if 'TE' in i.keys():
                                        updatedic["TE"] = i['TE']
                                    if 'Schedule' in i.keys():
                                        updatedic["Schedule"] = i['Schedule']
                                    if 'ProjectTestSKUfollowMatrix' in i.keys():
                                        if i['ProjectTestSKUfollowMatrix']:
                                            updatedic["ProjectTestSKUfollowMatrix"] = float(i['ProjectTestSKUfollowMatrix'])
                                    else:
                                        updatedic["ProjectTestSKUfollowMatrix"] =None
                                    if 'TimewConfigFollowmatrix' in i.keys():
                                        if i['TimewConfigFollowmatrix']:
                                            updatedic["TimewConfigFollowmatrix"] = float(i['TimewConfigFollowmatrix'])
                                    else:
                                        updatedic["TimewConfigFollowmatrix"] = None
                                    if 'ConfigAutomationItem' in i.keys():
                                        updatedic["ConfigAutomationItem"] = i['ConfigAutomationItem']
                                    if 'ConfigAutomationTime' in i.keys():
                                        if i['ConfigAutomationTime']:
                                            updatedic["ConfigAutomationTime"] = float(i['ConfigAutomationTime'])
                                    else:
                                        updatedic["ConfigAutomationTime"] = None
                                    if 'ConfigLeverageItem' in i.keys():
                                        updatedic["ConfigLeverageItem"] = i['ConfigLeverageItem']
                                    if 'ConfigLeverageTime' in i.keys():
                                        if i['ConfigLeverageTime']:
                                            updatedic["ConfigLeverageTime"] = float(i['ConfigLeverageTime'])
                                    else:
                                        updatedic["ConfigLeverageTime"] =None
                                    if 'CommentsLeverage' in i.keys():
                                        updatedic["CommentsLeverage"] = i['CommentsLeverage']
                                    if 'ConfigSmartItem' in i.keys():
                                        updatedic["ConfigSmartItem"] = i['ConfigSmartItem']
                                    if 'ConfigSmartItemPer' in i.keys():
                                        if i['ConfigSmartItemPer']:
                                            updatedic["ConfigSmartItemPer"] = float(i['ConfigSmartItemPer'])
                                    else:
                                        updatedic["ConfigSmartItemPer"] =None
                                    if 'ConfigSmartTime' in i.keys():
                                        if i['ConfigSmartTime']:
                                            updatedic["ConfigSmartTime"] = float(i['ConfigSmartTime'])
                                    else:
                                        updatedic["ConfigSmartTime"] =None
                                    if 'CommentsSmart' in i.keys():
                                        updatedic["CommentsSmart"] = i['CommentsSmart']
                                    if 'ProjectTestSKUOptimize' in i.keys():
                                        if i['ProjectTestSKUOptimize']:
                                            updatedic["ProjectTestSKUOptimize"] = float(i['ProjectTestSKUOptimize'])
                                    else:
                                        updatedic["ProjectTestSKUOptimize"] =None
                                    if 'AttendTimeOptimize' in i.keys():
                                        # print(i['AttendTimeOptimize'],type(i['AttendTimeOptimize']))
                                        #print出来是int型，excel中是文字格式
                                        if i['AttendTimeOptimize']:
                                            updatedic["AttendTimeOptimize"] = i['AttendTimeOptimize']#float(i['AttendTimeOptimize'])
                                            # print(type(updatedic["AttendTimeOptimize"]，type(i['AttendTimeOptimize']))
                                    else:
                                        updatedic["AttendTimeOptimize"] =None
                                    if 'SKU1' in i.keys():
                                        updatedic["SKU1"] = i['SKU1']
                                    if 'SKU2' in i.keys():
                                        updatedic["SKU2"] = i['SKU2']
                                    if 'SKU3' in i.keys():
                                        updatedic["SKU3"] = i['SKU3']
                                    if 'SKU4' in i.keys():
                                        updatedic["SKU4"] = i['SKU4']
                                    if 'SKU5' in i.keys():
                                        updatedic["SKU5"] = i['SKU5']
                                    if 'SKU6' in i.keys():
                                        updatedic["SKU6"] = i['SKU6']
                                    if 'SKU7' in i.keys():
                                        updatedic["SKU7"] = i['SKU7']
                                    if 'SKU8' in i.keys():
                                        updatedic["SKU8"] = i['SKU8']
                                    if 'SKU9' in i.keys():
                                        updatedic["SKU9"] = i['SKU9']
                                    if 'SKU10' in i.keys():
                                        updatedic["SKU10"] = i['SKU10']
                                    if 'SKU11' in i.keys():
                                        updatedic["SKU11"] = i['SKU11']
                                    if 'SKU12' in i.keys():
                                        updatedic["SKU12"] = i['SKU12']
                                    if 'SKU13' in i.keys():
                                        updatedic["SKU13"] = i['SKU13']
                                    if 'SKU14' in i.keys():
                                        updatedic["SKU14"] = i['SKU14']
                                    if 'SKU15' in i.keys():
                                        updatedic["SKU15"] = i['SKU15']
                                    if 'SKU16' in i.keys():
                                        updatedic["SKU16"] = i['SKU16']
                                    if 'SKU17' in i.keys():
                                        updatedic["SKU17"] = i['SKU17']
                                    if 'SKU18' in i.keys():
                                        updatedic["SKU18"] = i['SKU18']
                                    if 'SKU19' in i.keys():
                                        updatedic["SKU19"] = i['SKU19']
                                    if 'SKU20' in i.keys():
                                        updatedic["SKU20"] = i['SKU20']
                                    if 'SKU21' in i.keys():
                                        updatedic["SKU21"] = i['SKU21']
                                    if 'SKU22' in i.keys():
                                        updatedic["SKU22"] = i['SKU22']
                                    if 'SKU23' in i.keys():
                                        updatedic["SKU23"] = i['SKU23']
                                    if 'SKU24' in i.keys():
                                        updatedic["SKU24"] = i['SKU24']
                                    if 'SKU25' in i.keys():
                                        updatedic["SKU25"] = i['SKU25']
                                    if 'SKU26' in i.keys():
                                        updatedic["SKU26"] = i['SKU26']
                                    if 'SKU27' in i.keys():
                                        updatedic["SKU27"] = i['SKU27']
                                    if 'SKU28' in i.keys():
                                        updatedic["SKU28"] = i['SKU28']
                                    if 'SKU29' in i.keys():
                                        updatedic["SKU29"] = i['SKU29']
                                    if 'SKU30' in i.keys():
                                        updatedic["SKU30"] = i['SKU30']
                                    if 'SKU31' in i.keys():
                                        updatedic["SKU31"] = i['SKU31']
                                    if 'SKU32' in i.keys():
                                        updatedic["SKU32"] = i['SKU32']
                                    if 'SKU33' in i.keys():
                                        updatedic["SKU33"] = i['SKU33']
                                    if 'SKU34' in i.keys():
                                        updatedic["SKU34"] = i['SKU34']
                                    if 'SKU35' in i.keys():
                                        updatedic["SKU35"] = i['SKU35']
                                    if 'SKU36' in i.keys():
                                        updatedic["SKU36"] = i['SKU36']
                                    if 'SKU37' in i.keys():
                                        updatedic["SKU37"] = i['SKU37']
                                    if 'SKU38' in i.keys():
                                        updatedic["SKU38"] = i['SKU38']
                                    if 'SKU39' in i.keys():
                                        updatedic["SKU39"] = i['SKU39']
                                    if 'SKU40' in i.keys():
                                        updatedic["SKU40"] = i['SKU40']
                                    if 'ConfigRetestCycle' in i.keys():
                                        if i['ConfigRetestCycle']:
                                            updatedic["ConfigRetestCycle"] = float(i['ConfigRetestCycle'])
                                    else:
                                        updatedic["ConfigRetestCycle"] =None
                                    if 'ConfigRetestSKU' in i.keys():
                                        if i['ConfigRetestSKU']:
                                            updatedic["ConfigRetestSKU"] = float(i['ConfigRetestSKU'])
                                    else:
                                        updatedic["ConfigRetestSKU"] = None
                                    if 'ConfigRetestTime' in i.keys():
                                        if i['ConfigRetestTime']:
                                            updatedic["ConfigRetestTime"] = float(i['ConfigRetestTime'])
                                    else:
                                        updatedic["ConfigRetestTime"] =None


                                    # print(updatedic)
                                    # for m in updatedic:
                                    #     print (m,type(updatedic[m]))
                                    RetestItemSW.objects.create(**updatedic)
                            else:
                                print("Case_ID&Case_Name&Test_Items can't be null")
                        #Others
                        else:#存到TestPlan表里，需要link TestItem
                            # print("normal category")
                            # print ('others')

                            # print("normal category")
                            # print ('others')
                            if 'TestItems' in i.keys():#FFRT的Testcase,GSKU
                                if "Phase_Case" in i.keys():
                                    check_dic = {'Customer': responseData['customer'], 'Phase': i['Phase_Case'],
                                                 'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],
                                                 'TestItems': i['TestItems']}
                                else:#没有Phase_Case这一列，也就是除了B，C，FFRT其他都不做link
                                    check_dic = {'Customer': responseData['customer'],'Phase': Phase,
                                                 'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],
                                                 'TestItems': i['TestItems']}
                                check_dic_inplan = {'Customer': responseData['customer'], 'Phase': Phase,
                                                    'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],
                                                    'TestItems': i['TestItems']}
                            else:#B或C的Testcase
                                if "Phase_Case" in i.keys():
                                    check_dic = {'Customer': responseData['customer'], 'Phase': i['Phase_Case'],
                                                'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                                else:#没有Phase_Case这一列，也就是除了B，C，FFRT其他都不做link
                                    check_dic = {'Customer': responseData['customer'],  'Phase': Phase,
                                                'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                                check_dic_inplan = {'Customer': responseData['customer'], 'Phase': Phase,
                                                    'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                            # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                            # print(check_dic)
                            check_list = TestItemSW.objects.filter(**check_dic).first()
                            check_dic_inplan["Projectinfo"] = Projectinfos
                            check_list_plan = TestPlanSW.objects.filter(**check_dic_inplan).first()
                            # print(check_list)

                            if check_list_plan:  # 其实跟editplan是一样的，这时不能去比较Items的信息（不是Id获取），因为TestItems表里的都是最新的信息，而TestPlan表里的是测试当下的case信息

                                editplan = TestPlanSW.objects.filter(**check_dic_inplan).first()
                                if editplan:
                                    # if editplan.ItemNo_d == "BFA001_01":
                                    #     print(editplan,editplan.BaseTime,i['BaseTime'],i)
                                    # 这几项是搜索条件中的一部分，如果不一样压根就搜不到。
                                    # editplan.Customer = responseData['customer']
                                    # editplan.Phase = Phase
                                    # editplan.Project = responseData['project']
                                    # editplan.ItemNo_d = i['ItemNo_d']
                                    # editplan.Item_d = i['Item_d']
                                    # if 'TestItems' in i.keys():
                                    #     editplan.TestItems = i['TestItems']
                                    if 'Category' in i.keys():
                                        editplan.Category = i['Category']
                                    if 'Category2' in i.keys():
                                        editplan.Category2 = i['Category2']
                                    if 'Version' in i.keys():
                                        editplan.Version = i['Version']
                                    if 'ReleaseDate' in i.keys():
                                        editplan.ReleaseDate = i['ReleaseDate']
                                    if 'Owner' in i.keys():
                                        editplan.Owner = i['Owner']
                                    if 'Priority' in i.keys():
                                        editplan.Priority = i['Priority']
                                    if 'TDMSTotalTime' in i.keys():
                                        if i['TDMSTotalTime']:
                                            editplan.TDMSTotalTime = float(i['TDMSTotalTime'])
                                        else:
                                            editplan.TDMSTotalTime = 0
                                    else:
                                        editplan.TDMSTotalTime = None
                                    if 'BaseTime' in i.keys():
                                        # print(i['BaseTime'])
                                        if i['BaseTime']:
                                            editplan.BaseTime = float(i['BaseTime'])
                                        else:
                                            editplan.BaseTime = 0
                                    else:
                                        editplan.BaseTime = 0
                                    if 'TDMSUnattendedTime' in i.keys():
                                        if i['TDMSUnattendedTime']:
                                            editplan.TDMSUnattendedTime = float(i['TDMSUnattendedTime'])
                                        else:
                                            editplan.TDMSUnattendedTime = 0
                                    else:
                                        editplan.TDMSUnattendedTime = None
                                    if 'BaseAotomationTime1SKU' in i.keys():
                                        if i['BaseAotomationTime1SKU']:
                                            # print(i['BaseAotomationTime1SKU'])
                                            editplan.BaseAotomationTime1SKU = float(i['BaseAotomationTime1SKU'])
                                        else:
                                            editplan.BaseAotomationTime1SKU = 0
                                    else:
                                        editplan.BaseAotomationTime1SKU = None
                                    if 'Chramshell' in i.keys():
                                        editplan.Chramshell = i['Chramshell']
                                    if 'ConvertibaleNBMode' in i.keys():
                                        editplan.ConvertibaleNBMode = i['ConvertibaleNBMode']
                                    if 'ConvertibaleYogaPadMode' in i.keys():
                                        editplan.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                                    if 'DetachablePadMode' in i.keys():
                                        editplan.DetachablePadMode = i['DetachablePadMode']
                                    if 'DetachableWDockmode' in i.keys():
                                        editplan.DetachableWDockmode = i['DetachableWDockmode']
                                    if 'PhaseFVT' in i.keys():
                                        editplan.PhaseFVT = i['PhaseFVT']
                                    if 'PhaseSIT' in i.keys():
                                        editplan.PhaseSIT = i['PhaseSIT']
                                    if 'PhaseFFRT' in i.keys():
                                        editplan.PhaseFFRT = i['PhaseFFRT']
                                    if 'Coverage' in i.keys():
                                        editplan.Coverage = i['Coverage']

                                    if 'FeatureSupport' in i.keys():
                                        editplan.FeatureSupport = i['FeatureSupport']
                                    if 'BaseTimeSupport' in i.keys():
                                        if i['BaseTimeSupport']:
                                            editplan.BaseTimeSupport = float(i['BaseTimeSupport'])
                                    else:
                                        editplan.BaseTimeSupport = None
                                    if 'TE' in i.keys():
                                        editplan.TE = i['TE']
                                    if 'Schedule' in i.keys():
                                        editplan.Schedule = i['Schedule']
                                    if 'ProjectTestSKUfollowMatrix' in i.keys():
                                        if i['ProjectTestSKUfollowMatrix']:
                                            editplan.ProjectTestSKUfollowMatrix = float(
                                                i['ProjectTestSKUfollowMatrix'])
                                    else:
                                        editplan.ProjectTestSKUfollowMatrix = None
                                    if 'TimewConfigFollowmatrix' in i.keys():
                                        if i['TimewConfigFollowmatrix']:
                                            editplan.TimewConfigFollowmatrix = float(i['TimewConfigFollowmatrix'])
                                    else:
                                        editplan.TimewConfigFollowmatrix = None
                                    if 'ConfigAutomationItem' in i.keys():
                                        editplan.ConfigAutomationItem = i['ConfigAutomationItem']
                                    if 'ConfigAutomationTime' in i.keys():
                                        if i['ConfigAutomationTime']:
                                            editplan.ConfigAutomationTime = float(i['ConfigAutomationTime'])
                                    else:
                                        editplan.ConfigAutomationTime = None
                                    if 'ConfigLeverageItem' in i.keys():
                                        editplan.ConfigLeverageItem = i['ConfigLeverageItem']
                                    if 'ConfigLeverageTime' in i.keys():
                                        if i['ConfigLeverageTime']:
                                            editplan.ConfigLeverageTime = float(i['ConfigLeverageTime'])
                                    else:
                                        editplan.ConfigLeverageTime = None
                                    if 'CommentsLeverage' in i.keys():
                                        editplan.CommentsLeverage = i['CommentsLeverage']
                                    if 'ConfigSmartItem' in i.keys():
                                        editplan.ConfigSmartItem = i['ConfigSmartItem']
                                    if 'ConfigSmartItemPer' in i.keys():
                                        if i['ConfigSmartItemPer']:
                                            editplan.ConfigSmartItemPer = float(i['ConfigSmartItemPer'])
                                    else:
                                        editplan.ConfigSmartItemPer = None
                                    if 'ConfigSmartTime' in i.keys():
                                        if i['ConfigSmartTime']:
                                            editplan.ConfigSmartTime = float(i['ConfigSmartTime'])
                                    else:
                                        editplan.ConfigSmartTime = None
                                    if 'CommentsSmart' in i.keys():
                                        editplan.CommentsSmart = i['CommentsSmart']
                                    if 'ProjectTestSKUOptimize' in i.keys():
                                        if i['ProjectTestSKUOptimize']:
                                            editplan.ProjectTestSKUOptimize = float(i['ProjectTestSKUOptimize'])
                                    else:
                                        editplan.ProjectTestSKUOptimize = None
                                    if 'AttendTimeOptimize' in i.keys():
                                        if i['AttendTimeOptimize']:
                                            editplan.AttendTimeOptimize = float(i['AttendTimeOptimize'])
                                    else:
                                        editplan.AttendTimeOptimize = None
                                    if 'SKU1' in i.keys():
                                        editplan.SKU1 = i['SKU1']
                                    if 'SKU2' in i.keys():
                                        # print(i['SKU2'])
                                        editplan.SKU2 = i['SKU2']
                                    if 'SKU3' in i.keys():
                                        editplan.SKU3 = i['SKU3']
                                    if 'SKU4' in i.keys():
                                        editplan.SKU4 = i['SKU4']
                                    if 'SKU5' in i.keys():
                                        editplan.SKU5 = i['SKU5']
                                    if 'SKU6' in i.keys():
                                        editplan.SKU6 = i['SKU6']
                                    if 'SKU7' in i.keys():
                                        editplan.SKU7 = i['SKU7']
                                    if 'SKU8' in i.keys():
                                        editplan.SKU8 = i['SKU8']
                                    if 'SKU9' in i.keys():
                                        editplan.SKU9 = i['SKU9']
                                    if 'SKU10' in i.keys():
                                        editplan.SKU10 = i['SKU10']
                                    if 'SKU11' in i.keys():
                                        editplan.SKU11 = i['SKU11']
                                    if 'SKU12' in i.keys():
                                        editplan.SKU12 = i['SKU12']
                                    if 'SKU13' in i.keys():
                                        editplan.SKU13 = i['SKU13']
                                    if 'SKU14' in i.keys():
                                        editplan.SKU14 = i['SKU14']
                                    if 'SKU15' in i.keys():
                                        editplan.SKU15 = i['SKU15']
                                    if 'SKU16' in i.keys():
                                        editplan.SKU16 = i['SKU16']
                                    if 'SKU17' in i.keys():
                                        editplan.SKU17 = i['SKU17']
                                    if 'SKU18' in i.keys():
                                        editplan.SKU18 = i['SKU18']
                                    if 'SKU19' in i.keys():
                                        editplan.SKU19 = i['SKU19']
                                    if 'SKU20' in i.keys():
                                        editplan.SKU20 = i['SKU20']
                                    if 'SKU21' in i.keys():
                                        editplan.SKU21 = i['SKU21']
                                    if 'SKU22' in i.keys():
                                        # print(i['SKU22'])
                                        editplan.SKU22 = i['SKU22']
                                    if 'SKU23' in i.keys():
                                        editplan.SKU23 = i['SKU23']
                                    if 'SKU24' in i.keys():
                                        editplan.SKU24 = i['SKU24']
                                    if 'SKU25' in i.keys():
                                        editplan.SKU25 = i['SKU25']
                                    if 'SKU26' in i.keys():
                                        editplan.SKU26 = i['SKU26']
                                    if 'SKU27' in i.keys():
                                        editplan.SKU27 = i['SKU27']
                                    if 'SKU28' in i.keys():
                                        editplan.SKU28 = i['SKU28']
                                    if 'SKU29' in i.keys():
                                        editplan.SKU29 = i['SKU29']
                                    if 'SKU30' in i.keys():
                                        editplan.SKU30 = i['SKU30']
                                    if 'SKU31' in i.keys():
                                        editplan.SKU31 = i['SKU31']
                                    if 'SKU32' in i.keys():
                                        editplan.SKU32 = i['SKU32']
                                    if 'SKU33' in i.keys():
                                        editplan.SKU33 = i['SKU33']
                                    if 'SKU34' in i.keys():
                                        editplan.SKU34 = i['SKU34']
                                    if 'SKU35' in i.keys():
                                        editplan.SKU35 = i['SKU35']
                                    if 'SKU36' in i.keys():
                                        editplan.SKU36 = i['SKU36']
                                    if 'SKU37' in i.keys():
                                        editplan.SKU37 = i['SKU37']
                                    if 'SKU38' in i.keys():
                                        editplan.SKU38 = i['SKU38']
                                    if 'SKU39' in i.keys():
                                        editplan.SKU39 = i['SKU39']
                                    if 'SKU40' in i.keys():
                                        editplan.SKU40 = i['SKU40']
                                    if 'ConfigRetestCycle' in i.keys():
                                        if i['ConfigRetestCycle']:
                                            editplan.ConfigRetestCycle = float(i['ConfigRetestCycle'])
                                    else:
                                        editplan.ConfigRetestCycle = None
                                    if 'ConfigRetestSKU' in i.keys():
                                        if i['ConfigRetestSKU']:
                                            editplan.ConfigRetestSKU = float(i['ConfigRetestSKU'])
                                    else:
                                        editplan.ConfigRetestSKU = None
                                    if 'ConfigRetestTime' in i.keys():
                                        if i['ConfigRetestTime']:
                                            editplan.ConfigRetestTime = float(i['ConfigRetestTime'])
                                    else:
                                        editplan.ConfigRetestTime = None
                                    editplan.editor = request.session.get('user_name')
                                    editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    editplan.save()
                            else:#create

                                # print(itemsinfo)
                                updatedic = {}
                                # 由于需要转成float,所以即使excel中的key与models中的一样也不能用如下方式
                                # for j in i.keys():
                                #     updatedic[j]=i[j]
                                # updatedic['Project'] = responseData['project']
                                # print(dic_Project)
                                updatedic['Projectinfo'] = TestProjectSW.objects.get(**dic_Project)
                                if check_list:  # 文档中的测项check_dic不存在于TestPlanSW中的某一个或几个机种中，但是存在于TestItemSW中，说明测试当下的case信息就是最新的case，则创建并linkTestItem表,否则只创建但是不linkTest Item表。
                                    itemsinfo = TestItemSW.objects.get(id=check_list.id)
                                    updatedic['Items'] = itemsinfo
                                updatedic['editor'] = request.session.get('user_name')
                                updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                updatedic["Customer"] = responseData['customer']
                                updatedic["Phase"] = Phase
                                # updatedic["Project"] = responseData['project']#TestPlan中没有这个key，只有Projectinfo，RetestItem里面才有
                                updatedic["ItemNo_d"] = i['ItemNo_d']
                                updatedic["Item_d"] = i['Item_d']
                                # 因为如上几项在other中是新增，并且可能重复存在，所以需要
                                if 'TestItems' in i.keys():
                                    updatedic["TestItems"] = i['TestItems']
                                if 'Category' in i.keys():
                                    updatedic["Category"] = i['Category']
                                if 'Category2' in i.keys():
                                    updatedic["Category2"] = i['Category2']
                                if 'Version' in i.keys():
                                    updatedic["Version"] = i['Version']
                                if 'ReleaseDate' in i.keys():
                                    updatedic["ReleaseDate"] = i['ReleaseDate']
                                if 'Owner' in i.keys():
                                    updatedic["Owner"] = i['Owner']
                                if 'Priority' in i.keys():
                                    updatedic["Priority"] = i['Priority']
                                if 'TDMSsTotalTime' in i.keys():
                                    if i['TDMSTotalTime'] and not i['TDMSTotalTime'] == " ":
                                        updatedic["TDMSTotalTime"] = float(i['TDMSTotalTime'])
                                else:
                                    updatedic["TDMSTotalTime"] = None
                                # if 'BaseTime' in i.keys():
                                #     if i['BaseTime'] and not i['BaseTime'] == " ":
                                #         updatedic["BaseTime"] = float(i['BaseTime'])
                                # else:
                                #     updatedic["BaseTime"] = None
                                if 'BaseTime' in i.keys():
                                    # print(i['BaseTime'])
                                    if i['BaseTime']:
                                        updatedic['BaseTime'] = float(i['BaseTime'])
                                    else:
                                        updatedic['BaseTime'] = 0
                                else:
                                    updatedic['BaseTime'] = 0

                                if 'TDMSUnattendedTime' in i.keys():
                                    if i['TDMSUnattendedTime'] and not i['TDMSUnattendedTime'] == " ":
                                        updatedic["TDMSUnattendedTime"] = float(i['TDMSUnattendedTime'])
                                else:
                                    updatedic["TDMSUnattendedTime"] = None
                                if 'BaseAotomationTime1SKU' in i.keys():
                                    if i['BaseAotomationTime1SKU'] and not i['BaseAotomationTime1SKU'] == " ":
                                        updatedic["BaseAotomationTime1SKU"] = float(i['BaseAotomationTime1SKU'])
                                else:
                                    updatedic["BaseAotomationTime1SKU"] = None
                                if 'Chramshell' in i.keys():
                                    updatedic["Chramshell"] = i['Chramshell']
                                if 'ConvertibaleNBMode' in i.keys():
                                    updatedic["ConvertibaleNBMode"] = i['ConvertibaleNBMode']
                                if 'ConvertibaleYogaPadMode' in i.keys():
                                    updatedic["ConvertibaleYogaPadMode"] = i['ConvertibaleYogaPadMode']
                                if 'DetachablePadMode' in i.keys():
                                    updatedic["DetachablePadMode"] = i['DetachablePadMode']
                                if 'DetachableWDockmode' in i.keys():
                                    updatedic["DetachableWDockmode"] = i['DetachableWDockmode']
                                if 'PhaseFVT' in i.keys():
                                    updatedic["PhaseFVT"] = i['PhaseFVT']
                                if 'PhaseSIT' in i.keys():
                                    updatedic["PhaseSIT"] = i['PhaseSIT']
                                if 'PhaseFFRT' in i.keys():
                                    updatedic["PhaseFFRT"] = i['PhaseFFRT']
                                if 'Coverage' in i.keys():
                                    updatedic["Coverage"] = i['Coverage']

                                if 'FeatureSupport' in i.keys():
                                    updatedic["FeatureSupport"] = i['FeatureSupport']
                                if 'BaseTimeSupport' in i.keys():
                                    if i['BaseTimeSupport'] and not i['BaseTimeSupport'] == " ":
                                        updatedic["BaseTimeSupport"] = float(i['BaseTimeSupport'])
                                else:
                                    updatedic["BaseTimeSupport"] = None
                                if 'TE' in i.keys():
                                    updatedic["TE"] = i['TE']
                                if 'Schedule' in i.keys():
                                    updatedic["Schedule"] = i['Schedule']
                                if 'ProjectTestSKUfollowMatrix' in i.keys():
                                    if i['ProjectTestSKUfollowMatrix'] and not i['ProjectTestSKUfollowMatrix'] == " ":
                                        updatedic["ProjectTestSKUfollowMatrix"] = float(
                                            i['ProjectTestSKUfollowMatrix'])
                                else:
                                    updatedic["ProjectTestSKUfollowMatrix"] = None
                                if 'TimewConfigFollowmatrix' in i.keys():
                                    if i['TimewConfigFollowmatrix'] and not i['TimewConfigFollowmatrix'] == " ":
                                        updatedic["TimewConfigFollowmatrix"] = float(i['TimewConfigFollowmatrix'])
                                else:
                                    updatedic["TimewConfigFollowmatrix"] = None
                                if 'ConfigAutomationItem' in i.keys():
                                    updatedic["ConfigAutomationItem"] = i['ConfigAutomationItem']
                                if 'ConfigAutomationTime' in i.keys():
                                    if i['ConfigAutomationTime'] and not i['ConfigAutomationTime'] == " ":
                                        updatedic["ConfigAutomationTime"] = float(i['ConfigAutomationTime'])
                                else:
                                    updatedic["ConfigAutomationTime"] = None
                                if 'ConfigLeverageItem' in i.keys():
                                    updatedic["ConfigLeverageItem"] = i['ConfigLeverageItem']
                                if 'ConfigLeverageTime' in i.keys():
                                    if i['ConfigLeverageTime'] and not i['ConfigLeverageTime'] == " ":
                                        updatedic["ConfigLeverageTime"] = float(i['ConfigLeverageTime'])
                                else:
                                    updatedic["ConfigLeverageTime"] = None
                                if 'CommentsLeverage' in i.keys():
                                    updatedic["CommentsLeverage"] = i['CommentsLeverage']
                                if 'ConfigSmartItem' in i.keys():
                                    updatedic["ConfigSmartItem"] = i['ConfigSmartItem']
                                if 'ConfigSmartItemPer' in i.keys():
                                    if i['ConfigSmartItemPer'] and not i['ConfigSmartItemPer'] == " ":
                                        updatedic["ConfigSmartItemPer"] = float(i['ConfigSmartItemPer'])
                                else:
                                    updatedic["ConfigSmartItemPer"] = None
                                if 'ConfigSmartTime' in i.keys():
                                    if i['ConfigSmartTime'] and not i['ConfigSmartTime'] == " ":
                                        updatedic["ConfigSmartTime"] = float(i['ConfigSmartTime'])
                                else:
                                    updatedic["ConfigSmartTime"] = None
                                if 'CommentsSmart' in i.keys():
                                    updatedic["CommentsSmart"] = i['CommentsSmart']
                                if 'ProjectTestSKUOptimize' in i.keys():
                                    if i['ProjectTestSKUOptimize'] and not i['ProjectTestSKUOptimize'] == " ":
                                        updatedic["ProjectTestSKUOptimize"] = float(i['ProjectTestSKUOptimize'])
                                else:
                                    updatedic["ProjectTestSKUOptimize"] = None
                                if 'AttendTimeOptimize' in i.keys():
                                    # print(i['AttendTimeOptimize'],type(i['AttendTimeOptimize']))
                                    # print出来是int型，excel中是文字格式
                                    if i['AttendTimeOptimize']:
                                        updatedic["AttendTimeOptimize"] = i[
                                            'AttendTimeOptimize']  # float(i['AttendTimeOptimize'])
                                        # print(type(updatedic["AttendTimeOptimize"]，type(i['AttendTimeOptimize']))
                                else:
                                    updatedic["AttendTimeOptimize"] = None
                                if 'SKU1' in i.keys():
                                    updatedic["SKU1"] = i['SKU1']
                                if 'SKU2' in i.keys():
                                    updatedic["SKU2"] = i['SKU2']
                                if 'SKU3' in i.keys():
                                    updatedic["SKU3"] = i['SKU3']
                                if 'SKU4' in i.keys():
                                    updatedic["SKU4"] = i['SKU4']
                                if 'SKU5' in i.keys():
                                    updatedic["SKU5"] = i['SKU5']
                                if 'SKU6' in i.keys():
                                    updatedic["SKU6"] = i['SKU6']
                                if 'SKU7' in i.keys():
                                    updatedic["SKU7"] = i['SKU7']
                                if 'SKU8' in i.keys():
                                    updatedic["SKU8"] = i['SKU8']
                                if 'SKU9' in i.keys():
                                    updatedic["SKU9"] = i['SKU9']
                                if 'SKU10' in i.keys():
                                    updatedic["SKU10"] = i['SKU10']
                                if 'SKU11' in i.keys():
                                    updatedic["SKU11"] = i['SKU11']
                                if 'SKU12' in i.keys():
                                    updatedic["SKU12"] = i['SKU12']
                                if 'SKU13' in i.keys():
                                    updatedic["SKU13"] = i['SKU13']
                                if 'SKU14' in i.keys():
                                    updatedic["SKU14"] = i['SKU14']
                                if 'SKU15' in i.keys():
                                    updatedic["SKU15"] = i['SKU15']
                                if 'SKU16' in i.keys():
                                    updatedic["SKU16"] = i['SKU16']
                                if 'SKU17' in i.keys():
                                    updatedic["SKU17"] = i['SKU17']
                                if 'SKU18' in i.keys():
                                    updatedic["SKU18"] = i['SKU18']
                                if 'SKU19' in i.keys():
                                    updatedic["SKU19"] = i['SKU19']
                                if 'SKU20' in i.keys():
                                    updatedic["SKU20"] = i['SKU20']
                                if 'SKU21' in i.keys():
                                    updatedic["SKU21"] = i['SKU21']
                                if 'SKU22' in i.keys():
                                    updatedic["SKU22"] = i['SKU22']
                                if 'SKU23' in i.keys():
                                    updatedic["SKU23"] = i['SKU23']
                                if 'SKU24' in i.keys():
                                    updatedic["SKU24"] = i['SKU24']
                                if 'SKU25' in i.keys():
                                    updatedic["SKU25"] = i['SKU25']
                                if 'SKU26' in i.keys():
                                    updatedic["SKU26"] = i['SKU26']
                                if 'SKU27' in i.keys():
                                    updatedic["SKU27"] = i['SKU27']
                                if 'SKU28' in i.keys():
                                    updatedic["SKU28"] = i['SKU28']
                                if 'SKU29' in i.keys():
                                    updatedic["SKU29"] = i['SKU29']
                                if 'SKU30' in i.keys():
                                    updatedic["SKU30"] = i['SKU30']
                                if 'SKU31' in i.keys():
                                    updatedic["SKU31"] = i['SKU31']
                                if 'SKU32' in i.keys():
                                    updatedic["SKU32"] = i['SKU32']
                                if 'SKU33' in i.keys():
                                    updatedic["SKU33"] = i['SKU33']
                                if 'SKU34' in i.keys():
                                    updatedic["SKU34"] = i['SKU34']
                                if 'SKU35' in i.keys():
                                    updatedic["SKU35"] = i['SKU35']
                                if 'SKU36' in i.keys():
                                    updatedic["SKU36"] = i['SKU36']
                                if 'SKU37' in i.keys():
                                    updatedic["SKU37"] = i['SKU37']
                                if 'SKU38' in i.keys():
                                    updatedic["SKU38"] = i['SKU38']
                                if 'SKU39' in i.keys():
                                    updatedic["SKU39"] = i['SKU39']
                                if 'SKU40' in i.keys():
                                    updatedic["SKU40"] = i['SKU40']
                                if 'ConfigRetestCycle' in i.keys():
                                    if i['ConfigRetestCycle']:
                                        updatedic["ConfigRetestCycle"] = float(i['ConfigRetestCycle'])
                                else:
                                    updatedic["ConfigRetestCycle"] = None
                                if 'ConfigRetestSKU' in i.keys():
                                    if i['ConfigRetestSKU']:
                                        updatedic["ConfigRetestSKU"] = float(i['ConfigRetestSKU'])
                                else:
                                    updatedic["ConfigRetestSKU"] = None
                                if 'ConfigRetestTime' in i.keys():
                                    if i['ConfigRetestTime']:
                                        updatedic["ConfigRetestTime"] = float(i['ConfigRetestTime'])
                                else:
                                    updatedic["ConfigRetestTime"] = None

                                # print(updatedic)
                                # for m in updatedic:
                                #     print (m,type(updatedic[m]))
                                TestPlanSW.objects.create(**updatedic)
                            # else:  # 新增的测项还没来得及维护到TestItemSW。
                            #     if 'TestItems' in i.keys():
                            #         item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase,
                            #                             'ItemNo_d': i['ItemNo_d'],
                            #                             'Item_d': i['Item_d'], 'TestItems': i['TestItems']})
                            #     else:
                            #         item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase,
                            #                             'ItemNo_d': i['ItemNo_d'],
                            #                             'Item_d': i['Item_d']})
                            #     # need update testitem first
                            #     print("新增的测项还没来得及维护到TestItemSW")
                            # else:#是OOC 或Wave,要么是FFRT的要么是C的，不会是B的
                            #     if 'TestItems' in i.keys():#link FFRT的TestItem
                            #         #OOC与Wave的test item可能来源于C或FFRT，但是有TestItems这个key说明一般是FFRT的Item
                            #         check_dic = {'Customer':responseData['customer'],'Phase': PhaseinItem[1],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems']}
                            #         check_dic_inplan = {'Customer': responseData['customer'], 'Phase': Phase,
                            #                      'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],
                            #                      'TestItems': i['TestItems']}
                            #     else:#link C的TestItem
                            #         #OOC与Wave的test item可能来源于C或FFRT，但是有TestItems这个key说明一般是C的Item
                            #         check_dic = {'Customer':responseData['customer'],'Phase': PhaseinItem[0],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                            #         check_dic_inplan = {'Customer': responseData['customer'], 'Phase': Phase,
                            #                      'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                            #     # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                            #     # print(check_dic)
                            #
                            #     check_list = TestItemSW.objects.filter(**check_dic).first()
                            #     check_dic_inplan["Projectinfo"] = Projectinfos
                            #     check_list_plan = TestPlanSW.objects.filter(**check_dic_inplan).first()
                            #     # print(check_list)
                            #
                            #     if check_list_plan:#其实跟editplan是一样的,update 直接找到这条的ID就可以了，他的关联的Test Item是不会变的。
                            #
                            #         editplan = TestPlanSW.objects.filter(**check_dic_inplan).first()
                            #         if editplan:
                            #             # if editplan.ItemNo_d == "BFA001_01":
                            #             #     print(editplan,editplan.BaseTime,i['BaseTime'],i)
                            #             #这几项是搜索条件中的一部分，如果不一样压根就搜不到。
                            #             # editplan.Customer = responseData['customer']
                            #             # editplan.Phase = Phase
                            #             #TestPlan表里没有Project，只有Re里面有
                            #             # editplan.Project = responseData['project']
                            #             # editplan.ItemNo_d = i['ItemNo_d']
                            #             # editplan.Item_d = i['Item_d']
                            #             # if 'TestItems' in i.keys():
                            #             #     editplan.TestItems = i['TestItems']
                            #             if 'Category' in i.keys():
                            #                 editplan.Category = i['Category']
                            #             if 'Category2' in i.keys():
                            #                 editplan.Category2 = i['Category2']
                            #             if 'Version' in i.keys():
                            #                 editplan.Version = i['Version']
                            #             if 'ReleaseDate' in i.keys():
                            #                 editplan.ReleaseDate = i['ReleaseDate']
                            #             if 'Owner' in i.keys():
                            #                 editplan.Owner = i['Owner']
                            #             if 'Priority' in i.keys():
                            #                 editplan.Priority = i['Priority']
                            #             if 'TDMSTotalTime' in i.keys():
                            #                 if i['TDMSTotalTime']:
                            #                     editplan.TDMSTotalTime = float(i['TDMSTotalTime'])
                            #             else:
                            #                 editplan.TDMSTotalTime = None
                            #             if 'BaseTime' in i.keys():
                            #                 # print(i['BaseTime'])
                            #                 if i['BaseTime']:
                            #                     editplan.BaseTime = float(i['BaseTime'])
                            #             else:
                            #                 editplan.BaseTime = None
                            #             if 'TDMSUnattendedTime' in i.keys():
                            #                 if i['TDMSUnattendedTime']:
                            #                     editplan.TDMSUnattendedTime = float(i['TDMSUnattendedTime'])
                            #             else:
                            #                 editplan.TDMSUnattendedTime = None
                            #             if 'BaseAotomationTime1SKU' in i.keys():
                            #                 if i['BaseAotomationTime1SKU']:
                            #                     # print(i['BaseAotomationTime1SKU'])
                            #                     editplan.BaseAotomationTime1SKU = float(i['BaseAotomationTime1SKU'])
                            #             else:
                            #                 editplan.BaseAotomationTime1SKU = None
                            #             if 'Chramshell' in i.keys():
                            #                 editplan.Chramshell = i['Chramshell']
                            #             if 'ConvertibaleNBMode' in i.keys():
                            #                 editplan.ConvertibaleNBMode = i['ConvertibaleNBMode']
                            #             if 'ConvertibaleYogaPadMode' in i.keys():
                            #                 editplan.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                            #             if 'DetachablePadMode' in i.keys():
                            #                 editplan.DetachablePadMode = i['DetachablePadMode']
                            #             if 'DetachableWDockmode' in i.keys():
                            #                 editplan.DetachableWDockmode = i['DetachableWDockmode']
                            #             if 'PhaseFVT' in i.keys():
                            #                 editplan.PhaseFVT = i['PhaseFVT']
                            #             if 'PhaseSIT' in i.keys():
                            #                 editplan.PhaseSIT = i['PhaseSIT']
                            #             if 'PhaseFFRT' in i.keys():
                            #                 editplan.PhaseFFRT = i['PhaseFFRT']
                            #             if 'Coverage' in i.keys():
                            #                 editplan.Coverage = i['Coverage']
                            #
                            #             if 'FeatureSupport' in i.keys():
                            #                 editplan.FeatureSupport = i['FeatureSupport']
                            #             if 'BaseTimeSupport' in i.keys():
                            #                 if i['BaseTimeSupport']:
                            #                     editplan.BaseTimeSupport = float(i['BaseTimeSupport'])
                            #             else:
                            #                 editplan.BaseTimeSupport = None
                            #             if 'TE' in i.keys():
                            #                 editplan.TE = i['TE']
                            #             if 'Schedule' in i.keys():
                            #                 editplan.Schedule = i['Schedule']
                            #             if 'ProjectTestSKUfollowMatrix' in i.keys():
                            #                 if i['ProjectTestSKUfollowMatrix']:
                            #                     editplan.ProjectTestSKUfollowMatrix = float(i['ProjectTestSKUfollowMatrix'])
                            #             else:
                            #                 editplan.ProjectTestSKUfollowMatrix = None
                            #             if 'TimewConfigFollowmatrix' in i.keys():
                            #                 if i['TimewConfigFollowmatrix']:
                            #                     editplan.TimewConfigFollowmatrix = float(i['TimewConfigFollowmatrix'])
                            #             else:
                            #                 editplan.TimewConfigFollowmatrix = None
                            #             if 'ConfigAutomationItem' in i.keys():
                            #                 editplan.ConfigAutomationItem = i['ConfigAutomationItem']
                            #             if 'ConfigAutomationTime' in i.keys():
                            #                 if i['ConfigAutomationTime']:
                            #                     editplan.ConfigAutomationTime = float(i['ConfigAutomationTime'])
                            #             else:
                            #                 editplan.ConfigAutomationTime = None
                            #             if 'ConfigLeverageItem' in i.keys():
                            #                 editplan.ConfigLeverageItem = i['ConfigLeverageItem']
                            #             if 'ConfigLeverageTime' in i.keys():
                            #                 if i['ConfigLeverageTime']:
                            #                     editplan.ConfigLeverageTime = float(i['ConfigLeverageTime'])
                            #             else:
                            #                 editplan.ConfigLeverageTime = None
                            #             if 'CommentsLeverage' in i.keys():
                            #                 editplan.CommentsLeverage = i['CommentsLeverage']
                            #             if 'ConfigSmartItem' in i.keys():
                            #                 editplan.ConfigSmartItem = i['ConfigSmartItem']
                            #             if 'ConfigSmartItemPer' in i.keys():
                            #                 if i['ConfigSmartItemPer']:
                            #                     editplan.ConfigSmartItemPer = float(i['ConfigSmartItemPer'])
                            #             else:
                            #                 editplan.ConfigSmartItemPer = None
                            #             if 'ConfigSmartTime' in i.keys():
                            #                 if i['ConfigSmartTime']:
                            #                     editplan.ConfigSmartTime = float(i['ConfigSmartTime'])
                            #             else:
                            #                 editplan.ConfigSmartTime = None
                            #             if 'CommentsSmart' in i.keys():
                            #                 editplan.CommentsSmart = i['CommentsSmart']
                            #             if 'ProjectTestSKUOptimize' in i.keys():
                            #                 if i['ProjectTestSKUOptimize']:
                            #                     editplan.ProjectTestSKUOptimize = float(i['ProjectTestSKUOptimize'])
                            #             else:
                            #                 editplan.ProjectTestSKUOptimize = None
                            #             if 'AttendTimeOptimize' in i.keys():
                            #                 if i['AttendTimeOptimize']:
                            #                     editplan.AttendTimeOptimize = float(i['AttendTimeOptimize'])
                            #             else:
                            #                 editplan.AttendTimeOptimize = None
                            #             if 'SKU1' in i.keys():
                            #                 editplan.SKU1 = i['SKU1']
                            #             if 'SKU2' in i.keys():
                            #                 # print(i['SKU2'])
                            #                 editplan.SKU2 = i['SKU2']
                            #             if 'SKU3' in i.keys():
                            #                 editplan.SKU3 = i['SKU3']
                            #             if 'SKU4' in i.keys():
                            #                 editplan.SKU4 = i['SKU4']
                            #             if 'SKU5' in i.keys():
                            #                 editplan.SKU5 = i['SKU5']
                            #             if 'SKU6' in i.keys():
                            #                 editplan.SKU6 = i['SKU6']
                            #             if 'SKU7' in i.keys():
                            #                 editplan.SKU7 = i['SKU7']
                            #             if 'SKU8' in i.keys():
                            #                 editplan.SKU8 = i['SKU8']
                            #             if 'SKU9' in i.keys():
                            #                 editplan.SKU9 = i['SKU9']
                            #             if 'SKU10' in i.keys():
                            #                 editplan.SKU10 = i['SKU10']
                            #             if 'SKU11' in i.keys():
                            #                 editplan.SKU11 = i['SKU11']
                            #             if 'SKU12' in i.keys():
                            #                 editplan.SKU12 = i['SKU12']
                            #             if 'SKU13' in i.keys():
                            #                 editplan.SKU13 = i['SKU13']
                            #             if 'SKU14' in i.keys():
                            #                 editplan.SKU14 = i['SKU14']
                            #             if 'SKU15' in i.keys():
                            #                 editplan.SKU15 = i['SKU15']
                            #             if 'SKU16' in i.keys():
                            #                 editplan.SKU16 = i['SKU16']
                            #             if 'SKU17' in i.keys():
                            #                 editplan.SKU17 = i['SKU17']
                            #             if 'SKU18' in i.keys():
                            #                 editplan.SKU18 = i['SKU18']
                            #             if 'SKU19' in i.keys():
                            #                 editplan.SKU19 = i['SKU19']
                            #             if 'SKU20' in i.keys():
                            #                 editplan.SKU20 = i['SKU20']
                            #             if 'ConfigRetestCycle' in i.keys():
                            #                 if i['ConfigRetestCycle']:
                            #                     editplan.ConfigRetestCycle = float(i['ConfigRetestCycle'])
                            #             else:
                            #                 editplan.ConfigRetestCycle = None
                            #             if 'ConfigRetestSKU' in i.keys():
                            #                 if i['ConfigRetestSKU']:
                            #                     editplan.ConfigRetestSKU = float(i['ConfigRetestSKU'])
                            #             else:
                            #                 editplan.ConfigRetestSKU = None
                            #             if 'ConfigRetestTime' in i.keys():
                            #                 if i['ConfigRetestTime']:
                            #                     editplan.ConfigRetestTime = float(i['ConfigRetestTime'])
                            #             else:
                            #                 editplan.ConfigRetestTime = None
                            #             editplan.editor = request.session.get('user_name')
                            #             editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            #             editplan.save()
                            #     else:
                            #         # create
                            #
                            #         # print(itemsinfo)
                            #         updatedic = {}
                            #         # 由于需要转成float,所以即使excel中的key与models中的一样也不能用如下方式
                            #         # for j in i.keys():
                            #         #     updatedic[j]=i[j]
                            #         # updatedic['Project'] = responseData['project']
                            #         updatedic['Projectinfo'] = TestProjectSW.objects.get(**dic_Project)
                            #         if check_list:  # 文档中的测项check_dic不存在于TestPlanSW中的某一个或几个机种中，但是存在于TestItemSW中，说明测试当下的case信息就是最新的case，则创建并linkTestItem表,否则只创建但是不linkTest Item表。
                            #             itemsinfo = TestItemSW.objects.get(id=check_list.id)
                            #             updatedic['Items'] = itemsinfo
                            #         updatedic['editor'] = request.session.get('user_name')
                            #         updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            #
                            #         updatedic["Customer"] = responseData['customer']
                            #         updatedic["Phase"] = Phase
                            #         # updatedic["Project"] = responseData['project']#TestPlan中没有这个key，只有Projectinfo，RetestItem里面才有
                            #         updatedic["ItemNo_d"] = i['ItemNo_d']
                            #         updatedic["Item_d"] = i['Item_d']
                            #         # 因为如上几项在other中是新增，并且可能重复存在，所以需要
                            #         if 'TestItems' in i.keys():
                            #             updatedic["TestItems"] = i['TestItems']
                            #         if 'Category' in i.keys():
                            #             updatedic["Category"] = i['Category']
                            #         if 'Category2' in i.keys():
                            #             updatedic["Category2"] = i['Category2']
                            #         if 'Version' in i.keys():
                            #             updatedic["Version"] = i['Version']
                            #         if 'ReleaseDate' in i.keys():
                            #             updatedic["ReleaseDate"] = i['ReleaseDate']
                            #         if 'Owner' in i.keys():
                            #             updatedic["Owner"] = i['Owner']
                            #         if 'Priority' in i.keys():
                            #             updatedic["Priority"] = i['Priority']
                            #         if 'TDMSsTotalTime' in i.keys():
                            #             if i['TDMSTotalTime']:
                            #                 updatedic["TDMSTotalTime"] = float(i['TDMSTotalTime'])
                            #         else:
                            #             updatedic["TDMSTotalTime"] = None
                            #         if 'BaseTime' in i.keys():
                            #             if i['BaseTime']:
                            #                 updatedic["BaseTime"] = float(i['BaseTime'])
                            #         else:
                            #             updatedic["BaseTime"] = None
                            #         if 'TDMSUnattendedTime' in i.keys():
                            #             if i['TDMSUnattendedTime']:
                            #                 updatedic["TDMSUnattendedTime"] = float(i['TDMSUnattendedTime'])
                            #         else:
                            #             updatedic["TDMSUnattendedTime"] = None
                            #         if 'BaseAotomationTime1SKU' in i.keys():
                            #             if i['BaseAotomationTime1SKU']:
                            #                 updatedic["BaseAotomationTime1SKU"] = float(i['BaseAotomationTime1SKU'])
                            #         else:
                            #             updatedic["BaseAotomationTime1SKU"] = None
                            #         if 'Chramshell' in i.keys():
                            #             updatedic["Chramshell"] = i['Chramshell']
                            #         if 'ConvertibaleNBMode' in i.keys():
                            #             updatedic["ConvertibaleNBMode"] = i['ConvertibaleNBMode']
                            #         if 'ConvertibaleYogaPadMode' in i.keys():
                            #             updatedic["ConvertibaleYogaPadMode"] = i['ConvertibaleYogaPadMode']
                            #         if 'DetachablePadMode' in i.keys():
                            #             updatedic["DetachablePadMode"] = i['DetachablePadMode']
                            #         if 'DetachableWDockmode' in i.keys():
                            #             updatedic["DetachableWDockmode"] = i['DetachableWDockmode']
                            #         if 'PhaseFVT' in i.keys():
                            #             updatedic["PhaseFVT"] = i['PhaseFVT']
                            #         if 'PhaseSIT' in i.keys():
                            #             updatedic["PhaseSIT"] = i['PhaseSIT']
                            #         if 'PhaseFFRT' in i.keys():
                            #             updatedic["PhaseFFRT"] = i['PhaseFFRT']
                            #         if 'Coverage' in i.keys():
                            #             updatedic["Coverage"] = i['Coverage']
                            #
                            #         if 'FeatureSupport' in i.keys():
                            #             updatedic["FeatureSupport"] = i['FeatureSupport']
                            #         if 'BaseTimeSupport' in i.keys():
                            #             if i['BaseTimeSupport']:
                            #                 updatedic["BaseTimeSupport"] = float(i['BaseTimeSupport'])
                            #         else:
                            #             updatedic["BaseTimeSupport"] = None
                            #         if 'TE' in i.keys():
                            #             updatedic["TE"] = i['TE']
                            #         if 'Schedule' in i.keys():
                            #             updatedic["Schedule"] = i['Schedule']
                            #         if 'ProjectTestSKUfollowMatrix' in i.keys():
                            #             if i['ProjectTestSKUfollowMatrix']:
                            #                 updatedic["ProjectTestSKUfollowMatrix"] = float(
                            #                     i['ProjectTestSKUfollowMatrix'])
                            #         else:
                            #             updatedic["ProjectTestSKUfollowMatrix"] = None
                            #         if 'TimewConfigFollowmatrix' in i.keys():
                            #             if i['TimewConfigFollowmatrix']:
                            #                 updatedic["TimewConfigFollowmatrix"] = float(i['TimewConfigFollowmatrix'])
                            #         else:
                            #             updatedic["TimewConfigFollowmatrix"] = None
                            #         if 'ConfigAutomationItem' in i.keys():
                            #             updatedic["ConfigAutomationItem"] = i['ConfigAutomationItem']
                            #         if 'ConfigAutomationTime' in i.keys():
                            #             if i['ConfigAutomationTime']:
                            #                 updatedic["ConfigAutomationTime"] = float(i['ConfigAutomationTime'])
                            #         else:
                            #             updatedic["ConfigAutomationTime"] = None
                            #         if 'ConfigLeverageItem' in i.keys():
                            #             updatedic["ConfigLeverageItem"] = i['ConfigLeverageItem']
                            #         if 'ConfigLeverageTime' in i.keys():
                            #             if i['ConfigLeverageTime']:
                            #                 updatedic["ConfigLeverageTime"] = float(i['ConfigLeverageTime'])
                            #         else:
                            #             updatedic["ConfigLeverageTime"] = None
                            #         if 'CommentsLeverage' in i.keys():
                            #             updatedic["CommentsLeverage"] = i['CommentsLeverage']
                            #         if 'ConfigSmartItem' in i.keys():
                            #             updatedic["ConfigSmartItem"] = i['ConfigSmartItem']
                            #         if 'ConfigSmartItemPer' in i.keys():
                            #             if i['ConfigSmartItemPer']:
                            #                 updatedic["ConfigSmartItemPer"] = float(i['ConfigSmartItemPer'])
                            #         else:
                            #             updatedic["ConfigSmartItemPer"] = None
                            #         if 'ConfigSmartTime' in i.keys():
                            #             if i['ConfigSmartTime']:
                            #                 updatedic["ConfigSmartTime"] = float(i['ConfigSmartTime'])
                            #         else:
                            #             updatedic["ConfigSmartTime"] = None
                            #         if 'CommentsSmart' in i.keys():
                            #             updatedic["CommentsSmart"] = i['CommentsSmart']
                            #         if 'ProjectTestSKUOptimize' in i.keys():
                            #             if i['ProjectTestSKUOptimize']:
                            #                 updatedic["ProjectTestSKUOptimize"] = float(i['ProjectTestSKUOptimize'])
                            #         else:
                            #             updatedic["ProjectTestSKUOptimize"] = None
                            #         if 'AttendTimeOptimize' in i.keys():
                            #             # print(i['AttendTimeOptimize'],type(i['AttendTimeOptimize']))
                            #             # print出来是int型，excel中是文字格式
                            #             if i['AttendTimeOptimize']:
                            #                 updatedic["AttendTimeOptimize"] = i[
                            #                     'AttendTimeOptimize']  # float(i['AttendTimeOptimize'])
                            #                 # print(type(updatedic["AttendTimeOptimize"]，type(i['AttendTimeOptimize']))
                            #         else:
                            #             updatedic["AttendTimeOptimize"] = None
                            #         if 'SKU1' in i.keys():
                            #             updatedic["SKU1"] = i['SKU1']
                            #         if 'SKU2' in i.keys():
                            #             updatedic["SKU2"] = i['SKU2']
                            #         if 'SKU3' in i.keys():
                            #             updatedic["SKU3"] = i['SKU3']
                            #         if 'SKU4' in i.keys():
                            #             updatedic["SKU4"] = i['SKU4']
                            #         if 'SKU5' in i.keys():
                            #             updatedic["SKU5"] = i['SKU5']
                            #         if 'SKU6' in i.keys():
                            #             updatedic["SKU6"] = i['SKU6']
                            #         if 'SKU7' in i.keys():
                            #             updatedic["SKU7"] = i['SKU7']
                            #         if 'SKU8' in i.keys():
                            #             updatedic["SKU8"] = i['SKU8']
                            #         if 'SKU9' in i.keys():
                            #             updatedic["SKU9"] = i['SKU9']
                            #         if 'SKU10' in i.keys():
                            #             updatedic["SKU10"] = i['SKU10']
                            #         if 'SKU11' in i.keys():
                            #             updatedic["SKU11"] = i['SKU11']
                            #         if 'SKU12' in i.keys():
                            #             updatedic["SKU12"] = i['SKU12']
                            #         if 'SKU13' in i.keys():
                            #             updatedic["SKU13"] = i['SKU13']
                            #         if 'SKU14' in i.keys():
                            #             updatedic["SKU14"] = i['SKU14']
                            #         if 'SKU15' in i.keys():
                            #             updatedic["SKU15"] = i['SKU15']
                            #         if 'SKU16' in i.keys():
                            #             updatedic["SKU16"] = i['SKU16']
                            #         if 'SKU17' in i.keys():
                            #             updatedic["SKU17"] = i['SKU17']
                            #         if 'SKU18' in i.keys():
                            #             updatedic["SKU18"] = i['SKU18']
                            #         if 'SKU19' in i.keys():
                            #             updatedic["SKU19"] = i['SKU19']
                            #         if 'SKU20' in i.keys():
                            #             updatedic["SKU20"] = i['SKU20']
                            #         if 'ConfigRetestCycle' in i.keys():
                            #             if i['ConfigRetestCycle']:
                            #                 updatedic["ConfigRetestCycle"] = float(i['ConfigRetestCycle'])
                            #         else:
                            #             updatedic["ConfigRetestCycle"] = None
                            #         if 'ConfigRetestSKU' in i.keys():
                            #             if i['ConfigRetestSKU']:
                            #                 updatedic["ConfigRetestSKU"] = float(i['ConfigRetestSKU'])
                            #         else:
                            #             updatedic["ConfigRetestSKU"] = None
                            #         if 'ConfigRetestTime' in i.keys():
                            #             if i['ConfigRetestTime']:
                            #                 updatedic["ConfigRetestTime"] = float(i['ConfigRetestTime'])
                            #         else:
                            #             updatedic["ConfigRetestTime"] = None
                            #
                            #         # print(updatedic)
                            #         # for m in updatedic:
                            #         #     print (m,type(updatedic[m]))
                            #         TestPlanSW.objects.create(**updatedic)
                            #     # else:#新增的测项还没来得及维护到TestItemSW。
                            #     #     if 'TestItems' in i.keys():
                            #     #         item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase, 'ItemNo_d': i['ItemNo_d'],
                            #     #                      'Item_d': i['Item_d'], 'TestItems': i['TestItems']})
                            #     #     else:
                            #     #         item_nodata.append({'Customer': responseData['customer'], 'Phase': Phase, 'ItemNo_d': i['ItemNo_d'],
                            #     #                      'Item_d': i['Item_d']})
                            #     #     #need update testitem first
                            #     #     print("新增的测项还没来得及维护到TestItemSW")
                # print("item_changeddata", item_changeddata)
                # print("item_nodata", item_nodata)

            # print(type(Phase))
            Phase = responseData['phase']

            if Phase == '0':
                Phase = 'B(FVT)'
                PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                PhaseinItem = ['Others']

            dic_Project_search = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
            # print(dic_Project)
            Projectinfos_search = TestProjectSW.objects.filter(**dic_Project_search).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos_search:
                for k in Projectinfos_search.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [
                        Projectinfos_search.SKU1, Projectinfos_search.SKU2, Projectinfos_search.SKU3, Projectinfos_search.SKU4,
                           Projectinfos_search.SKU5,
                           Projectinfos_search.SKU6, Projectinfos_search.SKU7, Projectinfos_search.SKU8, Projectinfos_search.SKU9,
                           Projectinfos_search.SKU10,
                           Projectinfos_search.SKU11, Projectinfos_search.SKU12, Projectinfos_search.SKU13, Projectinfos_search.SKU14,
                           Projectinfos_search.SKU15,
                           Projectinfos_search.SKU16, Projectinfos_search.SKU17, Projectinfos_search.SKU18, Projectinfos_search.SKU19,
                           Projectinfos_search.SKU20,
                        Projectinfos_search.SKU21, Projectinfos_search.SKU22, Projectinfos_search.SKU23,
                        Projectinfos_search.SKU24,
                        Projectinfos_search.SKU25,
                        Projectinfos_search.SKU26, Projectinfos_search.SKU27, Projectinfos_search.SKU28,
                        Projectinfos_search.SKU29,
                        Projectinfos_search.SKU30,
                        Projectinfos_search.SKU31, Projectinfos_search.SKU32, Projectinfos_search.SKU33,
                        Projectinfos_search.SKU34,
                        Projectinfos_search.SKU35,
                        Projectinfos_search.SKU36, Projectinfos_search.SKU37, Projectinfos_search.SKU38,
                        Projectinfos_search.SKU39,
                        Projectinfos_search.SKU40,
                        ]
                n = 1
                for l in SKUlist:
                    if l:
                        # print(l)
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": l.split('/')[1], "CPU": l.split('/')[0]})
                    n += 1
            # print(SKU)
            # if canEdit:
            #     itemlist = []
            #     for i in TestItemSW.objects.filter(Customer=responseData['customer'], Phase=Phase):
            #         itemlist.append(i.id)
            #     # print (itemlist,'yyy')
            #     existitem = []
            #     for i in Projectinfos.testplansw_set.all():
            #         existitem.append(i.Items.id)
            #     # print(existitem)
            #     for i in itemlist:
            #         if i in existitem:
            #             continue
            #         else:
            #             # print(TestProjectSW.objects.filter(**dic_Project).first())
            #             TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),
            #                                       Projectinfo=TestProjectSW.objects.filter(**dic_Project).first(),
            #                                       Customer=TestItemSW.objects.get(id=i).Customer,
            #                                       Phase=TestItemSW.objects.get(id=i).Phase,
            #                                       ItemNo_d=TestItemSW.objects.get(id=i).ItemNo_d,
            #                                       Item_d=TestItemSW.objects.get(id=i).Item_d,
            #                                       TestItems=TestItemSW.objects.get(id=i).TestItems,
            #                                       Category=TestItemSW.objects.get(id=i).Category,
            #                                       Category2=TestItemSW.objects.get(id=i).Category2,
            #                                       Version=TestItemSW.objects.get(id=i).Version,
            #                                       ReleaseDate=TestItemSW.objects.get(id=i).ReleaseDate,
            #                                       Owner=TestItemSW.objects.get(id=i).Owner,
            #                                       Priority=TestItemSW.objects.get(id=i).Priority,
            #                                       TDMSTotalTime=TestItemSW.objects.get(id=i).TDMSTotalTime,
            #                                       BaseTime=TestItemSW.objects.get(id=i).BaseTime,
            #                                       TDMSUnattendedTime=TestItemSW.objects.get(id=i).TDMSUnattendedTime,
            #                                       BaseAotomationTime1SKU=TestItemSW.objects.get(
            #                                           id=i).BaseAotomationTime1SKU,
            #                                       Chramshell=TestItemSW.objects.get(id=i).Chramshell,
            #                                       ConvertibaleNBMode=TestItemSW.objects.get(id=i).ConvertibaleNBMode,
            #                                       ConvertibaleYogaPadMode=TestItemSW.objects.get(
            #                                           id=i).ConvertibaleYogaPadMode,
            #                                       DetachablePadMode=TestItemSW.objects.get(id=i).DetachablePadMode,
            #                                       DetachableWDockmode=TestItemSW.objects.get(id=i).DetachableWDockmode,
            #                                       PhaseFVT=TestItemSW.objects.get(id=i).PhaseFVT,
            #                                       PhaseSIT=TestItemSW.objects.get(id=i).PhaseSIT,
            #                                       PhaseFFRT=TestItemSW.objects.get(id=i).PhaseFFRT,
            #                                       Coverage=TestItemSW.objects.get(id=i).Coverage,
            #                                       editor=request.session.get('user_name'),
            #                                       edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            #     # print (TestItemSW.objects.all().values('Category2').distinct().count())
            m = 0
            for i in TestItemSW.objects.all().values('Category2').distinct():
                # print(type(i),i)
                title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
                m += 1
            dic_Project = {'Customer': responseData['customer'], 'Project': responseData['project'], 'Phase': Phase}
            if RetestItemSW.objects.filter(**dic_Project).first():
                title.append({"caseid":  "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
            # print(title)

            updateData = {
                "MockData": title,
                "SKU": SKU,
                "selectMsg": combine,
                "canEdit": canEdit
            }
        #update
    return render(request, 'TestPlanSW/TestPlanSW_edit.html', locals())
#TestPlan_ME search
def TestPlanSW_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Search"
    # print(Skin)
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 1, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 1, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
    ]
    canEdit = 0
    title = [
        # {"caseid": "Basic", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Interaction", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Connectivity", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Process and Stroage", 'hasChildren': 'true',"unattendedtime": 6952, "basetimeA": 0,"basetime": 6952,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Performance", 'hasChildren': 'true',"unattendedtime": 6925, "basetimeA": 0,"basetime": 6925,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game Test", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6935,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Stress", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6495,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Application", 'hasChildren': 'true',"unattendedtime": 6595, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Compal internal", 'hasChildren': 'true',"unattendedtime": 6975, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game unique", 'hasChildren': 'true',"unattendedtime": 6957, "basetimeA": 0,"basetime": 6957,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Linux and DOS", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Accessories", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6975,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Gaming Unique", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6795,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
    ]
    proinfomation = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    SKU = [
        # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
        # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
        # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
        # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
        # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
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
    Sums = {
        # 'basetimeSum': 6000, 'unattendtimeSum': 5000, 'basetimeASum': 1000, 'BTSSum': 1299, 'TFCSum': 1999,
        #     'CATSum': 34556, 'CLTSum': 235, 'CSTSum': 5678, 'ATOSum': 9870, 'CRTSum': 2342
    }
    Sums1 = {
            # "Time_value": [1527, 1483, 344, 1971, 2103, 1493, 1000],
            # "Time_key": ["FVT Config-Retest time", "SIT Config-Retest time", "FFRT Config-Retest time",
            #              "FVT Attend Time", "SIT Attend Time", "FFRT 1st Attend Time", "FFRT 2nd Attend Time"],
            # "Quantity_top6_value": [1, 1, 1, 2, 3, 4],
            # 'Quantity_top6_key': ['EC Team', 'RF', 'EMI', 'SW Team', 'SA Team', 'Thermal Team']
            }
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]
    rdchangelist = [
        # {"Functionteam":"EC Team","Quantity":"1"},
        #           {"Functionteam":"RF","Quantity":"1"},
        #           {"Functionteam":"EMI","Quantity":"1"},
        #           {"Functionteam":"SW Team","Quantity":"2"},
        #           {"Functionteam":"SA Team","Quantity":"3"},
        #           {"Functionteam":"Thermal Team","Quantity":"4"}
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
    Customer_list = TestProjectSW.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSW.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSW.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(FVT)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "SIT2":
                    PhaseValue = 2
                if m['Phase'] == "GSKU":
                    PhaseValue = 3
                if m['Phase'] == "Wave":
                    PhaseValue = 4
                if m['Phase'] == "Wave2":
                    PhaseValue = 5
                if m['Phase'] == "Wave3":
                    PhaseValue = 6
                if m['Phase'] == "Wave4":
                    PhaseValue = 7
                if m['Phase'] == "Wave5":
                    PhaseValue = 8
                if m['Phase'] == "OOC":
                    PhaseValue = 9
                if m['Phase'] == "OOC2":
                    PhaseValue = 10
                if m['Phase'] == "OOC3":
                    PhaseValue = 11
                if m['Phase'] == "OOC4":
                    PhaseValue = 12
                if m['Phase'] == "OOC5":
                    PhaseValue = 13
                if m['Phase'] == "OOC6":
                    PhaseValue = 14
                if m['Phase'] == "FFRT":
                    PhaseValue = 15
                if m['Phase'] == "FFRT2":
                    PhaseValue = 16
                if m['Phase'] == "FFRT3":
                    PhaseValue = 17
                if m['Phase'] == "FFRT4":
                    PhaseValue = 18
                if m['Phase'] == "FFRT5":
                    PhaseValue = 19
                if m['Phase'] == "FFRT6":
                    PhaseValue = 20
                if m['Phase'] == "Others":
                    PhaseValue = 21
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    for i in TestProjectSW.objects.exclude(Customer='C38(AIO)').values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    # print (request.method)
    # print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            return HttpResponse(json.dumps(combine), content_type="application/json")
        elif request.GET.get("action") == "getCategory":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(FVT)'
                PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                PhaseinItem = ['Others']
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # func = lambda z: dict([(x, y) for y, x in z.items()])
            if TestItemSW.objects.count() > 0:
                for h in PhaseinItem:
                    dic_Item = {'Customer': Customer, 'Phase': h}
                    for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
                        title.append({"caseid": i['Category2']})

                seen = set()
                new_l = []
                for d in title:
                    t = tuple(d.items())
                    if t not in seen:
                        seen.add(t)
                        new_l.append(d)
                title = new_l
            if Phase == 'FFRT':
                title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
            # print (title)
            # if TestPlanSW.objects.filter(Projectinfo=Projectinfos).first():
            #     for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct().order_by('Category2'):
            #         title.append({"caseid": i['Category2']})
            # if RetestItemSW.objects.filter(**dic_Project).first():
            #     title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
            # # print (title)
            updateData = {
                "MockData": title,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        # elif request.GET.get("action") == "search":
        #     # if request.GET.get("customer") == "C38(NB)":
        #     Customer = request.GET.get('customer')
        #     Project = request.GET.get('project')
        #     Phase = request.GET.get('phase')
        #     # print(type(Phase))
        #     if Phase == '0':
        #         Phase = 'B(FVT)'
        #     if Phase == '1':
        #         Phase = 'C(SIT)'
        #     if Phase == '2':
        #         Phase = 'FFRT'
        #     if Phase == '3':
        #         Phase = 'Others'
        #     dic_Item = {'Customer': Customer, 'Phase': Phase}
        #     dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #     # print(dic_Project)
        #     Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
        #     # print(Projectinfos.Owner.all())
        #     # print(Projectinfos)
        #     canEdit = 0
        #     current_user = request.session.get('user_name')
        #     if Projectinfos:
        #         SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
        #                    Projectinfos.SKU5,
        #                    Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
        #                    Projectinfos.SKU10,
        #                    Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
        #                    Projectinfos.SKU15,
        #                    Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
        #                    Projectinfos.SKU20]
        #         n = 1
        #         for i in SKUlist:
        #             if i:
        #                 SKUno = 'SKU%s' % n
        #                 SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
        #             n += 1
        #     # print(SKU)
        #     m = 0
        #     for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct():
        #         # print(type(i),i)
        #         title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
        #         m += 1
        #     dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #     if RetestItemSW.objects.filter(**dic_Project).first():
        #         title.append({
        #                          "caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test",
        #                          'hasChildren': 'true'})
        #     # print(title)
        #
        #     updateData = {
        #         "MockData": title,
        #         "SKU": SKU,
        #         "selectMsg": combine,
        #         # "canEdit": canEdit
        #     }
        #     return HttpResponse(json.dumps(updateData), content_type="application/json")
        elif request.GET.get("action") == "getContent":#qishi mokeddata已经不要了，放到POST里面获取了，点击
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category2 = request.GET.get('category')
            # print(Category2)
            #Search的时候不需要知道Items是link那个Item的，度的都是TestPlan里面的测试当下的Item信息
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
            # print(Category2)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [
                        Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20,
                        Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                        Projectinfos.SKU25,
                        Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                        Projectinfos.SKU30,
                        Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                        Projectinfos.SKU35,
                        Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                        Projectinfos.SKU40,
                    ]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                        n += 1
                skuSHU = len(SKU)
            # print(SKU)
            # print(type(Phase))

            # if len(PhaseinItem) == 1:
            allSum = []#allSum的统计不受影响，因为统计是不管他的link的case
            # dic_ItemSum = {'Customer': Customer, 'Phase': PhaseinItem[0]}
            dic_ProjectSum = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            ProjectSum = TestProjectSW.objects.filter(**dic_ProjectSum).first()
            # print(ProjectSum)
            Retestitems = RetestItemSW.objects.filter(Projectinfo=ProjectSum).first()
            # print(Retestitems)
            #, Owner__contains="DQA"
            basetimesum = TestPlanSW.objects.filter(Projectinfo=ProjectSum,Owner__contains="DQA").values('Category2').annotate(
                Sum('BaseTime')).order_by('Category2')
            # basetimesumtotal = TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(
            #     Sum('BaseTime'))
            # print(basetimesum,'yy')
            # print(basetimesumtotal)
            BTSsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('BaseTimeSupport')).order_by('Category2')
            TFCsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('TimewConfigFollowmatrix')).order_by('Category2')
            CATsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('ConfigAutomationTime')).order_by('Category2')
            CLTsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('ConfigLeverageTime')).order_by('Category2')
            CSTsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('ConfigSmartTime')).order_by('Category2')
            ATOsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('AttendTimeOptimize')).order_by('Category2')
            CRTsum = TestPlanSW.objects.filter(Projectinfo=ProjectSum).values('Category2').annotate(
                Sum('ConfigRetestTime')).order_by('Category2')
            # print(basetimesum)
            # print(basetimesum[1])
            # print(BTSsum)
            if TestProjectSW.objects.filter(**dic_ProjectSum).first().Full_Function_Duration:
                FFD = TestProjectSW.objects.filter(**dic_ProjectSum).first().Full_Function_Duration
                # print(FFD)
            else:
                FFD = 0
            Num = 0
            for i in basetimesum:
                # print(i)
                if not BTSsum[Num]['BaseTimeSupport__sum']:
                    BTS1 = 0.00
                else:
                    BTS1 = round(BTSsum[Num]['BaseTimeSupport__sum'] / 60, 0)
                if not TFCsum[Num]['TimewConfigFollowmatrix__sum']:
                    TFC1 = 0.00
                else:
                    TFC1 = round(TFCsum[Num]['TimewConfigFollowmatrix__sum'] / 60, 0)
                if not CATsum[Num]['ConfigAutomationTime__sum']:
                    CAT1 = 0.00
                else:
                    CAT1 = round(CATsum[Num]['ConfigAutomationTime__sum'] / 60, 0)
                if not CLTsum[Num]['ConfigLeverageTime__sum']:
                    CLT1 = 0.00
                else:
                    CLT1 = round(CLTsum[Num]['ConfigLeverageTime__sum'] / 60, 0)
                if not CSTsum[Num]['ConfigSmartTime__sum']:
                    CST1 = 0.00
                else:
                    CST1 = round(CSTsum[Num]['ConfigSmartTime__sum'] / 60, 0)
                if not ATOsum[Num]['AttendTimeOptimize__sum']:
                    ATO1 = 0.00
                else:
                    ATO1 = round(ATOsum[Num]['AttendTimeOptimize__sum'] / 60, 0)
                if not CRTsum[Num]['ConfigRetestTime__sum']:
                    CRT1 = 0.00
                else:
                    CRT1 = round(CRTsum[Num]['ConfigRetestTime__sum'] / 60, 0)
                if not FFD:
                    HC = 0

                else:
                    HC = round(ATO1  / 6 / TestProjectSW.objects.filter(
                        **dic_ProjectSum).first().Full_Function_Duration, 2)
                allSum.append({'category': i['Category2'], 'basetime': round(i['BaseTime__sum'] / 60, 0), 'BTS': BTS1,
                               'TFC': TFC1, 'CAT': CAT1,
                               'CLT': CLT1, 'CST': CST1,
                               'ATO': ATO1, 'CRT': CRT1,
                               'HC': HC, 'HCOT': round(HC * 6 / 7, 2)})
                Num += 1

            if 'FFRT' in Phase:#FFRT，2，3，4，5，6上面的都一样，只是多了个Others，category,要在RetestItem里面算
                if Retestitems:
                    # dicSum_check = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
                    dicSum_check = {'Projectinfo': ProjectSum}
                    dicSum_check_BS = {'Projectinfo': ProjectSum, "Owner__contains": "DQA"}
                    # print(RetestItemSW.objects.filter(**dicSum_check))
                    if not FFD:
                        HCR = 0
                    else:
                        # print(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize'))[
                        #           'AttendTimeOptimize__sum'], TestProjectSW.objects.filter(
                        #     **dic_ProjectSum).first().Full_Function_Duration)
                        # print(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize')))
                        if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum']:
                            HCR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum'] / 60 / 6 / TestProjectSW.objects.filter(
                                **dic_ProjectSum).first().Full_Function_Duration, 2)
                        else:
                            HCR = 0
                        # print(HCR)
                    # 如果所有记录的这项内容都没填，结果就是none，提示不支持NoneType/int
                    if RetestItemSW.objects.filter(**dicSum_check_BS).aggregate(Sum('BaseTime'))['BaseTime__sum']:
                        basetimeR = round(RetestItemSW.objects.filter(**dicSum_check_BS).aggregate(Sum('BaseTime'))['BaseTime__sum'] / 60, 0)
                    else:
                        basetimeR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('BaseTimeSupport'))['BaseTimeSupport__sum']:
                        BTSR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('BaseTimeSupport'))['BaseTimeSupport__sum'] / 60, 0)
                    else:
                        BTSR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('TimewConfigFollowmatrix'))['TimewConfigFollowmatrix__sum']:
                        TFCR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('TimewConfigFollowmatrix'))['TimewConfigFollowmatrix__sum'] / 60, 0)
                    else:
                        TFCR =0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigAutomationTime'))['ConfigAutomationTime__sum']:
                        CATR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigAutomationTime'))['ConfigAutomationTime__sum'] / 60, 0)
                    else:
                        CATR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigLeverageTime'))['ConfigLeverageTime__sum']:
                        CLTR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigLeverageTime'))['ConfigLeverageTime__sum'] / 60, 0)
                    else:
                        CLTR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigSmartTime'))['ConfigSmartTime__sum']:
                        CSTR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigSmartTime'))['ConfigSmartTime__sum'] / 60, 0)
                    else:
                        CSTR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum']:
                        ATOR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum'] / 60, 0)
                    else:
                        ATOR = 0
                    if RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigRetestTime'))['ConfigRetestTime__sum']:
                        CRTR = round(RetestItemSW.objects.filter(**dicSum_check).aggregate(Sum('ConfigRetestTime'))['ConfigRetestTime__sum'] / 60, 0)
                    else:
                        CRTR = 0
                    allSum.append({
                        "category": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test",
                        'basetime': basetimeR, 'BTS': BTSR,
                        'TFC': TFCR, 'CAT': CATR,
                        'CLT': CLTR, 'CST': CSTR,
                        'ATO': ATOR, 'CRT': CRTR,
                        'HC': HCR, 'HCOT': round(HCR * 6 / 7, 2)})
            #allSum["Total"]
            basetime_Total = 0.0
            BTS1_Total = 0.00
            TFC1_Total = 0.00
            CAT1_Total = 0.00
            CLT1_Total = 0.00
            CST1_Total = 0.00
            ATO1_Total = 0.00
            CRT1_Total = 0.00
            HC_Total = 0.00
            HCOT_Total = 0.00
            for i in allSum:
                # basetime_Total += i["basetime"]
                # BTS1_Total += i["BTS"]
                # TFC1_Total += i["TFC"]
                # CAT1_Total += i["CAT"]
                # CLT1_Total += i["CLT"]
                # CST1_Total += i["CST"]
                # ATO1_Total += i["ATO"]
                # CRT1_Total += i["CRT"]
                HC_Total += i["HC"]
                HCOT_Total += i["HCOT"]
            #主要时为了与表格里面的算法一致，防止两边有误差
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").aggregate(Sum('BaseTime'))['BaseTime__sum']:
                basetime_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").aggregate(Sum('BaseTime'))['BaseTime__sum']/60, 0)
            else:
                basetime_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('BaseTimeSupport'))['BaseTimeSupport__sum']:
                BTS1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('BaseTimeSupport'))['BaseTimeSupport__sum']/60, 0)
            else:
                BTS1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('TimewConfigFollowmatrix'))['TimewConfigFollowmatrix__sum']:
                TFC1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('TimewConfigFollowmatrix'))['TimewConfigFollowmatrix__sum']/60, 0)
            else:
                TFC1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigAutomationTime'))['ConfigAutomationTime__sum']:
                CAT1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigAutomationTime'))['ConfigAutomationTime__sum']/60, 0)
            else:
                CAT1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigLeverageTime'))['ConfigLeverageTime__sum']:
                CLT1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigLeverageTime'))['ConfigLeverageTime__sum']/60, 0)
            else:
                CLT1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigSmartTime'))['ConfigSmartTime__sum']:
                CST1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigSmartTime'))['ConfigSmartTime__sum']/60, 0)
            else:
                CST1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum']:
                ATO1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('AttendTimeOptimize'))['AttendTimeOptimize__sum']/60, 0)
            else:
                ATO1_Total = 0
            if TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigRetestTime'))['ConfigRetestTime__sum']:
                CRT1_Total = round(TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigRetestTime'))['ConfigRetestTime__sum']/60, 0)
            else:
                CRT1_Total = 0
            if 'FFRT' in Phase:#FFRT，2，3，4，5，6上面的都一样，只是多了个Others，category,要在RetestItem里面算
                if Retestitems:
                    basetime_Total = basetime_Total+ basetimeR
                    BTS1_Total = BTS1_Total + BTSR
                    TFC1_Total = TFC1_Total + TFCR
                    CAT1_Total = CAT1_Total + CATR
                    CLT1_Total = CLT1_Total + CLTR
                    CST1_Total = CST1_Total + CSTR
                    ATO1_Total = ATO1_Total + ATOR
                    CRT1_Total = CRT1_Total + CRTR
            allSum.insert(0, {'category': 'Total', 'basetime': round(basetime_Total, 0), 'BTS': round(BTS1_Total, 0),
                           'TFC': round(TFC1_Total, 0), 'CAT': round(CAT1_Total, 0),
                           'CLT': round(CLT1_Total, 0), 'CST': round(CST1_Total, 0),
                           'ATO': round(ATO1_Total, 0), 'CRT': round(CRT1_Total, 0),
                           'HC': round(HC_Total, 2), 'HCOT': round(HCOT_Total, 2)})
            # print(allSum)

            # for i in PhaseinItem:
            #     dicItem = {'Customer': Customer, 'Phase': i, 'Category2': Category2}
            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            dic_Project_BS = {'Customer': Customer, 'Project': Project, 'Phase': Phase, "Owner":"DQA"}
            # print(dic_Project)
            if request.GET.get("category") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":#只有是FFRE，2，3，4，5，6才会有Others
                RetestItemSWinfo = RetestItemSW.objects.filter(**dic_Project)
                if RetestItemSWinfo:
                    # basetimeSum = 0.00
                    # unattendtimeSum = 0.00
                    # basetimeASum = 0.00
                    # BTSSum = 0.00
                    # TFCSum = 0.00
                    # CATSum = 0.00
                    # CLTSum = 0.00
                    # CSTSum = 0.00
                    # ATOSum = 0.00
                    # CRTSum = 0.00
                    for i in RetestItemSWinfo:
                        planOptimize = []
                        SKUlist_R = {
                                    "SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9, "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                                    "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24, "SKU25": i.SKU25,
                                    "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29, "SKU30": i.SKU30,
                                    "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34,
                                    "SKU35": i.SKU35,
                                    "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39,
                                    "SKU40": i.SKU40,
                        }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_R.keys():
                                planOptimize.append(SKUlist_R[j["skuNo"]])
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'conAtime': i.ConfigAutomationTime, 'conLtime': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItem, 'conStime': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })
                        # basetimeSum += i.BaseTime
                        # unattendtimeSum += i.TDMSUnattendedTime
                        # basetimeASum += i.BaseAotomationTime1SKU
                        # if i.BaseTimeSupport:
                        #     BTSSum += i.BaseTimeSupport
                        # if i.TimewConfigFollowmatrix:
                        #     TFCSum += i.TimewConfigFollowmatrix
                        # if i.ConfigAutomationTime:
                        #     CATSum += i.ConfigAutomationTime
                        # if i.ConfigLeverageTime:
                        #     CLTSum += i.ConfigLeverageTime
                        # if i.ConfigSmartTime:
                        #     CSTSum += i.ConfigSmartTime
                        # if i.AttendTimeOptimize:
                        #     ATOSum += i.AttendTimeOptimize
                        # if i.ConfigRetestTime:
                        #     CRTSum += i.ConfigRetestTime
                    Sums['basetimeSum'] = RetestItemSW.objects.filter(**dic_Project_BS).aggregate(Sum('BaseTime'))['BaseTime__sum']
                    Sums['unattendtimeSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('TDMSUnattendedTime'))['TDMSUnattendedTime__sum']
                    Sums['basetimeASum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('BaseAotomationTime1SKU'))['BaseAotomationTime1SKU__sum']
                    Sums['BTSSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('BaseTimeSupport'))['BaseTimeSupport__sum']
                    Sums['TFCSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('TimewConfigFollowmatrix'))[
                        'TimewConfigFollowmatrix__sum']
                    Sums['CATSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('ConfigAutomationTime'))[
                        'ConfigAutomationTime__sum']
                    Sums['CLTSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('ConfigLeverageTime'))[
                        'ConfigLeverageTime__sum']
                    Sums['CSTSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('ConfigSmartTime'))[
                        'ConfigSmartTime__sum']
                    Sums['ATOSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('AttendTimeOptimize'))[
                        'AttendTimeOptimize__sum']
                    Sums['CRTSum'] = RetestItemSW.objects.filter(**dic_Project).aggregate(Sum('ConfigRetestTime'))[
                        'ConfigRetestTime__sum']
                    # Sums['basetimeSum'] = basetimeSum
                    # Sums['unattendtimeSum'] = unattendtimeSum
                    # Sums['basetimeASum'] = basetimeASum
                    # Sums['BTSSum'] = BTSSum
                    # Sums['TFCSum'] = TFCSum
                    # Sums['CATSum'] = CATSum
                    # Sums['CLTSum'] = CLTSum
                    # Sums['CSTSum'] = CSTSum
                    # Sums['ATOSum'] = ATOSum
                    # Sums['CRTSum'] = CRTSum

                    # print(newContents)
            else:
                # print('Others')
                # Iteminfos = TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category2': Category2, "Projectinfo": Projectinfos}
                if Projectinfos:
                    x = 0

                    for i in TestPlanSW.objects.filter(**dicPlan):
                        x += 1
                        # print(i,type(i))
                        # print(i.id)
                        planOptimize = []
                        SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                     "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                                     "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24,
                                     "SKU25": i.SKU25,
                                     "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29,
                                     "SKU30": i.SKU30,
                                     "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34,
                                     "SKU35": i.SKU35,
                                     "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39,
                                     "SKU40": i.SKU40,
                                     }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_T.keys():
                                planOptimize.append(SKUlist_T[j["skuNo"]])
                        # print(planOptimize)
                        # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                        newContents.append(
                            {  # item
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT,
                                'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                # plan
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize,
                                'CRC': i.ConfigRetestCycle, 'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })

                    Sums['basetimeSum'] = TestPlanSW.objects.filter(**dicPlan).aggregate(Sum('BaseTime'))[
                        'BaseTime__sum']
                    Sums['unattendtimeSum'] = TestPlanSW.objects.filter(**dicPlan).aggregate(Sum('TDMSUnattendedTime'))[
                        'TDMSUnattendedTime__sum']
                    Sums['basetimeASum'] = TestPlanSW.objects.filter(**dicPlan).aggregate(Sum('BaseAotomationTime1SKU'))[
                        'BaseAotomationTime1SKU__sum']
                    # Sums['BTSSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('BaseTimeSupport'))[
                    #     'BaseTimeSupport__sum']
                    # Sums['TFCSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('TimewConfigFollowmatrix'))[
                    #     'TimewConfigFollowmatrix__sum']
                    # Sums['CATSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('ConfigAutomationTime'))[
                    #     'ConfigAutomationTime__sum']
                    # Sums['CLTSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('ConfigLeverageTime'))[
                    #     'ConfigLeverageTime__sum']
                    # Sums['CSTSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('ConfigSmartTime'))[
                    #     'ConfigSmartTime__sum']
                    # Sums['ATOSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('AttendTimeOptimize'))[
                    #     'AttendTimeOptimize__sum']
                    # Sums['CRTSum'] = TestPlanSW.objects.filter(**dic_Project).aggregate()(Sum('ConfigRetestTime'))[
                    #     'ConfigRetestTime__sum']
                    # Sums['basetimeSum'] = basetimeSum
                    # Sums['unattendtimeSum'] = unattendtimeSum
                    # Sums['basetimeASum'] = basetimeASum
                    for i in allSum:
                        if i['category'] == request.GET.get("category"):
                            Sums['BTSSum'] = i['BTS']
                            Sums['TFCSum'] = i['TFC']
                            Sums['CATSum'] = i['CAT']
                            Sums['CLTSum'] = i['CLT']
                            Sums['CSTSum'] = i['CST']
                            Sums['ATOSum'] = i['ATO']
                            Sums['CRTSum'] = i['CRT']
                    # print(newContents)
                    # print(x)
            # print(newContents)
            # print(Sums)
            # else:#OOC或Wave
            #     print()
            updateData = {
                "content": newContents,
                "SKU": SKU,
                "canEdit": canEdit,
                "Sum": Sums,
                "allSum": allSum,
                "skuSHU": skuSHU,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")
    if request.method == "POST":
        # print(request.POST.get("isGetData"))
        if request.POST.get("isGetData") == "first":
            selectItem
        if request.POST.get("isGetData") == "SEARCH":
            Customer = request.POST.get('Customer')
            Project = request.POST.get('Project')
            Phase = request.POST.get('Phase')
            Category2 = request.POST.get('category')
            if Phase == '0':
                Phase = 'B(FVT)'
                # PhaseinItem = ['B(FVT)']
            if Phase == '1':
                Phase = 'C(SIT)'
                # PhaseinItem = ['C(SIT)']
            if Phase == '2':
                Phase = 'SIT2'
                # PhaseinItem = ['C(SIT)']
            if Phase == '3':
                Phase = 'GSKU'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '4':
                Phase = 'Wave'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '5':
                Phase = 'Wave2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '6':
                Phase = 'Wave3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '7':
                Phase = 'Wave4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '8':
                Phase = 'Wave5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '9':
                Phase = 'OOC'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '10':
                Phase = 'OOC2'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '11':
                Phase = 'OOC3'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '12':
                Phase = 'OOC4'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '13':
                Phase = 'OOC5'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '14':
                Phase = 'OOC6'
                # PhaseinItem = ['C(SIT)', 'FFRT']
            if Phase == '15':
                Phase = 'FFRT'
                # PhaseinItem = ['FFRT']
            if Phase == '16':
                Phase = 'FFRT2'
                # PhaseinItem = ['FFRT']
            if Phase == '17':
                Phase = 'FFRT3'
                # PhaseinItem = ['FFRT']
            if Phase == '18':
                Phase = 'FFRT4'
                # PhaseinItem = ['FFRT']
            if Phase == '19':
                Phase = 'FFRT5'
                # PhaseinItem = ['FFRT']
            if Phase == '20':
                Phase = 'FFRT6'
                # PhaseinItem = ['FFRT']
            if Phase == '21':
                Phase = 'Others'
                # PhaseinItem = ['Others']
            # print(Category2)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20,
                           Projectinfos.SKU21, Projectinfos.SKU22, Projectinfos.SKU23, Projectinfos.SKU24,
                           Projectinfos.SKU25,
                           Projectinfos.SKU26, Projectinfos.SKU27, Projectinfos.SKU28, Projectinfos.SKU29,
                           Projectinfos.SKU30,
                           Projectinfos.SKU31, Projectinfos.SKU32, Projectinfos.SKU33, Projectinfos.SKU34,
                           Projectinfos.SKU35,
                           Projectinfos.SKU36, Projectinfos.SKU37, Projectinfos.SKU38, Projectinfos.SKU39,
                           Projectinfos.SKU40,
                           ]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1
            # print(SKU)
            # print(type(Phase))


            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            # print(request.POST.get("category"))
            if request.POST.get("category") == "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test":#只有是FFRE，2，3，4，5，6才会有Others
                # print('FFRTsubmit')
                RetestItemSWinfo = RetestItemSW.objects.filter(**dic_Project)
                if RetestItemSWinfo:
                    for i in RetestItemSWinfo:
                        planOptimize = []
                        SKUlist_R = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9, "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                                     "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24,
                                     "SKU25": i.SKU25,
                                     "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29,
                                     "SKU30": i.SKU30,
                                     "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34,
                                     "SKU35": i.SKU35,
                                     "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39,
                                     "SKU40": i.SKU40,
                                     }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_R.keys():
                                planOptimize.append(SKUlist_R[j["skuNo"]])
                            # print(planOptimize)
                        newContents.append(
                            {  # Reitem
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT, 'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize, 'CRC': i.ConfigRetestCycle,
                                'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'conAtime': i.ConfigAutomationTime, 'conLtime': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItemPer, 'conStime': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })

            else:
                # print('Others')
                # Iteminfos = TestItemSW.objects.filter(**dicItem)
                Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
                # print(Projectinfos.Owner.all())
                # print(Iteminfos)
                # print(Projectinfos)
                dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category2': Category2, "Projectinfo": Projectinfos}
                if Projectinfos:
                    x = 0

                    for i in TestPlanSW.objects.filter(**dicPlan):
                        x += 1
                        # print(i,type(i))
                        # print(i.id)
                        planOptimize = []
                        SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                     "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                     "SKU10": i.SKU10,
                                     "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                     "SKU15": i.SKU15,
                                     "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                     "SKU20": i.SKU20,
                                     "SKU21": i.SKU21, "SKU22": i.SKU22, "SKU23": i.SKU23, "SKU24": i.SKU24,
                                     "SKU25": i.SKU25,
                                     "SKU26": i.SKU26, "SKU27": i.SKU27, "SKU28": i.SKU28, "SKU29": i.SKU29,
                                     "SKU30": i.SKU30,
                                     "SKU31": i.SKU31, "SKU32": i.SKU32, "SKU33": i.SKU33, "SKU34": i.SKU34,
                                     "SKU35": i.SKU35,
                                     "SKU36": i.SKU36, "SKU37": i.SKU37, "SKU38": i.SKU38, "SKU39": i.SKU39,
                                     "SKU40": i.SKU40,
                                     }
                        for j in SKU:
                            if j["skuNo"] in SKUlist_T.keys():
                                planOptimize.append(SKUlist_T[j["skuNo"]])
                        # print(planOptimize)
                        # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                        newContents.append(
                            {  # item
                                "id": i.id, "caseid": i.ItemNo_d, "casename": i.Item_d,
                                "testitem": i.TestItems,
                                "version": i.Version,
                                "releasedate": i.ReleaseDate, "owner": i.Owner,
                                "priority": i.Priority,
                                # TDMSTotalTime前端直接后两项加总
                                "basetime": i.BaseTime,
                                "unattendedtime": i.TDMSUnattendedTime,
                                "basetimeA": i.BaseAotomationTime1SKU,
                                "chramshell": i.Chramshell, "conver_NB": i.ConvertibaleNBMode,
                                "conver_Yoga": i.ConvertibaleYogaPadMode,
                                "detach_Pad": i.DetachablePadMode, "detach_W": i.DetachableWDockmode,
                                "PhaseF": i.PhaseFVT, "PhaseS": i.PhaseSIT,
                                'PhaseFFRT': i.PhaseFFRT,
                                "coverage": i.Coverage,
                                # plan
                                'FS': i.FeatureSupport, 'TE': i.TE, 'schedule': i.Schedule,
                                'starttime': i.ProjectTestSKUfollowMatrix, 'conAitem': i.ConfigAutomationItem,
                                'conLitem': i.ConfigLeverageItem, 'comments1': i.CommentsLeverage,
                                'conSitem': i.ConfigSmartItem,
                                'comments2': i.CommentsSmart, "planOptimize": planOptimize,
                                'CRC': i.ConfigRetestCycle, 'CRS': i.ConfigRetestSKU, 'CRT': i.ConfigRetestTime,
                                # no need edit
                                'BTS': i.BaseTimeSupport, 'TFC': i.TimewConfigFollowmatrix,
                                'CAT': i.ConfigAutomationTime, 'CLT': i.ConfigLeverageTime,
                                'conSitemInAll': i.ConfigSmartItemPer, 'CST': i.ConfigSmartTime,
                                'proTS': i.ProjectTestSKUOptimize, 'ATO': i.AttendTimeOptimize
                            })
        if request.POST.get("isGetData") == "searchalert":
            Customer = request.POST.get("Customer")
            Prolist = []
            # print(Customer)
            if Customer:
                for i in TestProjectSW.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append({"Project": i["Project"]})
            else:
                for i in TestProjectSW.objects.all().values("Project").distinct().order_by("Project"):
                    Prolist.append({"Project": i["Project"]})
            # print(Prolist)
            for i in Prolist:
                # print(i)
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                    proinfomation.append({
                        "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                        "COMPRJCODE": i["Project"],
                        # "PHASE": i["Phase"],
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                        "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                        "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                    })
                else:
                    # print(i)
                    if len(i['Project']) > 5:
                        Prostr1 = i['Project'][0:5]
                        Prostr2 = i['Project'][0:3] + i['Project'][5:]
                        Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                        Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                        if Proinfo1 and Proinfo2:
                            if Proinfo1.Year == Proinfo2.Year:
                                Year = Proinfo1.Year
                            else:
                                Year = Proinfo1.Year + "/" + Proinfo2.Year
                            if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                PrjEngCode1 = Proinfo1.PrjEngCode1
                            else:
                                PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                            if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                PrjEngCode2 = Proinfo1.PrjEngCode2
                            else:
                                PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                            if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                ProjectName = Proinfo1.ProjectName
                            else:
                                ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                            if Proinfo1.Size == Proinfo2.Size:
                                Size = Proinfo1.Size
                            else:
                                Size = Proinfo1.Size + "/" + Proinfo2.Size
                            if Proinfo1.CPU == Proinfo2.CPU:
                                CPU = Proinfo1.CPU
                            else:
                                CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                            if Proinfo1.Platform == Proinfo2.Platform:
                                Platform = Proinfo1.Platform
                            else:
                                Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                            if Proinfo1.VGA == Proinfo2.VGA:
                                VGA = Proinfo1.VGA
                            else:
                                VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                            if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                OSSupport = Proinfo1.OSSupport
                            else:
                                OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                            if Proinfo1.Type == Proinfo2.Type:
                                Type = Proinfo1.Type
                            else:
                                Type = Proinfo1.Type + "/" + Proinfo2.Type
                            if Proinfo1.PPA == Proinfo2.PPA:
                                PPA = Proinfo1.PPA
                            else:
                                PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                            if Proinfo1.PQE == Proinfo2.PQE:
                                PQE = Proinfo1.PQE
                            else:
                                PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                            if Proinfo1.SS == Proinfo2.SS:
                                SS = Proinfo1.SS
                            else:
                                SS = Proinfo1.SS + "/" + Proinfo2.SS
                            if Proinfo1.LD == Proinfo2.LD:
                                LD = Proinfo1.LD
                            else:
                                LD = Proinfo1.LD + "/" + Proinfo2.LD
                            if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                DQAPL = Proinfo1.DQAPL
                            else:
                                DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                            proinfomation.append({
                                "id": Proinfo1.id,
                                "YEAR": Year,
                                "COMPRJCODE": i["Project"],
                                # "PHASE": i["Phase"],
                                "PrjEngCode1": PrjEngCode1,
                                "PrjEngCode2": PrjEngCode2,
                                "PROJECT": ProjectName,
                                "SIZE": Size,
                                "CPU": CPU,
                                "PLATFORM": Platform,
                                "VGA": VGA,
                                "OSSUPPORT": OSSupport,
                                "Type": Type,
                                "PPA": PPA,
                                "PQE": PQE,
                                "SS": SS,
                                "LD": LD,
                                "DQAPL": DQAPL,
                            })
                        else:
                            proinfomation.append({
                                "id": "",
                                "YEAR": "", "COMPRJCODE": i["Project"],
                                # "PHASE": i["Phase"],
                                # "CUSPRJCODE": "",
                                "PrjEngCode1": "",
                                "PrjEngCode2": "",
                                "PROJECT": "",
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
                    else:
                        proinfomation.append({
                            "id": "",
                            "YEAR": "", "COMPRJCODE": i["Project"],
                            # "PHASE": i["Phase"],
                            "PrjEngCode1": "",
                            "PrjEngCode2": "",
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
        if request.POST.get("isGetData") == "SELECTPRO":

            Customer = request.POST.get("Customer")
            Project = request.POST.get("COMPRJCODE")
            check_dic_Pro = {"Customer": Customer, "Project": Project}
            # print(Customer)
            Time_key = []
            if TestProjectSW.objects.filter(**check_dic_Pro).first():#至少存在一个Phase
                for h in TestProjectSW.objects.filter(**check_dic_Pro).values("Phase").order_by("-ScheduleEnd"):
                    Time_key.append(h["Phase"])

                Time_value_Re = []
                Time_value_Re_ATO = []
                Time_value_CAT = []
                Time_value_CLT = []
                Time_value_CST = []
                Quantity_top6_value = [
                                          # [1003, 1001, 1002, 1006],#auto
                                          # [1527, 1483, 344, 1971], #leverage
                                          # [1971, 2103, 1493, 1000] #smart
                                      ],
                Quantity_top6_key = [
                    # 'FFRT', 'SIT', 'FVT', 'TOTAL'
                ]
                for i in Time_key:
                    check_dic = {"Customer": Customer, "Project": Project, "Phase": i}
                    # print(check_dic)
                    Projectinfo = TestProjectSW.objects.filter(**check_dic).first()
                    CRTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigRetestTime'))
                    ATOsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('AttendTimeOptimize'))
                    CATsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigAutomationTime'))
                    CLTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigLeverageTime'))
                    CSTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigSmartTime'))
                    CRTsuminre = RetestItemSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigRetestTime'))
                    ATOsuminre = RetestItemSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('AttendTimeOptimize'))
                    CATsuminre = RetestItemSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigAutomationTime'))
                    CLTsuminre = RetestItemSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigLeverageTime'))
                    CSTsuminre = RetestItemSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigSmartTime'))

                    if CRTsum["ConfigRetestTime__sum"]:
                        CRTtotal = CRTsum["ConfigRetestTime__sum"]
                    else:
                        CRTtotal = 0
                    if CRTsuminre["ConfigRetestTime__sum"]:
                        CRTtotal = CRTtotal + CRTsuminre["ConfigRetestTime__sum"]
                    else:
                        CRTtotal = CRTtotal + 0

                    if ATOsum["AttendTimeOptimize__sum"]:
                        ATOtotal = ATOsum["AttendTimeOptimize__sum"]
                    else:
                        ATOtotal = 0
                    if ATOsuminre["AttendTimeOptimize__sum"]:
                        ATOtotal = ATOtotal + ATOsuminre["AttendTimeOptimize__sum"]
                    else:
                        ATOtotal = ATOtotal + 0

                    if CATsum["ConfigAutomationTime__sum"]:
                        CATtotal = CATsum["ConfigAutomationTime__sum"]
                    else:
                        CATtotal = 0
                    if CATsuminre["ConfigAutomationTime__sum"]:
                        CATtotal = CATtotal + CATsuminre["ConfigAutomationTime__sum"]
                    else:
                        CATtotal = CATtotal + 0

                    if CLTsum["ConfigLeverageTime__sum"]:
                        CLTtotal = CLTsum["ConfigLeverageTime__sum"]
                    else:
                        CLTtotal = 0
                    if CLTsuminre["ConfigLeverageTime__sum"]:
                        CLTtotal = CLTtotal + CLTsuminre["ConfigLeverageTime__sum"]
                    else:
                        CLTtotal = CLTtotal + 0

                    if CSTsum["ConfigSmartTime__sum"]:
                        CSTtotal = CSTsum["ConfigSmartTime__sum"]
                    else:
                        CSTtotal = 0
                    if CSTsuminre["ConfigSmartTime__sum"]:
                        CSTtotal = CSTtotal + CSTsuminre["ConfigSmartTime__sum"]
                    else:
                        CSTtotal = CSTtotal + 0

                    Time_value_Re.append(round(CRTtotal/60, 0))
                    Time_value_Re_ATO.append(round(ATOtotal/60, 0))
                    Time_value_CAT.append(round(CATtotal/60, 0))
                    Time_value_CLT.append(round(CLTtotal / 60, 0))
                    Time_value_CST.append(round(CSTtotal / 60, 0))
                Project_ReTotal = 0
                for i in Time_value_Re:
                    Project_ReTotal += i
                Time_value_Re.append(round(Project_ReTotal, 0))
                Project_ATOTotal = 0
                for i in Time_value_Re_ATO:
                    Project_ATOTotal += i
                Time_value_Re_ATO.append(round(Project_ATOTotal, 0))
                Project_CATTotal = 0
                for i in Time_value_CAT:
                    Project_CATTotal += i
                Time_value_CAT.append(round(Project_CATTotal, 0))
                Project_CLTotal = 0
                for i in Time_value_CLT:
                    Project_CLTotal += i
                Time_value_CLT.append(round(Project_CLTotal, 0))
                Project_CSTotal = 0
                for i in Time_value_CST:
                    Project_CSTotal += i
                Time_value_CST.append(round(Project_CSTotal, 0))
                Time_key.append("Total")
                Sums1["Time_value"] = [Time_value_Re, Time_value_Re_ATO]
                Sums1["Time_key"] = Time_key

                Quantity_top6_key = Time_key
                Sums1["Quantity_top6_value"] = [Time_value_CAT, Time_value_CLT, Time_value_CST]
                Sums1["Quantity_top6_key"] = Quantity_top6_key
            # if FFRTByRD.objects.filter(**check_dic_Pro).first():
            #     FFRTByRDinfo = FFRTByRD.objects.filter(**check_dic_Pro).first()
            #     Quantity_dic = {"EC": FFRTByRDinfo.EC, "RF": FFRTByRDinfo.RF, "EMI": FFRTByRDinfo.EMI, "ESD": FFRTByRDinfo.ESD,
            #                     "HW": FFRTByRDinfo.HW, "SW": FFRTByRDinfo.SW, "SA": FFRTByRDinfo.SA, "SIT": FFRTByRDinfo.SIT,
            #                     "Thermal": FFRTByRDinfo.Thermal, "Power": FFRTByRDinfo.Power, "SED": FFRTByRDinfo.SED,}
            #
            #     TOP_list = sorted(Quantity_dic.items(), key=lambda x: x[1], reverse=False)[-5:]
            #     Quantity_top6_key = []
            #     Quantity_top6_value = []
            #     for i in TOP_list:
            #         Quantity_top6_value.append(i[1])
            #         Quantity_top6_key.append(i[0])
            #     Sums1["Quantity_top6_value"] = Quantity_top6_value
            #     Sums1["Quantity_top6_key"] = Quantity_top6_key

            canEdit = 0
            current_user = request.session.get('user_name')
            if TestProjectSW.objects.filter(**check_dic_Pro).first():
                for h in TestProjectSW.objects.filter(**check_dic_Pro):
                    for i in h.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if i.username == current_user:
                            canEdit = 1
                            break
        # if request.POST.get("isGetData") == "getRdChange":
        #     Customer = request.POST.get("Customer")
        #     Project = request.POST.get("Project")
        #     check_dic_Pro = {"Customer": Customer, "Project": Project}
        #     # print(Customer)
        #     if FFRTByRD.objects.filter(**check_dic_Pro).first():
        #         FFRTByRDinfo = FFRTByRD.objects.filter(**check_dic_Pro).first()
        #         rdchangelist = [
        #             {"Functionteam":"EC","Quantity":FFRTByRDinfo.EC},
        #                       {"Functionteam":"RF","Quantity":FFRTByRDinfo.RF},
        #                       {"Functionteam":"EMI","Quantity":FFRTByRDinfo.EMI},
        #                       {"Functionteam": "ESD", "Quantity": FFRTByRDinfo.ESD},
        #                       {"Functionteam": "HW", "Quantity": FFRTByRDinfo.HW},
        #                       {"Functionteam":"SW","Quantity":FFRTByRDinfo.SW},
        #                       {"Functionteam":"SA","Quantity":FFRTByRDinfo.SA},
        #                       {"Functionteam": "SIT", "Quantity": FFRTByRDinfo.SIT},
        #                       {"Functionteam":"Thermal","Quantity":FFRTByRDinfo.Thermal},
        #                       {"Functionteam": "Power", "Quantity": FFRTByRDinfo.Power},
        #                       {"Functionteam": "SED", "Quantity": FFRTByRDinfo.SED},
        #         ]
        #     else:#没有则create空的
        #         createFFRT = {
        #             "Customer": Customer, "Project": Project, "EC": 0, "RF": 0, "EMI": 0, "ESD": 0, "HW": 0,
        #             "SW": 0, "SA": 0, "SIT": 0, "Thermal": 0, "Power": 0, "SED": 0,
        #         }
        #         FFRTByRD.objects.create(**createFFRT)
        #         FFRTByRDinfo = FFRTByRD.objects.filter(**check_dic_Pro).first()
        #         rdchangelist = [
        #             {"Functionteam": "EC", "Quantity": FFRTByRDinfo.EC},
        #             {"Functionteam": "RF", "Quantity": FFRTByRDinfo.RF},
        #             {"Functionteam": "EMI", "Quantity": FFRTByRDinfo.EMI},
        #             {"Functionteam": "ESD", "Quantity": FFRTByRDinfo.ESD},
        #             {"Functionteam": "HW", "Quantity": FFRTByRDinfo.HW},
        #             {"Functionteam": "SW", "Quantity": FFRTByRDinfo.SW},
        #             {"Functionteam": "SA", "Quantity": FFRTByRDinfo.SA},
        #             {"Functionteam": "SIT", "Quantity": FFRTByRDinfo.SIT},
        #             {"Functionteam": "Thermal", "Quantity": FFRTByRDinfo.Thermal},
        #             {"Functionteam": "Power", "Quantity": FFRTByRDinfo.Power},
        #             {"Functionteam": "SED", "Quantity": FFRTByRDinfo.SED},
        #         ]
        #
        #     canEdit = 0
        #     current_user = request.session.get('user_name')
        #     if TestProjectSW.objects.filter(**check_dic_Pro).first():
        #         for h in TestProjectSW.objects.filter(**check_dic_Pro):
        #             for i in h.Owner.all():
        #                 # print(i.username,current_user)
        #                 # print(type(i.username),type(current_user))
        #                 if i.username == current_user:
        #                     canEdit = 1
        #                     break
        # if request.POST.get("isGetData") == "SAVE":
        #     Customer = request.POST.get("Customer")
        #     Project = request.POST.get("Project")
        #     check_dic_Pro = {"Customer": Customer, "Project": Project}
        #     FunctionTeam = request.POST.get("rows[Functionteam]")
        #     FunctionTeamValue = request.POST.get("rows[Quantity]")
        #     # print(Customer)
        #     updatedic = {}
        #     updatedic[FunctionTeam] = int(FunctionTeamValue)
        #     if FFRTByRD.objects.filter(**check_dic_Pro).first():#edit
        #         FFRTByRD.objects.filter(**check_dic_Pro).first()
        #         FFRTByRD.objects.filter(**check_dic_Pro).update(**updatedic)
        #
        #     FFRTByRDinfo = FFRTByRD.objects.filter(**check_dic_Pro).first()
        #     rdchangelist = [
        #                   {"Functionteam":"EC","Quantity":FFRTByRDinfo.EC},
        #                   {"Functionteam":"RF","Quantity":FFRTByRDinfo.RF},
        #                   {"Functionteam":"EMI","Quantity":FFRTByRDinfo.EMI},
        #                   {"Functionteam": "ESD", "Quantity": FFRTByRDinfo.ESD},
        #                   {"Functionteam": "HW", "Quantity": FFRTByRDinfo.HW},
        #                   {"Functionteam":"SW","Quantity":FFRTByRDinfo.SW},
        #                   {"Functionteam":"SA","Quantity":FFRTByRDinfo.SA},
        #                   {"Functionteam": "SIT", "Quantity": FFRTByRDinfo.SIT},
        #                   {"Functionteam":"Thermal","Quantity":FFRTByRDinfo.Thermal},
        #                   {"Functionteam": "Power", "Quantity": FFRTByRDinfo.Power},
        #                   {"Functionteam": "SED", "Quantity": FFRTByRDinfo.SED},
        #     ]
        #     #試試渲染圖表，需要save是返回最新的數據
        #     Time_key = []
        #     if TestProjectSW.objects.filter(**check_dic_Pro).first():  # 至少存在一个Phase
        #         for h in TestProjectSW.objects.filter(**check_dic_Pro).values("Phase").order_by("-ScheduleEnd"):
        #             Time_key.append(h["Phase"])
        #
        #         Time_value_Re = []
        #         Time_value_Re_ATO = []
        #
        #         for i in Time_key:
        #             check_dic = {"Customer": Customer, "Project": Project, "Phase": i}
        #             # print(check_dic)
        #             Projectinfo = TestProjectSW.objects.filter(**check_dic).first()
        #             CRTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigRetestTime'))
        #             ATOsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('AttendTimeOptimize'))
        #             CATsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigAutomationTime'))
        #             CLTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigLeverageTime'))
        #             CSTsum = TestPlanSW.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigSmartTime'))
        #             if CRTsum["ConfigRetestTime__sum"]:
        #                 CRTtotal = CRTsum["ConfigRetestTime__sum"]
        #             else:
        #                 CRTtotal = 0
        #             if ATOsum["AttendTimeOptimize__sum"]:
        #                 ATOtotal = ATOsum["AttendTimeOptimize__sum"]
        #             else:
        #                 ATOtotal = 0
        #             Time_value_Re.append(round(CRTtotal / 60, 0))
        #             Time_value_Re_ATO.append(round(ATOtotal / 60, 0))
        #         Project_ReTotal = 0
        #         for i in Time_value_Re:
        #             Project_ReTotal += i
        #         Time_value_Re.append(round(Project_ReTotal, 0))
        #         Project_ATOTotal = 0
        #         for i in Time_value_Re_ATO:
        #             Project_ATOTotal += i
        #         Time_value_Re_ATO.append(round(Project_ATOTotal, 0))
        #         Time_key.append("Total")
        #         Sums1["Time_value"] = [Time_value_Re, Time_value_Re_ATO]
        #         Sums1["Time_key"] = Time_key
        #
        #
        #
        #
        #
        #     if FFRTByRD.objects.filter(**check_dic_Pro).first():
        #         FFRTByRDinfo = FFRTByRD.objects.filter(**check_dic_Pro).first()
        #         Quantity_dic = {"EC": FFRTByRDinfo.EC, "RF": FFRTByRDinfo.RF, "EMI": FFRTByRDinfo.EMI,
        #                         "ESD": FFRTByRDinfo.ESD,
        #                         "HW": FFRTByRDinfo.HW, "SW": FFRTByRDinfo.SW, "SA": FFRTByRDinfo.SA,
        #                         "SIT": FFRTByRDinfo.SIT,
        #                         "Thermal": FFRTByRDinfo.Thermal, "Power": FFRTByRDinfo.Power, "SED": FFRTByRDinfo.SED, }
        #
        #         TOP_list = sorted(Quantity_dic.items(), key=lambda x: x[1], reverse=False)[-6:]
        #         Quantity_top6_key = []
        #         Quantity_top6_value = []
        #         for i in TOP_list:
        #             Quantity_top6_value.append(i[1])
        #             Quantity_top6_key.append(i[0])
        #         Sums1["Quantity_top6_value"] = Quantity_top6_value
        #         Sums1["Quantity_top6_key"] = Quantity_top6_key
        #
        #     canEdit = 0
        #     current_user = request.session.get('user_name')
        #     if TestProjectSW.objects.filter(**check_dic_Pro).first():
        #         for h in TestProjectSW.objects.filter(**check_dic_Pro):
        #             for i in h.Owner.all():
        #                 # print(i.username,current_user)
        #                 # print(type(i.username),type(current_user))
        #                 if i.username == current_user:
        #                     canEdit = 1
        #                     break
        data = {
            "content": newContents,
            "SKU": SKU,
            "canEdit1": canEdit,
            "Sum": Sums,
            "Sum1": Sums1,
            "select1": selectItem,
            "proinfomation": proinfomation,
            "rdchangelist": rdchangelist,
            'canExport': canExport,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'TestPlanSW/TestPlanSW_search.html', locals())

def ItemSW_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Itemload"

    SWItem_lists = [{'Customer':'Customer','Phase':'Phase','ItemNo_d': 'ItemNo', 'Item_d': 'Item','TestItems':'TestItems'}]

    message_err = 0
    # print(request.POST,request.method)
    if request.method == "POST":
        # print(request.POST)
        if 'type' in request.POST:
            err_ok = 0
            xlsxlist = request.POST.get('upload')
            # print (simplejson.loads(xlsxlist))
            n=0
            j=0
            k=0

            for i in simplejson.loads(xlsxlist):
                n+=1
                SWItem_dic = {}
                # print(n,i)
                # print (i['Customer'])
                if 'TestItems' in i.keys():
                    check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d'],'TestItems':i['TestItems']}
                else:
                    check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['ItemNo_d'], 'Item_d': i['Item_d']}
                # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                # print(check_dic)
                check_list = TestItemSW.objects.filter(**check_dic).first()
                # print (check_list)
                if check_list:
                    # print (check_list)
                    j+=1
                    # err_ok = 1
                    SWItem_dic['Customer']=i['Customer']
                    SWItem_dic['Phase'] = i['Phase']
                    SWItem_dic['ItemNo_d'] = i['ItemNo_d']
                    SWItem_dic['Item_d'] = i['Item_d']
                    if 'TestItems' in i.keys():
                        SWItem_dic['TestItems'] = i['TestItems']
                    SWItem_lists.append(SWItem_dic)
                    # print(SWItem_dic)
                    Itemmodel = TestItemSW.objects.get(id=check_list.id)
                    # print(Itemmodel,type(Itemmodel))
                    if 'Customer' in i.keys():
                        Itemmodel.Customer = i['Customer']
                    if 'Phase' in i.keys():
                        Itemmodel.Phase = i['Phase']
                    if 'ItemNo_d' in i.keys():
                        Itemmodel.ItemNo_d = i['ItemNo_d']
                    if 'Item_d' in i.keys():
                        Itemmodel.Item_d = i['Item_d']
                    if 'TestItems' in i.keys():
                        Itemmodel.TestItems = i['TestItems']
                    if 'Category' in i.keys():
                        Itemmodel.Category = i['Category']
                    if 'Category2' in i.keys():
                        Itemmodel.Category2 = i['Category2']
                    if 'Version' in i.keys():
                        Itemmodel.Version = i['Version']
                    if 'ReleaseDate' in i.keys():
                        # print(i['Release_date'])
                        Itemmodel.ReleaseDate = i['ReleaseDate']
                    if 'Owner' in i.keys():
                        Itemmodel.Owner = i['Owner']
                    if 'Priority' in i.keys():
                        Itemmodel.Priority = i['Priority']
                    if 'TDMSTotalTime' in i.keys():
                        if i['TDMSTotalTime']:
                            Itemmodel.TDMSTotalTime = float(i['TDMSTotalTime'])
                    else:
                        Itemmodel.TDMSTotalTime =None
                    if 'BaseTime' in i.keys():
                        # print(i['Base_time'])
                        if i['BaseTime']:
                            Itemmodel.BaseTime = float(i['BaseTime'])
                    else:
                        Itemmodel.BaseTime =None
                    if 'TDMSUnattendedTime' in i.keys():
                        if i['TDMSUnattendedTime']:
                            Itemmodel.TDMSUnattendedTime = float(i['TDMSUnattendedTime'])
                    else:
                        Itemmodel.TDMSUnattendedTime =None
                    if 'BaseAotomationTime1SKU' in i.keys():
                        if i['BaseAotomationTime1SKU']:
                            Itemmodel.BaseAotomationTime1SKU = float(i['BaseAotomationTime1SKU'])
                    else:
                        Itemmodel.BaseAotomationTime1SKU =None
                    if 'Chramshell' in i.keys():
                        Itemmodel.Chramshell = i['Chramshell']
                    if 'ConvertibaleNBMode' in i.keys():
                        Itemmodel.ConvertibaleNBMode = i['ConvertibaleNBMode']
                    if 'ConvertibaleYogaPadMode' in i.keys():
                        Itemmodel.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                    if 'DetachablePadMode' in i.keys():
                        Itemmodel.DetachablePadMode = i['DetachablePadMode']
                    if 'DetachableWDockmode' in i.keys():
                        Itemmodel.DetachableWDockmode = i['DetachableWDockmode']
                    if 'PhaseFVT' in i.keys():
                        Itemmodel.PhaseFVT = i['PhaseFVT']
                        # print(i['FVT'])
                        # print(Itemmodel.PhaseFVT)
                    if 'PhaseSIT' in i.keys():
                        Itemmodel.PhaseSIT = i['PhaseSIT']
                    if 'PhaseFFRT' in i.keys():
                        Itemmodel.PhaseFFRT = i['PhaseFFRT']
                    if 'Coverage' in i.keys():
                        Itemmodel.Coverage = i['Coverage']
                    # print(i)
                    Itemmodel.save()
                    continue
                else:
                    # print('save')
                    # print(i)
                    k+=1
                    Itemmodel = TestItemSW()
                    if 'Customer' in i.keys():
                        Itemmodel.Customer = i['Customer']
                    if 'Phase' in i.keys():
                        Itemmodel.Phase = i['Phase']
                    if 'ItemNo_d' in i.keys():
                        Itemmodel.ItemNo_d = i['ItemNo_d']
                    if 'Item_d' in i.keys():
                        Itemmodel.Item_d = i['Item_d']
                    if 'TestItems' in i.keys():
                        Itemmodel.TestItems = i['TestItems']
                    if 'Category' in i.keys():
                        Itemmodel.Category = i['Category']
                    if 'Category2' in i.keys():
                        Itemmodel.Category2 = i['Category2']
                    if 'Version' in i.keys():
                        Itemmodel.Version = i['Version']
                    if 'ReleaseDate' in i.keys():
                        Itemmodel.ReleaseDate = i['ReleaseDate']
                    if 'Owner' in i.keys():
                        Itemmodel.Owner = i['Owner']
                    if 'Priority' in i.keys():
                        Itemmodel.Priority = i['Priority']
                    if 'TDMSTotalTime' in i.keys():
                        if i['TDMSTotalTime']:
                            Itemmodel.TDMSTotalTime = float(i['TDMSTotalTime'])
                    else:
                        Itemmodel.TDMSTotalTime = None
                    if 'BaseTime' in i.keys():
                        # print(i['Base_time'])
                        if i['BaseTime']:
                            Itemmodel.BaseTime = float(i['BaseTime'])
                    else:
                        Itemmodel.BaseTime = None
                    if 'TDMSUnattendedTime' in i.keys():
                        if i['TDMSUnattendedTime']:
                            Itemmodel.TDMSUnattendedTime = float(i['TDMSUnattendedTime'])
                    else:
                        Itemmodel.TDMSUnattendedTime = None
                    if 'BaseAotomationTime1SKU' in i.keys():
                        if i['BaseAotomationTime1SKU']:
                            Itemmodel.BaseAotomationTime1SKU = float(i['BaseAotomationTime1SKU'])
                    else:
                        Itemmodel.BaseAotomationTime1SKU = None
                    if 'Chramshell' in i.keys():
                        Itemmodel.Chramshell = i['Chramshell']
                    if 'ConvertibaleNBMode' in i.keys():
                        Itemmodel.ConvertibaleNBMode = i['ConvertibaleNBMode']
                    if 'ConvertibaleYogaPadMode' in i.keys():
                        Itemmodel.ConvertibaleYogaPadMode = i['ConvertibaleYogaPadMode']
                    if 'DetachablePadMode' in i.keys():
                        Itemmodel.DetachablePadMode = i['DetachablePadMode']
                    if 'DetachableWDockmode' in i.keys():
                        Itemmodel.DetachableWDockmode = i['DetachableWDockmode']
                    if 'PhaseFVT' in i.keys():
                        Itemmodel.PhaseFVT = i['PhaseFVT']
                    if 'PhaseSIT' in i.keys():
                        Itemmodel.PhaseSIT = i['PhaseSIT']
                    if 'PhaseFFRT' in i.keys():
                        Itemmodel.PhaseFFRT = i['PhaseFFRT']
                    if 'Coverage' in i.keys():
                        Itemmodel.Coverage = i['Coverage']
                    Itemmodel.save()
                    # print('ttt')
            # if not message_CDM:
            #     message_CDM = "Upload Successfully"
            # print(message_CDM)
            print(n,j,k)
            datajason={
                'err_ok':err_ok,
                'content': SWItem_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")

    return render(request, 'TestPlanSW/itemuploadSW.html', locals())

@csrf_exempt
def TestPlanSW_Edit_AIO(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Edit"
    # MockData = [
    #             # {"caseid": "Basic", "contents": [
    #             #     {"id": 20191210, "caseid": "BFA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "unattendedtime": 695,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191211, "caseid": "BFA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 400, "unattendedtime": 400,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191212, "caseid": "BFA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 500, "unattendedtime": 500,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191213, "caseid": "BFA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 600, "unattendedtime": 600,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191214, "caseid": "BFA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 700, "unattendedtime": 700,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191215, "caseid": "BFA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 800, "unattendedtime": 800,
    #             #      "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X", "detach_Pad": "X", "detach_W": "X",
    #             #      "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete", "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Interaction", "contents": [
    #             #     {"id": 20191216, "caseid": "IAA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 10,
    #             #      "unattendedtime": 10, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191217, "caseid": "IAA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 20,
    #             #      "unattendedtime": 20, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191218, "caseid": "IAA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 30,
    #             #      "unattendedtime": 30, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191219, "caseid": "IAA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 40,
    #             #      "unattendedtime": 40, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191220, "caseid": "IAA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 50,
    #             #      "unattendedtime": 50, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191221, "caseid": "IAA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 60,
    #             #      "unattendedtime": 60, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Connectivity", "contents": [
    #             #     {"id": 20191222, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191223, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191224, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191225, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191226, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191227, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     ]},
    #             # {"caseid": "Process and Stroage", "contents": [
    #             #     {"id": 20191228, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191229, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191230, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191231, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191232, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191233, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Performance", "contents": [
    #             #     {"id": 20191234, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191235, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191236, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191237, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191238, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191239, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game Test", "contents": [
    #             #     {"id": 20191240, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191241, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191242, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191243, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191244, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191245, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Stress", "contents": [
    #             #     {"id": 20191246, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191247, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191248, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191249, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191250, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191251, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Application", "contents": [
    #             #     {"id": 20191252, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191253, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191254, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191255, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191256, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191257, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Compal internal", "contents": [
    #             #     {"id": 20191258, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191259, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191260, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191261, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191262, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191263, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Game unique", "contents": [
    #             #     {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Linux and DOS", "contents": [
    #             #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Accessories", "contents": [
    #             #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             # {"caseid": "Gaming Unique", "contents": [
    #             #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #             #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #             #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #             #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #             #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #             # ]},
    #             ]
    # newMockData = [
    #                #  {"caseid": "Game unique", "contents": [
    #                #      {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #      {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #       "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #       "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #       "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #       "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #  ]},
    #                # {"caseid": "Linux and DOS", "contents": [
    #                #     {"id": 20191270, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191271, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191272, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191273, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191274, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191275, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Accessories", "contents": [
    #                #     {"id": 20191276, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191277, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191278, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191279, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191280, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191281, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                # {"caseid": "Gaming Unique", "contents": [
    #                #     {"id": 20191282, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191283, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191284, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191285, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191286, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                #     {"id": 20191287, "caseid": "PFA005_15", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
    #                #      "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
    #                #      "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
    #                #      "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
    #                #      "planOptimize": [2, 1, 3, 4, 5, 3, 0]},
    #                # ]},
    #                ]
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "Category": "CTA001", "Test_Title": "BIOS SETUP(NoteBook)",
        #  "Sub_Test_Title": "3.1.5", "Test_Item": "", "Priority": "P1",
        #  "Release_Date": "2018/12/21", "Owner__contains": "DQA", "Attend_Time": 66, "Unattend_Time": 0, "Automation": 0,
        #  "Attend_Time_hrs": 1.1,
        #  "Unattend_Time_hrs": 0, "TUC": 1, "Smart_Item": "", "Cusumer": "V", "Commercial": "V", "SDV": "V", "SIT": "V",
        #  "Coverage": "All SKU", "FS": 0, "BTS": 90, "TE": "LUX", "schedule": "", "NUMX": "", "NUMX_TIME": "60",
        #  "NUMA": "", "CAT": "90", "NUML": "", "CLT": "10", "conSitemInAll": "",
        #  "CST": 59.79, "comments": "sdafghfraerwrfgthnrtrgnh", "proTS": "6", "ATO": "960",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"],
        #  "CRC": "", "CRS": "", "CRT": ""},
    ]
    title = [
             {"caseid": "01 System Unit For Test Perpare ", },
             {"caseid": "02 System Gerber Test", },
             {"caseid": "03 OS & Platform", },
             {"caseid": "04 Multi-Media", },
             {"caseid": "05 Standard Interface", },
             {"caseid": "06 Communication", },
             {"caseid": "07 Natural User Interface", },
             {"caseid": "08 Special Test", },
             {"caseid": "09 Sample Stability Test", },
             {"caseid": "10 APP", },
             {"caseid": "11 Common Stress", },
             {"caseid": "12 Common Stress_DCT", },
             ]
    SKU = [
           # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
           # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
           # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
           # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
           # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
           # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
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
    customerOptions = [
        {"label": "C38(AIO)", "value": "C38(AIO)"},
    ]
    Customer_list = TestProjectSWAIO.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSWAIO.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSWAIO.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(SDV)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "Wave2":
                    PhaseValue = 2
                if m['Phase'] == "Wave3":
                    PhaseValue = 3
                if m['Phase'] == "EELP+":
                    PhaseValue = 4
                if m['Phase'] == "OOC":
                    PhaseValue = 5
                if m['Phase'] == "OOC2":
                    PhaseValue = 6
                if m['Phase'] == "OOC3":
                    PhaseValue = 7
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
            combine[i['Customer']] = Customerlist
    # print (request.method)
    # print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    # print(request.method)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            # print(combine)
            # print(TestPlanSWAIO._meta.fields)
            # for i in TestPlanSWAIO._meta.fields:
            #     print(i.name)
            return HttpResponse(json.dumps(combine), content_type="application/json")
        elif request.GET.get("action") == "getCategory":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'



            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # func = lambda z: dict([(x, y) for y, x in z.items()])

            if TestPlanSWAIO.objects.filter(Projectinfo=Projectinfos).first():
                title = []
                for i in TestPlanSWAIO.objects.filter(Projectinfo=Projectinfos).values("Category").distinct().order_by("Category"):
                    title.append({"caseid": i['Category']})
            updateData = {
                "MockData": title,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        # elif request.GET.get("action") == "search":
        #     # if request.GET.get("customer") == "C38(NB)":
        #         Customer = request.GET.get('customer')
        #         Project = request.GET.get('project')
        #         Phase = request.GET.get('phase')
        #         # print(type(Phase))
        #         if Phase == '0':
        #             Phase = 'B(FVT)'
        #         if Phase == '1':
        #             Phase = 'C(SIT)'
        #         if Phase == '2':
        #             Phase = 'FFRT'
        #         if Phase == '3':
        #             Phase = 'Others'
        #         dic_Item=     {'Customer': Customer, 'Phase': Phase}
        #         dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #         # print(dic_Project)
        #         Projectinfos = TestProjectSW.objects.filter(**dic_Project).first()
        #         # print(Projectinfos.Owner.all())
        #         # print(Projectinfos)
        #         canEdit = 0
        #         current_user = request.session.get('user_name')
        #         if Projectinfos:
        #             for i in Projectinfos.Owner.all():
        #                 # print(i.username,current_user)
        #                 # print(type(i.username),type(current_user))
        #                 if i.username == current_user:
        #                     canEdit = 1
        #                     break
        #             SKUlist=[Projectinfos.SKU1,Projectinfos.SKU2,Projectinfos.SKU3,Projectinfos.SKU4,Projectinfos.SKU5,
        #                       Projectinfos.SKU6,Projectinfos.SKU7,Projectinfos.SKU8,Projectinfos.SKU9,Projectinfos.SKU10,
        #                       Projectinfos.SKU11,Projectinfos.SKU12,Projectinfos.SKU13,Projectinfos.SKU14,Projectinfos.SKU15,
        #                       Projectinfos.SKU16,Projectinfos.SKU17,Projectinfos.SKU18,Projectinfos.SKU19,Projectinfos.SKU20]
        #             n=1
        #             for i in SKUlist:
        #                 if i:
        #                     SKUno='SKU%s'%n
        #                     SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
        #                     n+=1
        #         # print(SKU)
        #         if canEdit:
        #             itemlist = []
        #             for i in TestItemSW.objects.filter(Customer=Customer,Phase=Phase):
        #                 itemlist.append(i.id)
        #             # print (itemlist,'yyy')
        #             existitem = []
        #             for i in Projectinfos.testplansw_set.all():
        #                 existitem.append(i.Items.id)
        #             # print(existitem)
        #             for i in itemlist:
        #                 if i in existitem:
        #                     continue
        #                 else:
        #                     # print(TestProjectSW.objects.filter(**dic_Project).first())
        #                     TestPlanSW.objects.create(Items=TestItemSW.objects.get(id=i),
        #                                               Projectinfo=TestProjectSW.objects.filter(**dic_Project).first())
        #             # print (TestItemSW.objects.all().values('Category2').distinct().count())
        #         m=0
        #         for i in TestItemSW.objects.filter(**dic_Item).values('Category2').distinct():
        #             # print(type(i),i)
        #             title.append({"caseid": i['Category2'], 'hasChildren': 'true'})
        #             m+=1
        #         dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
        #         if RetestItemSW.objects.filter(**dic_Project).first():
        #             title.append({"caseid": "Others (Project Leader update)(1. Base on Golden BIOS/Image's change list)(2. Retest for w/o solution's issue ) for full function test"})
        #         # print(title)
        #
        #
        #         updateData = {
        #             "MockData": title,
        #             "SKU": SKU,
        #             "selectMsg": combine,
        #             "canEdit": canEdit
        #         }
        #         return HttpResponse(json.dumps(updateData), content_type="application/json")

        elif request.GET.get("action") == "getContent":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category=request.GET.get('category')
            # print(Category2)
            #Search的时候不需要知道Items是link那个Item的，读的都是TestPlan里面的测试当下的Item信息，并且创建时可能就没有Link case（比如测试当下的版本不是上传时的最新版本，因为现在只有excel才能创建PLan）
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'

            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1

            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}

            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Iteminfos)
            # print(Projectinfos)
            dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category': Category, "Projectinfo": Projectinfos}
            # print(dicPlan)
            if Projectinfos:
                x = 0
                for i in TestPlanSWAIO.objects.filter(**dicPlan):
                    x += 1
                    # print(i,type(i))
                    # print(i.id)
                    planOptimize = []
                    SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                 "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                 "SKU10": i.SKU10,
                                 "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                 "SKU15": i.SKU15,
                                 "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                 "SKU20": i.SKU20}
                    for j in SKU:
                        if j["skuNo"] in SKUlist_T.keys():
                            planOptimize.append(SKUlist_T[j["skuNo"]])
                    # print(planOptimize)
                    # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                    newContents.append(
                        {"id": i.id, "Category": i.Category, "Test_Title": i.TestTitle,
                         "Sub_Test_Title": i.Subtesttitle, "Test_Item": i.TestItem, "Priority": i.Priority,
                         "Release_Date": i.ReleaseDate, "Owner": i.Owner, "Attend_Time": i.AT_AttendTime, "Unattend_Time": i.AT_UnattendTime,
                         "Automation": i.AT_Automation, "Attend_Time_hrs": i.DQMS_AttendTime,
                         "Unattend_Time_hrs": i.DQMS_UnattendTime, "TUC": i.TestUnitsConfig, "Smart_Item": i.SmartItem,
                         "Cusumer": i.Cusumer, "Commercial": i.Commercial,
                         "SDV": i.SDV, "SIT": i.SIT, "Coverage": i.Coverage, "FS": i.FeatureSupport, "BTS": i.Basetimesupport,
                         "TE": i.TE, "schedule": i.Schedule,
                         "NUMX": i.Configalltestunits, "NUMX_TIME": i.Configalltesttime, "NUMA": i.ConfigAutomationItem,
                         "CAT": i.ConfigAutomationtime, "NUML": i.ConfigLeverageItem, "CLT": i.ConfigLeveragetime,
                         "conSitemInAll": i.ConfigSmartItemper,
                         "CST": i.ConfigSmarttime, "comments": i.Comments, "proTS": i.ProjecttestSKUOptimize, "ATO": i.AttendtimeOptimize,
                         "planOptimize": planOptimize,
                         "CRC": i.ConfigRetestCycle, "CRS": i.ConfigRetestSKU, "CRT": i.ConfigRetesttime},)
                # print(newContents)
                # print(x)
        # print(newContents)
            updateData = {
                "content": newContents,
                "SKU": SKU,
                "canEdit": canEdit
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")

        elif request.GET.get("action") == "DeleteAll":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            Category=request.GET.get('category')
            # print(Category2)
            #Search的时候不需要知道Items是link那个Item的，读的都是TestPlan里面的测试当下的Item信息，并且创建时可能就没有Link case（比如测试当下的版本不是上传时的最新版本，因为现在只有excel才能创建PLan）
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'

            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            # Delete TestPlanSWAIO
            if Projectinfos:
                Deldic = {'Customer': Customer, 'Phase': Phase, "Projectinfo": Projectinfos}
                if TestPlanSWAIO.objects.filter(**Deldic):
                    # print(1)
                    TestPlanSWAIO.objects.filter(**Deldic).delete()
            # Searchs
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20]
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1

            # print(dicItem)
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}

            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Iteminfos)
            # print(Projectinfos)
            dicPlan = {'Customer': Customer, 'Phase': Phase, 'Category': Category, "Projectinfo": Projectinfos}
            # print(dicPlan)
            if Projectinfos:
                x = 0
                for i in TestPlanSWAIO.objects.filter(**dicPlan):
                    x += 1
                    # print(i,type(i))
                    # print(i.id)
                    planOptimize = []
                    SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                 "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                 "SKU10": i.SKU10,
                                 "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                 "SKU15": i.SKU15,
                                 "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                 "SKU20": i.SKU20}
                    for j in SKU:
                        if j["skuNo"] in SKUlist_T.keys():
                            planOptimize.append(SKUlist_T[j["skuNo"]])
                    # print(planOptimize)
                    # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                    newContents.append(
                        {"id": i.id, "Category": i.Category, "Test_Title": i.TestTitle,
                         "Sub_Test_Title": i.Subtesttitle, "Test_Item": i.TestItem, "Priority": i.Priority,
                         "Release_Date": i.ReleaseDate, "Owner": i.Owner, "Attend_Time": i.AT_AttendTime, "Unattend_Time": i.AT_UnattendTime,
                         "Automation": i.AT_Automation, "Attend_Time_hrs": i.DQMS_AttendTime,
                         "Unattend_Time_hrs": i.DQMS_UnattendTime, "TUC": i.TestUnitsConfig, "Smart_Item": i.SmartItem,
                         "Cusumer": i.Cusumer, "Commercial": i.Commercial,
                         "SDV": i.SDV, "SIT": i.SIT, "Coverage": i.Coverage, "FS": i.FeatureSupport, "BTS": i.Basetimesupport,
                         "TE": i.TE, "schedule": i.Schedule,
                         "NUMX": i.Configalltestunits, "NUMX_TIME": i.Configalltesttime, "NUMA": i.ConfigAutomationItem,
                         "CAT": i.ConfigAutomationtime, "NUML": i.ConfigLeverageItem, "CLT": i.ConfigLeveragetime,
                         "conSitemInAll": i.ConfigSmartItemper,
                         "CST": i.ConfigSmarttime, "comments": i.Comments, "proTS": i.ProjecttestSKUOptimize, "ATO": i.AttendtimeOptimize,
                         "planOptimize": planOptimize,
                         "CRC": i.ConfigRetestCycle, "CRS": i.ConfigRetestSKU, "CRT": i.ConfigRetesttime},)
                # print(newContents)
                # print(x)
        # print(newContents)
            updateData = {
                "content": newContents,
                "SKU": SKU,
                "canEdit": canEdit
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
            # if request.GET.get("contents") == "Basic":
            #     return HttpResponse(json.dumps(newContents), content_type="application/json")
            # if request.GET.get("contents") == "Interaction":
            #     return HttpResponse(json.dumps(newContents1), content_type="application/json")
            # if request.GET.get("contents") == "Connectivity":
            #     return HttpResponse(json.dumps(newContents2), content_type="application/json")

    if request.method == "POST":
        # print(request.POST)
        # print(request.body)
        if request.POST.get('action') == 'first':
            # print(combine)

            data = {
                'customerOptions': customerOptions,
                # 'canEdit': canEdit,
                "selectMsg": combine,
                "content": newContents,
                # "SKU": SKU,
                # "editResult": 1,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        if request.POST.get('action')=='edit':
            # print(request.POST)
            updatedate = {
                # 'FeatureSupport': request.POST.get('FS'), "BaseTimeSupport": request.POST.get('BTS'),
                #           "TE": request.POST.get('TE'),"Schedule": request.POST.get('schedule'),"ProjectTestSKUfollowMatrix":request.POST.get('starttime'),
                #           "TimewConfigFollowmatrix":request.POST.get('TFC'),"ConfigAutomationItem":request.POST.get('conAitem'),
                #           "ConfigAutomationTime":request.POST.get('CAT'),"ConfigLeverageItem":request.POST.get('conLitem'),
                #           "ConfigLeverageTime":request.POST.get('CLT'),"CommentsLeverage":request.POST.get('comments1'),
                #           "ConfigSmartItem":request.POST.get('conSitem'),"ConfigSmartItemPer":request.POST.get(''),
                          }
            Customer = request.POST.get('customer')
            Project = request.POST.get('project')
            Phase = request.POST.get('phase')
            # print(type(Phase))
            #edit时也不需要知道Items是link那个Item的，直接通过id查找的
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(float('1.1'))
            #print(float('NULL'))
            # print(float(''))#hui baocuo
            if 'FS' in request.POST.keys():
                updatedate['FeatureSupport']=request.POST.get('FS')
            if 'BTS' in request.POST.keys():
                updatedate['Basetimesupport'] = request.POST.get('BTS')
            if 'TE' in request.POST.keys():
                updatedate['TE'] = request.POST.get('TE')
            if 'NUMX_TIME' in request.POST.keys():
                updatedate['Configalltesttime'] = request.POST.get('NUMX_TIME')
            if 'NUMX' in request.POST.keys():
                updatedate['Configalltestunits'] = request.POST.get('NUMX')
            if 'schedule' in request.POST.keys():
                updatedate['Schedule'] = request.POST.get('schedule')
            if 'CAT' in request.POST.keys():
                updatedate['ConfigAutomationtime'] = request.POST.get('CAT')
            if 'CLT' in request.POST.keys():
                updatedate['ConfigLeveragetime'] = request.POST.get('CLT')
            if 'CST' in request.POST.keys():
                updatedate['ConfigSmarttime'] = request.POST.get('CST')
            if 'proTS' in request.POST.keys():
                updatedate['ProjecttestSKUOptimize'] = request.POST.get('proTS')
            if 'ATO' in request.POST.keys():
                updatedate['AttendtimeOptimize'] = request.POST.get('ATO')
            if 'comments' in request.POST.keys():
                updatedate['Comments'] = request.POST.get('comments')
            if 'CRC' in request.POST.keys():
                updatedate['ConfigRetestCycle'] = request.POST.get('CRC')
            if 'CRS' in request.POST.keys():
                updatedate['ConfigRetestSKU'] = request.POST.get('CRS')
            if 'CRT' in request.POST.keys():
                updatedate['ConfigRetesttime'] = request.POST.get('CRT')
            if 'conSitemInAll' in request.POST.keys():
                updatedate['ConfigSmartItemper'] = request.POST.get('conSitemInAll')
            updatedate['editor'] = request.session.get('user_name')
            updatedate['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if 'planOptimize' in request.POST.keys():
                # print('ppp')
                planOptimize = request.POST.getlist('planOptimize',[])
            # print(planOptimize,'111')

            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(dic_Project)
            # print (Projectinfos)
            if Projectinfos:
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20]
                # print(SKUlist)
                n = 1
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                    n += 1

            x=0
            # print(SKU)
            for k in SKU:
                updatedate[k["skuNo"]] = planOptimize[x]
                x+=1
            # print((updatedate))


            Category = request.POST.get('category')
            TestPlanSWAIO.objects.filter(id=request.POST.get('ID')).update(**updatedate)
            return HttpResponse(json.dumps({'editResult':1}), content_type="application/json")
        if 'ExcelData' in str(request.body):
            responseData = json.loads(request.body)
            xlsxlist = json.loads(responseData['ExcelData'])
            if responseData:
                # print(responseData)
                check_dic_list = []
                check_list_list = []
                Phase = responseData['phase']

                if Phase == '0':
                    Phase = 'B(SDV)'
                if Phase == '1':
                    Phase = 'C(SIT)'
                if Phase == '2':
                    Phase = 'Wave2'
                if Phase == '3':
                    Phase = 'Wave3'
                if Phase == '4':
                    Phase = 'EELP+'
                if Phase == '5':
                    Phase = 'OOC'
                if Phase == '6':
                    Phase = 'OOC2'
                if Phase == '7':
                    Phase = 'OOC3'

                dic_Project = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
                Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
                # print(dic_Project)
                # item_nodata = [{'Customer':'Customer','Phase':'Phase','Category': 'Category', 'TestTitle': 'TestTitle','Subtesttitle':'Subtesttitle',"TestItem":"TestItem"}]
                # item_changeddata = [{'Customer':'Customer','Phase':'Phase','Category': 'Category', 'TestTitle': 'TestTitle','Subtesttitle':'Subtesttitle',"TestItem":"TestItem"}]
                for i in xlsxlist:
                    # print(i)
                    #RetestFFRT
                    if 'Category' in i.keys():#转换的文档中最后会多一些空值
                        check_dic_inplan = {'Customer': responseData['customer'], 'Phase': Phase,
                                    'Category': i['Category'], 'TestTitle': i['TestTitle'], 'Subtesttitle': i['Subtesttitle'],
                                     'TestItem': i['TestItem']}
                        # check_dic = {'Customer':i['Customer'],'Phase':i['Phase'],'ItemNo_d': i['Case_ID'], 'Item_d': i['Case_Name'],'TestItems':i['Test_Items']}
                        # print(check_dic)
                        check_dic_inplan["Projectinfo"] = Projectinfos
                        check_list_plan = TestPlanSWAIO.objects.filter(**check_dic_inplan).first()
                        # print(check_list)
                        keywords = []
                        for j in TestPlanSWAIO._meta.fields:
                            # print(i.name)
                            if j.name != "Projectinfo" and j.name != "id":
                                keywords.append(j.name)

                        if check_list_plan:
                            # print(check_dic_inplan)
                            updatedic = {}
                            editplan = TestPlanSWAIO.objects.filter(**check_dic_inplan).first()
                            for m in keywords:
                                if m in i.keys():
                                    updatedic[m] = i[m]
                                else:
                                    updatedic[m] = ""
                            # if i['Category'] == "01 System Unit For Test Perpare ":
                            #     print("U",updatedic)
                            #     print(TestPlanSWAIO.objects.filter(**check_dic_inplan))
                            updatedic["editor"] = request.session.get('user_name')
                            updatedic["edit_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            TestPlanSWAIO.objects.filter(**check_dic_inplan).update(**updatedic)
                        else:#create

                            # print(itemsinfo)
                            updatedic = {}
                            # 由于需要转成float,所以即使excel中的key与models中的一样也不能用如下方式
                            # for j in i.keys():
                            #     updatedic[j]=i[j]
                            # updatedic['Project'] = responseData['project']
                            updatedic['Projectinfo'] = TestProjectSWAIO.objects.get(**dic_Project)
                            updatedic['editor'] = request.session.get('user_name')
                            updatedic['edit_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            updatedic["Customer"] = responseData['customer']
                            updatedic["Phase"] = Phase
                            # updatedic["Project"] = responseData['project']#TestPlan中没有这个key，只有Projectinfo，RetestItem里面才有
                            for m in keywords:
                                if m in i.keys():
                                    updatedic[m] = i[m]
                                else:
                                    updatedic[m] = ""
                                # if j =='DQMS_AttendTime':
                                #     print(i[j])
                            # print("C", updatedic)
                            TestPlanSWAIO.objects.create(**updatedic)

            Phase = responseData['phase']
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'
            dic_Project_search = {'Customer': responseData['customer'],
                               'Project': responseData['project'], 'Phase': Phase}
            # print(dic_Project)
            Projectinfos_search = TestProjectSWAIO.objects.filter(**dic_Project_search).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)
            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos_search:
                for k in Projectinfos_search.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if k.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos_search.SKU1, Projectinfos_search.SKU2, Projectinfos_search.SKU3, Projectinfos_search.SKU4,
                           Projectinfos_search.SKU5,
                           Projectinfos_search.SKU6, Projectinfos_search.SKU7, Projectinfos_search.SKU8, Projectinfos_search.SKU9,
                           Projectinfos_search.SKU10,
                           Projectinfos_search.SKU11, Projectinfos_search.SKU12, Projectinfos_search.SKU13, Projectinfos_search.SKU14,
                           Projectinfos_search.SKU15,
                           Projectinfos_search.SKU16, Projectinfos_search.SKU17, Projectinfos_search.SKU18, Projectinfos_search.SKU19,
                           Projectinfos_search.SKU20]
                n = 1
                for l in SKUlist:
                    if l:
                        # print(l)
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": l.split('/')[1], "CPU": l.split('/')[0]})
                    n += 1
            if TestPlanSWAIO.objects.filter(Projectinfo=Projectinfos).first():
                title = []
                for i in TestPlanSWAIO.objects.filter(Projectinfo=Projectinfos).values("Category").distinct().order_by("Category"):
                    title.append({"caseid": i['Category']})
            dicPlan = {'Customer': responseData['customer'], "Category":responseData['category'],
                           'Phase': Phase, "Projectinfo":Projectinfos}
            if Projectinfos:
                x = 0
                for i in TestPlanSWAIO.objects.filter(**dicPlan):
                    x += 1
                    # print(i,type(i))
                    # print(i.id)
                    planOptimize = []
                    SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                 "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                 "SKU10": i.SKU10,
                                 "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                 "SKU15": i.SKU15,
                                 "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                 "SKU20": i.SKU20}
                    for j in SKU:
                        if j["skuNo"] in SKUlist_T.keys():
                            planOptimize.append(SKUlist_T[j["skuNo"]])
                    # print(planOptimize)
                    # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                    newContents.append(
                        {"id": i.id, "Category": i.Category, "Test_Title": i.TestTitle,
                         "Sub_Test_Title": i.Subtesttitle, "Test_Item": i.TestItem, "Priority": i.Priority,
                         "Release_Date": i.ReleaseDate, "Owner": i.Owner, "Attend_Time": i.AT_AttendTime,
                         "Unattend_Time": i.AT_UnattendTime,
                         "Automation": i.AT_Automation, "Attend_Time_hrs": i.DQMS_AttendTime,
                         "Unattend_Time_hrs": i.DQMS_UnattendTime, "TUC": i.TestUnitsConfig, "Smart_Item": i.SmartItem,
                         "Cusumer": i.Cusumer, "Commercial": i.Commercial,
                         "SDV": i.SDV, "SIT": i.SIT, "Coverage": i.Coverage, "FS": i.FeatureSupport,
                         "BTS": i.Basetimesupport,
                         "TE": i.TE, "schedule": i.Schedule,
                         "NUMX": i.Configalltestunits, "NUMX_TIME": i.Configalltesttime, "NUMA": i.ConfigAutomationItem,
                         "CAT": i.ConfigAutomationtime, "NUML": i.ConfigLeverageItem, "CLT": i.ConfigLeveragetime,
                         "conSitemInAll": i.ConfigSmartItemper,
                         "CST": i.ConfigSmarttime, "comments": i.Comments, "proTS": i.ProjecttestSKUOptimize,
                         "ATO": i.AttendtimeOptimize,
                         "planOptimize": planOptimize,
                         "CRC": i.ConfigRetestCycle, "CRS": i.ConfigRetestSKU, "CRT": i.ConfigRetesttime}, )
                # print(newContents)
                # print(x)
            updateData = {
                "content": newContents,
                "MockData": title,
                "SKU": SKU,
                "selectMsg": combine,
                "canEdit": canEdit,
            }
            # print(updateData)
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        #update
    return render(request, 'TestPlanSW/TestPlanSW_edit_AIO.html', locals())
#TestPlan_ME search
@csrf_exempt
def TestPlanSW_search_AIO(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/SW/Search"
    # print(Skin)
    newContents = [
        # {"id": 20191264, "caseid": "CTA001", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191265, "caseid": "CTA002", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191266, "caseid": "CTA003", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695,
        #  "conAitem": 1, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 1, "CST": 80,"starttime":102,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191267, "caseid": "CTA004", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 1, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191268, "caseid": "CTA005", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #   "conAitem": 0,"BTS":10,"FS":0,"TE":'WILL',"schedule":'2020/1/2',"CAT":100,"conLitem":1,"CLT":100,"conSitem":0,"CST":80,
        #  "TFC":80,"comments1":"备注1","comments2":"备注2","proTS":55,"ATO":99,"CRC":12,"CRS":15,"CRT":19,"conSitemInAll":1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
        # {"id": 20191269, "caseid": "CTA006", "casename": "BIOS SETUP(NoteBook)", "version": "3.1.5",
        #  "releasedate": "2018/12/21", "owner": "DQA", "priority": "P1", "basetime": 695, "FS": 0, "starttime": 10,
        #  "conAitem": 0, "BTS": 10, "FS": 0, "TE": 'WILL', "schedule": '2020/1/2', "CAT": 100, "conLitem": 1, "CLT": 100,
        #  "conSitem": 0, "CST": 80,
        #  "TFC": 80, "comments1": "备注1", "comments2": "备注2", "proTS": 55, "ATO": 99, "CRC": 12, "CRS": 15, "CRT": 19,
        #  "conSitemInAll": 1,
        #  "unattendedtime": 695, "basetimeA": 0, "chramshell": "V", "conver_NB": "V", "conver_Yoga": "X",
        #  "detach_Pad": "X", "detach_W": "X", "PhaseF": "V", "PhaseS": "V", "coverage": "UMA&Discrete",
        #  "planOptimize": ["V", "X", "A", "L", "S", "L", "V", "A"]},
    ]
    canEdit = 0
    title = [
        # {"caseid": "Basic", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Interaction", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Connectivity", 'hasChildren': 'true',"unattendedtime": 6950, "basetimeA": 0,"basetime": 6950,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Process and Stroage", 'hasChildren': 'true',"unattendedtime": 6952, "basetimeA": 0,"basetime": 6952,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Performance", 'hasChildren': 'true',"unattendedtime": 6925, "basetimeA": 0,"basetime": 6925,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game Test", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6935,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Stress", 'hasChildren': 'true',"unattendedtime": 6395, "basetimeA": 0,"basetime": 6495,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Application", 'hasChildren': 'true',"unattendedtime": 6595, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Compal internal", 'hasChildren': 'true',"unattendedtime": 6975, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Game unique", 'hasChildren': 'true',"unattendedtime": 6957, "basetimeA": 0,"basetime": 6957,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Linux and DOS", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6695,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Accessories", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6975,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
        #      {"caseid": "Gaming Unique", 'hasChildren': 'true',"unattendedtime": 6795, "basetimeA": 0,"basetime": 6795,"BTS":33,"TFC":33,"CAT":33,"CLT":33,"CST":34,"ATO":55,"CRT":60},
    ]
    proinfomation = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    SKU = [
        # {"skuNo": "SKU1", "VGA": "UMA", "CPU": "i3-8145U"},
        # {"skuNo": "SKU2", "VGA": "N17S-G2-A1", "CPU": "i5-8265U"},
        # {"skuNo": "SKU2", "VGA": "UMA", "CPU": "i5-8265U"},
        # {"skuNo": "SKU3", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU4", "VGA": "Picasso", "CPU": "i7-8565U"}, {"skuNo": "SKU5", "VGA": "UMA", "CPU": "i7-8565U"},
        # {"skuNo": "SKU6", "VGA": "N17S-G2-A1", "CPU": "i7-8565U"},
        # {"skuNo": "SKU7", "VGA": "N17S-G0-A1", "CPU": "i7-8565U"}
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
    allSum = [
        # {"category": "1340", "basetime": "0", "BTS": "0", "TFC": "0", "CAT": "0", "CLT": "0", "CST": "0", "ATO": "0",
        #  "CRT": "0"},
        # {"category": "8", "basetime": "0", "BTS": "0", "TFC": "0", "CAT": "0", "CLT": "0", "CST": "0", "ATO": "0",
        #  "CRT": "0"},
        # {"category": "60", "basetime": "0", "BTS": "0", "TFC": "0", "CAT": "0", "CLT": "0", "CST": "0", "ATO": "0",
        #  "CRT": "0"},
        # {"category": "258", "basetime": "0", "BTS": "0", "TFC": "0", "CAT": "0", "CLT": "0", "CST": "0", "ATO": "0",
        #  "CRT": "0"},
        # {"category": "154", "basetime": "0", "BTS": "0", "TFC": "0", "CAT": "0", "CLT": "0", "CST": "0", "ATO": "0",
        #  "CRT": "0"}
    ]
    Sums = {
        # 'basetimeSum': 6000, 'unattendtimeSum': 5000, 'basetimeASum': 1000, 'BTSSum': 1299, 'TFCSum': 1999,
        #     'CATSum': 34556, 'CLTSum': 235, 'CSTSum': 5678, 'ATOSum': 9870, 'CRTSum': 2342
    }
    Sums1 = {
        # "Testahour_value": [[1527, 1483, 344, 1971, 2103, 1493, 1000], [1463, 1443, 111, 2564, 2103, 1493, 1000]],
        # "Testahour_key": ["FVT Config-Retest time", "SIT Config-Retest time", "FFRT Config-Retest time",
        #                   "FVT Attend Time", "SIT Attend Time", "FFRT 1st Attend Time", "FFRT 2nd Attend Time"],
        # "SaveTime_value": [[1001, 1003, 11002, 1006], [1527, 1483, 344, 1971], [2456, 767, 433, 2335]],
        # 'SaveTime_key': ['FFRT', 'SIT', 'FVT', 'TOTAL']
    }
    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]
    rdchangelist = [
        # {"Functionteam":"EC Team","Quantity":"1"},
        #           {"Functionteam":"RF","Quantity":"1"},
        #           {"Functionteam":"EMI","Quantity":"1"},
        #           {"Functionteam":"SW Team","Quantity":"2"},
        #           {"Functionteam":"SA Team","Quantity":"3"},
        #           {"Functionteam":"Thermal Team","Quantity":"4"}
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
    Customer_list = TestProjectSWAIO.objects.all().values('Customer').distinct().order_by('Customer')
    for i in Customer_list:
        Customerlist = []
        for j in TestProjectSWAIO.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectSWAIO.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(SDV)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "Wave2":
                    PhaseValue = 2
                if m['Phase'] == "Wave3":
                    PhaseValue = 3
                if m['Phase'] == "EELP+":
                    PhaseValue = 4
                if m['Phase'] == "OOC":
                    PhaseValue = 5
                if m['Phase'] == "OOC2":
                    PhaseValue = 6
                if m['Phase'] == "OOC3":
                    PhaseValue = 7
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    for i in TestProjectSWAIO.objects.all().values("Customer").distinct().order_by("Customer"):
        selectItem.append(i["Customer"])
    # print (request.method)
    # print(request.GET,request.GET.get("action"),request.POST)
    # print(request.body)
    # print(request.method)
    if request.method == "GET":
        if request.GET.get("action") == "first":
            return HttpResponse(json.dumps(combine), content_type="application/json")
        if request.GET.get("action") == "getContent":
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')

            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'

            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectSWAIO.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            # print(Projectinfos)

            canEdit = 0
            current_user = request.session.get('user_name')
            if Projectinfos:
                for i in Projectinfos.Owner.all():
                    # print(i.username,current_user)
                    # print(type(i.username),type(current_user))
                    if i.username == current_user:
                        canEdit = 1
                        break
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3, Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8, Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13, Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18, Projectinfos.SKU19,
                           Projectinfos.SKU20]
                n = 1
                skuSHU = 0
                for i in SKUlist:
                    if i:
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": i.split('/')[1], "CPU": i.split('/')[0]})
                        skuSHU += 1
                    n += 1


            # dic_ItemSum = {'Customer': Customer, 'Phase': PhaseinItem[0]}
            dic_ProjectSum = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            ProjectSum = TestProjectSWAIO.objects.filter(**dic_ProjectSum).first()
            basetimesum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").values('Category').annotate(
                Sum('AT_AttendTime')).order_by('Category')
            # basetimesumtotal = TestPlanSW.objects.filter(Projectinfo=ProjectSum).aggregate(
            #     Sum('BaseTime'))
            # print(basetimesum,'yy')
            # print(basetimesumtotal)
            BTSsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('Basetimesupport')).order_by('Category')
            TFCsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('Configalltesttime')).order_by('Category')
            CATsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('ConfigAutomationtime')).order_by('Category')
            CLTsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('ConfigLeveragetime')).order_by('Category')
            CSTsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('ConfigSmarttime')).order_by('Category')
            ATOsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('AttendtimeOptimize')).order_by('Category')
            CRTsum = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).values('Category').annotate(
                Sum('ConfigRetesttime')).order_by('Category')
            Num = 0
            for i in basetimesum:
                # print(i)
                allSum.append({'category': i['Category'], 'basetime': round(i['AT_AttendTime__sum'] / 60, 0), 'BTS': round(BTSsum[Num]['Basetimesupport__sum'] / 60, 0),
                               'TFC': round(TFCsum[Num]['Configalltesttime__sum'] / 60, 0), 'CAT': round(CATsum[Num]['ConfigAutomationtime__sum'] / 60, 0),
                               'CLT': round(CLTsum[Num]['ConfigLeveragetime__sum'] / 60, 0), 'CST': round(CSTsum[Num]['ConfigSmarttime__sum'] / 60, 0),
                               'ATO': round(ATOsum[Num]['AttendtimeOptimize__sum'] / 60, 0), 'CRT': round(CRTsum[Num]['ConfigRetesttime__sum'] / 60, 0),
                               })
                Num += 1
            basetimesumTotal = TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").values('Category').annotate(
                Sum('AT_AttendTime')).order_by('Category')
            allSum.insert(0, {'category': 'Total',
                              'basetime': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum, Owner__contains="DQA").aggregate(Sum('AT_AttendTime'))['AT_AttendTime__sum']/60, 0),
                              'BTS': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('Basetimesupport'))['Basetimesupport__sum']/60, 0),
                              'TFC': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('Configalltesttime'))['Configalltesttime__sum']/60, 0),
                              'CAT': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigAutomationtime'))['ConfigAutomationtime__sum']/60, 0),
                              'CLT': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigLeveragetime'))['ConfigLeveragetime__sum']/60, 0),
                              'CST': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigSmarttime'))['ConfigSmarttime__sum']/60, 0),
                              'ATO': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('AttendtimeOptimize'))['AttendtimeOptimize__sum']/60, 0),
                              'CRT': round(TestPlanSWAIO.objects.filter(Projectinfo=ProjectSum).aggregate(Sum('ConfigRetesttime'))['ConfigRetesttime__sum']/60, 0),
                              # 'HC': round(HC_Total, 2), 'HCOT': round(HCOT_Total, 2)
                              }
                          )
            data = {
                "content": newContents,
                "SKU": SKU,
                'skuSHU': skuSHU,
                "canEdit1": canEdit,
                "Sum": Sums,
                "Sum1": Sums1,
                "allSum": allSum,
                "select1": selectItem,
                "proinfomation": proinfomation,
                "rdchangelist": rdchangelist,
                "canExport": canExport,
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            selectItem
        if request.POST.get("isGetData") == "searchalert":
            Customer = request.POST.get("Customer")
            Prolist = []
            # print(Customer)
            if Customer:
                for i in TestProjectSWAIO.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append({"Project": i["Project"]})
            else:
                for i in TestProjectSWAIO.objects.all().values("Project").distinct().order_by("Project"):
                    Prolist.append({"Project": i["Project"]})
            # print(Prolist)
            for i in Prolist:
                # print(i)
                if ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first():
                    # print(ProjectinfoinDCT.objects.filter(ComPrjCode=i).first())
                    proinfomation.append({
                        "id": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().id,
                        "YEAR": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Year,
                        "COMPRJCODE": i["Project"],
                        # "PHASE": i["Phase"],
                        "PrjEngCode1": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode1,
                        "PrjEngCode2": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PrjEngCode2,
                        "PROJECT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().ProjectName,
                        "SIZE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Size,
                        "CPU": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CPU,
                        "PLATFORM": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Platform,
                        "VGA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().VGA,
                        "OSSUPPORT": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().OSSupport,
                        "Type": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().Type,
                        "PPA": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PPA,
                        "PQE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().PQE,
                        "SS": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().SS,
                        "LD": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().LD,
                        "DQAPL": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().DQAPL,
                    })
                else:
                    # print(i)
                    if len(i['Project']) > 5:
                        Prostr1 = i['Project'][0:5]
                        Prostr2 = i['Project'][0:3] + i['Project'][5:]
                        Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                        Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                        if Proinfo1 and Proinfo2:
                            if Proinfo1.Year == Proinfo2.Year:
                                Year = Proinfo1.Year
                            else:
                                Year = Proinfo1.Year + "/" + Proinfo2.Year
                            if Proinfo1.PrjEngCode1 == Proinfo2.PrjEngCode1:
                                PrjEngCode1 = Proinfo1.PrjEngCode1
                            else:
                                PrjEngCode1 = Proinfo1.PrjEngCode1 + "/" + Proinfo2.PrjEngCode1
                            if Proinfo1.PrjEngCode2 == Proinfo2.PrjEngCode2:
                                PrjEngCode2 = Proinfo1.PrjEngCode2
                            else:
                                PrjEngCode2 = Proinfo1.PrjEngCode2 + "/" + Proinfo2.PrjEngCode2
                            if Proinfo1.ProjectName == Proinfo2.ProjectName:
                                ProjectName = Proinfo1.ProjectName
                            else:
                                ProjectName = Proinfo1.ProjectName + "/" + Proinfo2.ProjectName
                            if Proinfo1.Size == Proinfo2.Size:
                                Size = Proinfo1.Size
                            else:
                                Size = Proinfo1.Size + "/" + Proinfo2.Size
                            if Proinfo1.CPU == Proinfo2.CPU:
                                CPU = Proinfo1.CPU
                            else:
                                CPU = Proinfo1.CPU + "/" + Proinfo2.CPU
                            if Proinfo1.Platform == Proinfo2.Platform:
                                Platform = Proinfo1.Platform
                            else:
                                Platform = Proinfo1.Platform + "/" + Proinfo2.Platform
                            if Proinfo1.VGA == Proinfo2.VGA:
                                VGA = Proinfo1.VGA
                            else:
                                VGA = Proinfo1.VGA + "/" + Proinfo2.VGA
                            if Proinfo1.OSSupport == Proinfo2.OSSupport:
                                OSSupport = Proinfo1.OSSupport
                            else:
                                OSSupport = Proinfo1.OSSupport + "/" + Proinfo2.OSSupport
                            if Proinfo1.Type == Proinfo2.Type:
                                Type = Proinfo1.Type
                            else:
                                Type = Proinfo1.Type + "/" + Proinfo2.Type
                            if Proinfo1.PPA == Proinfo2.PPA:
                                PPA = Proinfo1.PPA
                            else:
                                PPA = Proinfo1.PPA + "/" + Proinfo2.PPA
                            if Proinfo1.PQE == Proinfo2.PQE:
                                PQE = Proinfo1.PQE
                            else:
                                PQE = Proinfo1.PQE + "/" + Proinfo2.PQE
                            if Proinfo1.SS == Proinfo2.SS:
                                SS = Proinfo1.SS
                            else:
                                SS = Proinfo1.SS + "/" + Proinfo2.SS
                            if Proinfo1.LD == Proinfo2.LD:
                                LD = Proinfo1.LD
                            else:
                                LD = Proinfo1.LD + "/" + Proinfo2.LD
                            if Proinfo1.DQAPL == Proinfo2.DQAPL:
                                DQAPL = Proinfo1.DQAPL
                            else:
                                DQAPL = Proinfo1.DQAPL + "/" + Proinfo2.DQAPL
                            proinfomation.append({
                                "id": Proinfo1.id,
                                "YEAR": Year,
                                "COMPRJCODE": i["Project"],
                                # "PHASE": i["Phase"],
                                "PrjEngCode1": PrjEngCode1,
                                "PrjEngCode2": PrjEngCode2,
                                "PROJECT": ProjectName,
                                "SIZE": Size,
                                "CPU": CPU,
                                "PLATFORM": Platform,
                                "VGA": VGA,
                                "OSSUPPORT": OSSupport,
                                "Type": Type,
                                "PPA": PPA,
                                "PQE": PQE,
                                "SS": SS,
                                "LD": LD,
                                "DQAPL": DQAPL,
                            })
                        else:
                            proinfomation.append({
                                "id": "",
                                "YEAR": "", "COMPRJCODE": i["Project"],
                                # "PHASE": i["Phase"],
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
                    else:
                        proinfomation.append({
                            "id": "",
                            "YEAR": "", "COMPRJCODE": i["Project"],
                            # "PHASE": i["Phase"],
                            "PrjEngCode1": "",
                            "PrjEngCode2": "",
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
        if request.POST.get("isGetData") == "SELECTPRO":

            Customer = request.POST.get("Customer")
            Project = request.POST.get("COMPRJCODE")
            check_dic_Pro = {"Customer": Customer, "Project": Project}
            # print(Customer)
            Testahour_key = []
            if TestProjectSWAIO.objects.filter(**check_dic_Pro).first():#至少存在一个Phase
                for h in TestProjectSWAIO.objects.filter(**check_dic_Pro).values("Phase").order_by("-ScheduleEnd"):
                    Testahour_key.append(h["Phase"])

                Time_value_Re = []
                Time_value_Re_ATO = []
                Time_value_CAT = []
                Time_value_CLT = []
                Time_value_CST = []
                SaveTime_value = [
                                          # [1003, 1001, 1002, 1006],#auto
                                          # [1527, 1483, 344, 1971], #leverage
                                          # [1971, 2103, 1493, 1000] #smart
                                      ],
                SaveTime_key = [
                    # 'FFRT', 'SIT', 'FVT', 'TOTAL'
                ]
                for i in Testahour_key:
                    check_dic = {"Customer": Customer, "Project": Project, "Phase": i}
                    # print(check_dic)
                    Projectinfo = TestProjectSWAIO.objects.filter(**check_dic).first()
                    CRTsum = TestPlanSWAIO.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigRetesttime'))
                    ATOsum = TestPlanSWAIO.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('AttendtimeOptimize'))
                    CATsum = TestPlanSWAIO.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigAutomationtime'))
                    CLTsum = TestPlanSWAIO.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigLeveragetime'))
                    CSTsum = TestPlanSWAIO.objects.filter(Projectinfo=Projectinfo).aggregate(Sum('ConfigSmarttime'))


                    if CRTsum["ConfigRetesttime__sum"]:
                        CRTtotal = CRTsum["ConfigRetesttime__sum"]
                    else:
                        CRTtotal = 0
                    if ATOsum["AttendtimeOptimize__sum"]:
                        ATOtotal = ATOsum["AttendtimeOptimize__sum"]
                    else:
                        ATOtotal = 0

                    if CATsum["ConfigAutomationtime__sum"]:
                        CATtotal = CATsum["ConfigAutomationtime__sum"]
                    else:
                        CATtotal = 0

                    if CLTsum["ConfigLeveragetime__sum"]:
                        CLTtotal = CLTsum["ConfigLeveragetime__sum"]
                    else:
                        CLTtotal = 0

                    if CSTsum["ConfigSmarttime__sum"]:
                        CSTtotal = CSTsum["ConfigSmarttime__sum"]
                    else:
                        CSTtotal = 0
                    # print(CRTtotal,ATOtotal,CATtotal,CLTtotal,CSTtotal)
                    Time_value_Re.append(round(CRTtotal/60, 0))
                    Time_value_Re_ATO.append(round(ATOtotal/60, 0))
                    Time_value_CAT.append(round(CATtotal/60, 0))
                    Time_value_CLT.append(round(CLTtotal / 60, 0))
                    Time_value_CST.append(round(CSTtotal / 60, 0))
                Project_ReTotal = 0
                for i in Time_value_Re:
                    Project_ReTotal += i
                Time_value_Re.append(round(Project_ReTotal, 0))
                Project_ATOTotal = 0
                for i in Time_value_Re_ATO:
                    Project_ATOTotal += i
                Time_value_Re_ATO.append(round(Project_ATOTotal, 0))
                Project_CATTotal = 0
                for i in Time_value_CAT:
                    Project_CATTotal += i
                Time_value_CAT.append(round(Project_CATTotal, 0))
                Project_CLTotal = 0
                for i in Time_value_CLT:
                    Project_CLTotal += i
                Time_value_CLT.append(round(Project_CLTotal, 0))
                Project_CSTotal = 0
                for i in Time_value_CST:
                    Project_CSTotal += i
                Time_value_CST.append(round(Project_CSTotal, 0))
                Testahour_key.append("Total")
                Sums1["Testahour_value"] = [Time_value_Re, Time_value_Re_ATO]
                Sums1["Testahour_key"] = Testahour_key

                SaveTime_key = Testahour_key
                Sums1["SaveTime_value"] = [Time_value_CAT, Time_value_CLT, Time_value_CST]
                Sums1["SaveTime_key"] = SaveTime_key

            canEdit = 0
            current_user = request.session.get('user_name')
            if TestProjectSW.objects.filter(**check_dic_Pro).first():
                for h in TestProjectSW.objects.filter(**check_dic_Pro):
                    for i in h.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if i.username == current_user:
                            canEdit = 1
                            break
        if request.POST.get("isGetData") == "SEARCH":
            Customer = request.POST.get("Customer")
            Project = request.POST.get("Project")
            Phase = request.POST.get("Phase")
            if Phase == '0':
                Phase = 'B(SDV)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'Wave2'
            if Phase == '3':
                Phase = 'Wave3'
            if Phase == '4':
                Phase = 'EELP+'
            if Phase == '5':
                Phase = 'OOC'
            if Phase == '6':
                Phase = 'OOC2'
            if Phase == '7':
                Phase = 'OOC3'
            Category = request.POST.get("category")
            dicProject = {'Customer': Customer, "Project": Project,
                       'Phase': Phase,}
            Projectinfos = TestProjectSWAIO.objects.filter(**dicProject).first()
            dicPlan = {'Customer': Customer, "Category": Category,
                       'Phase': Phase, "Projectinfo": Projectinfos}
            if Projectinfos:
                SKUlist = [Projectinfos.SKU1, Projectinfos.SKU2, Projectinfos.SKU3,
                           Projectinfos.SKU4,
                           Projectinfos.SKU5,
                           Projectinfos.SKU6, Projectinfos.SKU7, Projectinfos.SKU8,
                           Projectinfos.SKU9,
                           Projectinfos.SKU10,
                           Projectinfos.SKU11, Projectinfos.SKU12, Projectinfos.SKU13,
                           Projectinfos.SKU14,
                           Projectinfos.SKU15,
                           Projectinfos.SKU16, Projectinfos.SKU17, Projectinfos.SKU18,
                           Projectinfos.SKU19,
                           Projectinfos.SKU20]
                n = 1
                for l in SKUlist:
                    if l:
                        # print(l)
                        SKUno = 'SKU%s' % n
                        SKU.append({"skuNo": SKUno, "VGA": l.split('/')[1], "CPU": l.split('/')[0]})
                    n += 1
                x = 0
                for i in TestPlanSWAIO.objects.filter(**dicPlan):
                    x += 1
                    # print(i,type(i))
                    # print(i.id)
                    planOptimize = []
                    SKUlist_T = {"SKU1": i.SKU1, "SKU2": i.SKU2, "SKU3": i.SKU3, "SKU4": i.SKU4, "SKU5": i.SKU5,
                                 "SKU6": i.SKU6, "SKU7": i.SKU7, "SKU8": i.SKU8, "SKU9": i.SKU9,
                                 "SKU10": i.SKU10,
                                 "SKU11": i.SKU11, "SKU12": i.SKU12, "SKU13": i.SKU13, "SKU14": i.SKU14,
                                 "SKU15": i.SKU15,
                                 "SKU16": i.SKU16, "SKU17": i.SKU17, "SKU18": i.SKU18, "SKU19": i.SKU19,
                                 "SKU20": i.SKU20}
                    for j in SKU:
                        if j["skuNo"] in SKUlist_T.keys():
                            planOptimize.append(SKUlist_T[j["skuNo"]])
                    # print(planOptimize)
                    # print(i.ConfigSmartItemPer,i.ConfigSmartTime)
                    newContents.append(
                        {"id": i.id, "Category": i.Category, "Test_Title": i.TestTitle,
                         "Sub_Test_Title": i.Subtesttitle, "Test_Item": i.TestItem, "Priority": i.Priority,
                         "Release_Date": i.ReleaseDate, "Owner": i.Owner, "Attend_Time": i.AT_AttendTime,
                         "Unattend_Time": i.AT_UnattendTime,
                         "Automation": i.AT_Automation, "Attend_Time_hrs": i.DQMS_AttendTime,
                         "Unattend_Time_hrs": i.DQMS_UnattendTime, "TUC": i.TestUnitsConfig, "Smart_Item": i.SmartItem,
                         "Cusumer": i.Cusumer, "Commercial": i.Commercial,
                         "SDV": i.SDV, "SIT": i.SIT, "Coverage": i.Coverage, "FS": i.FeatureSupport,
                         "BTS": i.Basetimesupport,
                         "TE": i.TE, "schedule": i.Schedule,
                         "NUMX": i.Configalltestunits, "NUMX_TIME": i.Configalltesttime, "NUMA": i.ConfigAutomationItem,
                         "CAT": i.ConfigAutomationtime, "NUML": i.ConfigLeverageItem, "CLT": i.ConfigLeveragetime,
                         "conSitemInAll": i.ConfigSmartItemper,
                         "CST": i.ConfigSmarttime, "comments": i.Comments, "proTS": i.ProjecttestSKUOptimize,
                         "ATO": i.AttendtimeOptimize,
                         "planOptimize": planOptimize,
                         "CRC": i.ConfigRetestCycle, "CRS": i.ConfigRetestSKU, "CRT": i.ConfigRetesttime}, )
        data = {
            "content": newContents,
            "SKU": SKU,
            "canEdit1": canEdit,
            "Sum": Sums,
            "Sum1": Sums1,
            "allSum": allSum,
            "select1": selectItem,
            "proinfomation": proinfomation,
            "rdchangelist": rdchangelist,
        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")


    return render(request, 'TestPlanSW/TestPlanSW_search_AIO.html', locals())