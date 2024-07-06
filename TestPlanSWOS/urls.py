from django.urls import path
# 引入views.py
from . import views

app_name = 'TestPlanSWOS'

urlpatterns = [
    #
    # path('CDM-upload/', views.CDM_upload, name='CDM_upload'),
    #
    path('TestPlanSWOS-edit/', views.TestPlanSW_Edit, name='TestPlanSWOS_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('TestPlanSWOS-search/', views.TestPlanSW_search, name='TestPlanSWOS_search'),
    # path('ItemSW-upload/', views.ItemSW_upload, name='ItemSW_upload'),
    path('TestPlanSWOS-summary/', views.TestPlanSW_summary, name='TestPlanSWOS_summary'),
    path('TestPlanSWOS-search-AIO/', views.TestPlanSW_search_AIO, name='TestPlanSWOS_search_AIO'),
    path('TestPlanSWOS-edit-AIO/', views.TestPlanSW_Edit_AIO, name='TestPlanSWOS_edit_AIO'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),


]