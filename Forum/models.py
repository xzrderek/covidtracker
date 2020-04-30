from django.db import models

# Create your models here.
class Post(models.Model):
    """A Post a User Makes"""
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.CharField(max_length=100)
    def __str__(self):
        """Return a string representation of the model."""
        return str(self.id)

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=100)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
