from django.contrib.auth.models import AbstractUser
from django.db import models


def get_avatar(instance, filename):
    return "users/%s" % (filename)


# Create your models here.


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=255, default="")
    sms_code = models.IntegerField(null=True)
    avatar = models.ImageField(null=True, upload_to=get_avatar, default='users/default.png')
    complete = models.IntegerField(default=0)
    langtude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)


