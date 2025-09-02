from rest_framework import filters

class StudentEnrolledFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        user = request.user
        if queryset.model.__name__ == "Course":
            return queryset.filter(students=user).distinct()

        if hasattr(queryset.model, "course"):
            return queryset.filter(course__students=user).distinct()

        return queryset.none()
