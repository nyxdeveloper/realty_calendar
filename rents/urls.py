from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import RentViewSet
from .views import FlatViewSet
from .views import ColorsAPIView
from .views import FixAPIView

urlpatterns = [
    path('fix/', FixAPIView.as_view()),
    path('colors/', ColorsAPIView.as_view())
]

router = DefaultRouter()

router.register('rents', RentViewSet)
router.register('flats', FlatViewSet)

urlpatterns += router.urls
