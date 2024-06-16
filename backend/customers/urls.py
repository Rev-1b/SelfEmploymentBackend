from django.urls import path, include
from rest_framework import routers

from customers.views import CustomerDetailViewSet

router = routers.DefaultRouter()
router.register('', CustomerDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
