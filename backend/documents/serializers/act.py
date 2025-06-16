from rest_framework import serializers

from documents.models import Act


class ActSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'agreement', 'title', 'content', 'updated_at']
        extra_kwargs = {
            'updated_at': {'read_only': True},
        }


class ActInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Act
        fields = ['id', 'number']


__all__ = ['ActSerializer', 'ActInfoSerializer']
