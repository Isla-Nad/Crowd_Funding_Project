from django.urls import path
from categories.views import admin_home

urlpatterns = [
    path('admin_home/', admin_home, name='admin_home'),

]
