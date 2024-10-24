from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from documents import models as document_models, serializers as document_serializers
from pagination import StandardResultsSetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        return document_models.Payment.objects.filter(agreement__customer__user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = document_serializers.payment.PaymentSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False)
    def month_statistic(self, request):
        start_date = datetime.now() - timedelta(days=30)
        payment_records = document_models.Payment.objects.with_check().filter(
            created_at__gte=start_date).values('id', 'created_at', 'amount')

        serializer = document_serializers.payment.StatisticSerializer(payment_records, many=True)
        return Response(serializer.data)


__all__ = ['PaymentViewSet']
