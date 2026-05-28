# PCRList/urls.py
from django.urls import path
from . import views

app_name = 'PCRList'

urlpatterns = [
    # 页面路由
    path('Summary/', views.pcr_list_page, name='pcr_list_page'),

    # API 路由
    path('api/list/', views.pcr_list_api, name='pcr_list_api'),
    path('api/statistics/', views.pcr_statistics_api, name='pcr_statistics_api'),
    path('api/create/', views.pcr_create_api, name='pcr_create_api'),
    path('api/update/', views.pcr_update_api, name='pcr_update_api'),
    path('api/delete/', views.pcr_delete_api, name='pcr_delete_api'),
    path('api/upload_excel/', views.pcr_upload_excel_api, name='pcr_upload_excel_api'),
]