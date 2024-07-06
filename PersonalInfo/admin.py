from django.contrib import admin

# Register your models here.
from .models import local_identity, Departments, Positions, MajorIfo, Portraits, PersonalInfo, PersonalInfoHisByPer, PersonalInfoHisByYear, MainPower, WorkOvertime, LeaveInfo

@admin.register(local_identity)
class local_identityAdmin(admin.ModelAdmin):

    list_display = ('provincecode', 'provincevalue', 'citycode', 'cityvalue', 'countycode', 'countyvalue', 'longitude', 'latitude', )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-provincevalue',)
    #后台数据列表排序方式
    list_display_links = ('provincecode', 'provincevalue', 'citycode', 'cityvalue', 'countycode', 'countyvalue', 'longitude', 'latitude', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'provincevalue',
        'cityvalue',
        'countyvalue',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('provincecode', 'provincevalue', 'citycode', 'cityvalue', 'countycode', 'countyvalue', 'longitude', 'latitude',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Departments)
class DepartmentsAdmin(admin.ModelAdmin):

    list_display = ('Year', 'Companys', 'Plants', 'CHU', 'BU', 'KE', 'Customer', 'Department_Code', 'Manager',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year', 'Companys', 'Plants', 'CHU', 'BU', 'KE', 'Customer', 'Department_Code', 'Manager', )
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year', 'Companys', 'Plants', 'CHU', 'BU', 'KE', 'Customer', 'Department_Code', 'Manager',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year', 'Companys', 'Plants', 'CHU', 'BU', 'KE', 'Customer', 'Department_Code', 'Manager',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Positions)
class PositionsAdmin(admin.ModelAdmin):

    list_display = ('Year', 'Grade', 'Item', 'Nationality', 'Positions_Code', 'Positions_Name',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Grade', 'Item', 'Nationality', 'Positions_Code', 'Positions_Name',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year', 'Grade', 'Item', 'Nationality', 'Positions_Code', 'Positions_Name',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year', 'Grade', 'Item', 'Nationality', 'Positions_Code', 'Positions_Name',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(MajorIfo)
class MajorIfoAdmin(admin.ModelAdmin):

    list_display = ('Education', 'Categories', 'Subject', 'category', 'Major', 'MajorForExcel',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Education',)
    #后台数据列表排序方式
    list_display_links = ('Education', 'Categories', 'Subject', 'category', 'Major', 'MajorForExcel',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Education', 'Categories', 'Subject', 'category', 'Major', 'MajorForExcel',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Education', 'Categories', 'Subject', 'category', 'Major', 'MajorForExcel',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(Portraits)
class PortraitsAdmin(admin.ModelAdmin):

    list_display = ('img', 'single',)
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-single',)
    #后台数据列表排序方式
    list_display_links = ('img', 'single',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'img', 'single',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('img', 'single',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

from django.utils.safestring import mark_safe
@admin.register(PersonalInfo)
class PersonalInfoAdmin(admin.ModelAdmin):
    def upload_img(self, obj):
        img = ''
        try:
            for imgurls in obj.Portrait.all():
                # print(imgurls)
                # imgurls.append(imgurls.img)
                img = mark_safe('<img src="/media/%s" width="50px" />' % (imgurls.img,))
        except Exception as e:
            print(e)
            img = ''
        print(img)
        return img
        # return '， '.join(img)

    upload_img.short_description = 'Thumb'
    upload_img.allow_tags = True

    list_display = ('Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',
                    # 'Portrait',
                    'upload_img',
                    )
    readonly_fields = ['upload_img']

    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-DepartmentCode',)
    #后台数据列表排序方式
    list_display_links = ('Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Status',
        'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
    filter_horizontal = ('Portrait',)

@admin.register(PersonalInfoHisByYear)
class PersonalInfoHisByYearAdmin(admin.ModelAdmin):

    list_display = ('Year', 'Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',
                    # 'Portrait',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year', 'Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year', 'Status',
        'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year', 'Status', 'RegistrationDate', 'QuitDate', 'PlanQuitDate', 'QuitReason', 'QuitDetail', 'Whereabouts', 'NewCompany', 'Aalary', 'LastAchievements',
                    'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'LastPromotionData',
                    'RegistPosition', 'PositionTimes', 'Experience', 'GraduationYear', 'Education', 'School', 'Major', 'MajorAscription', 'ENLevel', 'IdCard',
                    'NativeProvince', 'NativeCity', 'NativeCounty', 'ResidenceProvince', 'ResidenceCity', 'ResidenceCounty', 'MobileNum',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选
    filter_horizontal = ('Portrait',)

@admin.register(PersonalInfoHisByPer)
class PersonalInfoHisByPerAdmin(admin.ModelAdmin):

    list_display = ('ChangeType',
                    'Customer', 'Department', 'DepartmentCode', 'DepartmentCodeYear', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'PositionOld', 'LastPromotionData',
                    'IntervalTime',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-DepartmentCode',)
    #后台数据列表排序方式
    list_display_links = ('ChangeType',
                    'Customer', 'Department', 'DepartmentCode', 'DepartmentCodeYear', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'PositionOld', 'LastPromotionData',
                    'IntervalTime',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'ChangeType',
        'Customer', 'Department', 'DepartmentCode', 'GroupNum', 'SAPNum', 'CNName',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('ChangeType',
                    'Customer', 'Department', 'DepartmentCode', 'DepartmentCodeYear', 'GroupNum', 'SAPNum', 'CNName', 'EngName', 'Sex', 'PositionNow', 'PositionOld', 'LastPromotionData',
                    'IntervalTime',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(MainPower)
class MainPowerAdmin(admin.ModelAdmin):

    list_display = ('Year',
                    'Companys', 'Plants', 'DepartmentCode', 'CHU', 'BU', 'KE', 'Customer', 'Item', 'Positions_Name', 'CodeNoH01', 'CodeNoH02',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Year',
                    'Companys', 'Plants', 'DepartmentCode', 'CHU', 'BU', 'KE', 'Customer', 'Item', 'Positions_Name', 'CodeNoH01', 'CodeNoH02',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Year',
        'DepartmentCode', 'CHU', 'BU', 'KE', 'Customer', 'Item', 'Positions_Name',

        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Year',
                    'Companys', 'Plants', 'DepartmentCode', 'CHU', 'BU', 'KE', 'Customer', 'Item', 'Positions_Name', 'CodeNoH01', 'CodeNoH02',
                    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(WorkOvertime)
class WorkOvertimeAdmin(admin.ModelAdmin):

    list_display = ('SalaryRange',
                    'Department_Code', 'Department_Des', 'GroupNum', 'CNName', 'RegistDate', 'PerNature', 'Classes', 'Year', 'Mounth',
                    'Peacetime', 'NationalHoliday', 'PeriodHoliday', 'Total',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('SalaryRange',
                    'Department_Code', 'Department_Des', 'GroupNum', 'CNName', 'RegistDate', 'PerNature', 'Classes', 'Year', 'Mounth',
                    'Peacetime', 'NationalHoliday', 'PeriodHoliday', 'Total',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Department_Code', 'GroupNum', 'CNName','Year', 'Mounth',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('SalaryRange',
                    'Department_Code', 'Department_Des', 'GroupNum', 'CNName', 'RegistDate', 'PerNature', 'Classes', 'Year', 'Mounth',
                    'Peacetime', 'NationalHoliday', 'PeriodHoliday', 'Total',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选

@admin.register(LeaveInfo)
class LeaveInfoAdmin(admin.ModelAdmin):

    list_display = ('Department_Code',
                    'GroupNum', 'CNName', 'Year', 'Mounth', 'PublicHoliday', 'WorkInjury', 'Matters', 'MattersContinuation', 'Sick',
                    'SickContinuation', 'Marriage', 'Bereavement', 'Special','OffDuty','Compensatory','EpidemicPrevention','NoScheduling',
                    'PaternityLeave', 'Absenteeism', 'Maternity', 'PregnancyExamination', 'Lactation', 'Others', 'Total',
                    )
    # 列表里显示想要显示的字段
    list_per_page = 500
    # 满50条数据就自动分页
    ordering = ('-Year',)
    #后台数据列表排序方式
    list_display_links = ('Department_Code',
                    'GroupNum', 'CNName', 'Year', 'Mounth', 'PublicHoliday', 'WorkInjury', 'Matters', 'MattersContinuation', 'Sick',
                    'SickContinuation', 'Marriage', 'Bereavement', 'Special','OffDuty','Compensatory','EpidemicPrevention','NoScheduling',
                    'PaternityLeave', 'Absenteeism', 'Maternity', 'PregnancyExamination', 'Lactation', 'Others', 'Total',)
    # 设置哪些字段可以点击进入编辑界面
    # list_editable = ('Object',)
    # 筛选器
    list_filter = (
        'Department_Code',
        'GroupNum', 'CNName', 'Year', 'Mounth',
        # ('Customer', UnionFieldListFilter),
        # ('Phase', UnionFieldListFilter),
    )
    search_fields = ('Department_Code',
                    'GroupNum', 'CNName', 'Year', 'Mounth', 'PublicHoliday', 'WorkInjury', 'Matters', 'MattersContinuation', 'Sick',
                    'SickContinuation', 'Marriage', 'Bereavement', 'Special','OffDuty','Compensatory','EpidemicPrevention','NoScheduling',
                    'PaternityLeave', 'Absenteeism', 'Maternity', 'PregnancyExamination', 'Lactation', 'Others', 'Total',)  # 搜索字段
    # date_hierarchy = 'Start_time'  # 详细时间分层筛选