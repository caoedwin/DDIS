from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import datetime, json, simplejson, requests, time
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app01.models import UserInfo
from django.db import transaction
from django.db.models import Max, Min, Sum, Count, Q, F, Value, CharField
from django.db.models.functions import Substr
from operator import itemgetter, attrgetter
from collections import Counter
from .models import CommonFiles, Category, SubCategory, files
from django.db.models.functions import ExtractYear

from django.db import models

headermodel_Commonfiles = {
    'CG': 'CG', 'HW/SW': 'SWHW', 'Category-L1': 'Category_L1', 'Category-L2': 'Category_L2',
    'Item': 'Item', 'Version': 'Version',
    'Owner': 'Owner',
    'Description': 'Description',
}

def map_field_type(field):
    """映射 Django 字段类型到前端显示类型"""
    if isinstance(field, models.BooleanField):
        return 'switch'
    elif isinstance(field, (models.DateField, models.DateTimeField)):
        return 'date'
    elif isinstance(field, models.ForeignKey):
        return 'relation'
    elif isinstance(field, models.TextField):
        return 'long-text'
    elif isinstance(field, models.FileField):
        return 'file'
    elif isinstance(field, models.CharField):
        return 'text'
    else:
        return 'text'  # 默认类型


def calculate_field_width(field):
    """计算字段建议宽度"""
    # 基于 max_length 的宽度计算
    if hasattr(field, 'max_length') and field.max_length:
        # 每字符约 8px，最小宽度 100px，最大 300px
        return min(max(field.max_length * 8, 100), 300)

    # 基于字段类型的默认宽度
    field_type = map_field_type(field)
    type_widths = {
        'switch': 100,
        'date': 150,
        'datetime': 180,
        'relation': 200,
        'file': 220,
        'long-text': 300,
        'text': 180
    }
    return type_widths.get(field_type, 180)  # 默认 180px


def get_table_columns(model):
    columns = []
    for field in model._meta.fields:
        # 跳过不需要的字段（如 ID）
        if field.name == 'id' or field.name.endswith('_ptr'):
            continue

        # 基本字段配置
        field_config = {
            'field': field.name,
            'title': field.verbose_name,  # 使用 verbose_name 作为标题
            'type': map_field_type(field),
            'width': calculate_field_width(field),
            'align': "center",
        }

        # 添加字段特定属性
        if hasattr(field, 'choices') and field.choices:
            field_config['choices'] = dict(field.choices)

        columns.append(field_config)
    return columns


