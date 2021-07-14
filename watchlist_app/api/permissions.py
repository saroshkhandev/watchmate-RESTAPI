from rest_framework import permissions


# This permission is for Owner can only Edit
# here we have to pass obj because obj contains that particular review fields from the queryset
class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user or request.user.is_staff
        # True or False based on the condition whether the author and the 
        # request user is same.

# This permission is for Admin can only edit

class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        admin_permission = bool(request.user and request.user.is_staff)
        return request.method == 'GET' or admin_permission