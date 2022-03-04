from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from django.db.models import Q
from django.db import transaction

from django_filters.rest_framework import DjangoFilterBackend

from .models import Rent
from .models import Flat

from .serializers import RentSerializer
from .serializers import FlatSerializer

from .appfunc import get_valid_phone

from tenants.serializers import TenantSerializer

from tenants.models import Tenant

from realty_calendar.paginators import StandardResultsSetPagination

from realty_calendar.permissions import IsSubscriptionOrOnlyGet

import datetime
import re

from calendar import monthrange
from datetime import timedelta

from django.utils import timezone


class RentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsSubscriptionOrOnlyGet, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['tenant', 'flat', 'start', 'end']
    search_fields = ['tenant__name', 'flat__short_name', 'flat__address', 'tenant__phone', 'tenant__email']
    ordering_fields = ['start', 'end', 'cost_per_night', 'paid', 'deposit', 'total_cost']
    queryset = Rent.objects.all()
    serializer_class = RentSerializer

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        month = request.query_params.get('month')
        year = request.query_params.get('year')
        if month and year:
            month = int(month)
            year = int(year)
            days_count = monthrange(year, month)[1]
            """
            Попадает под фильтр если дата начала 
            входит в указанный месяц
            """
            start_in_month = Q(start__range=[datetime.datetime(year, month, 1, 0, 0),
                                             datetime.datetime(year, month, days_count, 23, 59)])
            """
            Попадает под фильтр если дата конца 
            входит в указанный месяц
            """
            end_in_month = Q(end__range=[datetime.datetime(year, month, 1, 0, 0),
                                         datetime.datetime(year, month, days_count, 23, 59)])
            """
            Попадает под фильтр если дата начала 
            меньше начала указанного месяца, а дата 
            конца больше (если квартира занята 
            дольше чем на месяц)
            """
            over_month = Q(start__lte=datetime.datetime(year, month, 1, 0, 0),
                           end__gte=datetime.datetime(year, month, days_count, 23, 59))

            """
            Фильтрация по месяцу и году
            """
            queryset = queryset.filter(start_in_month | end_in_month | over_month)

            # queryset = queryset.filter(
            #     (Q(start__year=int(year)) |
            #      Q(end__year=int(year)) |
            #      Q(start__year__lt=int(year), end__year__gt=int(year))) &
            #     (Q(start__month=int(month)) |
            #      Q(end__month=int(month)) |
            #      Q(start__month__lt=int(month), end__month__gt=int(month)))
            # )

        if not year and not month:
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({"results": serializer.data})

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data

        """
            Автоматическое присваивание пользователя из запроса в 
            создаваемый объект.
        """
        data['user'] = request.user.pk

        """
            Если дата начала будет позже даты конца, будет выдан 
            400 BAD_REQUEST.
        """

        date_start = datetime.datetime.strptime(str(data['start']), '%d.%m.%Y %H:%M')
        date_end = datetime.datetime.strptime(str(data['end']), '%d.%m.%Y %H:%M')

        if date_start.date() >= date_end.date():
            return Response({'error': 'Дата начала и конца аренды не могут совпадать.'}, status=400)

        date_start = datetime.datetime.strftime(date_start, '%Y-%m-%d %H:%M:%S.%f%z')
        date_end = datetime.datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S.%f%z')

        """
            Проверка квартиры на наличие аренды на указанное время.
            Если на данную квартиру существует аренда, начинающаяся 
            раньше установленного конца или заканчивающаяся позже 
            установленного начала, будет выдан 404 BAD_REQUEST. 
        """

        if self.get_queryset().filter(flat_id=data['flat'], end__range=[date_start, date_end]).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)
        elif self.get_queryset().filter(flat_id=data['flat'], start__range=[date_start, date_end]).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)
        elif self.get_queryset().filter(flat_id=data['flat'], start__lte=date_start, end__gte=date_end).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)

        """
            Проверка наличия пользователя с указанными данными в базе 
            данных пользователя. Если пользователь не найден по номеру 
            телефона, создается новый пользователь, если нет, берется 
            существующий.
        """

        phone = get_valid_phone(data['tenant_phone'])

        if not Tenant.objects.filter(phone=phone, user_id=request.user.id).exists():
            new_tenant = {}
            new_tenant['name'] = data['tenant_name']
            new_tenant['user'] = request.user.id
            new_tenant['email'] = data['tenant_email']
            new_tenant['phone'] = phone
            tenant = TenantSerializer(data=new_tenant)
            tenant.is_valid(raise_exception=True)
            tenant.save()
            data['tenant'] = tenant.instance.id
        else:
            tenant = Tenant.objects.get(user_id=request.user.id, phone=phone)
            tenant.name = data['tenant_name']
            tenant.email = data['tenant_email']
            tenant.phone = phone
            tenant.save()
            data['tenant'] = tenant.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        data = request.data

        """
            Автоматическое присваивание пользователя из запроса в 
            создаваемый объект.
        """
        data['user'] = request.user.pk

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        date_start = datetime.datetime.strptime(str(data['start']), '%d.%m.%Y %H:%M')
        date_end = datetime.datetime.strptime(str(data['end']), '%d.%m.%Y %H:%M')

        if date_start.date() >= date_end.date():
            return Response({'error': 'Дата начала и конца аренды не могут совпадать.'}, status=400)

        date_start = datetime.datetime.strftime(date_start, '%Y-%m-%d %H:%M:%S.%f%z')
        date_end = datetime.datetime.strftime(date_end, '%Y-%m-%d %H:%M:%S.%f%z')

        """
            Проверка квартиры на наличие аренды на указанное время.
            Если на данную квартиру существует аренда, кроме изменяемой, 
            начинающаяся, раньше установленного конца или заканчивающаяся 
            позже установленного начала, будет выдан 404 BAD_REQUEST. 
        """

        if self.get_queryset().exclude(id=instance.id).filter(flat_id=data['flat'],
                                                              end__range=[date_start, date_end]).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)
        elif self.get_queryset().exclude(id=instance.id).filter(flat_id=data['flat'],
                                                                start__range=[date_start, date_end]).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)
        elif self.get_queryset().exclude(id=instance.id).filter(flat_id=data['flat'], start__lte=date_start,
                                                                end__gte=date_end).exists():
            return Response({'error': 'На данное время квартира занята. Сдвиньте дату или время аренды.'}, status=400)

        """
            Проверка наличия пользователя с указанными данными в базе 
            данных пользователя. Если пользователь не найден по номеру 
            телефона, создается новый пользователь, если нет, берется 
            существующий.
        """

        phone = get_valid_phone(data['tenant_phone'])

        if not Tenant.objects.filter(phone=phone, user_id=request.user.id).exists():
            new_tenant = {}
            new_tenant['user'] = request.user.id
            new_tenant['name'] = data['tenant_name']
            new_tenant['email'] = data['tenant_email']
            new_tenant['phone'] = phone
            tenant = TenantSerializer(data=new_tenant)
            tenant.is_valid(raise_exception=True)
            tenant.save()
            data['tenant'] = tenant.instance.id
        else:
            tenant = Tenant.objects.get(user_id=request.user.id, phone=phone)
            tenant.name = data['tenant_name']
            tenant.email = data['tenant_email']
            tenant.phone = phone
            tenant.save()
            data['tenant'] = tenant.pk

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        return Response(serializer.data)


class FlatViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, IsSubscriptionOrOnlyGet, ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, ]
    pagination_class = StandardResultsSetPagination
    filterset_fields = []
    search_fields = ['short_name', 'address']
    ordering_fields = ['id', 'cost_per_night']
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.pk
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.pk
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # refresh the instance from the database.
            instance = self.get_object()
            serializer = self.get_serializer(instance)

        return Response(serializer.data)


class ColorsAPIView(APIView):
    def get(self, request):
        return Response([
            'FFDEAD',
            'F4A460',
            'FA8072',
            'ADD8E6',
            'DDA0DD',
            '9ACD32'
        ])


class FixAPIView(APIView):
    def get(self, request):
        # for i in Rent.objects.filter(tenant__user__isnull=True):
        #     tenant = i.tenant
        #     tenant.user = i.user
        #     tenant.save()
        return Response()
