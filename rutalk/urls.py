from django.urls import path
from .views import dashboard, profile_list, profile, sign_up

app_name = 'rutalk'

urlpatterns = [
    path('', sign_up, name='sign_up'),
    path('dashboard/', dashboard, name='dashboard'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
]