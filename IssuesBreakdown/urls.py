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

app_name = 'IssuesBreakdown'

urlpatterns = [

    path('IssuesBreakdown_edit/', views.IssuesBreakdown_edit, name='IssuesBreakdown_edit'),
    path('IssuesBreakdown_Summary/', views.IssuesBreakdown_Summary, name='IssuesBreakdown_Summary'),

]
