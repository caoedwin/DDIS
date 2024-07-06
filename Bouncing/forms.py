from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField


class Bouncing(forms.Form):
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    A_Cover_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('Mg_AL', 'Mg_AL'),
        ('Plasttic', 'Plasttic'),
        ('AL', 'AL'),
    )
    C_Cover_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('Mg_AL', 'Mg_AL'),
        ('Plasttic', 'Plasttic'),
        ('AL', 'AL'),
    )
    D_Cover_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('Mg_AL', 'Mg_AL'),
        ('Plasttic', 'Plasttic'),
        ('AL', 'AL'),
    )
    Customer = forms.CharField(max_length=20, widget=forms.Select(choices=Customer_list))
    A_cover = forms.CharField(max_length=20,
                              widget=forms.Select(choices=A_Cover_list, attrs={'class': 'form-control-new'}))
    C_cover = forms.CharField(max_length=20, widget=forms.Select(choices=C_Cover_list,attrs={'class':'form-control-new'}))
    D_cover = forms.CharField(max_length=20, widget=forms.Select(choices=D_Cover_list,attrs={'class':'form-control-new'}))
    Project = forms.CharField(label="project", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'projectStyle'}))
    HS=forms.CharField(label="Object",max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Push_min = forms.CharField(label="push", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Push_max=forms.CharField(label="push",max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    PV_L_min=forms.FloatField(label="PV_L_min", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    PV_R_min=forms.FloatField(label="PV_R_min", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    D_L_min=forms.FloatField(label="D_L_min", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    D_R_min=forms.FloatField(label="D_R_min", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    PV_L_max = forms.FloatField(label="PV_L_max", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    PV_R_max = forms.FloatField(label="PV_R_max", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    D_L_max = forms.FloatField(label="D_L_max", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    D_R_max = forms.FloatField(label="D_R_max", required=True, widget=forms.NumberInput(attrs={'class': 'form-control-new'}))
    def editor_check(self):
        print('tt')
        value = self.cleaned_data['HS']
        if len(value) < 6:
            # 自定义规则不抛异常表示通过
            self.add_error('HS', 'min 6字符')
            raise ValidationError('小于6')
        else:
            return value