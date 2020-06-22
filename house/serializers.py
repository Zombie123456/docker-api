from rest_framework import serializers

from house.models import House, BuildNum, Community, ImportLog
from demo.lib import constans


class BuildNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildNum
        fields = '__all__'


class HouseManagerGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'room_num', 'floor')


class HouseManagerSerializer(serializers.ModelSerializer):
    build_num_id = serializers.IntegerField(write_only=True, required=False)
    is_car = serializers.ReadOnlyField()

    class Meta:
        model = House
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        staff = request.user.staff_user
        status = data.get('status')
        if request.method == 'PUT':
            if status is not None and self.instance.status in {House.Sign, House.FULL_MONEY} and staff.is_staff:
                raise serializers.ValidationError({constans.NOT_OK: '已签约的房源状态只有管理员才能修改'})

        return data

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        fields = ['is_full_money', 'is_car']
        for field in fields:
            if data.get(field) is None:
                ret.pop(field, None)
        return ret


class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'


class ImportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportLog
        fields = '__all__'
