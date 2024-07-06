from django import forms

class Issue_Notes_F(forms.Form):
    Customer_list = (
        ('', ''),
        ('C38(NB)', 'C38(NB)'),
        ('C38(AIO)', 'C38(AIO)'),
        ('T88(AIO)', 'T88(AIO)'),
        ('A39', 'A39'),
        ('Others', 'Others'),
    )


    Customer = forms.CharField(max_length=100, widget=forms.Select(choices=Customer_list, attrs={'class':'form-control-new'}))
    Project_Code = forms.CharField(label="Project_Code", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Platform = forms.CharField(label="Platform", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    TDMS_NO = forms.CharField(label="TDMS_NO", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Issue_Title = forms.CharField(label="Issue_Title", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Root_Cause = forms.CharField(label="Root_Cause", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    Solution = forms.CharField(label="Solution", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
    PL = forms.CharField(label="PL", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control-new'}))
