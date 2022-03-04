from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import status

from rest_framework.response import Response

from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.permissions import IsAuthenticated

from .appfunc import parse_forever
from rents.appfunc import get_valid_phone

from .models import Tenant

from .serializers import TenantSerializer

from realty_calendar.paginators import StandardResultsSetPagination

from rents.appfunc import get_valid_phone

from realty_calendar.permissions import IsSubscription
import re
# import pandas as pd
# import os
# from django.http.response import FileResponse


class BlacklistAPIView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsSubscription, ]
    queryset = Tenant.objects.filter(blacklist=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = StandardResultsSetPagination
    filterset_fields = ['blacklist']
    search_fields = ['phone', 'email', 'name', 'comment']
    ordering_fields = ['id', 'phone', 'email', 'name', 'comment']
    serializer_class = TenantSerializer

    def get_queryset(self):
        qs = self.queryset
        if self.request.query_params.get('phone'):
            phone = self.request.query_params.get('phone').replace(' ', '').replace('+', '').replace('(', '').replace(
                ')', '').replace('-', '')
            qs = qs.filter(phone=phone)
            if phone[0] == '8':
                phone[0] = '7'
                qs = qs and self.queryset.filter(phone=phone)
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        TenantSerializer(data=data).is_valid(raise_exception=True)

        data['phone'] = get_valid_phone(data['phone'])
        data['user'] = request.user.id

        if not Tenant.objects.filter(phone=data['phone'], user_id=request.user.id).exists():
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        else:
            tenant = Tenant.objects.get(user_id=request.user.id, phone=data['phone'])
            tenant.name = data['name']
            tenant.blacklist = True
            if data['email']:
                tenant.email = data['email']
            if data['comment']:
                tenant.comment = data['comment']
            tenant.user = request.user
            tenant.save()
            serializer = TenantSerializer(tenant)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CheckTenantAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, tenant_phone):
        phone = get_valid_phone(tenant_phone)
        response = {
            'tenant': None,
            'blacklist': []
        }

        if Tenant.objects.filter(user_id=request.user.id, phone=phone).exists():
            response['tenant'] = TenantSerializer(Tenant.objects.get(user_id=request.user.id, phone=phone),
                                                  many=False).data

        if Tenant.objects.filter(phone=phone, blacklist=True).exists():
            for tenant in Tenant.objects.filter(phone=phone, blacklist=True):
                response['blacklist'].append(TenantSerializer(tenant, many=False).data)
            if not response['tenant']:
                response['tenant'] = response['blacklist'][0]

        return Response(response)


class UploadBlacklistAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, requests):
        parse_forever()
        return Response({'success': 'Черный список обновляется.'})


class Fix(APIView):
    def get(self, request):
        # for i in Tenant.objects.all():
        #     phone = i.phone
        #     phone = phone.replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace(' ', '')
        #     if phone[0] == '8' and len(phone) > 10:
        #         re.sub('8', '7', phone, 1)
        #     i.phone = phone
        #     i.save()

        # from authentication.models import User
        #
        # for i in User.objects.all():
        #     id_list = i.tenant_set.order_by().distinct("phone").values_list("id")
        #     i.tenant_set.exclude(id__in=id_list).delete()

        # resp = []
        # for i in Tenant.objects.values_list("id", "user", "phone", "name", "email"):
        #     group = {
        #         "invalid": None,
        #         "valid": []
        #     }
        #     if i[2] != '':
        #         if i[2][0] == "8":
        #             valid_phone = i[2]
        #             valid_phone = re.sub('8', '7', valid_phone, 1)
        #             group["invalid"] = {
        #                 "id": i[0],
        #                 "user": i[1],
        #                 "phone": i[2],
        #                 "name": i[3],
        #                 "email": i[4]
        #             }
        #             for j in Tenant.objects.filter(phone=valid_phone).values_list("id", "user", "phone", "name",
        #                                                                           "email"):
        #                 group["valid"].append({
        #                     "id": j[0],
        #                     "user": j[1],
        #                     "phone": j[2],
        #                     "name": j[3],
        #                     "email": j[4]
        #                 })
        #             if len(group["valid"]) > 0:
        #                 resp.append(group)

        # return Response({"fix": "success"})

        # resp = []
        # for i in Tenant.objects.all():
        #     if i.rent_set.count() > 0:
        #         resp.append({
        #             "id": i.pk,
        #             "user": i.user_id,
        #             "name": i.name,
        #             "phone": i.phone,
        #             "email": i.email,
        #             "rents": [rent_id for rent_id in i.rent_set.values_list("id", flat=True)],
        #         })
        #
        # df = pd.DataFrame({
        #     'ID': [i['id'] for i in resp],
        #     'USER': [i['user'] for i in resp],
        #     'NAME': [i['name'] for i in resp],
        #     'PHONE': [i['phone'] for i in resp],
        #     'EMAIL': [i['email'] for i in resp],
        #     'RENTS': [str(i['rents']) for i in resp]
        # })
        #
        # return FileResponse(df.to_excel("tenants.xlsx", engine='xlsxwriter', sheet_name='TENANTS', index=False),
        #                     as_attachment=True)

        # for i in Tenant.objects.all():
        #     i.phone = get_valid_phone(i.phone)
        #     i.save()
        return Response("finish")
