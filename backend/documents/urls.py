from django.urls import path, include
from rest_framework import routers

from .views import AgreementViewSet

router = routers.DefaultRouter()
router.register('agreements', AgreementViewSet, basename='agreements')

urlpatterns = [
    path('', include(router.urls)),
    # path('agreements/', AgreementView.as_view()),
    # path('additional/', AdditionalView.as_view()),
]
