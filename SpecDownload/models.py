from django.db import models


# Create your models here.
class files_SpecD(models.Model):
    files = models.FileField(upload_to="files_SpecD/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_SpecD)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class SpecDownload(models.Model):
    Customer = models.CharField("Customer", max_length=20)
    Project = models.CharField("Project", max_length=20, default="")
    Category = models.CharField("Category", max_length=20)
    Functionn = models.CharField("Functionn", max_length=50)
    Case_name = models.CharField("Case_name", max_length=1000)
    Version = models.CharField("Version", max_length=20)
    files_Spec = models.ManyToManyField(files_SpecD, related_name='files_SpecD', blank=True, verbose_name='图文件表')
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

class files_SopRom(models.Model):
    files = models.FileField(upload_to="files_SopRom/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_SopRom)
def files_SopRom_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class ManagementSopRoom(models.Model):
    Num = models.CharField("No.", max_length=10)
    Title = models.CharField("Title", max_length=200, default="")
    Description = models.CharField("Description", max_length=1000)
    Version = models.CharField("Version", max_length=20)
    files_Spec = models.ManyToManyField(files_SopRom, related_name='files_SopRom', blank=True, verbose_name='图文件表')
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

class files_SopProcess(models.Model):
    files = models.FileField(upload_to="files_SopProcess/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_SopProcess)
def files_SopProcess_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class ManagementSopProcess(models.Model):
    Num = models.CharField("No.", max_length=10)
    Title = models.CharField("Title", max_length=200, default="")
    Description = models.CharField("Description", max_length=1000)
    Version = models.CharField("Version", max_length=20)
    files_Spec = models.ManyToManyField(files_SopProcess, related_name='files_SopProcess', blank=True, verbose_name='图文件表')
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

class files_SopDevice(models.Model):
    files = models.FileField(upload_to="files_SopDevice/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_SopDevice)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class ManagementSopDevice(models.Model):
    Num = models.CharField("No.", max_length=10)
    Title = models.CharField("Title", max_length=200, default="")
    Description = models.CharField("Description", max_length=1000)
    Version = models.CharField("Version", max_length=20)
    files_Spec = models.ManyToManyField(files_SopDevice, related_name='files_SopDevice', blank=True, verbose_name='图文件表')
    editor = models.CharField('editor', max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)