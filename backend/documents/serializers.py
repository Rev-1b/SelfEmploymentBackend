from rest_framework import serializers

from .models import Agreement, Additional, BaseAttachment, Act, CheckModel, Invoice


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['id', 'customer', 'agreement_number', 'content']


class AdditionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Additional
        fields = ['id', 'agreement', 'title', 'content']