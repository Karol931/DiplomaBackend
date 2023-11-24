from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractUser
# Create your models here.

class User(AbstractUser, PermissionsMixin):
    password = models.CharField(max_length=255)
    username = models.EmailField(max_length=255, unique=True)

