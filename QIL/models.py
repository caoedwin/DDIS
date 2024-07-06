from django.db import models
from LessonProjectME.models import TestProjectLL

# Create your models here.

class files_QIL(models.Model):
    files = models.FileField(upload_to="files_qil/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_QIL)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class QIL_M(models.Model):
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Status_list = (
        ('', ''),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted'),
        ('In Process', 'In Process'),
        ('Lesson Learn', 'Lesson Learn'),
        ('Open', 'Open'),
    )
    Product = models.CharField("Product", max_length=100,)
    Customer = models.CharField("Customer", max_length=20, choices=Customer_list)
    QIL_No = models.CharField("QIL_No", max_length=100, unique=True)
    Issue_Description = models.CharField("Issue_Description", max_length=3000)
    Root_Cause = models.CharField("Root_Cause", max_length=3000)
    Status = models.CharField("Status", max_length=100, choices=Status_list)
    Creator = models.CharField(max_length=100, default='')
    Created_On = models.CharField('Created_On', max_length=26, default='')
    files_QIL = models.ManyToManyField(files_QIL, related_name='files_QIL', blank=True, verbose_name='图文件表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26, blank=True)
		#upload_to参数为指定的文件服务器上保存路径，如果没有该目录django会自动创建
    class Meta:
        verbose_name = 'QIL_M'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Product}---{QIL_No}'.format(Product=self.Product, QIL_No=self.QIL_No)

class QIL_Project(models.Model):
    result_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('N/S', 'N/S'),
        ('N/A', 'N/A'),
    )
    Projectinfo = models.ForeignKey("LessonProjectME.TestProjectLL", on_delete=True)
    QIL = models.ForeignKey("QIL_M", on_delete=True)
    result = models.CharField(max_length=20, choices=result_choice)
    Comment = models.CharField(max_length=1000)
    editor = models.CharField(max_length=100, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, default='')
