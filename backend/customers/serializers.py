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

    FIELDS_TO_UPDATE = ['additional_id', 'customer_name', 'post_address', 'inn', 'full_company_name', 'orgn', 'kpp',
                        'legal_address', 'okpo', 'okved', 'place_of_residence', 'ogrnip']

    class Meta:
        model = Customer
        read_only_fields = ['id', 'date_created']
        fields = [
            'id', 'additional_id', 'customer_type', 'customer_name', 'date_created',
            'post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved',
            'place_of_residence', 'ogrnip', 'requisites', 'contacts'
        ]

    def create(self, validated_data):
        requisites_data = validated_data.pop('requisites', None)
        contacts_data = validated_data.pop('contacts', None)
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
        requisites_data = validated_data.pop('requisites', None)
        contacts_data = validated_data.pop('contacts', None)

        for field in self.FIELDS_TO_UPDATE:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        if requisites_data is not None:
            if hasattr(instance, 'requisites'):
                CustomerRequisites.objects.filter(customer=instance).delete()
            CustomerRequisites.objects.bulk_create(
                [CustomerRequisites(customer=instance, **data) for data in requisites_data]
            )

        if contacts_data is not None:
            if hasattr(instance, 'contacts'):
                CustomerContacts.objects.filter(customer=instance).delete()
            CustomerContacts.objects.bulk_create(
                [CustomerContacts(customer=instance, **data) for data in contacts_data]
            )

        instance.save()
        return instance
