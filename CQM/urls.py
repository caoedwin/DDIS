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
from .authentication import MyTokenObtainPairView

app_name = 'CQM'

urlpatterns = [

    path('CQM_upload/', views.CQM_upload, name='CQM_upload'),

    path('CQM_edit/', views.CQM_edit, name='CQM_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('CQM_search/', views.CQM_search, name='CQM_search'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),
    # path('apilogin/', views.LoginView.as_view(), name='apilogin'), # 用于登陆

    # 使用jwt自带的登录视图
    # path('', include(routers.urls)),
    # jwt
    path('api/login/', MyTokenObtainPairView.as_view(), name='login'),
    # path('test/', views.TestView.as_view(), name='test'),
    # jwt
    # path('api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('login/', obtain_jwt_token),
    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('CQMapi/', views.CQMSeriView.as_view(), name='CQMapi'),# 用于认证测试
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('api/token/', CustomJwtTokenView.as_view(), name='token_obtain_pair'),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
