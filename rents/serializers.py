from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from django.db.models import Q

from .models import Rent
from .models import Flat

from tenants.serializers import TenantSerializer


class FlatSerializer(ModelSerializer):
    rents_count = serializers.ReadOnlyField()

    # user = serializers.ReadOnlyField()

    class Meta:
        model = Flat
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if len(self.context) > 0:
            month = self.context['request'].query_params.get('month')
        else:
            month = None
        if not month:
            return data
        try:
            data['rents_count'] = Flat.objects.get(id=self.data['id']).rent_set.filter(
                (Q(start__month=month) | Q(end__month=month))).count()
        except:
            pass
        return data


class RentSerializer(ModelSerializer):
    _tenant = TenantSerializer(many=False, read_only=True, source='tenant')
    _flat = FlatSerializer(many=False, read_only=True, source='flat')

    tenant_phone = serializers.SlugRelatedField(many=False, read_only=True, slug_field='phone', source='tenant')
    tenant_name = serializers.SlugRelatedField(many=False, read_only=True, slug_field='name', source='tenant')
    tenant_email = serializers.SlugRelatedField(many=False, read_only=True, slug_field='email', source='tenant')

    # start = serializers.DateTimeField(input_formats=['%d.%m.%Y'], format='%d.%m.%Y')
    # end = serializers.DateTimeField(input_formats=['%d.%m.%Y'], format='%d.%m.%Y')

    start = serializers.DateTimeField(format='%d.%m.%Y %H:%M', input_formats=['%d.%m.%Y %H:%M'])
    end = serializers.DateTimeField(format='%d.%m.%Y %H:%M', input_formats=['%d.%m.%Y %H:%M'])

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if len(self.context) > 0:
            if self.context['request'].query_params.get('expand') is not None:
                data['start_time'] = data['start'].split(' ')[1]
                data['end_time'] = data['end'].split(' ')[1]

                data['start'] = data['start'].split(' ')[0]
                data['end'] = data['end'].split(' ')[0]
        return data

    class Meta:
        model = Rent
        fields = '__all__'
