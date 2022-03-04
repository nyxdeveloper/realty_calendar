from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Tenant


class TenantSerializer(ModelSerializer):
    # user = serializers.ReadOnlyField()

    class Meta:
        model = Tenant
        fields = '__all__'
