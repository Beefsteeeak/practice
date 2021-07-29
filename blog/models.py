from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    headline = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='images')
    blank = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline


class Comment(models.Model):
    username = models.CharField(max_length=255, default="Anonymous")
    text = models.TextField()
    is_published = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.username
