from rest_framework import permissions
from rest_framework import viewsets

from customers.models import Customer, CustomerRequisites, CustomerContacts
from customers.serializers import CustomerListSerializer, CustomerDetailSerializer, CustomerRequisitesSerializer, \
    CustomerContactsSerializer
from project.pagination import StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

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

    def get_queryset(self):
        return CustomerRequisites.objects.filter(customer__user=self.request.user)


class CustomerContactsViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerContactsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return CustomerContacts.objects.filter(customer__user=self.request.user)
