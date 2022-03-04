import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.utils import timezone

from .validators import validate_phone

from django.db.models.signals import post_save

from django.db import models
from django.db import transaction
from django.core.validators import EmailValidator

import uuid


class UserManager(BaseUserManager):

    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given username must be set')
        try:
            with transaction.atomic():
                user = self.model(phone=phone, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self._create_user(phone, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(verbose_name='Номер телефона', null=False, unique=True,
                             max_length=15, validators=[validate_phone])
    email = models.EmailField(verbose_name='Email', null=False, unique=True, validators=[EmailValidator])
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    subscription = models.DateField(default=timezone.now().date() + datetime.timedelta(days=133))
    manager = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    comment = models.TextField(verbose_name='Коментарий', default='', blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self

    def __str__(self):
        return self.name

    @property
    def name(self):
        if not self.first_name and not self.last_name:
            return 'USER_' + str(self.pk)
        return self.first_name + ' ' + self.last_name

    @property
    def flats_count(self):
        return self.flat_set.count()


class Email(models.Model):
    email = models.CharField(verbose_name='Почта', max_length=100)
    active = models.BooleanField(verbose_name='Активная', default=True)

    class Meta:
        verbose_name = 'Почта'
        verbose_name_plural = 'Почта для рассылки'
        ordering = ['-id']

    def __str__(self):
        return self.email


class Pin(models.Model):
    phone = models.CharField(max_length=13, primary_key=True, unique=True, db_index=True)
    code = models.IntegerField()

    class Meta:
        verbose_name = 'Пин'
        verbose_name_plural = 'Пинкоды'

    def __str__(self):
        return '%s === %s' % (self.phone, self.code)
