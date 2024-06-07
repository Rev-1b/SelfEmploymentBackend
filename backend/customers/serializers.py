from rest_framework import serializers

from .models import Customer


class CustomerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'additional_id', 'customer_name', 'date_created')

