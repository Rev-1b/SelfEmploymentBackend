from rest_framework import serializers

from users.models import UserRequisites


class UserRequisitesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequisites
        fields = ['id', 'bank_name', 'bic', 'bank_account', 'user_account', 'card_number']
        # extra_kwargs = {
        #     'id': {'read_only': True}
        # }


__all__ = ['UserRequisitesSerializer']