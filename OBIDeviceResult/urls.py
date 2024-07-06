from django.urls import path
# 引入views.py
from . import views

app_name = 'OBIDeviceResult'

urlpatterns = [

    # path('OBIDeviseResult_upload/', views.OBIDeviseResult_upload, name='OBIDeviseResult_upload'),

    path('OBIDeviceResult_edit/', views.OBIDeviceResult_edit, name='OBIDeviceResult_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('OBIDeviceResult_search/', views.OBIDeviceResult_search, name='OBIDeviceResult_search'),
    path('OBIDeviceResult_options/', views.OBIDeviceResult_options, name='OBIDeviceResult_options'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),



]