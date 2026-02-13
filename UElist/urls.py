from django.urls import path
# 引入views.py
from . import views

app_name = 'UElist'

urlpatterns = [
    path('UEItems_edit/', views.UEItems_edit),
    # path(r'Lesson_project/', views.Lesson_project),
    # path(r'Lesson_update/', views.Lessonupdate),
    path('UE_ProjectResult/', views.UE_ProjectResult, name='UE_ProjectResult'),
]