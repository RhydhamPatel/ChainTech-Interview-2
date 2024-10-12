from rest_framework import permissions

class IsOrganizerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.organizer == request.user

class IsInvitedOrPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_public:
            return True
        # Implement logic to check if the user is invited
        return False