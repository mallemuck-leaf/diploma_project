from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrUserIDOnly(BasePermission):

    # def has_permission(self, request, view):
    #     if request.user.is_staff:
    #         return bool(request.user and request.user.is_staff)
    #     return obj.user == request.user

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user
