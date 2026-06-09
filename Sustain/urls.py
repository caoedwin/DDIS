from django.urls import path
from . import views

app_name = 'sustain'

urlpatterns = [
    # 页面路由
    path('edit/', views.sustain_edit, name='sustain_edit'),
    path('summary/', views.sustain_summary, name='sustain_summary'),

    # API 接口
    path('api/get_customers/', views.get_customers, name='get_customers'),
    path('api/get_projects_by_customer/', views.get_projects_by_customer, name='get_projects_by_customer'),
    path('api/search_tasks/', views.search_tasks, name='search_tasks'),
    path('api/save_task/', views.save_task, name='save_task'),
    path('api/delete_task/', views.delete_task, name='delete_task'),
    path('api/upload_excel/', views.upload_excel, name='upload_excel'),
    path('api/batch_delete_tasks/', views.batch_delete_tasks, name='batch_delete_tasks'),
    path('api/summary_data/', views.summary_data, name='summary_data'),
]