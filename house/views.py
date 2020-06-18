from rest_framework import viewsets, mixins
from rest_condition import Or

from house.models import House, BuildNum
from house.serializers import HouseManagerSerializer, HouseStaffSerializer, BuildNumSerializer
from house.filters import StaffFilter
from loginsvc.permissions import IsSeller, IsManager, IsStaff, ReadOnly
from demo.utils import CampaignRenderer


class HouseViewSet(viewsets.ModelViewSet):
    model = House
    queryset = House.objects.all()
    serializer_class = HouseManagerSerializer
    permission_classes = [Or(IsManager, IsStaff)]
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]


class HouseStaffViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.RetrieveModelMixin):

    model = House
    queryset = House.objects.filter(status=House.CAN_SELA)
    serializer_class = HouseStaffSerializer
    permission_classes = [Or(IsSeller, IsManager, IsStaff)]
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]

    def get_queryset(self):
        if self.request.GET.get('my_sale_house'):
            return House.objects.filter(sela_staff=self.request.user)
        return self.queryset


class BuildNumViewSet(viewsets.ModelViewSet):
    model = BuildNum
    queryset = BuildNum.objects.all()
    permission_classes = [Or(IsStaff, IsManager, ReadOnly)]
    serializer_class = BuildNumSerializer
