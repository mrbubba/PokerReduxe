from django.test import TestCase
from django.contrib.auth.models import User

from accounts.forms import RegisterForm


# Create your tests here.
class TestForms(TestCase):
    def test_register_form(self):
        """ does our register form even function properly """
        form = RegisterForm({"password":"password", "user_name":"Jared"})
        self.assertTrue(form.is_valid())

    def test_no_password(self):
        """ do we fail appropriately if user did not submit a password? """
        form = RegisterForm({"password":"", "user_name":"Mark"})
        self.assertFalse(form.is_valid())

    def test_no_user_name(self):
        """ do we fail appropriately if user did not submit a user name? """
        form = RegisterForm({"password":"password", "user_name":""})
        self.assertFalse(form.is_valid())
