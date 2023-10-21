from django.urls import path
from projects.views import project_list, project_detail, Createform

urlpatterns = [
    path('projects/', project_list, name='projects'),
    path('create/', Createform, name='create'),
    path('view/<int:id>', project_detail, name="view"),
]
