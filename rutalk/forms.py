from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, AuthenticationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth.models import User
from .models import Post, Comment, Group, Profile, Channel


class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Напишите пост...",
            "class": "textarea is-success is-medium",
        }),
        label='',
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "file-input"}),
        label='Изображение',
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 10 * 1024 * 1024:
            raise forms.ValidationError('Размер изображения не должен превышать 10 МБ.')
        return image

    class Meta:
        model = Post
        exclude = ("user", "group", "channel")


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Электронная почта')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Используйте буквы, цифры и символы @ / . / + / - / _.'
        self.fields['password1'].help_text = 'Пароль должен быть достаточно надёжным.'
        self.fields['password2'].help_text = 'Введите пароль ещё раз для подтверждения.'


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput)
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, help_text='Придумайте новый надёжный пароль.')
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput, help_text='Введите новый пароль ещё раз.')


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Электронная почта')


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput, help_text='Придумайте новый надёжный пароль.')
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput, help_text='Введите новый пароль ещё раз.')


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            "placeholder": "Напишите комментарий...",
            "class": "textarea is-success is-medium",
        }),
        label='',
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "file-input"}),
        label='Изображение',
    )

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image and image.size > 10 * 1024 * 1024:
            raise forms.ValidationError('Размер изображения не должен превышать 10 МБ.')
        return image

    class Meta:
        model = Comment
        exclude = ("user", "post")


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        labels = {
            'name': 'Название группы',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Описание группы...'}),
        }


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'description']
        labels = {
            'name': 'Название канала',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Описание канала...'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'patronymic', 'bio', 'birth_date', 'education', 'phone']
        labels = {
            'avatar': 'Аватар',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'bio': 'О себе',
            'birth_date': 'Дата рождения',
            'education': 'Место учёбы/работы',
            'phone': 'Телефон',
        }
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Расскажите о себе...'}),
        }
