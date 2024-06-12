from django.urls import path, include
from rest_framework import routers

from .views import AgreementViewSet, AgreementView

# router = routers.DefaultRouter()
# router.register('agreements', AgreementViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('agreements/', AgreementView.as_view()),
]
