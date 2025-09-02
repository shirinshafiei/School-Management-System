from rest_framework import permissions

from schools.models import Course
from .models import Exercise

class IsCourseTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            course_id = request.data.get("course")
            if not course_id:
                return False
            try:
                course = Course.objects.get(id=course_id)
                return request.user.has_perm("change_course", course)
            except Course.DoesNotExist:
                return False

        return True

    def has_object_permission(self, request, view, obj):
        course = getattr(obj, 'course', None)
        if not course:
            return False

        return request.user.has_perm("change_course", course)


class IsEnrolledStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method == "POST":
            exercise_id = request.data.get("exercise")
            if not exercise_id:
                return False

            try:
                exercise = Exercise.objects.get(id=exercise_id)
                return request.user in exercise.course.students.all()
            except Exercise.DoesNotExist:
                return False
        return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if obj.student != request.user:
            return False

        return request.user in obj.exercise.course.students.all()
