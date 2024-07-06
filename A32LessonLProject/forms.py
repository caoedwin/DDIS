from django import forms
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
# from captcha.fields import CaptchaField
from DjangoUeditor.forms import UEditorField #头部增加这行代码导入UEditorField


class A32lessonlearn(forms.Form):
    choosecat = (
        ("", ""),
        ("Reliability", "Reliability"),
        ("Compatibility", "Compatibility")
    )
    choosestatus = [
        # ("", ""),
        ("active", "active"),
        ("inactive", "inactive")
    ]
    Category = forms.CharField(label="Category", max_length=100,required=True,widget=forms.Select(choices=choosecat))
    Object = forms.CharField(label="Object", max_length=100, required=True,widget=forms.TextInput(attrs={'class': 'form-control','size':60}))
    # Phase = forms.ModelChoiceField(queryset=Phase, empty_label='Choose Phase')
    Symptom = forms.CharField(label="Symptom", max_length=1000, required=True,widget=forms.TextInput(attrs={'class': 'form-control','size':60}))
    Reproduce_Steps = forms.CharField(label="Reproduce_Steps", max_length=10000, required=False, widget=forms.Textarea(attrs={'class': 'form-control','style': 'height: 150px;width:900px','cols': 60, 'rows': 15}))
    Root_Cause = forms.CharField(label="Root_Cause", max_length=10000, required=True,widget=forms.Textarea(attrs={'class': 'form-control','style': 'height: 150px;width:900px','cols': 60, 'rows': 15}))
    # Root_Cause = UEditorField('Root_Cause', width=900, height=150,
    #                           toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                           upload_settings={"imageMaxSize": 1204000, 'videoPathFormat': "videos/"},
    #                           settings={}, command=None  # , blank=True
    #                           )
    # # Usernamef = forms.CharField(label="Username", max_length=128) #定义了但是HTML没有上传，会造成is_valid一直是Faulse.
    Solution = forms.CharField(label="Solution", max_length=10000, required=True, widget=forms.Textarea(attrs={'class': 'form-control','style': 'height: 150px;width:900px','cols': 60, 'rows': 15}))
    # Solution = UEditorField('Solution/Action', width=900, height=300,
    #                         toolbars="full", imagePath="upimg/", filePath="upfile/",
    #                         upload_settings={"imageMaxSize": 1204000,'videoPathFormat': "videos/"},
    #                         settings={}, required=True,command=None#, blank=True
    #                         )
    Action = forms.CharField(label="Action", max_length=10000, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control', 'style': 'height: 150px;width:900px', 'cols': 60, 'rows': 15}))
    Status = forms.CharField(label="Status", max_length=100, required=True, widget=forms.Select(choices=choosestatus))

    def editor_check(self):
        print ('tt')
        value=self.cleaned_data['Solution']
        if value=='<p></p>':
            # 自定义规则不抛异常表示通过
            self.add_error('Solution','Solution/Action 不能为空')
            raise ValidationError('Solution 不能为空')
        else:
            return value
    def editor_check(self):
        print ('tt')
        value=self.cleaned_data['Object']
        if len(value)<6:
            # 自定义规则不抛异常表示通过
            self.add_error('Object','min 6字符')
            raise ValidationError('小于6')
        else:
            return value
