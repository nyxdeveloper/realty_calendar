import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, AuthenticationFailed


def custom_permission_denied_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if isinstance(exc, AuthenticationFailed):
        custom_response_data = {"detail": "Ошибка авторизации."}
        response.data = custom_response_data
        response.status_code = 401

    # checks if the raised exception is of the type you want to handle
    if isinstance(exc, PermissionDenied):
        # defines custom response data
        err_data = {'error': 'Доступ запрещен. Продлите подписку или обратитесь к администратору.'}

        # logs detail data from the exception being handled
        logging.error(f"Original error detail and callstack: {exc}")
        # returns a JsonResponse
        return Response(err_data, status=403)

    # returns response as handled normally by the framework
    return response
