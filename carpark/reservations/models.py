from django.db import models
from usersAPI.models import User
from parking_lot.models import Parking
# Create your models here.

class Reservations(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None)
    parking = models.ForeignKey(to=Parking, to_field='id', on_delete=models.CASCADE, default=None)

class ArchivedReservations(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(to=User, to_field='id', on_delete=models.CASCADE, default=None)
    parking = models.ForeignKey(to=Parking, to_field='id', on_delete=models.CASCADE, default=None)