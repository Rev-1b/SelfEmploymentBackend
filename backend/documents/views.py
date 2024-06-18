from django.db import models
from rest_framework import viewsets, permissions, exceptions

from . import models as document_models, serializers as document_serializers


class AgreementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_agreements = document_models.Agreement.objects.filter(customer__user=self.request.user)

        if self.action == 'retrieve':
            return user_agreements.annotate(
                additional_sum=models.Count('additional', distinct=True),
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )
        return user_agreements

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            serializer_class = document_serializers.AgreementDetailSerializer
        elif self.action == 'list':
            serializer_class = document_serializers.AgreementListSerializer
        else:
            serializer_class = document_serializers.AgreementCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class AdditionalViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        agreement_id = get_agreement_id(self)
        agreement_additional = document_models.Additional.objects.filter(agreement=agreement_id)

        if self.action == 'retrieve':
            return agreement_additional.annotate(
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )
        return agreement_additional

    def get_serializer(self, *args, **kwargs):
        if self.action == 'retrieve':
            serializer_class = document_serializers.AgreementListSerializer
        else:
            serializer_class = document_serializers.AgreementCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class ActsViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = document_serializers.ActSerializer

    def get_queryset(self):
        agreement_id = get_agreement_id(self)
        return document_models.Act.objects.filter(agreement=agreement_id)


class ChecksViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = document_serializers.CheckSerializer

    def get_queryset(self):
        agreement_id = get_agreement_id(self)
        return document_models.CheckModel.objects.filter(agreement=agreement_id)


class InvoicesViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = document_serializers.InvoiceSerializer

    def get_queryset(self):
        agreement_id = get_agreement_id(self)
        return document_models.Invoice.objects.filter(agreement=agreement_id)


def get_agreement_id(self):
    agreement_id = self.request.query_params.get('agreement_id', None)
    if agreement_id is None:
        raise exceptions.ValidationError('Не указан "agreement_id" в параметрах запроса')
    return agreement_id