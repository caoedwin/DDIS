from django.db import models

# Create your models here.
class ProjectPlan(models.Model):
    RD_Project_Plan = models.CharField('RD_Project_Plan', default='', max_length=12)
    Year = models.CharField('Year', max_length=12)
    DataType = models.CharField('DataType', max_length=12)
    CG = models.CharField('CG', max_length=20)
    Compal_Model = models.CharField('Compal Model', max_length=200)
    Customer_Model = models.CharField('Customer Model', max_length=400)
    Marketing_type = models.CharField("""Marketing type
(Commercial / Consumer)""", max_length=50)
    Status = models.CharField("""Status:
Planning  =P
Executing=E""", max_length=10)
    Customer = models.CharField('Customer', max_length=10)
    Product_Type = models.CharField("""Product Type
(NB/PAD/AIO/IPC)""", max_length=20)
    Jan = models.CharField("Jan", max_length=50, default='', null=True, blank=True)
    Feb = models.CharField("Feb", max_length=50, default='', null=True, blank=True)
    Mar = models.CharField("Mar", max_length=50, default='', null=True, blank=True)
    Apr = models.CharField("Apr", max_length=50, default='', null=True, blank=True)
    May = models.CharField("May", max_length=50, default='', null=True, blank=True)
    Jun = models.CharField("Jun", max_length=50, default='', null=True, blank=True)
    Jul = models.CharField("Jul", max_length=50, default='', null=True, blank=True)
    Aug = models.CharField("Aug", max_length=50, default='', null=True, blank=True)
    Sep = models.CharField("Sep", max_length=50, default='', null=True, blank=True)
    Oct = models.CharField("Oct", max_length=50, default='', null=True, blank=True)
    Nov = models.CharField("Nov", max_length=50, default='', null=True, blank=True)
    Dec = models.CharField("Dec", max_length=50, default='', null=True, blank=True)

    class Meta:
        verbose_name = 'ProjectPlan'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Year}--{DataType}--{Customer}'.format(Year=self.Year, DataType=self.DataType, Customer=self.Customer)