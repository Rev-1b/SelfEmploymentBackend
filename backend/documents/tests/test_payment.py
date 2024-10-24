from django.urls import reverse

from documents.models import Payment
from documents.tests.common import DocumentSetUP


class PaymentViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.payment = Payment.objects.create(
            agreement=self.agreement,
            status=Payment.StatusChoices.INITIATED
        )

        self.payment_list_url = reverse('payments-list')
        self.payment_detail_url = reverse('payments-detail', args=[self.payment.id])

    def test_get_payment_list(self):
        self.check_list(self, self.payment_list_url, 1)

    def test_status_filtered_list(self):
        self.check_list(self, self.payment_list_url + f'?status={Payment.StatusChoices.INITIATED}', 1)

    def test_invalid_status_filtered_list(self):
        self.check_bad_filtered_list(self, self.payment_list_url + '?status=IdaE')

    def test_create_payment(self):
        data = {
            "agreement": self.agreement.id
        }
        self.check_create(self, self.payment_list_url, data, Payment, 2)

    def test_delete_payment(self):
        self.check_delete(self, self.payment_detail_url, Payment, 0)
