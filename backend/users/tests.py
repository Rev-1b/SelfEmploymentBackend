from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import CustomUser, Passport
from .cryptography import encrypt_data

main_user = {
    'username': 'TestUser',
    'email': 'test@example.com',
    'password': 'qwerty2F'
}

main_user_auth = {
    'email': 'test@example.com',
    'password': 'qwerty2F'
}

new_user = {
    'username': 'newuser',
    'email': 'newuser@example.com',
    'password': 'qwerty2F'
}


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        super(UserRegistrationTestCase, self).setUp()
        self.user = CustomUser.objects.create_user(**main_user)
        self.token = encrypt_data(self.user.pk)

    def test_create_user(self):
        url = reverse('user-register')
        response = self.client.post(url, new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_user_login(self):
        url = reverse('create-token')
        response = self.client.post(url, main_user_auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_recover_password(self):
        url = reverse('user-recover-password')
        data = {
            'email': 'test@example.com'
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'Письмо отправлено')

    def test_recover_password_confirm(self):
        url = reverse('user-recover-password-confirm') + f'?confirmation_token={self.token}'
        data = {
            'new_password': 'Rev-1bUS^'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"new_password": 'Пароль успешно сменен'})

    def test_update_user_details(self):
        url = reverse('user-profile')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'Smith',
            'passport': {
                'series': '1234',
                'number': '56789',
                'release_date': '2022-01-01',
                'unit_code': 'ABC123'
            }
        }
        self.client.login(**main_user_auth)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = CustomUser.objects.get(email='test@example.com')
        passport = Passport.objects.get(user=user)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.middle_name, 'Smith')
        self.assertEqual(passport.series, '1234')
        self.assertEqual(passport.number, '56789')
        self.assertEqual(passport.release_date.strftime('%Y-%m-%d'), '2022-01-01')
        self.assertEqual(passport.unit_code, 'ABC123')

    # def test_update_user_requisites(self):
    #     url = reverse('user-requisites')
    #     data = {
    #         'bank_name': 'Bank',
    #         'bic': '12345678',
    #         'bank_account': '987654321',
    #         'user_account': '1234567890',
    #         'card_number': '1234567890123456'
    #     }
    #     self.client.login(username='testuser', password='testpassword')
    #     response = self.client.patch(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     user = CustomUser.objects.get(username='testuser')
    #     requisites = user.requisites
    #     self.assertEqual(requisites.bank_name, 'Bank')
    #     self.assertEqual(requisites.bic, '12345678')
    #     self.assertEqual(requisites.bank_account, '987654321')
    #     self.assertEqual(requisites.user_account, '1234567890')
    #     self.assertEqual(requisites.card_number, '1234567890123456')

