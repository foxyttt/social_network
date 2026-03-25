from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import (
    dashboard, profile_list, profile, sign_up, feed, post_detail, group_list, group,
    group_join, group_leave, group_create, edit_profile, channel_join, channel_create,
    channel_detail, channel_leave
)
from .forms import (
    CustomAuthenticationForm, CustomPasswordChangeForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)

app_name = 'rutalk'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('sign_up/', sign_up, name='sign_up'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=CustomAuthenticationForm), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(
        template_name='registration/custom_password_change_form.html',
        form_class=CustomPasswordChangeForm,
        success_url=reverse_lazy('rutalk:password_change_done')
    ), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='registration/custom_password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/custom_password_reset_form.html',
        form_class=CustomPasswordResetForm,
        success_url=reverse_lazy('rutalk:password_reset_done'),
        email_template_name='registration/custom_password_reset_email.html',
        subject_template_name='registration/custom_password_reset_subject.txt',
    ), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/custom_password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/custom_password_reset_confirm.html',
        form_class=CustomSetPasswordForm,
        success_url=reverse_lazy('rutalk:password_reset_complete')
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/custom_password_reset_complete.html'
    ), name='password_reset_complete'),
    path('feed/', feed, name='feed'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('profile_list/', profile_list, name='profile_list'),
    path('profile/<int:pk>', profile, name='profile'),
    path('groups/', group_list, name='group_list'),
    path('groups/create/', group_create, name='group_create'),
    path('groups/<int:pk>/', group, name='group'),
    path('groups/<int:pk>/join/', group_join, name='group_join'),
    path('groups/<int:pk>/leave/', group_leave, name='group_leave'),
    path('channels/create/', channel_create, name='channel_create'),
    path('channels/<int:pk>/', channel_detail, name='channel_detail'),
    path('channels/<int:pk>/join/', channel_join, name='channel_join'),
    path('channels/<int:pk>/leave/', channel_leave, name='channel_leave'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]
