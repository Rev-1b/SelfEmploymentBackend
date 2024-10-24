from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from pagination import StandardResultsSetPagination
from users.models import UserRequisites
from users.serializers import UserRequisitesSerializer


class UserRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserRequisites.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.get_queryset().create(user=request.user, **serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


__all__ = ['UserRequisitesViewSet']
