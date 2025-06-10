from rest_framework import serializers


class TelegramAuthSerializer(serializers.Serializer):
    id = serializers.CharField()
    auth_date = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    hash = serializers.CharField()


__all__ = ['TelegramAuthSerializer']