from django.urls import path
from projects.views import project_list, project_detail, createform, delete_project, add_report

urlpatterns = [
    path('projects/', project_list, name='projects.list'),
    path('create/', createform, name='project.create'),
    path('view/<int:id>', project_detail, name="project.view"),
    path('report/<id>', add_report, name='project.report'),
    path('delete/<int:id>', delete_project, name="project.delete"),
]
