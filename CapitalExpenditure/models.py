from django.db import models

# Create your models here.
class CapitalExpenditure(models.Model):
    PlanYear = models.CharField('PlanYear', default='', max_length=12)
    Customer = models.CharField('客戶別', default='', max_length=20, blank=True, null=True)
    BudgetCode = models.CharField('預算編號', max_length=30, blank=True, null=True)
    Investment_Nature = models.CharField('投資性質', max_length=12, blank=True, null=True)
    Attribute_Code = models.CharField('屬性代碼', max_length=20, blank=True, null=True)
    Application_Department = models.CharField('申請部門', max_length=20, blank=True, null=True)
    Device_Name = models.CharField('設備或工程名稱', max_length=400, blank=True, null=True)
    Usage_Description = models.CharField("""用途說明""", max_length=4000, blank=True, null=True)
    Specifications = models.CharField("""廠牌規格""", max_length=3000, blank=True, null=True)
    Acceptance_Month = models.CharField('驗收月份', max_length=10, blank=True, null=True)
    Budget_Quantity = models.IntegerField("""預算數量""", blank=True, null=True)
    Estimated_Original_Currency = models.CharField("""預估總價_原幣_幣別""", max_length=20, blank=True, null=True)
    Estimated_Original_Price = models.CharField("""預估總價_原幣_金額""", max_length=20, blank=True, null=True)
    Equivalent_To_RMB = models.IntegerField("""折合人民幣""", blank=True, null=True)
    Payment_Terms = models.CharField("""付款條件""", max_length=200, blank=True, null=True)
    Depreciation_Months = models.IntegerField("""折舊月數""", blank=True, null=True)
    Accounting_Subjects = models.CharField("""會計科目""", max_length=20, blank=True, null=True)
    Automated_Or_Not = models.CharField("""是否自動化""", max_length=20, blank=True, null=True)
    Project_Code = models.CharField("""Project Code""", max_length=20, blank=True, null=True)
    Current_Situation = models.CharField("""現狀說明""", max_length=20, blank=True, null=True)
    Applicable_Scope = models.CharField("""適用範圍""", max_length=20, blank=True, null=True)
    Investment_Purpose = models.CharField("""投資動機與目的""", max_length=5000, blank=True, null=True)
    Investment_Purpose_Des = models.CharField("""投資動機與目的其他說明""", max_length=3000, blank=True, null=True)
    Potential_Issues = models.CharField("""潛在問題""", max_length=3000, blank=True, null=True)
    Potential_Issues_Des = models.CharField("""潛在問題的其他說明""", max_length=1000, blank=True, null=True)
    Tighten_Expenses = models.CharField("""年節省支出""", max_length=20, blank=True, null=True)
    Annual_Increase_PerYear = models.IntegerField("""年增加收益""", blank=True, null=True)
    Investment_Benefits_PerYear = models.IntegerField("""年投資效益""", blank=True, null=True)
    Cash_Inflows_PerYear = models.IntegerField("""年淨現金流入""", blank=True, null=True)
    Payback_Period = models.IntegerField("""回收年限(月數)""", blank=True, null=True)
    Subscription_Status = models.CharField("""申購狀況""", max_length=20)
    Subscription_Quantity = models.IntegerField("""申購數量""", blank=True, null=True)
    Subscription_Amount = models.FloatField("""申購金額
(CNY)""", max_length=20, blank=True, null=True)
    Entry_Amount = models.FloatField("""入賬金額
(CNY)""", max_length=20, blank=True, null=True)


    class Meta:
        verbose_name = 'CapitalExpenditure'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{PlanYear}--{BudgetCode}--{Application_Department}'.format(PlanYear=self.PlanYear, BudgetCode=self.BudgetCode, Application_Department=self.Application_Department)

class C38CustomerT88AIODepartmentCode(models.Model):
    Year = models.CharField('Year', default='', max_length=12)
    Department_Code = models.CharField('部門代码', max_length=20, blank=True, null=True)\


    class Meta:
        verbose_name = 'C38CustomerT88AIODepartmentCode'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Year}--{Department_Code}'.format(Year=self.Year, Department_Code=self.Department_Code)