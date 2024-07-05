from copy import copy

from rest_framework import serializers, exceptions

from .models import Customer, CustomerRequisites, CustomerContacts, CustomerPassport


class CustomerPassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerPassport
        fields = ['series', 'number', 'release_date', 'unit_code']


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
    passport = CustomerPassportSerializer(required=False)

    FIELDS_TO_UPDATE = ['additional_id', 'customer_name', 'post_address', 'inn', 'full_company_name', 'orgn', 'kpp',
                        'legal_address', 'okpo', 'okved', 'place_of_residence', 'ogrnip']

    class Meta:
        model = Customer
        fields = [
            'id', 'additional_id', 'customer_type', 'customer_name', 'passport',
            'post_address', 'inn', 'full_company_name', 'orgn', 'kpp', 'legal_address', 'okpo', 'okved',
            'place_of_residence', 'ogrnip'
        ]

    def create(self, validated_data):
        passport_data = validated_data.pop('passport', None)
        user = self.context.get('request').user

        customer = Customer.objects.create(user=user, **validated_data)
        CustomerPassport.objects.create(customer=customer, **passport_data)

        return customer

    def update(self, instance, validated_data):
        passport_data = validated_data.pop('passport', None)

        for field in self.FIELDS_TO_UPDATE:
            setattr(instance, field, validated_data.get(field, getattr(instance, field)))

        if passport_data is not None:
            passport = CustomerPassport.objects.filter(customer=instance)
            passport.update(**passport_data)

        instance.save()
        return instance

    def validate(self, attrs: dict):
        table = {
            'CM': ['additional_id', 'customer_type', 'customer_name', 'passport'],
            'LC': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'full_company_name',
                   'orgn', 'kpp', 'legal_address', 'okpo', 'okved'],
            'IE': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'place_of_residence',
                   'ogrnip'],
        }

        customer_type = attrs.get("customer_type", None)
        if customer_type is None or customer_type not in ('CM', 'IE', 'LC'):
            raise exceptions.ValidationError({'customer_type': "Тип заказчика не указан, либо указан некорректно"})

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



