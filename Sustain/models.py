from django.db import models


class SustainTask(models.Model):
    """SW Sustain Tracking 主任务表"""

    # ----- 下拉选项定义 -----
    YEAR_CHOICES = [(y, str(y)) for y in range(2011, 2107)]  # 可根据需要调整年份范围
    MONTH_CHOICES = [
        ('Jan', 'Jan'), ('Feb', 'Feb'), ('Mar', 'Mar'), ('Apr', 'Apr'),
        ('May', 'May'), ('Jun', 'Jun'), ('Jul', 'Jul'), ('Aug', 'Aug'),
        ('Sep', 'Sep'), ('Oct', 'Oct'), ('Nov', 'Nov'), ('Dec', 'Dec'),
    ]
    CUSTOMER_CHOICES = [
        ('C38 NB', 'C38 NB'),
        ('C38 AIO', 'C38 AIO'),
        # 如有其他客户可继续添加
    ]
    SERIES_CHOICES = [
        ('Gaming', 'Gaming'),
        ('Consumer', 'Consumer'),
        ('SMB', 'SMB'),
        ('Consumer_CX', 'Consumer_CX'),
        ('Consumer_SX', 'Consumer_SX'),
        ('Consumer_SXP', 'Consumer_SXP'),
        ('', '----'),  # 空值占位
    ]
    EOP_OR_NOT_CHOICES = [('Y', 'Yes'), ('N', 'No')]

    # 基础信息（使用 choices）
    task_no = models.CharField(max_length=50, unique=True, verbose_name='Task No')
    year = models.IntegerField(choices=YEAR_CHOICES, verbose_name='Year')
    month = models.CharField(max_length=20, choices=MONTH_CHOICES, verbose_name='Month')
    customer = models.CharField(max_length=50, choices=CUSTOMER_CHOICES, verbose_name='Customer')
    series = models.CharField(max_length=200, choices=SERIES_CHOICES, blank=True, verbose_name='Series')
    project_code = models.CharField(max_length=50, verbose_name='Project Code')
    project_name = models.CharField(max_length=500, blank=True, verbose_name='Project Name')

    # 项目里程碑
    mp_date = models.DateField(null=True, blank=True, verbose_name='MP Date')
    eop_or_not = models.CharField(max_length=3, choices=EOP_OR_NOT_CHOICES, blank=True, verbose_name='EOP Or Not')
    eop_date = models.DateField(null=True, blank=True, verbose_name='EOP Date')
    eos_date = models.DateField(null=True, blank=True, verbose_name='EOS Date')
    project_status = models.CharField(max_length=20, blank=True, verbose_name='Project Status')
    mp_year = models.CharField(max_length=20, blank=True, verbose_name='MP Year')
    eop_year = models.CharField(max_length=20, blank=True, verbose_name='EOP Year')
    eos_year = models.CharField(max_length=20, blank=True, verbose_name='EOS Year')
    leverage_project = models.CharField(max_length=200, blank=True, verbose_name='Leverage Project')

    # 测试资源
    test_units_status = models.CharField(max_length=200, blank=True, verbose_name='Test Units status')
    unit_qty = models.IntegerField(default=0, verbose_name='Unit_Qty')
    total_test_resource = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                              verbose_name='Total Test Resource')
    total_actual_workload = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                                verbose_name='Total Actual Workload(Hrs)')
    total_leverage_workload = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                                  verbose_name='Total Leverage Workload(Hrs)')
    final_test_status = models.CharField(max_length=50, blank=True, verbose_name='Final Test Status')

    # 任务进度
    task_closure_date = models.DateField(null=True, blank=True, verbose_name='Task Closure Date')
    task_leading_time = models.IntegerField(default=0, verbose_name='Task Leading Time (Days)')
    total_planning_workload = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                                  verbose_name='Total Planning Workload(Hrs)')
    total_waste_time = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name='Total waste time (Hrs)')

    class Meta:
        verbose_name = 'Sustain Task'
        verbose_name_plural = 'Sustain Tasks'
        ordering = ['-year', '-task_no']

    def __str__(self):
        return f"{self.task_no} - {self.project_code}"


class SustainTestDetail(models.Model):
    """测试详情（New Test 或 Regression 测试块）"""
    TEST_STAGE_CHOICES = [
        ('New Test', 'New Test'),
        ('Regression1', 'Regression1'),
        ('Regression2', 'Regression2'),
        ('Regression3', 'Regression3'),
        ('Regression4', 'Regression4'),
        ('Regression5', 'Regression5'),
        # 可按需增加
    ]
    TEST_STATUS_CHOICES = [
        ('Pass', 'Pass'),
        ('Fail', 'Fail'),
        ('Conditional Pass', 'Conditional Pass'),
        ('Planning', 'Planning'),
        ('Pending', 'Pending'),
        ('Testing', 'Testing'),
    ]
    TEST_CATEGORY_CHOICES = [
        ('BIOS', 'BIOS'),
        ('VBIOS', 'VBIOS'),
        ('Driver', 'Driver'),
        ('APP', 'APP'),
        ('FW', 'FW'),
        ('Other', 'Other'),
    ]

    task = models.ForeignKey(SustainTask, on_delete=models.CASCADE, related_name='test_details',
                             verbose_name='所属任务')
    test_stage = models.CharField(max_length=20, choices=TEST_STAGE_CHOICES, verbose_name='Test Stage')

    test_status = models.CharField(max_length=50, choices=TEST_STATUS_CHOICES, blank=True, verbose_name='Test Status')
    test_category = models.CharField(max_length=200, choices=TEST_CATEGORY_CHOICES, blank=True,
                                     verbose_name='Test Category')
    category_info = models.CharField(max_length=500, blank=True, verbose_name='Category Info')
    test_version = models.CharField(max_length=1000, blank=True, verbose_name='Test Version')
    test_condition = models.TextField(blank=True, verbose_name='Test Condition (BIOS/Image/OS)')
    driver_cut_in_format = models.CharField(max_length=500, blank=True, verbose_name='Driver cut in format')
    issue_link = models.URLField(blank=True, verbose_name='Issue Link')

    test_resource = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Test Resource')
    actual_workload = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                          verbose_name='Actual Workload(Hrs)')
    leverage_workload = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                            verbose_name='Leverage Workload(Hrs)')
    test_team = models.CharField(max_length=200, blank=True, verbose_name='Test Team')
    test_owner = models.CharField(max_length=500, blank=True, verbose_name='Test_Owner')

    test_start = models.DateField(null=True, blank=True, verbose_name='Test_Start')
    test_end = models.DateField(null=True, blank=True, verbose_name='Test_End')
    working_day = models.IntegerField(default=0, verbose_name='Working Day')
    change_list = models.TextField(blank=True, verbose_name='Change list')
    remark = models.TextField(blank=True, verbose_name='Remark')

    class Meta:
        verbose_name = 'Test Detail'
        verbose_name_plural = 'Test Details'
        ordering = ['task', 'test_stage']

    def __str__(self):
        return f"{self.task.task_no} - {self.test_stage}"