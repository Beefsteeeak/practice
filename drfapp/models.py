from django.db import models


class Post(models.Model):
    headline = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.headline


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.text
