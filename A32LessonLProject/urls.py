from django.urls import path
# 引入views.py
from . import views

app_name = 'A32LessonLProject'

urlpatterns = [
    path('Lesson_upload/', views.A32Lesson_upload),
    path('Lesson_edit/', views.A32Lesson_edit),
    path('Lesson_search/', views.A32Lesson_search),
    path('Lesson_export/', views.A32Lesson_export),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path('redit_Lesson/<int:id>/', views.A32Lesson_update,name='Lesson_update'),#html{%url%}中调用的是name
    path('Lesson_ProjectResult/', views.A32Lesson_project, name='LessonProject_edit'),
    path('Lesson_SearchByProject/', views.A32Lesson_project_Search, name='LessonProject_search'),
]