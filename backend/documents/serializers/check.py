from rest_framework import serializers

from documents.models import CheckModel


class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'agreement', 'additional', 'amount', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


class CheckInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckModel
        fields = ['id', 'number']


__all__ = ['CheckSerializer', 'CheckInfoSerializer']
