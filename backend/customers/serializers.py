from rest_framework import serializers

from .models import Customer, CustomerRequisites, CustomerContacts


class CustomerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'additional_id', 'customer_type', 'customer_name', 'date_created']


class CustomerRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequisites
        read_only_fields = ['id']
        fields = ['id', 'bank_name', 'bic', 'bank_account', 'customer_account_number']


class CustomerContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContacts
        read_only_fields = ['id']
        fields = ['id', 'contact_name', 'contact_type', 'contact_info']


class CustomerDetailSerializer(serializers.ModelSerializer):
    requisites = CustomerRequisitesSerializer(many=True, required=False)
    contacts = CustomerContactsSerializer(many=True, required=False)

    COMMON_FIELDS = ['id', 'additional_id', 'customer_type', 'customer_name', 'date_created']
    LLC_FIELDS = ['post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved']
    IE_FIELDS = ['post_address', 'inn', 'place_of_residence', 'ogrnip']
    EXTERNAL_FIELDS = ['requisites', 'contacts']

    class Meta:
        model = Customer
        read_only_fields = ['id', 'date_created']
        fields = [
            'id', 'additional_id', 'customer_type', 'customer_name', 'date_created',
            'post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved',
            'place_of_residence', 'ogrnip', 'requisites', 'contacts'
        ]

    def create(self, validated_data):
        requisites_data = validated_data.pop('requisites')
        contacts_data = validated_data.pop('contacts')
        user = self.context.get('request').user

        customer = Customer.objects.create(user=user, **validated_data)
        CustomerRequisites.objects.bulk_create(
            [CustomerRequisites(customer=customer, **data) for data in requisites_data]
        )
        CustomerContacts.objects.bulk_create(
            [CustomerContacts(customer=customer, **data) for data in contacts_data]
        )

        return customer

    def update(self, instance, validated_data):
        pass