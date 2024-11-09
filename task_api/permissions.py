from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrUserIDOnly(BasePermission):

    # def has_permission(self, request, view):
    #     if request.user.is_staff:
    #         return bool(request.user and request.user.is_staff)
    #     return obj.user == request.user

    def has_object_permission(self, request, view, obj):
        print(request.user.username)
        if request.user.is_staff:
            return True
        # return obj.user == request.user
        return obj.user == request.user


class IsAuthenticatedOrCreateOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in ('POST', 'GET'):
            return True
        if request.user.is_authenticated:
            return True
        return False
