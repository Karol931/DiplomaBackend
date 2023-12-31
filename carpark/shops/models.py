from django.db import models

# Create your models here.

class Shops(models.Model):
    name = models.CharField(max_length=255)
    zone = models.CharField(max_length=1)