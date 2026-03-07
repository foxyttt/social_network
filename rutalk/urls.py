from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import dashboard, profile_list, profile, sign_up, feed, post_detail, group_list, group, group_join, group_leave, group_create, edit_profile

app_name = 'rutalk'

urlpatterns = [
    path('', dashboard, name='dashboard'), #входная страница
    path('sign_up/', sign_up, name='sign_up'), #страница регистрации
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'), #страница входа
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'), #страница выхода
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
    #сброс и смена пароля
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
    path('feed/', feed, name='feed'), #лента
    path('post/<int:pk>/', post_detail, name='post_detail'), #страница отдельного поста
    path('profile_list/', profile_list, name='profile_list'), #страница со списком профилей
    path('profile/<int:pk>', profile, name='profile'), #страница профиля конкретного пользователя
    path('groups/', group_list, name='group_list'), #список всех групп
    path('groups/<int:pk>/', group, name='group'), #страница отдельной группы
    path('groups/create/', group_create, name='group_create'), #страница создания группы
    path('groups/<int:pk>/join/', group_join, name='group_join'), #страница вступления
    path('groups/<int:pk>/leave/', group_leave, name='group_leave'), #страница покидания
    path('profile/edit/', edit_profile, name='edit_profile'), #страница редактирования профиля
]