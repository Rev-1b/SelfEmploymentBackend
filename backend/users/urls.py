from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, ProfileView, RegistrationView

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', TokenRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
]
