from rest_framework import mixins, viewsets, permissions

from .models import Agreement, Additional
from .serializers import AgreementSerializer, AdditionalSerializer


class AgreementViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Agreement.objects.all()
    serializer_class = AgreementSerializer
    permission_classes = [permissions.IsAuthenticated]


class AdditionalViewSet(mixins.CreateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    queryset = Additional.objects.all()
    serializer_class = AdditionalSerializer
    permission_classes = [permissions.IsAuthenticated]

