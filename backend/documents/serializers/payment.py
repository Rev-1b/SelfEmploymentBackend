from rest_framework import serializers

from documents.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['agreement', 'additional', 'act', 'invoice', 'check_link']


class StatisticSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    created_at = serializers.DateTimeField()
    amount = serializers.IntegerField()


__all__ = ['PaymentSerializer', 'StatisticSerializer']
