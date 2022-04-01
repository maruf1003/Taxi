from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255, default="")
    sms_code = models.IntegerField(null=True)
