from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.core.validators import validate_email
from django.db import transaction
from rest_framework import serializers

from users.models import CustomUser, Passport


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'error_messages': {'unique': 'Пользователь с такой электронной почтой уже существует'}},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = ['series', 'number', 'release_date', 'unit_code']


class UserDetailSerializer(serializers.ModelSerializer):
    passport = PassportSerializer()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'middle_name', 'passport']
        extra_kwargs = {
            'email': {'read_only': True},
            'username': {'read_only': True},
        }

    def update(self, instance, validated_data):
        passport_data = validated_data.pop('passport', None)
        with transaction.atomic():
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            instance.save()

            # Passport fields change
            if passport_data is not None:
                passport_serializer = PassportSerializer(
                    instance=instance.passport,
                    data=passport_data,
                    partial=True
                )
                if passport_serializer.is_valid(raise_exception=True):
                    passport_serializer.save(user=instance)

        return instance


class NewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate_new_passport(self, value):
        user = self.context["request"].user
        assert user is not None

        try:
            validate_password(value, user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return value


class OldToNewPasswordSerializer(NewPasswordSerializer):
    old_password = serializers.CharField(style={"input_type": "password"})


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    @staticmethod
    def validate_email(value):
        try:
            validate_email(value)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'email': list(e.messages)})

        return value


__all__ = [
    'UserDetailSerializer',
    'UserCreateSerializer',
    'PassportSerializer',
    'EmailSerializer',
    'NewPasswordSerializer',
    'OldToNewPasswordSerializer',
]
