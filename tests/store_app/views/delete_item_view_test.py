from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item

UserModel = get_user_model()

class TestDeleteItemView(TestCase):
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

    items_before_delete = None

    def setUp(self):
        Item.objects.create(**self.ITEM_DATA)
        self.items_before_delete = Item.objects.all()


    def test_delete_item_when_user_is_staff_expect_to_edit_item(self):
        user_data = {
            'email': self.USER_DATA['email'],
            'password': self.USER_DATA['password'],
            'is_staff': True
        }

        UserModel.object.create_user(**user_data)
        self.client.login(**user_data)

        item = Item.objects.all()[0]
        response = self.client.post(reverse('delete item', kwargs={'pk': item.id}))
        items_after_delete = Item.objects.all()

        self.assertEqual(len(items_after_delete), 0)
        self.assertEqual(response.status_code, 302)




    def test_delete_item_when_user_not_staff_expect_forbidden(self):
        UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)

        # items_before_delete = Item.objects.all()
        item = Item.objects.all()[0]
        response = self.client.post(reverse('delete item', kwargs={'pk': item.id}))
        items_after_delete = Item.objects.all()

        self.assertEqual(len(items_after_delete), len(self.items_before_delete))
        self.assertEqual(response.status_code, 403)

    def test_delete_item_when_not_user_expect_redirect(self):

        item = Item.objects.all()[0]
        response = self.client.post(reverse('delete item', kwargs={'pk': item.id}))
        items_after_delete = Item.objects.all()

        self.assertEqual(len(items_after_delete), len(self.items_before_delete))
        self.assertEqual(response.status_code, 302)

