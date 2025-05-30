from django.db import models
from app01.models import lesson_learn, UserInfo


# from TestPlanME.models import TestProjectME
# Create your models here.
class A31Imgs(models.Model):
    # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
    img = models.ImageField(upload_to='img/A31/Lesson/',verbose_name='图片地址')
    single = models.CharField(max_length=200,null=True, blank=True,verbose_name='图片名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.img)

    # def __str__(self):
    #     return str(self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=A31Imgs)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)
class A31files(models.Model):
    files = models.FileField(upload_to="videos/A31/Lesson/", null=True, blank=True, verbose_name="视频内容")
    single = models.CharField(max_length=200, null=True, blank=True, verbose_name='视频名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)

class A31lesson_learn(models.Model):
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
    Status = models.CharField('Status', choices=choosestatus, max_length=20, default='active', blank=True)
    Photo = models.ManyToManyField(A31Imgs, related_name='imgs', blank=True, verbose_name='图片表')
    video = models.ManyToManyField(A31files, related_name='video', blank=True, verbose_name='视频表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26, blank=True)
		#upload_to参数为指定的文件服务器上保存路径，如果没有该目录django会自动创建
    class Meta:
        verbose_name = 'A31lesson_learn'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Category}-{Object}---{Symptom}'.format(Category=self.Category, Object=self.Object,Symptom=self.Symptom)

class A31TestProjectLL(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('A31', 'A31'),
        ('Others', 'Others'),
    )
    Phase_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    Customer = models.CharField('Customer', choices=Customer_choice, max_length=20)
    Project = models.CharField('Project', max_length=100, unique=True)
    # Phase =models.CharField('Phase',choices=Phase_choice,max_length=20)
    Owner = models.ManyToManyField("app01.UserInfo")

    class Meta:
        verbose_name = 'A31TestProjectLL'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Project}'.format(Project=self.Project)

# class A31reports(models.Model):
#     # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
#     report = models.ImageField(upload_to='reports/A31/LessonProjectResult/',verbose_name='报告地址')
#     single = models.CharField(max_length=200,null=True, blank=True,verbose_name='报告名称')
#     def __unicode__(self):  # __str__ on Python 3
#         return (self.id,self.report)
# from django.db.models.signals import pre_delete
# from django.dispatch.dispatcher import receiver
# @receiver(pre_delete, sender=A31reports)
# def mymodel_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     instance.report.delete(False)

class A31lessonlearn_Project(models.Model):
    result_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('N/S', 'N/S'),
        ('N/A', 'N/A'),
        ('N/P', 'N/P'),
    )
    Projectinfo = models.ForeignKey("A31TestProjectLL", on_delete=True)
    lesson = models.ForeignKey("A31lesson_learn", on_delete=True)
    result = models.CharField(max_length=20, choices=result_choice)
    # Report = models.ManyToManyField(A31reports, related_name='reports', blank=True, verbose_name='报告表')
    Comment = models.CharField(max_length=1000)
    editor = models.CharField(max_length=100, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, default='')