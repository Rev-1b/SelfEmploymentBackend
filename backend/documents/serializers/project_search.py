from rest_framework import serializers

from customers.models import Customer
from documents.models import Agreement, Additional, Act, CheckModel, Invoice, Payment


class CustomerSearchSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='customers-detail')

    class Meta:
        model = Customer
        fields = ['id', 'url', 'customer_name', 'customer_type', 'updated_at']


class SearchCommonSerializer(serializers.Serializer):
    class Meta:
        model = Agreement

    def get_name(self):
        return self.Meta.model.Meta.verbose_name


class AgreementSearchSerializer(SearchCommonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='agreements-detail')

    class Meta:
        model = Agreement
        fields = ['id', 'url', 'number', 'updated_at']


class AdditionalSearchSerializer(SearchCommonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='additional-detail')

    class Meta:
        model = Additional
        fields = ['id', 'url', 'number', 'updated_at']


class ActSearchSerializer(SearchCommonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='acts-detail')

    class Meta:
        model = Act
        fields = ['id', 'url', 'number', 'updated_at']


class CheckSearchSerializer(SearchCommonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='checks-detail')

    class Meta:
        model = CheckModel
        fields = ['id', 'url', 'number', 'updated_at']


class InvoiceSearchSerializer(SearchCommonSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='invoices-detail')

    class Meta:
        model = Invoice
        fields = ['id', 'url', 'number', 'updated_at']


class PaymentSearchSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(view_name='payments-detail')

    class Meta:
        model = Payment
        fields = ['id', 'url', 'number', 'updated_at']


__all__ = [
    'CustomerSearchSerializer',
    'AgreementSearchSerializer',
    'AdditionalSearchSerializer',
    'ActSearchSerializer',
    'CheckSearchSerializer',
    'InvoiceSearchSerializer',
    'PaymentSearchSerializer',
]