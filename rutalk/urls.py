from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import dashboard, profile_list, profile, sign_up, feed

app_name = 'rutalk'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('sign_up/', sign_up, name='sign_up'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/password_change_form.html',
             success_url=reverse_lazy('rutalk:password_change_done')
         ),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/password_change_done.html'
         ),
         name='password_change_done'),
    path('feed/', feed, name='feed'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
]