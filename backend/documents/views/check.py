from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class CheckViewSet(CommonDocumentViewSet):
    model_class = document_models.CheckModel
    search_fields = ['number']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'search':
            serializer_class = document_serializers.CheckInfoSerializer
        else:
            serializer_class = document_serializers.CheckSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['CheckViewSet']
