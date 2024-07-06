from django.db import models

# Create your models here.
class local_identity(models.Model):
    provincecode = models.CharField("provincecode", max_length=6)
    provincevalue = models.CharField("provincevalue", max_length=50)
    citycode = models.CharField("citycode", max_length=6)
    cityvalue = models.CharField("cityvalue", max_length=50)
    countycode = models.CharField("countycode", max_length=6)
    countyvalue = models.CharField("countyvalue", max_length=50)
    longitude = models.CharField("longitude", max_length=6)
    latitude = models.CharField("latitude", max_length=100)
    class Meta:
        verbose_name = '地区代码'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

class Departments(models.Model):
    Year = models.CharField("年份", max_length=100)
    Companys = models.CharField("公司別", max_length=100, null=True, blank=True)
    Plants = models.CharField("厂区", max_length=100, null=True, blank=True)
    CHU = models.CharField("处", max_length=50)
    BU = models.CharField("部", max_length=50, null=True, blank=True)
    KE = models.CharField("课", max_length=50, null=True, blank=True)
    Customer = models.CharField("客户别", max_length=50)
    Department_Code = models.CharField("部门代码", max_length=50)
    Manager = models.CharField("管理者", max_length=50)
    parent = models.ForeignKey("Departments", null=True, blank=True, on_delete=True, verbose_name="上级部门")
    class Meta:
        verbose_name = '部门信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # 显示层级菜单
        title_list = [self.Department_Code]
        p = self.parent
        while p:
            title_list.insert(0, p.Department_Code)
            p = p.parent
        return '-'.join(title_list)

class Positions(models.Model):
    Grade = models.CharField("职等", max_length=10)#職等
    Item = models.CharField("项次", max_length=100)#項次
    Nationality = models.CharField("国籍", max_length=10)#國籍
    Positions_Code = models.CharField("职称代码", max_length=50)#職稱代碼
    Positions_Name = models.CharField("职称", max_length=50)#職稱
    Year = models.CharField("年份", max_length=100, default='')
    class Meta:
        verbose_name = '职位信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Grade}-{Item}-{Nationality}-{Positions_Code}-{Positions_Name}'.format(Grade=self.Grade, Item=self.Item,
            Nationality=self.Nationality, Positions_Code=self.Positions_Code, Positions_Name=self.Positions_Name,)

class MajorIfo(models.Model):
    Education = models.CharField("学历", max_length=20)  # 學歷
    Categories = models.CharField("大类", max_length=20)  # 大類
    Subject = models.CharField("学科", max_length=100)  # 學科
    category = models.CharField("门类", max_length=100)  # 門類
    Major = models.CharField("专业", max_length=100)  # 專業
    MajorForExcel = models.CharField("专业公式查找", max_length=100)  # 專業 for 公式查找
    class Meta:
        verbose_name = '专业信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

class Portraits(models.Model):
    # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
    img = models.ImageField(upload_to='Portraits/', verbose_name='头像地址')
    single = models.CharField(max_length=200,null=True, blank=True,verbose_name='头像名称')
    class Meta:
        verbose_name = '头像'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.img)

    # def __str__(self):
    #     return str(self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=Portraits)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)

