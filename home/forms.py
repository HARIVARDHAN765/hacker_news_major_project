from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from .models import Profile
from django.core.exceptions import ValidationError


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

    def clean(self):

        cleaned_data = super().clean()

        post_type = cleaned_data.get("post_type")
        url = cleaned_data.get("url")
        text = cleaned_data.get("text")

        if post_type == "NEWS" and not url:
            raise ValidationError(
                "News posts require a URL."
            )
        if post_type == "ASK" and url:
            raise ValidationError(
                "Ask HN posts cannot have a URL."
            )

        return cleaned_data



class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["content"]



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["about"]