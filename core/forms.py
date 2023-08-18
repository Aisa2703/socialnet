from django import forms
from django.contrib.auth.models import User
from .models import Comment, Profile, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']


class RegistrationUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'nickname', 'description', 'link_fb',
            'whatsapp', 'telegram', 'photo'
        ]


class PostsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name', 'description', 'photo',
            'status'
        ]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'name',
            'photo',
        ]