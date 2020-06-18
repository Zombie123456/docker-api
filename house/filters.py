import django_filters

from house.models import House


class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = House
        fields = '__all__'
