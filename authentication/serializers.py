from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'email',
            'first_name',
            'last_name',
            'manager'
        )


class UserManageSerializer(serializers.ModelSerializer):
    flats_count = serializers.ReadOnlyField()
    subscription = serializers.DateField(format='%d.%m.%Y', input_formats=['%d.%m.%Y'])
    date_joined = serializers.DateTimeField(format='%d.%m.%Y %H:%M', input_formats=['%d.%m.%Y %H:%M'])

    class Meta:
        model = User
        fields = (
            'id',
            'phone',
            'email',
            'is_active',
            'subscription',
            'manager',
            'date_joined',
            'first_name',
            'last_name',
            'comment',
            'flats_count'
        )
