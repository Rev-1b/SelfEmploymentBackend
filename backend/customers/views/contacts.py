from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from customers.models import CustomerContacts
from customers.serializers import CustomerContactsSerializer
from customers.views.common import get_customer_id
from pagination import StandardResultsSetPagination


class CustomerContactsViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerContactsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_type',]

    def get_queryset(self):
        # Swagger
        if getattr(self, 'swagger_fake_view', False):
            return CustomerContacts.objects.none()

        customer = get_customer_id(self)
        return CustomerContacts.objects.filter(customer__user=self.request.user, customer=customer)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('customer_id', openapi.IN_QUERY, description="ID of the customer", type=openapi.TYPE_STRING, required=True)
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


__all__ = ['CustomerContactsViewSet']
