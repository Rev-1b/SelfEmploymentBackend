from django.urls import path, include
from rest_framework import routers

from . import views as document_views

router = routers.DefaultRouter()
router.register('agreements', document_views.AgreementViewSet, basename='agreements')
router.register('additional', document_views.AdditionalViewSet, basename='additional')
router.register('acts', document_views.ActViewSet, basename='acts')
router.register('checks', document_views.CheckViewSet, basename='checks')
router.register('invoices', document_views.InvoiceViewSet, basename='invoices')
router.register('history', document_views.DocumentHistoryViewSet, basename='history')
router.register('payments', document_views.PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
]
