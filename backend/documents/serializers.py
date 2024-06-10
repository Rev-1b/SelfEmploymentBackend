from rest_framework import serializers

from .models import Agreement, Additional, BaseAttachment, Act, CheckModel, Invoice


class AgreementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agreement
        fields = ['customer', 'agreement_number', 'content']