from django.db import models

class Parking(models.Model):
    name = models.CharField(max_length=255, unique=True)
    is_paid = models.BooleanField()

class Level(models.Model):
    level_number = models.IntegerField()
    parking = models.ForeignKey(to=Parking, to_field='id', on_delete=models.CASCADE, default=None)

class Zone(models.Model):
    name = models.CharField(max_length=1)
    level = models.ForeignKey(to=Level, to_field='id', on_delete=models.CASCADE, default=None)

class Spot(models.Model):
    spot_number = models.IntegerField()
    is_taken = models.BooleanField(max_length=50)
    user_id = models.IntegerField(default=None, null=True)
    distance = models.FloatField(null=False)
    zone = models.ForeignKey(to=Zone, to_field='id', on_delete=models.CASCADE, default=None)






