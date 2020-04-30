from django import forms
from  . import models

#Contributers: Derek, Michael

class CreatePost(forms.ModelForm):
    '''Creates a post based on the Django Model Form that has the fields Post.title and Post.text'''
    class Meta:
        model = models.Post
        fields = ['title', 'text']
        labels = {
                'text': 'Post: ',
                'title': 'Title: ',
            }

class CreateComment(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ['text']
        labels = {
                'text': 'Comment: ',
            }
