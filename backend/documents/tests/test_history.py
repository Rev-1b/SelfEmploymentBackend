from django.urls import reverse
from rest_framework import status

from documents.models import Additional, Act, CheckModel, Invoice
from documents.tests.common import DocumentSetUP


class DocumentHistoryViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()

        self.additional = Additional.objects.create(
            agreement=self.agreement,
            number="AD654321",
            title="Additional title",
            content="Additional content",
            deal_amount=500
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

    def test_history_result(self):
        response = self.client.get(f'{reverse("history-list")}?records_number=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('latest_records')), 5)
