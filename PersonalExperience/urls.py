from django.urls import path
from . import views
app_name = 'PersonalExperience'
urlpatterns = [


    path('NPI-upload/', views.NPI_upload, name='NPI_upload'),
    path('INV-upload/', views.INV_upload, name='INV_upload'),
    path('OSR-upload/', views.OSR_upload, name='OSR_upload'),
    path('My-application/', views.My_application, name='My_application'),
    path('My-approve/', views.My_approve, name='My_approve'),
    path('Summary/', views.Summary, name='Summary'),
]