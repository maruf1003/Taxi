from django.db import models
from django.utils.timezone import now

from taxi.models import CustomUser


class Car_type(models.Model):
    name = models.CharField(max_length=50, default='', null=False)
    price = models.FloatField(default=0)


class Driver(models.Model):
    name = models.CharField(max_length=200, default='', null=False)
    car_name = models.CharField(max_length=100, default='', null=False)
    driver_avatar = models.ImageField(default='threads/default.png')
    car_number = models.CharField(max_length=20, default='', null=False)
    car_color = models.CharField(max_length=100, default='', null=False)
    car_type = models.ForeignKey(Car_type, on_delete=models.CASCADE, null=False, default='')
    phone = models.IntegerField(default='', null=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, default='')
    # review_driver = models.ForeignKey(ReviewDriver, on_delete=models.CASCADE, null=False, default='')


class ReviewDriver(models.Model):
    stars = models.IntegerField(default=False)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False, default='')
    message = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as goe_models
point = goe_models.PointField(null=True, spatial_index=True, geography=True, blank=True)

class Location(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False, default='')
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    point = goe_models.PointField(null=True, spatial_index=True, geography=True, blank=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name_plural = "Location"
        # ordering = ['order']

    def save(self, *args, **kwargs):
        if self.point != None:
            self.latitude = self.point.y
            self.longitude = self.point.x

        elif self.longitude != None and self.latitude != None:
            self.point = Point(float(self.longitude), float(self.latitude), srid=4326)

        super(Location, self).save(*args, **kwargs)






class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, default='')
    from_longitude = models.FloatField(default=0)
    from_latitude = models.FloatField(default=0)
    to_longitude = models.FloatField(default=0)
    to_latitude = models.FloatField(default=0)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=True, default='')
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=now)
    status = models.IntegerField()
    car_type = models.ForeignKey(Car_type, on_delete=models.CASCADE, null=True, default='')
