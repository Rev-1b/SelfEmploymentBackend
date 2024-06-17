from rest_framework import serializers

from .models import Agreement, Additional, Act, CheckModel, Invoice


class AgreementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'customer', 'customer__customer_name', 'customer__customer_type', 'agreement_number']


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
