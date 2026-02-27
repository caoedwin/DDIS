from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from CQM.models import CQMProject
from app01.models import UserInfo

# 基础模型：检查项
class UEInspectionItem(models.Model):
    CATEGORY_CHOICES = [
        ('Reliability', 'Reliability'),
        ('Compatibility', 'Compatibility'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]


    Item = models.CharField(max_length=20, verbose_name='Item')
    Function = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Function')
    Category = models.CharField(max_length=100, verbose_name='Category')
    characteristic = models.CharField(max_length=200, verbose_name='Characteristic')
    detailed_description = models.TextField(verbose_name='詳細說明（Detailed Description）')
    inspect_method = models.TextField(verbose_name='pect Methord')
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name='状态'
    )

    class Meta:
        verbose_name = 'UE检查项目'
        verbose_name_plural = 'UE检查项目'
        ordering = ['Item']

    def __str__(self):
        return f"{self.Item}. {self.characteristic}"

    def save(self, *args, **kwargs):
        # 去除首尾空格
        if self.Category:
            self.Category = self.Category.strip()
        if self.Item:
            self.Item = self.Item.strip()
        if self.characteristic:
            self.characteristic = self.characteristic.strip()
        if self.Function:
            self.Function = self.Function.strip()
        super().save(*args, **kwargs)


# 模型：检查批次
class UEBatch(models.Model):

    batch_id = models.AutoField(primary_key=True, verbose_name='批次ID')
    project = models.ForeignKey(CQMProject, on_delete=models.CASCADE, related_name='batches', verbose_name='所属项目')
    batch_name = models.CharField(max_length=100, verbose_name='批次名称')
    test_date = models.DateField(verbose_name='测试日期')
    testers = models.ManyToManyField(
        UserInfo,
        related_name='ue_batches',
        verbose_name='测试人员'
    )
    created_by = models.ForeignKey('app01.UserInfo', on_delete=models.SET_NULL, null=True, verbose_name='创建人', related_name='uebatch_created')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = 'UE检查批次'
        verbose_name_plural = 'UE检查批次'
        unique_together = ['project', 'batch_name']
        ordering = ['project', '-batch_name']

    def __str__(self):
        return f"{self.project.Project} - 批次: {self.batch_name}"


# 模型：评分记录
class UEScoreRecord(models.Model):
    CATEGORY_CHOICES = [
        ('Reliability', 'Reliability'),
        ('Compatibility', 'Compatibility'),
    ]

    SCORE_CHOICES = [
        ('V', 'V'),  # Not Support
    ]
    NotS_CHOICES = [
        ('N/S', 'N/S'),  # Not Support
    ]

    record_id = models.AutoField(primary_key=True, verbose_name='记录ID')
    batch = models.ForeignKey(UEBatch, on_delete=models.CASCADE, related_name='score_records', verbose_name='所属批次')
    inspection_item = models.ForeignKey(UEInspectionItem, on_delete=models.CASCADE, verbose_name='检查项目')

    scorer = models.ForeignKey('app01.UserInfo', on_delete=models.SET_NULL, null=True, verbose_name='评分人')
    OneStar = models.CharField(max_length=20, choices=SCORE_CHOICES, blank=True, verbose_name='★')
    TwoStar = models.CharField(max_length=20, choices=SCORE_CHOICES, blank=True, verbose_name='★★')
    ThreeStar = models.CharField(max_length=20, choices=SCORE_CHOICES, blank=True, verbose_name='★★★')
    NotSup = models.CharField(max_length=20, choices=NotS_CHOICES, blank=True, verbose_name='Not Support')
    remark = models.TextField(blank=True, null=True, verbose_name='备注')
    scored_date = models.DateTimeField(auto_now_add=True, verbose_name='评分时间')

    class Meta:
        verbose_name = 'UE评分记录'
        verbose_name_plural = 'UE评分记录'
        ordering = ['batch', 'inspection_item__item_id']

    def __str__(self):
        return f"{self.batch.batch_name} - 项目{self.inspection_item.Item}"

