
from rest_framework import permissions


class ManagerAllEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "GET", "POST")

    def has_permission(self, request, view):
        # return True
        if request.user.is_authenticated:
            #return True
            if request.user.is_superuser:
                return True
            if str(request.user) == "manager":
                return True
            # return False
            #return False

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     # if request.user != "admin":
    #     #     return False
    #
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     if obj.author == request.user:
    #         return True
    #
    #     if request.user.is_staff and request.method not in self.edit_methods:
    #         return True
    #
    #     return False


class WorkerAllEditOrReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH", "GET", "POST")

    def has_permission(self, request, view):
        # return True
        if request.user.is_authenticated:
            #return True
            if request.user.is_superuser:
                return True
            if str(request.user) == "worker":
                return True
            # return False
            #return False

    # def has_object_permission(self, request, view, obj):
    #     if request.user.is_superuser:
    #         return True
    #
    #     # if request.user != "admin":
    #     #     return False
    #
    #     if request.method in permissions.SAFE_METHODS:
    #         return True
    #
    #     if obj.author == request.user:
    #         return True
    #
    #     if request.user.is_staff and request.method not in self.edit_methods:
    #         return True
    #
    #     return False