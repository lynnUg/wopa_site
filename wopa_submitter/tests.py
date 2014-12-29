from django.test import TestCase

# Create your tests here.
from django.test.client import Client
from django.contrib.auth.models import User,Group
from django.test import RequestFactory,TestCase

from views import UserCreateView


class UserCreateViewTestCase(TestCase):
    def setUp(self):
        Group.objects.create(name='wopaTemp')
        

    def test_get(self):
        response=self.client.get('/website/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'wopa_submitter/auth/register.html')
    def test_post_errors(self):
        response=self.client.post('/website/register/',{'username':'','password':'','code':'','first_name':'','last_name':'','email':''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Error')
        self.assertContains(response, 'This field is required')
        self.assertContains(response,'>First name:</label>')

    def test_post_correct(self):
        response=self.client.post('/website/register/',{'username':'lynnug','password':'asiimwe','code':'@wopaTemp','first_name':'lynn','last_name':'asiimwe','email':'ntorantyo88@yahoo.com'})
        self.assertEqual(response.status_code, 302)


class LoginViewTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')

    def test_secure_page(self):
        self.client.login(username='temporary', password='temporary')
        response = self.client.get('/website/account', follow=True)
        user = User.objects.get(username='temporary')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].email, 'temporary@gmail.com')
    def test_logout(self):
        pass
class AssignmentListViewTestCase(TestCase):
    def setUp(self):
        pass
    def test_assignment_list_page(self):
        pass
class ReadingListViewTestCase(TestCase):
     def setUp(self):
        pass
     def test_reading_list_page(self):
        pass


   
