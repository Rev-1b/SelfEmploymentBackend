from datetime import datetime, timedelta

from django.db import models
from django.http import JsonResponse
from rest_framework import viewsets, permissions, exceptions, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from project.pagination import StandardResultsSetPagination
from . import models as document_models, serializers as document_serializers


class AgreementViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        user_agreements = document_models.Agreement.objects.filter(customer__user=self.request.user).order_by(
            '-updated_at')

        if self.action in ['retrieve', 'list']:
            return user_agreements.annotate(
                additional_sum=models.Count('additional', distinct=True),
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )
        return user_agreements

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = document_serializers.AgreementMainPageSerializer
        elif self.action == 'retrieve':
            serializer_class = document_serializers.AgreementDetailSerializer
        else:
            serializer_class = document_serializers.AgreementCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class AdditionalViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        agreement_id, _ = get_master_id(self).values()
        agreement_additional = document_models.Additional.objects.filter(agreement=agreement_id).order_by('-updated_at')
        if self.action in ['retrieve', 'list']:
            return agreement_additional.annotate(
                act_sum=models.Count('acts', distinct=True),
                check_sum=models.Count('checks', distinct=True),
                invoice_sum=models.Count('invoices', distinct=True),
            )

        return agreement_additional

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            serializer_class = document_serializers.AdditionalMainPageSerializer
        elif self.action == 'retrieve':
            serializer_class = document_serializers.AdditionalRetrieveSerializer
        else:
            serializer_class = document_serializers.AdditionalCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class CommonDocumentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    model_class = None

    def get_queryset(self):
        model = self.model_class
        if model is None:
            raise Exception('Не указан класс модели')

        agreement_id, additional_id = get_master_id(self).values()
        if agreement_id is not None:
            return model.objects.filter(agreement__customer__user=self.request.user, agreement=agreement_id)
        return model.objects.filter(additional__agreement__customer__user=self.request.user, additional=additional_id)


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
        raise exceptions.ValidationError(f'No "agreement_id" or "additional_id" specified in request parameters')
    if agreement_id and additional_id:
        raise exceptions.ValidationError(f'The request parameters contain the ids of both parents')
    return {'agreement_id': agreement_id, 'additional_id': additional_id}


class UserTemplateViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return document_models.UserTemplate.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = document_serializers.UserTemplateSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class DocumentHistoryViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    permissions = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        records = get_records_number(self)

        agreement_records = list(
            document_models.Agreement.objects.order_by('-updated_at')[:records].values('id', 'number', 'updated_at'))
        additional_records = list(
            document_models.Additional.objects.order_by('-updated_at')[:records].values('id', 'number', 'updated_at'))
        act_records = list(
            document_models.Act.objects.order_by('-updated_at')[:records].values('id', 'number', 'updated_at'))
        invoice_records = list(
            document_models.Invoice.objects.order_by('-updated_at')[:records].values('id', 'number', 'updated_at'))
        check_records = list(
            document_models.CheckModel.objects.order_by('-updated_at')[:records].values('id', 'number', 'updated_at'))

        def add_record_type(records_list, typename):
            for rec in records_list:
                rec['type'] = typename

        record_registry = {
            'agreement': agreement_records,
            'additional': additional_records,
            'act': act_records,
            'invoice': invoice_records,
            'check': check_records,
        }

        for key, value in record_registry.items():
            add_record_type(value, key)

        all_records = [rec for records in record_registry.values() for rec in records]
        sorted_records = sorted(all_records, key=lambda x: x['updated_at'], reverse=True)

        serializer = document_serializers.DocumentHistorySerializer(sorted_records, many=True)
        return JsonResponse({"latest_records": serializer.data})


def get_records_number(self):
    records_number = self.request.query_params.get('records_number')
    if records_number is None:
        raise exceptions.ValidationError(f'Не указан "records_number" в параметрах запроса')
    if not records_number.isdigit() or not 3 <= int(records_number) <= 10:
        raise exceptions.ValidationError(f'Неправильно указан "records_number" в параметрах запроса')
    return int(records_number)


class PaymentViewSet(viewsets.ModelViewSet):
    permissions = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return document_models.Payment.objects.filter(agreement__customer__user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = document_serializers.PaymentSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False)
    def month_statistic(self, request):
        start_date = datetime.now() - timedelta(days=30)
        payment_records = document_models.Payment.objects.with_check().filter(
            created_at__gte=start_date).values('id', 'created_at', 'amount')

        serializer = document_serializers.StatisticSerializer(payment_records, many=True)
        return Response(serializer.data)