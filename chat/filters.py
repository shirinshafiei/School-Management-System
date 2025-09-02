from rest_framework import filters
from django.db.models import Q

class UserMessagesFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if not user.is_authenticated:
            return queryset.none()
        return queryset.filter(Q(sender=user) | Q(receiver=user))
