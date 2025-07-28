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
from .models import CommonDevice, Category, SubCategory
from django.db.models.functions import ExtractYear

from django.db import models


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
def CommonDevice_edit(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    Skin = request.COOKIES.get('Skin_raw')
    # print(Skin)
    if not Skin:
        Skin = "/static/src/blue.jpg"
    weizhi = "DepartmentManage/公共設備"

    allCategorys = {}
    categoryOptions = []
    for i in Category.objects.all():
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
    for i in Category.objects.all():
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
    for i in CommonDevice._meta.get_field('Dev_Status').choices:
        StatusOptions.append(i[0])
    # print(StatusOptions, 'StatusOptions')

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
    tableColumns = get_table_columns(CommonDevice)
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
    mock_obj = CommonDevice.objects.all().order_by('-created_at')

    if request.method == "POST":
        try:
            if request.POST:
                ch_dic = {}
                if request.POST.get('isGetData') == 'SEARCH':
                    if request.POST.get('Category'):
                        ch_dic['Category'] = Category.objects.filter(id=request.POST.get('Category')).first()
                    if request.POST.get('Product_Type'):
                        ch_dic['Product_Type'] = SubCategory.objects.filter(id=request.POST.get('Product_Type')).first()
                    if request.POST.get('Owner'):
                        user = UserInfo.objects.filter(account=request.POST.get('OwnerNumber')).first()
                        ch_dic['Owner'] = user
                    if ch_dic:
                        mock_obj = CommonDevice.objects.filter(**ch_dic).order_by('-created_at')
                if request.POST.get('action') == 'addData':
                    # ID = request.POST.get('ID')
                    Owners = json.loads(request.POST.get('Owner'))
                    # print(Owners)
                    Mail = ''
                    UserInfos = UserInfo.objects.filter(account__in=Owners)
                    # print(UserInfos)
                    for i in UserInfos:
                        Mail += '%s/' % i.email.split('@')[0]
                    # print(Mail)
                    Mail = Mail[:-1] + '@Compal.com'
                    # print(Mail)
                    create_dic = {
                        "Category_id": request.POST.get('Category'),
                        "Product_Type_id": request.POST.get('Product_Type'),
                        "Name": request.POST.get('Name') if request.POST.get('Name') else '',
                        "Num": request.POST.get('Num') if request.POST.get('Num') else '',
                        "Manufacturer": request.POST.get('Manufacturer') if request.POST.get('Manufacturer') else '',
                        "Cost": request.POST.get('Cost') if request.POST.get('Cost') else '',
                        "Account": request.POST.get('Account') if request.POST.get('Account') and request.POST.get(
                            'Account') != 'null' else None,
                        "PW": request.POST.get('PW') if request.POST.get('PW') else '',
                        "Purchasing_Date": request.POST.get('Purchasing_Date') if request.POST.get(
                            'Purchasing_Date') and request.POST.get('Account') != 'None' and request.POST.get(
                            'Account') != 'null' else None,
                        "Department": request.POST.get('Department') if request.POST.get('Department') else '',
                        # 从有值变成空值的更新,整型，浮点型，日期都是None
                        "Location": request.POST.get('Location') if request.POST.get('Location') else '',
                        "Asset_Num": request.POST.get('Asset_Num') if request.POST.get('Asset_Num') else '',
                        "Dev_Status": request.POST.get('Status') if request.POST.get('Status') else '',
                        "Purpose": request.POST.get('Purpose') if request.POST.get('Purpose') else '',
                        "Mail": Mail,
                        "Contact_info": request.POST.get('Contact_info') if request.POST.get('Contact_info') else '',
                        "Comments": request.POST.get('Comments') if request.POST.get('Comments') else '',
                        "Creator": onlineuser,
                    }
                    # try:
                    with transaction.atomic():
                        Comdevice = CommonDevice.objects.create(**create_dic)
                        Comdevice.Owner.add(*UserInfos)

                        Comdevice.Category = Category.objects.get(id=request.POST.get('Category'))
                        Comdevice.Product_Type = SubCategory.objects.get(id=request.POST.get('Product_Type'))
                        Comdevice.save()
                    # except Exception as e:
                    #     # alert = '此数据正被其他使用者编辑中...'
                    #     errMsg = alert = str(e)
                    #     print(alert)

                    # mock_data
                    check_dic = {}
                    if request.POST.get('searchCategory'):
                        check_dic['Category'] = Category.objects.filter(id=request.POST.get('searchCategory')).first()
                    if request.POST.get('searchProduct_Type'):
                        check_dic['Product_Type'] = SubCategory.objects.filter(id=request.POST.get('searchProduct_Type')).first()
                    if request.POST.get('searchOwner'):
                        user = UserInfo.objects.filter(account=request.POST.get('searchOwnerNumber')).first()
                        check_dic['Owner'] = user
                    if check_dic:
                        mock_obj = CommonDevice.objects.filter(**check_dic).order_by('-created_at')
                if request.POST.get('action') == 'update':
                    ID = request.POST.get('ID')
                    Owners = json.loads(request.POST.get('Owner'))
                    # print(Owners)
                    Mail = ''
                    UserInfos = UserInfo.objects.filter(account__in=Owners)
                    # print(UserInfos)
                    for i in UserInfos:
                        Mail += '%s/' % i.email.split('@')[0]
                    # print(Mail)
                    Mail = Mail[:-1] + '@Compal.com'
                    # print(Mail)
                    update_dic = {
                        "Category_id": request.POST.get('Category'),
                        "Product_Type_id": request.POST.get('Product_Type'),
                        "Name": request.POST.get('Name') if request.POST.get('Name') else '',
                        "Num": request.POST.get('Num') if request.POST.get('Num') else '',
                        "Manufacturer": request.POST.get('Manufacturer') if request.POST.get('Manufacturer') else '',
                        "Cost": request.POST.get('Cost') if request.POST.get('Cost') else '',
                        "Account": request.POST.get('Account') if request.POST.get('Account') and request.POST.get(
                            'Account') != 'null' else None,
                        "PW": request.POST.get('PW') if request.POST.get('PW') else '',
                        "Purchasing_Date": request.POST.get('Purchasing_Date') if request.POST.get(
                            'Purchasing_Date') and request.POST.get('Account') != 'None' and request.POST.get(
                            'Account') != 'null' else None,
                        "Department": request.POST.get('Department') if request.POST.get('Department') else '',
                        # 从有值变成空值的更新,整型，浮点型，日期都是None
                        "Location": request.POST.get('Location') if request.POST.get('Location') else '',
                        "Asset_Num": request.POST.get('Asset_Num') if request.POST.get('Asset_Num') else '',
                        "Dev_Status": request.POST.get('Status') if request.POST.get('Status') else '',
                        "Purpose": request.POST.get('Purpose') if request.POST.get('Purpose') else '',
                        "Mail": Mail,
                        "Contact_info": request.POST.get('Contact_info') if request.POST.get('Contact_info') else '',
                        "Comments": request.POST.get('Comments') if request.POST.get('Comments') else '',
                    }
                    try:
                        with transaction.atomic():
                            CommonDevice.objects.filter(id=ID).update(**update_dic)

                            Comdevice = CommonDevice.objects.get(id=ID)
                            Comdevice.Owner.clear()
                            Comdevice.Owner.add(*UserInfos)

                            # Comdevice.Category = Category.objects.get(id=request.POST.get('Category'))
                            # Comdevice.Product_Type = SubCategory.objects.get(id=request.POST.get('Product_Type'))
                            # Comdevice.save()

                    except Exception as e:
                        # alert = '此数据正被其他使用者编辑中...'
                        errMsg = alert = str(e)
                        print(alert)

                    # mock_data
                    check_dic = {}
                    if request.POST.get('searchCategory'):
                        check_dic['Category'] = Category.objects.filter(id=request.POST.get('searchCategory')).first()
                    if request.POST.get('searchProduct_Type'):
                        check_dic['Product_Type'] = SubCategory.objects.filter(id=request.POST.get('searchProduct_Type')).first()
                    if request.POST.get('searchOwner'):
                        user = UserInfo.objects.filter(account=request.POST.get('searchOwnerNumber')).first()
                        check_dic['Owner'] = user
                    if check_dic:
                        mock_obj = CommonDevice.objects.filter(**check_dic).order_by('-created_at')

            else:
                try:
                    request.body

                except:
                    pass
                else:
                    if 'delete' in str(request.body):
                        responseData = json.loads(request.body)
                        for i in responseData['params']:
                            print(i)
                            CommonDevice.objects.get(id=i).delete()
                        # mock_data
                        check_dic = {}
                        if responseData['searchCategory']:
                            check_dic['Category'] = Category.objects.filter(id=responseData['searchCategory']).first()
                        if responseData['searchProduct_Type']:
                            check_dic['Product_Type'] = SubCategory.objects.filter(id=responseData['searchProduct_Type']).first()
                        if responseData['searchOwner']:
                            user = UserInfo.objects.filter(account=responseData['searchOwnerNumber']).first()
                            check_dic['Owner'] = user
                        if check_dic:
                            mock_obj = CommonDevice.objects.filter(**check_dic).order_by('-created_at')

            # mock_data
            for i in mock_obj:
                Duration = ''
                if i.Purchasing_Date:
                    if datetime.datetime.now().date() > i.Purchasing_Date:
                        Duration = round(
                            float(
                                str((datetime.datetime.now().date() - i.Purchasing_Date)).split(' ')[
                                    0]) / 365,
                            2)
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
                        "id": i.id, "Category": Category.objects.filter(name=i.Category).first().id,
                        "Product_Type": SubCategory.objects.filter(name=i.Product_Type).first().id,
                        "Name": i.Name,
                        "Num": i.Num,
                        "Manufacturer": i.Manufacturer,
                        "Cost": i.Cost,
                        "Account": i.Account,
                        "PW": i.PW,
                        "Purchasing_Date": str(i.Purchasing_Date) if i.Purchasing_Date else '',
                        "Duration": Duration,
                        "Department": i.Department,
                        "Location": i.Location,
                        "Asset_Num": i.Asset_Num,
                        "Status": i.Dev_Status,
                        "Purpose": i.Purpose,
                        "Owner": Owner_list,
                        "Mail": i.Mail,
                        "Contact_info": i.Contact_info,
                        "Comments": i.Comments,
                        "Creator": i.Creator,
                        # "Ownerflag": i.Creator == onlineuser, creator才有权限。
                        "Ownerflag": Ownerflag, # 只要是Owner中的一个有权限，Owner改变了权限就会随之变化
                        'CreatedBy': UserInfo.objects.filter(account=i.Creator).first().username if UserInfo.objects.filter(account=i.Creator).first() else '',
                    }
                )
            # print(mock_data)
        except Exception as e:
            errMsg = str(e)
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

        }
        # print(data)
        return HttpResponse(json.dumps(data), content_type="application/json")
    return render(request, 'CommonDevice/CommonDevice.html', locals())

