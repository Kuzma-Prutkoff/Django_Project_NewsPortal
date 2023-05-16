from django import forms
from .models import Post

class PostForm(forms.ModelForm): # какие поля используются при создании поста
    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'post_category']

