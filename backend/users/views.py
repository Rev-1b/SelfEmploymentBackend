from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from users.models import CustomUser
from users.serializers import CustomTokenObtainPairSerializer, UserProfileSerializer, RegistrationSerializer


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegistrationView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    queryset = CustomUser.objects.prefetch_related('requisites').all()
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = self.get_serializer(instance=request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
