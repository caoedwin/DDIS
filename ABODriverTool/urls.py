from django.urls import path
# 引入views.py
from . import views

app_name = 'ABODriverTool'

urlpatterns = [

    path('ABODriverList_upload/', views.ABODriverList_upload, name='ABODriverList_upload'),

    path('ABODriverList_edit/', views.ABODriverList_edit, name='ABODriverList_edit'),

    path('ABODriverList_search/', views.ABODriverList_search, name='ABODriverList_search'),

    path('ABOToolList_upload/', views.ABOToolList_upload, name='ABOToolList_upload'),

    path('ABOToolList_edit/', views.ABOToolList_edit, name='ABOToolList_edit'),

    path('ABOToolList_search/', views.ABOToolList_search, name='ABOToolList_search'),


]