@csrf_exempt
def CommonFiles_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DepartmentManage/知行智库"

    allCategorys = {}
    categoryOptions = []
    for i in Category.objects.all().order_by('id'):
        allCategorys[i.id] = i.name
        categoryOptions.append(i.name)

    allSubCategorys = {}
    for i in SubCategory.objects.all():
        # print(i)
        allSubCategorys[i.id] = i.name

    selectItem = [
        # {
        #   'id': 1,
        #   'name': '網絡設備',
        #   'SubCategorys': [
        #     { id: 11, 'name': '宽带' },
        #     { id: 12, 'name': '伺服器' }
        #   ]
        # },
    ]
    for i in Category.objects.all().order_by('id'):
        SubCategorylist = []

        for j in SubCategory.objects.filter(category__name=i.name):
            SubCategorylist.append(
                {"id": j.id, 'name': j.name}
            )
        selectItem.append(
            {
                'id': i.id,
                'name': i.name,
                'SubCategorys': SubCategorylist
            }
        )
    # print(selectItem, 'selectItem')

    StatusOptions = []
    # print(StatusOptions, 'StatusOptions')

    CGOptions = []
    for i in CommonFiles._meta.get_field('CG').choices:
        CGOptions.append(i[0])

    SWHWOptions = []
    for i in CommonFiles._meta.get_field('SWHW').choices:
        SWHWOptions.append(i[0])

    sectionOwner = [
        # {"value": "姚麗麗", "number": "22314345"}, {"value": "張亞萍", "number": "123456789"},
    ]
    for i in UserInfo.objects.all():
        sectionOwner.append(
            {
                "value": i.username, "number": i.account
            }
        )

    OwnersOptions = [
        # {"key": "姚丽丽", "label": "2222222"},
        # {"key": "张颖", "label": "1111111"},
    ]
    for i in UserInfo.objects.all():
        OwnersOptions.append(
            {
                "account": i.account, "username": i.username, "disabled": False if i.is_active else True, "id": i.id,
            }
        )

    mock_data = [
        # {"id": "1", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
        #
        # {"id": "2", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
        #
        # {"id": "3", "Category": "網絡設備", "Product_Type": "宽带", "Name": "ADSL #17", "Num": "18501560367",
        #  "Manufacturer": "電信", "Cost": "150", "Account": "NA",
        #  "PW": "NA", "Purchasing_Date": "YYYY-MM-DD", "Duration": "", "Department": "KMKACNQBA0", "Location": "V2FA-17",
        #  "Asset_Num": "NA",
        #  "Owner": "Heart_Liu", "Mail": "Heart_Liu@compal.com", "Contact_info": "", "Comments": ""},
    ]

    # # 1. 始终为动态列设置唯一的: key属性
    # #
    # # 2. 固定列（fixed）可在配置中添加fixed: 'left' / 'right'属性
    # #
    # # 3. 排序功能可通过添加sortable属性实现
    # #
    # # 4. 表头分组需嵌套使用el - table - column（ElementUI不支持单层动态分组）
    # # < el - table - column
    # #     v-for ="col in tableColumns"
    # #     :key = "col.prop"
    # #     :prop = "col.prop"
    # #     :label = "col.label"
    # #     :width = "col.width"
    # #     :align = "col.align"
    # #
    # # >
    # #     //自定义内容，如果只要默认的，直接去点下面的template这一段
    #         < !-- 根据字段类型使用不同的渲染方式 -->
    #         < template  # default="scope">
    #         < !-- 布尔值显示开关 -->
    #         < el - switch
    #         v - if = "col.type === 'switch'"
    #         v - model = "scope.row[col.prop]"
    #         disabled
    #
    #         / >
    #
    #         < !-- 日期格式化 -->
    #         < span
    #         v - else - if = "col.type === 'date'" >
    #         ${formatDate(scope.row[col.prop])}
    #         < / span >
    #
    #         < !-- 外键关系显示关联对象名称 -->
    #         < span
    #         v - else - if = "col.type === 'relation'" >
    #         ${scope.row[col.prop + '_name']} <!-- 假设返回了关联对象名称 -->
    #         < / span >
    #
    #         < !-- 长文本使用
    #         tooltip
    #         显示 -->
    #         < el - tooltip
    #         v - else - if = "col.type === 'long-text'"
    #         :content = "scope.row[col.prop]"
    #         placement = "top"
    #         >
    #         < span
    #
    #
    #         class ="text-truncate" >
    #
    #
    #         ${truncateText(scope.row[col.prop], 30)}
    #         < / span >
    #         < / el - tooltip >
    #
    #         < !-- 默认文本显示 -->
    #         < span
    #         v - else >
    #         ${scope.row[col.prop]}
    #         < / span >
    #         < / template >
    # # < / el - table - column >

    # 提取字段名和 verbose_name（过滤关系字段）
    tableColumns = [
        # {'id': 1, 'prop': 'status', 'lable': '状态', 'type': 'tag', 'width': '120', 'align': 'center'},
        #             {'id': 2, 'prop': 'createTime', 'lable': '创建时间', 'type': 'text', 'width': '180', 'align': 'center'}
    ]
    tableColumns = get_table_columns(CommonFiles)
    # print(tableColumns)

    errMsg = ''
    permission = 1  # 權限
    SSVIP_users = 0
    roles = []
    onlineuser = request.session.get('account')
    if UserInfo.objects.filter(account=onlineuser).first():
        for i in UserInfo.objects.filter(account=onlineuser).first().role.all():
            roles.append(i.name)
    # print(roles)
    for i in roles:
        if i == 'admin' or i == 'DQA_director':
            SSVIP_users = 1
        if i == 'admin' or i == 'PublicAreaAdmin':
            permission = 1
    mock_obj = CommonFiles.objects.all().order_by('-created_at')

    if request.method == "POST":
        # try:
        if request.POST:
            ch_dic = {}
            if request.POST.get('isGetData') == 'SEARCH':
                if request.POST.get('CG'):
                    ch_dic['CG'] = request.POST.get('CG')
                if request.POST.get('SWHW'):
                    ch_dic['SWHW'] = request.POST.get('SWHW')
                if request.POST.get('Category_L1'):
                    ch_dic['Category_L1'] = Category.objects.filter(id=request.POST.get('Category_L1')).first()
                if request.POST.get('Category_L2'):
                    ch_dic['Category_L2'] = SubCategory.objects.filter(id=request.POST.get('Category_L2')).first()
                if request.POST.get('Owner'):
                    user = UserInfo.objects.filter(account=request.POST.get('OwnerNumber')).first()
                    ch_dic['Owner'] = user
                if ch_dic:
                    mock_obj = CommonFiles.objects.filter(**ch_dic).order_by('-created_at')
            if request.POST.get('action') == 'addData':
                # ID = request.POST.get('ID')
                Owners = json.loads(request.POST.get('Owner'))
                # print(Owners)
                UserInfos = UserInfo.objects.filter(account__in=Owners)
                new_files = request.FILES.getlist("new_files", "")
                # print(new_files)
                files_to_delete = json.loads(request.POST.get('files_to_delete', '[]'))

                create_dic = {
                    "CG": request.POST.get('CG'),
                    "SWHW": request.POST.get('SWHW') if request.POST.get('SWHW') and request.POST.get(
                        'v') != 'null' and request.POST.get('SWHW') != 'None' else "",
                    "Category_L1_id": request.POST.get('Category_L1'),
                    # "Category_L2_id": request.POST.get('Category_L2'),
                    "Category_L2": SubCategory.objects.get(id=request.POST.get('Category_L2')) if request.POST.get('Category_L2') else None,
                    "Item": request.POST.get('Item') if request.POST.get('Item') else '',
                    "Description": request.POST.get('Description') if request.POST.get('Description') else '',
                    "Version": request.POST.get('Version') if request.POST.get('Version') else '',
                    "Creator": onlineuser,
                }
                if request.POST.get('Category_L2'):
                    create_dic["Category_L2_id"] = request.POST.get('Category_L2')
                # try:
                with transaction.atomic():
                    CommonFiles_object = CommonFiles.objects.create(**create_dic)
                    if new_files:
                        for f in new_files:
                            # print(f)
                            empt = files()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            CommonFiles_object.Attachment.add(empt)
                    fileslist = files.objects.filter(id__in=files_to_delete)  # 最好是用id，这样搜索时就需要返回带id的信息
                    # print(vedios)

                    # 解除关联
                    CommonFiles_object.Attachment.remove(*fileslist)  # 使用 * 解包列表
                    CommonFiles_object.Owner.add(*UserInfos)
                    fileslist.delete()  # 删除实体文件 model中的files_SopRom_delete方法
                    CommonFiles_object.save()
                # except Exception as e:
                #     # alert = '此数据正被其他使用者编辑中...'
                #     errMsg = alert = str(e)
                #     print(alert)

                # mock_data
                check_dic = {}
                if request.POST.get('searchCG'):
                    check_dic['searchCG'] = request.POST.get('searchCG')
                if request.POST.get('searchSWHW'):
                    check_dic['searchSWHW'] = request.POST.get('searchSWHW')
                if request.POST.get('searchCategory_L1'):
                    check_dic['Category_L1'] = Category.objects.filter(
                        id=request.POST.get('searchCategory_L1')).first()
                if request.POST.get('searchCategory_L2'):
                    check_dic['Category_L2'] = SubCategory.objects.filter(
                        id=request.POST.get('searchCategory_L2')).first()
                if request.POST.get('searchOwner'):
                    user = UserInfo.objects.filter(account=request.POST.get('searchOwnerNumber')).first()
                    check_dic['Owner'] = user
                if check_dic:
                    mock_obj = CommonFiles.objects.filter(**check_dic).order_by('-created_at')
            if request.POST.get('action') == 'update':
                ID = request.POST.get('ID')
                Owners = json.loads(request.POST.get('Owner'))
                # print(Owners)
                Mail = ''
                UserInfos = UserInfo.objects.filter(account__in=Owners)
                new_files = request.FILES.getlist("new_files", "")
                files_to_delete = json.loads(request.POST.get('files_to_delete', '[]'))

                update_dic = {
                    "CG": request.POST.get('CG'),
                    "SWHW": request.POST.get('SWHW') if request.POST.get('SWHW') and request.POST.get(
                        'SWHW') != 'null' and request.POST.get('SWHW') != 'None' else "",
                    "Category_L1_id": request.POST.get('Category_L1'),
                    # "Category_L2_id": request.POST.get('Category_L2'),
                    "Category_L2": SubCategory.objects.get(id=request.POST.get('Category_L2')) if request.POST.get('Category_L2') else None,
                    "Item": request.POST.get('Item') if request.POST.get('Item') else '',
                    "Description": request.POST.get('Description') if request.POST.get('Description') else '',
                    "Version": request.POST.get('Version') if request.POST.get('Version') else '',
                    # "Creator": onlineuser,
                }
                if request.POST.get('Category_L2'):
                    update_dic["Category_L2_id"] = request.POST.get('Category_L2')
                # try:
                with transaction.atomic():
                    CommonFiles.objects.filter(id=ID).update(**update_dic)
                    CommonFiles_object = CommonFiles.objects.filter(id=ID).first()
                    CommonFiles_object.Owner.clear()
                    CommonFiles_object.Owner.add(*UserInfos)
                    if new_files:
                        for f in new_files:
                            # print(f)
                            empt = files()
                            # 增加其他字段应分别对应填写
                            empt.single = f
                            empt.files = f
                            empt.save()
                            CommonFiles_object.Attachment.add(empt)
                    fileslist = files.objects.filter(id__in=files_to_delete)  # 最好是用id，这样搜索时就需要返回带id的信息
                    # print(vedios)

                    # 解除关联
                    CommonFiles_object.Attachment.remove(*fileslist)  # 使用 * 解包列表
                    fileslist.delete()  # 删除实体文件 model中的files_SopRom_delete方法

                    CommonFiles_object = CommonFiles.objects.get(id=ID)

                    CommonFiles_object.save()

                # except Exception as e:
                #     # alert = '此数据正被其他使用者编辑中...'
                #     errMsg = alert = str(e)
                #     print(alert)

                # mock_data
                check_dic = {}
                if request.POST.get('searchCG'):
                    check_dic['searchCG'] = request.POST.get('searchCG')
                if request.POST.get('searchSWHW'):
                    check_dic['searchSWHW'] = request.POST.get('searchSWHW')
                if request.POST.get('searchCategory_L1'):
                    check_dic['Category_L1'] = Category.objects.filter(
                        id=request.POST.get('searchCategory_L1')).first()
                if request.POST.get('searchCategory_L2'):
                    check_dic['Category_L2'] = SubCategory.objects.filter(
                        id=request.POST.get('searchCategory_L2')).first()
                if request.POST.get('searchOwner'):
                    user = UserInfo.objects.filter(account=request.POST.get('searchOwnerNumber')).first()
                    check_dic['Owner'] = user
                if check_dic:
                    mock_obj = CommonFiles.objects.filter(**check_dic).order_by('-created_at')

        else:
            try:
                request.body

            except:
                pass
            else:
                if 'upload' in str(request.body):
                    responseData = json.loads(request.body)
                    # print(responseData)

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
                    if True:
                        # print('1')
                        rownum = 0
                        startupload = 0
                        # print(xlsxlist)
                        uploadxlsxlist = []
                        C2s = []
                        for i in xlsxlist:
                            # print(type(i),i)
                            rownum += 1
                            modeldata = {}
                            for key, value in i.items():
                                if key in headermodel_Commonfiles.keys():
                                    # print(headermodel_Commonfiles[key],value)
                                    modeldata[headermodel_Commonfiles[key]] = value
                                # modeldata['created_at'] = datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')
                                # modeldata['updated_at'] = datetime.datetime.now().strftime('%m/%d/%Y %I:%M:%S %p') #auto
                                # modeldata['ModifiedDate'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            # print(modeldata)

                            if 'CG' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，CG不能爲空
                                                            """ % rownum
                                break
                            if 'SWHW' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，SWHW不能爲空
                                                            """ % rownum
                                break
                            if 'Category_L1' in modeldata.keys():
                                flag = False
                                for C1 in selectItem:
                                    if C1['name'] == modeldata['Category_L1']:
                                        # print(C1['name'], modeldata['Category_L1'])
                                        flag = True
                                        modeldata['Category_L1_id'] = Category.objects.get(name=modeldata['Category_L1']).id
                                        del modeldata['Category_L1']
                                        C2s = C1['SubCategorys']
                                        break
                                # print(flag)
                                if flag:
                                    startupload = 1
                                else:
                                    startupload = 0
                                    errMsg = """
                                                                            第"%s"條數據，Category_L1不在列表清单中，如需添加此清单项，请联系管理员
                                                                                                """ % rownum
                                    break
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Category_L1不能爲空
                                                            """ % rownum
                                break
                            if 'Category_L2' in modeldata.keys() and C2s:
                                # print(C2s,modeldata['Category_L2'],modeldata['Category_L2'] in C2s)

                                if any(d['name'] == modeldata['Category_L2'] for d in C2s):
                                    startupload = 1
                                    modeldata['Category_L2_id'] = SubCategory.objects.get(category=Category.objects.get(id=modeldata['Category_L1_id']), name=modeldata['Category_L2']).id
                                    del modeldata['Category_L2']
                                else:
                                    startupload = 0
                                    errMsg = """
                                                                            第"%s"條數據，Category_L2不在列表清单中，如需添加此清单项，请联系管理员
                                                                                                """ % rownum
                                    break
                            else:
                                # canEdit = 0
                                # startupload = 0
                                # errMsg = """
                                #         第"%s"條數據，Size不能爲空
                                #                             """ % rownum
                                pass
                            if 'Item' in modeldata.keys():
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Item不能爲空
                                                            """ % rownum
                                break
                            if 'Owner' in modeldata.keys():
                                modeldata['Owner'] = modeldata['Owner'].split('/')
                                modeldata['Creator'] = modeldata['Owner'][0]
                                startupload = 1
                            else:
                                # canEdit = 0
                                startupload = 0
                                errMsg = """
                                        第"%s"條數據，Owner工号不能爲空
                                                            """ % rownum
                                break

                            uploadxlsxlist.append(modeldata)
                            # print(create_list)
                        # print(errMsg, startupload)
                        # print(create_list,)
                        # print(startupload)
                        # print(rownum, type(rownum))
                        if startupload:
                            # 让数据可以从有值更新为无值
                            owner_data = []  # 单独保存每个对象对应的 Owner 数据
                            create_list = []
                            update_list = []
                            ComFileModelfiedlist = []
                            for i in CommonFiles._meta.fields:
                                if i.name != 'id':
                                    ComFileModelfiedlist.append([i.name, i.get_internal_type()])
                            for i in uploadxlsxlist:
                                # 深拷贝数据避免修改原始数据
                                data = i.copy()
                                for j in ComFileModelfiedlist:
                                        if j[0] not in i.keys():
                                            # print(j)
                                            if j[1] == "DateField" or j[1] == "ForeignKey":
                                                i[j[0]] = None
                                            else:
                                                i[j[0]] = ''
                                # if CommonFiles.objects.filter(Customer=i['CG'],SWHW=i['SWHW'],Category_L2=i['Category_L2'],
                                #                               Item=i['Item']):
                                #     update_list.append(i)
                                # else:
                                #     create_list.append(CommonFiles(**i))  # object(**dict)
                                # 提取并移除 Owner 字段
                                owner = data.pop("Owner", [])  # 假设这里存放用户 ID 列表
                                owner_data.append(owner)
                                create_list.append(CommonFiles(**data))  # object(**dict)
                                # print(create_list)
                            try:
                                with transaction.atomic():
                                    for i in uploadxlsxlist:
                                        print(i)
                                        UserInfos = UserInfo.objects.filter(account__in=i['Owner'])
                                        del i['Owner']
                                        CommonFiles_object = CommonFiles.objects.create(**i)
                                        CommonFiles_object.Owner.add(*UserInfos)
                                        CommonFiles_object.save()
                                    # if create_list:
                                    #     created_objs = CommonFiles.objects.bulk_create(create_list)# Category_L1,Category_L2也都是many_to_many
                                    #     #在 Django 中使用 bulk_create() 时，不能直接为多对多字段（如 Owner）赋值。这是因为多对多关系需要额外的中间表记录，而 bulk_create() 不会自动处理这种关系。
                                    #     # 3. 处理多对多关系
                                    #     for obj, owner in zip(created_objs, owner_data):
                                    #         # 获取用户对象集合
                                    #         UserInfos = UserInfo.objects.filter(account__in=owner)
                                    #
                                    #         # 设置多对多关系（使用 add()）
                                    #         obj.Owner.add(*UserInfos)  # 注意这里的 *
                                    if update_list:
                                        pass
                            except Exception as e:
                                # alert = '此数据正被其他使用者编辑中...'
                                errMsg = str(e)
                                print(errMsg)
                            # mock_data
                            check_dic = {}
                            if responseData['searchCG']:
                                check_dic['searchCG'] = Category.objects.filter(id=responseData['searchCG']).first()
                            if responseData['searchSWHW']:
                                check_dic['searchSWHW'] = SubCategory.objects.filter(
                                    id=responseData['searchSWHW']).first()
                            if responseData['searchCategory_L1']:
                                check_dic['searchCategory_L1'] = SubCategory.objects.filter(
                                    id=responseData['searchCategory_L1']).first()
                            if responseData['searchCategory_L2']:
                                check_dic['searchCategory_L2'] = SubCategory.objects.filter(
                                    id=responseData['searchCategory_L2']).first()
                            if responseData['searchOwner']:
                                user = UserInfo.objects.filter(account=responseData['searchOwnerNumber']).first()
                                check_dic['Owner'] = user
                            if check_dic:
                                mock_obj = CommonFiles.objects.filter(**check_dic).order_by('-created_at')

                if 'delete' in str(request.body):
                    responseData = json.loads(request.body)
                    for i in responseData['params']:
                        # print(i)
                        files_to_delete = []
                        # print(CommonFiles.objects.get(id=i).Attachment.all())
                        for j in CommonFiles.objects.get(id=i).Attachment.all():
                            files_to_delete.append(j.id)
                        # print(files_to_delete)
                        fileslist = files.objects.filter(id__in=files_to_delete)  # 最好是用id，这样搜索时就需要返回带id的信息
                        # print(vedios)

                        # 解除关联
                        CommonFiles.objects.get(id=i).Attachment.remove(*fileslist)  # 使用 * 解包列表
                        fileslist.delete()  # 删除实体文件 model中的files_SopRom_delete方法
                        CommonFiles.objects.get(id=i).delete()
                    # mock_data
                    check_dic = {}
                    if responseData['searchCG']:
                        check_dic['searchCG'] = Category.objects.filter(id=responseData['searchCG']).first()
                    if responseData['searchSWHW']:
                        check_dic['searchSWHW'] = SubCategory.objects.filter(id=responseData['searchSWHW']).first()
                    if responseData['searchCategory_L1']:
                        check_dic['searchCategory_L1'] = SubCategory.objects.filter(
                            id=responseData['searchCategory_L1']).first()
                    if responseData['searchCategory_L2']:
                        check_dic['searchCategory_L2'] = SubCategory.objects.filter(
                            id=responseData['searchCategory_L2']).first()
                    if responseData['searchOwner']:
                        user = UserInfo.objects.filter(account=responseData['searchOwnerNumber']).first()
                        check_dic['Owner'] = user
                    if check_dic:
                        mock_obj = CommonFiles.objects.filter(**check_dic).order_by('-created_at')

        # mock_data
        for i in mock_obj:

            # Ownerflag = False
            # for j in i.Owner.all():
            #     Owner_list.append(
            #         {
            #             "account": j.account, "username": j.username, "id": j.id
            #         }
            #     )
            #     if not Ownerflag:
            #         if j.account == onlineuser:
            #             Ownerflag = True
            Attachmentlist = []
            for h in i.Attachment.all():
                Attachmentlist.append({"id": h.id, "url": "/media/" + str(h.files)})

            Owner_list = []
            Ownerflag = False
            for j in i.Owner.all():
                Owner_list.append(
                    {
                        "account": j.account, "username": j.username, "id": j.id
                    }
                )
                if not Ownerflag:
                    if j.account == onlineuser:
                        Ownerflag = True

            mock_data.append(
                {
                    "id": i.id,
                    "CG": i.CG,
                    "SWHW": i.SWHW,
                    "Category_L1": Category.objects.filter(name=i.Category_L1).first().id,
                    "Category_L2": SubCategory.objects.filter(name=i.Category_L2).first().id if i.Category_L2 else '',
                    "Item": i.Item,
                    "Description": i.Description,
                    "Version": i.Version,
                    "updated_at": str(i.updated_at) if i.updated_at else '',
                    "Owner": Owner_list,
                    "Creator": UserInfo.objects.filter(
                        account=i.Creator).first().username + "/" + i.Creator if UserInfo.objects.filter(
                        account=i.Creator) else '',
                    "Ownerflag": Ownerflag,  # 只要是Owner中的一个有权限，Owner改变了权限就会随之变化
                    "Attachment": Attachmentlist,
                }
            )
                # print(mock_data)
        # except Exception as e:
        #     errMsg = str(e)
        data = {
            "errMsg": errMsg,
            "sectionOwner": sectionOwner,
            "OwnersOptions": OwnersOptions,
            "StatusOptions": StatusOptions,
            "allSubCategorys": allSubCategorys,
            "allCategorys": allCategorys,
            "content": mock_data,
            "permission": permission,
            "SSVIP_users": SSVIP_users,
            "selectItem": selectItem,
            "categoryOptions": categoryOptions,
            "CGOptions": CGOptions,
            "SWHWOptions": SWHWOptions,

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CommonFiles/ComFilesEdit.html', locals())
