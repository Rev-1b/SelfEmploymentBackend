from copy import copy

from rest_framework import serializers, exceptions

from .models import Customer, CustomerRequisites, CustomerContacts


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'additional_id', 'customer_type', 'customer_name', 'updated_at']


class CustomerRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRequisites
        fields = ['id', 'bank_name', 'bic', 'bank_account', 'customer_account_number', 'updated_at']


class CustomerContactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerContacts
        fields = ['id', 'contact_name', 'contact_type', 'contact_info', 'updated_at']


class CustomerDetailSerializer(serializers.ModelSerializer):
    requisites = CustomerRequisitesSerializer(many=True, required=False)
    contacts = CustomerContactsSerializer(many=True, required=False)

    FIELDS_TO_UPDATE = ['additional_id', 'customer_name', 'post_address', 'inn', 'full_company_name', 'orgn', 'kpp',
                        'legal_address', 'okpo', 'okved', 'place_of_residence', 'ogrnip']

    class Meta:
        model = Customer
        fields = [
            'id', 'additional_id', 'customer_type', 'customer_name',
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

    def validate(self, attrs: dict):
        table = {
            'CM': ['additional_id', 'customer_type', 'customer_name', 'requisites', 'contacts'],
            'LC': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'full_company_name',
                   'orgn', 'kpp', 'legal_address', 'okpo', 'okved', 'requisites', 'contacts'],
            'IE': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'place_of_residence',
                   'ogrnip', 'requisites', 'contacts'],
        }

        customer_type = attrs.get("customer_type", None)
        if customer_type is None or customer_type not in ('CM', 'IE', 'LC'):
            raise exceptions.ValidationError("Тип заказчика не указан, либо указан некорректно")

        if self.context.get('request').method == 'POST':
            self.check_required_attrs(attrs, table.get(customer_type))
            self.check_extra_attrs(attrs, table.get(customer_type))

        if self.context.get('request').method == 'PATCH':
            self.check_extra_attrs(attrs, table.get(customer_type))

        return super().validate(attrs)

    @staticmethod
    def check_required_attrs(attrs, required_keys):
        for key in required_keys:
            if key not in attrs:
                raise exceptions.ValidationError(f'Аттрибут "{key}" не указан :)')
            if attrs[key] is None:
                raise exceptions.ValidationError(f'Для атрибута {key} не указано значение')

    @staticmethod
    def check_extra_attrs(attrs, required_keys):
        copy_keys = copy(attrs)

        for key in required_keys:
            copy_keys.pop(key, None)

        if copy_keys:
            raise exceptions.ValidationError(f'Переданы лишние аттрибуты: ["{", ".join(copy_keys)}]"')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}



