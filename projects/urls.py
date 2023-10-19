from django.urls import path
from projects.views import projects
from projects.views import Createform
urlpatterns = [
    path('projects/', projects, name='projects'),
    path('create', Createform, name='create')
]
