from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import CustomUser
from ..serializers import TelegramAuthSerializer
from ..utils import verify_telegram_auth


class TelegramAuthView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = TelegramAuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if not verify_telegram_auth(data, settings.TELEGRAM_BOT_TOKEN):
            return Response({"detail": "Invalid Telegram signature"}, status=401)

        # Возможная проблема, если аккаунт уже существует
        telegram_id = data["id"]
        user, _ = CustomUser.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": f"tg_{telegram_id}",
                "first_name": data.get("first_name", ""),
                "last_name": data.get("last_name", ""),
            }
        )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })


__all__ = ["TelegramAuthView"]