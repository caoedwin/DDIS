from django.db import models

# Create your models here.

class files_BM(models.Model):
    files = models.FileField(upload_to="files_B/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files_BM)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)


class Bouncing_M(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)
    # Phase = models.CharField(max_length=20)
    A_cover = models.CharField(max_length=50,default='')
    C_cover = models.CharField(max_length=50)
    D_cover = models.CharField(max_length=50)
    HS= models.CharField(max_length=50)
    Torque = models.CharField(max_length=10)
    Push = models.CharField(max_length=10)
    PV_L = models.FloatField()
    PV_R = models.FloatField()
    D_L = models.FloatField()
    D_R = models.FloatField()
    Conclusion = models.CharField(max_length=1000)
    files_B = models.ManyToManyField(files_BM, related_name='files_B', blank=True, verbose_name='图文件表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26)
    class Meta:
        verbose_name = 'Bouncing'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name