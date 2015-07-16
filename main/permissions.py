from rest_framework import permissions
from main.models import Actor, Biography, ProfilePicture


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
        return obj.actor.id == request.user.id


class CanPostBio(permissions.BasePermission):

    """
    Permission to restrict actor from posting more than one Biography .
    Author : Kareem Tarek.
    """

    def has_permission(self, request, view):
        actor = Actor.objects.get(user=request.user)
        bio = Biography.objects.filter(actor=actor)
        if bio:
            return request.method not in 'POST'
        else:
            return True


class UserIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.method in permissions.SAFE_METHODS
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.actor.id == request.user.id


class IsSuperUserOrTargetUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return request.method in permissions.SAFE_METHODS
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.actor.id == request.user.id


class IsPhotoUploaded(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            actor = Actor.objects.get(user_id=request.user.id)
            img = ProfilePicture.objects.get(actor=actor)
        except:
            img = 0
        if request.user and request.user.is_authenticated():
            if img:
                return request.method not in ['POST', ]
        else:
            return request.method in permissions.SAFE_METHODS
        return True

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            actor = Actor.objects.get(user_id=request.user.id)
            return obj.actor_id == actor.id
        except:
            return False
