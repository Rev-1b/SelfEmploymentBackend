from rest_framework import serializers

from customers.models import CustomerPassport


class CustomerPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPassport
        fields = ['series', 'number', 'release_date', 'unit_code']


__all__ = ['CustomerPassportSerializer']
