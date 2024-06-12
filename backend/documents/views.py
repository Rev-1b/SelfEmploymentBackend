from rest_framework import mixins, viewsets, permissions, generics
from rest_framework.response import Response

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


class AgreementView(generics.GenericAPIView):
    def get(self, request):
        queryset = Agreement.objects.all().filter(customer__user=request.user)
        serializer = AgreementSerializer(queryset, many=True)
        return Response(serializer.data)



