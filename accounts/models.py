from django.db import models
from django.contrib.auth.models import User


class Register(models.Model):

    user_name = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=25)

    def __str__(self):
        return self.user_name
