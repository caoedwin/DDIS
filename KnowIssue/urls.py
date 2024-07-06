from django.urls import path
from . import views
app_name = 'KnowIssue'
urlpatterns = [


    path('KnowIssue-upload/', views.KnowIssue_upload, name='KnowIssue_upload'),
    path('KnowIssue-search/', views.KnowIssue_search, name='KnowIssue_search'),
    path('KnowIssue-edit/', views.KnowIssue_edit, name='KnowIssue_edit'),


]