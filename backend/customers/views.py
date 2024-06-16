from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import permissions

from customers.models import Customer
from customers.serializers import CustomerPageSerializer, CustomerDetailSerializer


class CustomerDetailViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = CustomerPageSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    # def get_serializer(self, *args, fields_type=None, **kwargs):
    #     serializer_class = self.get_serializer_class()
    #     kwargs.setdefault('context', self.get_serializer_context())
    #
    #     if fields_type is None:
    #         serializer_class.Meta.fields = serializer_class.COMMON_FIELDS
    #     return serializer_class(*args, **kwargs)
