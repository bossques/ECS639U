from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


# Create your models here.

class User(AbstractUser):
    profile_image = models.ImageField(null=True)
    date_of_birth = models.DateField(default=now)
    email = models.EmailField(unique=True)
