from django.urls import path
# 引入views.py
from . import views

app_name = 'QIL'

urlpatterns = [

    path('QIL_add/', views.QIL_add, name='QIL_add'),
    path('QIL_search/', views.QIL_search, name='QIL_search'),
    path('QIL_edit/', views.QIL_edit, name='QIL_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('QIL_projectresult/', views.QIL_projectresult, name='QIL_projectresult'),
    path('QIL_searchbyproject/', views.QIL_searchbyproject, name='QIL_searchbyproject'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),


]