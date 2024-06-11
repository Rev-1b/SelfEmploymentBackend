from django.urls import path, include
from rest_framework import routers

from .views import AgreementViewSet, AdditionalViewSet

router = routers.DefaultRouter()
router.register('agreements', AgreementViewSet)
router.register('additional', AdditionalViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
