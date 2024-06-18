from django.db import models
from rest_framework import mixins, viewsets, permissions

from .models import Agreement
from .serializers import AgreementListSerializer, AgreementDetailSerializer


class AgreementViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_agreements = Agreement.objects.select_related('customer').filter(customer__user=self.request.user)

        if self.action == 'retrieve':
            a =  user_agreements.annotate(
                additional_sum=models.Count('additional', distinct=True),
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )

            return a
        elif self.action == 'list':
            return user_agreements

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            serializer_class = AgreementDetailSerializer

        elif self.action == 'list':
            serializer_class = AgreementListSerializer
        else:
            serializer_class = AgreementListSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
