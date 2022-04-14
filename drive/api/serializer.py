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
        fields = ['name', 'driver_avatar', 'car_number', 'car_name', 'ReviewDriver', ]

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


# Pay Click
class ClickUzSerializer(serializers.Serializer):
    click_trans_id = serializers.CharField(allow_blank=True)
    service_id = serializers.CharField(allow_blank=True)
    merchant_trans_id = serializers.CharField(allow_blank=True)
    merchant_prepare_id = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    amount = serializers.CharField(allow_blank=True)
    action = serializers.CharField(allow_blank=True)
    error = serializers.CharField(allow_blank=True)
    error_note = serializers.CharField(allow_blank=True)
    sign_time = serializers.CharField()
    sign_string = serializers.CharField(allow_blank=True)
    click_paydoc_id = serializers.CharField(allow_blank=True)


# TellMe

# class TellMeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TellMe
#         fields = "__all__"
#
#
# # I  left an item
# class ILeftSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TellMe
#         fields = ['massage']
