from django.urls import path
from rest_framework import routers

from customers.views import CustomerPageView, CustomerDetailViewSet

router = routers.DefaultRouter()
router.register('', )


urlpatterns = [
    path('', CustomerPageView.as_view()),
    # path('<int:customer_id>/', RegistrationView.as_view()),
]
