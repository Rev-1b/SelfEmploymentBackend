from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from customers.models import Customer
from customers.serializers import CustomerInfoSerializer, CustomerDetailSerializer
from documents.views import ListNumberSearchMixin
from project.pagination import StandardResultsSetPagination


class CustomerViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer_type',]
    search_fields = ['customer_name']

    def get_queryset(self):
        return Customer.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = CustomerInfoSerializer if self.action in ['list', 'search'] else CustomerDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['CustomerViewSet']
