from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from electroshop.accounts.managers import StoreUserManager


class StoreUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    object = StoreUserManager()


class Profile(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=30)
    address = models.TextField()
    telephone = models.CharField(max_length=20)
    user = models.OneToOneField(StoreUser, on_delete=models.CASCADE, primary_key=True)


from .signals import *
