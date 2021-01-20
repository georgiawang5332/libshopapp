from django import forms
from posts.models import Post


class PostForms(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'img',
            'file',
            'content',
            'draft',
            'publish',
        ]
