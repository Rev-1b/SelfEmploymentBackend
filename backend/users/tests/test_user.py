from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.cryptography import encrypt_data
from users.models import CustomUser, Passport
import users.tests.data as test_data


class UserRegistrationTestCase(APITestCase):
    def setUp(self):
        super(UserRegistrationTestCase, self).setUp()
        self.user = CustomUser.objects.create_user(**test_data.main_user)
        self.passport = Passport.objects.create(user=self.user, **test_data.main_passport)
        self.token = encrypt_data(self.user.pk)

    def test_create_user(self):
        url = reverse('user-register')
        response = self.client.post(url, test_data.new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], test_data.new_user['username'])
        self.assertEqual(response.data['email'], test_data.new_user['email'])
        self.assertTrue(CustomUser.objects.filter(email=test_data.new_user.get('email')).exists())

    def test_user_login(self):
        url = reverse('create-token')
        response = self.client.post(url, test_data.main_user_auth, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_refresh_token(self):
        first_url = reverse('create-token')
        second_url = reverse('refresh-token')
        first_response = self.client.post(first_url, test_data.main_user_auth, format='json')
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
        self.client.login(**test_data.main_user_auth)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Temporally commented. Cant figure out, why user email does not change in tests, but in Postman
        user = CustomUser.objects.get(email=new_email)
        self.assertEqual(user.email, new_email)

    def test_change_password(self):
        url = reverse('user-change-password')
        new_password = 'Rev-1bUS^'
        data = {
            'old_password': test_data.main_user_auth.get('password'),
            'new_password': new_password
        }

        # change password
        self.client.login(**test_data.main_user_auth)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if password is changed (trying to log in with a new password)
        login_url = reverse('create-token')
        data = {
            'email': test_data.main_user.get('email'),
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

    def test_user_details(self):
        url = reverse('user-me')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'middle_name': 'Smith',
            'passport': test_data.main_passport
        }
        self.client.login(**test_data.main_user_auth)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_url = reverse('user-me')
        new_response = self.client.get(new_url, format='json')
        passport_data = new_response.data.pop('passport')

        self.assertEqual(new_response.data.get('first_name'), 'John')
        self.assertEqual(new_response.data.get('last_name'), 'Doe')
        self.assertEqual(new_response.data.get('middle_name'), 'Smith')

        self.assertEqual(passport_data.get('series'), '1234')
        self.assertEqual(passport_data.get('number'), '56789')
        self.assertEqual(passport_data.get('release_date'), '2022-01-01')
        self.assertEqual(passport_data.get('unit_code'), 'ABC123')

    def test_update_user_details(self):
        url = reverse('user-me')
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
        }
        self.assertEqual(self.user.first_name, '')
        self.assertEqual(self.user.last_name, '')

        self.client.login(**test_data.main_user_auth)
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data.get('first_name'), 'John')
        self.assertEqual(response.data.get('last_name'), 'Doe')


