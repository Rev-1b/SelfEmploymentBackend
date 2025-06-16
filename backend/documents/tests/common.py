from datetime import date

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from customers.models import Customer
from documents.models import Agreement
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
            customer_type=Customer.CustomerTypes.COMMON
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
