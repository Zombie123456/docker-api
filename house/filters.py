import django_filters

from house.models import House, CarSet


class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = House
        fields = '__all__'


class CarSetFilter(django_filters.FilterSet):

    set_num = django_filters.CharFilter(field_name='set_num', lookup_expr='icontains')

    class Meta:
        model = CarSet
        fields = '__all__'
