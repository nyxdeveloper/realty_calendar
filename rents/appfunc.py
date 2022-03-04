import re


def get_valid_phone(phone):
    ret_phone = phone.replace('(', '').replace(')', '').replace('+', '').replace('-', '').replace(' ', '')
    if ret_phone[0] == '8' and len(ret_phone) > 10:
        ret_phone = re.sub('8', '7', ret_phone, 1)
    return ret_phone
