from rest_framework import serializers

from customers.models import CustomerRequisites


class CustomerRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequisites
        fields = ['id', 'customer', 'bank_name', 'bic', 'bank_account', 'customer_account_number', 'updated_at']


__all__ = ['CustomerRequisitesSerializer']
