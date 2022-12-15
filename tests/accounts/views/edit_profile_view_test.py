from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, reverse_lazy

from electroshop.accounts.models import Profile

UserModel = get_user_model()

class TestUpdateUserProfileView(TestCase):
    PROFILE_DATA = {
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'address': 'test_address',
        'city': 'test_city',
        'zip_code': 'test_zip_code',
        'telephone': '008888444',
        'country': 'test_country'
    }
    USER_DATA = {'email': 'test_user@abv.bg', 'password': 'test'}
    def setUp(self):
        self.user = UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)

    def test_create_profile_when_user_is_logged_in_expect_to_create_profile(self):
        response = self.client.post(reverse('user profile', kwargs={'pk': self.user.id}), data=self.PROFILE_DATA)
        created_profile = Profile.objects.filter(**self.PROFILE_DATA)[0]
        self.assertIsNotNone(created_profile)
        self.assertEqual(response.status_code, 302)

