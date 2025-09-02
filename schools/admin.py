from django.contrib import admin
from .models import Course,Exercise, News, Submissions

admin.site.register(Course)
admin.site.register(Exercise)
admin.site.register(News)
admin.site.register(Submissions)
