from xml.dom import ValidationErr
from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 10,
                'cols': 40,
                'class': 'materialize-textarea'
                }),
        }
    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment',]
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 10,
                'cols': 20,
                'class': 'materialize-textarea',
                'data-length': '500'
                }),
        }

    def clean_comment(self):
        data = self.cleaned_data['comment']
        if len(data) > 500:
            msg = 'Comment is too long. Please keep your comment under 500 characters.'
            self.add_error('comment', msg)
        if len(data) < 5:
            msg = 'Comment is too short.'
            self.add_error('comment', msg)
        return data