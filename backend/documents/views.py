from datetime import datetime, timedelta

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, exceptions, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from project.pagination import StandardResultsSetPagination
from . import models as document_models, serializers as document_serializers
from customers import models as customer_models


class ListNumberSearchMixin:
    search_fields = None

    @action(detail=False)
    def search(self: ViewSet(), request):
        if self.search_fields is None:
            return Response({'detail': 'search_fields attribute is not specified!'}, status=status.HTTP_400_BAD_REQUEST)

        query = request.query_params.get('q', None)
        if query is None:
            return Response([], status=status.HTTP_200_OK)

        queries = [Q(**{f"{field}__istartswith": query}) for field in self.search_fields]
        query_obj = Q()
        for q in queries:
            query_obj |= q

        results = self.get_queryset().filter(query_obj).order_by('-updated_at')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        else:
            serializer_class = document_serializers.AdditionalCUDSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('agreement_id', openapi.IN_QUERY, description="ID of linked agreement",
                          type=openapi.TYPE_STRING, required=True)
    ])
    def list(self, request, *args, **kwargs):
        super(AdditionalViewSet, self).list(request, *args, **kwargs)


class CommonDocumentViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    model_class = None

    def get_queryset(self):
        model = self.model_class
        if model is None:
            raise Exception('Не указан класс модели')

        # Swagger
        if getattr(self, 'swagger_fake_view', False):
            return model.objects.none()

        agreement_id, additional_id = get_master_id(self).values()
        if agreement_id is not None:
            return model.objects.filter(agreement__customer__user=self.request.user, agreement=agreement_id)
        return model.objects.filter(additional__agreement__customer__user=self.request.user, additional=additional_id)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('agreement_id', openapi.IN_QUERY,
                          description="ID of linked agreement, you wil need one of those", type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('additional_id', openapi.IN_QUERY,
                          description="ID of linked additional, you wil need one of those", type=openapi.TYPE_STRING,
                          required=False)
    ])
    def list(self, request, *args, **kwargs):
        super().list(request, *args, **kwargs)


class ActViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.ActSerializer
    model_class = document_models.Act
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number', 'title']


class CheckViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.CheckSerializer
    model_class = document_models.CheckModel
    search_fields = ['number']


class InvoiceViewSet(CommonDocumentViewSet):
    serializer_class = document_serializers.InvoiceSerializer
    model_class = document_models.Invoice
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']
    search_fields = ['number']


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['template_type']
    search_fields = ['title']

    def get_queryset(self):
        return document_models.UserTemplate.objects.filter(user=self.request.user)

    def get_serializer(self, *args, **kwargs):
        serializer_class = document_serializers.UserTemplateSerializer

        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class DocumentHistoryViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    permissions = [permissions.IsAuthenticated]
    serializer_class = document_serializers.DocumentHistorySerializer

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

        serializer = self.get_serializer(sorted_records, many=True)
        return Response({"latest_records": serializer.data})


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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status']

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


class ProjectSearch(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permissions = [permissions.IsAuthenticated]
    serializer_class = document_serializers.DocumentHistorySerializer

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if not query:
            return Response({"detail": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = [
            (document_models.Agreement, document_serializers.AgreementSearchSerializer),
            (document_models.Additional, document_serializers.AdditionalSearchSerializer),
            (document_models.Act, document_serializers.ActSearchSerializer),
            (document_models.Invoice, document_serializers.InvoiceSearchSerializer),
            (document_models.CheckModel, document_serializers.CheckSearchSerializer),
            (document_models.Payment, document_serializers.PaymentSearchSerializer),
            (customer_models.Customer, document_serializers.CustomerSearchSerializer)
        ]

        result = []
        for model, serializer in model_serializer:
            queryset = self.get_same_entities(model, serializer, query)
            result.append(queryset)

        return Response(result, status=status.HTTP_200_OK)

    def get_same_entities(self, model, serializer, query):
        query_filters = Q()
        for field in model.search_fields:
            query_filters |= Q(**{f"{field}__icontains": query})

        results = model.objects.filter(query_filters)
        return serializer(results[:10], many=True, context={'request': self.request}).data