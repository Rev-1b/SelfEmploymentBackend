from rest_framework import generics
from rest_framework.response import Response

from customers.models import Customer
from customers.serializers import CustomerPageSerializer


class CustomerPageView(generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerPageSerializer

    def get(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

