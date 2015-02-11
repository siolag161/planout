from django.db import DataError
from django.test import TestCase

from .factories import *

# from accounts.models import User
# from django.contrib.auth.models import AbstractUser
# from django.db import models

#####################################################
class AvatarTestCase(TestCase):
    def setUp(self):
        #self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
        self.user = UserFactory.create(email='bunbun@gmail.com', password='testpassword')
        #self.user.save()
        #self.client.login(username='test', password='testpassword')
        #Image.init()

    def uploadWrongFileType(self):
	self.assertTrue(Fals)
class UserTestCase(TestCase):
    def setUp(self):
        #self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
        self.user = UserFactory.create(email='bunbun@gmail.com', password='testpassword')
        #self.user.save()
        #self.client.login(username='test', password='testpassword')
        #Image.init()
    def uploadWrongFileType(self):
	self.assertTrue(Fals)
    # def test_create_user(self):
    # 	u = User()
    # 	self.assertEqual( u.link_karma, None )
    # 	self.assertEqual( u.comment_karma, None )
    # 	self.assertEqual( u.desc, None)
    # 	self.assertTrue(isinstance(u, AbstractUser))
    # 	self.assertTrue(isinstance(u, User))

    # 	self.assertEqual(u.total_karmas, None)
    # 	u.username = "alibaba"
    # 	self.assertEqual(u.__unicode__(), u.username)
    # 	self.assertEqual(str(u), u.username)
	
    # def test_check_instance(self):
    # 	user = UserFactory.build(link_karma=1,comment_karma=1)	
    # 	self.assertEqual( user.link_karma, 1)
    # 	self.assertEqual( user.comment_karma, 1)
    
    # def test_create_random_username(self):
    # 	user = UserFactory.build()
    # 	self.assertEqual( len(user.username), 5 )
    # 	user = UserFactory.build(username=random_string(29)) 
    # 	self.assertEqual( len(user.username), 29 )
	
    # 	with self.assertRaises(DataError): # name <= 30 in length
    # 	    UserFactory.create(username=random_string(331)) # error raised when trying to persist

    # def test_create_default_karma(self):
    # 	user = UserFactory.build()
    # 	self.assertEqual(user.link_karma, None)
    # 	self.assertEqual(user.comment_karma, None)

    # def test_create_check_karma(self):
    # 	user = UserFactory.build(link_karma=28)
    # 	self.assertEqual(user.link_karma, 28)
    # 	self.assertEqual(user.comment_karma, None)

    
