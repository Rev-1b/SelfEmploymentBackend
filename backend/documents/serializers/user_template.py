from rest_framework import serializers

from documents.models import UserTemplate


class UserTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTemplate
        fields = ['id', 'user', 'template_type', 'title', 'content', 'updated_at']


__all__ = ['UserTemplateSerializer']
