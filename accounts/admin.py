from django.contrib.gis import admin
from .models import School, CustomUser

@admin.register(School)
class SchoolAdmin(admin.OSMGeoAdmin):
    list_display = ("name", "location")

@admin.register(CustomUser)
class SchoolAdmin(admin.OSMGeoAdmin):
    list_display = ("username", "location")
