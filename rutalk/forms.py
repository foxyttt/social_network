from django import forms
from .models import Post, Comment, Group, Profile
from django.contrib.auth.forms import UserCreationForm

class PostForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Post something...",
                "class": "textarea is-success is-medium",
            }
        ),
        label='',
    )
    image = forms.ImageField(
        required=False,
        widget=forms.widgets.ClearableFileInput(
            attrs={
                "class" : "file-input",
            }
        ),
        label='Upload image',
    )

    class Meta:
        model = Post
        exclude = ("user", "group",)

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ("email",)

class CommentForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.widgets.Textarea(
            attrs={
                "placeholder": "Comment...",
                "class": "textarea is-success is-medium",
            }
        ),
        label='',
    )
    image = forms.ImageField(
        required=False,
        widget=forms.widgets.ClearableFileInput(
            attrs={
                "class" : "file-input",
            }
        ),
        label='Upload image',
    )

    class Meta:
        model = Comment
        exclude = ("user", "post",)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Group description...'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'patronymic', 'bio', 'birth_date', 'education', 'phone']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
