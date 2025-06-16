from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions

from documents import models as document_models, serializers as document_serializers
from project.pagination import StandardResultsSetPagination


class UserTemplateViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['template_type']
    search_fields = ['title']

    def get_queryset(self):
        return document_models.UserTemplate.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = document_serializers.UserTemplateSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


__all__ = ['UserTemplateViewSet']
