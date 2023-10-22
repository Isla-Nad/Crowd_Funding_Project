from django.urls import path
from projects.views import project_list, project_detail, Createform, delete_project

urlpatterns = [
    path('projects/', project_list, name='projects'),
    path('create/', Createform, name='create'),
    path('view/<int:id>', project_detail, name="view"),
    path('delete/<int:id>', delete_project, name="delete"),

]


## ! 

from projects.views import add_report

urlpatterns+= [
    path('report/<id>',add_report,name='project.report')
]
