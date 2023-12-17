from django.db import models

class Shops(models.Model):
    name = models.CharField(max_length=255)
    zone = models.CharField(max_length=1)

class Parking(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_paid = models.BooleanField()

class Level(models.Model):
    # Define fields for the Level model
    level_number = models.IntegerField()
    parking = models.ForeignKey(to=Parking, to_field='id', on_delete=models.CASCADE, default=None)

class Zone(models.Model):
    # Define fields for the Zone model
    name = models.CharField(max_length=1)
    level = models.ForeignKey(to=Level, to_field='id', on_delete=models.CASCADE, default=None)

# Create your models here.
class Spot(models.Model):
    # Define fields for the Spot model
    # For example, assuming each spot has a name and a status
    spot_number = models.IntegerField()
    is_taken = models.BooleanField(max_length=50)
    user_id = models.IntegerField(default=None, null=True)
    distance = models.FloatField(null=False)
    zone = models.ForeignKey(to=Zone, to_field='id', on_delete=models.CASCADE, default=None)






