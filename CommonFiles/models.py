from django.db import models
from app01.models import UserInfo
# Create your models here.
class files(models.Model):
    files = models.FileField(upload_to="CommonFiles/", null=True, blank=True, verbose_name="文件内容")
    single = models.CharField(max_length=100, null=True, blank=True, verbose_name='文件名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class Category(models.Model):
    """大类模型"""
    name = models.CharField("大类名称", max_length=50, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """细项模型（依赖大类）"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField("细项名称", max_length=50)

    def __str__(self):
        return self.name

class CommonFiles(models.Model):
    chooseCG = (
        ("", ""),
        ("C38NB", "C38NB"),
        ("C38AIO", "C38AIO"),
        ("T88AIO", "T88AIO"),
        ("T89", "T89"),
        ("Common", "Common"),
    )
    chooseSWHW = (
        ("", ""),
        ("SW", "SW"),
        ("HW", "HW"),
        ("Common", "Common"),
    )
    CG = models.CharField(max_length=10, choices=chooseCG, default="")
    SWHW = models.CharField(max_length=10, choices=chooseSWHW, default="",  null=True, blank=True)
    Category_L1 = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="大类")
    Category_L2 = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="细项",  null=True, blank=True)
    Item = models.CharField('Item', max_length=100)
    Description = models.CharField("Description", max_length=1000)
    Version = models.CharField("Version", max_length=20)
    Attachment = models.ManyToManyField(files, related_name='Attachment', blank=True, verbose_name='文件表')
    Owner = models.ManyToManyField("app01.UserInfo")
    Creator = models.CharField("Creator", max_length=50,default='')
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '知行智库'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{CG}-{SWHW}-{Category_L1}-{Category_L2}-{Item}'.format(CG=self.CG, SWHW=self.SWHW,
                                                          Category_L1=self.Category_L1, Category_L2=self.Category_L2, Item=self.Item)