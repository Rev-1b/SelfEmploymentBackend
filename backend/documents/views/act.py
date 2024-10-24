from django_filters.rest_framework import DjangoFilterBackend

from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class ActViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.ActSerializer
    model_class = document_models.Act
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number', 'title']


__all__ = ['ActViewSet']
