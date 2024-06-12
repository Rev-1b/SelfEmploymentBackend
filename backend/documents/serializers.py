from rest_framework import serializers

from .models import Agreement, Additional, Act, CheckModel, Invoice


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'agreement', 'additional', 'title', 'content']


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'agreement', 'additional', 'amount']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'agreement', 'additional', 'amount']


class AdditionalSerializer(serializers.ModelSerializer):
    acts = ActSerializer(many=True, required=False)
    checks = CheckSerializer(many=True, required=False)
    invoices = InvoiceSerializer(many=True, required=False)

    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'title', 'content', 'acts', 'checks', 'invoices']


class AgreementSerializer(serializers.ModelSerializer):
    # additional = AdditionalSerializer(many=True, required=False)
    acts = ActSerializer(many=True, required=False)
    checks = CheckSerializer(many=True, required=False)
    invoices = InvoiceSerializer(many=True, required=False)

    class Meta:
        model = Agreement
        fields = ['id', 'customer', 'agreement_number', 'content', 'acts', 'checks', 'invoices']
