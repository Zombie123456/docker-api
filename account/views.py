from rest_framework import viewsets, status
from rest_framework.response import Response


from account.models import Staff
from loginsvc.permissions import IsStaff, IsManager, IsSeller
from account.serializers import StaffSerializer
from account.filters import StaffFilter
from demo.utils import CampaignRenderer


class StaffViewSet(viewsets.ModelViewSet):
    model = Staff
    queryset = Staff.objects.all()
    permission_classes = [IsManager]
    serializer_class = StaffSerializer
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        user.delete()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
