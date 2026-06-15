from django.urls import path
# 引入views.py
from . import views
from .views import (
    TestItemSWList, TestItemSWDetail,
    TestProjectSWList, TestProjectSWDetail,
    TestPlanSWList, TestPlanSWDetail,
    RetestItemSWList, RetestItemSWDetail,
    FFRTByRDList, FFRTByRDDetail,
    TestProjectSWAIOList, TestProjectSWAIODetail,
    TestPlanSWAIOList, TestPlanSWAIODetail,
)
# 导入认证视图
from .authentication import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView   # 可选


app_name = 'TestPlanSW'

urlpatterns = [
    #
    # path('CDM-upload/', views.CDM_upload, name='CDM_upload'),
    #
    path('TestPlanSW-edit/', views.TestPlanSW_Edit, name='TestPlanSW_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('TestPlanSW-search/', views.TestPlanSW_search, name='TestPlanSW_search'),
    path('ItemSW-upload/', views.ItemSW_upload, name='ItemSW_upload'),
    path('TestPlanSW-summary/', views.TestPlanSW_summary, name='TestPlanSW_summary'),
    path('TestPlanSW-search-AIO/', views.TestPlanSW_search_AIO, name='TestPlanSW_search_AIO'),
    path('TestPlanSW-edit-AIO/', views.TestPlanSW_Edit_AIO, name='TestPlanSW_edit_AIO'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),
    # 登录获取 Token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # 刷新 Token（可选）
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # API endpoints
    path('api/testitems/', TestItemSWList.as_view(), name='api_testitem_list'),
    path('api/testitems/<int:pk>/', TestItemSWDetail.as_view(), name='api_testitem_detail'),
    path('api/testprojects/', TestProjectSWList.as_view(), name='api_testproject_list'),
    path('api/testprojects/<int:pk>/', TestProjectSWDetail.as_view(), name='api_testproject_detail'),
    path('api/testplans/', TestPlanSWList.as_view(), name='api_testplan_list'),
    path('api/testplans/<int:pk>/', TestPlanSWDetail.as_view(), name='api_testplan_detail'),
    path('api/retestitems/', RetestItemSWList.as_view(), name='api_retestitem_list'),
    path('api/retestitems/<int:pk>/', RetestItemSWDetail.as_view(), name='api_retestitem_detail'),
    path('api/ffrtrd/', FFRTByRDList.as_view(), name='api_ffrtrd_list'),
    path('api/ffrtrd/<int:pk>/', FFRTByRDDetail.as_view(), name='api_ffrtrd_detail'),
    path('api/testprojects_aio/', TestProjectSWAIOList.as_view(), name='api_testproject_aio_list'),
    path('api/testprojects_aio/<int:pk>/', TestProjectSWAIODetail.as_view(), name='api_testproject_aio_detail'),
    path('api/testplans_aio/', TestPlanSWAIOList.as_view(), name='api_testplan_aio_list'),
    path('api/testplans_aio/<int:pk>/', TestPlanSWAIODetail.as_view(), name='api_testplan_aio_detail'),


]