from django.urls import reverse

from documents.models import Additional
from documents.tests.common import DocumentSetUP


class AdditionalViewSetTests(DocumentSetUP):
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

        self.additional_list_url = reverse('additional-list') + f'?agreement_id={self.agreement.id}'
        self.additional_detail_url = reverse(
            'additional-detail', args=[self.additional.id]) + f'?agreement_id={self.agreement.id}'

    def test_get_additional_list(self):
        self.check_list(self, self.additional_list_url, 1)

    def test_status_filtered_list(self):
        self.check_list(self, self.additional_list_url + f'&status={Additional.StatusChoices.CREATED}', 1)

    def test_invalid_status_filtered_list(self):
        self.check_bad_filtered_list(self, self.additional_list_url + '&status=IdaE')

    def test_create_additional(self):
        data = {
            "agreement": self.agreement.id,
            "number": "AD987654",
            "title": "New additional title",
            "content": "New additional content",
            "deal_amount": 800
        }
        self.check_create(self, self.additional_list_url, data, Additional, 2)

    def test_update_additional(self):
        data = {
            "title": "Updated additional title"
        }
        self.check_update(self, self.additional_detail_url, data, self.additional)

    def test_delete_additional(self):
        self.check_delete(self, self.additional_detail_url, Additional, 0)
