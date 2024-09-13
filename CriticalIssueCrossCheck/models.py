from django.db import models
from app01.models import lesson_learn, UserInfo


# from TestPlanME.models import TestProjectME
# Create your models here.
class CriticalIssueImgs(models.Model):
    # id = models.AutoField(max_length=10, primary_key=True, verbose_name='id')
    img = models.ImageField(upload_to='img/CriticalIssue/',verbose_name='图片地址')
    single = models.CharField(max_length=200,null=True, blank=True,verbose_name='图片名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.img)

    # def __str__(self):
    #     return str(self.single)
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
@receiver(pre_delete, sender=CriticalIssueImgs)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.img.delete(False)
class CriticalIssuefiles(models.Model):
    files = models.FileField(upload_to="videos/CriticalIssue/", null=True, blank=True, verbose_name="视频内容")
    single = models.CharField(max_length=200, null=True, blank=True, verbose_name='视频名称')
    def __unicode__(self):  # __str__ on Python 3
        return (self.id,self.files)

class CriticalIssue(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('T89(NB)', 'T89(NB)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('A31', 'A31'),
        ('A32', 'A32'),
        ('Others', 'Others'),
    )
    choosecat = (
        ("", ""),
        ("shutdown", "shutdown"),
        ("burnt out", "burnt out"),
        ("blue screen", "blue screen"),
        ("restart", "restart"),
        ("black screen", "black screen"),
        ("data lost", "data lost"),
    )
    choosestatus = (
        ("", ""),
        ("active", "active"),
        ("inactive", "inactive")
    )
    IssueNum = models.AutoField(primary_key=True, default=100001)
    CG = models.CharField('Customer', choices=Customer_choice, max_length=20)
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
    Project = models.CharField('Project', max_length=200,default='', blank=True)
    Status = models.CharField('Status', choices=choosestatus, max_length=20, default='active', blank=True)
    Photo = models.ManyToManyField(CriticalIssueImgs, related_name='imgs', blank=True, verbose_name='图片表')
    video = models.ManyToManyField(CriticalIssuefiles, related_name='video', blank=True, verbose_name='视频表')
    editor = models.CharField(max_length=100)
    edit_time = models.CharField('edit_time', max_length=26, blank=True)
		#upload_to参数为指定的文件服务器上保存路径，如果没有该目录django会自动创建
    class Meta:
        verbose_name = 'CriticalIssue'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Category}-{Object}---{Symptom}'.format(Category=self.Category, Object=self.Object,Symptom=self.Symptom)

class CriticalIssueTestProject(models.Model):
    Customer_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('T89(NB)', 'T89(NB)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('A31', 'A31'),
        ('A32', 'A32'),
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
        verbose_name = 'CriticalIssueTestProject'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Project}'.format(Project=self.Project)


class CriticalIssueCrossResult(models.Model):
    result_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('N/S', 'N/S'),
        ('N/A', 'N/A'),
        ('N/P', 'N/P'),
    )
    Projectinfo = models.ForeignKey("CriticalIssueTestProject", on_delete=True)
    CriticalIssue = models.ForeignKey("CriticalIssue", on_delete=True)
    result = models.CharField(max_length=20, choices=result_choice)
    Comment = models.CharField(max_length=1000)
    editor = models.CharField(max_length=100, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, default='')