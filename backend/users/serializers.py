from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, Passport, UserRequisites


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = CustomUser.EMAIL_FIELD


class PassportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passport
        fields = '__all__'


class UserRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequisites
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    passport = PassportSerializer()
    requisites = UserRequisitesSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'middle_name', 'passport', 'requisites']

    def update(self, instance, validated_data):
        pass