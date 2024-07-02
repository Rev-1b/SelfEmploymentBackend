from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Passport, UserRequisites


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


# auth through email
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD


# profile serializers
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
        # User fields change
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)

        # Passport fields change
        passport_data = validated_data.pop('passport', None)
        if passport_data is not None:
            passport = Passport.objects.filter(user=instance)
            if passport.exists():
                passport.update(**passport_data)
            else:
                Passport.objects.create(user=instance, **passport_data)

        instance.save()
        return instance


class UserRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequisites
        fields = ['id', 'bank_name', 'bic', 'bank_account', 'user_account', 'card_number']


class PasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        user = getattr(self, "user", None) or self.context["request"].user
        # why assert? There are ValidationError / fail everywhere
        assert user is not None

        try:
            validate_password(attrs["new_password"], user)
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})
        return super().validate(attrs)

