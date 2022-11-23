from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Item(models.Model):
    categories = models.CharField(
        choices=(
            ('laptops', 'Laptops'),
            ('smartphones', 'Smartphones'),
            ('cameras', 'Cameras'),
            ('accessories', 'Accessories')),
        default='Accessories',
        max_length=15
    )
    brand = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=6)
    image = models.ImageField(upload_to='items')
    in_stock = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    status = models.CharField(
        choices=(
            ('added', 'added'),
            ('confirmed', 'confirmed'),
            ('canceled', 'canceled')),
        default='added',
        max_length=15
    )
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
