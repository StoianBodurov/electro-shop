from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item, Order

UserModel = get_user_model()

class TestOrdersListView(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': 'path/to.image.img',
    }
    USER_DATA = {'email': 'test_user@abv.bg', 'password': 'test'}
    ORDER_COUNT = 10

    def setUp(self):
        item = Item.objects.create(**self.ITEM_DATA)
        user = UserModel.object.create_user(**self.USER_DATA)

        for _ in range(self.ORDER_COUNT):
            order_data = {
                'item': item,
                'user': user,
                'quantity': 1
            }

            Order.objects.create(**order_data)


    def test_order_list_same_user_logged_in_expect_order_count_exact_like_ORDER_COUNT(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(reverse('orders list'))

        self.assertEqual(len(response.context_data['orders']), self.ORDER_COUNT)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(float(response.context_data['total_price']), round((self.ITEM_DATA['price'] * self.ORDER_COUNT), 2))

    def test_order_list_another_user_logged_in_expect_order_count_exact_like_0(self):
        user_data = {
            'email': self.USER_DATA['email'] + str(1),
            'password': self.USER_DATA['password'] + str(1)
        }

        UserModel.object.create_user(**user_data)
        self.client.login(**user_data)
        response = self.client.get(reverse('orders list'))

        self.assertEqual(len(response.context_data['orders']), 0)
        self.assertEqual(response.status_code, 200)

    def test_order_list_not_user_logged_in_expect_redirect(self):
        response = self.client.get(reverse('orders list'))

        self.assertEqual(response.status_code, 302)



