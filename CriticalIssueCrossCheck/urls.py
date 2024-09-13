from django.urls import path
# 引入views.py
from . import views

app_name = 'CriticalIssueCrossCheck'

urlpatterns = [
    path('CriticalIssue_edit/', views.CriticalIssue_edit),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path('CriticalIssue_ProjectResult/', views.CriticalIssue_ProjectResult, name='LessonProject_edit'),
    path('CriticalIssue_SearchByProject/', views.CriticalIssue_SearchByProject, name='LessonProject_search'),
]