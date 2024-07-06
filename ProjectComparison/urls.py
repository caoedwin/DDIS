from django.urls import path, include
# 引入views.py
from . import views
from rest_framework_jwt.views import obtain_jwt_token

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = routers.DefaultRouter()
from django.urls import path, include

app_name = 'ProjectComparison'

urlpatterns = [

    path('ProjectComparison_Edit/', views.ProjectComparison_Edit, name='ProjectComparison_Edit'),
    path('ProjectComparison_Summary/', views.ProjectComparison_Summary, name='ProjectComparison_Summary'),

]
