from rest_framework import serializers

from customers.models import Customer
from documents.models import Payment, Agreement, Act, Invoice, CheckModel, Additional


class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'customer_name', 'customer_type']


class AgreementInfoSerializer(serializers.ModelSerializer):
    customer = CustomerInfoSerializer()

    class Meta:
        model = Agreement
        fields = ['id', 'number', 'start_date', 'customer']


class AdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ['id', 'number']


class ActInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'number']


class InvoiceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'number']


class CheckInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'number']


class ListPaymentSerializer(serializers.ModelSerializer):
    amount = serializers.ReadOnlyField()
    agreement_info = AgreementInfoSerializer(source='agreement')
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
    agreement_info = AgreementInfoSerializer(source='agreement')
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
    agreement_info = AgreementInfoSerializer(source='agreement')
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
