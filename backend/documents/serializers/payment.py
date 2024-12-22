from rest_framework import serializers

from documents.models import Payment
from documents.serializers import ActInfoSerializer, AdditionalInfoSerializer, InvoiceInfoSerializer, \
    CheckInfoSerializer, AgreementCustomerInfoSerializer


class ListPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    agreement_info = AgreementCustomerInfoSerializer(source='agreement')
    act_info = ActInfoSerializer(source='act')

    class Meta:
        model = Payment
        fields = ['id', 'agreement_info', 'act_info', 'status', 'amount', 'updated_at']


class CUDPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'agreement', 'additional', 'act', 'invoice', 'check_link', 'status']


class ReadPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    agreement_info = AgreementCustomerInfoSerializer(source='agreement')
    additional_info = AdditionalInfoSerializer(source='additional')
    act_info = ActInfoSerializer(source='act')
    invoice_info = InvoiceInfoSerializer(source='invoice')
    check_info = CheckInfoSerializer(source='check_link')

    class Meta:
        model = Payment
        fields = [
            'id', 'agreement_info', 'additional_info', 'act_info', 'invoice_info', 'check_info', 'status', 'amount'
        ]


class StatisticSerializer(serializers.ModelSerializer):
    agreement_info = AgreementCustomerInfoSerializer(source='agreement')
    amount = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = ['id', 'agreement_info', 'created_at', 'amount']


__all__ = [
    'ListPaymentSerializer',
    'CUDPaymentSerializer',
    'ReadPaymentSerializer',
    'StatisticSerializer'
]
