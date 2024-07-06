"""Reliability_Row_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path, include , re_path
from django.conf.urls.static import static
# from django.conf.urls import url, include
#留意上面这行比原来多了一个include
from django.views.static import serve
#导入静态文件模块
from django.conf import settings
#导入配置文件里的文件上传配置
from app01 import views
from ABOTestPlan import views as ABOviews
from django.conf.urls import url

from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.documentation import include_docs_urls
# import notifications.urls
urlpatterns = [
    # path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('admin/', admin.site.urls),
    # 实现了users和groups的API开发，但是我们可以发现，我们没有用户登录退出的按钮，以及权限设置（只有超级用户登录之后才可以看到列表和详情，非登录状态会显示没有权限查看）接下来我们对这两个地方进行优化：
    #
    # 1.
    # 为了显示登录退出按钮，在helloworld / urls.py里面加入
    # `url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), `因此helloworld / urls / py里面的内容如下：
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # path('api/token/', CustomJwtTokenView.as_view(), name='token_obtain_pair'),
    # url(r'^api-token-auth/', views.obtain_auth_token),
    # path(r'api-token-auth/', obtain_jwt_token),#貌似不需要数据库加Tokoen字段自带的auth_User
    # path(r'api-token-verify/', verify_jwt_token),
    # path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # url(r'^docs/', include_docs_urls(title='My API title')),
    path('docs/', include_docs_urls(title='接口文档')),
    path('ueditor/', include('DjangoUeditor.urls')), #添加DjangoUeditor的URL
    path(r'login/', views.login),
    path(r'', views.login),
    path(r'logout/', views.logout),
    path(r'Change_Password/', views.Change_Password),
    path(r'Change_Skin/', views.Change_Skin),
    path(r'index/', views.index),
    path(r'ttt/', views.ttt),
    path(r'ctest/', views.ctest),
    path(r'ProjectInfoSearch/', views.ProjectInfoSearch),
    path(r'FilesDownload/', views.FilesDownload),
    path(r'Navigation/', views.Navigation),
    path(r'Lesson_upload/', views.Lesson_upload),
    path(r'Lesson_edit/', views.Lesson_edit),
    path(r'Lesson_search/', views.Lesson_search),
    path(r'Lesson_export/', views.Lesson_export),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path(r'redit_Lesson/<int:id>/', views.Lesson_update,name='Lesson_update'),#html{%url%}中调用的是name
    path('CDM/', include('CDM.urls', namespace='CDM')),
    path('MQM/', include('MQM.urls', namespace='MQM')),
    path('CQM/', include('CQM.urls', namespace='CQM')),
    path('OBIDeviceResult/', include('OBIDeviceResult.urls', namespace='OBIDeviceResult')),
    path('Bouncing/', include('Bouncing.urls', namespace='Bouncing')),
    path('Package/', include('Package.urls', namespace='Package')),
    path('TestPlanME/', include('TestPlanME.urls', namespace='TestPlanME')),
    path('LessonProjectME/', include('LessonProjectME.urls', namespace='LessonProjectME')),
    path('QIL/', include('QIL.urls', namespace='QIL')),
    path('DriverTool/', include('DriverTool.urls', namespace='DriverTool')),
    path('TestPlanSW/', include('TestPlanSW.urls', namespace='TestPlanSW')),
    path('TestPlanSWOS/', include('TestPlanSWOS.urls', namespace='TestPlanSWOS')),
    path('AutoResult/', include('AutoResult.urls', namespace='AutoResult')),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),#增加此行
    re_path('^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),#增加此行
    path('Lesson/', include('LessonProjectME.urls', namespace='article')),
    path('mongotest/', include('mongotest.urls', namespace='mongotest')),
    path('INVGantt/', include('INVGantt.urls', namespace='INVGantt')),
    path('SpecDownload/', include('SpecDownload.urls', namespace='SpecDownload')),
    path('NonDQALesson/', include('NonDQALesson.urls', namespace='NonDQALesson')),
    path('Issue_Notes/', include('Issue_Notes.urls', namespace='Issue_Notes')),
    path('KnowIssue/', include('KnowIssue.urls', namespace='KnowIssue')),
    path('ABOTestPlan/', include('ABOTestPlan.urls', namespace='ABOTestPlan')),
    path('PersonalInfo/', include('PersonalInfo.urls', namespace='PersonnalInfo')),
    path('PersonalExperience/', include('PersonalExperience.urls', namespace='PersonalExperience')),
    path('LowLightList/', include('LowLightList.urls', namespace='LowLightList')),
    path('IssuesBreakdown/', include('IssuesBreakdown.urls', namespace='IssuesBreakdown')),
    path('ABOProjectLessonL/', include('ABOProjectLessonL.urls', namespace='ABOProjectLessonL')),
    path('ABOQIL/', include('ABOQIL.urls', namespace='ABOQIL')),
    path('ProjectComparison/', include('ProjectComparison.urls', namespace='ProjectComparison')),
    path('ABODriverTool/', include('ABODriverTool.urls', namespace='ABODriverTool')),
    path('CapitalExpenditure/', include('CapitalExpenditure.urls', namespace='CapitalExpenditure')),
    path('A31LessonLProject/', include('A31LessonLProject.urls', namespace='A31LessonLProject')),
    path('A32LessonLProject/', include('A32LessonLProject.urls', namespace='A32LessonLProject')),
]#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if settings.DEBUG:
    media_root = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT)
#     os.path.join()
#     函数：连接两个或更多的路径名组件
#
#     1.
#     如果各组件名首字母不包含’ / ’，则函数会自动加上
#
# 　　　　　　　　　2.
# 如果有一个组件是一个绝对路径，则在它之前的所有组件均会被舍弃
#
# 　　　　　　　　　3.
# 如果最后一个组件为空，则生成的路径以一个’ / ’分隔符结尾
#     print(media_root)
    urlpatterns += static(settings.MEDIA_URL, document_root=media_root)
    # print (urlpatterns)
