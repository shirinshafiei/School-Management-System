from rest_framework import permissions


class IsProfileOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'user'):
            return False
        is_owner = (obj.user == request.user)
        return is_owner

class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'system_admin'

class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'teacher'

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'