from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, exceptions
from rest_framework import viewsets

from customers.models import Customer, CustomerRequisites, CustomerContacts
from customers.serializers import CustomerListSerializer, CustomerDetailSerializer, CustomerRequisitesSerializer, \
    CustomerContactsSerializer
from project.pagination import StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer_type',]

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = CustomerListSerializer if self.action == 'list' else CustomerDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CustomerRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank_name',]

    def get_queryset(self):
        queryset = CustomerRequisites.objects.filter(customer__user=self.request.user)
        if self.action != 'create':
            customer = get_customer_id(self)
            return queryset.filter(customer=customer)
        return queryset


class CustomerContactsViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerContactsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contact_type',]

    def get_queryset(self):
        customer = get_customer_id(self)
        return CustomerContacts.objects.filter(customer__user=self.request.user, customer=customer)


def get_customer_id(self):
    customer_id = self.request.query_params.get('customer_id', None)

    if customer_id is None:
        raise exceptions.ValidationError(f'No "customer_id" specified in request parameters')
    return customer_id