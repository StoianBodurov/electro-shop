from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item, Order

UserModel = get_user_model()


class TestAddItemToOrderView(TestCase):
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

    def setUp(self):
        Item.objects.create(**self.ITEM_DATA)

    def test_add_item_to_order_when_not_logged_in_user_expect_redirect(self):
        item = Item.objects.all()[0]
        response = self.client.post(reverse('add order', kwargs={'pk': item.id}), data={'quantity': 1})
        orders = Order.objects.all()
        self.assertEqual(len(orders), 0)
        self.assertEqual(response.status_code, 302)

    def test_add_item_to_order_when_logged_in_user_expect_add_to_order(self):
        order_quantity = 3
        user = UserModel.object.create_user(**self.USER_DATA)
        self.client.login(**self.USER_DATA)
        item = Item.objects.all()[0]

        self.client.post(reverse('add order', kwargs={'pk': item.id}), data={'user': user, 'quantity': order_quantity})

        order = Order.objects.all()[0]
        self.assertEqual(user.id, order.user.id)
        self.assertEqual(order.quantity, order_quantity)
        self.assertEqual(order.status, 'added')
