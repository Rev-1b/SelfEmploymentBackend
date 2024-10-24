from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from customers.models import CustomerRequisites
from customers.serializers import CustomerRequisitesSerializer
from customers.views.common import get_customer_id
from pagination import StandardResultsSetPagination


class CustomerRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank_name',]

    def get_queryset(self):
        # Swagger
        if getattr(self, 'swagger_fake_view', False):
            return CustomerRequisites.objects.none()

        queryset = CustomerRequisites.objects.filter(customer__user=self.request.user)
        if self.action != 'create':
            customer = get_customer_id(self)
            return queryset.filter(customer=customer)
        return queryset

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('customer_id', openapi.IN_QUERY, description="ID of the customer", type=openapi.TYPE_STRING, required=True)
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


__all__ = ['CustomerRequisitesViewSet']
