from django.urls import path
# 引入views.py
from . import views

app_name = 'TestPlanME'

urlpatterns = [
    #
    # path('CDM-upload/', views.CDM_upload, name='CDM_upload'),
    #
    path('TestPlanME-summary/', views.TestPlanME_Summary, name='TestPlanME_Summary'),
    path('TestPlanME-edit/', views.TestPlanME_Edit, name='TestPlanME_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('TestPlanME-search/', views.TestPlanME_search, name='TestPlanME_search'),
    # path('TestPlanME-Summary/', views.TestPlanME_summary, name='TestPlanME_summary'),
    path('ItemME-upload/', views.ItemME_upload, name='ItemME_upload'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),


]