from django.contrib import admin
from taxi.models import *

# Register your models here.

admin.site.register(CustomUser)  # User
from django.contrib.gis.admin import OSMGeoAdmin

class CompanyAdmin(OSMGeoAdmin):



    default_lon = 7474999
    default_lat = 4931196
    default_zoom = 5


    class Meta:
        model = Company
admin.site.register(Company,CompanyAdmin)  # User
