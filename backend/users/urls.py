from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, ProfileView, RegistrationView, UserRequisitesViewSet

router = routers.DefaultRouter()
router.register('requisites', UserRequisitesViewSet, basename='requisites')

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', TokenRefreshView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('', include(router.urls)),
]
