from django import forms

class CQM_F(forms.Form):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('T89(NB)', 'T89(NB)'),
        ('C85', 'C85'),
        ('A39', 'A39'),
        ('Others', 'Others'),
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
        ('Not Build', 'Not Build')
    )
    Material_Group_list=(
        ('', ''),
        ('Active_Pen', 'Active_Pen'),
        ('Adapter', 'Adapter'),
        ('Battery', 'Battery'),
        ('Camera', 'Camera'),

        ('CPU', 'CPU'),
        ('EMMC', 'EMMC'),
        ('Finger_Print', 'Finger_Print'),
        ('HDD', 'HDD'),
        ('Keyboard', 'Keyboard'),

        ('Memory', 'Memory'),
        ('ODD', 'ODD'),
        ('Panel', 'Panel'),
        ('Power_Cord', 'Power_Cord'),
        ('Speaker', 'Speaker'),
        ('SSD', 'SSD'),
        ('Touch_Pad', 'Touch_Pad'),
        ('TPM', 'TPM'),
        ('TCM', 'TCM'),
        ('UFS', 'UFS'),
        ('VRAM', 'VRAM'),
        ('VGA', 'VGA'),
        ('WLAN', 'WLAN'),
        ('WWAN', 'WWAN'),
        ('Fan', 'Fan'),
        ('MIC', 'MIC'),
        ('Mouse', 'Mouse'),
        ('Stand', 'Stand'),
        ('Thermal module', 'Thermal module'),
        ('Wireless KB/MS', 'Wireless KB/MS'),
        ('WLAN+BT combo', 'WLAN+BT combo'),
        ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class':'form-control-new'}))
    Project = forms.CharField(label="project", max_length=100,required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Phase = forms.CharField(label="Phase", max_length=100,widget=forms.Select(choices=Phase_list, attrs={'class': 'form-control-new'}))
    Material_Group = forms.CharField(label="Material_Group", max_length=100, widget=forms.Select(choices=Material_Group_list,attrs={'id': 'Material_Group','class': 'form-control-new'}))
    # Material_Group = forms.ChoiceField()
    Keyparts = forms.CharField(label="Keyparts", max_length=1000, widget=forms.Textarea(attrs={'id': 'Keyparts','class': 'form-control-new'}))
    Character = forms.CharField(label="Character", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    PID = forms.CharField(label="PID", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    VID = forms.CharField(label="VID", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    HW = forms.CharField(label="HW", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    FW = forms.CharField(label="FW", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Supplier = forms.CharField(label="Supplier", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    R1_PN_Description = forms.CharField(label="R1_PN_Description", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Compal_R1_PN = forms.CharField(label="Compal_R1_PN", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Compal_R3_PN = forms.CharField(label="Compal_R3_PN", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    R1S = forms.CharField(label="R1S", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Reliability = forms.CharField(label="Reliability", max_length=100, required=False, widget=forms.Select(choices=Testresult_list,attrs={'id':'Reliability','class': 'form-control-new'}))
    Compatibility = forms.CharField(label="Compatibility", max_length=100, required=False, widget=forms.Select(choices=Testresult_list,attrs={'id':'Compatibility','class': 'form-control-new'}))
    Testresult = forms.CharField(label="Testresult", max_length=100, required=False, widget=forms.TextInput(attrs={'readonly':'true','id':'Testresult','class': 'form-control-new'}))
    ESD = forms.CharField(label="ESD", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    EMI = forms.CharField(label="EMI", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    RF = forms.CharField(label="RF", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    PMsummary = forms.CharField(label="PMsummary", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Controlrun = forms.CharField(label="Controlrun", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Comments = forms.CharField(label="Comments", max_length=500, required=False,  widget=forms.Textarea(attrs={'class': 'form-control-new'}))