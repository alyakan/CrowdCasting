from rest_framework import permissions
from main.models import Actor, Biography


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
