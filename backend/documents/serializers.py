from rest_framework import serializers

from customers.models import Customer
from .models import Agreement, Additional, Act, CheckModel, Invoice


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'customer_type', 'customer_name')


class AgreementListSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Agreement
        fields = ['id', 'agreement_number', 'customer']


class AgreementDetailSerializer(serializers.ModelSerializer):
    agreement_sum = serializers.IntegerField()
    act_sum = serializers.IntegerField()
    check_sum = serializers.IntegerField()
    invoice_sum = serializers.IntegerField()

    class Meta:
        model = Agreement
        fields = [
            'id', 'customer', 'agreement_number', 'content',
            'agreement_sum', 'act_sum', 'check_sum', 'invoice_sum'
        ]


class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'title', 'content', 'acts']


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'agreement', 'title', 'content']


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'agreement', 'additional', 'amount']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'agreement', 'additional', 'amount']
