from django import forms
from .models import BlogPost, Comment,CommentLike


class PostForm(forms.ModelForm):
   class Meta:
      model = BlogPost
      fields =['title', 'content']

      widgets = {
         'title': forms.TextInput(
            attrs={
               'class': 'form-control',
               'placeholder': 'enter Post title'
            }
         ),

         'content': forms.Textarea(
            attrs={
               'class':'form-control',
               'rows': 10,
               'placeholder':'Enter content Here'
            }
         )
      }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment...'
            })
        }