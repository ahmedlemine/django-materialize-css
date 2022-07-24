from django import forms

from .models import Post

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
