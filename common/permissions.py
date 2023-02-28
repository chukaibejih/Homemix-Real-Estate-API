from rest_framework import permissions

class IsSellerOReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow write permissions only if the user is the seller of the property
        return obj.seller == request.user