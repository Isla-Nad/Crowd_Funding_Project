from django.urls import path
from custom_admin.views import admin_home, categories_list, tags_list, category_create, tag_create, category_edit, tag_edit, category_delete, tag_delete

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
]
