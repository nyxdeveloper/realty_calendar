from django.db import models

from tenants.models import Tenant

from realty_calendar.settings import AUTH_USER_MODEL


class Flat(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    short_name = models.CharField(verbose_name='Короткое название', max_length=100)
    address = models.TextField(verbose_name='Адресс', null=True, blank=True)
    cost_per_night = models.FloatField(verbose_name='Стоимость за ночь', default=None, null=True, blank=True)
    comment = models.TextField(verbose_name='Примечание', blank=True, default='')

    @property
    def rents_count(self):
        return self.rent_set.all().count()

    class Meta:
        verbose_name = 'Квартира'
        verbose_name_plural = 'Квариры'

    def __str__(self):
        return self.short_name


class Rent(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    tenant = models.ForeignKey(Tenant, verbose_name='Съемщик', on_delete=models.SET_NULL, null=True, default=None,
                               blank=False)
    flat = models.ForeignKey(Flat, verbose_name='Квартира', on_delete=models.CASCADE)
    start = models.DateTimeField(verbose_name='Начало')
    end = models.DateTimeField(verbose_name='Конец')
    cost_per_night = models.FloatField(verbose_name='Цена за ночь', default=None, null=True, blank=True)
    paid = models.FloatField(verbose_name='Заплачено', default=None, null=True, blank=True)
    deposit = models.FloatField(verbose_name='Залог', default=None, null=True, blank=True)
    total_cost = models.FloatField(verbose_name='Полная стоимость', default=None, null=True, blank=True)
    color = models.CharField(verbose_name='Цвет', max_length=50)
    comment = models.TextField(verbose_name='Коментарий', blank=True, default='')

    send_mail = models.BooleanField(verbose_name='Письмо отправлено', default=False)

    class Meta:
        verbose_name = 'Аренда'
        verbose_name_plural = 'Аренды'

    def __str__(self):
        return self.flat.short_name


from django.db.models import signals

from .signals import send_rent_mail

signals.post_save.connect(send_rent_mail, sender=Rent)
