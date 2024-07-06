# -*- coding: utf-8 -*-
from django.db import models
import django.utils.timezone as timezone
# from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField
import datetime
# Create your models here.
from django.contrib.auth.models import User

#导入Django自带用户模块

# class UserToken(models.Model):
#     """
#     用户：划分角色
#     """
#     account = models.OneToOneField('UserInfo', on_delete=models.CASCADE,related_name='auth_token',verbose_name="User", primary_key=True)
#     token = models.CharField(max_length=64, blank=True, )
#     # created = models.DateTimeField(auto_now_add=True, null=False)
#
#
#     class Meta:
#         verbose_name = 'UserToken'#不写verbose_name, admin中默认的注册名会加s
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.username

class UserInfo(models.Model):
    """
    用户：划分角色
    """
    DEPARTMENT_CHOICES = {
        (1, '测试部门'),
        (2, '开发部门'),
        (3, 'PM'),
        (4, '其它部门'),
    }
    account = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=32)
    email = models.EmailField()
    department = models.IntegerField(verbose_name='部门', choices=DEPARTMENT_CHOICES, default=1)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_SVPuser = models.BooleanField(default=False)
    # created = models.DateTimeField(auto_now_add=True, null=False)
    # updated = models.DateTimeField(auto_now=True, null=False)
    role = models.ManyToManyField("Role")

    class Meta:
        verbose_name = 'UserInfo'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

class Role(models.Model):
    """
    角色：绑定权限
    """
    name = models.CharField(max_length=32, unique=True)
    perms=models.ManyToManyField('Permission')

    class Meta:
        verbose_name = 'Role'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

class Permission(models.Model):
    """
    权限
    """
    Menu_title=models.CharField(max_length=32, unique=True)
    url = models.CharField(max_length=128, unique=True)
    menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=True)
    class Meta:
        verbose_name = 'Permission'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # 显示带菜单前缀的权限
        return '{menu}---{permission}'.format(menu=self.menu, permission=self.Menu_title)

class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32, unique=True)
    parent = models.ForeignKey("Menu", null=True, blank=True,on_delete=True)
    # 定义菜单间的自引用关系
    # 权限url 在 菜单下；菜单可以有父级菜单；还要支持用户创建菜单，因此需要定义parent字段（parent_id）
    # blank=True 意味着在后台管理中填写可以为空，根菜单没有父级菜单
    class Meta:
        verbose_name = 'Menu'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # 显示层级菜单
        title_list = [self.title]
        p = self.parent
        while p:
            title_list.insert(0, p.title)
            p = p.parent
        return '-'.join(title_list)

class Imgs(models.Model):
    # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
    img = models.ImageField(upload_to='img/test/',verbose_name='图片地址')
    single = models.CharField(max_length=200,null=True, blank=True,verbose_name='图片名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.img)

    # def __str__(self):
    #     return str(self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=Imgs)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)
class files(models.Model):
    files = models.FileField(upload_to="videos/", null=True, blank=True, verbose_name="视频内容")
    single = models.CharField(max_length=200, null=True, blank=True, verbose_name='视频名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=files)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.files.delete(False)

class lesson_learn(models.Model):
    choosecat = (
        ("", ""),
        ("Reliability", "Reliability"),
        ("Compatibility", "Compatibility")
    )
    choosestatus = (
        ("", ""),
        ("active", "active"),
        ("inactive", "inactive")
    )
    Category = models.CharField(max_length=100, choices=choosecat, default="Reliability")
    Object = models.CharField(max_length=100)
    Symptom = models.CharField(max_length=1000)
    Reproduce_Steps = models.CharField('Reproduce_Steps', max_length=2000, default="", blank=True)
    Root_Cause = models.CharField('Root_Cause',max_length=2000)
    # Root_Cause=UEditorField('Root_Cause', width=800, height=150,
    #                         toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                         upload_settings={"imageMaxSize": 1204000, 'videoPathFormat': "videos/"},
    #                         settings={}, command=None#, blank=True
    #                         )
    # Solution = UEditorField('Solution/Action', width=800, height=300,
    #                         toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                         upload_settings={"imageMaxSize": 1204000, 'videoPathFormat': "videos/"},
    #                         settings={}, command=None#, blank=True
    #                         )
    Solution = models.CharField('Solution', max_length=2000)
    Action = models.CharField('Action', max_length=2000,default='', blank=True)
    Status = models.CharField('Status', choices=choosestatus,max_length=20, default='active', blank=True)
    Photo = models.ManyToManyField(Imgs, related_name='imgs', blank=True, verbose_name='图片表')
    video = models.ManyToManyField(files, related_name='video', blank=True, verbose_name='视频表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26, blank=True)
		#upload_to参数为指定的文件服务器上保存路径，如果没有该目录django会自动创建
    class Meta:
        verbose_name = 'lesson_learnME'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Category}-{Object}---{Symptom}'.format(Category=self.Category, Object=self.Object,Symptom=self.Symptom)
class ProjectinfoinDCT(models.Model):
    Customer = models.CharField('Customer', max_length=10, default="",)
    Year=models.CharField('Year', max_length=5)
    ComPrjCode = models.CharField('ComPrjCode', max_length=10)
    PrjEngCode1 = models.CharField('PrjEngCode1', default="", max_length=50, null=True, blank=True)
    PrjEngCode2 = models.CharField('PrjEngCode2', default="", max_length=50, null=True, blank=True)
    ProjectName = models.CharField('ProjectName', max_length=1000, null=True, blank=True)
    Size = models.CharField('Size', max_length=10, null=True, blank=True)
    CPU = models.CharField('CPU', max_length=50, null=True, blank=True)
    Platform = models.CharField('Platform', max_length=500, null=True, blank=True)
    VGA = models.CharField('VGA', max_length=1000, null=True, blank=True)
    OSSupport = models.CharField('OSSupport', max_length=500, null=True, blank=True)
    Type = models.CharField('Type', max_length=500, null=True, blank=True)
    PPA = models.CharField('PPA', max_length=500, null=True, blank=True)
    PQE = models.CharField('PQE', max_length=500, null=True, blank=True)
    SS = models.CharField("SS", max_length=30, null=True, blank=True)
    LD = models.CharField('LD', max_length=20, null=True, blank=True)
    LDNum = models.CharField('LDNum', max_length=20, null=True, blank=True)
    DQAPL = models.CharField('DQAPL', max_length=20, null=True, blank=True)
    DQAPLNum = models.CharField('DQAPLNum', max_length=20, null=True, blank=True)
    ModifiedDate = models.CharField('ModifiedDate', max_length=100, default="", null=True, blank=True)

# class lessonlearn_Project(models.Model):
#     Customer = models.CharField(max_length=20)
#     Project = models.CharField(max_length=50)
#     Phase = models.CharField(max_length=50,default='')
#     lesson = models.ForeignKey("lesson_learn",on_delete=True)
#     result=models.CharField(max_length=20)
#     Comment=models.CharField(max_length=1000)
