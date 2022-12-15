from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

UserModel = get_user_model()

class TestLogoutUserView(TestCase):
    USER_DATA = {'email': 'test_user@abv.bg', 'password': 'test'}

    def setUp(self):
        self.user = UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)

    def test_user_logout_expect_logout_user(self):
        response = self.client.post(reverse_lazy('user logout'))
        self.assertEqual(response.status_code, 302)
