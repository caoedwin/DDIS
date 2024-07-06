from django.urls import path
# 引入views.py
from . import views

app_name = 'MQM'

urlpatterns = [

    path('MQM_upload/', views.MQM_upload, name='MQM_upload'),

    path('MQM_edit/', views.MQM_edit, name='MQM_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('MQM_search/', views.MQM_search, name='MQM_search'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),


]