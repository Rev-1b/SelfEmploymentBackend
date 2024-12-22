from django.urls import reverse

from documents.models import Act
from documents.tests.common import DocumentSetUP


class ActViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.act = Act.objects.create(
            agreement=self.agreement,
            number="ACT789012",
            title="Act title",
            content="Act content",
            status=Act.StatusChoices.CREATED
        )

        self.act_list_url = reverse('acts-list') + f'?agreement_id={self.agreement.id}'
        self.act_search_url = reverse('acts-search') + f'?agreement_id={self.agreement.id}'
        self.act_detail_url = reverse(
            'acts-detail', args=[self.act.id]) + f'?agreement_id={self.agreement.id}'

    def test_get_act_list(self):
        self.check_list(self, self.act_list_url, 1)

    def test_status_filtered_list(self):
        self.check_list(self, self.act_list_url + f'&status={Act.StatusChoices.CREATED}', 1)

    def test_invalid_status_filtered_list(self):
        self.check_bad_filtered_list(self, self.act_list_url + '&status=IdaE')

    def test_create_act(self):
        data = {
            "agreement": self.agreement.id,
            "number": "ACT123456",
            "title": "New act title",
            "content": "New act content",
            "status": Act.StatusChoices.CREATED
        }
        self.check_create(self, self.act_list_url, data, Act, 2)

    def test_update_act(self):
        data = {
            "title": "Updated act title"
        }
        self.check_update(self, self.act_detail_url, data, self.act)

    def test_delete_act(self):
        self.check_delete(self, self.act_detail_url, Act, 0)

    def test_search_act(self):
        self.check_list(self, self.act_search_url + '&q=ACT', 1)

    def test_bad_search_act(self):
        self.check_list(self, self.act_search_url + '&q=DDD', 0)
