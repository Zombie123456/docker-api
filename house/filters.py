import django_filters

from house.models import House, BuildNum


class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = House
        fields = '__all__'


class BuildNumFilter(django_filters.FilterSet):
    class Meta:
        model = BuildNum
        fields = '__all__'
