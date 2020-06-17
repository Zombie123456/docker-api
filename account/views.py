from rest_framework import viewsets, mixins
from django.contrib.auth.models import User

from account.models import Staff
from loginsvc.permissions import IsStaff, IsManager, IsSeller
from account.serializers import StaffSerializer
from account.filters import StaffFilter


class StaffViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.all()
    permission_classes = [IsManager]
    serializer_class = StaffSerializer
    filter_class = StaffFilter
