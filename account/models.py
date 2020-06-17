from django.contrib.auth.models import User
from django.db import models


class Role(models.Model):

    MANAGER = 'manager'
    SELLER = 'seller'
    STAFF = 'staff'

    name = models.CharField(max_length=100, null=True, blank=True)
    key = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Staff(models.Model):
    STAFF_INACTIVE = 0
    STAFF_ACTIVE = 1
    STAFF_STATUS_OPTIONS = (
        (STAFF_INACTIVE, 'Inactive'),
        (STAFF_ACTIVE, 'Active'),
    )

    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE,
                                related_name='staff_user')
    memo = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL,
                                   related_name='staff_created_by')
    status = models.IntegerField(default=1, null=True, choices=STAFF_STATUS_OPTIONS)
    role = models.ForeignKey(Role, null=True, on_delete=models.SET_NULL, blank=True)

    def __str__(self):
        return self.user.username

    @property
    def is_manager(self):
        return self.role.key == Role.MANAGER

    @property
    def is_seller(self):
        return self.role.key == Role.SELLER

    @property
    def is_staff(self):
        return self.role.key == Role.STAFF
