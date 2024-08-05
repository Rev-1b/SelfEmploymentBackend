from django.urls import reverse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from project.pagination import StandardResultsSetPagination
from users.models import CustomUser, UserRequisites
from users.serializers import CustomTokenObtainPairSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserRequisitesSerializer, OldToNewPasswordSerializer, EmailSerializer, NewPasswordSerializer
from users.tasks import send_activation_email, send_password_reset_email
from .cryptography import decrypt_data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.GenericViewSet):
    def get_permissions(self):
        if self.action in ['register', 'activation', 'recover_password_confirm', 'recover_password']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'register':
            serializer_class = UserCreateSerializer
        elif self.action in ['recover_password', 'change_email']:
            serializer_class = EmailSerializer
        elif self.action == 'recover_password_confirm':
            serializer_class = NewPasswordSerializer
        elif self.action == 'change_password':
            serializer_class = OldToNewPasswordSerializer
        else:
            serializer_class = UserDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    # ------------------------------------------------------------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # sending activation email
        url_path = reverse('user-activation')
        absolute_url = request.build_absolute_uri(url_path)
        send_activation_email(absolute_url, user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('confirmation_token', openapi.IN_QUERY, description="Auto Generated Token", type=openapi.TYPE_STRING, required=True)
    ])
    def activation(self, request):
        user = self.get_user_from_token(request)
        if not user.exists():
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_400_BAD_REQUEST)

        user.update(is_email_verified=True)
        return Response({'email': 'Email Успешно Подтвержден!'})

    @action(detail=False, methods=['post'])
    def change_email(self, request):
        user = request.user

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.data.get('email')

        if user.email != new_email:
            if self.get_queryset().filter(email=new_email).exists():
                raise exceptions.ValidationError({'email': 'Пользователь с такой электронной почтой уже существует'})
            user.email = new_email
            user.save()

        # sending activation email
        url_path = reverse('user-activation')
        absolute_url = request.build_absolute_uri(url_path)
        send_activation_email(absolute_url, user)

        return Response({'user': user.email},
                        status=status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.data.get('old_password')
        new_password = serializer.data.get('new_password')

        # check old password
        if not user.check_password(old_password):
            return Response({'error': 'Старый пароль введен неверно'}, status=status.HTTP_400_BAD_REQUEST)

        # Изменяем пароль
        user.set_password(new_password)
        user.save()

        return Response({'success': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def recover_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        user = CustomUser.objects.filter(email=email)

        if not user.exists():
            raise exceptions.ValidationError({'email': 'Указана несуществующая почта'})

        url_path = reverse('user-recover-password-confirm')
        absolute_url = request.build_absolute_uri(url_path)
        send_password_reset_email(absolute_url, user.first())

        return Response({'email': 'Письмо отправлено'})

    @action(detail=False, methods=['post'])
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('confirmation_token', openapi.IN_QUERY, description="Auto Generated Token", type=openapi.TYPE_STRING, required=True)
    ])
    def recover_password_confirm(self, request):
        user = self.get_user_from_token(request)
        if not user.exists():
            return Response('Пользователь не найден', status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user.first().set_password(serializer.data.get('new_password'))

        return Response({"new_password": 'Пароль успешно сменен'})

    def get_user_from_token(self, request):
        token = request.query_params.get('confirmation_token')
        if token is None:
            raise exceptions.ValidationError({'token': f'Не указан токен подтверждения в параметрах запроса'})

        user_id = decrypt_data(token)
        if user_id is None:
            raise exceptions.ValidationError(
                {'token': f'Токен был поврежден, попробуйте получить ссылку активации еще раз'})

        return self.get_queryset().filter(id=user_id)


class UserRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserRequisites.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.get_queryset().create(user=request.user, **serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
