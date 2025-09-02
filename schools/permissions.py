from rest_framework import permissions

class IsCourseTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = getattr(obj, "course", None)

        if course is None:
            return False

        return request.user.has_perm("change_course", course)

class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        course = obj.exercise.course

        return course.students.filter(pk=user.pk).exists()