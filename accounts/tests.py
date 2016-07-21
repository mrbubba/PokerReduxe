from django.test import TestCase

from accounts.models import Register
from accounts.views import register
from django.contrib.auth.models import User


Class AccountsTestCase(TestCase):

    def test_register(self):
        """Can we create a user??  or as Jared said does our register function even mean shit"""
        user_name = 'BobaFet'
        password = 'Fuckoff'


