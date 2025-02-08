from django.db import models
from django.contrib.auth.models import AbstractUser
from user.managers import UserManager


# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(
        "Email Address",
        unique=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email
