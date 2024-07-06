from django.db import models

# Create your models here.
class ABODriverList_M(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)
    Phase0 = models.CharField(max_length=20)
    Name = models.CharField(max_length=400)
    Function = models.CharField(max_length=50,blank=True,null=True)
    Vendor = models.CharField(max_length=150,blank=True,null=True)
    Version = models.CharField(max_length=150)
    BIOS = models.CharField(max_length=150, default='')
    Image = models.CharField(max_length=50)
    Driver = models.CharField(max_length=50)
    editor = models.CharField(max_length=20,blank=True,null=True)
    edit_time = models.CharField('edit_time', max_length=26,blank=True,null=True)

class ABOToolList_M(models.Model):
    Customer = models.CharField(max_length=20)
    Project = models.CharField(max_length=20)
    Phase0 = models.CharField(max_length=20)
    Vendor = models.CharField(max_length=150,blank=True,null=True)
    Version = models.CharField(max_length=150)
    ToolName = models.CharField(max_length=300)
    TestCase = models.CharField(max_length=100,blank=True,null=True)
    editor = models.CharField(max_length=20,blank=True,null=True)
    edit_time = models.CharField('edit_time', max_length=26,blank=True,null=True)