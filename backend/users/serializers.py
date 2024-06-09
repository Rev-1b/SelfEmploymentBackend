from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Passport, UserRequisites


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        # if settings.SEND_ACTIVATION_EMAIL:
        #     user.is_active = False
        #     user.save(update_fields=["is_active"])
        return user


# auth through email
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD


# profile serializers
class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        # read_only_fields = ['id']
        fields = ['series', 'number', 'release_date', 'unit_code']


class UserRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequisites
        # read_only_fields = ['id']
        fields = ['bank_name', 'bic', 'bank_account', 'user_account', 'card_number']


class UserProfileSerializer(serializers.ModelSerializer):
    passport = PassportSerializer()
    requisites = UserRequisitesSerializer(many=True)

    class Meta:
        model = CustomUser
        read_only_fields = ['email', 'username']
        fields = ['email', 'username', 'first_name', 'last_name', 'middle_name', 'passport', 'requisites']

    def update(self, instance, validated_data):
        # User fields change
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)

        # Passport fields change
        passport_data = validated_data.get('passport')
        if passport_data is not None:
            if hasattr(instance, 'passport'):
                passport = instance.passport
                passport.series = passport_data.get('series', passport.series)
                passport.number = passport_data.get('number', passport.number)
                passport.release_date = passport_data.get('release_date', passport.release_date)
                passport.unit_code = passport_data.get('unit_code', passport.unit_code)
                passport.save()
            else:
                Passport.objects.create(user=instance, **passport_data)

        # Requisites fields change
        requisites_data = validated_data.get('requisites')
        if requisites_data is not None:
            if hasattr(instance, 'requisites'):
                UserRequisites.objects.filter(user=instance).delete()
            UserRequisites.objects.bulk_create(
                [UserRequisites(user=instance, **data) for data in requisites_data]
            )

        instance.save()
        return instance
