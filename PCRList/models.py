# pcr/models.py
from django.db import models
from django.core.validators import MinValueValidator
from app01.models import UserInfo
from CQM.models import CQMProject


class PCR(models.Model):
    """
    PCR 记录主表
    """
    # 基本信息
    pcr_no = models.CharField(max_length=100, verbose_name="PCR No")
    pcr_title = models.CharField(max_length=200, verbose_name="PCR Title")

    Customer_CHOICES = [
        ('NB', 'NB'),
        ('AIO', 'AIO'),
    ]
    Customer = models.CharField(max_length=10, choices=Customer_CHOICES, verbose_name="Customer")

    # 项目信息：Project 用于显示，Compalproject 用于关联 CQMProject 表做权限控制
    Project = models.CharField(max_length=500, verbose_name="Project")
    Compalproject = models.CharField(max_length=50, verbose_name="Compal Project")

    # 阶段 NPI / INV
    PHASE_CHOICES = [
        ('NPI', 'NPI'),
        ('INV', 'INV'),
    ]
    phase = models.CharField(max_length=3, choices=PHASE_CHOICES, verbose_name="NPI or INV")
    category = models.CharField(max_length=50, verbose_name="Category")

    receive_date = models.DateField(verbose_name="Receive Date", null=True)

    STATUS_CHOICES = [
        ('Perform', 'Perform'),
        ('On going', 'On going'),
        ('Plan', 'Plan'),
        ('Ongoing', 'Ongoing'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Status")

    # NRE 工作量
    sample_qty = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)], verbose_name="Sample Q'ty"
    )
    hc_qty = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)], verbose_name="HC Q'ty"
    )
    hc_days = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        validators=[MinValueValidator(0)], verbose_name="HC Days"
    )
    pd = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, blank=True,
        verbose_name="PD"
    )
    device_fee_usd = models.DecimalField(
        max_digits=12, decimal_places=2, default=0,
        validators=[MinValueValidator(0)], verbose_name="Device fee (USD)"
    )

    # 流程与预算
    dqa_nre_mail_to_pm = models.TextField(blank=True, verbose_name="DQA NRE mail to PM")
    pm_send_nre_to_sales = models.BooleanField(default=False, verbose_name="PM send NRE to Sales")
    execution_start = models.DateField(null=True, blank=True, verbose_name="Execution Start")
    execution_end = models.DateField(null=True, blank=True, verbose_name="Execution End")
    whether_in_budget = models.BooleanField(default=True, verbose_name="Whether In Budget")
    in_budget_but_cost_add = models.BooleanField(default=False, verbose_name="In budget but cost add")
    remark = models.TextField(blank=True, verbose_name="Remark")
    attachment = models.FileField(
        upload_to='pcr_attachments/%Y/%m/',
        blank=True, null=True,
        verbose_name="報NRE郵件"
    )

    # 审计与权限
    created_by = models.ForeignKey(
        UserInfo,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="创建者"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        ordering = ['-receive_date']
        verbose_name = "PCR"
        verbose_name_plural = "PCR"
        # 唯一约束：PCR No + Project + PCR Title
        unique_together = [['pcr_no', 'Project', 'pcr_title']]
        indexes = [
            models.Index(fields=['Project', 'phase', 'status']),
        ]

    def save(self, *args, **kwargs):
        if self.hc_qty and self.hc_days:
            self.pd = self.hc_qty * self.hc_days
        else:
            self.pd = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.pcr_no} - {self.pcr_title[:50]}"