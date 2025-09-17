from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
app_name = 'CommonFiles'
urlpatterns = [

    path('CommonFiles_edit/', views.CommonFiles_edit, name='CommonFiles_edit'),
    path('ppt_preview/<int:file_id>/', views.ppt_preview, name='ppt_preview'),
]