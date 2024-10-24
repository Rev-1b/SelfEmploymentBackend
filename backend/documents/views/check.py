from documents import serializers as document_serializers, models as document_models
from documents.views.common import CommonDocumentViewSet


class CheckViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.CheckSerializer
    model_class = document_models.CheckModel
    search_fields = ['number']


__all__ = ['CheckViewSet']
