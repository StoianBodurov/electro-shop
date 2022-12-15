from django.test import TestCase
from django.urls import reverse


class TestRegisterUserView(TestCase):

    def test_user_register_successful(self):
        user_data = {'email': 'test_user@abv.bg', 'password1': 'test', 'password2': 'test'}
        response = self.client.post(reverse('user register'), data=user_data)

        self.assertEqual(response.status_code, 302)


