from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from electroshop.common.models import Review
from electroshop.store_app.models import Item

UserModel = get_user_model()


class TestItemReviewView(TestCase):
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

    REVIEW_DATA = {
        'review': 'test_review',
        'rating': 3
    }
    user = None
    item = None
    def setUp(self):
        self.item = Item.objects.create(**self.ITEM_DATA)
        self.user = UserModel.object.create_user(**self.USER_DATA)


    def test_review_when_not_logged_in_user_expect_not_add_review_and_redirect(self):
        response = self.client.post(reverse('review item', kwargs={'pk': self.item.id}), data=self.REVIEW_DATA)
        item_reviews = Review.objects.filter(item_id=self.item.id)

        self.assertEqual(len(item_reviews), 0)
        self.assertEqual(response.status_code, 302)

    def test_review_when_logged_in_user_expect_add_review(self):
        self.client.login(**self.USER_DATA)
        self.client.post(reverse('review item', kwargs={'pk': self.item.id}), data=self.REVIEW_DATA)
        item_review = Review.objects.filter(item_id=self.item.id).get()

        self.assertIsNotNone(item_review)
        self.assertEqual(item_review.review, self.REVIEW_DATA['review'])
        self.assertEqual(item_review.rating, self.REVIEW_DATA['rating'])
        self.assertEqual(item_review.user_id, self.user.id)

    def test_review_when_logged_in_user_and_already_add_review_expect_change_review_data(self):
        review_data = {
            'review': self.REVIEW_DATA['review'],
            'rating': self.REVIEW_DATA['rating'],
            'user': self.user,
            'item': self.item
        }

        new_review_data = {
            'review': 'new_review',
            'rating': self.REVIEW_DATA['rating'] + 1
        }

        review = Review.objects.create(**review_data)
        self.client.login(**self.USER_DATA)
        res = self.client.post(reverse('review item', kwargs={'pk': self.item.id}), data=new_review_data)

        new_review = Review.objects.filter(item_id=self.item.id).get()
        self.assertEquals(review, new_review)
