from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, ProfileView, RegistrationView, UserRequisitesViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='profile')
router.register('requisites', UserRequisitesViewSet, basename='requisites')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view()),
    path('auth/jwt/refresh/', TokenRefreshView.as_view()),
    # path('register/', RegistrationView.as_view()),
    # path('profile/', ProfileView.as_view()),
]

