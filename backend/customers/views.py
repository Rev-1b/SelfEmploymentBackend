from rest_framework import generics
from rest_framework.response import Response

from customers.models import Customer
from customers.serializers import CustomerPageSerializer


class CustomerPageView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerPageSerializer
