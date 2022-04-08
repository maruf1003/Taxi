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
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)

from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as goe_models

point = goe_models.PointField(null=True, spatial_index=True, geography=True, blank=True)

class Company(models.Model):
    point = goe_models.PointField(null=True, spatial_index=True, geography=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Companies"
        # ordering = ['order']

    def save(self, *args, **kwargs):
        if self.point != None:
            self.latitude = self.point.y
            self.longitude = self.point.x

        elif self.longitude != None and self.latitude != None:
            self.point = Point(float(self.longitude), float(self.latitude), srid=4326)

        super(Company, self).save(*args, **kwargs)

