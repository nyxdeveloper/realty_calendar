from rest_framework import permissions

from django.utils import timezone


class IsSubscriptionOrOnlyGet(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.subscription >= timezone.now().date() or request.user.manager:
            return True
        if request.method == 'GET':
            return True
        return False


class IsSubscription(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.subscription >= timezone.now().date() or request.user.manager:
            return True
        return False


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.manager:
            return True
        return False
