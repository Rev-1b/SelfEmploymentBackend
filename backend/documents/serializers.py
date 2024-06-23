from rest_framework import serializers

from customers.models import Customer
from .models import Agreement, Additional, Act, CheckModel, Invoice, Deal, UserTemplate


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
        fields = ['id', 'agreement_number', 'status', 'customer', 'related_entities_data']

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
        fields = ['id', 'agreement_number', 'status', 'content', 'customer', 'related_entities_data']

    def get_related_entities_data(self, agreement):
        return {
            'additional_sum': agreement.additional_sum,
            'act_sum': agreement.act_sum,
            'check_sum': agreement.check_sum,
            'invoice_sum': agreement.invoice_sum,
        }


class AgreementListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'agreement_number', 'status']


# ------------------------------------ Additional serializers section --------------------------------------------------
class AdditionalRetrieveSerializer(serializers.ModelSerializer):
    related_entities_data = serializers.SerializerMethodField()

    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'title', 'content', 'related_entities_data']

    def get_related_entities_data(self, additional):
        return {
            'act_sum': additional.act_sum,
            'check_sum': additional.check_sum,
            'invoice_sum': additional.invoice_sum,
        }


class AdditionalCLUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'title', 'content']


# ---------------------------------- Acts, Checks and Invoices serializers section -------------------------------------
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


# ----------------------------------------- UserTemplates serializers section ------------------------------------------
class UserTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplate
        fields = ['id', 'template_type', 'title', 'content']


# --------------------------------------------- Deals serializers section ----------------------------------------------
class DealGetSerializer(serializers.ModelSerializer):
    agreement = AgreementListSerializer()

    class Meta:
        model = Deal
        fields = ['id', 'service_type', 'amount', 'service_date', 'agreement']


class DealCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = ['service_type', 'amount', 'service_date']