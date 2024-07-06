from django.db import models
from app01.models import lesson_learn, UserInfo
# from TestPlanME.models import TestProjectME
# Create your models here.

class TestProjectLL(models.Model):
    Customer_choice=(
        # ('Select Customer', 'Select Customer'),
        ('',''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others'),
    )
    Phase_choice =(
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    Customer=models.CharField('Customer',choices=Customer_choice,max_length=20)
    Project=models.CharField('Project',max_length=20, unique=True)
    # Phase =models.CharField('Phase',choices=Phase_choice,max_length=20)
    Owner=models.ManyToManyField("app01.UserInfo")
    class Meta:
        verbose_name = 'TestProjectLL'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{Project}'.format(Project=self.Project)

class lessonlearn_Project(models.Model):
    result_choice = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('N/S', 'N/S'),
        ('N/A', 'N/A'),
        ('N/P', 'N/P'),
    )
    Projectinfo = models.ForeignKey("TestProjectLL", on_delete=True)
    lesson = models.ForeignKey("app01.lesson_learn", on_delete=True)
    result=models.CharField(max_length=20, choices=result_choice)
    Comment=models.CharField(max_length=1000)
    editor = models.CharField(max_length=100, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, default='')
