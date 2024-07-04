from django.urls import reverse
from rest_framework import generics, viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from project.pagination import StandardResultsSetPagination
from users.models import CustomUser, UserRequisites
from users.serializers import CustomTokenObtainPairSerializer, UserDetailSerializer, UserCreateSerializer, \
    UserRequisitesSerializer, PasswordSerializer
from users.tasks import send_activation_email, send_password_reset_email
from .cryptography import decrypt_data


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.GenericViewSet):
    def get_permissions(self):
        if self.action in ['register', 'activation', 'reset_password_confirm', 'recover_password']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.action == 'register':
            serializer_class = UserCreateSerializer
        elif self.action == 'reset_password':
            serializer_class = PasswordSerializer
        else:
            serializer_class = UserDetailSerializer
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(detail=False, methods=['get', 'patch'])
    def profile(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.serializer_class(request.user, data=request.data, partial=True)
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

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def activation(self, request):
        user = self.get_user_from_token(request)
        if not user.exists():
            return Response('Пользователь не найден', status=status.HTTP_400_BAD_REQUEST)

        user.update(is_active=True)
        return Response('Email Успешно Подтвержден!')

    @action(detail=False, methods=['post'])
    def change_email(self, request):
        user = request.user

        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        new_email = serializer.data.get('email')

        if user.email != new_email:
            user.email = new_email
            user.save()

        # sending activation email
        url_path = reverse('user-activation')
        absolute_url = request.build_absolute_uri(url_path)
        send_activation_email(absolute_url, user)

        return Response({'success': 'Email успешно изменен. Письмо для активации отправлено'},
                        status=status.HTTP_200_OK)

    # ------------------------------------------------------------------------------------------------------------------
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        user = request.user  # get authorizer user

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # check old password
        if not user.check_password(old_password):
            return Response({'error': 'Старый пароль введен неверно'}, status=status.HTTP_400_BAD_REQUEST)

        # Изменяем пароль
        user.set_password(new_password)
        user.save()

        return Response({'success': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def recover_password(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get('email')
        user = CustomUser.objects.filter(email=email)

        if not user.exists():
            raise exceptions.ValidationError({'email': 'Указана несуществующая почта'})

        url_path = reverse('user-reset_password')
        absolute_url = request.build_absolute_uri(url_path)
        send_password_reset_email(absolute_url, user)

        return Response('Письмо отправлено')

    @action(detail=False, methods=['post'])
    def recover_password_confirm(self, request):
        user = self.get_user_from_token(request)

        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get('new_password'))

        return Response({"new_password": 'Пароль успешно сменен'})

    def get_user_from_token(self, request):
        token = request.query_params.get('confirmation_token')
        if token is None:
            raise exceptions.ValidationError(f'Не указан токен подтверждения в параметрах запроса')

        user_id = decrypt_data(token)
        if user_id is None:
            raise exceptions.ValidationError(f'Токен был поврежден, попробуйте получить ссылку активации еще раз')

        return get_object_or_404(self.get_queryset(), id=user_id)


class UserRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserRequisites.objects.filter(user=self.request.user)


