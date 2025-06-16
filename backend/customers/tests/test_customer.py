from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from customers.models import Customer, CustomerPassport
from customers.serializers import CustomerInfoSerializer, CustomerDetailSerializer
from users.models import CustomUser


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.customer = Customer.objects.create(
            additional_id=123,
            user=self.user,
            customer_name="Test Customer",
            customer_type=Customer.CustomerTypes.COMMON
        )
        self.passport = CustomerPassport.objects.create(
            customer=self.customer,
            series="1234",
            number="567890",
            release_date="2020-01-01",
            issued="Test Issued",
            unit_code="123-456"
        )

        self.customer_list_url = reverse('customers-list')
        self.customer_detail_url = reverse('customers-detail', args=[self.customer.id])

    def test_get_customer_list(self):
        response = self.client.get(self.customer_list_url)
        customers = Customer.objects.filter(user=self.user)
        serializer = CustomerInfoSerializer(customers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_customer_filtered_list(self):
        response = self.client.get(self.customer_list_url, data={'customer_type': 'COMMON'})
        customers = Customer.objects.filter(user=self.user, customer_type=Customer.CustomerTypes.COMMON)
        serializer = CustomerInfoSerializer(customers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_customer_detail(self):
        response = self.client.get(self.customer_detail_url)
        serializer = CustomerDetailSerializer(self.customer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_customer(self):
        data = {
            "additional_id": 124,
            "customer_name": "New Customer",
            "customer_type": Customer.CustomerTypes.COMMON,
            "passport": {
                "series": "5678",
                "number": "123456",
                "release_date": "2021-01-01",
                "issued": "New Issued",
                "unit_code": "654-321"
            }
        }
        response = self.client.post(self.customer_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(id=response.data['id']).customer_name, "New Customer")

    def test_update_customer(self):
        data = {
            "customer_name": "Updated Customer",
            "customer_type": Customer.CustomerTypes.COMMON
        }
        response = self.client.patch(self.customer_detail_url, data, format='json')
        self.customer.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.customer.customer_name, "Updated Customer")

    def test_delete_customer(self):
        # Тест удаления клиента
        response = self.client.delete(self.customer_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Customer.objects.filter(id=self.customer.id).exists())

    def test_invalid_customer_creation(self):
        data = {
            "additional_id": 125,
            "customer_name": "Invalid Customer",
            "customer_type": "INVALID"
        }
        response = self.client.post(self.customer_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_type", response.data)

    def test_unauthorized_access(self):
        self.client.logout()
        response = self.client.get(self.customer_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_search_customer(self):
        response = self.client.get(self.customer_list_url + '?q=Tes')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)

    def test_bad_search_customer(self):
        response = self.client.get(self.customer_list_url + 'search/?q=ABOBA')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 0)
