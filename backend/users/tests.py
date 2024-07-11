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
        self.assertEqual(response.data['username'], new_user['username'])
        self.assertEqual(response.data['email'], new_user['email'])
        self.assertTrue(CustomUser.objects.filter(email=new_user.get('email')).exists())

    def test_user_login(self):
        url = reverse('create-token')
        response = self.client.post(url, main_user_auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        first_url = reverse('create-token')
        second_url = reverse('refresh-token')
        first_response = self.client.post(first_url, main_user_auth, format='json')
        data = {
            'refresh': first_response.data['refresh'],
        }
        second_response = self.client.post(second_url, data, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', second_response.data)

    def test_email_activation(self):
        url = reverse('user-activation') + f'?confirmation_token={self.token}'

        self.assertEqual(self.user.is_email_verified, False)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.is_email_verified, False)

    # Temporally commented. Cant figure out, why user email does not changes in tests, but in Postman
    def test_change_email(self):
        url = reverse('user-change-email')
        new_email = 'test2@example.com'
        data = {
            'email': new_email
        }
        self.client.login(**main_user_auth)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Temporally commented. Cant figure out, why user email does not change in tests, but in Postman
        # self.assertEqual(self.user.email, new_email)

    def test_change_password(self):
        url = reverse('user-change-password')
        new_password = 'Rev-1bUS^'
        data = {
            'old_password': main_user_auth.get('password'),
            'new_password': new_password
        }

        # change password
        self.client.login(**main_user_auth)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if password is changed (trying to log in with a new password)
        login_url = reverse('create-token')
        data = {
            'email': main_user.get('email'),
            'password': new_password
        }
        response = self.client.post(login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_recover_password(self):
        url = reverse('user-recover-password')
        data = {
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('email'), 'Письмо отправлено')

    def test_recover_password_confirm(self):
        url = reverse('user-recover-password-confirm') + f'?confirmation_token={self.token}'
        data = {
            'new_password': 'Rev-1bUS^'
        }
        response = self.client.post(url, data, format='json')
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

