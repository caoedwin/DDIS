from django.db import models
from app01.models import UserInfo

# Create your models here.
class TestItemME(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    ItemNo_d=models.CharField('ItemNo',max_length=50,)#unique=True)
    Item_d=models.CharField('Item',max_length=150,)
    Customer = models.CharField('Customer', choices=Customer_choice, max_length=20,default='C38(NB)')
    Phase =models.CharField('Phase',choices=Phase_choice,max_length=20,default='',blank=True,null=True)
    Facility_Name_d=models.CharField('Facility_Name',max_length=50,blank=True,null=True)
    Voltage_d=models.CharField('Voltage',max_length=15,blank=True,null=True)
    Sample_Size_d=models.CharField('Sample_Size',max_length=100,blank=True,null=True)
    TimePunits_Facility_d=models.FloatField('TimePunits_Facility',max_length=10,blank=True,null=True)
    TimePunits_Manual_d = models.FloatField('TimePunits_Manual', max_length=10, blank=True,null=True)
    TimePunits_Program_d = models.FloatField('TimePunits_Program', max_length=10, blank=True,null=True)
    Formula=models.CharField('Formula',max_length=50,blank=True,null=True)
    class Meta:
        verbose_name = 'TestItemME'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ItemNo_d
class TestProjectME(models.Model):
    Customer_choice=(
        # ('Select Customer', 'Select Customer'),
        ('',''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Phase_choice =(
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    Customer=models.CharField('Customer',choices=Customer_choice,max_length=20)
    Project=models.CharField('Project',max_length=20)
    Phase =models.CharField('Phase',choices=Phase_choice,max_length=20)
    ScheduleBegin = models.DateField('ScheduleBegin', blank=True, null=True, )
    Owner=models.ManyToManyField("app01.UserInfo")
    class Meta:
        verbose_name = 'TestProjectME'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Project}--{Phase}'.format(Project=self.Project,Phase=self.Phase)
class TestPlanME(models.Model):
    Items=models.ForeignKey('TestItemME',on_delete=True)
    Projectinfo=models.ForeignKey('TestProjectME',on_delete=True)
    NormalAmount=models.FloatField('NormalAmount',max_length=10,blank=True,null=True)
    NormalFacilityTime=models.FloatField('NormalFacilityTime',max_length=10,blank=True,null=True)
    NormalAttendTime=models.FloatField('NormalAttendTime',max_length=10,blank=True,null=True)
    NormalProgramtime=models.FloatField('NormalProgramtime',max_length=10,blank=True,null=True)
    RegCycles = models.FloatField('RegCycles', max_length=10, blank=True,null=True)
    RegAmount = models.FloatField('RegAmount', max_length=10, blank=True,null=True)
    RegFacilityTime = models.FloatField('RegFacilityTime', max_length=10, blank=True,null=True)
    RegAttendTime = models.FloatField('RegAttendTime', max_length=10, blank=True,null=True)
    RegProgramtime = models.FloatField('RegProgramtime', max_length=10, blank=True,null=True)
    editor = models.CharField(max_length=100,default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True,default='')
    class Meta:
        verbose_name = 'TestPlanME'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Project}---{Item}'.format(Project=self.Projectinfo, Item=self.Items)

class KeypartAIO(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('C38(AIO)-T88', 'C38(AIO)-T88'),
        ('A39', 'A39'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer_R', choices=Customer_choice, max_length=20, default='C38(NB)')
    Project = models.CharField('Project_R', max_length=20, )
    Phase = models.CharField('Phase', max_length=20, )
    IDs = models.CharField("ID",  max_length=20,blank=True, null=True)
    Type = models.CharField("Type", max_length=100, blank=True, null=True)
    SKU = models.CharField("SKU",max_length=20, blank=True, null=True)
    Planar = models.CharField("Planar", max_length=20,blank=True, null=True)
    Panel = models.CharField("Panel", max_length=20,blank=True, null=True)
    Stand = models.CharField("Stand", max_length=20, blank=True, null=True)
    Cable = models.CharField("Cable", max_length=20, blank=True, null=True)
    Connectorsource = models.CharField("Connectorsource",max_length=20,blank=True, null=True)
    SSDHHD = models.CharField("SSDHHD", max_length=20,blank=True, null=True)
    Camera = models.CharField("Camera", max_length=20,blank=True, null=True)
    ODD = models.CharField("ODD", max_length=20,blank=True, null=True)
    Package = models.CharField("Package", max_length=20,blank=True, null=True)
    RegularAttendTime = models.CharField("RegularAttendTime", max_length=20,blank=True, null=True)
    RegressiveAttendTime = models.CharField("RegressiveAttendTime", max_length=20,blank=True, null=True)
    class Meta:
        verbose_name = 'KeypartAIO'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}-{Project}-{Phase}'.format(Customer=self.Customer, Project=self.Project, Phase=self.Phase)

class KeypartC38NB(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('C38(AIO)-T88', 'C38(AIO)-T88'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer_R', choices=Customer_choice, max_length=20, default='C38(NB)')
    Project = models.CharField('Project_R', max_length=20, )
    Phase = models.CharField('Phase', max_length=20, )
    IDs = models.CharField("ID", max_length=20, blank=True, null=True)
    Type = models.CharField("Type", max_length=20, blank=True, null=True)
    SKU = models.CharField("SKU", max_length=20,blank=True, null=True)
    Planar = models.CharField("Planar", max_length=20,blank=True, null=True)
    Panel = models.CharField("Panel", max_length=20,blank=True, null=True)
    Hinge = models.CharField("Hinge", max_length=20, blank=True, null=True)
    Cable = models.CharField("Cable", max_length=20, blank=True, null=True)
    Connectorsource = models.CharField("Connectorsource", max_length=20,blank=True, null=True)
    Keyboard = models.CharField("Keyboard", max_length=20,blank=True, null=True)
    ClickPad = models.CharField("ClickPad", max_length=20,blank=True, null=True)
    SSDHHD = models.CharField("SSDHHD", max_length=20,blank=True, null=True)
    Camera = models.CharField("Camera", max_length=20,blank=True, null=True)
    Rubberfoot = models.CharField("Rubberfoot",max_length=20, blank=True, null=True)
    ODD = models.CharField("ODD", max_length=20,blank=True, null=True)
    TrapDoorRJ45 = models.CharField("TrapDoorRJ45", max_length=20,blank=True, null=True)
    RegularAttendTime = models.CharField("RegularAttendTime", max_length=20,blank=True, null=True)
    RegressiveAttendTime = models.CharField("RegressiveAttendTime", max_length=20,blank=True, null=True)
    class Meta:
        verbose_name = 'KeypartC38NB'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}-{Project}-{Phase}'.format(Customer=self.Customer, Project=self.Project, Phase=self.Phase)