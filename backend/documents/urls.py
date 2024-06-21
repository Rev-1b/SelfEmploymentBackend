from django.urls import path, include
from rest_framework import routers

from . import views as document_views

router = routers.DefaultRouter()
router.register('agreements', document_views.AgreementViewSet, basename='agreements')
router.register('additional', document_views.AgreementViewSet, basename='additional')
router.register('acts', document_views.AgreementViewSet, basename='acts')
router.register('checks', document_views.AgreementViewSet, basename='checks')
router.register('invoices', document_views.AgreementViewSet, basename='invoices')
router.register('deals', document_views.DealsViewSet, basename='deals')

urlpatterns = [
    path('', include(router.urls)),
    # path('agreements/', AgreementView.as_view()),
    # path('additional/', AdditionalView.as_view()),
]
