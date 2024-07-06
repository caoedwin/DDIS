from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField


class DriverList(forms.Form):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Phase_list = (

        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class': 'customerdiv'}))
    Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    Phase0 = forms.CharField(label="Phase0", max_length=100,widget=forms.Select(choices=Phase_list, attrs={'class': 'phasediv'}))
    Name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'namediv'}))
    Function0 = forms.CharField(label="Function0", max_length=100, widget=forms.TextInput(attrs={'class': 'functiondiv'}))
    Vendor = forms.CharField(label="Vendor", max_length=100, widget=forms.TextInput(attrs={'class': 'vendordiv'}))
    Version = forms.CharField(label="Version", max_length=100, widget=forms.TextInput(attrs={'class': 'versiondiv'}))
    Image = forms.CharField(label="Image", max_length=100, widget=forms.TextInput(attrs={'class': 'imagediv'}))
    Driver = forms.CharField(label="Driver", max_length=100, widget=forms.TextInput(attrs={'class': 'driverdiv'}))

class ToolList(forms.Form):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Phase_list = (
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
        ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class': 'customerdiv'}))
    Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    Phase0 = forms.CharField(label="Phase0", max_length=100,widget=forms.Select(choices=Phase_list, attrs={'class': 'phasediv'}))
    Vendor = forms.CharField(label="Vendor", max_length=100, widget=forms.TextInput(attrs={'class': 'vendordiv'}))
    Version = forms.CharField(label="Version", max_length=100, widget=forms.TextInput(attrs={'class': 'versiondiv'}))
    ToolName = forms.CharField(label="ToolName", max_length=100, widget=forms.TextInput(attrs={'class': 'toolnamediv'}))
    TestCase = forms.CharField(label="TestCase", max_length=100, widget=forms.TextInput(attrs={'class': 'testcasediv'}))

class MQM_F(forms.Form):
    # PartsSelect_list = (
    #     # ('Select Customer', 'Select Customer'),
    #     ('', ''),
    #     ('C38(NB)', 'C38(NB)'),
    #     ('C38(AIO)', 'C38(AIO)'),
    #     ('A39', 'A39'),
    #     ('Others', 'Others'),
    #
    # )
    SourcePriority_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('M', 'M'),
        ('S1', 'S1'),
        ('S2', 'S2'),

    )
    State_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('AP/AL', 'AP/AL'),
    )
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    ReliabilityB_list = (
        ('', ''),
        ('QS', 'QS'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('QT', 'QT'),
        ('QF', 'QF'),
        ('QF_L', 'QF_L'),
        ('DisQ', 'DisQ'),
        ('Drop', 'Drop'),
        ('Not Build', 'Not Build')
    )
    CompatibilityB_list = (
        ('', ''),
        ('QS', 'QS'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('QT', 'QT'),
        ('QF', 'QF'),
        ('QF_L', 'QF_L'),
        ('DisQ', 'DisQ'),
        ('Drop', 'Drop'),
        ('Not Build', 'Not Build')
    )
    ReliabilityC_list = (
        ('', ''),
        ('QS', 'QS'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('QT', 'QT'),
        ('QF', 'QF'),
        ('QF_L', 'QF_L'),
        ('DisQ', 'DisQ'),
        ('Drop', 'Drop'),
        ('Not Build', 'Not Build')
    )
    CompatibilityC_list = (
        ('', ''),
        ('QS', 'QS'),
        ('Qd_L', 'Qd_L'),
        ('Qd_C', 'Qd_C'),
        ('QT', 'QT'),
        ('QF', 'QF'),
        ('QF_L', 'QF_L'),
        ('DisQ', 'DisQ'),
        ('Drop', 'Drop'),
        ('Not Build', 'Not Build')
    )
    # Project_list = (
    #     # ('Select Customer', 'Select Customer'),
    #     ('', ''),
    # )
    # Phase_list = (
    #     # ('Select Customer', 'Select Customer'),
    #     ('', ''),
    #     ('B(FVT)', 'B(FVT)'),
    #     ('C(SIT)', 'C(SIT)'),
    #     ('INV', 'INV'),
    #     ('Others', 'Others'),
    # )
    # PartsSelect = forms.CharField(max_length=20, widget=forms.Select(choices=PartsSelect_list,attrs={'class':'form-control-new'}))
    SourcePriority = forms.CharField(max_length=20, widget=forms.Select(choices=SourcePriority_list,attrs={'class':'form-control-new'}))
    Customer = forms.CharField(max_length=20, widget=forms.Select(choices=Customer_list,attrs={'height':'40px','class': 'form-control-new'}))
    Project = forms.CharField(max_length=20, widget=forms.Textarea(attrs={'height':'40px','class': 'form-control-new'}))
    # Phase = forms.CharField(max_length=20,widget=forms.Select(choices=Phase_list, attrs={'class': 'form-control-new'}))
    Status = forms.CharField(max_length=20, widget=forms.Select(choices=State_list,attrs={'class':'form-control-new'}))
    #Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    Category = forms.CharField(label="Category", required=True, widget=forms.Textarea(attrs={'class': 'form-control-new'}))
    Name = forms.CharField(label="Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Vendor=forms.CharField(label="Object",max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    CompalPN = forms.CharField(label="push", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Description=forms.CharField(label="Description", required=False, widget=forms.Textarea(attrs={'class': 'form-control-new'}))
    Qty=forms.IntegerField(label="PV_L_min", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    Location = forms.CharField(label="Location", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    VendorPN = forms.CharField(label="VendorPN", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Controlrun = forms.CharField(label="Controlrun", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Comments = forms.CharField(label="Comments", max_length=500, required=False,widget=forms.Textarea(attrs={'class': 'form-control-new'}))
    DataCodeB = forms.CharField(label="DataCodeB", max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    ReliabilityB = forms.CharField(label="ReliabilityB", max_length=100, required=False,widget=forms.Select(choices=ReliabilityB_list,attrs={'id':'ReliabilityB','class': 'form-control-new'}))
    CompatibilityB = forms.CharField(label="CompatibilityB", max_length=100, required=False,widget=forms.Select(choices=CompatibilityB_list,attrs={'id':'CompatibilityB','class': 'form-control-new'}))
    ResultforB = forms.CharField(label="ResultforB", max_length=100, required=False,widget=forms.TextInput(attrs={'readonly':'true','id':'ResultforB','class': 'form-control-new'}))
    ESDB = forms.CharField(label="ESDB", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    EMIB = forms.CharField(label="EMIB", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    RFB = forms.CharField(label="RFB", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    DataCodeC = forms.CharField(label="DataCodeC", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    ReliabilityC = forms.CharField(label="ReliabilityC", max_length=100, required=False,widget=forms.Select(choices=ReliabilityC_list,attrs={'id':'ReliabilityC','class': 'form-control-new'}))
    CompatibilityC = forms.CharField(label="CompatibilityC", max_length=100, required=False,widget=forms.Select(choices=CompatibilityC_list,attrs={'id':'CompatibilityC','class': 'form-control-new'}))
    ResultforC = forms.CharField(label="ResultforC", max_length=100, required=False,widget=forms.TextInput(attrs={'readonly':'true','id':'ResultforC','class': 'form-control-new'}))
    ESDC = forms.CharField(label="ESDC", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    EMIC = forms.CharField(label="EMIC", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    RFC = forms.CharField(label="RFC", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    DataCodeINV = forms.CharField(label="DataCodeINV", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    ReliabilityINV = forms.CharField(label="ReliabilityINV", max_length=100, required=False,widget=forms.Select(choices=ReliabilityC_list,attrs={'id': 'ReliabilityINV', 'class': 'form-control-new'}))
    CompatibilityINV = forms.CharField(label="CompatibilityINV", max_length=100, required=False,widget=forms.Select(choices=CompatibilityC_list, attrs={'id': 'CompatibilityINV','class': 'form-control-new'}))
    ResultforINV = forms.CharField(label="ResultforINV", max_length=100, required=False, widget=forms.TextInput(attrs={'readonly': 'true', 'id': 'ResultforINV', 'class': 'form-control-new'}))
    ESDINV = forms.CharField(label="ESDINV", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    EMIINV = forms.CharField(label="EMIINV", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    RFINV = forms.CharField(label="RFINV", max_length=100, required=False,widget=forms.TextInput(attrs={'class': 'form-control-new'}))

    def editor_check(self):
        print('tt')
        value = self.cleaned_data['HS']
        if len(value) < 6:
            # 自定义规则不抛异常表示通过
            self.add_error('HS', 'min 6字符')
            raise ValidationError('小于6')
        else:
            return value