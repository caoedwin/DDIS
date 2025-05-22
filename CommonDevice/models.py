from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from app01.models import UserInfo
# Create your models here.

class Category(models.Model):
    """大类模型"""
    name = models.CharField("大类名称", max_length=50, unique=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    """细项模型（依赖大类）"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField("细项名称", max_length=50)

    def __str__(self):
        return self.name

class CommonDevice(models.Model):
    # Category_choice = (
    #     # ('Select Customer', 'Select Customer'),
    #     ('', ''),
    #     ('網絡設備', '網絡設備'),
    #     ('自動化設備', '自動化設備'),
    # )
    # Product_Type_choice = (
    #     # ('Select Customer', 'Select Customer'),
    #     ('', ''),
    #     ('宽带', '宽带'),
    #     ('伺服器', '伺服器'),
    #     ('交換機', '交換機'),
    #     ('自動化設備', '自動化設備'),
    # )
    Status_choice = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('使用中', '使用中'),
        ('損壞', '損壞'),
        ('閑置', '閑置'),
        ('報廢', '報廢'),
    )
    Category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="大类")
    Product_Type = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name="细项")
    # Category = models.CharField("大项", choices=Category_choice, max_length=50)
    # Product_Type = models.CharField("细项", choices=Product_Type_choice, max_length=50)
    Name = models.CharField("Name", max_length=50, null=True, blank=True)
    Num = models.CharField("號碼", max_length=50, null=True, blank=True)
    Manufacturer = models.CharField("廠商", max_length=50, null=True, blank=True)
    Cost = models.FloatField("費用(CNY)", max_length=50, null=True, blank=True)
    Account = models.CharField("Account", max_length=50, null=True, blank=True)
    PW = models.CharField("密碼", max_length=50, null=True, blank=True)
    Purchasing_Date = models.DateField("購買日期", max_length=50)
    Department = models.CharField("部別", max_length=50)
    Location = models.CharField("位置", max_length=50, null=True, blank=True)
    Asset_Num = models.CharField("資產編號", max_length=50, null=True, blank=True)
    Dev_Status = models.CharField("狀態", choices=Status_choice, max_length=50, null=True, blank=True)
    Owner = models.ManyToManyField("app01.UserInfo")
    # Owner = models.CharField("负责人", max_length=50, null=True, blank=True)
    Mail = models.EmailField("郵件地址", null=True, blank=True)
    Contact_info = models.CharField("聯係方式", max_length=50, null=True, blank=True)
    Comments = models.CharField("Comments", max_length=2000, null=True, blank=True)
    Creator = models.CharField("Creator", max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    # password_hash = models.CharField(max_length=128, null=True)

    # def set_password(self, raw_password):
    #     self.password_hash = make_password(raw_password)
    #
    # def check_password(self, raw_password):
    #     return check_password(raw_password, self.password_hash)
    #
    # def save(self, *args, **kwargs):
    #     # 自动哈希新密码或修改后的密码
    #     if not self.password_hash.startswith('pbkdf2_sha256$'):
    #         self.set_password(self.password_hash)
    #     super().save(*args, **kwargs)
    class Meta:
        verbose_name = '公共设备'#不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name
    def __str__(self):
        # '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
        return '{Category}-{Product_Type}-{Name}-{Owner}'.format(Category=self.Category, Product_Type=self.Product_Type,
                                                                                           Name=self.Name, Owner=self.Owner)