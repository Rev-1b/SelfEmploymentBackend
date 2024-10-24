from rest_framework import mixins, viewsets, permissions
from rest_framework.response import Response

from documents import serializers as document_serializers, models as document_models
from documents.views.common import get_records_number


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


__all__ = ['DocumentHistoryViewSet']
