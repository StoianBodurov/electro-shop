from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item

UserModel = get_user_model()


class TestLastAddedItemsView(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': 'path/to.image.img'
    }
    def test_get_expect_correct_template(self):
        response = self.client.get(reverse('home page'))
        self.assertTemplateUsed(response, 'home page/home.html')

    def test_get_when_logged_in_user_expect_correct_template(self):
        user_data = {
            'email': 'test@abv.bg',
            'password': 'test'
        }
        UserModel.object.create_user(**user_data)
        self.client.login(**user_data)
        response = self.client.get(reverse('home page'))

        self.assertEqual(user_data['email'], response.context['user'].email)

    def test_get_when_one_item_expect_contain_one_item(self):

        Item.objects.create(**self.ITEM_DATA)
        response = self.client.get(reverse('home page'))
        items = response.context['object_list']
        self.assertEqual(len(items), 1)

    def test_get_when_more_than_twenty_expect_contain_twenty_item(self):

        for _ in range(25):
            Item.objects.create(**self.ITEM_DATA)
        response = self.client.get(reverse('home page'))
        items = response.context['object_list']
        self.assertEqual(len(items), 20)


