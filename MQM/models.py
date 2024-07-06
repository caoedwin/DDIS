from django.db import models

# Create your models here.
class MQM(models.Model):
    Choice_customer=(
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('C85', 'C85'),
        ('Others', 'Others')
    )
    Choice_result=(
        ('', ''),
        ('QS', 'QS'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('QT', 'QT'),
        ('QF', 'QF'),
        ('QF_L', 'QF_L'),
        ('DisQ', 'DisQ'),
        ('Drop', 'Drop'),
        ('Not Build', 'Not Build'),
    )
    Customer=models.CharField('Customer', max_length=10, choices=Choice_customer, default='')
    Project = models.CharField('Project', max_length=20)
    Category = models.CharField('Category', max_length=200,default='',)
    Name=models.CharField('Name', max_length=300)
    Vendor=models.CharField('Vender', max_length=50, default='', blank=True, null=True)
    SourcePriority=models.CharField('SourcePriority', max_length=10)
    CompalPN=models.CharField('CompalPN', max_length=50, default='', blank=True, null=True)
    VendorPN=models.CharField('VendorPN', max_length=50, default='', blank=True, null=True)
    Status = models.CharField('Status', max_length=50, default='', blank=True, null=True)
    Description=models.CharField('Description', max_length=500, default='')
    Qty = models.CharField('Qty', max_length=50, default='', blank=True, null=True)
    Location=models.CharField('Location', max_length=100, default='', blank=True, null=True)
    B_DQA_DataCode=models.CharField('B_DQA_DataCode',max_length=100, blank=True, null=True)
    B_DQA_Reliability=models.CharField('B_DQA_Reliability', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_DQA_Compatibility=models.CharField('B_DQA_Compatibility', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_DQA_Result=models.CharField('B_DQA_Result', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_ESD=models.CharField('B_RD_ESD', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_EMI=models.CharField('B_RD_EMI', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_RF=models.CharField('B_RD_RF', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_1 = models.CharField('B_RD_1', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_2 = models.CharField('B_RD_2', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_3 = models.CharField('B_RD_3', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_4 = models.CharField('B_RD_4', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    B_RD_5 = models.CharField('B_RD_5', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_DQA_DataCode=models.CharField('C_DQA_DataCode', max_length=100, blank=True, null=True)
    C_DQA_Reliability=models.CharField('C_DQA_Reliability', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_DQA_Compatibility=models.CharField('C_DQA_Compatibility', max_length=10, choices=Choice_result, default='', blank=True,null=True)
    C_DQA_Result=models.CharField('C_DQA_Result', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_ESD=models.CharField('C_RD_ESD', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_EMI=models.CharField('C_RD_EMI', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_RF=models.CharField('C_RD_RF', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_1 = models.CharField('C_RD_1', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_2 = models.CharField('C_RD_2', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_3 = models.CharField('C_RD_3', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_4 = models.CharField('C_RD_4', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    C_RD_5 = models.CharField('C_RD_5', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_DQA_DataCode = models.CharField('INV_DQA_DataCode', max_length=100, blank=True, null=True)
    INV_DQA_Reliability = models.CharField('INV_DQA_Reliability', max_length=10, choices=Choice_result, default='',
                                         blank=True, null=True)
    INV_DQA_Compatibility = models.CharField('INV_DQA_Compatibility', max_length=10, choices=Choice_result, default='',
                                           blank=True, null=True)
    INV_DQA_Result = models.CharField('INV_DQA_Result', max_length=10, choices=Choice_result, default='', blank=True,
                                    null=True)
    INV_RD_ESD = models.CharField('INV_RD_ESD', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_EMI = models.CharField('INV_RD_EMI', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_RF = models.CharField('INV_RD_RF', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_1 = models.CharField('INV_RD_1', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_2 = models.CharField('INV_RD_2', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_3 = models.CharField('INV_RD_3', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_4 = models.CharField('INV_RD_4', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    INV_RD_5 = models.CharField('INV_RD_5', max_length=10, choices=Choice_result, default='', blank=True, null=True)
    Control_run = models.CharField('Control_run', max_length=100, default='', blank=True, null=True)
    Comments = models.CharField('Comments', max_length=4000, default='', blank=True, null=True)
    editor = models.CharField('editor', max_length=100, default='')
    edit_time = models.CharField('edit_time', max_length=26, blank=True, default='')
    class Meta:
        verbose_name = "MQM"
        verbose_name_plural = verbose_name
    def __str__(self):
        return '{Project}-{CompalPN}-{Location}'.format(Project=self.Project, CompalPN=self.CompalPN, Location=self.Location)