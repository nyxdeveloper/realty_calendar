from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import BlacklistAPIView
from .views import CheckTenantAPIView
from .views import UploadBlacklistAPIView
from .views import Fix

urlpatterns = [
    path('upload_blacklist/', UploadBlacklistAPIView.as_view()),
    path('check/<str:tenant_phone>/', CheckTenantAPIView.as_view()),
    path('blacklist/', BlacklistAPIView.as_view()),
    path('fix/', Fix.as_view()),
]

router = DefaultRouter()

urlpatterns += router.urls
