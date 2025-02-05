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

app_name = 'MiscellaneousPurchases'

urlpatterns = [

    path('Budget/', views.Budget, name='Budget'),
    path('ReceiptAmount/', views.ReceiptAmount, name='SubscriptionStatus'),
    path('SubscriptionStatus/', views.SubscriptionStatus, name='SubscriptionStatus'),

]
