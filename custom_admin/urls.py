from django.urls import path
from custom_admin.views import admin_home, categories_list, create_donation, create_report, delete_donation, delete_report, donation, edit_donation, edit_report, report, tags_list, category_create, tag_create, category_edit, tag_edit, category_delete, tag_delete

urlpatterns = [
    path('admin_home/', admin_home, name='admin_home'),
    path('categories_list/', categories_list, name='categories_list'),
    path('tags_list/', tags_list, name='tags_list'),
    path('category_create/', category_create, name='category_create'),
    path('tag_create/', tag_create, name='tag_create'),
    path('<int:id>/category_edit/', category_edit, name='category_edit'),
    path('<int:id>/tag_edit/', tag_edit, name='tag_edit'),
    path('<int:id>/category_delete/', category_delete, name='category_delete'),
    path('<int:id>/tag_delete/', tag_delete, name='tag_delete'),
    path('admin_home/donation', donation, name='donation'),
    path('edit_donation/<int:pk>/', edit_donation, name='edit_donation'),
    path('delete_donation/<int:pk>/', delete_donation, name='delete_donation'),
    path('create_donation/', create_donation, name='create_donation'),
    path('admin_home/report', report, name='report'),
    path('edit_report/<int:pk>/', edit_report, name='edit_report'),
    path('delete_report/<int:pk>/', delete_report, name='delete_report'),
    path('create_report/', create_report, name='create_report'),
]
