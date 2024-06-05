from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, ProfileView

urlpatterns = [
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', TokenRefreshView.as_view()),
    path('users/profile/', ProfileView.as_view()),
]
