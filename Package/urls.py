from django.urls import path
# 引入views.py
from . import views

app_name = 'Bouncing'

urlpatterns = [

    path('Package-upload/', views.Package_upload, name='Package_upload'),

    path('Package-edit/', views.package_edit, name='Package_edit'),
    # path('Bouncing-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('Package-search/', views.Package_search, name='Package_search'),
    path('Package-export/', views.Package_export, name='Package_export'),


]