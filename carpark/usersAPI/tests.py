from django.test import TestCase
from django.urls import reverse
import json
# Create your tests here.

class TestUsers(TestCase):
    def setUp(self):
        self.content_type = 'application/json'

        self.data = json.dumps({"username": "login_test@test.com", "password": "test"})
        self.user = self.client.post(reverse('user_register'), self.data, content_type=self.content_type)
        self.response = self.client.post(reverse('token_obtain_pair'), self.data, content_type=self.content_type)


    def test_register(self):
        data = json.dumps({"username": "test@test.com", "password": "test_password"})
        
        # test rejestracji
        response = self.client.post(reverse('user_register'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

        # test ponownej rejestracji
        response = self.client.post(reverse('user_register'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['username'], 'user with this username already exists.')

    def test_login(self):

        # test logowania ze złymi danymi
        wrong_data = json.dumps({"username": "wrong@test.com", "password": "test"})

        response = self.client.post(reverse('token_obtain_pair'), wrong_data, content_type=self.content_type)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()['detail'], 'No active account found with the given credentials')

        # test poprawnego logowania
        response = self.client.post(reverse('token_obtain_pair'), self.data, content_type=self.content_type)
    
        self.assertTrue('access' in response.json())
        self.assertTrue('refresh' in response.json())

    def test_token_refresh(self):

        wrong_token = self.response.json()['refresh'] + "abc"
        token = self.response.json()['refresh']

        data = json.dumps({"refresh": wrong_token})
        response = self.client.post(reverse('token_refresh'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 401)
        
        data = json.dumps({"refresh": token})
        response = self.client.post(reverse('token_refresh'), data, content_type=self.content_type)

        self.assertEqual(response.status_code, 200)

    def test_token_verify(self):
        wrong_token = self.response.json()['access'] + "abc"
        token = self.response.json()['access']

        data = json.dumps({"token": wrong_token})
        response = self.client.post(reverse('token_verify'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 401)
        
        data = json.dumps({"token": token})
        response = self.client.post(reverse('token_verify'), data, content_type=self.content_type)
        self.assertEqual(response.status_code, 200)

    def test_get_id(self):
        username = json.loads(self.data)['username']
        id = self.user.json()['id']
        response = self.client.post(reverse('user_get_id'), json.dumps({"username":username}), content_type=self.content_type)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], id)
