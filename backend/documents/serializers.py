from rest_framework import serializers

from customers.models import Customer
from .models import Agreement, Additional, Act, CheckModel, Invoice, UserTemplate, Payment


class ShortCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'customer_type', 'customer_name')


# ----------------------------------------- Agreement serializers section ----------------------------------------------
class AgreementMainPageSerializer(serializers.ModelSerializer):
    customer = ShortCustomerSerializer()
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
    customer = ShortCustomerSerializer()
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


class AgreementListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Agreement
        fields = ['id', 'number', 'status']


# ------------------------------------ Additional serializers section --------------------------------------------------
class AdditionalMainPageSerializer(serializers.ModelSerializer):
    related_entities_data = serializers.SerializerMethodField()

    class Meta:
        model = Additional
        fields = ['id',  'title', 'updated_at', 'related_entities_data']

    def get_related_entities_data(self, additional):
        return {
            'act_sum': additional.act_sum,
            'check_sum': additional.check_sum,
            'invoice_sum': additional.invoice_sum,
        }


class AdditionalRetrieveSerializer(serializers.ModelSerializer):
    related_entities_data = serializers.SerializerMethodField()

    class Meta:
        model = Additional
        fields = ['id', 'title', 'content', 'updated_at', 'related_entities_data']

    def get_related_entities_data(self, additional):
        return {
            'act_sum': additional.act_sum,
            'check_sum': additional.check_sum,
            'invoice_sum': additional.invoice_sum,
        }


class AdditionalCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'number', 'title', 'content', 'deal_amount']


# ---------------------------------- Acts, Checks and Invoices serializers section -------------------------------------
class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'agreement', 'title', 'content', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'agreement', 'additional', 'amount', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['id', 'agreement', 'additional', 'amount', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


# ----------------------------------------- UserTemplates serializers section ------------------------------------------
class UserTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplate
        fields = ['id', 'user', 'template_type', 'title', 'content', 'updated_at']


class DocumentHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.CharField()
    type = serializers.CharField()
    updated_at = serializers.DateTimeField()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['agreement', 'additional', 'act', 'invoice', 'check_link']


class StatisticSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    amount = serializers.IntegerField()