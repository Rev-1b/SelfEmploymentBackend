from django.urls import reverse
from rest_framework.test import APITestCase, APIClient

from documents.models import UserTemplate
from documents.tests.common import CRUDLTestMixin
from users.models import CustomUser


class UserTemplateViewSetTests(APITestCase, CRUDLTestMixin):

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)
        self.template = UserTemplate.objects.create(
            user=self.user,
            title="Template title",
            template_type=UserTemplate.TemplateTypeChoices.AGREEMENT,
            content="Template content"
        )

        self.template_list_url = reverse('templates-list')
        self.template_detail_url = reverse('templates-detail', args=[self.template.id])

    def test_get_user_template_list(self):
        self.check_list(self, self.template_list_url, 1)

    def test_template_type_filtered_list(self):
        self.check_list(self, self.template_list_url + f'?template_type={UserTemplate.TemplateTypeChoices.AGREEMENT}',
                        1)

    def test_invalid_template_type_filtered_list(self):
        self.check_bad_filtered_list(self, self.template_list_url + '?template_type=IdaE')

    def test_create_user_template(self):
        data = {
            "user": self.user.id,
            "title": "New template title",
            "template_type": UserTemplate.TemplateTypeChoices.ADDITIONAL,
            "content": "New template content"
        }
        self.check_create(self, self.template_list_url, data, UserTemplate, 2)

    def test_update_user_template(self):
        data = {
            "title": "Updated template title"
        }
        self.check_update(self, self.template_detail_url, data, self.template)

    def test_delete_user_template(self):
        self.check_delete(self, self.template_detail_url, UserTemplate, 0)
