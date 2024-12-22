from django.urls import reverse

from documents.models import CheckModel
from documents.tests.common import DocumentSetUP


class CheckViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.check = CheckModel.objects.create(
            agreement=self.agreement,
            number="CHK345678",
            amount=300
        )

        self.check_list_url = reverse('checks-list') + f'?agreement_id={self.agreement.id}'
        self.check_search_url = reverse('checks-search') + f'?agreement_id={self.agreement.id}'
        self.check_detail_url = reverse(
            'checks-detail', args=[self.check.id]) + f'?agreement_id={self.agreement.id}'

    def test_get_check_list(self):
        self.check_list(self, self.check_list_url, 1)

    def test_create_check(self):
        data = {
            "agreement": self.agreement.id,
            "number": "CHK987654",
            "amount": 500
        }
        self.check_create(self, self.check_list_url, data, CheckModel, 2)

    def test_update_check(self):
        data = {
            "amount": 400
        }
        self.check_update(self, self.check_detail_url, data, self.check)

    def test_delete_check(self):
        self.check_delete(self, self.check_detail_url, CheckModel, 0)

    def test_search_check(self):
        self.check_list(self, self.check_search_url + '&q=CHK', 1)

    def test_bad_search_check(self):
        self.check_list(self, self.check_search_url + '&q=DDD', 0)

