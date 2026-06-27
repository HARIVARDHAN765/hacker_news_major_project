from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = [
            "title",
            "url",
            "text",
            "post_type",
        ]



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]