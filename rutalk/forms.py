from django import forms
from .models import Post, Comment
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
        exclude = ("user", )

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
    # image = forms.ImageField(
    #     required=False,
    #     widget=forms.widgets.ClearableFileInput(
    #         attrs={
    #             "class" : "file-input",
    #         }
    #     ),
    #     label='Upload image',
    # )

    class Meta:
        model = Comment
        exclude = ("user", "post",)
