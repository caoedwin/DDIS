from django.urls import path
# 引入views.py
from . import views

app_name = 'ABOQIL'

urlpatterns = [

    path('ABOQIL_add/', views.ABOQIL_add, name='ABOQIL_add'),
    path('ABOQIL_search/', views.ABOQIL_search, name='ABOQIL_search'),
    path('ABOQIL_edit/', views.ABOQIL_edit, name='ABOQIL_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('ABOQIL_projectresult/', views.ABOQIL_projectresult, name='ABOQIL_projectresult'),
    path('ABOQIL_searchbyproject/', views.ABOQIL_searchbyproject, name='ABOQIL_searchbyproject'),


]