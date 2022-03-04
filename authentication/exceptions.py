from rest_framework.exceptions import APIException


class InvalidPhoneException(APIException):
    status_code = 400
    default_detail = {"error": "Неверный формат номера телефона."}
