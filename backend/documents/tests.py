from datetime import date

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from customers.models import Customer
from documents.models import Agreement, Additional, Act, CheckModel, Invoice, UserTemplate, Payment
from users.models import CustomUser


class CRUDLTestMixin:
    list_url = None
    detail_url = None

    @staticmethod
    def check_list(test_case, url_name, expected_number):
        response = test_case.client.get(url_name)
        test_case.assertEqual(response.status_code, status.HTTP_200_OK)
        test_case.assertEqual(len(response.data.get('results')), expected_number)
        return response

    @staticmethod
    def check_bad_filtered_list(test_case, url_name):
        response = test_case.client.get(url_name)
        test_case.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        return response

    @staticmethod
    def check_create(test_case, url_name, body, model, expected_number):
        response = test_case.client.post(url_name, body)
        test_case.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_case.assertEqual(model.objects.count(), expected_number)
        return response

    @staticmethod
    def check_update(test_case, url_name, body, instance):
        response = test_case.client.patch(url_name, body)
        test_case.assertEqual(response.status_code, status.HTTP_200_OK)
        instance.refresh_from_db()
        for attr, value in body.items():
            test_case.assertEqual(getattr(instance, attr), value)
        return response

    @staticmethod
    def check_delete(test_case, url_name, model, expected_number):
        response = test_case.client.delete(url_name)
        test_case.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        test_case.assertEqual(model.objects.count(), expected_number)
        return response


class DocumentSetUP(APITestCase, CRUDLTestMixin):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.customer = Customer.objects.create(
            additional_id=123,
            user=self.user,
            customer_name="Test Customer",
            customer_type="CM"
        )
        self.agreement = Agreement.objects.create(
            customer=self.customer,
            number="AG123456",
            content="Agreement content",
            status=Agreement.StatusChoices.CREATED,
            deal_amount=1000,
            start_date=date.today(),
            end_date=date.today()
        )


class AgreementViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.agreement_list_url = reverse('agreements-list')
        self.agreement_detail_url = reverse('agreements-detail', args=[self.agreement.id])

    def test_get_agreement_list(self):
        self.check_list(self, self.agreement_list_url, 1)

    def test_customer_type_filtered_list(self):
        self.check_list(self, self.agreement_list_url + '?customer__customer_type=CM', 1)

    def test_non_existing_customer_type_filtered_list(self):
        self.check_list(self, self.agreement_list_url + '?customer__customer_type=IE', 0)

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


class AdditionalViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.additional = Additional.objects.create(
            agreement=self.agreement,
            number="AD654321",
            title="Additional title",
            content="Additional content",
            deal_amount=500,
            status='CR'
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


class CheckViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.check = CheckModel.objects.create(
            agreement=self.agreement,
            number="CHK345678",
            amount=300
        )

        self.check_list_url = reverse('checks-list') + f'?agreement_id={self.agreement.id}'
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


class UserTemplateViewSetTests(APITestCase, CRUDLTestMixin):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.template = UserTemplate.objects.create(
            user=self.user,
            title="Template title",
            template_type=UserTemplate.TemplateTypeChoices.AGREEMENT,
            content="Template content"
        )

        self.template_list_url = reverse('templates-list')
        self.template_detail_url = reverse('templates-detail', args=[self.template.id])

    def test_get_user_template_list(self):
        self.check_list(self, self.template_list_url, 1)

    def test_template_type_filtered_list(self):
        self.check_list(self, self.template_list_url + f'?template_type={UserTemplate.TemplateTypeChoices.AGREEMENT}',
                        1)

    def test_invalid_template_type_filtered_list(self):
        self.check_bad_filtered_list(self, self.template_list_url + '?template_type=IdaE')

    def test_create_user_template(self):
        data = {
            "user": self.user.id,
            "title": "New template title",
            "template_type": UserTemplate.TemplateTypeChoices.ADDITIONAL,
            "content": "New template content"
        }
        self.check_create(self, self.template_list_url, data, UserTemplate, 2)

    def test_update_user_template(self):
        data = {
            "title": "Updated template title"
        }
        self.check_update(self, self.template_detail_url, data, self.template)

    def test_delete_user_template(self):
        self.check_delete(self, self.template_detail_url, UserTemplate, 0)


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
