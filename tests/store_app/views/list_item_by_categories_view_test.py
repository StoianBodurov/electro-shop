from django.test import TestCase
from django.urls import reverse

from electroshop.store_app.models import Item
from electroshop.store_app.views import ListItemByCategoriesView


class TestListItemByCategoriesView(TestCase):
    ITEM_DATA = {
        'categories': 'laptops',
        'brand': 'brand',
        'model': 'model',
        'description': 'description',
        'price': 12.56,
        'image': 'path/to.image.img'
    }

    def test_get_expect_correct_template_and_context(self):

        response1 = self.client.get(reverse('store page', kwargs={'categories':'laptops'}))
        response2 = self.client.get(reverse('store page', kwargs={'categories':'all'}))
        response3 = self.client.get(reverse('store page', kwargs={'categories':'smartphones'}))
        response4 = self.client.get(reverse('store page', kwargs={'categories':'cameras'}))
        response5 = self.client.get(reverse('store page', kwargs={'categories':'accessories'}))

        self.assertTemplateUsed(response1, 'store/store.html')
        self.assertEqual(response1.context['categories_name'], 'laptops')

        self.assertTemplateUsed(response2, 'store/store.html')
        self.assertEqual(response2.context['categories_name'], 'all')

        self.assertTemplateUsed(response3, 'store/store.html')
        self.assertEqual(response3.context['categories_name'], 'smartphones')

        self.assertTemplateUsed(response4, 'store/store.html')
        self.assertEqual(response4.context['categories_name'], 'cameras')

        self.assertTemplateUsed(response5, 'store/store.html')
        self.assertEqual(response5.context['categories_name'], 'accessories')

    def test_get_expect_correct_count_off_items_by_categories(self):
        laptop_item_count = 0
        cameras_item_count = 0

        for _ in range(10):
            Item.objects.create(**self.ITEM_DATA)
            laptop_item_count += 1

        for _ in range(10):
            self.ITEM_DATA['categories'] = 'cameras'
            Item.objects.create(**self.ITEM_DATA)
            cameras_item_count += 1

        response_all = self.client.get(reverse('store page', kwargs={'categories':'all'}))
        response_laptops = self.client.get(reverse('store page', kwargs={'categories':'laptops'}))
        response_cameras = self.client.get(reverse('store page', kwargs={'categories':'cameras'}))

        self.assertEqual(response_all.context['paginator'].count, laptop_item_count + cameras_item_count)
        self.assertEqual(len(response_all.context['object_list']), ListItemByCategoriesView.paginate_by)

        self.assertEqual(response_laptops.context['paginator'].count, laptop_item_count)
        self.assertEqual(len(response_laptops.context['object_list']), ListItemByCategoriesView.paginate_by)

        self.assertEqual(response_cameras.context['paginator'].count, cameras_item_count)
        self.assertEqual(len(response_cameras.context['object_list']), ListItemByCategoriesView.paginate_by)

