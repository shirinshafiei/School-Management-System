from rest_framework import permissions

from schools.models import Course


class IsCourseTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        course = getattr(obj, "course", None)

        if course is None:
            return False

        return request.user.has_perm("change_course", course)

class IsCourseTeacherOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            course_id = request.data.get("course")
            return request.user.has_perm("change_course", Course.objects.get(id=course_id))

        return True

    def has_object_permission(self, request, view, obj):
        course = getattr(obj, "course", None)
        if not course:
            return False

        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.has_perm("change_course", course) or
                request.user in course.students.all()
            )

        return request.user.has_perm("change_course", course)

class IsEnrolledStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user.is_authenticated:
            return False

        course = obj.exercise.course

        return course.students.filter(pk=user.pk).exists()