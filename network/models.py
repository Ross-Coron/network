from django.contrib.auth.models import AbstractUser
from django.db import models

# Inherits from AbstractUser - has access to username, email, password, etc.
class User(AbstractUser):
    pass

class Tweet(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tweetText = models.CharField(max_length=255)
    posted = models.DateTimeField(auto_now_add=True)
