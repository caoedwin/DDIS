from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
import datetime, os
from django.http import HttpResponse
import datetime, json, simplejson, pprint
from .models import ProjectPlan
from CQM.models import CQMProject
from app01.models import UserInfo, ProjectinfoinDCT, Role
from django.db import transaction
from django.forms.models import model_to_dict

# Create your views here.
headermodel_ProjectPlan = {
    'RD Project Plan': 'RD_Project_Plan', 'Year': 'Year', 'DataType': 'DataType', 'CG': 'CG',
    'Compal Model': 'Compal_Model', 'Customer Model': 'Customer_Model',
    'Marketing type\r\r\n(Commercial / Consumer)': 'Marketing_type',
    """Status:\r\r\nPlanning  =P\r\r\nExecuting=E""": 'Status', 'Customer': 'Customer',
    """Product Type\r\r\n(NB/PAD/AIO/IPC)""": 'Product_Type', 'Jan': 'Jan', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Apr',
    'May': 'May', 'Jun': 'Jun', 'July': 'Jul', 'Aug': 'Aug', 'Sep': 'Sep',
    'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dec',
}


@csrf_exempt
def ProjectComparison_Edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DDIS/ProjectComparison_edit"
    weizhi = "ProjectComparison/ProjectComparison_Edit"

    yearOptions = [
        # "2020", "2021", "2023"
    ]
    for i in ProjectPlan.objects.all().values("Year").distinct().order_by("Year"):
        yearOptions.append(i["Year"])

    datatypeOption = [
        # "Actual", "w/o OOC", "with OOC"
    ]
    for i in ProjectPlan.objects.all().values("DataType").distinct().order_by("DataType"):
        datatypeOption.append(i["DataType"])

    mock_data = [
        # {"id": "1", "Year": "2024", "DataType": "Actual", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Product_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "2", "Year": "2024", "DataType": "Actual", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Product_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "3", "Year": "2024", "DataType": "Actual", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Product_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""}
    ]

    errMsg = ''

    permission = 0  # 1:有權限
    roles = []
    onlineuser = request.session.get('account')
    # onlineuser = '0502413'
    onlineuserDepartment = ''
    # print(onlineuser,UserInfo.objects.get(account=onlineuser))
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    for i in roles:
        if 'admin' == i or 'DQA_LNV_ProjectCom_admin' in i:
            permission = 1
    # print(roles)
    # print(permission)
    # print(request.POST)
    # print(request.body)
    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            pass

        if request.POST.get('isGetData') == 'SEARCH':
            # mock_data
            Check_dic_ProjectPlan = {}
            YearSearch = request.POST.get('Year')
            DataTypeSearch = request.POST.get('DataType')
            if YearSearch:
                Check_dic_ProjectPlan["Year"] = YearSearch
            if DataTypeSearch:
                Check_dic_ProjectPlan["DataType"] = DataTypeSearch
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )
        elif request.POST.get('action') == 'onSubmit':
            ID = request.POST.get('ID')
            RD_Project_Plan = request.POST.get('RD_Project_Plan')
            Year = request.POST.get('Year')
            DataType = request.POST.get('DataType')
            CG = request.POST.get('CG')
            Compal_Model = request.POST.get('Compal_Model')
            Customer_Model = request.POST.get('Customer_Model')
            Marketing_type = request.POST.get('Marketing_type')
            Status = request.POST.get('Status')
            Customer = request.POST.get('Customer')
            Product_Type = request.POST.get('Product_Type')
            Jan = request.POST.get('Jan')
            Feb = request.POST.get('Feb')
            Mar = request.POST.get('Mar')
            Apr = request.POST.get('Apr')
            May = request.POST.get('May')
            Jun = request.POST.get('Jun')
            Jul = request.POST.get('July')
            Aug = request.POST.get('Aug')
            Sep = request.POST.get('Sep')
            Oct = request.POST.get('Oct')
            Nov = request.POST.get('Nov')
            Dec = request.POST.get('Dec')
            update_dic = {
                "RD_Project_Plan": RD_Project_Plan, "Year": Year, "DataType": DataType,
                "CG": CG,
                "Compal_Model": Compal_Model,
                "Customer_Model": Customer_Model,
                "Marketing_type": Marketing_type,
                "Status": Status,
                "Customer": Customer,
                "Product_Type": Product_Type,
                "Jan": Jan,
                "Feb": Feb,
                "Mar": Mar,
                "Apr": Apr,
                "May": May,
                "Jun": Jun,
                "Jul": Jul,
                "Aug": Aug,
                "Sep": Sep,
                "Oct": Oct,
                "Nov": Nov,
                "Dec": Dec,
            }
            try:
                with transaction.atomic():
                    ProjectPlan.objects.filter(id=ID).update(**update_dic)
            except Exception as e:
                # alert = '此数据正被其他使用者编辑中...'
                alert = str(e)
                print(alert)

            # mock_data
            Check_dic_ProjectPlan = {}
            YearSearch = request.POST.get('searchYear')
            DataTypeSearch = request.POST.get('searchDataType')
            if YearSearch:
                Check_dic_ProjectPlan["Year"] = YearSearch
            if DataTypeSearch:
                Check_dic_ProjectPlan["DataType"] = DataTypeSearch
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
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
                    # for i in responseData['params']:
                    #     ProjectPlan.objects.get(id=i).delete()
                    try:
                        with transaction.atomic():
                            ProjectPlan.objects.filter(id__in=responseData['params']).delete()
                    except Exception as e:
                        # alert = '此数据正被其他使用者编辑中...'
                        alert = str(e)
                        print(alert)
                    # mock_data
                    yearOptions = [
                        # "2020", "2021", "2023"
                    ]
                    for i in ProjectPlan.objects.all().values("Year").distinct().order_by("Year"):
                        yearOptions.append(i["Year"])

                    datatypeOption = [
                        # "Actual", "w/o OOC", "with OOC"
                    ]
                    for i in ProjectPlan.objects.all().values("DataType").distinct().order_by("DataType"):
                        datatypeOption.append(i["DataType"])
                    Check_dic_ProjectPlan = {}
                    YearSearch = request.POST.get('Year')
                    DataTypeSearch = request.POST.get('DataType')
                    if YearSearch:
                        Check_dic_ProjectPlan["Year"] = YearSearch
                    if DataTypeSearch:
                        Check_dic_ProjectPlan["DataType"] = DataTypeSearch
                    # print(Check_dic_ProjectPlan)
                    for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year,
                                "DataType": i.DataType,
                                "CG": i.CG,
                                "Compal_Model": i.Compal_Model,
                                "Customer_Model": i.Customer_Model,
                                "Marketing_type": i.Marketing_type,
                                "Status": i.Status,
                                "Customer": i.Customer,
                                "Product_Type": i.Product_Type,
                                "Jan": i.Jan if i.Jan != None else '',
                                "Feb": i.Feb if i.Feb != None else '',
                                "Mar": i.Mar if i.Mar != None else '',
                                "Apr": i.Apr if i.Apr != None else '',
                                "May": i.May if i.May != None else '',
                                "Jun": i.Jun if i.Jun != None else '',
                                "July": i.Jul if i.Jul != None else '',
                                "Aug": i.Aug if i.Aug != None else '',
                                "Sep": i.Sep if i.Sep != None else '',
                                "Oct": i.Oct if i.Oct != None else '',
                                "Nov": i.Nov if i.Nov != None else '',
                                "Dec": i.Dec if i.Dec != None else '',
                            }
                        )

                elif 'upload' in str(request.body):

                    responseData = json.loads(request.body)
                    # print(responseData['historyYear'],type(responseData['historyYear']))
                    YearSearch = responseData['Year']
                    YearSearch_backup = ''
                    DataTypeSearch = responseData['DataType']

                    xlsxlist = json.loads(responseData['ExcelData'])
                    # print(xlsxlist)
                    # pprint.pprint(xlsxlist)
                    # 验证，先验证再上传,必须要先验证，如果边验证边上传，一旦报错，下次再传就无法通过同机种验证
                    # Check_dic_Project = {'Customer': CustomerSearch, 'Project': ProjectSearch, }
                    # # print(Check_dic_ProjectCQM)
                    # Projectinfo = CQMProject.objects.filter(**Check_dic_Project).first()
                    # print(Projectinfo)
                    # current_user = request.session.get('user_name')
                    # current_account = request.session.get('account')
                    # ProjectComparison_admin_user = "0301507" #Canny
                    # # if Projectinfo:s
                    # #                     #     for k in Projectinfo.Owner.all():
                    # #                     #         # print(k.username,current_user)
                    # #                     #         # print(type(k.username),type(current_user))
                    # #                     #         if k.username == current_uer:
                    # #             canEdit = 1
                    # #             break
                    # if current_account == ProjectComparison_admin_user:
                    #     canEdit = 1
                    # print(canEdit)
                    # try:
                    if permission:
                        rownum = 0
                        startupload = 0
                        # print(xlsxlist)
                        create_list = []
                        for i in xlsxlist:
                            # print(type(i),i)
                            rownum += 1
                            modeldata = {}
                            for key, value in i.items():
                                if key in headermodel_ProjectPlan.keys():
                                    # print(headermodel_ProjectPlan[key],value)
                                    modeldata[headermodel_ProjectPlan[key]] = value
                            # print(modeldata)

                            if 'Year' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Year不能爲空
                                                            """ % rownum
                                break
                            if 'DataType' in modeldata.keys():
                                if modeldata['DataType'] == 'Actual':
                                    if 'RD_Project_Plan' in modeldata.keys():
                                        startupload = 1
                                    else:
                                        # canEdit = 0
                                        startupload = 0
                                        errMsg = """
                                                第"%s"條數據，DataType 是Actual时， RD_Project_Plan不能为空
                                                                    """ % rownum
                                        break
                                else:
                                    startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，DataType不能爲空
                                                            """ % rownum
                                break
                            if 'CG' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，CG不能爲空
                                                            """ % rownum
                                break
                            if 'Compal_Model' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Compal_Model不能爲空
                                                            """ % rownum
                                break
                            if 'Customer_Model' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Customer_Model不能爲空
                                                            """ % rownum
                                break
                            if 'Marketing_type' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Marketing_type不能爲空
                                                            """ % rownum
                                break
                            if 'Status' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Status不能爲空
                                                            """ % rownum
                                break
                            if 'Customer' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Customer不能爲空
                                                            """ % rownum
                                break
                            if 'Product_Type' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Product_Type不能爲空
                                                            """ % rownum
                                break

                            create_list.append(ProjectPlan(**modeldata))  # object(**dict)
                            # print(create_list)
                            if rownum == 1:
                                YearSearch_backup = modeldata['Year']
                                # print(modeldata['Year'])
                        # print(errMsg, startupload)
                        # print(create_list,)
                        # print(startupload)
                        # print(rownum, type(rownum))
                        if startupload:
                            try:
                                with transaction.atomic():
                                    ProjectPlan.objects.bulk_create(create_list)
                            except Exception as e:
                                # alert = '此数据正被其他使用者编辑中...'
                                alert = str(e)
                                print(alert)

                    # print('IssuesBreakdown')
                    # mock_data
                    yearOptions = [
                        # "2020", "2021", "2023"
                    ]
                    for i in ProjectPlan.objects.all().values("Year").distinct().order_by("Year"):
                        yearOptions.append(i["Year"])

                    datatypeOption = [
                        # "Actual", "w/o OOC", "with OOC"
                    ]
                    for i in ProjectPlan.objects.all().values("DataType").distinct().order_by("DataType"):
                        datatypeOption.append(i["DataType"])
                    Check_dic_ProjectPlan = {}
                    if YearSearch:
                        Check_dic_ProjectPlan["Year"] = YearSearch
                    elif YearSearch_backup:
                        Check_dic_ProjectPlan["Year"] = YearSearch_backup
                    if DataTypeSearch:
                        Check_dic_ProjectPlan["DataType"] = DataTypeSearch
                    for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year,
                                "DataType": i.DataType,
                                "CG": i.CG,
                                "Compal_Model": i.Compal_Model,
                                "Customer_Model": i.Customer_Model,
                                "Marketing_type": i.Marketing_type,
                                "Status": i.Status,
                                "Customer": i.Customer,
                                "Product_Type": i.Product_Type,
                                "Jan": i.Jan if i.Jan != None else '',
                                "Feb": i.Feb if i.Feb != None else '',
                                "Mar": i.Mar if i.Mar != None else '',
                                "Apr": i.Apr if i.Apr != None else '',
                                "May": i.May if i.May != None else '',
                                "Jun": i.Jun if i.Jun != None else '',
                                "July": i.Jul if i.Jul != None else '',
                                "Aug": i.Aug if i.Aug != None else '',
                                "Sep": i.Sep if i.Sep != None else '',
                                "Oct": i.Oct if i.Oct != None else '',
                                "Nov": i.Nov if i.Nov != None else '',
                                "Dec": i.Dec if i.Dec != None else '',
                            }
                        )
                    # except Exception as e:
                    #     errMsg = str(e)

                elif 'MUTIDELALL' in str(request.body):
                    responseData = json.loads(request.body)
                    Year = responseData["Year"]
                    # for i in responseData['params']:
                    #     ProjectPlan.objects.get(id=i).delete()
                    # print(Year)
                    try:
                        with transaction.atomic():
                            ProjectPlan.objects.filter(Year=Year).delete()
                    except Exception as e:
                        # alert = '此数据正被其他使用者编辑中...'
                        alert = str(e)
                        print(alert)
                    # mock_data
                    yearOptions = [
                        # "2020", "2021", "2023"
                    ]
                    for i in ProjectPlan.objects.all().values("Year").distinct().order_by("Year"):
                        yearOptions.append(i["Year"])

                    datatypeOption = [
                        # "Actual", "w/o OOC", "with OOC"
                    ]
                    for i in ProjectPlan.objects.all().values("DataType").distinct().order_by("DataType"):
                        datatypeOption.append(i["DataType"])
                    Check_dic_ProjectPlan = {}
                    YearSearch = request.POST.get('Year')
                    # DataTypeSearch = request.POST.get('DataType')
                    if YearSearch:
                        Check_dic_ProjectPlan["Year"] = YearSearch
                    # if DataTypeSearch:
                    #     Check_dic_ProjectPlan["DataType"] = DataTypeSearch
                    # print(Check_dic_ProjectPlan)
                    for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                        # print(i)
                        mock_data.append(
                            {
                                "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year,
                                "DataType": i.DataType,
                                "CG": i.CG,
                                "Compal_Model": i.Compal_Model,
                                "Customer_Model": i.Customer_Model,
                                "Marketing_type": i.Marketing_type,
                                "Status": i.Status,
                                "Customer": i.Customer,
                                "Product_Type": i.Product_Type,
                                "Jan": i.Jan if i.Jan != None else '',
                                "Feb": i.Feb if i.Feb != None else '',
                                "Mar": i.Mar if i.Mar != None else '',
                                "Apr": i.Apr if i.Apr != None else '',
                                "May": i.May if i.May != None else '',
                                "Jun": i.Jun if i.Jun != None else '',
                                "July": i.Jul if i.Jul != None else '',
                                "Aug": i.Aug if i.Aug != None else '',
                                "Sep": i.Sep if i.Sep != None else '',
                                "Oct": i.Oct if i.Oct != None else '',
                                "Nov": i.Nov if i.Nov != None else '',
                                "Dec": i.Dec if i.Dec != None else '',
                            }
                        )

        data = {
            "errMsg": errMsg,
            "yearOptions": yearOptions,
            "datatypeOption": datatypeOption,
            "content": mock_data,
            "permission": permission,

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ProjectComparison/ProjectComparison_Edit.html', locals())


def mockdatas_count(Year, Customer_list):
    mock_data1 = []
    mock_data2 = []
    mock_data3 = []
    mock_data4 = []
    # mock_data2 Actual
    phase_list = ["FVT", "SIT", "OOC", "OS-R"]
    DataTypeSearh = "Actual"
    id_num = 1
    for i in phase_list:
        mock_data_dic = {"id": id_num, "Phase": i,
                         "Jan": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jan=i).count(),
                         "Feb": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Feb=i).count(),
                         "Mar": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Mar=i).count(),
                         "Apr": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Apr=i).count(),
                         "May": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           May=i).count(),
                         "Jun": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jun=i).count(),
                         "July": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                            Jul=i).count(),
                         "Aug": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Aug=i).count(),
                         "Sep": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Sep=i).count(),
                         "Oct": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Oct=i).count(),
                         "Nov": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Nov=i).count(),
                         "Dec": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Dec=i).count()}
        mock_data_dic["Total"] = mock_data_dic["Jan"] + mock_data_dic["Feb"] + mock_data_dic["Mar"] + mock_data_dic[
            "Apr"] + mock_data_dic["May"] + mock_data_dic["Jun"] + mock_data_dic["July"] + mock_data_dic["Aug"] + \
                                 mock_data_dic["Sep"] + mock_data_dic["Oct"] + mock_data_dic["Nov"] + mock_data_dic[
                                     "Dec"]
        print(i, mock_data_dic)
        mock_data2.append(mock_data_dic)
        id_num += 1

    # mock_data3 w/o OOC
    DataTypeSearh = "w/o OOC"
    id_num = 1
    for i in phase_list:
        mock_data_dic = {"id": id_num, "Phase": i,
                         "Jan": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jan=i).count(),
                         "Feb": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Feb=i).count(),
                         "Mar": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Mar=i).count(),
                         "Apr": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Apr=i).count(),
                         "May": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           May=i).count(),
                         "Jun": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jun=i).count(),
                         "July": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                            Jul=i).count(),
                         "Aug": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Aug=i).count(),
                         "Sep": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Sep=i).count(),
                         "Oct": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Oct=i).count(),
                         "Nov": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Nov=i).count(),
                         "Dec": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Dec=i).count()}
        mock_data_dic["Total"] = mock_data_dic["Jan"] + mock_data_dic["Feb"] + mock_data_dic["Mar"] + mock_data_dic[
            "Apr"] + mock_data_dic["May"] + mock_data_dic["Jun"] + mock_data_dic["July"] + mock_data_dic["Aug"] + \
                                 mock_data_dic["Sep"] + mock_data_dic["Oct"] + mock_data_dic["Nov"] + mock_data_dic[
                                     "Dec"]
        mock_data3.append(mock_data_dic)
        id_num += 1

    # mock_data4 with OOC
    DataTypeSearh = "with OOC"
    id_num = 1
    for i in phase_list:
        mock_data_dic = {"id": id_num, "Phase": i,
                         "Jan": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jan=i).count(),
                         "Feb": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Feb=i).count(),
                         "Mar": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Mar=i).count(),
                         "Apr": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Apr=i).count(),
                         "May": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           May=i).count(),
                         "Jun": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Jun=i).count(),
                         "July": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                            Jul=i).count(),
                         "Aug": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Aug=i).count(),
                         "Sep": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Sep=i).count(),
                         "Oct": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Oct=i).count(),
                         "Nov": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Nov=i).count(),
                         "Dec": ProjectPlan.objects.filter(Year=Year, DataType=DataTypeSearh,
                                                           Dec=i).count()}
        mock_data_dic["Total"] = mock_data_dic["Jan"] + mock_data_dic["Feb"] + mock_data_dic["Mar"] + mock_data_dic[
            "Apr"] + mock_data_dic["May"] + mock_data_dic["Jun"] + mock_data_dic["July"] + mock_data_dic["Aug"] + \
                                 mock_data_dic["Sep"] + mock_data_dic["Oct"] + mock_data_dic["Nov"] + mock_data_dic[
                                     "Dec"]
        mock_data4.append(mock_data_dic)
        id_num += 1

    # mock_data1 Act - Plan
    Phase = "FVT"
    mock_data_FVT_dic = {"id": 1, "Phase": Phase,
                         "Jan": mock_data2[0]["Jan"] - mock_data4[0]["Jan"],
                         "Feb": mock_data2[0]["Feb"] - mock_data4[0]["Feb"],
                         "Mar": mock_data2[0]["Mar"] - mock_data4[0]["Mar"],
                         "Apr": mock_data2[0]["Apr"] - mock_data4[0]["Apr"],
                         "May": mock_data2[0]["May"] - mock_data4[0]["May"],
                         "Jun": mock_data2[0]["Jun"] - mock_data4[0]["Jun"],
                         "July": mock_data2[0]["July"] - mock_data4[0]["July"],
                         "Aug": mock_data2[0]["Aug"] - mock_data4[0]["Aug"],
                         "Sep": mock_data2[0]["Sep"] - mock_data4[0]["Sep"],
                         "Oct": mock_data2[0]["Oct"] - mock_data4[0]["Oct"],
                         "Nov": mock_data2[0]["Nov"] - mock_data4[0]["Nov"],
                         "Dec": mock_data2[0]["Dec"] - mock_data4[0]["Dec"],
                         "Total": mock_data2[0]["Total"] - mock_data4[0]["Total"],
                         }
    mock_data1.append(mock_data_FVT_dic)

    Phase = "SIT"
    mock_data_SIT_dic = {"id": 2, "Phase": Phase,
                         "Jan": mock_data2[1]["Jan"] - mock_data4[1]["Jan"],
                         "Feb": mock_data2[1]["Feb"] - mock_data4[1]["Feb"],
                         "Mar": mock_data2[1]["Mar"] - mock_data4[1]["Mar"],
                         "Apr": mock_data2[1]["Apr"] - mock_data4[1]["Apr"],
                         "May": mock_data2[1]["May"] - mock_data4[1]["May"],
                         "Jun": mock_data2[1]["Jun"] - mock_data4[1]["Jun"],
                         "July": mock_data2[1]["July"] - mock_data4[1]["July"],
                         "Aug": mock_data2[1]["Aug"] - mock_data4[1]["Aug"],
                         "Sep": mock_data2[1]["Sep"] - mock_data4[1]["Sep"],
                         "Oct": mock_data2[1]["Oct"] - mock_data4[1]["Oct"],
                         "Nov": mock_data2[1]["Nov"] - mock_data4[1]["Nov"],
                         "Dec": mock_data2[1]["Dec"] - mock_data4[1]["Dec"],
                         "Total": mock_data2[1]["Total"] - mock_data4[1]["Total"],
                         }
    mock_data1.append(mock_data_SIT_dic)

    Phase = "OOC"
    print(mock_data2[2]["Jan"], mock_data4[2]["Jan"])
    mock_data_OOC_dic = {"id": 3, "Phase": Phase,
                         "Jan": mock_data2[2]["Jan"] - mock_data4[2]["Jan"],
                         "Feb": mock_data2[2]["Feb"] - mock_data4[2]["Feb"],
                         "Mar": mock_data2[2]["Mar"] - mock_data4[2]["Mar"],
                         "Apr": mock_data2[2]["Apr"] - mock_data4[2]["Apr"],
                         "May": mock_data2[2]["May"] - mock_data4[2]["May"],
                         "Jun": mock_data2[2]["Jun"] - mock_data4[2]["Jun"],
                         "July": mock_data2[2]["July"] - mock_data4[2]["July"],
                         "Aug": mock_data2[2]["Aug"] - mock_data4[2]["Aug"],
                         "Sep": mock_data2[2]["Sep"] - mock_data4[2]["Sep"],
                         "Oct": mock_data2[2]["Oct"] - mock_data4[2]["Oct"],
                         "Nov": mock_data2[2]["Nov"] - mock_data4[2]["Nov"],
                         "Dec": mock_data2[2]["Dec"] - mock_data4[2]["Dec"],
                         "Total": mock_data2[2]["Total"] - mock_data4[2]["Total"],
                         }
    mock_data1.append(mock_data_OOC_dic)

    Phase = "OS-R"
    mock_data_OSR_dic = {"id": 4, "Phase": Phase,
                         "Jan": mock_data2[3]["Jan"] - mock_data4[3]["Jan"],
                         "Feb": mock_data2[3]["Feb"] - mock_data4[3]["Feb"],
                         "Mar": mock_data2[3]["Mar"] - mock_data4[3]["Mar"],
                         "Apr": mock_data2[3]["Apr"] - mock_data4[3]["Apr"],
                         "May": mock_data2[3]["May"] - mock_data4[3]["May"],
                         "Jun": mock_data2[3]["Jun"] - mock_data4[3]["Jun"],
                         "July": mock_data2[3]["July"] - mock_data4[3]["July"],
                         "Aug": mock_data2[3]["Aug"] - mock_data4[3]["Aug"],
                         "Sep": mock_data2[3]["Sep"] - mock_data4[3]["Sep"],
                         "Oct": mock_data2[3]["Oct"] - mock_data4[3]["Oct"],
                         "Nov": mock_data2[3]["Nov"] - mock_data4[3]["Nov"],
                         "Dec": mock_data2[3]["Dec"] - mock_data4[3]["Dec"],
                         "Total": mock_data2[3]["Total"] - mock_data4[3]["Total"],
                         }

    mock_data1.append(mock_data_OSR_dic)
    return [mock_data1, mock_data2, mock_data3, mock_data4]


@csrf_exempt
def ProjectComparison_Summary(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DDIS/ProjectComparison_Summary"
    yearOptions = [
        # "2020", "2021", "2023"
    ]
    for i in ProjectPlan.objects.all().values("Year").distinct().order_by("Year"):
        yearOptions.append(i["Year"])

    # 表格數據
    mock_data1 = [
        # {"id": 1, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 2, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 3, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},

    ]
    mock_data2 = [
        # {"id": 1, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 2, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 3, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},

    ]

    mock_data3 = [

        # {"id": "1", "RD_Project_Plan": "No", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "2", "RD_Project_Plan": "No", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "3", "RD_Project_Plan": "No", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""}
    ]

    mock_data4 = [
        # {"id": 1, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 2, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 3, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},

    ]

    mock_data5 = [

        # {"id": "1", "CG": "CG13", "Compal_Model": "ILVR4", "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "2", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "3", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""}
    ]

    mock_data6 = [
        # {"id": 1, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 2, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},
        # {"id": 3, "Phase": "FVT", "Jan": 0, "Feb": 0, "Mar": 1, "Apr": 2, "May": 3, "Jun": 4,
        #  "July": 5, "Aug": 6, "Sep": 7, "Oct": 8, "Nov": 9, "Dec": 0},

    ]

    mock_data7 = [

        # {"id": "1", "CG": "CG13", "Compal_Model": "ILVR4", "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "2", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""},
        # {"id": "3", "CG": "CG13", "Compal_Model": "ILVR4",
        #  "Customer_Model": "S590 14Intel MTL H28(Plastic/Metal)",
        #  "Marketing_type": "SMB/Commercial", "Status": "E", "Customer": "C38", "Project_Type": "NB", "Jan": "OOC",
        #  "Feb": "SIT",
        #  "Mar": "", "Apr": "", "May": "", "Jun": "", "July": "", "Aug": "", "Sep": "", "Oct": "", "Nov": "", "Dec": ""}
    ]

    if request.method == "POST":
        if request.POST.get('isGetData') == 'first':
            YearNow = str(datetime.datetime.now().year)
            # Year = request.POST.get('Year')
            Customer_list = [
                # 'C38', 'T12', 'T89', 'T12',
                             ]
            mockdatas = mockdatas_count(YearNow, Customer_list)
            mock_data1 = mockdatas[0]
            mock_data2 = mockdatas[1]
            mock_data4 = mockdatas[2]
            mock_data6 = mockdatas[3]
            Year = YearNow
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "Actual"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data3.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "w/o OOC"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data5.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "with OOC"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data7.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )

        if request.POST.get('isGetData') == 'SEARCH':
            # YearNow = str(datetime.datetime.now().year)
            Year = request.POST.get('Year')
            Customer_list = ['C38', 'T12', 'T89', 'T12', ]
            mockdatas = mockdatas_count(Year, Customer_list)
            mock_data1 = mockdatas[0]
            mock_data2 = mockdatas[1]
            mock_data4 = mockdatas[2]
            mock_data6 = mockdatas[3]
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "Actual"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data3.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "w/o OOC"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data5.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )
            Check_dic_ProjectPlan = {'Year': Year, "DataType": "with OOC"}
            # print(Check_dic_ProjectPlan)
            for i in ProjectPlan.objects.filter(**Check_dic_ProjectPlan):
                # print(i)
                mock_data7.append(
                    {
                        "id": i.id, "RD_Project_Plan": i.RD_Project_Plan, "Year": i.Year, "DataType": i.DataType,
                        "CG": i.CG,
                        "Compal_Model": i.Compal_Model,
                        "Customer_Model": i.Customer_Model,
                        "Marketing_type": i.Marketing_type,
                        "Status": i.Status,
                        "Customer": i.Customer,
                        "Product_Type": i.Product_Type,
                        "Jan": i.Jan if i.Jan != None else '',
                        "Feb": i.Feb if i.Feb != None else '',
                        "Mar": i.Mar if i.Mar != None else '',
                        "Apr": i.Apr if i.Apr != None else '',
                        "May": i.May if i.May != None else '',
                        "Jun": i.Jun if i.Jun != None else '',
                        "July": i.Jul if i.Jul != None else '',
                        "Aug": i.Aug if i.Aug != None else '',
                        "Sep": i.Sep if i.Sep != None else '',
                        "Oct": i.Oct if i.Oct != None else '',
                        "Nov": i.Nov if i.Nov != None else '',
                        "Dec": i.Dec if i.Dec != None else '',
                    }
                )

        data = {
            "yearOptions": yearOptions,
            "content1": mock_data1,
            "content2": mock_data2,
            "content3": mock_data3,
            "content4": mock_data4,
            "content5": mock_data5,
            "content6": mock_data6,
            "content7": mock_data7,

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'ProjectComparison/ProjectComparison_Summary.html', locals())
