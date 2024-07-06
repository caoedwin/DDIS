from django.urls import path
from . import views
app_name = 'Issue_Notes'
urlpatterns = [


    path('Issue_Notes-upload/', views.Issue_Notes_upload, name='Issue_Notes_upload'),
    path('Issue_Notes-search/', views.Issue_Notes_search, name='Issue_Notes_search'),
    path('Issue_Notes-edit/', views.Issue_Notes_edit, name='Issue_Notes_edit'),


]