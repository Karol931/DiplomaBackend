from django.test import TestCase
from django.urls import reverse
import json
from usersAPI.models import User
from shops.models import Shops
# Create your tests here.

class TestUsers(TestCase):
    def setUp(self):
        self.content_type = 'application/json'
        self.data = json.dumps({"levels": 3, "name": "test", "occupacy": "25%", "isPaid": True})
        self.client.post(reverse('parking_create'), self.data, content_type=self.content_type)

    def test_create(self):
        data = json.dumps({"levels": 3, "name": "create_test", "occupacy": "25%", "isPaid": True})

        response = self.client.post(reverse('parking_create'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('parking_create'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['err'], "Parking with this name alerady exists")

    def test_get_parking(self):
        data = json.dumps({"name": "test"})
        
        response = self.client.post(reverse('get_parking'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], 'test')
        self.assertEqual(response.json()['is_paid'], True)
        self.assertEqual(len(response.json()['levels']), 3)
        for l in range(len(response.json()['levels'])):
            self.assertTrue('level' in response.json()['levels'][l])
            self.assertTrue('zones' in response.json()['levels'][l])
            for z in range(len(response.json()['levels'][l]['zones'])):
                self.assertTrue('zone' in response.json()['levels'][l]['zones'][z])
                self.assertTrue('spots' in response.json()['levels'][l]['zones'][z])
                for s in range(len(response.json()['levels'][l]['zones'][z]['spots'])):
                    self.assertTrue('is_taken' in response.json()['levels'][l]['zones'][z]['spots'][s])
                    self.assertTrue('number' in response.json()['levels'][l]['zones'][z]['spots'][s])
                    self.assertTrue('user_id' in response.json()['levels'][l]['zones'][z]['spots'][s])

    def test_get_names(self):
        data2 = json.dumps({"levels": 2, "name": "test2", "occupacy": "75%", "isPaid": False})
        data3 = json.dumps({"levels": 5, "name": "test3", "occupacy": "50%", "isPaid": True})
        self.client.post(reverse('parking_create'), data2, content_type=self.content_type)
        self.client.post(reverse('parking_create'), data3, content_type=self.content_type)
        response = self.client.get(reverse('parking_get_names'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"names": ["test", "test2", "test3"]})
    
    def test_find_spot(self):
        data = json.dumps({"levels": 3, "name": "full_test", "occupacy": "100%", "isPaid": True})
        self.client.post(reverse('parking_create'), data, content_type=self.content_type)
        user = User.objects.create(username="test@test.com", password="test")

        data = json.dumps({'userId': user.id, 'parkingName': 'test', 'level':'','zone':''})
        response = self.client.post(reverse('parking_find_spot'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('spot' in response.json())

        data = json.dumps({'userId': user.id, 'parkingName': 'test', 'level':'','shop':''})
        response = self.client.post(reverse('parking_find_spot'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('spot' in response.json())

        data = json.dumps({'userId': user.id, 'parkingName': 'full_test', 'level':'', 'zone':''})
        response = self.client.post(reverse('parking_find_spot'), data, content_type=self.content_type)
      
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['err'], "No free spots in desired zone")

        data = json.dumps({'userId': user.id, 'parkingName': 'full_test', 'level':'', 'shop':''})
        response = self.client.post(reverse('parking_find_spot'), data, content_type=self.content_type)
      
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['err'], "No free spots in desired zone")


    def test_delete_spot(self):
        user = User.objects.create(username="test@test.com", password="test")
        data = json.dumps({'id': user.id})
        
        response = self.client.post(reverse('parking_delete_spot'), data, content_type=self.content_type)

        self.assertTrue(response.status_code, 400)
        self.assertTrue(response.json()['err'], 'user had no spot assigned')

        data = json.dumps({'userId': user.id, 'parkingName': 'test', 'level':''})
        self.client.post(reverse('parking_find_spot'), data, content_type=self.content_type)
        
        data = json.dumps({'id': user.id})
        response = self.client.post(reverse('parking_delete_spot'), data, content_type=self.content_type)

        self.assertTrue(response.status_code, 200)

    def test_get_parking_options(self):
        shops = json.dumps({"shops": [{"name":"Adidas", "zone": "A"},{ "name":"Nike","zone": "B"}]})
        self.client.post(reverse('shop_create'), shops, content_type=self.content_type)
        
        data = json.dumps({"parkingName": "test"})

        response = self.client.post(reverse('get_parking_options'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('shops' in response.json())        
        self.assertTrue('levels' in response.json())
        self.assertTrue('zones' in response.json())        
        self.assertEqual(len(response.json()['shops']), 2)
        for s in range(len(response.json()['shops'])):
            self.assertTrue('name' in response.json()['shops'][s])

        self.assertEqual(len(response.json()['levels']), 3)
        for l in range(len(response.json()['levels'])):
            self.assertTrue('number' in response.json()['levels'][l])

        self.assertEqual(len(response.json()['zones']), 4)
        for z in range(len(response.json()['zones'])):
            self.assertTrue('name' in response.json()['zones'][z])
