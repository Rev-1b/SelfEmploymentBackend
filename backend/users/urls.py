from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView, UserRequisitesViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('', UserViewSet, basename='user')
router.register('requisites', UserRequisitesViewSet, basename='requisites')
# print(router.urls)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/jwt/create/', EmailTokenObtainPairView.as_view(), name='create-token'),
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
]

