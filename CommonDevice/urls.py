from django.urls import path
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
app_name = 'CommonDevice'
urlpatterns = [

    path('CommonDevice_edit/', views.CommonDevice_edit, name='CommonDevice_edit'),
]