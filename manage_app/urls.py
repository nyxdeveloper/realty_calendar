from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import TenantViewSet
from .views import RentViewSet
from .views import FlatViewSet
from .views import UserViewSet

urlpatterns = [

]

router = DefaultRouter()

router.register('tenants', TenantViewSet)
router.register('rents', RentViewSet)
router.register('flats', FlatViewSet)
router.register('users', UserViewSet)

urlpatterns += router.urls
