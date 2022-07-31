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
# class PostForm(forms.Form):
#     model = Post
#     title = forms.CharField(
#         label= "Post Title",
#         widget=forms.TextInput(attrs= {
#             'class': 'input-field'
#         })
#     )
#     body = forms.Textarea(
#         # label="Post Body",
#         widget=forms.Textarea(attrs= {
#             'class': 'materialize-textarea',
#             'rows': 13
#         }),
#     )

#     # class Meta:
#     #     fields = ['title', 'body' ]
