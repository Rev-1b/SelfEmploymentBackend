from rest_framework import serializers

from customers.models import CustomerContacts


class CustomerContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContacts
        fields = ['id', 'customer', 'contact_name', 'contact_type', 'contact_info', 'updated_at']


__all__ = ['CustomerContactsSerializer']
