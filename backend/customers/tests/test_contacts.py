from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from customers.models import Customer, CustomerContacts
from customers.serializers import CustomerContactsSerializer
from users.models import CustomUser


class CustomerContactsViewSetTest(APITestCase):
    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные для Customer и CustomerContacts
        self.customer = Customer.objects.create(
            additional_id=123,
            user=self.user,
            customer_name="Test Customer",
            customer_type="CM"
        )
        self.contact = CustomerContacts.objects.create(
            customer=self.customer,
            contact_name="John Doe",
            contact_type="PH",
            contact_info="+123456789"
        )
        CustomerContacts.objects.create(
            customer=self.customer,
            contact_name="John Doe",
            contact_type="EL",
            contact_info="test@gmail.com"
        )

        # URL для тестов
        self.contact_list_url = reverse('customer-contacts-list') + f'?customer_id={self.customer.id}'
        self.contact_detail_url = reverse('customer-contacts-detail',
                                          args=[self.contact.id]) + f'?customer_id={self.customer.id}'

    def test_get_contacts_list(self):
        # Тест получения списка контактов
        response = self.client.get(self.contact_list_url)
        contacts = CustomerContacts.objects.filter(customer__user=self.user)
        serializer = CustomerContactsSerializer(contacts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_contacts_filtered_list(self):
        # Не пользуюсь self.url потому что нужно дополнительно использовать data в client.get()
        response = self.client.get(reverse('customer-contacts-list'),
                                   data={'contact_type': 'PH', 'customer_id': self.customer.id})

        contacts = CustomerContacts.objects.filter(customer__user=self.user, contact_type='PH')
        serializer = CustomerContactsSerializer(contacts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_bad_filter(self):
        response = self.client.get(reverse('customer-contacts-list'),
                                   data={'contact_type': 'PHdsadsf', 'customer_id': self.customer.id})
        # ожидаем 400, так как content_type указан через TextChoices
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_contact_detail(self):
        # Тест получения деталей контакта
        response = self.client.get(self.contact_detail_url)
        serializer = CustomerContactsSerializer(self.contact)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_contact(self):
        # Тест создания контакта
        data = {
            "contact_name": "Jane Doe",
            "contact_type": "EL",
            "contact_info": "jane.doe@example.com",
            "customer": self.customer.id  # ID клиента
        }
        response = self.client.post(self.contact_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomerContacts.objects.count(), 3)
        self.assertEqual(CustomerContacts.objects.get(id=response.data['id']).contact_name, "Jane Doe")

    def test_update_contact(self):
        # Тест обновления контакта
        data = {
            "contact_name": "Updated Name"
        }
        response = self.client.patch(self.contact_detail_url, data, format='json')
        self.contact.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.contact.contact_name, "Updated Name")

    def test_delete_contact(self):
        # Тест удаления контакта
        response = self.client.delete(self.contact_detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CustomerContacts.objects.filter(id=self.contact.id).exists())

    def test_invalid_contact_creation(self):
        # Тест создания контакта с неверными данными
        data = {
            "contact_name": "",  # Пустое имя контакта
            "contact_type": "EL",
            "contact_info": "jane.doe@example.com",
            "customer": self.customer.id
        }
        response = self.client.post(self.contact_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("contact_name", response.data)

    def test_unauthorized_access(self):
        # Тест попытки доступа без авторизации
        self.client.logout()
        response = self.client.get(self.contact_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
