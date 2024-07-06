from django.urls import path
from . import views
app_name = 'SpecDownload'
urlpatterns = [


    path('SpecDownload-summary/', views.SpecDownload_summary, name='SpecDownload_summary'),


]