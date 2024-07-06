from django.db import models

# Create your models here.
class KnowIssue_M(models.Model):
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
    Issue_NO = models.CharField("Issue_NO", max_length=50)
    Issue_Title = models.CharField("Issue_Title", max_length=1000)
    Issue_Component = models.CharField("Issue_Component", max_length=1000)
    Detect_By_Case = models.CharField("Detect_By_Case", max_length=1000)
    Root_Cause = models.CharField("Root_Cause", max_length=2000)
    Issue_Status = models.CharField("Issue_Status", max_length=100)
    PL = models.CharField("PL", max_length=20)
    Editor = models.CharField('Editor', max_length=20)
    Edittime = models.DateTimeField('Edittime', max_length=20)
