from tenants.models import Tenant
from tenants.serializers import TenantSerializer

from rents.models import Rent
from rents.models import Flat
from rents.serializers import RentSerializer
from rents.serializers import FlatSerializer

from authentication.models import User
from authentication.serializers import UserManageSerializer

from realty_calendar.permissions import IsManager

from rest_framework.viewsets import ModelViewSet

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class UserViewSet(ModelViewSet):
    permission_classes = [IsManager, ]
    queryset = User.objects.all()
    serializer_class = UserManageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['is_active', 'subscription', 'manager', 'date_joined']
    search_fields = ['phone', 'email', 'first_name', 'last_name', 'comment']
    ordering_fields = [
        'id', 'phone', 'email', 'first_name', 'last_name', 'is_active', 'subscription', 'manager', 'date_joined',
        'comment'
    ]


class RentViewSet(ModelViewSet):
    permission_classes = [IsManager, ]
    queryset = Rent.objects.all()
    serializer_class = RentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['user', 'tenant', 'flat', 'start', 'end', 'start_time', 'end_time']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__phone', 'user__email', 'tenant__name', 'tenant__phone',
        'tenant__email', 'flat__short_name', 'flat__address', 'flat__comment', 'comment'
    ]
    ordering_fields = [
        'user', 'tenant', 'flat', 'start', 'end', 'start_time', 'end_time', 'user__first_name', 'user__last_name',
        'user__phone', 'user__email', 'tenant__name', 'tenant__phone', 'tenant__email', 'flat__short_name',
        'flat__address', 'flat__comment', 'comment', 'start', 'end', 'start_time', 'end_time', 'cost_per_night', 'paid',
        'deposit', 'total_cost', 'color', 'comment'
    ]


class FlatViewSet(ModelViewSet):
    permission_classes = [IsManager, ]
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['user']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__phone', 'user__email', 'short_name', 'address', 'comment'
    ]
    ordering_fields = [
        'id', 'user', 'user__first_name', 'user__last_name', 'user__phone', 'user__email', 'short_name', 'address',
        'comment', 'cost_per_night'
    ]


class TenantViewSet(ModelViewSet):
    permission_classes = [IsManager, ]
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    filterset_fields = ['user', 'blacklist']
    search_fields = [
        'user__first_name', 'user__last_name', 'user__phone', 'user__email', 'phone', 'name', 'email', 'comment'
    ]
    ordering_fields = [
        'user', 'blacklist', 'user__first_name', 'user__last_name', 'user__phone', 'user__email', 'phone', 'name',
        'email', 'comment'
    ]
