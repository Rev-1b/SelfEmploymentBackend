from django.urls import path, include
from rest_framework import routers

from .views import AgreementViewSet

agreement_router = routers.DefaultRouter()
agreement_router.register('agreement', AgreementViewSet)


urlpatterns = [
    path('', include(agreement_router.urls)),
    # path('<int:customer_id>/', RegistrationView.as_view()),
]
