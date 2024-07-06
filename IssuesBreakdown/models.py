from django.db import models

# Create your models here.
class IssuesBreakdown(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(NB)-SMB', 'C38(NB)-SMB'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('T88(NB)', 'T88(NB)'),
        ('ABO', 'ABO'),
        ('Others', 'Others'),
    )
    Category_list = (
        ('', ''),
        ('New found_Unidentified', 'New found_Unidentified'),
        ('New found_MWD', 'New found_MWD'),
        ('New found_New Implement', 'New found_New Implement'),
        ('New found_Stress', 'New found_Stress'),
        ('Regression Fail', 'Regression Fail'),
        ('UE', 'UE'),
        ('Adhoc', 'Adhoc'),
        ('Late found', 'Late found'),
    )
    Customer = models.CharField('Customer', choices=Customer_list, max_length=100)
    Project = models.CharField('Project', max_length=100)
    FFRT_Entry_unclose_issue = models.CharField('FFRT Entry unclose issue', max_length=10, blank=True, null=True)
    SIT_Exit_unclose_issue = models.CharField('SIT Exit unclose issue', max_length=10, blank=True, null=True)
    first_FFRT = models.CharField('1st FFRT', max_length=21, blank=True, null=True)
    second_FFRT = models.CharField('2nd FFRT', max_length=21, blank=True, null=True)
    third_FFRT = models.CharField('3rd FFRT', max_length=21, blank=True, null=True)
    fourth_FFRT = models.CharField('4th FFRT', max_length=21, blank=True, null=True)
    fifth_FFRT = models.CharField('5th FFRT', max_length=21, blank=True, null=True)
    sixth_FFRT = models.CharField('6th FFRT', max_length=21, blank=True, null=True)
    issue_def = models.CharField('分類', choices=Category_list, max_length=50, blank=True, null=True)
    Remark = models.TextField('Remark', max_length=5000, blank=True, null=True)
    FFRT = models.CharField('FFRT', max_length=20, blank=True, null=True)
    Defect_ID = models.CharField('Defect ID', max_length=20, blank=True, null=True)
    Title = models.CharField('Title', max_length=1000, blank=True, null=True)
    Create_date = models.DateTimeField('Create date')
    Update_date = models.DateTimeField('Update date')
    Status = models.CharField('Status', max_length=50, blank=True, null=True)
    Severity = models.CharField('Severity', max_length=50, blank=True, null=True)
    Category = models.CharField('Category', max_length=100, blank=True, null=True)
    Component = models.CharField('Component', max_length=200, blank=True, null=True)
    BIOS_KBC = models.CharField('BIOS/KBC', max_length=100, blank=True, null=True)
    Comments = models.TextField('Comments', max_length=5000, blank=True, null=True)
    Author = models.CharField('Author', max_length=200, blank=True, null=True)
    Assign_to = models.CharField('Assign to', max_length=200, blank=True, null=True)
    Description = models.TextField('Description', max_length=6000, blank=True, null=True)
    Reproduce_steps = models.TextField('Reproduce steps', max_length=6000, blank=True, null=True)
    Age = models.CharField('Age', max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'IssuesBreakdown'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}--{Project}--{Defect_ID}'.format(Customer=self.Customer, Project=self.Project, Defect_ID=self.Defect_ID)