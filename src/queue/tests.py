"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.utils import unittest
from queue.forms import RegistrationForm
from json import loads, dumps
from django.contrib.auth.models import User
from queue.models import *
from datetime import datetime, date
from django.http import HttpRequest


class LoginFunctionality(unittest.TestCase):

    def setUp(self):
        self.c = Client()


    def test_registration_valid(self):
        response = self.c.post('/register/', {'username' : 'testuser', 'password1' : 'testuser', 'password2' : 'testuser'}, follow=True)
        self.failUnlessEqual(response.status_code, 200)
     
        
    def test_registration_invalid_request(self):
        response = self.c.get('/register/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template.name, 'registration/register.html')
    
    
    def test_registration_invalid_username(self):                
        response = self.c.post('/register/', {'username' : 'test-user', 'password1' : 'testuser', 'password2' : 'testuser'}, follow=True)
        self.assertEqual(response.context['form']['username'].errors, [u'Username can only contain alphanumeric characters and the underscore.'])


    def test_registration_passwords_not_match(self):
        response = self.c.post('/register/', {'username' : 'testuser', 'password1' : 'testuser', 'password2' : 'invalidpassword'}, follow=True)
        self.assertEqual(response.context['form']['password2'].errors, [u'Passwords do not match.'])
        
        
    def test_registration_username_is_taken(self):
        response = self.c.post('/register/', {'username' : 'testuser', 'password1' : 'testuser', 'password2' : 'testuser'}, follow=True)
        response = self.c.post('/register/', {'username' : 'testuser', 'password1' : 'testuser', 'password2' : 'testuser'}, follow=True)
        self.assertEqual(response.context['form']['username'].errors, [u'Username is already taken.'])


    def test_login(self):
        response = self.c.post('/login/', {'username' : 'testuser', 'password' : 'testuser'})
        self.failUnlessEqual(response.status_code, 200)
       
        
    def test_logout(self):
        response = self.c.get('/logout/')
        self.failUnlessEqual(response.status_code, 302)
        
        
class QueueItemsFunctionality(unittest.TestCase):
    
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(u'push_user', 'myemail@test.com', u'push_user')
        self.branch = Branch.objects.create(name = 'master')
        self.push1 = QueueRecord.objects.create(ps = "PS_01", description = "Push #1",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "123456",
                                index = 1, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.REVERTED)
        self.push2 = QueueRecord.objects.create(ps = "PS_02", description = "Push #2",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "qwerty",
                                index = 2, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.DONE)
        self.push3 = QueueRecord.objects.create(ps = "PS_03", description = "Push #3",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "asdfgh",
                                index = 3, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.IN_PROGRESS)


    def tearDown(self):
        self.user.delete()
        self.branch.delete()
        self.push1.delete()
        self.push2.delete()
        self.push3.delete()


    def test_queue_item_list(self):
        """
        Tests that Queue Item list could be displayed.
        """
        response = self.c.get('/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template[0].name, 'dpq_queue.html')
        response = self.c.get('/ajax/refresh/master/')
        self.failUnlessEqual(response.status_code, 200)
        self.failUnlessEqual(response.template.name, 'queue_table.html')
        
        
    def test_key_request(self):
        #think how to validate result

        response = self.c.get('/ajax/request/key/')
        self.failUnlessEqual(response.status_code, 200)
        self.assertIsNot(response, "None")

        
    def test_queue_item_creation(self):
        self.c.login(username='push_user', password='push_user')
        json_data = {
                                "ps": "PS_05",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale"
                            }
        response = self.c.post("/ajax/create/",
                            dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        
        
    def test_queue_item_creation_invalid(self):
        self.c.login(username='push_user', password='push_user')
        json_invalid_data = {
                                "description": "",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale"
                            }
        response = self.c.post("/ajax/create/", 
                            dumps(json_invalid_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)
    
    
    def test_queue_item_modify_No_W(self):
        """
        Status P, new index > max
        """
        self.c.login(username='push_user', password='push_user')
        json_data = {
                                "ps": "PS_05",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale",
                                "status" : "P",
                                "index" : 6,
                                "id" : "qwerty"
                            }

        response = self.c.post("/ajax/modify/", dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")
                 
             
    def test_queue_item_modify_P(self):
        """
        Status P, new index > max
        """
        self.c.login(username='push_user', password='push_user')
        push4 = QueueRecord.objects.create(ps = "PS_06", description = "Push #2",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "098765",
                                index = 4, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.WAITING)
        push5 = QueueRecord.objects.create(ps = "PS_05", description = "Push #3",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "zxcvb",
                                index = 5, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.WAITING)
        json_data = {
                                "ps": "PS_05",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale",
                                "status" : "P",
                                "index" : 6,
                                "id" : "098765"
                            }

        response = self.c.post("/ajax/modify/", dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")
        push4.delete()
        push5.delete()

    
    def test_queue_item_modify_W(self):
        """
        Status W, new index < min
        """
        self.c.login(username='push_user', password='push_user')    
        push4 = QueueRecord.objects.create(ps = "PS_06", description = "Push #2",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "098765",
                                index = 4, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.WAITING)
        push5 = QueueRecord.objects.create(ps = "PS_05", description = "Push #3",
                                branch = self.branch,
                                developerA = "Ritchie Blackmore",
                                developerB = "Jon Lord",
                                tester = "David Coverdale", owner = self.user, queue_id = "zxcvb",
                                index = 5, creation_date = datetime.now(), modified_date = datetime.now(),
                                push_date = datetime.now(), done_date = datetime.now(), status = QueueRecord.WAITING)
        json_data = {
                                "ps": "PS_05",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale",
                                "status" : "P",
                                "index" : 1,
                                "id" : "098765"
                            }
        response = self.c.post("/ajax/modify/", dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")
        push4.delete()
        push5.delete()
        
    def test_queue_item_modify_index_0(self):
        """
        Status P, new index > max
        """
        self.c.login(username='push_user', password='push_user')
        json_data = {
                                "ps": "PS_05",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale",
                                "status" : "P",
                                "index" : 0,
                                "id" : "asdfgh"
                            }

        response = self.c.post("/ajax/modify/", dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, "OK")
        
        
    def test_queue_item_modify_invalid_request(self):
        """
        Tests that Queue Item is modified.
        """
        self.c.login(username='push_user', password='push_user')
        json_data = {
                                "ps": "PS_04",
                                "description": "Some description",
                                "branch": "master",
                                "devA": "Ritchie Blackmore",
                                "devB": "Jon Lord",
                                "tester": "David Coverdale"
                            }
        response = self.c.post("/ajax/modify/", dumps(json_data), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 404)   
        
        
    def test_fetch_queue_item(self):
        """
        Tests that Queue Item could be fetched.
        """
        self.c.login(username='push_user', password='push_user')
        json_request = {"mode" : "fetch"}
        json_request["id"] = "asdfgh"
        response = self.c.post("/ajax/request/fetch/", dumps(json_request), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')    
        self.assertEqual(response.status_code, 200)  
        
        """
        Fetch last item.
        """
        json_request["mode"] = "last"  
        response = self.c.post("/ajax/request/fetch/", dumps(json_request), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')    
        self.assertEqual(response.status_code, 200)  
        
        """
        Request with invalid id.
        """
        json_request["mode"] = "fetch"
        json_request["id"] = "1234"  
        response = self.c.post("/ajax/request/fetch/", dumps(json_request), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')    
        self.assertEqual(response.status_code, 404)
        
        """
        Invalid Request.
        """
        json_invalid_request = {"id": "asdfgh"}
        response = self.c.post("/ajax/request/fetch/", dumps(json_invalid_request), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')    
        self.assertEqual(response.status_code, 404)   
        
 
class FetchLastItem(unittest.TestCase):
    
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(u'push_user', 'myemail@test.com', u'push_user')
    
    def tearDown(self):
        self.user.delete()
        
    def test_fetch_last_queue_item(self):
        """
        Tests that last Queue Item could not exist.
        """
        self.c.login(username='push_user', password='push_user') 
        json_request = {"mode" : "last"}
        response = self.c.post("/ajax/request/fetch/", dumps(json_request), "text/json",
                            HTTP_X_REQUESTED_WITH='XMLHttpRequest')    
        self.assertRaises(IndexError)
        self.assertEqual(response.status_code, 200)         
        

class Users_On_Duty(TestCase):
    
    def setUp(self):
        self.c = Client()
    
    def test_fetch_superusers_list(self):
        response = self.c.get('/ajax/request/superusers/')
        self.assertContains(response, "List is empty", status_code = 200)
        
        User.objects.create_user('push_user', 'myemail@test.com', 'push_user')
        User.objects.create_superuser('super_user', 'myemail@test.com', 'super_user')
        
        response = self.c.get('/ajax/request/superusers/')
        self.failUnlessEqual(response.template.name, 'dpq_superusers_list.html')
        self.assertContains(response, "super_user", status_code = 200)
        