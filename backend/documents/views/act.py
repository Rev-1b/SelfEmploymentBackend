from django_filters.rest_framework import DjangoFilterBackend

from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class ActViewSet(CommonDocumentViewSet):
    model_class = document_models.Act
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number', 'title']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'search':
            serializer_class = document_serializers.ActInfoSerializer
        else:
            serializer_class = document_serializers.ActSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['ActViewSet']
