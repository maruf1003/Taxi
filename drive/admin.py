from django.contrib import admin
from drive.models import *
from django.contrib.gis.admin import OSMGeoAdmin

class DriverAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Driver,DriverAdmin)
admin.site.register(Order)
admin.site.register(Car_type)
admin.site.register(ReviewDriver)


class LocationAdmin(OSMGeoAdmin):
    default_lon = 7474999
    default_lat = 4931196
    default_zoom = 5

    class Meta:
        model = Location
admin.site.register(Location,LocationAdmin)
