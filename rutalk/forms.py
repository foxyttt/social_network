from django import forms
from .models import Post

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

    class Meta:
        model = Post
        exclude = ("user", )