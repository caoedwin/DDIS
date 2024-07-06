from django.urls import path
# 引入views.py
from . import views

app_name = 'ABOTestPlan'

urlpatterns = [

    path('ABOTestPlan_summary/', views.ABOTestPlan_summary, name='ABOTestPlan_summary'),
    path('ABOTestPlan_edit/', views.ABOTestPlan_edit, name='ABOTestPlan_edit'),
    path('ABOTestPlan_search/', views.ABOTestPlan_search, name='ABOTestPlan_search'),


]