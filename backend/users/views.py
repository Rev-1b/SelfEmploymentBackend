from django.contrib.auth.tokens import default_token_generator
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


class RegistrationView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileView(generics.GenericAPIView):
    serializer_class = UserDetailSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserViewSet(viewsets.GenericViewSet):
    def get_permissions(self):
        if self.action == 'register':
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

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        url_path = reverse('user-activation')
        absolute_url = request.build_absolute_uri(url_path)

        send_activation_email(absolute_url, user)

        return Response(serializer.data)

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

    @action(detail=False, methods=['get'])
    def activation(self, request):
        token = request.query_params.get('confirmation_token')
        if token is None:
            raise exceptions.ValidationError(f'Не указан токен подтверждения в параметрах запроса')

        user_id = decrypt_data(token)
        if user_id is None:
            raise exceptions.ValidationError(f'Токен был поврежден, попробуйте получить ссылку активации еще раз')

        user = self.get_queryset().filter(pk=user_id)
        if not user.exists():
            return Response('Пользователь не найден', status=status.HTTP_400_BAD_REQUEST)

        user.update(is_active=True)
        return Response('Email Успешно Подтвержден!')

    @action(detail=False, methods=['post'])
    def reset_password_confirm(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.data.get('user_id')
        user = get_object_or_404(self.get_queryset(), id=user_id)
        user.set_password(serializer.data.get('new_password'))

        return Response('Пароль успешно сменен')

    @action(detail=False, methods=['post'])
    def recover_password(self, request):
        email = request.data.get('email', None)
        if email is None:
            raise exceptions.ValidationError(f'Не указан email в теле запроса')
        user = CustomUser.objects.filter(email=email)

        if not user.exists():
            raise exceptions.ValidationError(f'Указана несуществующая почта')

        url_path = reverse('user-reset_password')
        absolute_url = request.build_absolute_uri(url_path)

        send_password_reset_email(absolute_url, user)
        return Response('Письмо отправлено')


class UserRequisitesViewSet(viewsets.ModelViewSet):
    serializer_class = UserRequisitesSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return UserRequisites.objects.filter(user=self.request.user)
