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

app_name = 'LowLightList'

urlpatterns = [

    path('LowLightList_edit/', views.LowLightList_edit, name='LowLightList_edit'),

]
