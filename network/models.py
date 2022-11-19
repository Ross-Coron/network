from django.contrib.auth.models import AbstractUser
from django.db import models

# Inherits from AbstractUser - has access to username, email, password, etc.
class User(AbstractUser):
    pass
