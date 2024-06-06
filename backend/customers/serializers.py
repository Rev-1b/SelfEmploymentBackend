from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Customer, CustomerContacts, CustomerRequisites


class CustomerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ()
