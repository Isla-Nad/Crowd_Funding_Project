from django.urls import path
from projects.views import project_list, project_detail, Createform

urlpatterns = [
    path('projects/', project_list, name='projects'),
    path('create/', Createform, name='create'),
    path('view/<int:id>', project_detail, name="view"),
]


## ! 

from projects.views import add_report,report_comment_view

urlpatterns+= [
    path('report/<id>',add_report,name='project.report'),
    path('reportcomment/<id>',report_comment_view,name='comment.report'),
]
