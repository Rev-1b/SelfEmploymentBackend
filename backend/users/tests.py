from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import CustomUser


class UserRegistrationTestCase(APITestCase):
    def test_user_registration(self):
        url = reverse('user-register')

        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'qwerty2F'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = CustomUser.objects.get(email='test@example.com')
        self.assertFalse(user.is_active)

        # Добавьте здесь проверки отправки письма для активации почты

    def test_user_login(self):
        url = reverse('create_token')  # Замените 'token_obtain_pair' на фактический URL для получения JWT-токена

        data = {
            'email': 'test@example.com',
            'password': 'qwerty2F'
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

