from django.db import models

# Create your models here.
class SubscriptionStatus(models.Model):
    Year = models.CharField('Year', default='', max_length=12)
    Ledger = models.CharField('會計科目', default='', max_length=20, blank=True, null=True)
    Name = models.CharField('設備名稱/项目', max_length=500, blank=True, null=True)
    Status = models.CharField('到貨狀態', max_length=50, blank=True, null=True)
    ModelSpecifications = models.CharField('型號規格', max_length=1000, blank=True, null=True)
    SubscribeDate = models.DateField('申購日期', blank=True, null=True)
    SubscribeForm = models.CharField('申購單', max_length=50, blank=True, null=True)
    SubscribeUnitPrice = models.FloatField("""申購單價""", max_length=20, blank=True, null=True)
    Number = models.IntegerField("""數量""", blank=True, null=True)
    AcceptanceForm = models.CharField('驗收單號', max_length=20, blank=True, null=True)
    AcceptanceDate = models.DateField("""驗收日期""", blank=True, null=True)
    ActUnitPrice = models.FloatField("""實際單價""", max_length=20, blank=True, null=True)
    Customer = models.CharField("""客戶別""", max_length=20, blank=True, null=True)
    ProjectCode = models.CharField("""Project Code""", max_length=50, blank=True, null=True)
    Department = models.CharField("""申購部門""", max_length=20, blank=True, null=True)
    RequisitionerNum = models.CharField("""申購人工號""", max_length=20, blank=True, null=True)
    Requisitioner = models.CharField("""申購人""", max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = 'SubscriptionStatus'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Year}--{Ledger}--{Name}--{SubscribeForm}--{AcceptanceForm}--{Requisitioner}'.format(Year=self.Year, Ledger=self.Ledger, Name=self.Name, SubscribeForm=self.SubscribeForm, AcceptanceForm=self.AcceptanceForm, Requisitioner=self.Requisitioner)

class Budget(models.Model):
    Year = models.CharField("年份", max_length=100)  # 數據年份
    Ledger = models.CharField('會計科目', default='', max_length=20, blank=True, null=True)
    Jan = models.FloatField("Jan", max_length=50, null=True, blank=True)
    Feb = models.FloatField("Feb", max_length=50, null=True, blank=True)
    Mar = models.FloatField("Mar", max_length=50, null=True, blank=True)
    Apr = models.FloatField("Apr", max_length=50, null=True, blank=True)
    May = models.FloatField("May", max_length=50, null=True, blank=True)
    Jun = models.FloatField("Jun", max_length=50, null=True, blank=True)
    Jul = models.FloatField("Jul", max_length=50, null=True, blank=True)
    Aug = models.FloatField("Aug", max_length=50, null=True, blank=True)
    Sep = models.FloatField("Sep", max_length=50, null=True, blank=True)
    Oct = models.FloatField("Oct", max_length=50, null=True, blank=True)
    Nov = models.FloatField("Nov", max_length=50, null=True, blank=True)
    Dec = models.FloatField("Dec", max_length=50, null=True, blank=True)
    class Meta:
        verbose_name = '預算費用'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Year}-{Ledger}'.format(Year=self.Year, Ledger=self.Ledger)

class ReceiptAmount(models.Model):
    Year = models.CharField("年份", max_length=100)  # 數據年份
    Ledger = models.CharField('會計科目', default='', max_length=20, blank=True, null=True)
    Jan = models.FloatField("Jan", max_length=50, null=True, blank=True)
    Feb = models.FloatField("Feb", max_length=50, null=True, blank=True)
    Mar = models.FloatField("Mar", max_length=50, null=True, blank=True)
    Apr = models.FloatField("Apr", max_length=50, null=True, blank=True)
    May = models.FloatField("May", max_length=50, null=True, blank=True)
    Jun = models.FloatField("Jun", max_length=50, null=True, blank=True)
    Jul = models.FloatField("Jul", max_length=50, null=True, blank=True)
    Aug = models.FloatField("Aug", max_length=50, null=True, blank=True)
    Sep = models.FloatField("Sep", max_length=50, null=True, blank=True)
    Oct = models.FloatField("Oct", max_length=50, null=True, blank=True)
    Nov = models.FloatField("Nov", max_length=50, null=True, blank=True)
    Dec = models.FloatField("Dec", max_length=50, null=True, blank=True)
    class Meta:
        verbose_name = '實際入賬金額'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Year}-{Ledger}'.format(Year=self.Year, Ledger=self.Ledger)