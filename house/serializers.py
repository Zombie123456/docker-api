from rest_framework import serializers

from house.models import House, BuildNum, CarSet
from demo.lib import constans


class BuildNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuildNum
        fields = '__all__'


class HouseManagerSerializer(serializers.ModelSerializer):
    build_num_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = House
        fields = '__all__'
        depth = 1

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
        field = 'is_full_money'
        if data.get(field) is None:
            ret.pop(field, None)
        return ret


class HouseStaffSerializer(serializers.ModelSerializer):

    floor = serializers.IntegerField(read_only=True)
    room_num = serializers.CharField(read_only=True)
    area = serializers.CharField(read_only=True)
    unit_type = serializers.CharField(read_only=True)
    unit_price = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
    memo = serializers.CharField(read_only=True)
    sela_staff = serializers.CharField(read_only=True, source='sela_staff.user.username')
    build_num = BuildNumSerializer(read_only=True)

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


class CarSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarSet
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        staff = request.user.staff_user
        status = data.get('status')
        if request.method == 'PUT':
            if status is not None and self.instance.status in {CarSet.Sign, CarSet.FULL_MONEY} and staff.is_staff:
                raise serializers.ValidationError({constans.NOT_OK: '已签约的车位状态只有管理员才能修改'})

        return data

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)
        field = 'is_full_money'
        if data.get(field) is None:
            ret.pop(field, None)
        return ret


class CarStaffSerializer(serializers.ModelSerializer):
    floor = serializers.IntegerField(read_only=True)
    set_num = serializers.CharField(read_only=True)
    set_type = serializers.CharField(read_only=True)
    price = serializers.CharField(read_only=True)
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
        if status is not None and status not in {CarSet.CAN_SELA, CarSet.CONTROL}:
            raise serializers.ValidationError({constans.NOT_OK: '车位状态只能修改为 可售车位 或 销控车位'})

        return data

    def update(self, instance, validated_data):
        request = self.context['request']
        instance = super().update(instance, validated_data)
        if instance.status == CarSet.CAN_SELA:
            instance.sela_staff = None
        else:
            instance.sela_staff = request.user.staff_user
        instance.save()
        return instance
