from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from rest_framework import filters

class IsCourseTeacherFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_teacher():
            return queryset.filter(teacher=user)
        return queryset.none()

from django.contrib.gis.db.models.functions import Distance

class NearbySchoolsFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if not user.location:
            return queryset.none()

        user_location = user.location

        max_distance = 5000
        return queryset.annotate(
            distance=Distance('location', user_location)
        ).filter(distance__lte=max_distance).order_by('distance')
