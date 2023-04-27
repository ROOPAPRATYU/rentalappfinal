from rest_framework.permissions import BasePermission, BasePermissionMetaclass, SAFE_METHODS

class OwnerOrReadObly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user == obj.owner.is_owner