class PersonalInfo(models.Model):

    Status = models.CharField("状态", max_length=10)#狀態
    RegistrationDate = models.DateField("报道日期", null=True, blank=True)#報到日期
    OldCustomer = models.CharField("原客户", max_length=20, null=True, blank=True, default='')  # 客戶
    transferDate = models.DateField("轉職日期", null=True, blank=True)#轉職日期
    OldDepartmentCode = models.CharField("原部门代码", max_length=50, null=True, blank=True, default='')
    #离职信息
    QuitDate = models.DateField("离职日期", null=True, blank=True)#離職日期
    PlanQuitDate = models.DateField("预计离职日期", null=True, blank=True)#预计离职日期
    QuitReason = models.CharField("离职原因", max_length=100, null=True, blank=True)#離職原因
    QuitDetail = models.CharField("离职详情", max_length=1000, null=True, blank=True)#离职详情
    Whereabouts = models.CharField("离职去向", max_length=50, null=True, blank=True)#離職去向
    NewCompany = models.CharField("新公司名称", max_length=100, null=True, blank=True)#新公司名稱
    Aalary = models.CharField("薪资", max_length=50, null=True, blank=True)#薪资
    LastAchievements = models.CharField("最后一次绩效", max_length=10, null=True, blank=True)#最近一次績效

    Customer = models.CharField("客户", max_length=20)#客戶
    Department = models.CharField("部门", max_length=50)#部門
    DepartmentCode = models.CharField("部门代码", max_length=50)#課別
    GroupNum = models.CharField("集团员工", max_length=50)#集團員工
    SAPNum = models.CharField("SAP员工", max_length=50, null=True, blank=True)#SAP員工
    CNName = models.CharField("中文姓名", max_length=50)#中文姓名
    EngName = models.CharField("英文姓名", max_length=50)#英文姓名
    Sex = models.CharField("性别", max_length=20)#性別
    PositionNow = models.CharField("现职称", max_length=20)#現職稱
    LastPromotionData = models.DateField("最近一次晋升日期", null=True, blank=True)#最近一次晉升日期
    RegistPosition = models.CharField("入职职称", max_length=20)#入職職稱
    PositionTimes = models.CharField("晋升次数", max_length=20)#晉升次數
    Experience = models.CharField("是否承认工作经验", max_length=20)  #是否承認工作經驗
    GraduationYear = models.CharField("毕业年度", max_length=20) #畢業年度
    Education = models.CharField("学历", max_length=20) #學歷
    School = models.CharField("学校", max_length=20) #學校
    Major = models.CharField("专业", max_length=500) #專業
    MajorAscription = models.CharField("专业归属", max_length=500) #專業歸屬
    ENLevel = models.CharField("英语", max_length=500, null=True, blank=True) #英語
    IdCard = models.CharField("身份证号", max_length=500) #身份証號
    NativeProvince = models.CharField("籍贯省份", max_length=100) #籍貫省份
    NativeCity = models.CharField("籍贯地市", max_length=100) #籍貫地市
    NativeCounty = models.CharField("籍贯县市", max_length=100) #籍貫縣市
    ResidenceProvince = models.CharField("户口省份", max_length=100)  # 戶口省份
    ResidenceCity = models.CharField("户口地市", max_length=100)  # 戶口地市
    ResidenceCounty = models.CharField("户口县市", max_length=100)  # 戶口縣市
    MobileNum = models.CharField("手机号码", max_length=20)  # 手機號碼
    Portrait = models.ManyToManyField(Portraits, related_name='Portrait', blank=True, verbose_name='头像')  # 头像表

    class Meta:
        verbose_name = '人员信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{GroupNum}-{SAPNum}-{CNName}-{EngName}'.format(GroupNum=self.GroupNum, SAPNum=self.SAPNum,
            CNName=self.CNName, EngName=self.EngName,)

class PersonalInfoHisByYear(models.Model):
    Year = models.CharField("年份", max_length=100)  # 數據年份
    Status = models.CharField("状态", max_length=10)#狀態
    RegistrationDate = models.DateField("报道日期", null=True, blank=True)#報到日期
    transferDate = models.DateField("轉職日期", null=True, blank=True)  # 轉職日期
    OldCustomer = models.CharField("原客户", max_length=20, null=True, blank=True, default='')  # 客戶
    OldDepartmentCode = models.CharField("原部门代码", max_length=50, null=True, blank=True, default='')
    #离职信息
    QuitDate = models.DateField("离职日期", null=True, blank=True)#離職日期
    PlanQuitDate = models.DateField("预计离职日期", null=True, blank=True)#预计离职日期
    QuitReason = models.CharField("离职原因", max_length=100, null=True, blank=True)#離職原因
    QuitDetail = models.CharField("离职详情", max_length=1000, null=True, blank=True)#离职详情
    Whereabouts = models.CharField("离职去向", max_length=50, null=True, blank=True)#離職去向
    NewCompany = models.CharField("新公司名称", max_length=100, null=True, blank=True)#新公司名稱
    Aalary = models.CharField("薪资", max_length=50, null=True, blank=True)#薪资
    LastAchievements = models.CharField("最后一次绩效", max_length=10, null=True, blank=True)#最近一次績效

    Customer = models.CharField("客户", max_length=20)#客戶
    Department = models.CharField("部门", max_length=50)#部門
    DepartmentCode = models.CharField("部门代码", max_length=50)#課別
    GroupNum = models.CharField("集团员工", max_length=50)#集團員工
    SAPNum = models.CharField("SAP员工", max_length=50)#SAP員工
    CNName = models.CharField("中文姓名", max_length=50, null=True, blank=True)#中文姓名
    EngName = models.CharField("英文姓名", max_length=50)#英文姓名
    Sex = models.CharField("性别", max_length=20)#性別
    PositionNow = models.CharField("现职称", max_length=20)#現職稱
    LastPromotionData = models.DateField("最后一次晋升日期", null=True)#最近一次晉升日期
    RegistPosition = models.CharField("入职职称", max_length=20)#入職職稱
    PositionTimes = models.CharField("晋升次数", max_length=20)#晉升次數
    Experience = models.CharField("是否承认工作经验", max_length=20)  #是否承認工作經驗
    GraduationYear = models.CharField("毕业年度", max_length=20) #畢業年度
    Education = models.CharField("学历", max_length=20) #學歷
    School = models.CharField("学校", max_length=20) #學校
    Major = models.CharField("专业", max_length=500) #專業
    MajorAscription = models.CharField("专业归属", max_length=500) #專業歸屬
    ENLevel = models.CharField("英语", max_length=500, null=True, blank=True) #英語
    IdCard = models.CharField("身份证号", max_length=500) #身份証號
    NativeProvince = models.CharField("籍贯省份", max_length=100) #籍貫省份
    NativeCity = models.CharField("籍贯地市", max_length=100) #籍貫地市
    NativeCounty = models.CharField("籍贯县市", max_length=100) #籍貫縣市
    ResidenceProvince = models.CharField("户口省份", max_length=100)  # 戶口省份
    ResidenceCity = models.CharField("户口地市", max_length=100)  # 戶口地市
    ResidenceCounty = models.CharField("户口县市", max_length=100)  # 戶口縣市
    MobileNum = models.CharField("手机号码", max_length=20)  # 手機號碼
    Portrait = models.ManyToManyField(Portraits, related_name='PortraitH', blank=True, verbose_name='头像')  # 手機號碼

    class Meta:
        verbose_name = '往年人员信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{GroupNum}-{SAPNum}-{CNName}-{EngName}'.format(GroupNum=self.GroupNum, SAPNum=self.SAPNum,
            CNName=self.CNName, EngName=self.EngName,)

