import re

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers

from account.models import Staff, Role
from demo.lib import constans


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    role = RoleSerializer(required=False)
    created_by = serializers.ReadOnlyField(source='created_by.username')
    role_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Staff
        fields = '__all__'

    def to_internal_value(self, data):
        ret = super().to_internal_value(data)

        ret['password'] = data.get('password')
        ret['username'] = data.get('username')
        return ret

    def validate(self, data):
        data = super().validate(data)
        request = self.context.get('request')
        if request.method == 'POST':
            if not data['password']:
                raise serializers.ValidationError({'password': 'This field is required.'})
        if data['username'] is not None and not re.match('^[a-zA-Z0-9]{5,15}$', data['username']):
            raise serializers.ValidationError({constans.NOT_OK: '用户名必须为5-15位的英数字'})

        pk = self.instance.user.pk if self.instance else None
        if User.objects.filter(username__iexact=data['username']).exclude(pk=pk).exists():
            raise serializers.ValidationError({constans.NOT_OK: '用户名已经存在'})

        if request.method == 'POST' or data.get('role_id') is not None:
            if not Role.objects.filter(id=data.get('role_id', 0)).exists():
                raise serializers.ValidationError({constans.NOT_OK: '身份 id 不存在'})

        return data

    def update(self, instance, validated_data):
        if validated_data.get('username'):
            instance.user.username = validated_data['username']
            instance.user.save()

        if validated_data.get('password'):
            new_password = validated_data['password']
            instance.user.set_password(new_password)
            instance.user.save()

        return super().update(instance, validated_data)

    def create(self, validated_data):
        request = self.context['request']
        creator = request.user
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        with transaction.atomic():
            user = User.objects.create_user(username=username,
                                            password=password,
                                            email=None)
            validated_data['user'] = user
            validated_data['created_by'] = creator
            staff = Staff.objects.create(**validated_data)

        return staff

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['username'] = instance.user.username
        return ret
