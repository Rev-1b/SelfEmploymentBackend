from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions

from documents import models as document_models, serializers as document_serializers
from documents.views.common import ListNumberSearchMixin, get_master_id
from project.pagination import StandardResultsSetPagination


class AdditionalViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number', 'title']

    def get_queryset(self):
        # Swagger
        if getattr(self, 'swagger_fake_view', False):
            return document_models.Additional.objects.none()

        agreement_id, _ = get_master_id(self).values()
        agreement_additional = document_models.Additional.objects.filter(agreement=agreement_id).order_by('-updated_at')
        return agreement_additional.with_sums() if self.action in ['retrieve', 'list'] else agreement_additional

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = document_serializers.AdditionalMainPageSerializer
        elif self.action == 'retrieve':
            serializer_class = document_serializers.AdditionalRetrieveSerializer
        elif self.action == 'search':
            serializer_class = document_serializers.AdditionalInfoSerializer
        else:
            serializer_class = document_serializers.AdditionalCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('agreement_id', openapi.IN_QUERY, description="ID of linked agreement",
                          type=openapi.TYPE_STRING, required=True)
    ])
    def list(self, request, *args, **kwargs):
        return super(AdditionalViewSet, self).list(request, *args, **kwargs)


__all__ = ['AdditionalViewSet']