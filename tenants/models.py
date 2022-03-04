from django.db import models

from realty_calendar.settings import AUTH_USER_MODEL

from django.db.models.signals import pre_save

from .signals import set_blacklist_date
from .signals import set_valid_number


class Tenant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=15, blank=True, null=True)
    name = models.CharField(verbose_name='Имя', max_length=100)
    email = models.CharField(verbose_name='Email', max_length=100, blank=True, null=True)
    comment = models.TextField(verbose_name='Примечание', blank=True, null=True)
    blacklist = models.BooleanField(verbose_name='Черный список', default=False, blank=True)
    date_blacklist_added = models.DateTimeField(verbose_name='Дата добавления в черный список', default=None, null=True,
                                                blank=True)

    class Meta:
        verbose_name = 'Съемщик'
        verbose_name_plural = 'Съемщики'
        ordering = ['-id', '-date_blacklist_added']
        # unique_together = ["phone", "user"]

    def __str__(self):
        return self.name


pre_save.connect(set_blacklist_date, sender=Tenant)
pre_save.connect(set_valid_number, sender=Tenant)
