from django.contrib import admin
from .models import CustomUser  ,School

admin.site.register(CustomUser)
# admin.site.register(Teacher)
# admin.site.register(Student)
admin.site.register(School)
