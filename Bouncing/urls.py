from django.urls import path
# 引入views.py
from . import views

app_name = 'Bouncing'

urlpatterns = [

    path('Bouncing-upload/', views.bouncingtest_upload, name='bouncingtest_upload'),

    path('Bouncing-edit/', views.bouncingtest_edit, name='bouncingtest_edit'),
    # path('Bouncing-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('Bouncing-search/', views.bouncingtest_search, name='bouncingtest_search'),
    path('Bouncing-export/', views.bouncingtest_export, name='bouncingtest_export'),


]