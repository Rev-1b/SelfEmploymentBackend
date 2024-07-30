from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Customer, CustomerRequisites, CustomerContacts, CustomUser, CustomerPassport
from .serializers import CustomerRequisitesSerializer, CustomerContactsSerializer, CustomerListSerializer, \
    CustomerDetailSerializer


class CustomerViewSetTest(APITestCase):
    def setUp(self):
        # Создаем пользователя и логинимся
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Создаем тестовые данные для Customer и CustomerPassport
        self.customer = Customer.objects.create(
            additional_id=123,
            user=self.user,
            customer_name="Test Customer",
            customer_type="CM"
        )
        self.passport = CustomerPassport.objects.create(
            customer=self.customer,
            series="1234",
            number="567890",
            release_date="2020-01-01",
            issued="Test Issued",
            unit_code="123-456"
        )

        # URL для тестов
        self.customer_list_url = reverse('customers-list')
        self.customer_detail_url = reverse('customers-detail', args=[self.customer.id])

    def test_get_customer_list(self):
        # Тест получения списка клиентов
        response = self.client.get(self.customer_list_url)
        customers = Customer.objects.filter(user=self.user)
        serializer = CustomerListSerializer(customers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_customer_filtered_list(self):
        response = self.client.get(self.customer_list_url, data={'customer_type': 'CM'})
        customers = Customer.objects.filter(user=self.user, customer_type='CM')
        serializer = CustomerListSerializer(customers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_customer_detail(self):
        # Тест получения деталей клиента
        response = self.client.get(self.customer_detail_url)
        serializer = CustomerDetailSerializer(self.customer)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_customer(self):
        # Тест создания клиента
        data = {
            "additional_id": 124,
            "customer_name": "New Customer",
            "customer_type": "CM",
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
        # Тест обновления клиента
        data = {
            "customer_name": "Updated Customer",
            "customer_type": "CM"
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
        # Тест создания клиента с неверными данными
        data = {
            "additional_id": 125,
            "customer_name": "Invalid Customer",
            "customer_type": "INVALID"  # Некорректный тип клиента
        }
        response = self.client.post(self.customer_list_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_type", response.data)

    def test_unauthorized_access(self):
        # Тест попытки доступа без авторизации
        self.client.logout()
        response = self.client.get(self.customer_list_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
        self.requisite_list_url = reverse('customer-requisites-list') + f'?customer_id={self.customer.id}'
        self.requisite_detail_url = reverse('customer-requisites-detail',
                                            args=[self.requisite.id]) + f'?customer_id={self.customer.id}'

    def test_get_requisites_list(self):
        # Тест получения списка реквизитов
        response = self.client.get(self.requisite_list_url)
        requisites = CustomerRequisites.objects.filter(customer__user=self.user)
        serializer = CustomerRequisitesSerializer(requisites, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_requisites_filtered_list(self):
        # Не пользуюсь self.url потому что нужно дополнительно использовать data в client.get()
        response = self.client.get(reverse('customer-requisites-list'),
                                   data={'bank_name': 'Sberbank', 'customer_id': self.customer.id})
        requisites = CustomerRequisites.objects.filter(customer__user=self.user, bank_name='Sberbank')
        serializer = CustomerRequisitesSerializer(requisites, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_bad_filter(self):
        # Не пользуюсь self.url потому что нужно дополнительно использовать data в client.get()
        response = self.client.get(reverse('customer-requisites-list'),
                                   data={'bank_name': 'Sberbankswdfsd', 'customer_id': self.customer.id})
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
