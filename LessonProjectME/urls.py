from django.urls import path
# 引入views.py
from . import views

app_name = 'LessonProjectME'

urlpatterns = [

    path('Lesson_ProjectResult/', views.Lesson_project, name='LessonProjectME_edit'),
    path('Lesson_SearchByProject/', views.Lesson_project_Search, name='LessonProjectME_search'),


]