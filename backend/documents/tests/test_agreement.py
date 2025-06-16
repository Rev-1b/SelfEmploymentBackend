from datetime import date

from django.urls import reverse

from customers.models import Customer
from documents.models import Agreement
from documents.tests.common import DocumentSetUP


class AgreementViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.agreement_list_url = reverse('agreements-list')
        self.agreement_search_url = reverse('agreements-search')
        self.agreement_detail_url = reverse('agreements-detail', args=[self.agreement.id])

    def test_get_agreement_list(self):
        self.check_list(self, self.agreement_list_url, 1)

    def test_customer_type_filtered_list(self):
        self.check_list(self, self.agreement_list_url + f'?customer__customer_type={Customer.CustomerTypes.COMMON}', 1)

    def test_non_existing_customer_type_filtered_list(self):
        self.check_list(self, self.agreement_list_url + f'?customer__customer_type={Customer.CustomerTypes.IE}', 0)

    def test_invalid_customer_type_filtered_list(self):
        self.check_bad_filtered_list(self, self.agreement_list_url + '?customer__customer_type=IdaE')

    def test_status_filtered_list(self):
        self.check_list(self, self.agreement_list_url + f'?status={Agreement.StatusChoices.CREATED}', 1)

    def test_invalid_status_filtered_list(self):
        self.check_bad_filtered_list(self, self.agreement_list_url + '?status=IdaE')

    def test_create_agreement(self):
        data = {
            "customer": self.customer.id,
            "number": "AG654321",
            "content": "New agreement content",
            "status": Agreement.StatusChoices.SIGNED,
            "deal_amount": 2000,
            "start_date": date.today(),
            "end_date": date.today()
        }
        self.check_create(self, self.agreement_list_url, data, Agreement, 2)

    def test_update_agreement(self):
        data = {
            "status": Agreement.StatusChoices.CLOSED
        }

        self.check_update(self, self.agreement_detail_url, data, self.agreement)

    def test_delete_agreement(self):
        self.check_delete(self, self.agreement_detail_url, Agreement, 0)

    def test_search_agreement(self):
        self.check_list(self, self.agreement_search_url + '?q=AG', 1)

    def test_bad_search_agreement(self):
        self.check_list(self, self.agreement_search_url + '?q=DDD', 0)

