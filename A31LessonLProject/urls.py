from django.urls import path
# 引入views.py
from . import views

app_name = 'A31LessonLProject'

urlpatterns = [
    path('Lesson_upload/', views.A31Lesson_upload),
    path('Lesson_edit/', views.A31Lesson_edit),
    path('Lesson_search/', views.A31Lesson_search),
    path('Lesson_export/', views.A31Lesson_export),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path('redit_Lesson/<int:id>/', views.A31Lesson_update,name='Lesson_update'),#html{%url%}中调用的是name
    path('Lesson_ProjectResult/', views.A31Lesson_project, name='LessonProject_edit'),
    path('Lesson_SearchByProject/', views.A31Lesson_project_Search, name='LessonProject_search'),
]