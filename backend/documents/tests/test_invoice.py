from django.urls import reverse

from documents.models import Invoice
from documents.tests.common import DocumentSetUP


class InvoiceViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.invoice = Invoice.objects.create(
            agreement=self.agreement,
            number="INV901234",
            amount=400
        )

        self.invoice_list_url = reverse('invoices-list') + f'?agreement_id={self.agreement.id}'
        self.invoice_detail_url = reverse(
            'invoices-detail', args=[self.invoice.id]) + f'?agreement_id={self.agreement.id}'

    def test_get_invoice_list(self):
        self.check_list(self, self.invoice_list_url, 1)

    def test_status_filtered_list(self):
        self.check_list(self, self.invoice_list_url + f'&status={Invoice.StatusChoices.CREATED}', 1)

    def test_invalid_status_filtered_list(self):
        self.check_bad_filtered_list(self, self.invoice_list_url + '&status=IdaE')

    def test_create_invoice(self):
        data = {
            "agreement": self.agreement.id,
            "number": "INV123456",
            "amount": 600
        }
        self.check_create(self, self.invoice_list_url, data, Invoice, 2)

    def test_update_invoice(self):
        data = {
            "amount": 500
        }
        self.check_update(self, self.invoice_detail_url, data, self.invoice)

    def test_delete_invoice(self):
        self.check_delete(self, self.invoice_detail_url, Invoice, 0)
