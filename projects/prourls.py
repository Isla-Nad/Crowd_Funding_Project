from django.urls import path
from projects.views import projects,View,review_page
from projects.views import Createform
urlpatterns = [
path('projects/',projects,name='projects'),
path('create',Createform,name='create'),
path('view/<int:id>',View,name="view"),
path('comment/<int:id>',review_page,name="comment"),


]