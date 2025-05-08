from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from app01.models import UserInfo
# Create your models here.
class CommonDevice(models.Model):
    Category = models.CharField("大项", max_length=50)
    Product_Type = models.CharField("细项", max_length=50)
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
    Owner_Num = models.ManyToManyField("app01.UserInfo")
    Owner = models.CharField("负责人", max_length=50, null=True, blank=True)
    Mail = models.EmailField("郵件地址", null=True, blank=True)
    Contact_info = models.CharField("聯係方式", max_length=50, null=True, blank=True)
    Comments = models.CharField("Comments", max_length=2000, null=True, blank=True)
    Editor = models.CharField("Editor", max_length=50)
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
        return '{Category}-{Product_Type}-{Name}-{Owner_Num}-{Owner}'.format(Category=self.Category, Product_Type=self.Product_Type,
                                                                                           Name=self.Name, Owner_Num=self.Owner_Num, Owner=self.Owner)