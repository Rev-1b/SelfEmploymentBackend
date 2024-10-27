from django.urls import path, include
from rest_framework_nested import routers

from customers.views import CustomerViewSet, CustomerContactsViewSet, CustomerRequisitesViewSet

router = routers.DefaultRouter()
router.register('', CustomerViewSet, basename='customers')

# Вложенный роутер для контактов и реквизитов, связанных с заказчиком
customers_router = routers.NestedDefaultRouter(router, '', lookup='customer')
customers_router.register('contacts', CustomerContactsViewSet, basename='customer-contacts')
customers_router.register('requisites', CustomerRequisitesViewSet, basename='customer-requisites')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(customers_router.urls)),
]