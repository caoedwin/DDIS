from django.db import models

# Create your models here.
class LowLightList(models.Model):
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
    # Phase_list = (
    #     ('', ''),
    #     ('SIT', 'SIT'),
    #     ('FVT', 'FVT'),
    #     ('OOC', 'OOC'),
    #     ('INV', 'INV'),
    # )
    Customer = models.CharField('Customer', choices=Customer_list, max_length=100)
    ProjectCompal = models.CharField('ProjectCompal', max_length=100)
    Lowlight_item = models.CharField('Lowlight_item', max_length=1000, blank=True, null=True)
    Root_Cause = models.CharField('Root_Cause',max_length=5000)
    LD = models.CharField('LD', max_length=100)
    Owner = models.CharField('Owner', max_length=200, blank=True, null=True)
    Mitigation_plan = models.CharField('Mitigation_plan', max_length=5000, blank=True, null=True)
    editor = models.CharField('editor', max_length=100)
    edit_time = models.DateTimeField('edit_time')

    class Meta:
        verbose_name = 'LowLightList'  # 不写verbose_name, admin中默认的注册名会加s
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{Customer}--{Project}--{Lowlight_item}'.format(Customer=self.Customer, Project=self.ProjectCompal, Lowlight_item=self.Lowlight_item)