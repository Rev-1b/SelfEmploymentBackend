from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from documents import models as document_models, serializers as document_serializers
from documents.views.common import ListNumberSearchMixin
from pagination import StandardResultsSetPagination


class AgreementViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer__customer_type', 'status']
    search_fields = ['number']

    def get_queryset(self):
        user_agreements = document_models.Agreement.objects.filter(customer__user=self.request.user).order_by(
            '-updated_at')

        return user_agreements.with_sums() if self.action in ['retrieve', 'list'] else user_agreements

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = document_serializers.AgreementMainPageSerializer
        elif self.action == 'retrieve':
            serializer_class = document_serializers.AgreementDetailSerializer
        elif self.action == 'search':
            serializer_class = document_serializers.AgreementListSerializer
        else:
            serializer_class = document_serializers.AgreementCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['AgreementViewSet']
