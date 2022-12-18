from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item, Order

UserModel = get_user_model()

class TestOrderRemove(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': 'path/to.image.img',
    }

    USER_DATA = {
        'email': 'test@abv.bg',
        'password': 'test'
    }

    user = None
    def setUp(self):
        item = Item.objects.create(**self.ITEM_DATA)
        self.items_before_delete = Item.objects.all()
        self.user = UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)
        self.client.post(reverse('add order', kwargs={'pk': item.id}), data={'user': self.user, 'quantity': 1})


    def test_remove_order_remove_expect_remove_order(self):
        order_before_response= Order.objects.all()[0]

        self.client.post(reverse('order remove', kwargs={'pk': order_before_response.id}), data={'user': self.user})
        order_after_response = Order.objects.all()[0]
        self.assertEqual(order_after_response.status, 'canceled')