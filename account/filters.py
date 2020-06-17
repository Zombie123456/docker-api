import django_filters

from account.models import Staff


class StaffFilter(django_filters.FilterSet):
    class Meta:
        model = Staff
        fields = '__all__'