class PersonalInfoHisByPer(models.Model):
    Personallink = models.ForeignKey('PersonalInfo', on_delete=True, blank=True, verbose_name="人员信息")
    ChangeType = models.CharField('修改类型', max_length=5)
    Customer = models.CharField('客户', max_length=5)
    Department = models.CharField("部门", max_length=50)
    DepartmentCode = models.CharField("部门代码", max_length=50)
    DepartmentCodeYear = models.CharField("部门代码年份", max_length=10)
    GroupNum = models.CharField("集团员工", max_length=50)
    SAPNum = models.CharField("SAP员工", max_length=50)
    CNName = models.CharField("中文姓名", max_length=50)
    EngName = models.CharField("英文姓名", max_length=50)
    Sex = models.CharField("性别", max_length=20)  # 性別
    PositionNow = models.CharField("现职称", max_length=20)  # 現職稱
    PositionOld = models.CharField("原职称", max_length=20)
    LastPromotionData = models.DateField("最近一次晋升日期", null=True, blank=True)  # 最近一次晉升日期
    IntervalTime = models.CharField("间隔时间", max_length=20)#間隔時間
    Editor = models.CharField("编辑者", max_length=100)
    EditTime = models.CharField('编辑时间', max_length=26,)
    class Meta:
        verbose_name = '人员晋升历史'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{GroupNum}-{SAPNum}-{CNName}-{PositionNow}-{LastPromotionData}'.format(GroupNum=self.GroupNum, SAPNum=self.SAPNum,
            CNName=self.CNName, PositionNow=self.PositionNow, LastPromotionData=self.LastPromotionData)

class MainPower(models.Model):
    Year = models.CharField("年份", max_length=100)  # 數據年份
    Companys = models.CharField("公司别", max_length=100, null=True, blank=True)
    Plants = models.CharField("厂区", max_length=100, null=True, blank=True)
    DepartmentCode = models.CharField("部门代码", max_length=50)
    CHU = models.CharField("处", max_length=50)
    BU = models.CharField("部", max_length=50, null=True, blank=True)
    KE = models.CharField("课", max_length=50, null=True, blank=True)
    Customer = models.CharField("客户别", max_length=50)
    Item = models.CharField("项次", max_length=100)  # 項次
    Positions_Name = models.CharField("职称", max_length=50)  # 職稱
    CodeNoH01 = models.CharField("CodeNoH01", max_length=50)
    CodeNoH02 = models.CharField("CodeNoH02", max_length=50)
    Jan = models.CharField("Jan", max_length=50, null=True, blank=True)
    Feb = models.CharField("Feb", max_length=50, null=True, blank=True)
    Mar = models.CharField("Mar", max_length=50, null=True, blank=True)
    Apr = models.CharField("Apr", max_length=50, null=True, blank=True)
    May = models.CharField("May", max_length=50, null=True, blank=True)
    Jun = models.CharField("Jun", max_length=50, null=True, blank=True)
    Jul = models.CharField("Jul", max_length=50, null=True, blank=True)
    Aug = models.CharField("Aug", max_length=50, null=True, blank=True)
    Sep = models.CharField("Sep", max_length=50, null=True, blank=True)
    Oct = models.CharField("Oct", max_length=50, null=True, blank=True)
    Nov = models.CharField("Nov", max_length=50, null=True, blank=True)
    Dec = models.CharField("Dec", max_length=50, null=True, blank=True)
    class Meta:
        verbose_name = '人力信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{CHU}-{BU}-{KE}-{Customer}-{DepartmentCode}-{Item}'.format(CHU=self.CHU, BU=self.BU,
            KE=self.KE, Customer=self.Customer, DepartmentCode=self.DepartmentCode, Item=self.Item)

