from rest_framework import permissions
from django.utils.translation import ugettext_lazy as _


class IsManager(permissions.BasePermission):
    message = _('只有管理员才可以访问')

    def has_permission(self, request, view):
        user = request.user

        return user.is_authenticated and user.staff_user.is_manager


class IsStaff(permissions.BasePermission):
    message = _('只有后勤人员可以访问')

    def has_permission(self, request, view):
        user = request.user

        return user.is_authenticated and user.staff_user.is_staff


class IsSeller(permissions.BasePermission):
    message = _('销售人员只可以查看数据')

    def has_permission(self, request, view):
        user = request.user

        return user.is_authenticated and user.staff_user.is_seller and request.method in permissions.SAFE_METHODS
