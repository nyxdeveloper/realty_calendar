# from django.core.cache import cache
#
# from .models import Pin
#
# from notifications.appfunc import send_sms_to_number

from django.contrib.auth import user_logged_in

from rest_framework.response import Response
from rest_framework import status

from rest_framework_jwt.serializers import jwt_payload_handler

from realty_calendar import settings

from .serializers import UserSerializer

# import random
import jwt


# def get_pin(length=5):
#     return random.sample(range(10 ** (length - 1), 10 ** length), 1)[0]
#
#
# def verify_pin(phone, pin):
#     if Pin.objects.filter(phone=phone).exists():
#         return pin == Pin.objects.get(phone=phone).code
#     return False
#
#
# def send_pin(phone):
#     if settings.DEBUG:
#         Pin(phone=phone, code=1111).save()
#         return Response({'success': 'Сообщение с кодом отправлено на номер %s' % phone})
#     pin = get_pin()
#
#     if Pin.objects.filter(phone=phone).exists():
#         Pin.objects.get(phone=phone).delete()
#
#     Pin(phone=phone, code=pin).save()
#
#     resp = send_sms_to_number(message='code: %s' % pin, phone=phone)
#     if resp.status_code != 200:
#         return Response({'error': 'Введенный номер телефона не валиден.'}, status=400)
#     return Response({'success': 'Сообщение с кодом отправлено на номер %s' % phone})


def get_auth_payload(user, request):
    try:
        payload = jwt_payload_handler(user)
        token = jwt.encode(payload, settings.SECRET_KEY)
        user_logged_in.send(sender=user.__class__, request=request, user=user)
        user_data = UserSerializer(user).data
        return Response({"token": token, "user": user_data}, status=status.HTTP_200_OK)
    except Exception as e:
        raise e


def get_token(user, request):
    token = jwt.encode(jwt_payload_handler(user), settings.SECRET_KEY)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return token
