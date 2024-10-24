from django_filters.rest_framework import DjangoFilterBackend

from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class InvoiceViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.InvoiceSerializer
    model_class = document_models.Invoice
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number']


__all__ = ['InvoiceViewSet']
