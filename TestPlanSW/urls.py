from django.urls import path
# 引入views.py
from . import views

app_name = 'TestPlanSW'

urlpatterns = [
    #
    # path('CDM-upload/', views.CDM_upload, name='CDM_upload'),
    #
    path('TestPlanSW-edit/', views.TestPlanSW_Edit, name='TestPlanSW_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('TestPlanSW-search/', views.TestPlanSW_search, name='TestPlanSW_search'),
    path('ItemSW-upload/', views.ItemSW_upload, name='ItemSW_upload'),
    path('TestPlanSW-summary/', views.TestPlanSW_summary, name='TestPlanSW_summary'),
    path('TestPlanSW-search-AIO/', views.TestPlanSW_search_AIO, name='TestPlanSW_search_AIO'),
    path('TestPlanSW-edit-AIO/', views.TestPlanSW_Edit_AIO, name='TestPlanSW_edit_AIO'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),


]