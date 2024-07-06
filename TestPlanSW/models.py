from django.db import models
from app01.models import UserInfo

# Create your models here.
class TestItemSW(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('T89(NB)', 'T89(NB)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        # ('Wave', 'Wave'),
        ('FFRT', 'FFRT'),
        ('Others', 'Others'),
    )
    Choose=(
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('O', 'O'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice, max_length=20, default='C38(NB)')
    Phase = models.CharField('Phase', choices=Phase_choice, max_length=20, default='', )
    ItemNo_d=models.CharField('ItemNo',max_length=50,)
    Item_d=models.CharField('Item',max_length=150,)
    TestItems= models.CharField('TestItems',max_length=1000,blank=True,null=True,default='')
    Category = models.CharField('Category', max_length=250,blank=True,null=True)
    Category2 = models.CharField('Category2', max_length=250,blank=True,null=True)
    Version=models.CharField('Version',max_length=100,blank=True,null=True)
    ReleaseDate=models.CharField('ReleaseDate',max_length=50,blank=True,null=True)
    Owner=models.CharField('Owner',max_length=30,blank=True,null=True)
    Priority=models.CharField('Priority',max_length=10,blank=True,null=True)
    TDMSTotalTime=models.FloatField('TDMSTotalTime',max_length=20,blank=True,null=True)
    BaseTime=models.FloatField('BaseTime',max_length=20,blank=True,null=True)
    TDMSUnattendedTime=models.FloatField('TDMSUnattendedTime',max_length=20,blank=True,null=True)
    BaseAotomationTime1SKU=models.FloatField('BaseAotomationTime1SKU',max_length=10,blank=True,null=True)
    Chramshell= models.CharField('Chramshell', choices=Choose, max_length=10,default='',blank=True,null=True)
    ConvertibaleNBMode=models.CharField('ConvertibaleNBMode', choices=Choose, max_length=10,default='',blank=True,null=True)
    ConvertibaleYogaPadMode=models.CharField('ConvertibaleYogaPadMode', choices=Choose, max_length=10,default='',blank=True,null=True)
    DetachablePadMode=models.CharField('DetachablePadMode', choices=Choose, max_length=10,default='',blank=True,null=True)
    DetachableWDockmode=models.CharField('DetachableWDockmode', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseFVT=models.CharField('PhaseFVT', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseSIT=models.CharField('PhaseSIT', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseFFRT=models.CharField('PhaseFFRT', choices=Choose, max_length=10,default='',blank=True,null=True)
    Coverage=models.CharField('Category',max_length=500,blank=True,null=True)
    class Meta:
        verbose_name = 'TestItemSW'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.TestItems:
            return '{Customer}-{Phase}-{ItemNo_d}-{TestItems}'.format(Customer=self.Customer,Phase=self.Phase,ItemNo_d=self.ItemNo_d,TestItems=self.TestItems)
        else:
            return '{Customer}-{Phase}-{ItemNo_d}'.format(Customer=self.Customer, Phase=self.Phase,ItemNo_d=self.ItemNo_d)
class TestProjectSW(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Phase_choice =(
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('SIT2', 'SIT2'),
        ('GSKU', 'GSKU'),
        ('Downgrade', 'Downgrade'),
        ('Wave', 'Wave'),
        ('Wave2', 'Wave2'),
        ('Wave3', 'Wave3'),
        ('Wave4', 'Wave4'),
        ('Wave5', 'Wave5'),
        ('OOC', 'OOC'),
        ('OOC2', 'OOC2'),
        ('OOC3', 'OOC3'),
        ('OOC4', 'OOC4'),
        ('OOC5', 'OOC5'),
        ('OOC6', 'OOC6'),
        ('FFRT', 'FFRT'),
        ('FFRT2', 'FFRT2'),
        ('FFRT3', 'FFRT3'),
        ('FFRT4', 'FFRT4'),
        ('FFRT5', 'FFRT5'),
        ('FFRT6', 'FFRT6'),
        ('SIT_U9', 'SIT_U9'),
        ('U9_FFRT', 'U9_FFRT'),
        ('U9_FFRT2', 'U9_FFRT2'),
        ('U9_FFRT3', 'U9_FFRT3'),
        ('GSKU_FFRT', 'GSKU_FFRT'),
        ('GSKU_FFRT2', 'GSKU_FFRT2'),
        ('GSKU_FFRT3', 'GSKU_FFRT3'),
        ('DG_FFRT', 'DG_FFRT'),
        ('DG_FFRT2', 'DG_FFRT2'),
        ('DG_FFRT3', 'DG_FFRT3'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice,max_length=20)
    Project = models.CharField('Project', max_length=20)
    Phase = models.CharField('Phase', choices=Phase_choice, max_length=20)
    ScheduleBegin = models.DateField('ScheduleBegin', blank=True, null=True, )
    ScheduleEnd = models.DateField('ScheduleEnd', blank=True, null=True, )
    Full_Function_Duration = models.FloatField('Full_Function_Duration', blank=True, null=True, default=0.00)
    Gerber = models.DateField('Gerber', blank=True, null=True, )
    Owner = models.ManyToManyField("app01.UserInfo")
    SKU1 = models.CharField('SKU1', max_length=200,blank=True,null=True,default='')
    SKU2 = models.CharField('SKU2',  max_length=200, blank=True, null=True,default='')
    SKU3 = models.CharField('SKU3',  max_length=200, blank=True, null=True,default='')
    SKU4 = models.CharField('SKU4',  max_length=200, blank=True, null=True,default='')
    SKU5 = models.CharField('SKU5',  max_length=200, blank=True, null=True,default='')
    SKU6 = models.CharField('SKU6',  max_length=200, blank=True, null=True,default='')
    SKU7 = models.CharField('SKU7',  max_length=200, blank=True, null=True,default='')
    SKU8 = models.CharField('SKU8',  max_length=200, blank=True, null=True,default='')
    SKU9 = models.CharField('SKU9',  max_length=200, blank=True, null=True,default='')
    SKU10 = models.CharField('SKU10',  max_length=200, blank=True, null=True,default='')
    SKU11 = models.CharField('SKU11',  max_length=200, blank=True, null=True,default='')
    SKU12 = models.CharField('SKU12',  max_length=200, blank=True, null=True,default='')
    SKU13 = models.CharField('SKU13',  max_length=200, blank=True, null=True, default='')
    SKU14 = models.CharField('SKU14',  max_length=200, blank=True, null=True, default='')
    SKU15 = models.CharField('SKU15',  max_length=200, blank=True, null=True, default='')
    SKU16 = models.CharField('SKU16',  max_length=200, blank=True, null=True, default='')
    SKU17 = models.CharField('SKU17',  max_length=200, blank=True, null=True, default='')
    SKU18 = models.CharField('SKU18',  max_length=200, blank=True, null=True, default='')
    SKU19 = models.CharField('SKU19',  max_length=200, blank=True, null=True, default='')
    SKU20 = models.CharField('SKU20',  max_length=200, blank=True, null=True, default='')
    SKU21 = models.CharField('SKU21', max_length=200, blank=True, null=True, default='')
    SKU22 = models.CharField('SKU22', max_length=200, blank=True, null=True, default='')
    SKU23 = models.CharField('SKU23', max_length=200, blank=True, null=True, default='')
    SKU24 = models.CharField('SKU24', max_length=200, blank=True, null=True, default='')
    SKU25 = models.CharField('SKU25', max_length=200, blank=True, null=True, default='')
    SKU26 = models.CharField('SKU26', max_length=200, blank=True, null=True, default='')
    SKU27 = models.CharField('SKU27', max_length=200, blank=True, null=True, default='')
    SKU28 = models.CharField('SKU28', max_length=200, blank=True, null=True, default='')
    SKU29 = models.CharField('SKU29', max_length=200, blank=True, null=True, default='')
    SKU30 = models.CharField('SKU30', max_length=200, blank=True, null=True, default='')
    SKU31 = models.CharField('SKU31', max_length=200, blank=True, null=True, default='')
    SKU32 = models.CharField('SKU32', max_length=200, blank=True, null=True, default='')
    SKU33 = models.CharField('SKU33', max_length=200, blank=True, null=True, default='')
    SKU34 = models.CharField('SKU34', max_length=200, blank=True, null=True, default='')
    SKU35 = models.CharField('SKU35', max_length=200, blank=True, null=True, default='')
    SKU36 = models.CharField('SKU36', max_length=200, blank=True, null=True, default='')
    SKU37 = models.CharField('SKU37', max_length=200, blank=True, null=True, default='')
    SKU38 = models.CharField('SKU38', max_length=200, blank=True, null=True, default='')
    SKU39 = models.CharField('SKU39', max_length=200, blank=True, null=True, default='')
    SKU40 = models.CharField('SKU40', max_length=200, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'TestProjectSW'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Project}-{Phase}'.format(Project=self.Project,Phase=self.Phase)
class TestPlanSW(models.Model):
    ChoiceFeatureSupport=(
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
    )
    ChoiceYN = (
        ('', ''),
        ('Y', 'Y'),
        ('N', 'N'),
    )
    SKUResult = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('A', 'A'),
        ('L', 'L'),
        ('S', 'S'),
    )

    #测试当下的版本信息
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('SIT2', 'SIT2'),
        ('GSKU', 'GSKU'),
        ('Downgrade', 'Downgrade'),
        ('Wave', 'Wave'),
        ('Wave2', 'Wave2'),
        ('Wave3', 'Wave3'),
        ('Wave4', 'Wave4'),
        ('Wave5', 'Wave5'),
        ('OOC', 'OOC'),
        ('OOC2', 'OOC2'),
        ('OOC3', 'OOC3'),
        ('OOC4', 'OOC4'),
        ('OOC5', 'OOC5'),
        ('OOC6', 'OOC6'),
        ('FFRT', 'FFRT'),
        ('FFRT2', 'FFRT2'),
        ('FFRT3', 'FFRT3'),
        ('FFRT4', 'FFRT4'),
        ('FFRT5', 'FFRT5'),
        ('FFRT6', 'FFRT6'),
        ('SIT_U9', 'SIT_U9'),
        ('U9_FFRT', 'U9_FFRT'),
        ('U9_FFRT2', 'U9_FFRT2'),
        ('U9_FFRT3', 'U9_FFRT3'),
        ('GSKU_FFRT', 'GSKU_FFRT'),
        ('GSKU_FFRT2', 'GSKU_FFRT2'),
        ('GSKU_FFRT3', 'GSKU_FFRT3'),
        ('DG_FFRT', 'DG_FFRT'),
        ('DG_FFRT2', 'DG_FFRT2'),
        ('DG_FFRT3', 'DG_FFRT3'),
        ('Others', 'Others'),
    )
    Choose = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('O', 'O'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice, max_length=20, default='C38(NB)')
    Phase = models.CharField('Phase', choices=Phase_choice, max_length=20, default='', )
    ItemNo_d = models.CharField('ItemNo', max_length=50,  blank=True, null=True)
    Item_d = models.CharField('Item', max_length=150,  blank=True, null=True)
    TestItems = models.CharField('TestItems', max_length=1000, blank=True, null=True, default='')
    Category = models.CharField('Category', max_length=250, blank=True, null=True)
    Category2 = models.CharField('Category2', max_length=250, blank=True, null=True)
    Version = models.CharField('Version', max_length=100, blank=True, null=True)
    ReleaseDate = models.CharField('ReleaseDate', max_length=50, blank=True, null=True)
    Owner = models.CharField('Owner', max_length=30, blank=True, null=True)
    Priority = models.CharField('Priority', max_length=10, blank=True, null=True)
    TDMSTotalTime = models.FloatField('TDMSTotalTime', max_length=20, blank=True, null=True)
    BaseTime = models.FloatField('BaseTime', max_length=20, blank=True, null=True)
    TDMSUnattendedTime = models.FloatField('TDMSUnattendedTime', max_length=20, blank=True, null=True)
    BaseAotomationTime1SKU = models.FloatField('BaseAotomationTime1SKU', max_length=10, blank=True, null=True)
    Chramshell = models.CharField('Chramshell', choices=Choose, max_length=10, default='', blank=True, null=True)
    ConvertibaleNBMode = models.CharField('ConvertibaleNBMode', choices=Choose, max_length=10, default='', blank=True,
                                          null=True)
    ConvertibaleYogaPadMode = models.CharField('ConvertibaleYogaPadMode', choices=Choose, max_length=10, default='',
                                               blank=True, null=True)
    DetachablePadMode = models.CharField('DetachablePadMode', choices=Choose, max_length=10, default='', blank=True,
                                         null=True)
    DetachableWDockmode = models.CharField('DetachableWDockmode', choices=Choose, max_length=10, default='', blank=True,
                                           null=True)
    PhaseFVT = models.CharField('PhaseFVT', choices=Choose, max_length=10, default='', blank=True, null=True)
    PhaseSIT = models.CharField('PhaseSIT', choices=Choose, max_length=10, default='', blank=True, null=True)
    PhaseFFRT = models.CharField('PhaseFFRT', choices=Choose, max_length=10, default='', blank=True, null=True)
    Coverage = models.CharField('Coverage', max_length=500, blank=True, null=True)

    Items=models.ForeignKey(TestItemSW,on_delete=True, blank=True, null=True)
    # RetestItems = models.ForeignKey('RetestItemSW', on_delete=True)
    Projectinfo=models.ForeignKey(TestProjectSW,on_delete=True)
    FeatureSupport=models.CharField('FeatureSupport', choices=ChoiceYN, max_length=5, blank=True, null=True, default='' )
    BaseTimeSupport=models.FloatField('BaseTimeSupport', max_length=20, blank=True, null=True)
    TE=models.CharField('TE',max_length=30, blank=True, null=True, default='')
    Schedule=models.CharField('Schedule',max_length=40, blank=True, null=True, default='')
    ProjectTestSKUfollowMatrix=models.FloatField('ProjectTestSKUfollowMatrix', max_length=10, blank=True, null=True,)
    TimewConfigFollowmatrix=models.FloatField('TimewConfigFollowmatrix', max_length=20, blank=True, null=True,)
    ConfigAutomationItem=models.CharField('ConfigAutomationItem',choices=ChoiceYN,max_length=5, blank=True, null=True, default='')
    ConfigAutomationTime=models.FloatField('ConfigAutomationTime',max_length=20, blank=True, null=True, )
    ConfigLeverageItem=models.CharField('ConfigLeverageItem',choices=ChoiceYN,max_length=5, blank=True, null=True, default='')
    ConfigLeverageTime = models.FloatField('ConfigLeverageTime', max_length=20, blank=True, null=True, )
    CommentsLeverage=models.CharField('Comment',max_length=1500,blank=True,null=True,default='')
    ConfigSmartItem=models.CharField('ConfigSmartItem',choices=ChoiceYN,max_length=5, blank=True, null=True, default='')
    ConfigSmartItemPer=models.FloatField('ConfigSmartItemPer', max_length=10, blank=True, null=True,)
    ConfigSmartTime=models.FloatField('ConfigSmartTime', max_length=20, blank=True, null=True, )
    CommentsSmart=models.CharField('Comment',max_length=1500,blank=True,null=True,default='')
    ProjectTestSKUOptimize=models.FloatField('ProjectTestSKUOptimize', max_length=20, blank=True, null=True, )
    AttendTimeOptimize=models.FloatField('AttendTimeOptimize', max_length=20, blank=True, null=True, )
    SKU1 = models.CharField('SKU1', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU2 = models.CharField('SKU2', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU3 = models.CharField('SKU3', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU4 = models.CharField('SKU4', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU5 = models.CharField('SKU5', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU6 = models.CharField('SKU6', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU7 = models.CharField('SKU7', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU8 = models.CharField('SKU8', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU9 = models.CharField('SKU9', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU10 = models.CharField('SKU10', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU11 = models.CharField('SKU11', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU12 = models.CharField('SKU12', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU13 = models.CharField('SKU13', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU14 = models.CharField('SKU14', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU15 = models.CharField('SKU15', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU16 = models.CharField('SKU16', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU17 = models.CharField('SKU17', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU18 = models.CharField('SKU18', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU19 = models.CharField('SKU19', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU20 = models.CharField('SKU20', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU21 = models.CharField('SKU21', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU22 = models.CharField('SKU22', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU23 = models.CharField('SKU23', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU24 = models.CharField('SKU24', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU25 = models.CharField('SKU25', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU26 = models.CharField('SKU26', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU27 = models.CharField('SKU27', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU28 = models.CharField('SKU28', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU29 = models.CharField('SKU29', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU30 = models.CharField('SKU30', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU31 = models.CharField('SKU31', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU32 = models.CharField('SKU32', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU33 = models.CharField('SKU33', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU34 = models.CharField('SKU34', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU35 = models.CharField('SKU35', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU36 = models.CharField('SKU36', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU37 = models.CharField('SKU37', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU38 = models.CharField('SKU38', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU39 = models.CharField('SKU39', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU40 = models.CharField('SKU40', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    ConfigRetestCycle=models.FloatField('ConfigRetestCycle', max_length=20, blank=True, null=True,)
    ConfigRetestSKU=models.FloatField('ConfigRetestSKU', max_length=20, blank=True, null=True,)
    ConfigRetestTime=models.FloatField('ConfigRetestTime', max_length=20, blank=True, null=True,)
    editor = models.CharField('editor',max_length=100, blank=True, null=True, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'TestPlanSW'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Project}--{Item}'.format(Project=self.Projectinfo,Item=self.Items)

class RetestItemSW(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('SIT2', 'SIT2'),
        ('GSKU', 'GSKU'),
        ('Downgrade', 'Downgrade'),
        ('Wave', 'Wave'),
        ('Wave2', 'Wave2'),
        ('Wave3', 'Wave3'),
        ('Wave4', 'Wave4'),
        ('Wave5', 'Wave5'),
        ('OOC', 'OOC'),
        ('OOC2', 'OOC2'),
        ('OOC3', 'OOC3'),
        ('OOC4', 'OOC4'),
        ('OOC5', 'OOC5'),
        ('OOC6', 'OOC6'),
        ('FFRT', 'FFRT'),
        ('FFRT2', 'FFRT2'),
        ('FFRT3', 'FFRT3'),
        ('FFRT4', 'FFRT4'),
        ('FFRT5', 'FFRT5'),
        ('FFRT6', 'FFRT6'),
        ('SIT_U9', 'SIT_U9'),
        ('U9_FFRT', 'U9_FFRT'),
        ('U9_FFRT2', 'U9_FFRT2'),
        ('U9_FFRT3', 'U9_FFRT3'),
        ('GSKU_FFRT', 'GSKU_FFRT'),
        ('GSKU_FFRT2', 'GSKU_FFRT2'),
        ('GSKU_FFRT3', 'GSKU_FFRT3'),
        ('DG_FFRT', 'DG_FFRT'),
        ('DG_FFRT2', 'DG_FFRT2'),
        ('DG_FFRT3', 'DG_FFRT3'),
        ('Others', 'Others'),
    )
    Choose=(
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('O', 'O'),
    )
    Customer = models.CharField('Customer_R', choices=Customer_choice, max_length=20, default='C38(NB)')
    Phase = models.CharField('Phase_R', choices=Phase_choice, max_length=20, default='', )
    Project=models.CharField('Project_R',max_length=20, )
    ItemNo_d=models.CharField('ItemNo_d_R',max_length=50,)
    Item_d=models.CharField('Item_d_R',max_length=150,)
    TestItems= models.CharField('TestItems_R',max_length=1000,blank=True,null=True)
    Category = models.CharField('Category_R', max_length=250,blank=True,null=True)
    Category2 = models.CharField('Category2_R', max_length=250,blank=True,null=True)
    Version=models.CharField('Version_R',max_length=100,blank=True,null=True)
    ReleaseDate=models.CharField('ReleaseDate_R',max_length=50,blank=True,null=True)
    Owner=models.CharField('Owner_R',max_length=30,blank=True,null=True)
    Priority=models.CharField('Priority_R',max_length=10,blank=True,null=True)
    TDMSTotalTime=models.FloatField('TDMSTotalTime_R',max_length=20,blank=True,null=True)
    BaseTime=models.FloatField('BaseTime_R',max_length=20,blank=True,null=True)
    TDMSUnattendedTime=models.FloatField('TDMSUnattendedTime_R',max_length=20,blank=True,null=True)
    BaseAotomationTime1SKU=models.FloatField('BaseAotomationTime1SKU_R',max_length=10,blank=True,null=True)
    Chramshell= models.CharField('Chramshell_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    ConvertibaleNBMode=models.CharField('ConvertibaleNBMode_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    ConvertibaleYogaPadMode=models.CharField('ConvertibaleYogaPadMode_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    DetachablePadMode=models.CharField('DetachablePadMode_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    DetachableWDockmode=models.CharField('DetachableWDockmode_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseFVT=models.CharField('PhaseFVT_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseSIT=models.CharField('PhaseSIT_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    PhaseFFRT=models.CharField('PhaseFFRT_R', choices=Choose, max_length=10,default='',blank=True,null=True)
    Coverage=models.CharField('Category_R',max_length=500,blank=True,null=True)
    ChoiceFeatureSupport = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
    )
    ChoiceYN = (
        ('', ''),
        ('Y', 'Y'),
        ('N', 'N'),
    )
    SKUResult = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('A', 'A'),
        ('L', 'L'),
        ('S', 'S'),
    )
    # RetestItems = models.ForeignKey('RetestItemSW', on_delete=True)
    Projectinfo = models.ForeignKey('TestProjectSW', on_delete=True)
    FeatureSupport = models.CharField('FeatureSupport_R', choices=ChoiceFeatureSupport, max_length=5, blank=True,
                                      null=True, default='')
    BaseTimeSupport = models.FloatField('BaseTimeSupport_R', max_length=20, blank=True, null=True)
    TE = models.CharField('TE_R', max_length=30, blank=True, null=True, default='')
    Schedule = models.CharField('Schedule_R', max_length=40, blank=True, null=True, default='')
    ProjectTestSKUfollowMatrix = models.FloatField('ProjectTestSKUfollowMatrix_R', max_length=10, blank=True, null=True)
    TimewConfigFollowmatrix = models.FloatField('TimewConfigFollowmatrix_R', max_length=20, blank=True, null=True)
    ConfigAutomationItem = models.CharField('ConfigAutomationItem_R', choices=ChoiceYN, max_length=5, blank=True,
                                            null=True, default='')
    ConfigAutomationTime = models.FloatField('ConfigAutomationTime_R', max_length=20, blank=True, null=True)
    ConfigLeverageItem = models.CharField('ConfigLeverageItem_R', choices=ChoiceYN, max_length=5, blank=True, null=True,
                                          default='')
    ConfigLeverageTime = models.FloatField('ConfigLeverageTime_R', max_length=20, blank=True, null=True)
    CommentsLeverage = models.CharField('Comment_R', max_length=1500, blank=True, null=True, default='')
    ConfigSmartItem = models.CharField('ConfigSmartItem_R', choices=ChoiceYN, max_length=5, blank=True, null=True,
                                       default='')
    ConfigSmartItemPer = models.FloatField('ConfigSmartItemPer_R', max_length=10, blank=True, null=True)
    ConfigSmartTime = models.FloatField('ConfigSmartTime_R', max_length=20, blank=True, null=True)
    CommentsSmart = models.CharField('Comment_R', max_length=1500, blank=True, null=True, default='')
    ProjectTestSKUOptimize = models.FloatField('ProjectTestSKUOptimize_R', max_length=20, blank=True, null=True)
    AttendTimeOptimize = models.FloatField('AttendTimeOptimize_R', max_length=20, blank=True, null=True)
    SKU1 = models.CharField('SKU1_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU2 = models.CharField('SKU2_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU3 = models.CharField('SKU3_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU4 = models.CharField('SKU4_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU5 = models.CharField('SKU5_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU6 = models.CharField('SKU6_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU7 = models.CharField('SKU7_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU8 = models.CharField('SKU8_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU9 = models.CharField('SKU9_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU10 = models.CharField('SKU10_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU11 = models.CharField('SKU11_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU12 = models.CharField('SKU12_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU13 = models.CharField('SKU13_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU14 = models.CharField('SKU14_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU15 = models.CharField('SKU15_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU16 = models.CharField('SKU16_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU17 = models.CharField('SKU17_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU18 = models.CharField('SKU18_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU19 = models.CharField('SKU19_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU20 = models.CharField('SKU20_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU21 = models.CharField('SKU21_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU22 = models.CharField('SKU22_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU23 = models.CharField('SKU23_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU24 = models.CharField('SKU24_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU25 = models.CharField('SKU25_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU26 = models.CharField('SKU26_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU27 = models.CharField('SKU27_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU28 = models.CharField('SKU28_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU29 = models.CharField('SKU29_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU30 = models.CharField('SKU30_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU31 = models.CharField('SKU31_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU32 = models.CharField('SKU32_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU33 = models.CharField('SKU33_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU34 = models.CharField('SKU34_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU35 = models.CharField('SKU35_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU36 = models.CharField('SKU36_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU37 = models.CharField('SKU37_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU38 = models.CharField('SKU38_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU39 = models.CharField('SKU39_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU40 = models.CharField('SKU40_R', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    ConfigRetestCycle = models.FloatField('ConfigRetestCycle_R', max_length=20, blank=True, null=True)
    ConfigRetestSKU = models.FloatField('ConfigRetestSKU_R', max_length=20, blank=True, null=True)
    ConfigRetestTime = models.FloatField('ConfigRetestTime_R', max_length=20, blank=True, null=True)
    editor = models.CharField('editor_R', max_length=100, blank=True, null=True, default='')
    edit_time = models.CharField('edit_time_R', max_length=26, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'RetestItemSW'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}-{Phase}-{ItemNo_d}-{TestItems}'.format(Customer=self.Customer,Phase=self.Phase,ItemNo_d=self.ItemNo_d,TestItems=self.TestItems)
class FFRTByRD(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer_R', choices=Customer_choice, max_length=20, default='C38(NB)')
    Project = models.CharField('Project_R', max_length=20, )
    EC = models.IntegerField("EC",  blank=True, null=True)
    RF = models.IntegerField("RF",  blank=True, null=True)
    EMI = models.IntegerField("EMI", blank=True, null=True)
    ESD = models.IntegerField("ESD", blank=True, null=True)
    HW = models.IntegerField("HW", blank=True, null=True)
    SW = models.IntegerField("SW",  blank=True, null=True)
    SA = models.IntegerField("SA",  blank=True, null=True)
    SIT = models.IntegerField("SIT", blank=True, null=True)
    Thermal = models.IntegerField("Themal", blank=True, null=True)
    Power = models.IntegerField("Power", blank=True, null=True)
    SED = models.IntegerField("SED", blank=True, null=True)
    class Meta:
        verbose_name = 'FFRTByRD'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}-{Project}'.format(Customer=self.Customer,Project=self.Project)

class TestProjectSWAIO(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Phase_choice =(
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(SDV)', 'B(SDV)'),
        ('C(SIT)', 'C(SIT)'),
        ('Wave2', 'Wave2'),
        ('Wave3', 'Wave3'),
        ('EELP+', 'EELP+'),
        ('OOC', 'OOC'),
        ('OOC2', 'OOC2'),
        ('OOC3', 'OOC3'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice,max_length=20)
    Project = models.CharField('Project', max_length=20)
    Phase = models.CharField('Phase', choices=Phase_choice, max_length=20)
    ScheduleBegin = models.DateField('ScheduleBegin', blank=True, null=True, )
    ScheduleEnd = models.DateField('ScheduleEnd', blank=True, null=True, )
    Full_Function_Duration = models.FloatField('Full_Function_Duration', blank=True, null=True, default=0.00)
    Gerber = models.DateField('Gerber', blank=True, null=True, )
    Owner = models.ManyToManyField("app01.UserInfo")
    SKU1 = models.CharField('SKU1', max_length=200,blank=True,null=True,default='')
    SKU2 = models.CharField('SKU2',  max_length=200, blank=True, null=True,default='')
    SKU3 = models.CharField('SKU3',  max_length=200, blank=True, null=True,default='')
    SKU4 = models.CharField('SKU4',  max_length=200, blank=True, null=True,default='')
    SKU5 = models.CharField('SKU5',  max_length=200, blank=True, null=True,default='')
    SKU6 = models.CharField('SKU6',  max_length=200, blank=True, null=True,default='')
    SKU7 = models.CharField('SKU7',  max_length=200, blank=True, null=True,default='')
    SKU8 = models.CharField('SKU8',  max_length=200, blank=True, null=True,default='')
    SKU9 = models.CharField('SKU9',  max_length=200, blank=True, null=True,default='')
    SKU10 = models.CharField('SKU10',  max_length=200, blank=True, null=True,default='')
    SKU11 = models.CharField('SKU11',  max_length=200, blank=True, null=True,default='')
    SKU12 = models.CharField('SKU12',  max_length=200, blank=True, null=True,default='')
    SKU13 = models.CharField('SKU13',  max_length=200, blank=True, null=True, default='')
    SKU14 = models.CharField('SKU14',  max_length=200, blank=True, null=True, default='')
    SKU15 = models.CharField('SKU15',  max_length=200, blank=True, null=True, default='')
    SKU16 = models.CharField('SKU16',  max_length=200, blank=True, null=True, default='')
    SKU17 = models.CharField('SKU17',  max_length=200, blank=True, null=True, default='')
    SKU18 = models.CharField('SKU18',  max_length=200, blank=True, null=True, default='')
    SKU19 = models.CharField('SKU19',  max_length=200, blank=True, null=True, default='')
    SKU20 = models.CharField('SKU20',  max_length=200, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'TestProjectSWAIO'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Project}-{Phase}'.format(Project=self.Project,Phase=self.Phase)
class TestPlanSWAIO(models.Model):
    ChoiceFeatureSupport=(
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
    )
    ChoiceYN = (
        ('', ''),
        ('Y', 'Y'),
        ('N', 'N'),
    )
    SKUResult = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('A', 'A'),
        ('L', 'L'),
        ('S', 'S'),
    )

    #测试当下的版本信息
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(SDV)', 'B(SDV)'),
        ('C(SIT)', 'C(SIT)'),
        ('Wave2', 'Wave2'),
        ('Wave3', 'Wave3'),
        ('EELP+', 'EELP+'),
        ('OOC', 'OOC'),
        ('OOC2', 'OOC2'),
        ('OOC3', 'OOC3'),
        ('Others', 'Others'),
    )
    Choose = (
        ('', ''),
        ('V', 'V'),
        ('X', 'X'),
        ('O', 'O'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice, max_length=20,)
    Phase = models.CharField('Phase', choices=Phase_choice, max_length=20, default='', )
    Category = models.CharField('Category', max_length=50,  blank=True, null=True)
    TestTitle = models.CharField('TestTitle', max_length=500,  blank=True, null=True)
    Subtesttitle = models.CharField('Subtesttitle', max_length=500, blank=True, null=True,)
    TestItem = models.CharField('TestItem', max_length=1000, blank=True, null=True)
    Priority = models.CharField('Priority', max_length=10, blank=True, null=True)
    ReleaseDate = models.CharField('ReleaseDate', max_length=50, blank=True, null=True)
    Owner = models.CharField('Owner', max_length=30, blank=True, null=True)

    AT_Totaltime = models.CharField('AT_Totaltime', max_length=20, blank=True, null=True)
    AT_AttendTime = models.CharField('AT_AttendTime', max_length=20, blank=True, null=True)
    AT_UnattendTime = models.CharField('AT_UnattendTime', max_length=20, blank=True, null=True)
    AT_Automation = models.CharField('AT_Automation', max_length=20, blank=True, null=True)
    DQMS_AttendTime = models.CharField('DQMS_AttendTime', max_length=20,  blank=True, null=True)
    DQMS_UnattendTime = models.CharField('DQMS_UnattendTime', max_length=20,  blank=True, null=True)
    TestUnitsConfig = models.CharField('TestUnitsConfig', max_length=10, blank=True, null=True)
    SmartItem = models.CharField('SmartItem', max_length=10, blank=True, null=True)
    Cusumer = models.CharField('Cusumer', choices=Choose, max_length=10, default='', blank=True,
                                           null=True)
    Commercial = models.CharField('Commercial', choices=Choose, max_length=10, default='', blank=True, null=True)
    SDV = models.CharField('SDV', choices=Choose, max_length=10, default='', blank=True, null=True)
    SIT = models.CharField('SIT', choices=Choose, max_length=10, default='', blank=True, null=True)
    Coverage = models.CharField('Coverage', max_length=500, blank=True, null=True)


    # RetestItems = models.ForeignKey('RetestItemSW', on_delete=True)
    Projectinfo=models.ForeignKey(TestProjectSWAIO,on_delete=True)
    FeatureSupport=models.CharField('FeatureSupport', choices=ChoiceYN, max_length=5, blank=True, null=True, default='' )
    Basetimesupport=models.CharField('Basetimesupport', max_length=20, blank=True, null=True)
    TE = models.CharField('TE', max_length=30, blank=True, null=True, default='')
    Schedule=models.CharField('Schedule',max_length=40, blank=True, null=True, default='')
    Configalltestunits=models.CharField('Configalltestunits', max_length=10, blank=True, null=True,)
    Configalltesttime=models.CharField('Configalltesttime', max_length=20, blank=True, null=True,)
    ConfigAutomationItem=models.CharField('ConfigAutomationItem',max_length=20, blank=True, null=True, default='')
    ConfigAutomationtime=models.CharField('ConfigAutomationtime',max_length=20, blank=True, null=True, )
    ConfigLeverageItem=models.CharField('ConfigLeverageItem', max_length=20, blank=True, null=True, default='')
    ConfigLeveragetime = models.CharField('ConfigLeveragetime', max_length=20, blank=True, null=True, )
    # CommentsLeverage=models.CharField('Comment',max_length=1500,blank=True,null=True,default='')
    ConfigSmartItemper=models.CharField('ConfigSmartItemper', max_length=20, blank=True, null=True, default='')
    ConfigSmarttime=models.CharField('ConfigSmarttime', max_length=20, blank=True, null=True, )
    Comments=models.CharField('Comments',max_length=1500,blank=True,null=True,default='')
    ProjecttestSKUOptimize=models.CharField('ProjecttestSKUOptimize', max_length=20, blank=True, null=True, )
    AttendtimeOptimize=models.CharField('AttendtimeOptimize', max_length=20, blank=True, null=True, )
    SKU1 = models.CharField('SKU1', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU2 = models.CharField('SKU2', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU3 = models.CharField('SKU3', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU4 = models.CharField('SKU4', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU5 = models.CharField('SKU5', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU6 = models.CharField('SKU6', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU7 = models.CharField('SKU7', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU8 = models.CharField('SKU8', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU9 = models.CharField('SKU9', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU10 = models.CharField('SKU10', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU11 = models.CharField('SKU11', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU12 = models.CharField('SKU12', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU13 = models.CharField('SKU13', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU14 = models.CharField('SKU14', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU15 = models.CharField('SKU15', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU16 = models.CharField('SKU16', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU17 = models.CharField('SKU17', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU18 = models.CharField('SKU18', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU19 = models.CharField('SKU19', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    SKU20 = models.CharField('SKU20', choices=SKUResult, max_length=200, blank=True, null=True, default='')
    ConfigRetestCycle=models.CharField('ConfigRetestCycle', max_length=20, blank=True, null=True,)
    ConfigRetestSKU=models.CharField('ConfigRetestSKU', max_length=20, blank=True, null=True,)
    ConfigRetesttime=models.CharField('ConfigRetesttime', max_length=20, blank=True, null=True,)
    editor = models.CharField('editor',max_length=100, blank=True, null=True, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, null=True, default='')
    class Meta:
        verbose_name = 'TestPlanSWAIO'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Project}--{TestTitle}'.format(Project=self.Projectinfo,TestTitle=self.TestTitle)