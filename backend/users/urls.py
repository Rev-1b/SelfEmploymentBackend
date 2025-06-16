from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, UserViewSet, UserRequisitesViewSet, TelegramAuthView

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='user')
router.register('requisites', UserRequisitesViewSet, basename='requisites')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view(), name='create-token'),
    path("auth/jwt/telegram/", TelegramAuthView.as_view(), name="telegram-auth"),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]
