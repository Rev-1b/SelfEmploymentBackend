from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, exceptions
from rest_framework import viewsets

from customers.models import Customer, CustomerRequisites, CustomerContacts
from customers.serializers import CustomerListSerializer, CustomerDetailSerializer, CustomerRequisitesSerializer, \
    CustomerContactsSerializer
from project.pagination import StandardResultsSetPagination
from documents.views import ListNumberSearchMixin


class CustomerViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer_type',]
    search_fields = ['customer_name']

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = CustomerListSerializer if self.action in ['list', 'search'] else CustomerDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


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


def get_customer_id(self):
    customer_id = self.request.query_params.get('customer_id', None)
    if customer_id is None:
        raise exceptions.ValidationError(f'No "customer_id" specified in request parameters')
    return customer_id