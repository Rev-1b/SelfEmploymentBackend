from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from project.pagination import StandardResultsSetPagination
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

        # Создаем объект через serializer.save(), который автоматически добавит user
        serializer.save(user=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


__all__ = ['UserRequisitesViewSet']
