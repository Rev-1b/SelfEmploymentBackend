from django.urls import path, include
from rest_framework import routers

from customers.views import CustomerViewSet, CustomerContactsViewSet, CustomerRequisitesViewSet

router = routers.DefaultRouter()
router.register('', CustomerViewSet, 'customers')
router.register('contacts', CustomerContactsViewSet, 'customer-contacts')
router.register('requisites', CustomerRequisitesViewSet, 'customer-requisites')

urlpatterns = [
    path('', include(router.urls)),
]
