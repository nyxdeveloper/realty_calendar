from django.utils import timezone
import re


def set_blacklist_date(sender, instance, **kwargs):
    if instance.blacklist:
        instance.date_blacklist_added = timezone.now()


def set_valid_number(sender, instance, **kwargs):
    for i in ['+', ' ', '(', ')', '-']:
        if i in instance.phone:
            phone = instance.phone.replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace(' ', '')
            if phone[0] == '8' and len(phone) > 10:
                phone = re.sub('8', '7', phone, 1)
            instance.phone = phone
            instance.save()
