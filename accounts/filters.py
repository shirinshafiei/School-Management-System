from rest_framework import filters

class IsCourseTeacherFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        user = request.user
        if user.is_teacher():
            return queryset.filter(teacher=user)
        return queryset.none()

