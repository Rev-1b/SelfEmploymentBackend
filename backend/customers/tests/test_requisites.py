from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from customers.models import Customer, CustomerRequisites
from customers.serializers import CustomerRequisitesSerializer
from users.models import CustomUser


class CustomerRequisitesViewSetTest(APITestCase):
    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные для Customer и CustomerRequisites
        self.customer = Customer.objects.create(
            additional_id=123,
            user=self.user,
            customer_name="Test Customer",
            customer_type="CM"
        )
        self.requisite = CustomerRequisites.objects.create(
            customer=self.customer,
            bank_name="Test Bank",
            bic="123456789",
            bank_account="000000000000",
            customer_account_number="1234567890123456"
        )
        CustomerRequisites.objects.create(
            customer=self.customer,
            bank_name="Sberbank",
            bic="123456789",
            bank_account="000000000000",
            customer_account_number="1234567890123456"
        )

        # URL для тестов
        self.requisite_list_url = reverse('customer-requisites-list', kwargs={'customer_pk': self.customer.pk})
        self.requisite_detail_url = reverse(
            'customer-requisites-detail',
            kwargs={'customer_pk': self.customer.pk, 'pk': self.requisite.pk}
        )

    def test_get_requisites_list(self):
        # Тест получения списка реквизитов
        response = self.client.get(self.requisite_list_url)
        requisites = CustomerRequisites.objects.filter(customer__user=self.user)
        serializer = CustomerRequisitesSerializer(requisites, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_requisites_filtered_list(self):
        response = self.client.get(self.requisite_list_url, data={'bank_name': 'Sberbank'})
        requisites = CustomerRequisites.objects.filter(customer__user=self.user, bank_name='Sberbank')
        serializer = CustomerRequisitesSerializer(requisites, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_bad_filter(self):
        response = self.client.get(self.requisite_list_url, data={'bank_name': 'Sberbanksdfsdfs'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), [])

    def test_get_requisite_detail(self):
        # Тест получения деталей реквизита
        response = self.client.get(self.requisite_detail_url)
        serializer = CustomerRequisitesSerializer(self.requisite)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_requisite(self):
        # Тест создания реквизита
        data = {
            "bank_name": "New Bank",
            "bic": "987654321",
            "bank_account": "111111111111",
            "customer_account_number": "6543210987654321",
            "customer": self.customer.id  # ID клиента
        }
        response = self.client.post(self.requisite_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerRequisites.objects.count(), 3)
        self.assertEqual(CustomerRequisites.objects.get(id=response.data['id']).bank_name, "New Bank")

    def test_update_requisite(self):
        # Тест обновления реквизита
        data = {
            "bank_name": "Updated Bank"
        }
        response = self.client.patch(self.requisite_detail_url, data, format='json')
        self.requisite.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.requisite.bank_name, "Updated Bank")

    def test_delete_requisite(self):
        # Тест удаления реквизита
        response = self.client.delete(self.requisite_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomerRequisites.objects.filter(id=self.requisite.id).exists())

    def test_invalid_requisite_creation(self):
        # Тест создания реквизита с неверными данными
        data = {
            "bank_name": "",  # Пустое название банка
            "bic": "987654321",
            "bank_account": "111111111111",
            "customer_account_number": "6543210987654321",
            "customer": self.customer.id
        }
        response = self.client.post(self.requisite_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bank_name", response.data)

    def test_unauthorized_access(self):
        # Тест попытки доступа без авторизации
        self.client.logout()
        response = self.client.get(self.requisite_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
