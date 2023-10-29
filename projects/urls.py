from django.urls import path
from projects.views import project_list, project_detail, createform, delete_project, add_report, report_comment_view, index, category_details, projects_search

urlpatterns = [
    path('projects/', project_list, name='projects.list'),
    path('create/', createform, name='project.create'),
    path('view/<int:id>', project_detail, name="project.view"),
    path('report/<int:id>', add_report, name='project.report'),
    path('reportcomment/<int:id>', report_comment_view, name='comment.report'),
    path('delete/<int:id>', delete_project, name="project.delete"),
    path('search/', projects_search, name='projects.search'),
    path('categorydetails/<category>', category_details, name='category'),
]
