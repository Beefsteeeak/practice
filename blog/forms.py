from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Comment, Post


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["headline", "short_description", "description", "image", "blank"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    text = forms.CharField(required=True, widget=forms.Textarea)
