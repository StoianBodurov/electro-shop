from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

UserModel = get_user_model()


class TestLoginUserView(TestCase):
    USER_DATA = {'email': 'test_user@abv.bg', 'password': 'test'}

    def setUp(self):
        self.user = UserModel.object.create_user(**self.USER_DATA)

    def test_user_login_valid_data_expect_login_user(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(reverse_lazy('user profile', kwargs={'pk': self.user.id}))
        self.assertEqual(self.USER_DATA['email'], response.context['user'].email)
