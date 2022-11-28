from django.contrib.auth import get_user_model
from django.db import models

from electroshop.store_app.models import Item

UserModel = get_user_model()


class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField(default=0, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
