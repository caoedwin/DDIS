from django.urls import path
from . import views
app_name = 'INVGantt'
urlpatterns = [
path('INVGantt-upload/', views.INVGantt_upload, name='INVGantt_upload'),

    path('INVGantt-search/', views.INVGantt_search, name='INVGantt_search'),
    path('INVGantt-searchByProject/', views.INVGantt_searchByProject, name='INVGantt_searchByProject'),

    path('INVGantt-edit/', views.INVGantt_edit, name='INVGantt_edit'),

    path('INVGantt-summary/', views.INVGantt_summary, name='INVGantt_summary'),

    path('INVGantt-top/', views.INVGantt_top, name='INVGantt_top'),
    path('INVGantSerire/', views.INVGantViewre, name='INVGantSerire'),
    path('apilogin/', views.LoginView.as_view(), name='apilogin'), # 用于登陆
    path('INVGantSeriv/', views.TestView.as_view(), name='INVGantSeriv'),# 用于认证测试
]

from rest_framework.routers import DefaultRouter
# 定义视图处理的路由器
router = DefaultRouter()
router.register('INVGantSeri',views.INVGantView,)  # 类试图在路由器中注册视图集



urlpatterns += router.urls