from django.urls import include, path
from accounts.views import activate, password_change, delete_account, edit_profile, edit_user, profile, register, user_login, user_logout

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register, name='accounts.register'),
    path('register/activate/<str:uidb64>/<str:token>/',
         activate, name='accounts.activate'),
    path('user_login/', user_login, name='accounts.login'),
    path('user_logout/', user_logout, name='accounts.logout'),
    path('profile/<int:pk>', profile, name='accounts.profile'),
    path('edit/', edit_user, name='accounts.edit'),
    path('edit/profile/<int:pk>', edit_profile, name='profile.edit'),
    path('delete/', delete_account, name='accounts.delete'),
    path('password_change/<int:id>', password_change, name='password_change'),
]
