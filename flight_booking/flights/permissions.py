from rest_framework import permissions


class IsSuperUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """
        allows only super users to create, edit and delete a flight.
        Other users are allow to view flights
        :param request:
        :param view:
        :param obj:
        :return:
        """
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff



