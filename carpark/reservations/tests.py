from django.test import TestCase
from django.urls import reverse
import json
from datetime import datetime, timedelta
from parking_lot.models import Parking
from usersAPI.models import User
import re
from .models import Reservations
# Create your tests here.

class TestReservations(TestCase):
    def setUp(self):
        self.parking = Parking.objects.create(name="test", is_paid=True)
        self.user = User.objects.create(username="test@test.com", password="test_password")

        self.content_type = 'application/json'


    def test_create(self):  
        data = json.dumps({"hours" : "1", "minutes" : "1", "parkingName": self.parking.name, "userId": self.user.id})

        response = self.client.post(reverse('reservation_create'), data, content_type=self.content_type)
        end_date = (datetime.now() + timedelta(hours=1, minutes=1)).strftime('%Y-%m-%dT%H:%M:%S.%f')
        
        # sprawdzanie poprawności tworzenia rezerwacji
        self.assertEqual(response.status_code, 200)
        self.assertEqual(re.sub(r'\..*', '', response.json()['end_date']), re.sub(r'\..*', '', end_date))

        reservation = Reservations.objects.get(parking_id=self.parking.id, user_id=self.user.id)

        # sprawdzanie poprawności przedłużenia rezerwacji
        response = self.client.post(reverse('reservation_create'), data, content_type=self.content_type)
        end_date = (reservation.end_date + timedelta(hours=1, minutes=1)).strftime('%Y-%m-%dT%H:%M:%S.%f')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(re.sub(r'\..*', '', response.json()['end_date']), re.sub(r'\..*', '', end_date))

    def test_cancel_reservation(self):
        data = json.dumps({"parkingName": self.parking.name, "userId": self.user.id})
        
        start_date = datetime.now()
        end_date = start_date + timedelta(hours=1)
        Reservations.objects.create(user=self.user, parking=self.parking, end_date=end_date, start_date=start_date)

        response = self.client.post(reverse('reservation_cancel'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

    def test_get_reservation(self):
        data = json.dumps({"parkingName": self.parking.name, "userId": self.user.id})

        # test bez rezerwacji
        response = self.client.post(reverse('reservation_get'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['end_date'], "doesn\'t exist")

        start_date = datetime.now()
        end_date = start_date + timedelta(hours=1)
        reservation = Reservations.objects.create(user=self.user, parking=self.parking, end_date=end_date, start_date=start_date)
        
        # test posiadanej rezerwacji
        end_date = reservation.end_date.strftime('%Y-%m-%dT%H:%M:%S.%f')
        response = self.client.post(reverse('reservation_get'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(re.sub(r'\..*', '', response.json()['end_date']), re.sub(r'\..*', '', end_date))


