from django.db import models

from CQM.models import CQMProject
# Create your models here.

class OBIDeviceResult(models.Model):
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
    Phase_list = (
        ('', ''),
        ('SIT', 'SIT'),
        ('FVT', 'FVT'),
        # ('OOC', 'OOC'),
        # ('INV', 'INV'),
    )
    Testresult_list = (
        ('', ''),
        ('Qd', 'Qd'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        # ('T', 'T'),
        # ('F', 'F'),
        # ('DisQ', 'DisQ'),
        # ('Drpd', 'Drpd'),
        # ('No Build', 'No Build')
    )
    # Projectinfo = models.ForeignKey("CQMProject", on_delete=True)
    Customer = models.CharField('Customer', choices=Customer_list, max_length=100)
    Project = models.CharField('Project', max_length=100)
    Platform = models.CharField('Platform', max_length=100)
    Series = models.CharField('Series', max_length=100)
    Category = models.CharField('Category', max_length=100)
    DeviceNo = models.CharField('DeviceNo', max_length=100)
    PN = models.CharField('PN', max_length=100)
    Devicename = models.CharField('Devicename', max_length=1000)
    Testresult = models.CharField('Testresult', choices=Testresult_list, max_length=10)
    FWversion = models.CharField('FWversion', blank=True, null=True, max_length=100)
    Softwareversion = models.CharField('Softwareversion', blank=True, null=True, max_length=100)
    HWIDversion = models.CharField('HWIDversion', blank=True, null=True, max_length=100)
    TestPhase = models.CharField('TestPhase',  max_length=100)
    Comments = models.CharField('Comments',max_length=5000, blank=True, null=True)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'OBIDeviceResult'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}--{Project}--{DeviceNo}'.format(Customer=self.Customer, Project=self.Project, DeviceNo=self.DeviceNo,)

class SeriesInfo(models.Model):

    Series = models.CharField('Series', unique=True, max_length=100)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'SeriesInfo'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

class CategoryInfo(models.Model):

    Category = models.CharField('Category', unique=True, max_length=100)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'CategoryInfo'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
