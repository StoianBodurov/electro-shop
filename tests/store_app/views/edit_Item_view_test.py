from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item

UserModel = get_user_model()


class TestEditItemView(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': 'path/to.image.img'
    }

    USER_DATA = {
        'email': 'test@abv.bg',
        'password': 'test'
    }

    def setUp(self):
        Item.objects.create(**self.ITEM_DATA)

    def test_edit_item_when_user_is_staff_expect_to_edit_item(self):
        new_categories = 'cameras'
        new_brand = 'new_brand'

        new_item = {
            'categories': new_categories,
            'brand': new_brand,
            'model': 'model',
            'description': 'description',
            'price': 12.56,
            'image': 'path/to.image.img'
        }

        user_data = {
            'email': self.USER_DATA['email'],
            'password': self.USER_DATA['password'],
            'is_staff': True
        }
        UserModel.object.create_user(**user_data)
        self.client.login(**user_data)
        old_item = Item.objects.all()[0]
        response = self.client.post(reverse('edit item', kwargs={'pk': old_item.id}), data=new_item)
        edited_item = Item.objects.all()[0]

        self.assertEqual(edited_item.brand, new_brand)
        self.assertEqual(edited_item.categories, new_categories)

    def test_edit_item_when_user_not_staff_expect_forbidden(self):
        UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)
        Item.objects.create(**self.ITEM_DATA)

        item = Item.objects.all()[0]

        response = self.client.post(reverse('edit item', kwargs={'pk': item.id}), data=self.ITEM_DATA)

        self.assertEqual(response.status_code, 403)

    def test_edit_item_when_not_user_expect_redirect(self):
        new_categories = 'cameras'
        new_brand = 'new_brand'
        Item.objects.create(**self.ITEM_DATA)

        new_item = {
            'categories': new_categories,
            'brand': new_brand,
            'model': 'model',
            'description': 'description',
            'price': 12.56,
            'image': 'path/to.image.img'
        }

        item = Item.objects.all()[0]
        response = self.client.post(reverse('edit item', kwargs={'pk': item.id}), data=new_item)
        edited_items = Item.objects.all()[0]

        self.assertEqual(response.status_code, 302)
        self.assertEqual(item.categories, edited_items.categories)
        self.assertEqual(item.brand, edited_items.brand)
