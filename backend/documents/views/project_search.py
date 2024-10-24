from django.db.models import Q
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.response import Response

import customers.models as customers_models

from documents import serializers as document_serializers, models as document_models


class ProjectSearch(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    permissions = [permissions.IsAuthenticated]
    serializer_class = document_serializers.DocumentHistorySerializer

    def list(self, request, *args, **kwargs):
        query = request.query_params.get('q', None)

        if not query:
            return Response({"detail": "Query parameter 'q' is required."}, status=status.HTTP_400_BAD_REQUEST)

        model_serializer = [
            (document_models.Agreement, document_serializers.AgreementSearchSerializer),
            (document_models.Additional, document_serializers.AdditionalSearchSerializer),
            (document_models.Act, document_serializers.ActSearchSerializer),
            (document_models.Invoice, document_serializers.InvoiceSearchSerializer),
            (document_models.CheckModel, document_serializers.CheckSearchSerializer),
            (document_models.Payment, document_serializers.PaymentSearchSerializer),
            (customers_models.Customer, document_serializers.CustomerSearchSerializer)
        ]

        result = []
        for model, serializer in model_serializer:
            queryset = self.get_same_entities(model, serializer, query)
            result.append(queryset)

        return Response(result, status=status.HTTP_200_OK)

    def get_same_entities(self, model, serializer, query):
        query_filters = Q()
        for field in model.search_fields:
            query_filters |= Q(**{f"{field}__icontains": query})

        results = model.objects.filter(query_filters)
        return serializer(results[:10], many=True, context={'request': self.request}).data


__all__ = ['ProjectSearch']
