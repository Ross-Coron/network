from django.contrib.auth.models import AbstractUser
from django.db import models

# Inherits from AbstractUser - has access to username, email, password, etc.
class User(AbstractUser):
    pass

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    following = models.ForeignKey(User, on_delete=models.CASCADE)

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweetText = models.CharField(max_length=255)
    posted = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    likedBy = models.ForeignKey(User, on_delete=models.CASCADE)