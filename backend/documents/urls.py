from django.urls import path, include
from rest_framework import routers

import documents.views.act
import documents.views.additional
import documents.views.agreement
import documents.views.check
import documents.views.history
import documents.views.invoice
import documents.views.payment
import documents.views.project_search
import documents.views.user_template
from . import views as document_views

router = routers.DefaultRouter()
router.register('agreements', documents.views.agreement.AgreementViewSet, basename='agreements')
router.register('additional', documents.views.additional.AdditionalViewSet, basename='additional')
router.register('acts', documents.views.act.ActViewSet, basename='acts')
router.register('checks', documents.views.check.CheckViewSet, basename='checks')
router.register('invoices', documents.views.invoice.InvoiceViewSet, basename='invoices')
router.register('templates', documents.views.user_template.UserTemplateViewSet, basename='templates')
router.register('history', documents.views.history.DocumentHistoryViewSet, basename='history')
router.register('payments', documents.views.payment.PaymentViewSet, basename='payments')
router.register('search', documents.views.project_search.ProjectSearch, basename='search')

urlpatterns = [
    path('', include(router.urls)),
]
