from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, exceptions, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from project.pagination import StandardResultsSetPagination


class ListNumberSearchMixin:
    search_fields = None

    @action(detail=False)
    def search(self: ViewSet(), request):
        if self.search_fields is None:
            return Response({'detail': 'search_fields attribute is not specified!'}, status=status.HTTP_400_BAD_REQUEST)

        query = request.query_params.get('q', None)
        if query is None:
            return Response([], status=status.HTTP_200_OK)

        queries = [Q(**{f"{field}__istartswith": query}) for field in self.search_fields]
        query_obj = Q()
        for q in queries:
            query_obj |= q

        results = self.get_queryset().filter(query_obj).order_by('-updated_at')
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_master_id(self):
    agreement_id = self.request.query_params.get('agreement_id', None)
    additional_id = self.request.query_params.get('additional_id', None)

    if agreement_id is None and additional_id is None:
        raise exceptions.ValidationError(f'No "agreement_id" or "additional_id" specified in request parameters')
    if agreement_id and additional_id:
        raise exceptions.ValidationError(f'The request parameters contain the ids of both parents')
    return {'agreement_id': agreement_id, 'additional_id': additional_id}


def get_records_number(self):
    records_number = self.request.query_params.get('records_number')
    if records_number is None:
        raise exceptions.ValidationError(f'Не указан "records_number" в параметрах запроса')
    if not records_number.isdigit() or not 3 <= int(records_number) <= 10:
        raise exceptions.ValidationError(f'Неправильно указан "records_number" в параметрах запроса')
    return int(records_number)


class CommonDocumentViewSet(viewsets.ModelViewSet, ListNumberSearchMixin):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    model_class = None

    def get_queryset(self):
        model = self.model_class
        if model is None:
            raise Exception('Не указан класс модели')

        # Swagger
        if getattr(self, 'swagger_fake_view', False):
            return model.objects.none()

        agreement_id, additional_id = get_master_id(self).values()
        if agreement_id is not None:
            return model.objects.filter(agreement__customer__user=self.request.user, agreement=agreement_id)
        return model.objects.filter(additional__agreement__customer__user=self.request.user, additional=additional_id)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('agreement_id', openapi.IN_QUERY,
                          description="ID of linked agreement, you wil need one of those", type=openapi.TYPE_STRING,
                          required=False),
        openapi.Parameter('additional_id', openapi.IN_QUERY,
                          description="ID of linked additional, you wil need one of those", type=openapi.TYPE_STRING,
                          required=False)
    ])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


__all__ = ['CommonDocumentViewSet', 'ListNumberSearchMixin', 'get_records_number', 'get_master_id']
