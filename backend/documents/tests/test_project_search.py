from django.urls import reverse

from documents.models import Additional, Act, CheckModel, Invoice, Payment
from documents.tests.common import DocumentSetUP


class GlobalSearchTest(DocumentSetUP):
    def setUp(self):
        super().setUp()

        self.additional = Additional.objects.create(
            agreement=self.agreement,
            number="AD654321",
            title="Additional title",
            content="Additional content",
            deal_amount=500,
            status=Additional.StatusChoices.CREATED
        )

        self.act = Act.objects.create(
            agreement=self.agreement,
            number="ACT789012",
            title="Act title",
            content="Act content",
            status=Act.StatusChoices.CREATED
        )

        self.check = CheckModel.objects.create(
            agreement=self.agreement,
            number="CHK345678",
            amount=300
        )

        self.invoice = Invoice.objects.create(
            agreement=self.agreement,
            number="INV901234",
            amount=400
        )

        self.payment = Payment.objects.create(
            agreement=self.agreement,
            additional=self.additional,
            status=Payment.StatusChoices.INITIATED,
            act=self.act,
            check_link=self.check,
            invoice=self.invoice,
        )

    def test_search_by_customer_name(self):
        response = self.client.get(reverse('search-list') + '?q=Test')
