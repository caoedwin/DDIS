from django.urls import path
from . import views
app_name = 'NonDQALesson'
urlpatterns = [


    path('NonDQALesson-summary/', views.NonDQALesson_summary, name='NonDQALesson_summary'),


]