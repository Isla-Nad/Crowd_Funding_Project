from django.urls import path
from projects.views import projects
from projects.views import Createform,index
urlpatterns = [
    path('projects/', projects, name='projects'),
    path('create', Createform, name='create'),
    path('index', index, name='projects.index')
]
