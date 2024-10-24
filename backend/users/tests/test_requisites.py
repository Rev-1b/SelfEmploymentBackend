from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser, UserRequisites
from users.tests.data import main_user


class UserRequisitesTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(**main_user)
        self.client.force_authenticate(user=self.user)
        self.requisites_data = {
            'bank_name': 'Test Bank',
            'bic': 'TESTBIC',
            'bank_account': '1234567890',
            'user_account': 'testuser',
            'card_number': '1234-5678-9012-3456'
        }

    def test_create_user_requisites(self):
        url = reverse('requisites-list')
        response = self.client.post(url, data=self.requisites_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(UserRequisites.objects.filter(user=self.user).exists())

    def test_list_user_requisites(self):
        UserRequisites.objects.create(user=self.user, **self.requisites_data)
        url = reverse('requisites-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get('results')), 1)
        self.assertEqual(response.data.get('results')[0]['bank_name'], 'Test Bank')

    def test_update_user_requisites(self):
        requisites = UserRequisites.objects.create(user=self.user, **self.requisites_data)
        updated_data = {
            'bank_name': 'Updated Bank',
            'bic': 'UPDATEDBIC'
        }
        url = reverse('requisites-detail', kwargs={'pk': requisites.pk})
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        requisites.refresh_from_db()
        self.assertEqual(requisites.bank_name, 'Updated Bank')
        self.assertEqual(requisites.bic, 'UPDATEDBIC')

    def test_delete_user_requisites(self):
        requisites = UserRequisites.objects.create(user=self.user, **self.requisites_data)
        url = reverse('requisites-detail', kwargs={'pk': requisites.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(UserRequisites.objects.filter(id=requisites.id).exists())
