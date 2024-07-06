from django.urls import path
# 引入views.py
from . import views

app_name = 'ABOProjectLessonL'

urlpatterns = [
    path('Lesson_upload/', views.ABOLesson_upload),
    path('Lesson_edit/', views.ABOLesson_edit),
    path('Lesson_search/', views.ABOLesson_search),
    path('Lesson_export/', views.ABOLesson_export),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path('redit_Lesson/<int:id>/', views.ABOLesson_update,name='Lesson_update'),#html{%url%}中调用的是name
    path('Lesson_ProjectResult/', views.ABOLesson_project, name='LessonProject_edit'),
    path('Lesson_SearchByProject/', views.ABOLesson_project_Search, name='LessonProject_search'),
]