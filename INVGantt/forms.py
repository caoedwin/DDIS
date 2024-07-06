from django import forms

class INVGantt_F(forms.Form):
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
    # Material_Group_list=(
    #     ('', ''),
    #     ('Active pen', 'Active pen'),
    #     ('Adapter', 'Adapter'),
    #     ('Audio codec', 'Audio codec'),
    #     ('Battery', 'Battery'),
    #     ('Camera', 'Camera'),
    #     ('CardReader', 'CardReader'),
    #     ('CPU', 'CPU'),
    #     ('Fan', 'Fan'),
    #     ('Finger_print', 'Finger_print'),
    #     ('HDD', 'HDD'),
    #     ('Keyboard', 'Keyboard'),
    #     ('LCD_Panel', 'LCD_Panel'),
    #     ('ODD', 'ODD'),
    #     ('Power_Cord', 'Power_Cord'),
    #     ('RAM', 'RAM'),
    #     ('RAM on board', 'RAM on board'),
    #     ('Speaker', 'Speaker'),
    #     ('SSD', 'SSD'),
    #     ('Touch_Pad', 'Touch_Pad'),
    #     ('Thermal module', 'Thermal module'),
    #     ('VRAM', 'VRAM'),
    #     ('VGA', 'VGA'),
    #     ('WLAN', 'WLAN'),
    #     ('Others', 'Others'),
    # )

    Qualify_Cycles_list = (
        ('', ''),
        ('New-Qualify', 'New-Qualify'),
        ('Re-Qualify', 'Re-Qualify'),
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
    Unit_Origin_list = (
        ('', ''),
        ('Self', 'Self'),
        ('New', 'New'),
    )

    Customer = forms.CharField(label="Customer", max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class':'form-control-new'}))
    INV_Number = forms.CharField(label="INV_Number", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    INV_Model = forms.CharField(label="INV_Model", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Project_Name = forms.CharField(label="Project_Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Unit_Origin = forms.CharField(label="Unit_Origin", max_length=100, widget=forms.Select(choices=Unit_Origin_list,attrs={'id': 'Unit_Origin', 'class': 'form-control-new'}))
    Year = forms.CharField(label="Year", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Unit_Qty = forms.CharField(label="Unit_Qty", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    TP_Kinds = forms.CharField(label="TP_Kinds", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Qualify_Cycles = forms.CharField(label="Qualify_Cycles", max_length=100, widget=forms.Select(choices=Qualify_Cycles_list,attrs={'id': 'Qualify_Cycles', 'class': 'form-control-new'}))
    Status = forms.CharField(label="Status", max_length=100, widget=forms.Select(choices=Status_list,attrs={'id': 'Status', 'class': 'form-control-new'}))
    TP_Cat = forms.CharField(label="TP_Cat", max_length=100, widget=forms.Select(choices=TP_Cat_list, attrs={'id': 'TP_Cat','class': 'form-control-new'}))
    # TP_Cat = forms.CharField(label="TP_Cat", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Trial_Run_Type = forms.CharField(label="Trial_Run_Type", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    TP_Vendor = forms.CharField(label="TP_Vendor", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    TP_Key_Parameter = forms.CharField(label="TP_Key_Parameter", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Lenovo_TP_PN = forms.CharField(label="Lenovo_TP_PN", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Compal_TP_PN = forms.CharField(label="Compal_TP_PN", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Issue_Link = forms.CharField(label="Issue_Link", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Remark = forms.CharField(label="Remark", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Attend_Time = forms.CharField(label="Attend_Time", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    ReTest_Attend_Time = forms.CharField(label="ReTest_Attend_Time", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    TestOwner = forms.CharField(label="TestOwner", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Month = forms.CharField(label="Month", max_length=100, widget=forms.Select(choices=Month_list,attrs={'id': 'Month', 'class': 'form-control-new'}))
    # Test_Start = forms.CharField(label="Test_Start", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Test_Start = forms.DateField(label="Test_Start", required=True, widget=forms.DateTimeInput(
        attrs={'class': 'form-control-new', 'type': 'text', 'readonly': "readonly",
               "onclick": "fPopCalendar(event,this,this)"}))
    # Test_End = forms.CharField(label="Test_End", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Test_End = forms.DateField(label="Test_End", required=True, widget=forms.DateTimeInput(
        attrs={'class': 'form-control-new', 'type': 'text', 'readonly': "readonly",
               "onclick": "fPopCalendar(event,this,this)"}))
