from django.urls import path
# 引入views.py
from . import views

app_name = 'DriverTool'

urlpatterns = [

    path('DriverList_upload/', views.DriverList_upload, name='DriverList_upload'),

    path('DriverList_edit/', views.DriverList_edit, name='DriverList_edit'),

    path('DriverList_search/', views.DriverList_search, name='DriverList_search'),

    path('ToolList_upload/', views.ToolList_upload, name='ToolList_upload'),

    path('ToolList_edit/', views.ToolList_edit, name='ToolList_edit'),

    path('ToolList_search/', views.ToolList_search, name='ToolList_search'),


]