class WorkOvertime(models.Model):
    SalaryRange = models.CharField("计薪区间", max_length=20)#計薪區間
    Department_Code = models.CharField("部门代码", max_length=50)
    Department_Des = models.CharField("部门描述", max_length=20)
    GroupNum = models.CharField("集团员工", max_length=50)  # 集團員工
    CNName = models.CharField("中文姓名", max_length=50)  # 姓名
    RegistDate = models.CharField("报道日期", max_length=20)  # 報到日期
    PerNature = models.CharField("人员性质", max_length=20)  # 人員性質
    Classes = models.CharField("班别", max_length=20)  # 班別
    Year = models.CharField("年份", max_length=10)  # 年份
    Mounth = models.CharField("月份", max_length=10)  # 月份
    Peacetime = models.CharField("平时加班", max_length=10)  # 平時加班
    NationalHoliday = models.CharField("国假加班", max_length=10)  # 國假加班
    PeriodHoliday = models.CharField("例假加班", max_length=10)  # 例假加班
    Total = models.CharField("总计", max_length=10)  # Total
    class Meta:
        verbose_name = '加班信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Department_Code}-{GroupNum}-{CNName}-{Year}-{Mounth}'.format(Department_Code=self.Department_Code, GroupNum=self.GroupNum,
            CNName=self.CNName, Year=self.Year, Mounth=self.Mounth,)

class LeaveInfo(models.Model):
    # SalaryRange = models.CharField("SalaryRange", max_length=20)
    Department_Code = models.CharField("部门代码", max_length=50)
    # Department_Des = models.CharField("Department_Des", max_length=20)
    GroupNum = models.CharField("请假人工号", max_length=50)  # 請假人工號
    CNName = models.CharField("请假人姓名", max_length=50)  # 請假人姓名
    Year = models.CharField("年份", max_length=10)  # 年份
    Mounth = models.CharField("月份", max_length=10)  # 月份
    PublicHoliday = models.CharField("公假", max_length=10)  # 公假
    WorkInjury = models.CharField("工伤假", max_length=10)  # 工傷假
    Matters = models.CharField("事假", max_length=10)  # 事假
    MattersContinuation = models.CharField("续事假", max_length=10)  # 續事假
    Sick = models.CharField("病假", max_length=10)  # 病假
    SickContinuation = models.CharField("续病假", max_length=10)  # 續病假
    Marriage = models.CharField("婚假", max_length=10)  # 婚假
    Bereavement = models.CharField("丧假", max_length=10)  # 喪假
    Special = models.CharField("特休假", max_length=10)  # 特休假
    OffDuty = models.CharField("不上班假", max_length=10)  # 不上班假
    Compensatory = models.CharField("补休", max_length=10)  # 補休
    EpidemicPrevention = models.CharField("防疫假", max_length=10)  # 防疫假
    NoScheduling = models.CharField("无排程假", max_length=10)  # 無排程假
    PaternityLeave = models.CharField("陪产假", max_length=10)  # 陪產假
    Absenteeism = models.CharField("矿工", max_length=10)  # 曠工
    Maternity = models.CharField("产假", max_length=10)  # 產假
    PregnancyExamination = models.CharField("产检假", max_length=10)  # 產檢假
    Lactation = models.CharField("哺乳假", max_length=10)  # 哺乳假
    Others = models.CharField("其他", max_length=10)  # 其他
    Total = models.CharField("总计", max_length=10)  # 总時數
    class Meta:
        verbose_name = '请假信息'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Department_Code}-{GroupNum}-{CNName}-{Year}-{Mounth}'.format(Department_Code=self.Department_Code, GroupNum=self.GroupNum,
            CNName=self.CNName, Year=self.Year, Mounth=self.Mounth,)

class PublicAreaM(models.Model):
    Category = models.CharField("Category", max_length=50)
    XX = models.CharField("細項", max_length=50)
    FZR = models.CharField("負責人", max_length=50)
    CHU = models.CharField("處", max_length=50)
    DEPARTMENT = models.CharField("部別", max_length=50, default='')
    MAIL = models.CharField("郵件地址", max_length=50)
    LXFS = models.CharField("聯係方式", max_length=50)