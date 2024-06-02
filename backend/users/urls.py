from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import EmailTokenObtainPairView

urlpatterns = [
    path('create/', EmailTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]
