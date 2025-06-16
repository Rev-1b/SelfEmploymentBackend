from django_filters.rest_framework import DjangoFilterBackend

from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class InvoiceViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.InvoiceSerializer
    model_class = document_models.Invoice
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'search':
            serializer_class = document_serializers.InvoiceInfoSerializer
        else:
            serializer_class = document_serializers.InvoiceSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['InvoiceViewSet']
