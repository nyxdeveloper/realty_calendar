from django.core.mail import send_mail

from realty_calendar.settings import EMAIL_HOST_USER


def send_rent_mail(sender, instance, **kwargs):
    if not instance.send_mail:
        email = instance.tenant.email
        if email is not None and email != '':
            owner_data = ''
            if instance.user.first_name:
                owner_data += instance.user.first_name
                if instance.user.last_name:
                    owner_data += ' ' + instance.user.last_name
                if instance.user.phone:
                    owner_data += ' ' + str(instance.user.phone)
            else:
                owner_data += str(instance.user.phone)
            subject = 'Для вас забронирована квартира'
            message = f'Добрый день, {instance.tenant.name}\n' \
                      f'Для вас забронирована квартира.\n' \
                      f'Адрес: {instance.flat.address}\n' \
                      f'Стоимость одной ночи: {instance.flat.cost_per_night} руб.\n' \
                      f'Полная стоимость: {instance.total_cost} руб.\n' \
                      f'Дата въезда: {instance.start.strftime("%d.%m.%Y")} в {instance.start.strftime("%H:%M")}' \
                      f'Дата выезда: {instance.end.strftime("%d.%m.%Y")} в {instance.end.strftime("%H:%M")}' \
                      f'\n\n' \
                      f'Данные владельца: {owner_data}'

            send_mail(subject, message, EMAIL_HOST_USER, [email])
            instance.send_mail = True
            instance.save()
