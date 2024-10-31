from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from customers.models import CustomerContacts
from customers.serializers import CustomerContactsSerializer
from project.pagination import StandardResultsSetPagination


class CustomerContactsViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerContactsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_type',]

    def get_queryset(self):
        # Swagger
        # if getattr(self, 'swagger_fake_view', False):
        #     return CustomerContacts.objects.none()

        # Можно убрать проверку на пользователя, так как заказчик уже уникальный
        return CustomerContacts.objects.filter(customer__user=self.request.user, customer=self.kwargs.get('customer_pk'))

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


__all__ = ['CustomerContactsViewSet']
