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

    @staticmethod
    def check_create(test_case, url_name, body, model, expected_number):
        response = test_case.client.post(url_name, body)
        test_case.assertEqual(response.status_code, status.HTTP_201_CREATED)
        test_case.assertEqual(model.objects.count(), expected_number)

    @staticmethod
    def check_update(test_case, url_name, body, instance):
        response = test_case.client.patch(url_name, body)
        test_case.assertEqual(response.status_code, status.HTTP_200_OK)
        instance.refresh_from_db()
        for attr, value in body.items():
            test_case.assertEqual(getattr(instance, attr), value)

    @staticmethod
    def check_delete(test_case, url_name, model, expected_number):
        response = test_case.client.delete(url_name)
        test_case.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        test_case.assertEqual(model.objects.count(), expected_number)


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
        response = self.client.get(self.agreement_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

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
        response = self.client.post(self.agreement_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Agreement.objects.count(), 2)

    def test_update_agreement(self):
        data = {
            "status": Agreement.StatusChoices.CLOSED
        }
        response = self.client.patch(self.agreement_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.agreement.refresh_from_db()
        self.assertEqual(self.agreement.status, Agreement.StatusChoices.CLOSED)

    def test_delete_agreement(self):
        response = self.client.delete(self.agreement_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Agreement.objects.count(), 0)


class AdditionalViewSetTests(DocumentSetUP):
    def setUp(self):
        super().setUp()
        self.additional = Additional.objects.create(
            agreement=self.agreement,
            number="AD654321",
            title="Additional title",
            content="Additional content",
            deal_amount=500
        )

        self.additional_list_url = reverse('additional-list')
        self.additional_detail_url = reverse('additional-detail', args=[self.additional.id])

    def test_get_additional_list(self):
        response = self.client.get(f'{self.additional_list_url}?agreement_id={self.agreement.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_create_additional(self):
        data = {
            "agreement": self.agreement.id,
            "number": "AD987654",
            "title": "New additional title",
            "content": "New additional content",
            "deal_amount": 800
        }
        response = self.client.post(self.additional_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Additional.objects.count(), 2)

    def test_update_additional(self):
        data = {
            "title": "Updated additional title"
        }
        response = self.client.patch(f'{self.additional_detail_url}?agreement_id={self.agreement.id}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.additional.refresh_from_db()
        self.assertEqual(self.additional.title, "Updated additional title")

    def test_delete_additional(self):
        response = self.client.delete(f'{self.additional_detail_url}?agreement_id={self.agreement.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Additional.objects.count(), 0)


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

        self.act_list_url = reverse('acts-list')
        self.act_detail_url = reverse('acts-detail', args=[self.act.id])

    def test_get_act_list(self):
        response = self.client.get(f'{self.act_list_url}?agreement_id={self.agreement.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_create_act(self):
        data = {
            "agreement": self.agreement.id,
            "number": "ACT123456",
            "title": "New act title",
            "content": "New act content",
            "status": Act.StatusChoices.CREATED
        }
        response = self.client.post(self.act_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Act.objects.count(), 2)

    def test_update_act(self):
        data = {
            "title": "Updated act title"
        }
        response = self.client.patch(f'{self.act_detail_url}?agreement_id={self.agreement.id}', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.act.refresh_from_db()
        self.assertEqual(self.act.title, "Updated act title")

    def test_delete_act(self):
        response = self.client.delete(f'{self.act_detail_url}?agreement_id={self.agreement.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Act.objects.count(), 0)


# class CheckViewSetTests(DocumentSetUP):
#     def setUp(self):
#         super().setUp()
#         self.check = CheckModel.objects.create(
#             agreement=self.agreement,
#             number="CHK345678",
#             amount=300
#         )
#
#         self.check_list_url = reverse('checks-list')
#         self.check_detail_url = reverse('checks-detail', args=[self.check.id])
#
#     def test_get_check_list(self):
#         response = self.client.get(f'{self.check_list_url}?agreement_id={self.agreement.id}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data.get('result')), 1)
#
#     def test_create_check(self):
#         data = {
#             "agreement": self.agreement.id,
#             "number": "CHK987654",
#             "amount": 500
#         }
#         response = self.client.post(f'{self.check_list_url}?agreement_id={self.agreement.id}', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(CheckModel.objects.count(), 2)
#
#     def test_update_check(self):
#         data = {
#             "amount": 400
#         }
#         response = self.client.patch(f'/api/checks/{self.check.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.check.refresh_from_db()
#         self.assertEqual(self.check.amount, 400)
#
#     def test_delete_check(self):
#         response = self.client.delete(f'/api/checks/{self.check.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(CheckModel.objects.count(), 0)

#
# class InvoiceViewSetTests(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CustomUser.objects.create_user(username="testuser", password="password")
#         self.client.force_authenticate(user=self.user)
#         self.customer = Customer.objects.create(user=self.user, customer_name="Test Customer")
#         self.agreement = Agreement.objects.create(
#             customer=self.customer,
#             number="AG123456",
#             content="Agreement content",
#             status=Agreement.StatusChoices.CREATED,
#             deal_amount=1000,
#             start_date=date.today(),
#             end_date=date.today()
#         )
#         self.invoice = Invoice.objects.create(
#             agreement=self.agreement,
#             number="INV901234",
#             amount=400
#         )
#
#     def test_get_invoice_list(self):
#         response = self.client.get(f'/api/invoices/?agreement_id={self.agreement.id}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_invoice(self):
#         data = {
#             "agreement": self.agreement.id,
#             "number": "INV123456",
#             "amount": 600
#         }
#         response = self.client.post('/api/invoices/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Invoice.objects.count(), 2)
#
#     def test_update_invoice(self):
#         data = {
#             "amount": 500
#         }
#         response = self.client.patch(f'/api/invoices/{self.invoice.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.invoice.refresh_from_db()
#         self.assertEqual(self.invoice.amount, 500)
#
#     def test_delete_invoice(self):
#         response = self.client.delete(f'/api/invoices/{self.invoice.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Invoice.objects.count(), 0)
#
#
# class UserTemplateViewSetTests(APITestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CustomUser.objects.create_user(username="testuser", password="password")
#         self.client.force_authenticate(user=self.user)
#         self.template = UserTemplate.objects.create(
#             user=self.user,
#             title="Template title",
#             template_type=UserTemplate.TemplateTypeChoices.AGREEMENT,
#             content="Template content"
#         )
#
#     def test_get_user_template_list(self):
#         response = self.client.get('/api/user_templates/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_user_template(self):
#         data = {
#             "user": self.user.id,
#             "title": "New template title",
#             "template_type": UserTemplate.TemplateTypeChoices.ADDITIONAL,
#             "content": "New template content"
#         }
#         response = self.client.post('/api/user_templates/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(UserTemplate.objects.count(), 2)
#
#     def test_update_user_template(self):
#         data = {
#             "title": "Updated template title"
#         }
#         response = self.client.patch(f'/api/user_templates/{self.template.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.template.refresh_from_db()
#         self.assertEqual(self.template.title, "Updated template title")
#
#     def test_delete_user_template(self):
#         response = self.client.delete(f'/api/user_templates/{self.template.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(UserTemplate.objects.count(), 0)
#
#
# class PaymentViewSetTests(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user = CustomUser.objects.create_user(username="testuser", password="password")
#         self.client.force_authenticate(user=self.user)
#         self.customer = Customer.objects.create(user=self.user, customer_name="Test Customer")
#         self.agreement = Agreement.objects.create(
#             customer=self.customer,
#             number="AG123456",
#             content="Agreement content",
#             status=Agreement.StatusChoices.CREATED,
#             deal_amount=1000,
#             start_date=date.today(),
#             end_date=date.today()
#         )
#         self.payment = Payment.objects.create(
#             agreement=self.agreement
#         )
#
#     def test_get_payment_list(self):
#         response = self.client.get(f'/api/payments/?agreement_id={self.agreement.id}')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_payment(self):
#         data = {
#             "agreement": self.agreement.id
#         }
#         response = self.client.post('/api/payments/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Payment.objects.count(), 2)
#
#     def test_delete_payment(self):
#         response = self.client.delete(f'/api/payments/{self.payment.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Payment.objects.count(), 0)
