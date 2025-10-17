from django.db import models
from app01.models import UserInfo
from CQM.models import CQMProject

# Create your models here.

class PICS(models.Model):
    # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
    pic = models.ImageField(upload_to='Adapter/PIC/',verbose_name='图片地址')
    single = models.CharField(max_length=200,null=True, blank=True,verbose_name='图片名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.pic)

    # def __str__(self):
    #     return str(self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=PICS)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.pic.delete(False)


class files(models.Model):
    files = models.FileField(upload_to="Autotool/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')

    def save(self, *args, **kwargs):
        # 处理 single 字段可能为文件对象的情况
        if hasattr(self.single, 'name'):
            # 如果是文件对象，获取文件名
            self.single = self.single.name

        # 自动设置文件类型
        if self.single:
            # 确保 single 是字符串
            if isinstance(self.single, str):
                ext = self.single.split('.')[-1].lower()
            else:
                # 如果不是字符串，尝试转换为字符串
                ext = str(self.single).split('.')[-1].lower()

            if ext in ['jpg', 'jpeg', 'png', 'gif']:
                self.file_type = 'image'
            elif ext in ['mp4', 'avi', 'mov']:
                self.file_type = 'video'
            elif ext in ['pdf']:
                self.file_type = 'pdf'
            elif ext in ['ppt', 'pptx']:
                self.file_type = 'ppt'
            elif ext in ['xls', 'xlsx']:
                self.file_type = 'excel'
            elif ext in ['doc', 'docx']:
                self.file_type = 'word'
            else:
                self.file_type = 'other'
        else:
            self.file_type = 'other'

        super().save(*args, **kwargs)

    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class AutoItems(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('C85', 'C85'),
        ('A39', 'A39'),
        ('T89(NB)', 'T89(NB)'),
        ('Common', 'Common'),
        ('網絡', '網絡'),
    )
    ValueIf_choice = (
        # ('Select Customer', 'Select Customer'),
        # ('', ''),
        ('N-VA', 'N-VA'),
        ('VA', 'VA'),
    )
    Status_choice = (
        # ('Select Customer', 'Select Customer'),
        # ('', ''),
        ('Ready', 'Ready'),
        ('Cancel', 'Cancel'),
        ('Ongoing', 'Ongoing'),
    )
    Number = models.CharField(max_length=64, unique=True, verbose_name='No.')
    Customer = models.CharField(max_length=64, choices=Customer_list, verbose_name='CG')
    ValueIf = models.CharField(max_length=64, choices=ValueIf_choice, verbose_name='VA/N-VA')
    BaseIncome = models.CharField(max_length=64, null=True, blank=True, verbose_name='Base效益')
    CaseID = models.CharField(max_length=64, null=True, blank=True, verbose_name='Case ID')
    CaseName = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Case Name')
    Item = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Item')
    Status = models.CharField(max_length=50, choices=Status_choice, default='', verbose_name='Status')
    Owner = models.CharField(max_length=50, null=True, blank=True, verbose_name='開發者')
    proposer = models.CharField(max_length=50, null=True, blank=True, verbose_name='提案者')
    Import_Date = models.DateField("導入日期", null=True, blank=True, max_length=50)
    Ver = models.CharField(max_length=30, null=True, blank=True, verbose_name='工具版本')
    FunDescription = models.CharField(max_length=1000, null=True, blank=True, verbose_name='功能簡介')
    Comment = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Comment')
    Attachment = models.ManyToManyField(files, related_name='Attachment', blank=True, verbose_name='工具及Sop')
    # Photo = models.ManyToManyField(PICS, related_name='pics', blank=True, verbose_name='图片表')
    class Meta:
        verbose_name = 'AutoItems'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{Number}--{Item}'.format(Number=self.Number, Item=self.Item)

class AutoProject(models.Model):
    Customer_choice=(
        # ('Select Customer', 'Select Customer'),
        ('',''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('T89(NB)', 'T89(NB)'),
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
    Customer=models.CharField('Customer', choices=Customer_choice, max_length=20)
    Project=models.CharField('Project', max_length=20, unique=True)
    Year =models.CharField('SS年份', max_length=20, default="")
    Owner=models.ManyToManyField("app01.UserInfo")
    class Meta:
        verbose_name = 'AutoProject'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{Customer}--{Project}'.format(Customer=self.Customer, Project=self.Project)

class AutoResult(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('C85', 'C85'),
        ('A39', 'A39'),
        ('T89(NB)', 'T89(NB)'),
        ('Common', 'Common'),
        ('網絡', '網絡'),
    )
    ValueIf_choice = (
        # ('Select Customer', 'Select Customer'),
        # ('', ''),
        ('N-VA', 'N-VA'),
        ('VA', 'VA'),
    )
    Status_choice = (
        # ('Select Customer', 'Select Customer'),
        # ('', ''),
        ('V', 'V'),
        ('X', 'X'),
    )
    Number = models.CharField(max_length=64, verbose_name='No.')
    Customer = models.CharField(max_length=64, choices=Customer_list, verbose_name='CG')
    ValueIf = models.CharField(max_length=64, choices=ValueIf_choice, verbose_name='VA/N-VA')
    BaseIncome = models.CharField(max_length=64, null=True, blank=True, verbose_name='Base效益')
    CaseID = models.CharField(max_length=64, null=True, blank=True, verbose_name='Case ID')
    CaseName = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Case Name')
    Item = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Item')
    Status = models.CharField(max_length=50, choices=Status_choice, default='', verbose_name='Status')
    Owner = models.CharField(max_length=50, null=True, blank=True, verbose_name='開發者')
    proposer = models.CharField(max_length=50, null=True, blank=True, verbose_name='提案者')
    Import_Date = models.DateField("導入日期", null=True, blank=True, max_length=50)
    Ver = models.CharField(max_length=30, null=True, blank=True, verbose_name='工具版本')
    FunDescription = models.CharField(max_length=1000, null=True, blank=True, verbose_name='功能簡介')
    Comment = models.CharField(max_length=1000, null=True, blank=True, verbose_name='Comment')
    # Photo = models.ManyToManyField(PICS, related_name='pics', blank=True, verbose_name='图片表')

    AutoItem = models.ForeignKey("AutoItems", null=True, blank=True, on_delete=True)
    Projectinfo = models.ForeignKey("AutoProject", null=True, blank=True, on_delete=True)
    ProjectinfoCQM = models.ForeignKey("CQM.CQMProject", null=True, blank=True, on_delete=True)

    ProjectName = models.CharField('ProjectName', max_length=50, blank=True, null=True)
    Year = models.CharField('SS年份', max_length=20, default="", blank=True, null=True)
    Cycles = models.CharField('Cycles', max_length=10, blank=True, null=True)
    Comments = models.CharField('Comments', max_length=5000, blank=True, null=True)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)