from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item

UserModel = get_user_model()


class TestCreateItemView(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': SimpleUploadedFile(name='test_image.png',
                                    content=open('tests/media/panasonic-lumix-gh5-ii.png', 'rb').read(),
                                    content_type='image/png'),
        'in_stock': True,
    }

    USER_DATA = {
        'email': 'test@abv.bg',
        'password': 'test',
    }

    # def test_create_item_when_user_is_staff_expect_to_create_item(self):
    #     user_data = {
    #         'email': self.USER_DATA['email'],
    #         'password': self.USER_DATA['password'],
    #         'is_staff': True
    #     }
    #
    #     UserModel.object.create_user(**user_data)
    #     self.client.login(**user_data)
    #     response = self.client.post(reverse('create item'), data=self.ITEM_DATA)
    #     item = Item.objects.all()[0]
    #
    #     self.assertEqual(item.id, 1)
    #     self.assertEqual(item.brand, self.ITEM_DATA['brand'])
    #     self.assertEqual(item.categories, self.ITEM_DATA['categories'])
    #     self.assertEqual(item.description, self.ITEM_DATA['description'])
    #     self.assertEqual(float(item.price), self.ITEM_DATA['price'])
    #     self.assertEqual(item.in_stock, self.ITEM_DATA['in_stock'])
    #     self.assertEqual(response.status_code, 302)

    def test_create_item_when_user_not_is_staff_expect_forbidden(self):
        UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)

        response = self.client.post(reverse('create item'), data=self.ITEM_DATA)
        items = Item.objects.all()

        self.assertEqual(response.status_code, 403)
        self.assertEqual(len(items), 0)

    def test_create_item_when_not_user_expect_redirect(self):
        response = self.client.post(reverse('create item'), data=self.ITEM_DATA)
        items = Item.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(items), 0)
