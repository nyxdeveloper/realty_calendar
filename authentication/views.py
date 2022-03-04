from rest_framework.views import APIView

from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate

from .models import User

from .serializers import UserSerializer

from realty_calendar.settings import EMAIL_HOST_USER
from realty_calendar.settings import EMAIL_HOST_PASSWORD

from .appfunc import get_auth_payload
from .appfunc import get_token
# from .appfunc import verify_pin
# from .appfunc import send_pin

from django.core.mail import send_mail

import random
import re

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib

from django.db import transaction


# class PhoneAuthAPIView(APIView):
#     def post(self, request):
#         phone = request.data.get('phone')
#
#         if not phone:
#             return Response({'error': 'Укажите номер телефона.'}, status=400)
#         phone = phone.replace('+', '')
#         pin = request.data.get('pin')
#
#         if pin:
#             if verify_pin(phone=phone, pin=pin):
#                 if User.objects.filter(phone=phone).exists():
#                     return get_auth_payload(user=User.objects.get(phone=phone), request=request)
#                 return get_auth_payload(user=User(phone=phone).save(), request=request)
#             return Response({'error': 'Неверный пин.'}, status=400)
#         return send_pin(phone=phone)


class AuthAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            resp = {}
            if not email:
                resp['email'] = 'Укажите Email'
            if not password:
                resp['password'] = 'Укажите пароль.'
            return Response(resp, status=400)

        test = User.objects.filter(email=email)

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Пользователь не зарегистрирован'}, status=401)
        if user.is_anonymous:
            return Response({'error': 'Пользователь не зарегистрирован'}, status=401)

        return get_auth_payload(user, request)


class RegAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        repeat_password = request.data.get('repeat_password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone = request.data.get('phone')

        if not email or not password or not repeat_password or not first_name or not last_name or not phone:
            resp = {}
            if not email:
                resp['email'] = 'Укажите Email.'
            if not password:
                resp['password'] = 'Укажите пароль.'
            if not repeat_password:
                resp['repeat_password'] = 'Подтвердите пароль.'
            if not first_name:
                resp['first_name'] = 'Укажите имя.'
            if not last_name:
                resp['last_name'] = 'Укажите фамилию.'
            if not phone:
                resp['phone'] = 'Укажите номер телефона.'
            return Response(resp, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'email': 'Данный Email уже зарегистрирован в системе.'}, status=400)

        if User.objects.filter(phone=phone).exists():
            return Response({'phone': 'Данный номер телефона уже зарегистрирован в системе.'}, status=400)

        if password != repeat_password:
            return Response({'repeat_password': 'Пароли не совпадают.'}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({'email': 'Данный Email уже зарегистрирован в системе.'})

        if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone) is None:
            return Response({'phone': 'Введите корректное значение.'}, status=400)

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone
        )
        user.set_password(password)
        user.save()

        return get_auth_payload(user, request)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        SMTP_SERVER = "smtp.mail.ru"
        SMTP_PORT = 465
        SMTP_USER = "NaSutkiCalendar@mail.ru"
        SMTP_PASSWORD = "f2YnZ6LJ3QBfmktVd2SF"
        to_email = request.data.get('email')
        if not User.objects.filter(email=to_email, is_active=True).exists():
            return Response({'error': 'Пользователь не зарегистрирован'}, status=401)
        user = User.objects.get(email=to_email, is_active=True)
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            password = ''
            for i in range(8):
                password += random.choice('*!&$#@abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890')
            user.set_password(password)
            user.save()
            msg = MIMEMultipart()
            msg["Subject"] = 'Новый пароль'
            msg["From"] = SMTP_USER
            msg["To"] = to_email
            msg.attach(MIMEText(f'Добрый день, ваш новый пароль: {password}'))
            server.sendmail(SMTP_USER, [to_email], msg.as_string())
        return Response({'success': 'Письмо с новым паролем отправлено на почту.'})


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def put(self, request):
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        password = request.data.get('password')
        repeat_password = request.data.get('repeat_password')
        current_password = request.data.get('current_password')

        user = self.request.user

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({'email': 'Пользова тель с такой почтой уже существует.'}, status=400)
            user.email = email
        if phone:
            if re.match('^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$', phone) is None:
                return Response({'phone': 'Введите корректное значение.'}, status=400)
            if User.objects.filter(phone=phone).exclude(id=user.id).exists():
                return Response({'phone': 'Пользова тель с таким номером телефона уже существует.'}, status=400)
            user.phone = phone
        if password:
            if not current_password:
                return Response({'current_password': 'Введите текущий пароль.'}, status=400)
            current_user = authenticate(email=user.email, password=current_password)
            if current_user is None:
                return Response({'current_password': 'Неверный пароль.'}, status=400)
            if current_user.pk != user.pk:
                return Response({'current_password': 'Неверный пароль.'}, status=400)
            if not repeat_password:
                return Response({'repeat_password': 'Подтвердите пароль.'}, status=400)
            if password != repeat_password:
                return Response({'repeat_password': 'Пароли не совпадают'}, status=400)
            user.set_password(password)

        user.save()

        data = UserSerializer(user).data
        if email:
            data['token'] = get_token(user, request)

        return Response(data)


class FixAPIView(APIView):
    def get(self, request):
        from django.utils import timezone
        import datetime
        User.objects.update(subscription=timezone.now().date() + datetime.timedelta(days=365))
        return Response({"detail": "Subscription update"})
