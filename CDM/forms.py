from django import forms
# from django.contrib.admin import widgets
# from django.core.validators import ValidationError
# from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
# from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField

class DateInput(forms.DateInput):
    input_type = 'date'

class CDMform(forms.Form):
    Customer_list = (
        # ('Select Customer', 'Select Customer'),
        ('',''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )
    Phase_list = (
        # ('Select Phase', 'Select Phase'),
        ('', ''),
        ('B(FVT)', 'B(FVT)'),
        ('C(SIT)', 'C(SIT)'),
        ('INV', 'INV'),
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
    Customer = forms.CharField(label="客户",max_length=20,widget=forms.Select(choices=Customer_list,attrs={'class': 'form-control-new', 'style': 'height: 30px;width:100px',}))
    Project = forms.CharField(label="机种",max_length=20,widget=forms.TextInput(attrs={'size':10}))
    # Phase = forms.CharField(max_length=20,widget=forms.Select(choices=Phase_list))
    # SS_Data_1 =  forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'date'}))#IE edge不兼容
    # SS_Data =  forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'text','readonly':"readonly",'id':'mydatepicker2'}))#带默认值value无法使用
    SS_Data = forms.DateField(widget=forms.DateTimeInput(attrs={'type': 'text','readonly':"readonly","onclick":"fPopCalendar(event,this,this)"}))
    # A_cover_Material = forms.CharField(label="A件", max_length=50, widget=forms.Select(choices=A_Cover_list, attrs={'class': 'form-control-new', 'style': 'height: 30px;width:200px',}))
    # C_cover_Material = forms.CharField(label="C件",max_length=50, widget=forms.Select(choices=C_Cover_list, attrs={'class': 'form-control-new', 'style': 'height: 30px;width:200px',}))
    # D_cover_Material = forms.CharField(label="D件",max_length=50, widget=forms.Select(choices=D_Cover_list, attrs={'class': 'form-control-new', 'style': 'height: 30px;width:200px',}))
    A_cover_Material = forms.CharField(label="A件", max_length=50, widget=forms.TextInput(attrs={'size':20}))
    C_cover_Material = forms.CharField(label="C件", max_length=50, widget=forms.TextInput(attrs={'size':20}))
    D_cover_Material = forms.CharField(label="D件", max_length=50, widget=forms.TextInput(attrs={'size':20}))
    SKU_NO = forms.CharField(max_length=10,widget=forms.TextInput(attrs={'size':10}))
    L1 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L2 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L3 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L4 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L5 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L6 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    L7 = forms.FloatField(widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    # Ave = forms.FloatField(label="均值",widget=forms.NumberInput(attrs={'size':5,'type': 'text','onkeyup':"only_num(this)", 'onblur':"only_num(this})"}),error_messages={"required": "输入不对！！"},)
    Conclusion = forms.CharField(label="结论",widget=forms.Textarea(attrs={'style': 'height: 200px;width:770px'}))