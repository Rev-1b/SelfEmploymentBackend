from django.db import models
from rest_framework import viewsets, permissions, exceptions

from . import models as document_models, serializers as document_serializers


class AgreementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_agreements = document_models.Agreement.objects.filter(customer__user=self.request.user)

        if self.action in ['retrieve', 'list']:
            return user_agreements.annotate(
                additional_sum=models.Count('additional', distinct=True),
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )
        return user_agreements

    def get_serializer(self, *args, **kwargs):
        # if self.action == 'retrieve':
        #     serializer_class = document_serializers.AgreementDetailSerializer
        if self.action == 'list':
            serializer_class = document_serializers.AgreementMainPageSerializer
        else:
            serializer_class = document_serializers.AgreementDetailSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class AdditionalViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        agreement_id, _ = get_master_id(self).values()
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
            serializer_class = document_serializers.AdditionalRetrieveSerializer
        else:
            serializer_class = document_serializers.AdditionalCLUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CommonDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    model_class = None

    def get_queryset(self):
        model = self.model_class
        if model is None:
            raise Exception('Не указан класс модели')

        agreement_id, additional_id = get_master_id(self).values()

        return model.objects.filter(agreement=agreement_id) if agreement_id is not None \
            else model.objects.filter(additional=additional_id)


class ActViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.ActSerializer
    model_class = document_models.Act


class CheckViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.CheckSerializer
    model_class = document_models.CheckModel


class InvoiceViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.InvoiceSerializer
    model_class = document_models.Invoice


def get_master_id(self):
    agreement_id = self.request.query_params.get('agreement_id', None)
    additional_id = self.request.query_params.get('additional_id', None)

    if agreement_id is None and additional_id is None:
        raise exceptions.ValidationError(f'Не указан "agreement_id" или "additional_id" в параметрах запроса')
    if agreement_id and additional_id:
        raise exceptions.ValidationError(f'В параметрах запроса указаны id обоих родителей')
    return {'agreement_id': agreement_id, 'additional_id': additional_id}


class UserTemplateViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return document_models.UserTemplate.objects.filter(user=self.request.user)


class DealViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]

    def get_queryset(self):
        return document_models.Deal.objects.filter(agreement__customer__user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        if self.action in ['list', 'retrieve']:
            serializer_class = document_serializers.DealGetSerializer
        else:
            serializer_class = document_serializers.DealCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)
