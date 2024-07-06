from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField


class QIL_F(forms.Form):
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Status_list = (
        ('', ''),
        ('Closed', 'Closed'),
        ('Deleted', 'Deleted'),
        ('In Process', 'In Process'),
        ('Lesson Learn', 'Lesson Learn'),
        ('Open', 'Open'),
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
    Product= forms.CharField(label="Product", max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Customer = forms.CharField(max_length=20, widget=forms.Select(choices=Customer_list,attrs={'class': 'form-control-new'}))
    QIL_No = forms.CharField(label="QIL_No", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Issue_Description=forms.CharField(label="Issue_Description", required=True, widget=forms.Textarea(attrs={'class': 'form-control-new'}))
    Root_Cause=forms.CharField(label="Root_Cause", required=True, widget=forms.Textarea(attrs={'class': 'form-control-new'}))
    Status = forms.CharField(max_length=20, widget=forms.Select(choices=Status_list,attrs={'class':'form-control-new'}))
    Creator = forms.CharField(label="Creator", max_length=100, required=True,
                              widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Created_On = forms.DateField(label="Creator", required=True, widget=forms.DateTimeInput(
        attrs={'class': 'form-control-new', 'type': 'text', 'readonly': "readonly",
               "onclick": "fPopCalendar(event,this,this)"}))


def editor_check(self):
        # print('tt')
        value = self.cleaned_data['HS']
        if len(value) < 6:
            # 自定义规则不抛异常表示通过
            self.add_error('HS', 'min 6字符')
            raise ValidationError('小于6')
        else:
            return value