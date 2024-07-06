from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField

class ABODriverList(forms.Form):
    Customer_list = (
        ('', ''),
        ('T88(NB)', 'T88(NB)'),
        ('ABO', 'ABO'),
        ('Others', 'Others'),
    )
    Phase_list = (

        ('', ''),
        ('NPI', 'NPI'),
        ('19H1', '19H1'),
        ('19H2', '19H2'),
        ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class': 'customerdiv'}))
    Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    Phase0 = forms.CharField(label="Phase0", max_length=100,widget=forms.Select(choices=Phase_list, attrs={'class': 'phasediv'}))
    Name = forms.CharField(label="Name", max_length=100, widget=forms.TextInput(attrs={'class': 'namediv'}))
    Function = forms.CharField(label="Function", max_length=100, widget=forms.TextInput(attrs={'class': 'functiondiv'}))
    Vendor = forms.CharField(label="Vendor", max_length=100, widget=forms.TextInput(attrs={'class': 'vendordiv'}))
    Version = forms.CharField(label="Version", max_length=100, widget=forms.TextInput(attrs={'class': 'versiondiv'}))
    Bios = forms.CharField(label="Bios", max_length=100, widget=forms.TextInput(attrs={'class': 'biosdiv'}))
    Image = forms.CharField(label="Image", max_length=100, widget=forms.TextInput(attrs={'class': 'imagediv'}))
    Driver = forms.CharField(label="Driver", max_length=100, widget=forms.TextInput(attrs={'class': 'driverdiv'}))

class ABOToolList(forms.Form):
    Customer_list = (
        ('', ''),
        ('T88(NB)', 'T88(NB)'),
        ('ABO', 'ABO'),
        ('Others', 'Others'),
    )
    Phase_list = (
        ('', ''),
        ('NPI', 'NPI'),
        ('19H1', '19H1'),
        ('19H2', '19H2'),
        ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=100,widget=forms.Select(choices=Customer_list, attrs={'class': 'customerdiv'}))
    Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    Phase0 = forms.CharField(label="Phase0", max_length=100,widget=forms.Select(choices=Phase_list, attrs={'class': 'phasediv'}))
    Vendor = forms.CharField(label="Vendor", max_length=100, widget=forms.TextInput(attrs={'class': 'vendordiv'}))
    Version = forms.CharField(label="Version", max_length=100, widget=forms.TextInput(attrs={'class': 'versiondiv'}))
    ToolName = forms.CharField(label="ToolName", max_length=100, widget=forms.TextInput(attrs={'class': 'toolnamediv'}))
    TestCase = forms.CharField(label="TestCase", max_length=100, widget=forms.TextInput(attrs={'class': 'testcasediv'}))