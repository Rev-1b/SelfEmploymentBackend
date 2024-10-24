from rest_framework import serializers


class DocumentHistorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    number = serializers.CharField()
    type = serializers.CharField()
    updated_at = serializers.DateTimeField()


__all__ = ['DocumentHistorySerializer']
