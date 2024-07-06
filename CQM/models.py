from django.db import models
from DjangoUeditor.models import UEditorField
from app01.models import UserInfo

class CQMProject(models.Model):
    Customer_choice=(
        # ('Select Customer', 'Select Customer'),
        ('',''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('T89(NB)', 'T89(NB)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    # Phase_choice =(
    #     # ('Select Phase', 'Select Phase'),
    #     ('', ''),
    #     ('NPI', 'NPI'),
    #     ('OS refresh', 'OS refresh'),
    #     ('OOC', 'OOC'),
    #     ('INV', 'INV'),
    # )
    Customer=models.CharField('Customer',choices=Customer_choice,max_length=20)
    Project=models.CharField('Project',max_length=20,unique=True)
    # Phase =models.CharField('Phase',choices=Phase_choice,max_length=20)
    Owner=models.ManyToManyField("app01.UserInfo")
    class Meta:
        verbose_name = 'CQMProject'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{Customer}--{Project}'.format(Customer=self.Customer, Project=self.Project)

class CQM(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    # Phase_list = (
    #     ('', ''),
    #     ('SIT', 'SIT'),
    #     ('FVT', 'FVT'),
    #     ('OOC', 'OOC'),
    #     ('INV', 'INV'),
    # )
    Testresult_list = (
        ('', ''),
        ('Qd', 'Qd'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('T', 'T'),
        ('F', 'F'),
        ('DisQ', 'DisQ'),
        ('Drpd', 'Drpd'),
        ('Not Build', 'Not Build')
    )
    Projectinfo = models.ForeignKey("CQMProject", on_delete=True)
    Customer = models.CharField('Customer', choices=Customer_list, max_length=100)
    Project = models.CharField('Project', max_length=100)
    Phase = models.CharField('Phase',  max_length=100)
    Material_Group = models.CharField('Material_Group',max_length=100, blank=True, null=True)
    Keyparts = models.CharField('Keyparts',max_length=1000)
    Character = models.CharField('Character',max_length=100)
    PID = models.CharField('PID',max_length=100, blank=True, null=True)
    VID = models.CharField('VID',max_length=100, blank=True, null=True)
    HW = models.CharField('HW',max_length=100, blank=True, null=True)
    FW = models.CharField('FW',max_length=100, blank=True, null=True)
    Supplier = models.CharField('Supplier',max_length=100, blank=True, null=True)
    R1_PN_Description = models.CharField('R1_PN_Description',max_length=500, blank=True, null=True)
    Compal_R1_PN = models.CharField('Compal_R1_PN',max_length=100, blank=True, null=True)
    Compal_R3_PN = models.CharField('Compal_R3_PN',max_length=100, blank=True, null=True)
    R1S = models.CharField('R1S', max_length=100, blank=True, null=True)
    Reliability = models.CharField('Reliability', choices=Testresult_list,  max_length=100, blank=True, null=True)
    Compatibility = models.CharField('Compatibility', choices=Testresult_list,  max_length=100, blank=True, null=True)
    Testresult = models.CharField('Testresult', choices=Testresult_list,  max_length=100, blank=True, null=True)
    ESD = models.CharField('ESD',max_length=100, blank=True, null=True)
    EMI = models.CharField('EMI',max_length=100, blank=True, null=True)
    RF = models.CharField('RF',max_length=100, blank=True, null=True)
    RD1 = models.CharField('RD1', max_length=100, blank=True, null=True)
    RD2 = models.CharField('RD2', max_length=100, blank=True, null=True)
    RD3 = models.CharField('RD3', max_length=100, blank=True, null=True)
    RD4 = models.CharField('RD4', max_length=100, blank=True, null=True)
    RD5 = models.CharField('RD5', max_length=100, blank=True, null=True)
    RD6 = models.CharField('RD6', max_length=100, blank=True, null=True)
    PMsummary = models.CharField('PMsummary',max_length=100, blank=True, null=True)
    Controlrun = models.CharField('Controlrun',max_length=100, blank=True, null=True)
    Comments = models.CharField('Comments',max_length=10000, blank=True, null=True)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'CQM'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}--{Project}--{Phase}--{Material_Group}--{Character}--{PID}--{VID}--{HW}--{FW}--{Compal_R1_PN}--{Compal_R3_PN}'.format(Customer=self.Customer, Project=self.Project, Phase=self.Phase,
    Material_Group=self.Material_Group, Character=self.Character, PID=self.PID, VID=self.VID, HW=self.HW, FW=self.FW, Compal_R1_PN=self.Compal_R1_PN, Compal_R3_PN=self.Compal_R3_PN)

class CQM_history(models.Model):
    Changeid = models.ForeignKey("CQM", on_delete=True)
    Changecontent = models.CharField('Changecontent',  max_length=10000)
    Changeto = models.CharField('Changecontent',  max_length=10000)
    Changeowner = models.CharField('Changeowner', max_length=100)
    Change_time = models.CharField('Change_time', max_length=26)
    class Meta:
        verbose_name = 'CQM_history'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name