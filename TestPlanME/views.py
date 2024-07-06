from django.shortcuts import render
from django.shortcuts import render,redirect

from django.views.decorators.csrf import csrf_exempt
import datetime,os
from service.init_permission import init_permission
from django.conf import settings
# Create your views here.
from django.forms import forms


from django.conf import settings
from django.http import HttpResponse
from TestPlanME.models import TestPlanME,TestProjectME,TestItemME,KeypartAIO,KeypartC38NB
from app01.models import ProjectinfoinDCT, UserInfo
import datetime,json,simplejson
from django.db.models import Max,Min,Sum,Count

# Create your views here.

def TestPlanME_Summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    mock_data = [
    #     {
    #     "ItemNo": "H1-1", "Item": "Basic Function Check", "Facility Name": "N/A", "Voltage (our)": "N/A",
    #     "Sample Size": "All units", "TTF": 0, "TTM": 1, "TTP": 1, "NTU": 12, "RTR": 0, "RTU": 12
    # }, {
    #     "ItemNo": "H1-2", "Item": "Structure Analysis Test", "Facility Name": "N/A", "Voltage (our)": "N/A",
    #     "Sample Size": "At least 10 units", "TTF": 0, "TTM": 4, "TTP": 0, "NTU": 10, "RTR": 0, "RTU": 12
    # }, {
    #     "ItemNo": "H1-3", "Item": "Operation Temp/Hum Cycle Test", "Facility Name": "恆溫恆濕試驗機", "Voltage (our)": "12000",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 80, "TTM": 1, "TTP": 0.5, "NTU": 23, "RTR": 7, "RTU": 12
    # }, {
    #     "ItemNo": "H1-4", "Item": "Storage Temp/Hum Test", "Facility Name": "恆溫恆濕試驗機", "Voltage (our)": "12000",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 96, "TTM": 1, "TTP": 0.5, "NTU": 5, "RTR": 7, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #1-1", "Item": "Cold start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 19, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 6, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #1-1", "Item": "Cold start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 19, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 5, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #2-1", "Item": "Hot start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 9, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 3, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #2-1", "Item": "Hot start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 9, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 0, "RTU": 6
    # }, {
    #     "ItemNo": "H1-6", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 7
    # }, {
    #     "ItemNo": "H1-4", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 3
    # }, {
    #     "ItemNo": "H1-33", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 8, "TTM": 8, "TTP": 0, "NTU": 22, "RTR": 0, "RTU": 6
    # }, {
    #     "ItemNo": "H1-34", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 1, "NTU": 22, "RTR": 0, "RTU": 5
    # }, {
    #     "ItemNo": "H1-30", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 5, "TTM": 1, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 12
    # },
    ]
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/ME/Search"

    selectItem = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]
    searchalert = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus","PHASE":"FVT",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMS0", "CUSPRJCODE": "Taurus","PHASE":"FVT",
        #  "PROJECT": "IdeaPad5 14IIL05 Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "Intel",
        #  "PLATFORM": "Intel Ice Lake-U", "VGA": "NV N175-G3 NV N175-G5 UMA", "OS SUPPORT": "WIN10 19H2",
        #  "SS": "2020-01-17", "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FLAE1", "CUSPRJCODE": "Tata 3","Phase":"FVT", "PROJECT": "Lenovo E41-45", "SIZE": "14",
        #  "CPU": "AMD", "PLATFORM": "AMDStoney Ridge", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-01-16",
        #  "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "ELY5U", "CUSPRJCODE": "Zeus","PHASE":"FVT",
        #  "PROJECT": "Legion Y740S-15IRH Legion Y90000X 2019", "SIZE": "15", "CPU": "Intel",
        #  "PLATFORM": "Intel Coffee Lake H-Refresh", "VGA": "UMA", "OS SUPPORT": "WIN10 19H1 WIN10 19H2 WIN10 RS5",
        #  "SS": "2019-09-30", "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "EL571", "CUSPRJCODE": "Mars","PHASE":"FVT",
        #  "PROJECT": "Lenovo Yoga S740-15IRH Lenovo IdeaPad S740-15IRH Lenovo IdeaPad S740-15IRH Touch Lenovo 小新Pro-15 2019",
        #  "SIZE": "15", "CPU": "Intel", "PLATFORM": "Intel Coffee Lake H-Refresh", "VGA": "N18P-G0-MP-A1",
        #  "OS SUPPORT": "WIN10 19H1 WIN10 19H2", "SS": "2019-09-27", "LD": "王青", "DQA PL": "张亚萍",
        #  "MODIFIED DATE": "2020-01-18"},
        # {"YEAR": "Y2019", "COMPRJCODE": "FL5C5", "CUSPRJCODE": "Rhode","PHASE":"FVT",
        #  "PROJECT": "Lenovo IdeaPad C340-15IIL Lenovo IdeaPad Flex-15IIL", "SIZE": "15", "CPU": "Intel",
        #  "PLATFORM": "Intel Ice Lake-U", "VGA": "UMA", "OS SUPPORT": "WIN10 19H1 WIN10 19H2", "SS": "2019-09-08",
        #  "LD": "王青", "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"}
    ]
    mock_data = [
        # {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1", "Panel": "1", "Hinge": "1",
        #  "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1", "SSD/HDD": "1", "Camera": "1",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "305.5", "RegressiveAttendTime": "0"},
        # {"Project": "Standard1", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "2", "Panel": "6", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2", "SSD/HDD": "6", "Camera": "3",
        #  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "700", "RegressiveAttendTime": "0"},
        # {"Project": "Single-2", "ID": "1", "Type": "Yoga", "SKU": "1", "Planar": "1", "Panel": "1", "Hinge": "1",
        #  "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1", "SSD/HDD": "1", "Camera": "1",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "328.5", "RegressiveAttendTime": "0"},
        # {"Project": "Standard2", "ID": "1", "Type": "Yoga", "SKU": "6", "Planar": "2", "Panel": "6", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2", "SSD/HDD": "6", "Camera": "3",
        #  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "855", "RegressiveAttendTime": "0"},
        # {"Project": "ELY5U FVT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "3", "Hinge": "2",
        #  "Cable": "4", "Connectorsource": "2", "Keyboard": "2", "ClickPad": "1", "SSD/HDD": "1", "Camera": "3",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "519", "RegressiveAttendTime": "145"},
        # {"Project": "ELY5U SIT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "3", "Hinge": "2",
        #  "Cable": "4", "Connectorsource": "2", "Keyboard": "2", "ClickPad": "1", "SSD/HDD": "6", "Camera": "3",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "527", "RegressiveAttendTime": "199"},
        # {"Project": "Y750 FVT", "ID": "1", "Type": "Normal", "SKU": "5", "Planar": "1", "Panel": "3", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "1", "Keyboard": "2", "ClickPad": "1", "SSD/HDD": "6", "Camera": "1",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "428", "RegressiveAttendTime": "113"},
        # {"Project": "Y750 SIT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "5", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "3", "Keyboard": "4", "ClickPad": "1", "SSD/HDD": "6", "Camera": "2",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "579", "RegressiveAttendTime": "111"},
        # {"Project": "WOS FVT", "ID": "1", "Type": "Yoga", "SKU": "3", "Planar": "1", "Panel": "1", "Hinge": "1",
        #  "Cable": "1", "Connectorsource": "2", "Keyboard": "1", "ClickPad": "1", "SSD/HDD": "6", "Camera": "2",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "401", "RegressiveAttendTime": "164"},
        # {"Project": "S550 FVT", "ID": "1", "Type": "Normal", "SKU": "4", "Planar": "2", "Panel": "1", "Hinge": "1",
        #  "Cable": "1", "Connectorsource": "2", "Keyboard": "1", "ClickPad": "2", "SSD/HDD": "6", "Camera": "2",
        #  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "317.5",
        #  "RegressiveAttendTime": "123"},
        # {"Project": "S550 SIT", "ID": "1", "Type": "Normal", "SKU": "7", "Planar": "2", "Panel": "2", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "2", "Keyboard": "1", "ClickPad": "2", "SSD/HDD": "6", "Camera": "4",
        #  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "485", "RegressiveAttendTime": "212"},

    ]
    AIO_tableData = [
        # {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1", "Panel": "1", "Stand": "1",
        #  "Cable": "1", "Connectorsource": "1", "SSD/HDD": "1", "Camera": "1", "ODD": "0", "Package": "1",
        #  "RegularAttendTime": "700", "RegressiveAttendTime": "0"},
        # {"Project": "Standard1", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "2", "Panel": "6", "Stand": "2",
        #  "Cable": "3", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "3", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "700", "RegressiveAttendTime": "0"},
        # {"Project": "Single-2", "ID": "1", "Type": "Yoga", "SKU": "1", "Planar": "1", "Panel": "1", "Stand": "1",
        #  "Cable": "1", "Connectorsource": "1", "SSD/HDD": "1", "Camera": "1", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "328.5", "RegressiveAttendTime": "0"},
        # {"Project": "Standard2", "ID": "1", "Type": "Yoga", "SKU": "6", "Planar": "2", "Panel": "6", "Stand": "2",
        #  "Cable": "3", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "3", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "855", "RegressiveAttendTime": "0"},
        # {"Project": "ELY5U FVT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "3", "Stand": "2",
        #  "Cable": "4", "Connectorsource": "2", "SSD/HDD": "1", "Camera": "3", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "519", "RegressiveAttendTime": "145"},
        # {"Project": "ELY5U SIT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "3", "Stand": "2",
        #  "Cable": "4", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "3", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "527", "RegressiveAttendTime": "199"},
        # {"Project": "Y750 FVT", "ID": "1", "Type": "Normal", "SKU": "5", "Planar": "1", "Panel": "3", "Stand": "2",
        #  "Cable": "3", "Connectorsource": "1", "SSD/HDD": "6", "Camera": "1", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "428", "RegressiveAttendTime": "113"},
        # {"Project": "Y750 SIT", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "1", "Panel": "5", "Hinge": "2",
        #  "Cable": "3", "Connectorsource": "3", "SSD/HDD": "6", "Camera": "2", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "579", "RegressiveAttendTime": "111"},
        # {"Project": "WOS FVT", "ID": "1", "Type": "Yoga", "SKU": "3", "Planar": "1", "Panel": "1", "Stand": "1",
        #  "Cable": "1", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "2", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "401", "RegressiveAttendTime": "164"},
        # {"Project": "S550 FVT", "ID": "1", "Type": "Normal", "SKU": "4", "Planar": "2", "Panel": "1", "Stand": "1",
        #  "Cable": "1", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "2", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "317.5", "RegressiveAttendTime": "123"},
        # {"Project": "S550 SIT", "ID": "1", "Type": "Normal", "SKU": "7", "Planar": "2", "Panel": "2", "Stand": "2",
        #  "Cable": "3", "Connectorsource": "2", "SSD/HDD": "6", "Camera": "4", "ODD": "0", "Package": "0",
        #  "RegularAttendTime": "485", "RegressiveAttendTime": "212"},

    ]
    Top10 = {
        # "Execution_key": ['xxxxx', 'xxxxxcdcdfsff', 'xfbgbd', 'x', 'x', 'x', 'x', 'x', 'x', 'c'],
        # "Regression_key": ['cccccccc', 'ccc', 'cvbnmhgffg', 'c', 'cc', 'c', 'ccc', 'c', 'ccc', 'cvc']
    }
    Execution_Top10 = [
    #     {
    #     "name": 'B(FVT)',
    #     "type": 'bar',
    #     "stack": '总量',
    #     "data": [
    #         {"value": 320, "name": "xxxxx"}, {"value": 302, "name": "xxxxxcdcdfsff"}, {"value": 301, "name": "xfbgbd"},
    #         {"value": 334, "name": "x"}, {"value": 390, "name": "x"}, {"value": 330, "name": "x"},
    #         {"value": 320, "name": "x"}, {"value": 330, "name": "x"}, {"value": 110, "name": "x"},
    #         {"value": 456, "name": "c"}
    #     ]  # 这里面的数据要与Top10标签中的顺序对应
    # },
    #     {
    #         "name": 'C(SIT)',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [
    #             {"value": 120, "name": "xxxxx"}, {"value": 132, "name": "xxxxxcdcdfsff"},
    #             {"value": 101, "name": "xfbgbd"}, {"value": 134, "name": "x"}, {"value": 90, "name": "x"},
    #             {"value": 230, "name": "x"}, {"value": 330, "name": "x"}, {"value": 567, "name": "x"},
    #             {"value": 908, "name": "x"},
    #             {"value": 107, "name": "c"}
    #         ]
    #     },
    #     {
    #         "name": 'FFRT',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [
    #             {"value": 220, "name": "xxxxx"}, {"value": 182, "name": "xxxxxcdcdfsff"},
    #             {"value": 191, "name": "xfbgbd"}, {"value": 234, "name": "x"}, {"value": 290, "name": "x"},
    #             {"value": 330, "name": "x"}, {"value": 310, "name": "x"}, {"value": 291, "name": "x"},
    #             {"value": 281, "name": "x"},
    #             {"value": 222, "name": "c"}
    #         ]
    #     },
    #     {
    #         "name": 'OOC',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [
    #             {"value": 150, "name": "xxxxx"}, {"value": 212, "name": "xxxxxcdcdfsff"},
    #             {"value": 201, "name": "xfbgbd"}, {"value": 154, "name": "x"}, {"value": 190, "name": "x"},
    #             {"value": 330, "name": "x"}, {"value": 410, "name": "x"}, {"value": 154, "name": "x"},
    #             {"value": 367, "name": "x"},
    #             {"value": 345, "name": "c"}
    #         ]
    #     },
    #     {
    #         "name": 'Wave',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [
    #             {"value": 820, "name": "xxxxx"},
    #             {"value": "null", "name": "xxxxxcdcdfsff"},
    #             {"value": 901, "name": "xfbgbd"}, {"value": 934, "name": "x"}, {"value": 1290, "name": "x"},
    #             {"value": 1330, "name": "x"}, {"value": 1320, "name": "x"}, {"value": 476, "name": "x"},
    #             {"value": 376, "name": "x"},
    #             {"value": 333, "name": "c"}
    #         ]
    #     }
    ]
    Regression_Top10 = [
    #     {
    #     "name": 'B(FVT)',
    #     "type": 'bar',
    #     "stack": '总量',
    #     "data": [320, 302, 301, 334, 390, 330, 320, 154, 190, 330]
    # },
    #     {
    #         "name": 'C(SIT)',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [120, 132, 101, 134, 90, 230, 210, 934, 1290, 1330]
    #     },
    #     {
    #         "name": 'FFRT',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [220, 182, 191, 234, 290, 330, 310, 832, 901, 934]
    #     },
    #     {
    #         "name": 'OOC',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [150, 212, 201, 154, 190, 330, 410, 290, 330, 310]
    #     },
    #     {
    #         "name": 'Wave',
    #         "type": 'bar',
    #         "stack": '总量',
    #         "data": [820, 832, 901, 934, 1290, 1330, 1320, 832, 901, 934]
    #     }
    ]
    for i in TestProjectME.objects.all().values("Customer").distinct().order_by("Customer"):
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
            defaultproject = TestProjectME.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                "-ScheduleBegin")
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

            print(counter, defaultprojectlist)

            Projectlist = []
            for i in defaultprojectlist:
                # print(i)
                for j in TestProjectME.objects.filter(Customer=Customer, Project=i):
                    Projectlist.append({"name": i, "value": j.Phase})
            # print(Projectlist)

            # 之后的跟getMsg里面的一样
            if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                for i in Projectlist:
                    check_dic_Project = {"Customer": Customer, "Project": i["name"], "Phase": i["value"]}
                    if KeypartAIO.objects.filter(**check_dic_Project).first():
                        serchProjectresult = KeypartAIO.objects.filter(**check_dic_Project).first()
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        AIO_tableData.append({"Project": i["name"], "Phase": i["value"], "ID": serchProjectresult.IDs,
                                              "Type": serchProjectresult.Type,
                                              "SKU": serchProjectresult.SKU, "Planar": serchProjectresult.Planar,
                                              "Panel": serchProjectresult.Panel,
                                              "Stand": serchProjectresult.Stand, "Cable": serchProjectresult.Cable,
                                              "Connectorsource": serchProjectresult.Connectorsource,
                                              "SSD/HDD": serchProjectresult.SSDHHD, "Camera": serchProjectresult.Camera,
                                              "ODD": serchProjectresult.ODD,
                                              "Package": serchProjectresult.Package,
                                              "RegularAttendTime": RegularAttendTime,
                                              "RegressiveAttendTime": RegressiveAttendTime})
                    else:
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        AIO_tableData.append({"Project": i["name"], "Phase": i["value"], "ID": '',
                                              "Type": '',
                                              "SKU": '', "Planar": '',
                                              "Panel": '',
                                              "Stand": '', "Cable": '',
                                              "Connectorsource": '',
                                              "SSD/HDD": '', "Camera": '',
                                              "ODD": '',
                                              "Package": '',
                                              "RegularAttendTime": RegularAttendTime,
                                              "RegressiveAttendTime": RegressiveAttendTime})

            else:
                for i in Projectlist:
                    check_dic_Project = {"Customer": Customer, "Project": i["name"], "Phase": i["value"]}
                    # print(check_dic_Project)
                    if KeypartC38NB.objects.filter(**check_dic_Project).first():
                        serchProjectresult = KeypartC38NB.objects.filter(**check_dic_Project).first()
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)
                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        mock_data.append({"Project": i["name"], "Phase": i["value"], "ID": serchProjectresult.IDs,
                                          "Type": serchProjectresult.Type, "SKU": serchProjectresult.SKU,
                                          "Planar": serchProjectresult.Planar, "Panel": serchProjectresult.Panel,
                                          "Hinge": serchProjectresult.Hinge,
                                          "Cable": serchProjectresult.Cable,
                                          "Connectorsource": serchProjectresult.Connectorsource,
                                          "Keyboard": serchProjectresult.Keyboard,
                                          "ClickPad": serchProjectresult.ClickPad, "SSD/HDD": serchProjectresult.SSDHHD,
                                          "Camera": serchProjectresult.Camera,
                                          "Rubberfoot": serchProjectresult.Rubberfoot, "ODD": serchProjectresult.ODD,
                                          "TrapDoorRJ45": serchProjectresult.TrapDoorRJ45,
                                          "RegularAttendTime": RegularAttendTime,
                                          "RegressiveAttendTime": RegressiveAttendTime})
                    else:
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        mock_data.append({"Project": i["name"], "Phase": i["value"], "ID": '',
                                          "Type": '', "SKU": '',
                                          "Planar": '', "Panel": '',
                                          "Hinge": '',
                                          "Cable": '',
                                          "Connectorsource": '',
                                          "Keyboard": '',
                                          "ClickPad": '', "SSD/HDD": '',
                                          "Camera": '',
                                          "Rubberfoot": '', "ODD": '',
                                          "TrapDoorRJ45": '',
                                          "RegularAttendTime": RegularAttendTime,
                                          "RegressiveAttendTime": RegressiveAttendTime})
            # print(mock_data)
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
            Phasesortorder = {'B(FVT)': 0, 'C(SIT)': 1, }
            # print(Projectlist_top)
            Phaselist_top.sort(key=lambda x: Phasesortorder[x])
            for i in Projectlist_top:
                ProjecttotalATO = 0.00
                ProjecttotalRe = 0.00
                datainphase_normal = {}
                datainphase_retest = {}
                if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                    for j in AIO_tableData:  # 尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            ProjecttotalATO += j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            ProjecttotalRe += j["RegressiveAttendTime"]

                            datainphase_normal[j['Phase']] = j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            datainphase_retest[j['Phase']] = j["RegressiveAttendTime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]
                else:
                    for j in mock_data:  # 尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            # print(j["Project"],j["Phase"],j["RegularAttendTime"],type(j["RegularAttendTime"]))
                            ProjecttotalATO += j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            ProjecttotalRe += j["RegressiveAttendTime"]

                            datainphase_normal[j['Phase']] = j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            datainphase_retest[j['Phase']] = j["RegressiveAttendTime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]

            # reverse为True从大到小
            top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1][0], reverse=True)
            top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1][0], reverse=True)
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
            # print(datetime.datetime.now(), "图表1")
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
            mock_data.insert(0, {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1",
                                 "Panel": "1", "Hinge": "1",
                                 "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1",
                                 "SSD/HDD": "1", "Camera": "1",
                                 "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "305.5",
                                 "RegressiveAttendTime": "0"})
            mock_data.insert(1,
                             {"Project": "Standard1", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "2",
                              "Panel": "6",
                              "Hinge": "2",
                              "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2",
                              "SSD/HDD": "6",
                              "Camera": "3",
                              "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "700",
                              "RegressiveAttendTime": "0"})
            mock_data.insert(2,
                             {"Project": "Single-2", "ID": "1", "Type": "Yoga", "SKU": "1", "Planar": "1",
                              "Panel": "1",
                              "Hinge": "1",
                              "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1",
                              "SSD/HDD": "1",
                              "Camera": "1",
                              "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "328.5",
                              "RegressiveAttendTime": "0"})
            mock_data.insert(3,
                             {"Project": "Standard2", "ID": "1", "Type": "Yoga", "SKU": "6", "Planar": "2",
                              "Panel": "6",
                              "Hinge": "2",
                              "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2",
                              "SSD/HDD": "6",
                              "Camera": "3",
                              "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "855",
                              "RegressiveAttendTime": "0"})
            # print(datetime.datetime.now(), "图表2")
            # print(Top10)
        if request.POST.get("isGetData") == "SEARCHALERT":
            Customer = request.POST.get("Customer")
            timerange = request.POST.getlist("Date", [])
            # print(timerange[0])
            # print(not timerange[0])
            Prolist = []
            # print(Customer)
            if not timerange[0]:
                # 应该是统计只要某机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                if Customer:
                    # for i in TestProjectSW.objects.filter(Customer=Customer).values("Project", "Phase").distinct().order_by(
                    #         "Project"):
                    #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                    for i in TestProjectME.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                            "Project"):
                        # print(i)
                        for j in TestProjectME.objects.filter(Customer=Customer, Project=i["Project"]):
                            Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                else:
                    # for i in TestProjectSW.objects.all().values("Project", "Phase").distinct().order_by("Project"):
                    #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                    for i in TestProjectME.objects.all().values("Project").distinct().order_by("Project"):
                        for j in TestProjectME.objects.filter(Project=i["Project"]):
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
                            # print(i['Project'],i['Project'][0:5],i['Project'][0:3],i['Project'][5:])
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
            else:
                # 应该是统计只要某 机种有一个Phase在规定时间段内，就统计这个机种的所有Phase的结果
                if Customer:
                    # for i in TestProjectSW.objects.filter(Customer=Customer).filter(Gerber__range=timerange).values("Project", "Phase").distinct().order_by(
                    #         "Project"):
                    #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                    for i in TestProjectME.objects.filter(Customer=Customer).filter(ScheduleBegin__range=timerange).values(
                            "Project").distinct().order_by(
                        "Project"):
                        for j in TestProjectME.objects.filter(Customer=Customer, Project=i["Project"]):
                            Prolist.append({"Project": i["Project"], "Phase": j.Phase})
                else:
                    # for i in TestProjectSW.objects.filter(Gerber__range=timerange).values("Project", "Phase").distinct().order_by("Project"):
                    #     Prolist.append({"Project": i["Project"], "Phase": i["Phase"]})
                    for i in TestProjectME.objects.filter(ScheduleBegin__range=timerange).values(
                            "Project").distinct().order_by(
                            "Project"):
                        for j in TestProjectME.objects.filter(Project=i["Project"]):
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
                            "CUSPRJCODE": ProjectinfoinDCT.objects.filter(ComPrjCode=i["Project"]).first().CusPrjCode,
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
                            # print(i['Project'],i['Project'][0:5],i['Project'][0:3],i['Project'][5:])
                            Prostr1 = i['Project'][0:5]
                            Prostr2 = i['Project'][0:3]+i['Project'][5:]
                            Proinfo1 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr1).first()
                            Proinfo2 = ProjectinfoinDCT.objects.filter(ComPrjCode=Prostr2).first()
                            if Proinfo1 and Proinfo2:
                                if Proinfo1.Year == Proinfo2.Year:
                                    Year = Proinfo1.Year
                                else:
                                    Year = Proinfo1.Year + "/" + Proinfo2.Year
                                if Proinfo1.CusPrjCode == Proinfo2.CusPrjCode:
                                    CusPrjCode = Proinfo1.CusPrjCode
                                else:
                                    CusPrjCode = Proinfo1.CusPrjCode + "/" + Proinfo2.CusPrjCode
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
                                    "CUSPRJCODE": CusPrjCode,
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
                            searchalert.append({
                                "id": "",
                                "YEAR": "", "COMPRJCODE": i["Project"],
                                "PHASE": i["Phase"],
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
        if 'getMsg' in str(request.body):#前端穿Jason数据
            getdata = json.loads(request.body)
            # print(getdata)
            # print(datetime.datetime.now())
            Customer = getdata['customer']
            Projectlist = getdata["searchalert"]
            # print(Projectlist)
            if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                for i in Projectlist:
                    check_dic_Project = {"Customer": Customer, "Project": i["name"], "Phase": i["value"]}
                    if KeypartAIO.objects.filter(**check_dic_Project).first():
                        serchProjectresult = KeypartAIO.objects.filter(**check_dic_Project).first()
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        AIO_tableData.append({"Project": i["name"], "Phase": i["value"], "ID": serchProjectresult.IDs, "Type": serchProjectresult.Type,
                                              "SKU": serchProjectresult.SKU, "Planar": serchProjectresult.Planar, "Panel": serchProjectresult.Panel,
                                              "Stand": serchProjectresult.Stand,"Cable": serchProjectresult.Cable, "Connectorsource": serchProjectresult.Connectorsource,
                                              "SSD/HDD": serchProjectresult.SSDHHD, "Camera": serchProjectresult.Camera, "ODD": serchProjectresult.ODD,
                                              "Package": serchProjectresult.Package,"RegularAttendTime": RegularAttendTime, "RegressiveAttendTime": RegressiveAttendTime})
                    else:
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        AIO_tableData.append({"Project": i["name"], "Phase": i["value"], "ID": '',
                                              "Type": '',
                                              "SKU": '', "Planar": '',
                                              "Panel": '',
                                              "Stand": '', "Cable": '',
                                              "Connectorsource": '',
                                              "SSD/HDD": '', "Camera": '',
                                              "ODD": '',
                                              "Package": '',
                                              "RegularAttendTime": RegularAttendTime,
                                              "RegressiveAttendTime": RegressiveAttendTime})

            else:
                for i in Projectlist:
                    check_dic_Project = {"Customer": Customer, "Project": i["name"], "Phase": i["value"]}
                    # print(check_dic_Project)
                    if KeypartC38NB.objects.filter(**check_dic_Project).first():
                        serchProjectresult = KeypartC38NB.objects.filter(**check_dic_Project).first()
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)
                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        mock_data.append({"Project": i["name"], "Phase": i["value"], "ID": serchProjectresult.IDs, "Type": serchProjectresult.Type, "SKU": serchProjectresult.SKU,
                                          "Planar": serchProjectresult.Planar, "Panel": serchProjectresult.Panel, "Hinge": serchProjectresult.Hinge,
                                         "Cable": serchProjectresult.Cable, "Connectorsource": serchProjectresult.Connectorsource, "Keyboard": serchProjectresult.Keyboard,
                                          "ClickPad": serchProjectresult.ClickPad, "SSD/HDD": serchProjectresult.SSDHHD, "Camera": serchProjectresult.Camera,
                                         "Rubberfoot": serchProjectresult.Rubberfoot, "ODD": serchProjectresult.ODD, "TrapDoorRJ45": serchProjectresult.TrapDoorRJ45,
                                          "RegularAttendTime": RegularAttendTime, "RegressiveAttendTime": RegressiveAttendTime})
                    else:
                        Projectinfos = TestProjectME.objects.filter(**check_dic_Project).first()
                        # print(Projectinfos)
                        TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')

                        # print(RTRMax)

                        if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                            RegularAttendTime = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                        else:
                            RegularAttendTime = 0
                        if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                            RegressiveAttendTime = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                        else:
                            RegressiveAttendTime = 0
                        mock_data.append({"Project": i["name"], "Phase": i["value"],  "ID": '',
                                          "Type": '', "SKU": '',
                                          "Planar": '', "Panel": '',
                                          "Hinge": '',
                                          "Cable": '',
                                          "Connectorsource": '',
                                          "Keyboard": '',
                                          "ClickPad": '', "SSD/HDD": '',
                                          "Camera": '',
                                          "Rubberfoot": '', "ODD": '',
                                          "TrapDoorRJ45": '',
                                          "RegularAttendTime": RegularAttendTime,
                                          "RegressiveAttendTime": RegressiveAttendTime})
            # print(mock_data)
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
            Phasesortorder = {'B(FVT)': 0, 'C(SIT)': 1, }
            # print(Projectlist_top)
            Phaselist_top.sort(key=lambda x: Phasesortorder[x])
            for i in Projectlist_top:
                ProjecttotalATO = 0.00
                ProjecttotalRe = 0.00
                datainphase_normal = {}
                datainphase_retest = {}
                if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                    for j in AIO_tableData:#尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            ProjecttotalATO += j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            ProjecttotalRe += j["RegressiveAttendTime"]

                            datainphase_normal[j['Phase']] = j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            datainphase_retest[j['Phase']] = j["RegressiveAttendTime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]
                else:
                    for j in mock_data:  # 尽量减少数据库 的遍历次数，增加每次遍历的内容，提升性能
                        if j["Project"] == i:
                            # print(j["Project"],j["Phase"],j["RegularAttendTime"],type(j["RegularAttendTime"]))
                            ProjecttotalATO += j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            ProjecttotalRe += j["RegressiveAttendTime"]

                            datainphase_normal[j['Phase']] = j["RegularAttendTime"] + j["RegressiveAttendTime"]
                            datainphase_retest[j['Phase']] = j["RegressiveAttendTime"]
                    Projectlist_top_normal[i] = [round(ProjecttotalATO, 0), datainphase_normal]
                    Projectlist_top_retest[i] = [round(ProjecttotalRe, 0), datainphase_retest]

            # reverse为True从大到小
            top_normal = sorted(Projectlist_top_normal.items(), key=lambda x: x[1][0], reverse=True)
            top_retest = sorted(Projectlist_top_retest.items(), key=lambda x: x[1][0], reverse=True)
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
            if Customer == "C38(NB)-SMB":
                mock_data.insert(0, {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1", "Panel": "1", "Hinge": "1",
                 "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1", "SSD/HDD": "1", "Camera": "1",
                 "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "226.5", "RegressiveAttendTime": "0"})
                mock_data.insert(1,
                                 {"Project": "Standard1", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "2", "Panel": "6",
                                  "Hinge": "2",
                                  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2", "SSD/HDD": "6",
                                  "Camera": "3",
                                  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "576.5",
                                  "RegressiveAttendTime": "0"})
                mock_data.insert(2,
                                 {"Project": "Single-2", "ID": "1", "Type": "Yoga", "SKU": "1", "Planar": "1", "Panel": "1",
                                  "Hinge": "1",
                                  "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1", "SSD/HDD": "1",
                                  "Camera": "1",
                                  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "231.5",
                                  "RegressiveAttendTime": "0"})
                mock_data.insert(3,
                                 {"Project": "Standard2", "ID": "1", "Type": "Yoga", "SKU": "6", "Planar": "2", "Panel": "6",
                                  "Hinge": "2",
                                  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2", "SSD/HDD": "6",
                                  "Camera": "3",
                                  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "618.5",
                                  "RegressiveAttendTime": "0"})
            else:
                mock_data.insert(0, {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1",
                                     "Panel": "1", "Hinge": "1",
                                     "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1",
                                     "SSD/HDD": "1", "Camera": "1",
                                     "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "305.5",
                                     "RegressiveAttendTime": "0"})
                mock_data.insert(1,
                                 {"Project": "Standard1", "ID": "1", "Type": "Normal", "SKU": "6", "Planar": "2",
                                  "Panel": "6",
                                  "Hinge": "2",
                                  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2",
                                  "SSD/HDD": "6",
                                  "Camera": "3",
                                  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "700",
                                  "RegressiveAttendTime": "0"})
                mock_data.insert(2,
                                 {"Project": "Single-2", "ID": "1", "Type": "Yoga", "SKU": "1", "Planar": "1",
                                  "Panel": "1",
                                  "Hinge": "1",
                                  "Cable": "1", "Connectorsource": "1", "Keyboard": "1", "ClickPad": "1",
                                  "SSD/HDD": "1",
                                  "Camera": "1",
                                  "Rubberfoot": "1", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "328.5",
                                  "RegressiveAttendTime": "0"})
                mock_data.insert(3,
                                 {"Project": "Standard2", "ID": "1", "Type": "Yoga", "SKU": "6", "Planar": "2",
                                  "Panel": "6",
                                  "Hinge": "2",
                                  "Cable": "3", "Connectorsource": "2", "Keyboard": "6", "ClickPad": "2",
                                  "SSD/HDD": "6",
                                  "Camera": "3",
                                  "Rubberfoot": "2", "ODD": "0", "TrapDoorRJ45": "0", "RegularAttendTime": "855",
                                  "RegressiveAttendTime": "0"})
        AIO_tableData.insert(0, {"Project": "Single-1", "ID": "1", "Type": "Normal", "SKU": "1", "Planar": "1", "Panel": "1", "Stand": "1",
         "Cable": "1", "Connectorsource": "1", "SSD/HDD": "1", "Camera": "1", "ODD": "0", "Package": "1",
         "RegularAttendTime": "700", "RegressiveAttendTime": "0"})
        data = {
            "err_ok": "0",
            "content": mock_data,
            "AIO_tableData": AIO_tableData,
            "select": selectItem,
            "sear": searchalert,
            "Top10": Top10,
            "Execution_Top10": Execution_Top10,
            "Regression_Top10": Regression_Top10,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(data), content_type="application/json")

    return render(request, 'TestPlanME/TestPlanME_Summary.html', locals())

def TestPlanME_Edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/ME/Edit"
    mock_data = [
    ]
    combine = {
        # "C38(NB)": [{"customer": "ELMV2", "phase": [1, 2, 3]}, {"customer": "FLY00", "phase": [2, 3]},
        #             {"customer": "ELZP5", "phase": [1]}, {"customer": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"customer": "FLMS0", "phase": [1, 2, 3]}, {"customer": "FLMS1", "phase": [1, 2, 3]},
        #              {"customer": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"customer": "DLAE1", "phase": [1, 2, 3]}, {"customer": "DLAE2", "phase": [1, 2, 3]},
        #         {"customer": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"customer": "OTHER", "phase": [1, 2, 3]}]
    }
    Keypartlist = [
        #  {"Keypartname": "ID", "Keypartvalue": "1"},
        # {"Keypartname": "Type", "Keypartvalue": "1"},
        # {"Keypartname": "SKU", "Keypartvalue": "1"},
        # {"Keypartname": "Planar", "Keypartvalue": "2"},
        # {"Keypartname": "Panel", "Keypartvalue": "3"},
        # {"Keypartname": "Stand", "Keypartvalue": "4"},
        # {"Keypartname": "Cable", "Keypartvalue": "4"},
        # {"Keypartname": "Connectorsource", "Keypartvalue": "4"},
        # {"Keypartname": "SSD/HHD", "Keypartvalue": "4"},
        # {"Keypartname": "Camera", "Keypartvalue": "4"},
        # {"Keypartname": "ODD", "Keypartvalue": "4"},
        # {"Keypartname": "Package", "Keypartvalue": "4"},
        # {"Keypartname": "RegularAttendTime", "Keypartvalue": "4"},
        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": "4"}
    ]
    Customer_list = TestProjectME.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectME.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectME.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase']=="B(FVT)":
                    PhaseValue=0
                if m['Phase']=="C(SIT)":
                    PhaseValue=1
                if m['Phase']=="INV":
                    PhaseValue=2
                if m['Phase']=="Others":
                    PhaseValue=3
                phaselist.append(PhaseValue)
            Projectinfo['phase']=phaselist
            Projectinfo['Project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print(combine)
    # print(request.method)
    # print(request.GET)
    # print(request.POST)
    # print(str(request.body, encoding='utf-8'))

    if request.method == "GET":
        if request.GET.get("action") == "get":
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        if request.GET.get("action") == "search":
            # print(request.GET)
            Customer = request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            # print(type(Phase))
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'INV'
            if Phase == '3':
                Phase = 'Others'

            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            Projectinfos = TestProjectME.objects.filter(**dic_Project).first()
            # print(Projectinfos.Owner.all())
            canEdit=0
            current_user = request.session.get('user_name')
            for i in Projectinfos.Owner.all():
                # print(i.username,current_user)
                # print(type(i.username),type(current_user))
                if i.username==current_user:
                    canEdit=1
                    break
            # print(canEdit)

            itemlist = []
            for i in TestItemME.objects.filter(Customer=Customer):
                itemlist.append(i.id)
            # print (itemlist,'yyy')
            existitem=[]
            for i in Projectinfos.testplanme_set.all():
                existitem.append(i.Items.id)
            # print(existitem)
            for i in itemlist:
                if i in existitem:
                    continue
                else:
                    TestPlanME.objects.create(Items=TestItemME.objects.get(id=i), Projectinfo=TestProjectME.objects.filter(**dic_Project).first(),
                                              editor=request.session.get('user_name'),edit_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


            for i in  Projectinfos.testplanme_set.all().order_by('Items'):
                # print(i,type(i))
                TestPlanInfo = {}
                TestPlanInfo['ItemNo'] = i.Items.ItemNo_d
                TestPlanInfo['Item'] = i.Items.Item_d
                TestPlanInfo['Facility Name'] = i.Items.Facility_Name_d
                TestPlanInfo['Voltage (our)'] = i.Items.Voltage_d
                TestPlanInfo['Sample Size'] = i.Items.Sample_Size_d
                TestPlanInfo['TTF'] = i.Items.TimePunits_Facility_d
                TestPlanInfo['TTM'] = i.Items.TimePunits_Manual_d
                TestPlanInfo['TTP'] = i.Items.TimePunits_Program_d
                TestPlanInfo['NTU'] = i.NormalAmount
                TestPlanInfo['RTR'] = i.RegCycles
                TestPlanInfo['RTU'] = i.RegAmount
                mock_data.append(TestPlanInfo)
            # print (mock_data)
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
                'canEdit':canEdit
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")

    if request.method == "POST" :
        if request.POST:
            if request.POST.get("isGetData") == "openKeypart":
                Customer = request.POST.get("Customer")
                Project = request.POST.get("Project")
                Phase = request.POST.get('Phase')
                if Phase == '0':
                    Phase = 'B(FVT)'
                if Phase == '1':
                    Phase = 'C(SIT)'
                if Phase == '2':
                    Phase = 'INV'
                if Phase == '3':
                    Phase = 'Others'
                dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
                # print(dic_Project)
                if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                    if KeypartAIO.objects.filter(**dic_Project).first():
                        KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                        Keypartlist = [
                                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                                       {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                                       {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                                       {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                                       {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                                       {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                                       {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                                       {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                                       {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                                       {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                                       {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                                       {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                                       # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                                       # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                                       ]
                    else:
                        createFFRT = {
                            "Customer": Customer, "Project": Project, 'Phase': Phase, "IDs": "", "Type": "", "SKU": "", "Planar": "", "Panel": "",
                            "Stand": "", "Cable": "", "Connectorsource": "", "SSDHHD": "", "Camera": "", "ODD": "", "Package": "", "RegularAttendTime": "", "RegressiveAttendTime": "",
                        }
                        KeypartAIO.objects.create(**createFFRT)
                        KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                        Keypartlist = [
                            {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                            {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                            {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                            {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                            {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                            {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                            {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                            {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                            {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                            {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                            {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                            {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                            # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                            # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                        ]
                else:
                    if KeypartC38NB.objects.filter(**dic_Project).first():
                        KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                        Keypartlist = [
                                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                                       {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                                       {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                                       {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                                       {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                                       {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                                       {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                                       {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                                        {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                                        {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                                       {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                                       {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                                        {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                                       {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                                       {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                                       # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                                       # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                                       ]
                    else:
                        createFFRT = {
                            "Customer": Customer, "Project": Project, 'Phase': Phase, "IDs": "", "Type": "", "SKU": "", "Planar": "", "Panel": "",
                            "Hinge": "", "Cable": "", "Connectorsource": "", "Keyboard":"", "ClickPad":"", "SSDHHD": "", "Camera": "", "Rubberfoot":"",
                            "ODD": "", "TrapDoorRJ45": "", "RegularAttendTime": "", "RegressiveAttendTime": "",
                        }
                        KeypartC38NB.objects.create(**createFFRT)
                        KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                        Keypartlist = [
                            {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                            {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                            {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                            {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                            {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                            {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                            {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                            {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                            {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                            {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                            {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                            {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                            {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                            {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                            {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                            # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                            # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                        ]
                canEdit = 0
                current_user = request.session.get('user_name')
                if TestProjectME.objects.filter(**dic_Project).first():
                    for h in TestProjectME.objects.filter(**dic_Project):
                        for i in h.Owner.all():
                            # print(i.username,current_user)
                            # print(type(i.username),type(current_user))
                            if i.username == current_user:
                                canEdit = 1
                                break
                updateData = {
                    "MockData": mock_data,
                    "selectMsg": combine,
                    "Keypartlist": Keypartlist,
                }
                return HttpResponse(json.dumps(updateData), content_type="application/json")
            if request.POST.get("isGetData") == "SAVE":
                Customer = request.POST.get("Customer")
                Project = request.POST.get("Project")
                Phase = request.POST.get('Phase')
                if Phase == '0':
                    Phase = 'B(FVT)'
                if Phase == '1':
                    Phase = 'C(SIT)'
                if Phase == '2':
                    Phase = 'INV'
                if Phase == '3':
                    Phase = 'Others'
                dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}

                Keypartname = request.POST.get("rows[Keypartname]")
                Keypartvalue = request.POST.get("rows[Keypartvalue]")
                # print(Customer)

                if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                    updatedic = {}
                    updatedic[Keypartname] = Keypartvalue
                    if KeypartAIO.objects.filter(**dic_Project).first():#edit

                        KeypartAIO.objects.filter(**dic_Project).update(**updatedic)

                    KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                    Keypartlist = [
                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                        {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                        {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                        {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                        {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                        {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                        {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                        {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                        {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                        {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                        {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                        {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                        # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                    ]
                else:
                    updatedic = {}
                    if Keypartname == "ODD(Option)":
                        Keypartname = "ODD"
                    if Keypartname == "Trap Door RJ45(Option)":
                        Keypartname = "TrapDoorRJ45"
                    updatedic[Keypartname] = Keypartvalue
                    if KeypartC38NB.objects.filter(**dic_Project).first():  # edit

                        KeypartC38NB.objects.filter(**dic_Project).update(**updatedic)
                        KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                        Keypartlist = [
                            {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                            {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                            {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                            {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                            {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                            {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                            {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                            {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                            {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                            {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                            {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                            {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                            {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                            {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                            {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                            # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                            # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                        ]
                updateData = {
                    "MockData": mock_data,
                    "selectMsg": combine,
                    "Keypartlist": Keypartlist,
                }
                return HttpResponse(json.dumps(updateData), content_type="application/json")
        else:
            #str(request.body, encoding='utf-8')
            # print (str(request.body, encoding='utf-8'))
            # print(json.loads(request.body))

            # print(responseData)
            # print(request.body)
            try:
                responseData = json.loads(request.body)
            except:
                pass
            else:
                if 'ExcelData' in responseData.keys():
                    if responseData:
                        # print(responseData['Projectinfo'][2])
                        if responseData['Projectinfo'][2] == 0:
                            Phase = 'B(FVT)'
                        if responseData['Projectinfo'][2] == 1:
                            Phase = 'C(SIT)'
                        if responseData['Projectinfo'][2] == 2:
                            Phase = 'INV'
                        if responseData['Projectinfo'][2] == 3:
                            Phase = 'Others'
                        dic_Project = {'Customer': responseData['Projectinfo'][0],
                                       'Project': responseData['Projectinfo'][1], 'Phase': Phase}
                        # print(dic_Project)
                        item_nodata=[]
                        itemindata=[]
                        for i in TestItemME.objects.all():
                            itemindata.append(i.ItemNo_d)
                            # print(itemindata)
                        for i in responseData['ExcelData']:
                            # print(type(i['phase']))
                            # print(i)
                            if i['Item No.'] in itemindata:
                                itemsinfo = TestItemME.objects.get(Customer=responseData['Projectinfo'][0],ItemNo_d=i['Item No.'])

                                Projectinfos = TestProjectME.objects.filter(**dic_Project).first()
                                editplan=TestPlanME.objects.filter(Items=itemsinfo,Projectinfo=Projectinfos).first()
                                # print(type(editplan))
                                if 'NormalAmount' in i.keys():
                                    editplan.NormalAmount=i['NormalAmount']
                                if 'NormalFacilityTime' in i.keys():
                                    editplan.NormalFacilityTime = i['NormalFacilityTime']
                                if 'NormalAttendTime' in i.keys():
                                    editplan.NormalAttendTime = i['NormalAttendTime']
                                if 'NormalProgramtime' in i.keys():
                                    editplan.NormalProgramtime = i['NormalProgramtime']
                                if 'RegCycles' in i.keys():
                                    editplan.RegCycles = i['RegCycles']
                                if 'RegAmount' in i.keys():
                                    editplan.RegAmount = i['RegAmount']
                                if 'RegFacilityTime' in i.keys():
                                    editplan.RegFacilityTime = i['RegFacilityTime']
                                if 'RegAttendTime' in i.keys():
                                    editplan.RegAttendTime = i['RegAttendTime']
                                if 'RegProgramtime' in i.keys():
                                    editplan.RegProgramtime = i['RegProgramtime']
                                editplan.editor = request.session.get('user_name')
                                editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                editplan.save()
                            else:
                                item_nodata.append(i['Item No.'])
                        # print (item_nodata)
                        Projectinfos = TestProjectME.objects.filter(**dic_Project).first()
                        for i in Projectinfos.testplanme_set.all().order_by('Items'):
                            TestPlanInfo = {}
                            TestPlanInfo['ItemNo'] = i.Items.ItemNo_d
                            TestPlanInfo['Item'] = i.Items.Item_d
                            TestPlanInfo['Facility Name'] = i.Items.Facility_Name_d
                            TestPlanInfo['Voltage (our)'] = i.Items.Voltage_d
                            TestPlanInfo['Sample Size'] = i.Items.Sample_Size_d
                            TestPlanInfo['TTF'] = i.Items.TimePunits_Facility_d
                            TestPlanInfo['TTM'] = i.Items.TimePunits_Manual_d
                            TestPlanInfo['TTP'] = i.Items.TimePunits_Program_d
                            TestPlanInfo['NTU'] = i.NormalAmount
                            TestPlanInfo['RTR'] = i.RegCycles
                            TestPlanInfo['RTU'] = i.RegAmount
                            mock_data.append(TestPlanInfo)
                        updateData = {
                            "MockData": mock_data,
                            "selectMsg": combine,
                            'canEdit': 1
                        }

                        return HttpResponse(json.dumps(updateData), content_type="application/json")
                if 'uploadData' in json.loads(request.body):
                    if responseData:
                        if responseData['uploadData'][0]['phase'] == 0:
                            Phase = 'B(FVT)'
                        if responseData['uploadData'][0]['phase'] == 1:
                            Phase = 'C(SIT)'
                        if responseData['uploadData'][0]['phase'] == 2:
                            Phase = 'INV'
                        if responseData['uploadData'][0]['phase'] == 3:
                            Phase = 'Others'
                        dic_Project = {'Customer': responseData['uploadData'][0]['customer'] , 'Project': responseData['uploadData'][0]['project'] , 'Phase': Phase}
                        for i in responseData['uploadData']:
                            # print(type(i['phase']))
                            # print(i)
                            Projectinfos = TestProjectME.objects.filter(**dic_Project).first()
                            itemsinfo=TestItemME.objects.get(Customer=responseData['uploadData'][0]['customer'], ItemNo_d=i['itemNo'])
                            editplan=TestPlanME.objects.filter(Items=itemsinfo, Projectinfo=Projectinfos).first()
                            # print(type(editplan))
                            editplan.NormalAmount=i['NTU']
                            editplan.NormalFacilityTime = i['NTF']
                            editplan.NormalAttendTime = i['NTA']
                            editplan.NormalProgramtime = i['NTP']
                            editplan.RegCycles = i['RTR']
                            editplan.RegAmount = i['RTU']
                            editplan.RegFacilityTime = i['RTF']
                            editplan.RegAttendTime = i['RTA']
                            editplan.RegProgramtime = i['RTP']
                            editplan.editor = request.session.get('user_name')
                            editplan.edit_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            editplan.save()
                        Projectinfos = TestProjectME.objects.filter(**dic_Project).first()
                        for i in Projectinfos.testplanme_set.all().order_by('Items'):
                            TestPlanInfo = {}
                            TestPlanInfo['ItemNo'] = i.Items.ItemNo_d
                            TestPlanInfo['Item'] = i.Items.Item_d
                            TestPlanInfo['Facility Name'] = i.Items.Facility_Name_d
                            TestPlanInfo['Voltage (our)'] = i.Items.Voltage_d
                            TestPlanInfo['Sample Size'] = i.Items.Sample_Size_d
                            TestPlanInfo['TTF'] = i.Items.TimePunits_Facility_d
                            TestPlanInfo['TTM'] = i.Items.TimePunits_Manual_d
                            TestPlanInfo['TTP'] = i.Items.TimePunits_Program_d
                            TestPlanInfo['NTU'] = i.NormalAmount
                            TestPlanInfo['RTR'] = i.RegCycles
                            TestPlanInfo['RTU'] = i.RegAmount
                            mock_data.append(TestPlanInfo)
                        # print (mock_data)
                        updateData = {
                            "MockData": mock_data,
                            "selectMsg": combine,
                            'canEdit': 1
                        }

                    return HttpResponse(json.dumps(updateData), content_type="application/json")




    return render(request, 'TestPlanME/TestPlanME_edit.html', locals())
#TestPlan_ME search
def TestPlanME_search(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    mock_data = [
    #     {
    #     "ItemNo": "H1-1", "Item": "Basic Function Check", "Facility Name": "N/A", "Voltage (our)": "N/A",
    #     "Sample Size": "All units", "TTF": 0, "TTM": 1, "TTP": 1, "NTU": 12, "RTR": 0, "RTU": 12
    # }, {
    #     "ItemNo": "H1-2", "Item": "Structure Analysis Test", "Facility Name": "N/A", "Voltage (our)": "N/A",
    #     "Sample Size": "At least 10 units", "TTF": 0, "TTM": 4, "TTP": 0, "NTU": 10, "RTR": 0, "RTU": 12
    # }, {
    #     "ItemNo": "H1-3", "Item": "Operation Temp/Hum Cycle Test", "Facility Name": "恆溫恆濕試驗機", "Voltage (our)": "12000",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 80, "TTM": 1, "TTP": 0.5, "NTU": 23, "RTR": 7, "RTU": 12
    # }, {
    #     "ItemNo": "H1-4", "Item": "Storage Temp/Hum Test", "Facility Name": "恆溫恆濕試驗機", "Voltage (our)": "12000",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 96, "TTM": 1, "TTP": 0.5, "NTU": 5, "RTR": 7, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #1-1", "Item": "Cold start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 19, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 6, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #1-1", "Item": "Cold start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 19, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 5, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #2-1", "Item": "Hot start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 9, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 3, "RTU": 12
    # }, {
    #     "ItemNo": "H1-5 #2-1", "Item": "Hot start Test-AC", "Facility Name": "步入式恆溫恆濕試驗機", "Voltage (our)": "28500",
    #     "Sample Size": "2unit/SKU (At least 6 units)", "TTF": 9, "TTM": 5, "TTP": 2, "NTU": 22, "RTR": 0, "RTU": 6
    # }, {
    #     "ItemNo": "H1-6", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 7
    # }, {
    #     "ItemNo": "H1-4", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 3
    # }, {
    #     "ItemNo": "H1-33", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 8, "TTM": 8, "TTP": 0, "NTU": 22, "RTR": 0, "RTU": 6
    # }, {
    #     "ItemNo": "H1-34", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 0, "TTM": 0.5, "TTP": 1, "NTU": 22, "RTR": 0, "RTU": 5
    # }, {
    #     "ItemNo": "H1-30", "Item": "Brightness test", "Facility Name": "亮度儀", "Voltage (our)": "2200",
    #     "Sample Size": "2units/SKU", "TTF": 5, "TTM": 1, "TTP": 0.5, "NTU": 22, "RTR": 0, "RTU": 12
    # },
    ]
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/ME/Search"
    selectItem1 = [
        # "C38(NB)", "C38(AIO)", "A39", "Other"
    ]
    combine = {
        # "C38(NB)": [{"customer": "ELMV2", "phase": [1, 2, 3]}, {"customer": "FLY00", "phase": [2, 3]},
        #             {"customer": "ELZP5", "phase": [1]}, {"customer": "ELZP7", "phase": [1, 2, 3]}],
        # "C38(AIO)": [{"customer": "FLMS0", "phase": [1, 2, 3]}, {"customer": "FLMS1", "phase": [1, 2, 3]},
        #              {"customer": "FLMS2", "phase": [1, 2, 3]}],
        # "A39": [{"customer": "DLAE1", "phase": [1, 2, 3]}, {"customer": "DLAE2", "phase": [1, 2, 3]},
        #         {"customer": "DLAE3", "phase": [1, 2, 3]}],
        # "Other": [{"customer": "OTHER", "phase": [1, 2, 3]}]
    }
    proinfomation = [
        # {"YEAR": "Y2019", "COMPRJCODE": "FLMA0", "CUSPRJCODE": "Taurus",
        #  "PROJECT": "For Worldwide:IdeaPad5(14,05)For China:Lenovo 小新Air-14IIL 2020", "SIZE": "14", "CPU": "AMD",
        #  "PLATFORM": "AMD Renoir", "VGA": "UMA", "OS SUPPORT": "WIN10 19H2", "SS": "2020-03-16", "LD": "王青",
        #  "DQA PL": "张亚萍", "MODIFIED DATE": "2020-01-18"},
    ]
    Sums={
        # 'NTUSum': 465, 'NTFSum':{'value':4462.5,'name':'Non-Attend time'}, 'NTASum': {'value':507,'name':'Attend time'}, 'NTPSum': 420, 'RTRSum': 3, 'RTUSum': 76, 'RTFSum': {'value':1089.3,'name':'Non-Attend time'},'RTASum':{'value':107.8,'name':'Attend time'},'RTPSum':53,
        #  'TOPRegression_key': ["H1-1:Basic Function Check", "H1-2:Structure Analysis Test","H1-3:Operation Temp/Hum Cycle Test","H1-4:Storage Temp/Hum Test","H1-24:CDM test","H1-25:KB feeling measurement Test","H1-12:Weight Drop Test","H1-29:Operating Force Measurement","H1-21 #2:LCD Enclosure Pressure Test(static stress)","H1-20:Pressure Test"],
        #  'TOPRegression_value': [1, 1, 1, 1, 2, 2, 2, 2, 2, 3]
         }
    Keypartlist = [
        #  {"Keypartname": "ID", "Keypartvalue": "1"},
        # {"Keypartname": "Type", "Keypartvalue": "1"},
        # {"Keypartname": "SKU", "Keypartvalue": "1"},
        # {"Keypartname": "Planar", "Keypartvalue": "2"},
        # {"Keypartname": "Panel", "Keypartvalue": "3"},
        # {"Keypartname": "Stand", "Keypartvalue": "4"},
        # {"Keypartname": "Cable", "Keypartvalue": "4"},
        # {"Keypartname": "Connectorsource", "Keypartvalue": "4"},
        # {"Keypartname": "SSD/HHD", "Keypartvalue": "4"},
        # {"Keypartname": "Camera", "Keypartvalue": "4"},
        # {"Keypartname": "ODD", "Keypartvalue": "4"},
        # {"Keypartname": "Package", "Keypartvalue": "4"},
        # {"Keypartname": "RegularAttendTime", "Keypartvalue": "4"},
        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": "4"}
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
    Customer_list = TestProjectME.objects.all().values('Customer').distinct().order_by('Customer')

    for i in Customer_list:
        Customerlist = []
        for j in TestProjectME.objects.filter(Customer=i['Customer']).values('Project').distinct().order_by('Project'):
            Projectinfo = {}
            phaselist = []
            dic = {'Customer': i['Customer'], 'Project': j['Project']}
            for m in TestProjectME.objects.filter(**dic).values('Phase').distinct().order_by('Phase'):

                if m['Phase'] == "B(FVT)":
                    PhaseValue = 0
                if m['Phase'] == "C(SIT)":
                    PhaseValue = 1
                if m['Phase'] == "INV":
                    PhaseValue = 2
                if m['Phase'] == "Others":
                    PhaseValue = 3
                phaselist.append(PhaseValue)
            Projectinfo['phase'] = phaselist
            Projectinfo['Project'] = j['Project']
            Customerlist.append(Projectinfo)
        combine[i['Customer']] = Customerlist
    # print(combine)
    # print(request.method)
    # print(request.GET)
    if request.method == "GET":
        if request.GET.get("action") == "get":
            # TestPlanMEs = TestPlanME.objects.all().order_by('Items')
            #
            # for i in TestPlanMEs:
            #     TestPlanInfo = {}
            #     TestPlanInfo['ItemNo'] = i.Items.ItemNo_d
            #     TestPlanInfo['Item'] = i.Items.Item_d
            #     TestPlanInfo['Facility Name'] = i.Items.Facility_Name_d
            #     TestPlanInfo['Voltage (our)'] = i.Items.Voltage_d
            #     TestPlanInfo['Sample Size'] = i.Items.Sample_Size_d
            #     TestPlanInfo['TTF'] = i.Items.TimePunits_Facility_d
            #     TestPlanInfo['TTM'] = i.Items.TimePunits_Manual_d
            #     TestPlanInfo['TTP'] = i.Items.TimePunits_Program_d
            #     TestPlanInfo['NTU'] = i.NormalAmount
            #     TestPlanInfo['RTR'] = i.RegCycles
            #     TestPlanInfo['RTU'] = i.RegAmount
            #     mock_data.append(TestPlanInfo)
            # # print (mock_data)
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
        if request.GET.get("action") == "search":
            Customer=request.GET.get('customer')
            Project = request.GET.get('project')
            Phase = request.GET.get('phase')
            if Phase=='0':
                Phase='B(FVT)'
            if Phase=='1':
                Phase='C(SIT)'
            if Phase=='2':
                Phase='INV'
            if Phase=='3':
                Phase='Others'

            dic_Project={'Customer':Customer,'Project':Project,'Phase':Phase}
            # print(dic_Project)
            Projectinfos=TestProjectME.objects.filter(**dic_Project).first()
            # print(Projectinfos)
            TestPlanMEs=Projectinfos.testplanme_set.all().order_by('Items')

            Sums = {}
            # NTUSum = 0.00
            # NTFSum = 0.00
            # NTASum = 0.00
            # NTPSum = 0.00
            # RTRMax = 0.00
            # RTUSum = 0.00
            # RTFSum = 0.00
            # RTASum = 0.00
            # RTPSum = 0.00

            # print(RTRMax)
            Sums['NTUSum'] = TestPlanMEs.aggregate(Sum('NormalAmount'))['NormalAmount__sum']
            Sums['NTFSum'] = TestPlanMEs.aggregate(Sum('NormalFacilityTime'))['NormalFacilityTime__sum']
            Sums['NTASum'] = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
            Sums['NTPSum'] = TestPlanMEs.aggregate(Sum('NormalProgramtime'))['NormalProgramtime__sum']
            Sums['RTRSum'] = TestPlanMEs.aggregate(Max('RegCycles'))['RegCycles__max']
            Sums['RTUSum'] = TestPlanMEs.aggregate(Sum('RegAmount'))['RegAmount__sum']
            Sums['RTFSum'] = TestPlanMEs.aggregate(Sum('RegFacilityTime'))['RegFacilityTime__sum']
            Sums['RTASum'] = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
            Sums['RTPSum'] = TestPlanMEs.aggregate(Sum('RegProgramtime'))['RegProgramtime__sum']
            # Top ten cycles Items Sums["Topregresion"]={"No. 1": 4}
            courses = TestPlanMEs.order_by('-RegCycles').values('Items__ItemNo_d', 'Items__Item_d', 'RegCycles')
            TopRegression = {}
            count = 1
            for i in courses:
                # print(i)
                if count > 10:
                    break
                else:
                    key = i["Items__ItemNo_d"] + ":" + i["Items__Item_d"]
                    TopRegression[key] = i["RegCycles"]
                count += 1
            # print(TopRegression)
            for i in TopRegression:
                if not TopRegression[i]:
                    TopRegression[i] = 0
            TOPRegression_list = sorted(TopRegression.items(), key=lambda x: x[1], reverse=False)
            # print(TOPRegression_list)s
            TOPRegression_listvalue = []
            TOPRegression_listkey = []
            for i in TOPRegression_list:
                TOPRegression_listvalue.append(i[1])
                TOPRegression_listkey.append(i[0])
            # print(TOPRegression_listvalue)
            # print(TOPRegression_listkey)
            # print(Sums)
            Sums["TOPRegression_value"] = TOPRegression_listvalue
            Sums["TOPRegression_key"] = TOPRegression_listkey
            for i in TestPlanMEs:
                TestPlanInfo = {}
                TestPlanInfo['ItemNo'] = i.Items.ItemNo_d
                TestPlanInfo['Item'] = i.Items.Item_d
                TestPlanInfo['Facility Name'] = i.Items.Facility_Name_d
                TestPlanInfo['Voltage (our)'] = i.Items.Voltage_d
                TestPlanInfo['Sample Size'] = i.Items.Sample_Size_d
                TestPlanInfo['TTF'] = i.Items.TimePunits_Facility_d
                TestPlanInfo['TTM'] = i.Items.TimePunits_Manual_d
                TestPlanInfo['TTP'] = i.Items.TimePunits_Program_d
                TestPlanInfo['NTU'] = i.NormalAmount
                TestPlanInfo['NTF'] = i.NormalFacilityTime
                TestPlanInfo['NTA'] = i.NormalAttendTime
                TestPlanInfo['NTP'] = i.NormalProgramtime
                TestPlanInfo['RTR'] = i.RegCycles
                TestPlanInfo['RTU'] = i.RegAmount
                TestPlanInfo['RTF'] = i.RegFacilityTime
                TestPlanInfo['RTA'] = i.RegAttendTime
                TestPlanInfo['RTP'] = i.RegProgramtime
                mock_data.append(TestPlanInfo)
            TTFTotal = 0
            TTMTotal = 0
            TTPTotal = 0
            SampleTotal = 0
            for i in mock_data:
                if i['TTF']:
                    TTFTotal = TTFTotal + float(i['TTF'])
                if i['TTM']:
                    TTMTotal = TTMTotal + float(i['TTM'])
                if i['TTP']:
                    TTPTotal = TTPTotal + float(i['TTP'])
            mock_data.insert(0, {'ItemNo': 'Total',
                                 'TTF': TTFTotal,
                                 'TTM': TTMTotal,
                                 'TTP': TTPTotal,
                                 'NTU': round(TestPlanMEs.aggregate(Sum('NormalAmount'))['NormalAmount__sum'], 2),
                                 'NTF': round(TestPlanMEs.aggregate(Sum('NormalFacilityTime'))['NormalFacilityTime__sum'], 2),
                                 'NTA': round(TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum'], 2),
                                 'NTP': round(TestPlanMEs.aggregate(Sum('NormalProgramtime'))['NormalProgramtime__sum'], 2),
                                 'RTR': round(TestPlanMEs.aggregate(Max('RegCycles'))['RegCycles__max'], 2),
                                 'RTU': round(TestPlanMEs.aggregate(Sum('RegAmount'))['RegAmount__sum'], 2),
                                 'RTF': round(TestPlanMEs.aggregate(Sum('RegFacilityTime'))['RegFacilityTime__sum'], 2),
                                 'RTA': round(TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum'], 2),
                                 'RTP': round(TestPlanMEs.aggregate(Sum('RegProgramtime'))['RegProgramtime__sum'], 2),
                                 })


            # print (mock_data)
            print(Sums)
            canEdit = 0
            current_user = request.session.get('user_name')
            if TestProjectME.objects.filter(**dic_Project).first():
                for h in TestProjectME.objects.filter(**dic_Project):
                    for i in h.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if i.username == current_user:
                            canEdit = 1
                            break
            updateData = {
                "MockData": mock_data,
                "selectMsg": combine,
                'Sum': Sums,
                'canEdit': canEdit,
            }
            return HttpResponse(json.dumps(updateData), content_type="application/json")
    if request.method == "POST":
        if request.POST.get("isGetData") == "first":
            for i in TestProjectME.objects.all().values("Customer").distinct().order_by('Customer'):
                selectItem1.append(i["Customer"])
        if request.POST.get("isGetData") == "searchalert":
            Customer = request.POST.get("Customer")
            Prolist = []
            # print(Customer)
            if Customer:
                for i in TestProjectME.objects.filter(Customer=Customer).values("Project").distinct().order_by(
                        "Project"):
                    Prolist.append({"Project": i["Project"]})
            else:
                for i in TestProjectME.objects.all().values("Project").distinct().order_by("Project"):
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
                        # print(i['Project'], i['Project'][0:5], i['Project'][0:3], i['Project'][5:])
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
            Phaselist = []
            if TestProjectME.objects.filter(**check_dic_Pro).first():
                for i in TestProjectME.objects.filter(**check_dic_Pro).values("Phase").order_by("-Phase"):
                    Phaselist.append(i["Phase"])
                Time_value_Re = []
                Time_value_Re_ATO = []
                for i in Phaselist:
                    check_dic_Phase = {"Customer": Customer, "Project": Project, "Phase":i}
                    Projectinfos = TestProjectME.objects.filter(**check_dic_Phase).first()
                    # print(Projectinfos)
                    TestPlanMEs = Projectinfos.testplanme_set.all().order_by('Items')
                    Sums = {}

                    if TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']:
                        NAT = TestPlanMEs.aggregate(Sum('NormalAttendTime'))['NormalAttendTime__sum']
                    else:
                        NAT = 0
                    if TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']:
                        RAT = TestPlanMEs.aggregate(Sum('RegAttendTime'))['RegAttendTime__sum']
                    else:
                        RAT = 0
                    Time_value_Re.append(round(NAT, 0))
                    Time_value_Re_ATO.append(round(RAT, 0))
                Time_key = Phaselist
                Project_ReTotal = 0
                for i in Time_value_Re:
                    Project_ReTotal += i
                Time_value_Re.append(round(Project_ReTotal, 0))
                Project_ATOTotal = 0
                for i in Time_value_Re_ATO:
                    Project_ATOTotal += i
                Time_value_Re_ATO.append(round(Project_ATOTotal, 0))
                Time_key.append("Total")
                Sums["Time_value"] = [Time_value_Re_ATO, Time_value_Re]
                Sums["Time_key"] = Time_key

                courses = TestPlanME.objects.filter(Projectinfo__Customer=Customer,Projectinfo__Project=Project).order_by('-RegCycles').values("Projectinfo__Phase", 'Items__ItemNo_d', 'Items__Item_d', 'RegCycles')
                TopRegression = {}
                count = 1
                for i in courses:
                    # print(i)
                    if count > 10:
                        break
                    else:
                        key = i["Projectinfo__Phase"] + ":" + i["Items__ItemNo_d"] + ":" + i["Items__Item_d"]
                        TopRegression[key] = i["RegCycles"]
                    count += 1
                # print(TopRegression)
                for i in TopRegression:
                    if not TopRegression[i]:
                        TopRegression[i] = 0
                TOPRegression_list = sorted(TopRegression.items(), key=lambda x: x[1], reverse=False)
                # print(TOPRegression_list)s
                TOPRegression_listvalue = []
                TOPRegression_listkey = []
                for i in TOPRegression_list:
                    TOPRegression_listvalue.append(i[1])
                    TOPRegression_listkey.append(i[0])
                # print(TOPRegression_listvalue)
                # print(TOPRegression_listkey)
                # print(Sums)
                Sums["TOPRegression_value"] = TOPRegression_listvalue
                Sums["TOPRegression_key"] = TOPRegression_listkey
        if request.POST.get("isGetData") == "openKeypart":
            Customer = request.POST.get("Customer")
            Project = request.POST.get("Project")
            Phase = request.POST.get('Phase')
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'INV'
            if Phase == '3':
                Phase = 'Others'
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}
            # print(dic_Project)
            if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                if KeypartAIO.objects.filter(**dic_Project).first():
                    KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                    Keypartlist = [
                                    {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                                   {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                                   {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                                   {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                                   {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                                   {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                                   {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                                   {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                                   {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                                   {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                                   {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                                   {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                                   # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                                   # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                                   ]
                else:
                    createFFRT = {
                        "Customer": Customer, "Project": Project, 'Phase': Phase, "IDs": "", "Type": "", "SKU": "", "Planar": "", "Panel": "",
                        "Stand": "", "Cable": "", "Connectorsource": "", "SSDHHD": "", "Camera": "", "ODD": "", "Package": "", "RegularAttendTime": "", "RegressiveAttendTime": "",
                    }
                    KeypartAIO.objects.create(**createFFRT)
                    KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                    Keypartlist = [
                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                        {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                        {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                        {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                        {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                        {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                        {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                        {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                        {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                        {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                        {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                        {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                        # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                    ]
            else:
                if KeypartC38NB.objects.filter(**dic_Project).first():
                    KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                    Keypartlist = [
                                    {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                                   {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                                   {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                                   {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                                   {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                                   {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                                   {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                                   {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                                    {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                                    {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                                   {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                                   {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                                    {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                                   {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                                   {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                                   # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                                   # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                                   ]
                else:
                    createFFRT = {
                        "Customer": Customer, "Project": Project, 'Phase': Phase, "IDs": "", "Type": "", "SKU": "", "Planar": "", "Panel": "",
                        "Hinge": "", "Cable": "", "Connectorsource": "", "Keyboard":"", "ClickPad":"", "SSDHHD": "", "Camera": "", "Rubberfoot":"",
                        "ODD": "", "TrapDoorRJ45": "", "RegularAttendTime": "", "RegressiveAttendTime": "",
                    }
                    KeypartC38NB.objects.create(**createFFRT)
                    KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                    Keypartlist = [
                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                        {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                        {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                        {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                        {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                        {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                        {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                        {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                        {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                        {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                        {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                        {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                        {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                        {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                        {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                        # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                    ]
            canEdit = 0
            current_user = request.session.get('user_name')
            if TestProjectME.objects.filter(**dic_Project).first():
                for h in TestProjectME.objects.filter(**dic_Project):
                    for i in h.Owner.all():
                        # print(i.username,current_user)
                        # print(type(i.username),type(current_user))
                        if i.username == current_user:
                            canEdit = 1
                            break
        if request.POST.get("isGetData") == "SAVE":
            Customer = request.POST.get("Customer")
            Project = request.POST.get("Project")
            Phase = request.POST.get('Phase')
            if Phase == '0':
                Phase = 'B(FVT)'
            if Phase == '1':
                Phase = 'C(SIT)'
            if Phase == '2':
                Phase = 'INV'
            if Phase == '3':
                Phase = 'Others'
            dic_Project = {'Customer': Customer, 'Project': Project, 'Phase': Phase}

            Keypartname = request.POST.get("rows[Keypartname]")
            Keypartvalue = request.POST.get("rows[Keypartvalue]")
            # print(Customer)

            if "C38(AIO)" in Customer or "T88(AIO)" in Customer:
                updatedic = {}
                updatedic[Keypartname] = Keypartvalue
                if KeypartAIO.objects.filter(**dic_Project).first():#edit

                    KeypartAIO.objects.filter(**dic_Project).update(**updatedic)

                KeyPart = KeypartAIO.objects.filter(**dic_Project).first()
                Keypartlist = [
                    {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                    {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                    {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                    {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                    {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                    {"Keypartname": "Stand", "Keypartvalue": KeyPart.Stand},
                    {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                    {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                    {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                    {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                    {"Keypartname": "ODD", "Keypartvalue": KeyPart.ODD},
                    {"Keypartname": "Package", "Keypartvalue": KeyPart.Package},
                    # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                    # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                ]
            else:
                updatedic = {}
                if Keypartname == "ODD(Option)":
                    Keypartname = "ODD"
                if Keypartname == "Trap Door RJ45(Option)":
                    Keypartname = "TrapDoorRJ45"
                updatedic[Keypartname] = Keypartvalue
                if KeypartC38NB.objects.filter(**dic_Project).first():  # edit

                    KeypartC38NB.objects.filter(**dic_Project).update(**updatedic)
                    KeyPart = KeypartC38NB.objects.filter(**dic_Project).first()
                    Keypartlist = [
                        {"Keypartname": "IDs", "Keypartvalue": KeyPart.IDs},
                        {"Keypartname": "Type", "Keypartvalue": KeyPart.Type},
                        {"Keypartname": "SKU", "Keypartvalue": KeyPart.SKU},
                        {"Keypartname": "Planar", "Keypartvalue": KeyPart.Planar},
                        {"Keypartname": "Panel", "Keypartvalue": KeyPart.Panel},
                        {"Keypartname": "Hinge", "Keypartvalue": KeyPart.Hinge},
                        {"Keypartname": "Cable", "Keypartvalue": KeyPart.Cable},
                        {"Keypartname": "Connectorsource", "Keypartvalue": KeyPart.Connectorsource},
                        {"Keypartname": "Keyboard", "Keypartvalue": KeyPart.Keyboard},
                        {"Keypartname": "ClickPad", "Keypartvalue": KeyPart.ClickPad},
                        {"Keypartname": "SSDHHD", "Keypartvalue": KeyPart.SSDHHD},
                        {"Keypartname": "Camera", "Keypartvalue": KeyPart.Camera},
                        {"Keypartname": "Rubberfoot", "Keypartvalue": KeyPart.Rubberfoot},
                        {"Keypartname": "ODD(Option)", "Keypartvalue": KeyPart.ODD},
                        {"Keypartname": "Trap Door RJ45(Option)", "Keypartvalue": KeyPart.TrapDoorRJ45},
                        # {"Keypartname": "RegularAttendTime", "Keypartvalue": KeyPart.RegularAttendTime},
                        # {"Keypartname": "RegressiveAttendTime", "Keypartvalue": KeyPart.RegressiveAttendTime}
                    ]


        updateData = {
            "MockData": mock_data,
            "selectMsg": combine,
            "select1": selectItem1,
            "proinfomation": proinfomation,
            'Sum': Sums,
            "Keypartlist": Keypartlist,
            'canExport': canExport,
        }
        return HttpResponse(json.dumps(updateData), content_type="application/json")

    return render(request, 'TestPlanME/TestPlanME_search.html', locals())

def ItemME_upload(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "TestPlan/ME/Itemload"

    MEItem_lists = [{'ItemNo_d': 'ItemNo_d', 'Item_d': 'Item_d'}]

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
                MEItem_dic = {}
                # print(i)
                # print (i['Customer'])
                check_dic = {"Customer": i['Customer'], 'ItemNo_d': i['ItemNo_d']}
                # print(check_dic)
                check_list = TestItemME.objects.filter(**check_dic)
                # print (check_list)
                if check_list:
                    j+=1
                    err_ok = 1
                    MEItem_dic['ItemNo_d']=i['ItemNo_d']
                    MEItem_dic['Item_d'] = i['Item_d']
                    MEItem_lists.append(MEItem_dic)
                    continue
                else:
                    # print('save')
                    k+=1
                    Itemmodel = TestItemME()
                    if 'ItemNo_d' in i.keys():
                        Itemmodel.ItemNo_d = i['ItemNo_d']
                    if 'Item_d' in i.keys():
                        Itemmodel.Item_d = i['Item_d']
                    if 'Customer' in i.keys():
                        Itemmodel.Customer = i['Customer']
                    if 'Phase' in i.keys():
                        Itemmodel.Phase = i['Phase']
                    if 'Facility_Name_d' in i.keys():
                        Itemmodel.Facility_Name_d = i['Facility_Name_d']
                    if 'Voltage_d' in i.keys():
                        Itemmodel.Voltage_d = i['Voltage_d']
                    if 'Sample_Size_d' in i.keys():
                        Itemmodel.Sample_Size_d = i['Sample_Size_d']
                    if 'TimePunits_Facility_d' in i.keys():
                        Itemmodel.TimePunits_Facility_d = i['TimePunits_Facility_d']
                    if 'TimePunits_Manual_d' in i.keys():
                        Itemmodel.TimePunits_Manual_d = i['TimePunits_Manual_d']
                    if 'TimePunits_Program_d' in i.keys():
                        Itemmodel.TimePunits_Program_d = i['TimePunits_Program_d']
                    Itemmodel.save()
                    # print('ttt')
            # if not message_CDM:
            #     message_CDM = "Upload Successfully"
            # print(message_CDM)
            # print(n,j,k)
            datajason={
                'err_ok':err_ok,
                'content': MEItem_lists
            }
            # print(datajason)
            # print(json.dumps(datajason))
            return HttpResponse(json.dumps(datajason), content_type="application/json")

    return render(request, 'TestPlanME/itemuploadME.html', locals())