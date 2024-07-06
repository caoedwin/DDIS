from django.db import models

# Create your models here.
class INVGantt(models.Model):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    TP_Cat_list = (
        ('', ''),
        ('adapter', 'adapter'),
        ('Battery', 'Battery'),
        ('BIOS ROM', 'BIOS ROM'),
        ('Camera', 'Camera'),
        ('Connector', 'Connector'),
        ('CPU', 'CPU'),
        ('EE', 'EE'),
        ('FAN', 'FAN'),
        ('Finger Print', 'Finger Print'),
        ('HDD', 'HDD'),
        ('KB/Mouse', 'KB/Mouse'),
        ('Keyborad', 'Keyborad'),
        ('ME', 'ME'),
        ('package', 'package'),
        ('Panel', 'Panel'),
        ('RAM', 'RAM'),
        ('SSD', 'SSD'),
        ('SSD+Opante', 'SSD+Opante'),
        ('Thermal Module', 'Thermal Module'),
        ('Touch Panel', 'Touch Panel'),
        ('TPM', 'TPM'),
        ('VRAM', 'VRAM'),
        ('WLAN', 'WLAN'),
    )

    Phase_list = (
        ('', ''),
        ('SIT', 'SIT'),
        ('FVT', 'FVT'),
        ('OOC', 'OOC'),
        ('INV', 'INV'),
    )

    Testresult_list = (
        ('', ''),
        ('Qd', 'Qd'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('T', 'T'),
        ('F', 'F'),
        ('DisQ', 'DisQ'),
        ('Drpd', 'Drpd'),
        ('No Build', 'No Build')
    )
    Material_Group_list = (
        ('', ''),
        ('Active pen', 'Active pen'),
        ('Adapter', 'Adapter'),
        ('Audio codec', 'Audio codec'),
        ('Battery', 'Battery'),
        ('Camera', 'Camera'),
        ('CardReader', 'CardReader'),
        ('CPU', 'CPU'),
        ('Fan', 'Fan'),
        ('Finger_print', 'Finger_print'),
        ('HDD', 'HDD'),
        ('Keyboard', 'Keyboard'),
        ('LCD_Panel', 'LCD_Panel'),
        ('ODD', 'ODD'),
        ('Power_Cord', 'Power_Cord'),
        ('RAM', 'RAM'),
        ('RAM on board', 'RAM on board'),
        ('Speaker', 'Speaker'),
        ('SSD', 'SSD'),
        ('Touch_Pad', 'Touch_Pad'),
        ('Thermal module', 'Thermal module'),
        ('VRAM', 'VRAM'),
        ('VGA', 'VGA'),
        ('WLAN', 'WLAN'),
        ('Others', 'Others'),
    )

    Qualify_Cycles_list = (
        ('', ''),
        ('New-Qualify', 'New-Qualify'),
        ('Re-Qualify', 'Re-Qualify'),
    )

    Unit_Origin_list = (
        ('', ''),
        ('Self', 'Self'),
        ('New', 'New'),
    )

    Month_list = (
        ('', ''),
        ('Jan', 'Jan'),
        ('Feb', 'Feb'),
        ('Mar', 'Mar'),
        ('Apr', 'Apr'),
        ('May', 'May'),
        ('Jun', 'Jun'),
        ('Jul', 'Jul'),
        ('Aug', 'Aug'),
        ('Sep', 'Sep'),
        ('Oct', 'Oct'),
        ('Nov', 'Nov'),
        ('Dec', 'Dec'),
    )

    Status_list = (
        ('', ''),
        ('Pass', 'Pass'),
        ('Conditional Pass', 'Conditional Pass'),
        ('Fail', 'Fail'),
        ('Planning', 'Planning'),
        ('Pending', 'Pending'),
        ('Testing', 'Testing'),
    )

    Customer = models.CharField('Customer', choices=Customer_list, max_length=100)
    INV_Number = models.CharField("INV_Number", max_length=100)
    INV_Model = models.CharField("INV_Model", max_length=100)
    Project_Name = models.CharField("Project_Name", max_length=100)
    Unit_Origin = models.CharField("Unit_Origin", default="", max_length=100, choices=Unit_Origin_list)
    Year = models.CharField("Year", max_length=100)

    # Year = models.DateField(label="Year", required=True, widget=models.DateInput(
    #     attrs={'class': 'form-control-new', 'type': 'text', 'readonly': "readonly",
    #            "onclick": "WdatePicker()"}))

    Unit_Qty = models.CharField("Unit_Qty", max_length=100)
    TP_Kinds = models.CharField("TP_Kinds", max_length=100)
    Qualify_Cycles = models.CharField("Qualify_Cycles", max_length=100, choices=Qualify_Cycles_list)
    Status = models.CharField("Status", max_length=100, choices=Status_list)
    TP_Cat = models.CharField("TP_Cat", max_length=100, choices=TP_Cat_list)
    # TP_Cat = models.CharField(label="TP_Cat", max_length=100, widget=models.TextInput(attrs={'class': 'form-control-new'}))
    Trial_Run_Type = models.CharField("Trial_Run_Type", max_length=100)
    TP_Vendor = models.CharField("TP_Vendor", max_length=100)
    TP_Key_Parameter = models.CharField("TP_Key_Parameter", max_length=500)
    Lenovo_TP_PN = models.CharField("Lenovo_TP_PN", max_length=100)
    Compal_TP_PN = models.CharField("Compal_TP_PN", max_length=200)
    Issue_Link = models.CharField("Issue_Link", max_length=100)
    Remark = models.CharField("Remark", max_length=1000)
    Attend_Time = models.CharField("Attend_Time", max_length=100)
    ReTest_Attend_Time = models.CharField("ReTest_Attend_Time", default='', max_length=100)
    TestOwner = models.CharField("TestOwner", default='', max_length=100)
    Month = models.CharField("Month", max_length=100, choices=Month_list)
    # Test_Start = models.CharField(label="Test_Start", max_length=100, widget=models.TextInput(attrs={'class': 'form-control-new'}))
    Test_Start = models.DateField("Test_Start", null=True)
    # Test_End = models.CharField(label="Test_End", max_length=100, widget=models.TextInput(attrs={'class': 'form-control-new'}))
    Test_End = models.DateField("Test_End", null=True)
    Editor = models.CharField('Editor', max_length=20)
    Edittime = models.DateTimeField('Edittime', max_length=20)