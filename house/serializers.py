from rest_framework import serializers

from house.models import House, BuildNum
from demo.lib import constans


class HouseManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        staff = request.user.staff_user
        status = data.get('status')
        if request.method == 'PUT':
            if status is not None and self.instance.status in {House.Sign, House.FULL_MONEY} and staff.is_staff:
                raise serializers.ValidationError({constans.NOT_OK: '已签约的房源状态不允许修改'})

        return data


class HouseStaffSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    info = serializers.CharField(read_only=True)
    room_num = serializers.CharField(read_only=True)
    area = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    memo = serializers.CharField(read_only=True)
    sela_staff = serializers.CharField(read_only=True, source='sela_staff.user.username')

    class Meta:
        model = House
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        field = 'is_full_money'
        if data.get(field) is None:
            ret.pop(field, None)
        return ret

    def validate(self, data):
        status = data.get('status')
        if status is not None and status not in {House.CAN_SELA, House.CONTROL}:
            raise serializers.ValidationError({constans.NOT_OK: '房源状态只能修改为 可售房源 或 销控房源'})

        return data

    def update(self, instance, validated_data):
        request = self.context['request']
        instance = super().update(instance, validated_data)
        if instance.status == House.CAN_SELA:
            instance.sela_staff = None
        else:
            instance.sela_staff = request.user.staff_user
        instance.save()
        return instance


class BuildNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildNum
        fields = '__all__'
