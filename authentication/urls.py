from .views import AuthAPIView
from .views import RegAPIView
# from .views import PhoneAuthAPIView
from .views import ResetPasswordAPIView
from .views import ProfileAPIView
from .views import FixAPIView

from django.urls import path

urlpatterns = [
    path('auth/', AuthAPIView.as_view()),
    path('reg/', RegAPIView.as_view()),
    path('profile/', ProfileAPIView.as_view()),
    path('password_reset/', ResetPasswordAPIView.as_view()),
    path('fix/', FixAPIView.as_view()),
]
