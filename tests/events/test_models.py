from django.db import DataError
from django.test import TestCase

from factories import *

#####################################################
class OrganizationTestCase(TestCase):
    def setUp(self):
        #self.testdatapath = os.path.join(os.path.dirname(__file__), "data")
        self.user = UserFactory.create(email='bunbun@gmail.com', password='testpassword')
        #self.user.save()
        #self.client.login(username='test', password='testpassword')
        #Image.init()
	self.assertTrue(False)
