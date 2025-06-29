from rest_framework import serializers

from documents.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'agreement', 'additional', 'amount', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


class InvoiceInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'number']


__all__ = ['InvoiceSerializer', 'InvoiceInfoSerializer']
