from requests import request

from .sms_notifications_config import SMS_SEND_URL
from .sms_notifications_config import SMS_SIGN_DEFAULT


def send_sms_to_number(message, phone, sign=SMS_SIGN_DEFAULT):
    url = SMS_SEND_URL + '?text=%s&number=%s&sign=%s' % (message, phone, sign)
    return request(method='GET', url=url)
