from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField


class package0(forms.Form):
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Phase_list = (
        # ('Select Phase', 'Select Phase'),
        # ('', ''),
        # ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        # ('INV', 'INV'),
        # ('Others', 'Others'),
    )
    Customer = forms.CharField(max_length=20, widget=forms.Select(choices=Customer_list,attrs={'class': 'customerdiv'}))
    Phase = forms.CharField(max_length=20, widget=forms.Select(choices=Phase_list,attrs={'class': 'phasediv'}))
    Project = forms.CharField(label="Project", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'projectdiv'}))
    degree = forms.CharField(label="degree", max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'degreediv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    duan = forms.CharField(label="duan", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'duandiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    zhong = forms.CharField(label="zhong", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'zhongdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    chang = forms.CharField(label="chang", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'changdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    left = forms.CharField(label="left", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'leftdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    right = forms.CharField(label="right", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'rightdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    top = forms.CharField(label="top", max_length=25, required=True, widget=forms.TextInput(attrs={'class': 'topdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    bottom = forms.CharField(label="bottom", max_length=25, required=True, widget=forms.TextInput(attrs={'class': 'bottomdiv','size':7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    zheng = forms.CharField(label="zheng", max_length=25, required=True, widget=forms.TextInput(attrs={'class': 'zhengdiv', 'size': 7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    fan = forms.CharField(label="fan", max_length=25, required=True,widget=forms.TextInput(attrs={'class': 'fandiv', 'size': 7,'onkeyup':"only_num(this)", 'onblur':"only_num(this})"}))
    Pattern = forms.CharField(label="pattern", max_length=30,required=True,widget=forms.TextInput(attrs={'size': '143'}))

    def editor_check(self):
        print('tt')
        value = self.cleaned_data['HS']
        if len(value) < 6:
            # 自定义规则不抛异常表示通过
            self.add_error('HS', 'min 6字符')
            raise ValidationError('小于6')
        else:
            return value