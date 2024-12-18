from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from documents import models as document_models, serializers as document_serializers
from project.pagination import StandardResultsSetPagination


class PaymentViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        queryset = document_models.Payment.objects.filter(agreement__customer__user=self.request.user)
        if self.action == 'list':
            queryset = queryset.select_related('agreement', 'agreement__customer', 'act')
        elif self.action == 'retrieve':
            queryset = queryset.select_related(
                'agreement', 'agreement__customer', 'additional', 'act', 'check_link', 'invoice'
            )
        # elif self.action == 'statistic':
        #     queryset = queryset.select_related('agreement', 'agreement__customer')
        else:
            queryset = queryset

        return queryset

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = document_serializers.payment.ListPaymentSerializer
        elif self.action == 'statistic':
            serializer_class = document_serializers.payment.StatisticSerializer
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            serializer_class = document_serializers.payment.CUDPaymentSerializer
        else:
            serializer_class = document_serializers.payment.ReadPaymentSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def paginate_queryset(self, queryset):
        if self.action == 'statistic':
            return queryset
        return super().paginate_queryset(queryset)

    @action(detail=False)
    def statistic(self, request):
        period = request.query_params.get('period', 'month').lower()

        if period == 'week':
            start_date = datetime.now() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.now() - timedelta(days=30)
        elif period == 'year':
            start_date = datetime.now() - timedelta(days=365)
        else:
            raise ValidationError({'detail': 'Invalid period. Choose from "week", "month", or "year".'})

        # todo: Probably should use with_check manager method
        payment_records = document_models.Payment.objects.filter(
            created_at__gte=start_date)

        serializer = self.get_serializer(payment_records, many=True)
        return Response(serializer.data)


__all__ = ['PaymentViewSet']
