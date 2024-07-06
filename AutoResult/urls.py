from django.urls import path
# 引入views.py
from . import views

app_name = 'AutoResult'

urlpatterns = [

    path('AutoItem_edit/', views.AutoItem_edit, name='AutoItem_edit'),
    path('AutoResult_edit/', views.AutoResult_edit, name='AutoResult_edit'),
    path('AutoResult_search/', views.AutoResult_search, name='AutoResult_search'),
    path('AutoResult_summary/', views.AutoResult_summary, name='AutoResult_summary'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),



]