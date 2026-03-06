from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import dashboard, profile_list, profile, sign_up, feed

app_name = 'rutalk'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('sign_up/', sign_up, name='sign_up'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    #смена пароля
    path('accounts/password_change/',
         auth_views.PasswordChangeView.as_view(
             template_name='registration/custom_password_change_form.html',
             success_url=reverse_lazy('rutalk:password_change_done')
         ),
         name='password_change'),
    path('accounts/password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(
             template_name='registration/custom_password_change_done.html'
         ),
         name='password_change_done'),
    #сброс пароля
    path('accounts/password_reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/custom_password_reset_form.html',
             success_url=reverse_lazy('rutalk:password_reset_done'),
             email_template_name='registration/custom_password_reset_email.html',
             subject_template_name='registration/custom_password_reset_subject.txt',
         ),
         name='password_reset'),
    path('accounts/password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/custom_password_reset_done.html'
         ),
         name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/custom_password_reset_confirm.html',
             success_url=reverse_lazy('rutalk:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('accounts/reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/custom_password_reset_complete.html'
         ),
         name='password_reset_complete'),

    path('feed/', feed, name='feed'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
]