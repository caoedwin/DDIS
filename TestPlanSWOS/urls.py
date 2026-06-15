from django.urls import path
# 引入views.py
from . import views
from .authentication import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    TestItemOSList, TestItemOSDetail,
    TestProjectOSList, TestProjectOSDetail,
    TestPlanOSList, TestPlanOSDetail,
    RetestItemOSList, RetestItemOSDetail,
    FFRTByRDOSList, FFRTByRDOSDetail,
    TestProjectOSAIOList, TestProjectOSAIODetail,
    TestPlanOSAIOList, TestPlanOSAIODetail,
)


app_name = 'TestPlanSWOS'

urlpatterns = [
    #
    # path('CDM-upload/', views.CDM_upload, name='CDM_upload'),
    #
    path('TestPlanSWOS-edit/', views.TestPlanSW_Edit, name='TestPlanSWOS_edit'),
    # path('CDM-update/<int:id>/', views.CDM_update, name='CDM_update'),
    path('TestPlanSWOS-search/', views.TestPlanSW_search, name='TestPlanSWOS_search'),
    # path('ItemSW-upload/', views.ItemSW_upload, name='ItemSW_upload'),
    path('TestPlanSWOS-summary/', views.TestPlanSW_summary, name='TestPlanSWOS_summary'),
    path('TestPlanSWOS-search-AIO/', views.TestPlanSW_search_AIO, name='TestPlanSWOS_search_AIO'),
    path('TestPlanSWOS-edit-AIO/', views.TestPlanSW_Edit_AIO, name='TestPlanSWOS_edit_AIO'),
    # path('CDM-export/', views.CDM_export, name='CDM_search'),

    # 新增 API 路由
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/testitems/', TestItemOSList.as_view(), name='api_testitem_list'),
    path('api/testitems/<int:pk>/', TestItemOSDetail.as_view(), name='api_testitem_detail'),
    path('api/testprojects/', TestProjectOSList.as_view(), name='api_testproject_list'),
    path('api/testprojects/<int:pk>/', TestProjectOSDetail.as_view(), name='api_testproject_detail'),
    path('api/testplans/', TestPlanOSList.as_view(), name='api_testplan_list'),
    path('api/testplans/<int:pk>/', TestPlanOSDetail.as_view(), name='api_testplan_detail'),
    path('api/retestitems/', RetestItemOSList.as_view(), name='api_retestitem_list'),
    path('api/retestitems/<int:pk>/', RetestItemOSDetail.as_view(), name='api_retestitem_detail'),
    path('api/ffrtrd/', FFRTByRDOSList.as_view(), name='api_ffrtrd_list'),
    path('api/ffrtrd/<int:pk>/', FFRTByRDOSDetail.as_view(), name='api_ffrtrd_detail'),
    path('api/testprojects_aio/', TestProjectOSAIOList.as_view(), name='api_testproject_aio_list'),
    path('api/testprojects_aio/<int:pk>/', TestProjectOSAIODetail.as_view(), name='api_testproject_aio_detail'),
    path('api/testplans_aio/', TestPlanOSAIOList.as_view(), name='api_testplan_aio_list'),
    path('api/testplans_aio/<int:pk>/', TestPlanOSAIODetail.as_view(), name='api_testplan_aio_detail'),


]