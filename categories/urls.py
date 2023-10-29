from django.urls import path
from categories.views import admin_home,donation,edit_donation,delete_donation,create_donation,report,edit_report,delete_report,create_report

urlpatterns = [
    path('admin_home/', admin_home, name='admin_home'),
    path('admin_home/donation', donation, name='donation'),
    path('edit_donation/<int:pk>/', edit_donation, name='edit_donation'),
    path('delete_donation/<int:pk>/', delete_donation, name='delete_donation'),
    path('create_donation/', create_donation, name='create_donation'),
    path('admin_home/report', report, name='report'),
    path('edit_report/<int:pk>/', edit_report, name='edit_report'),
    path('delete_report/<int:pk>/', delete_report, name='delete_report'),
    path('create_report/', create_report, name='create_report'),

]
