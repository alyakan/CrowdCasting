from rest_framework import permissions
from main.models import Actor


class IsStaffOrTargetUser(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow user to list all users if logged in user is staff
        return view.action == 'retrieve' or request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # allow logged in user to view own details, allows staff to view all
        # records
        return request.user.is_staff or obj == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            actor = Actor.objects.get(user_id=request.user.id)
            return obj.actor.id == actor.id
        except:
            pass


class IsSuperUserOrTargetUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.method in permissions.SAFE_METHODS
        else:
            return True
