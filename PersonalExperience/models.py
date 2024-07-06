from django.db import models

# Create your models here.
class PerExperience(models.Model):
    Dalei_choice = (
        ('', ''),
        ('NPI', 'NPI'),
        ('OSR', 'OSR'),
        ('INV', 'INV'),
    )
    Status_choice = (
        ('', ''),
        ('待簽核', '待簽核'),
        ('同意', '同意'),
        ('拒絕', '拒絕'),
    )
    Proposer_Num = models.CharField("申請人工號", max_length=10)
    Proposer_Name = models.CharField("申請人姓名(中)", max_length=20)
    Department_Code = models.CharField("課別", max_length=20)
    Item = models.CharField("职称项次", max_length=20, default='')
    Positions_Name = models.CharField("职称", max_length=20, default='')
    Dalei = models.CharField("大类", max_length=20, choices=Dalei_choice, null=True, blank=True)
    Project = models.CharField("Project", max_length=50)
    SS_Date = models.DateField("SS時間", null=True, blank=True)
    Year = models.CharField("年份", max_length=10, null=True, blank=True)
    Time_Interval = models.CharField("時間區間", max_length=20, null=True, blank=True)
    Phase = models.CharField("Phase", max_length=20, null=True, blank=True)
    Role = models.CharField("Role", max_length=20)
    Function = models.CharField("Function", max_length=20)
    SubFunction_Com = models.CharField("Sub Function-Compatibility", max_length=100, null=True, blank=True)
    KeypartNum = models.CharField("Keypart數量", max_length=100, null=True, blank=True)
    Comments = models.CharField("Comments", max_length=1000, null=True, blank=True)
    Approved_Officer = models.CharField("簽核人員工號", max_length=10)
    Status = models.CharField("狀態", choices=Status_choice, max_length=10)
    EditTime = models.DateField("EditTime", null=True, blank=True)
    class Meta:
        verbose_name = '個人測試履歷'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Proposer_Name}-{Project}'.format(Proposer_Name=self.Proposer_Name, Project=self.Project,)

class OSR_OSinfo(models.Model):
    OSinfo = models.CharField("OSR系統版本", max_length=50)
    Editer = models.CharField("添加人", max_length=10)
    EditTime = models.DateField("EditTime", null=True, blank=True)
    class Meta:
        verbose_name = 'OSR系統版本'
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{OSinfo}'.format(OSinfo=self.OSinfo,)