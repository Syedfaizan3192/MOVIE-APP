from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):

    # admin  can added but user can read only permissions
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

        # admin_permission = bool(request.user and request.user.is_staff)
        # return request.method == "GET" or admin_permission


class ReviewUSerOrReadOnly (permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff
