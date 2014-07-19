from django.test import TestCase

# Create your tests here.
from django.test.client import Client
from django.contrib.auth.models import User


class LoginTestCase(TestCase):
    def setUp(self):
        User.objects.create_user(username="lynn", password="asiimwe18")

    def test_login(self):
        # self.client.login(username='lynn', password='asiimwe18')
        resp = self.client.post('/login/', {'username': 'lynn', 'password': 'asiimwe18'})
        self.assertEqual(resp.status_code, 302)
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get('/logout/')
        self.assertEqual(resp.status_code, 302)


class wopaViewsTestCase(TestCase):
    def test_register(self):
        resp = self.client.get('/register/')
        self.assertEqual(resp.status_code, 200)

    def test_stuAssignment(self):
        pass

    def test_createAssignment(self):
        pass
