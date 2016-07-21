from django.test import TestCase
from django.contrib.auth.models import User

# Create your tests here.

from accounts.models import Register


class AccountsTestCase(TestCase):

    def setup(self):
        Register.objects.create("Jared", "Password")
        Register.objects.create("Mark", "Password2")

    def register_test(self):
        """ Can we create a user in django DB with register function """
        Register.objects.create("Jared", "Password").save()
        Register.objects.create("Mark", "Password2").save()
        jared = User.objects.get("Jared")
        mark = User.objects.get("Mark")
        self.assertEqual(jared.password, "Password")
        self.assertEqual(mark.password, "Password2")
