from django.urls import path
# 引入views.py
from . import views

app_name = 'CDM'

urlpatterns = [

    path('CDM-upload/', views.CDM_upload, name='CDM_upload'),

    path('CDM-edit/', views.CDM_edit, name='CDM_edit'),
    path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('CDM-search/', views.CDM_search, name='CDM_search'),
    path('CDM-export/', views.CDM_export, name='CDM_search'),


]