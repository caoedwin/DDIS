from django.db import models

# Create your models here.
class Issue_Notes_M(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )

    Customer = models.CharField("Customer", choices=Customer_list, max_length=20)
    Project_Code = models.CharField("Project_Code", max_length=50)
    Platform = models.CharField("Platform", max_length=100)
    TDMS_NO = models.CharField("TDMS_NO", max_length=50)
    Issue_Title = models.CharField("Issue_Title", max_length=1000)
    Root_Cause = models.CharField("Root_Cause", max_length=2000)
    Solution = models.CharField("Solution", max_length=2000)
    PL = models.CharField("PL", max_length=20)
    Editor = models.CharField('Editor', max_length=20)
    Edittime = models.DateTimeField('Edittime', max_length=20)
