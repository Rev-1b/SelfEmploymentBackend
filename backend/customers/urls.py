from django.urls import path
from customers.views import CustomerPageView

urlpatterns = [
    path('', CustomerPageView.as_view()),
    # path('<int:customer_id>/', RegistrationView.as_view()),
]
