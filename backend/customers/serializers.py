from rest_framework import serializers

from .models import Customer, CustomerRequisites, CustomerContacts


class CustomerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'additional_id', 'customer_type', 'customer_name', 'date_created']


class CustomerRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequisites
        fields = '__all__'


class CustomerContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContacts
        fields = '__all__'


class CustomerDetailSerializer(serializers.ModelSerializer):
    requisites = CustomerRequisitesSerializer(many=True, required=False)
    contacts = CustomerContactsSerializer(many=True, required=False)

    COMMON_FIELDS = ['id', 'additional_id', 'customer_type', 'customer_name', 'date_created']
    LLC_FIELDS = ['post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved']
    IE_FIELDS = ['post_address', 'inn', 'place_of_residence', 'ogrnip']
    EXTERNAL_FIELDS = ['requisites', 'contacts']

    class Meta:
        model = Customer
        fields = [
            'id', 'additional_id', 'customer_type', 'customer_name', 'date_created',
            'post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved',
            'place_of_residence', 'ogrnip', 'requisites', 'contacts'
        ]
