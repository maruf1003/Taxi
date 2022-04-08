from rest_framework import serializers
from django.db.models import Avg, Sum, Count
from drive.models import *


class OrderCreatSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class DriverSerializers(serializers.ModelSerializer):
    ReviewDriver = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['name', 'driver_avatar', 'car_number', 'car_name', 'ReviewDriver',]

    def get_ReviewDriver(self, obj):
        return ReviewDriver.objects.filter(driver=obj).aggregate(Avg('stars'), Sum('stars'), Count('stars'))


class Car_typeSerializers(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Car_type
        fields = "__all__"

    def get_total_price(self, obj):
        return obj.price * self.context['langht']

class LocationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"
