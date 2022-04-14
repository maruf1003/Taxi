from django.contrib import admin
from drive.models import *
from django.contrib.gis.admin import OSMGeoAdmin

admin.site.register(Order)
admin.site.register(Car_type)
admin.site.register(ReviewDriver)
admin.site.register(Transaction)
admin.site.register(TellMe)
admin.site.register(TellMeType)


class DriverAdmin(OSMGeoAdmin):
    default_lon = 7474999
    default_lat = 4931196
    default_zoom = 5
    list_display = ['name']

    class Meta:
        model = Driver


admin.site.register(Driver, DriverAdmin)


class LocationAdmin(OSMGeoAdmin):
    default_lon = 7474999
    default_lat = 4931196
    default_zoom = 5

    class Meta:
        model = Location


admin.site.register(Location, LocationAdmin)
