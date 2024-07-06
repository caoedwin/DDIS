from django.db import models

# Create your models here.
# class Imgs_P(models.Model):
#     # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
#     img = models.ImageField(upload_to='img/test/',verbose_name='图片地址')
#     single = models.CharField(max_length=20,null=True, blank=True,verbose_name='图片名称')
#     def __unicode__(self):  # __str__ on Python 3
#         return (self.id,self.img)

class files_PM(models.Model):
    files = models.FileField(upload_to="files_P/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_PM)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class Package_M(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)
    Phase = models.CharField(max_length=20)
    Degree = models.FloatField()
    Duan = models.FloatField()
    Zhong= models.FloatField()
    Chang = models.FloatField()
    Left = models.FloatField()
    Right = models.FloatField()
    Top = models.FloatField()
    Bottom = models.FloatField()
    Zheng = models.FloatField()
    Fan = models.FloatField()
    Pattern = models.CharField(max_length=30)
    Conclusion = models.CharField(max_length=1000)
    files_P = models.ManyToManyField(files_PM, related_name='files_P', blank=True, verbose_name='图文件表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)

    class Meta:
        verbose_name = 'Package'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name