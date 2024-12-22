from rest_framework import serializers

from customers.models import Customer
from customers.serializers import CustomerInfoSerializer
from documents.models import Agreement


class AgreementMainPageSerializer(serializers.ModelSerializer):
    customer = CustomerInfoSerializer(read_only=True)
    related_entities_data = serializers.SerializerMethodField()

    class Meta:
        model = Agreement
        fields = ['id', 'number', 'status', 'updated_at', 'customer', 'related_entities_data']

    def get_related_entities_data(self, agreement):
        return {
            'additional_sum': agreement.additional_sum,
            'act_sum': agreement.act_sum,
            'check_sum': agreement.check_sum,
            'invoice_sum': agreement.invoice_sum,
        }


class AgreementDetailSerializer(serializers.ModelSerializer):
    customer = CustomerInfoSerializer(read_only=True)
    related_entities_data = serializers.SerializerMethodField()

    class Meta:
        model = Agreement
        fields = ['id', 'number', 'status', 'content', 'start_date', 'end_date', 'customer', 'related_entities_data']

    def get_related_entities_data(self, agreement):
        return {
            'additional_sum': agreement.additional_sum,
            'act_sum': agreement.act_sum,
            'check_sum': agreement.check_sum,
            'invoice_sum': agreement.invoice_sum,
        }


class AgreementCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'customer', 'number', 'status', 'content', 'start_date', 'end_date']


class AgreementInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'number']


class AgreementCustomerInfoSerializer(serializers.ModelSerializer):
    customer = CustomerInfoSerializer(read_only=True)

    class Meta:
        model = Agreement
        fields = ['id', 'number', 'status', 'customer']


__all__ = [
    'AgreementMainPageSerializer',
    'AgreementDetailSerializer',
    'AgreementCUDSerializer',
    'AgreementInfoSerializer',
    'AgreementCustomerInfoSerializer'
]