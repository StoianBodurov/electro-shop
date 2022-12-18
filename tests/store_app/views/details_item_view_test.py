from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.test import TestCase
from django.urls import reverse

from electroshop.common.models import Review
from electroshop.store_app.models import Item

UserModel = get_user_model()

class TestDetailsItemView(TestCase):
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
        item = Item.objects.create(**self.ITEM_DATA)

        for i in range(1, 11):
            user_data = {
                'email': self.USER_DATA['email'] + str(i),
                'password': self.USER_DATA['password'] + str(i)
            }
            user = UserModel.object.create_user(**user_data)

            Review.objects.create(**{
                'review': f'test{i}',
                'rating': 3,
                'item': item,
                'user': user
            })

    def test_details_get_expect_correct_data(self):
        item = Item.objects.filter(**self.ITEM_DATA).get()
        item_reviews = Review.objects.filter(item_id=item.id)
        avg_rating =  round(item_reviews.aggregate(Avg('rating'))['rating__avg'], 1)

        response = self.client.get(reverse('details item', kwargs={'pk': item.id}))
        response_item = response.context_data['item']
        response_reviews = response.context_data['reviews']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['average_rating'], avg_rating)
        self.assertEquals(item, response_item)
        self.assertEqual(len(item_reviews), len(response_reviews))


