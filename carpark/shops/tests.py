from django.test import TestCase
from django.urls import reverse
import json
# Create your tests here.

class TestShop(TestCase):
    def setUp(self):
        self.shops = {"shops": [{"name":"Adidas", "zone": "A"},{ "name":"Nike","zone": "B"}]}
        self.content_type = 'application/json'

    def test_create(self):
        data = json.dumps(self.shops)
        
        # test for adding shops
        response = self.client.post(reverse('shop_create'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        # test for adding shops if one or more exist
        response = self.client.post(reverse('shop_create'), data, content_type=self.content_type)
        self.assertEqual(response.json()['err'], 'one or more shops already exist')