from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as goe_models


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
    # mobile_phone = models.CharField(max_length=100, default='', null=True)


# point = goe_models.PointField(null=True, spatial_index=True, geography=True, blank=True)


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


class FaqCategory(models.Model):
    name = models.CharField(max_length=200, default='', null=False)
    order = models.IntegerField(default=0)


class Faq(models.Model):
    title = models.CharField(max_length=200, default='', null=False)
    desc = models.CharField(max_length=255, default='', null=True)
    status = models.IntegerField(default=0)
    faqCategory = models.ForeignKey(FaqCategory, on_delete=models.CASCADE, null=True, blank=True)
