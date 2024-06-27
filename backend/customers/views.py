
from rest_framework import permissions
from rest_framework import viewsets

from customers.models import Customer
from customers.serializers import CustomerListSerializer, CustomerDetailSerializer
from project.pagination import StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = CustomerListSerializer if self.action == 'list' else CustomerDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


