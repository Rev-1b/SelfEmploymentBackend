from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from customers.models import CustomerRequisites
from customers.serializers import CustomerRequisitesSerializer
from project.pagination import StandardResultsSetPagination


class CustomerRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bank_name',]

    def get_queryset(self):
        # Можно убрать проверку на пользователя, так как заказчик уже уникальный
        queryset = CustomerRequisites.objects.filter(customer__user=self.request.user)
        if self.action != 'create':
            return queryset.filter(customer=self.kwargs.get('customer_pk'))
        return queryset


__all__ = ['CustomerRequisitesViewSet']
