from rest_framework import generics, mixins
from rest_framework import viewsets
from rest_framework.response import Response

from customers.models import Customer
from customers.serializers import CustomerPageSerializer, CustomerDetailSerializer


class CustomerPageView(generics.GenericAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerPageSerializer

    def get(self, request):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = CustomerPageSerializer(queryset, many=True)
        return Response(serializer.data)


class CustomerDetailViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer

    # def get_serializer(self, *args, fields_type=None, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs.setdefault('context', self.get_serializer_context())
    #
    #     if fields_type is None:
    #         serializer_class.Meta.fields = serializer_class.COMMON_FIELDS
    #     return serializer_class(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
