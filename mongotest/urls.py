from django.urls import path
# 引入views.py
from . import views

app_name = 'mongotest'

urlpatterns = [

    path('mongotest-upload/', views.ToolListmongo.as_view(), name='mongotest_upload'),#用rest_framework要加as_view()
    # path('mongotest-upload/', views.addInvitations, name='mongotest_upload'),

]
# from rest_framework.routers import DefaultRouter
#
# urlpatterns = []  # 路由列表
# router = DefaultRouter()  # 可以处理视图的路由器
# router.register('mongotest', views.FirstMongoView,basename='')  # 向路由器中注册视图集
# urlpatterns += router.urls  # 将路由器中的所有路由信息追加到Django的路由列表中