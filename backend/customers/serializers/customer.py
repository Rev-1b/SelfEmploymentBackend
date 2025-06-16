from copy import copy

from rest_framework import serializers, exceptions

from customers.models import Customer, CustomerPassport
from customers.serializers.passport import CustomerPassportSerializer


class CustomerInfoSerializer(serializers.ModelSerializer):
    # customer_type = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ['id', 'additional_id', 'customer_type', 'customer_name', 'updated_at']

    # todo: Uncomment if client needs localisation of CUSTOMER_TYPE field
    # def get_customer_type(self, obj):
    #     return obj.get_customer_type_display()


class CustomerDetailSerializer(serializers.ModelSerializer):
    passport = CustomerPassportSerializer(required=False)
    # customer_type = serializers.SerializerMethodField()

    FIELDS_TO_UPDATE = [
        'additional_id', 'customer_name', 'post_address', 'inn', 'full_company_name', 'orgn', 'kpp',
        'legal_address', 'okpo', 'okved', 'place_of_residence', 'ogrnip'
    ]

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
        if passport_data is not None:
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
            'COMMON': ['additional_id', 'customer_type', 'customer_name', 'passport'],
            'LLC': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'full_company_name',
                    'orgn', 'kpp', 'legal_address', 'okpo', 'okved'],
            'IE': ['additional_id', 'customer_type', 'customer_name', 'post_address', 'inn', 'place_of_residence',
                   'ogrnip'],
        }

        customer_type = attrs.get("customer_type", None)
        if customer_type is None or customer_type not in ('COMMON', 'IE', 'LLC'):
            raise exceptions.ValidationError(
                {'customer_type': "Customer type is not specified or is specified incorrectly"})

        errors = {}

        if self.context.get('request').method == 'POST':
            errors.update(self.check_required_attrs(attrs, table.get(customer_type)))
            errors.update(self.check_extra_attrs(attrs, table.get(customer_type)))

        if self.context.get('request').method == 'PATCH':
            errors.update(self.check_extra_attrs(attrs, table.get(customer_type)))

        if errors:
            raise exceptions.ValidationError(errors)

        return super().validate(attrs)

    # todo: Uncomment if client needs localisation of CUSTOMER_TYPE field
    # def get_customer_type(self, obj):
    #     return obj.get_customer_type_display()

    @staticmethod
    def check_required_attrs(attrs, required_keys):
        errors = {}
        for key in required_keys:
            if key not in attrs:
                errors[key] = 'Обязательное поле'
            if key in attrs and attrs[key] is None:
                errors[key] = 'Для поля не указано значение'
        return errors

    @staticmethod
    def check_extra_attrs(attrs, required_keys):
        copy_keys = copy(attrs)
        errors = {}

        for key in required_keys:
            copy_keys.pop(key, None)

        for key in copy_keys:
            errors.update({key: "Лишнее поле"})

        return errors

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {key: value for key, value in data.items() if value is not None}


__all__ = ['CustomerInfoSerializer', 'CustomerDetailSerializer']
