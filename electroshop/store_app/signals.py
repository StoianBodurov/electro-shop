import os
from os.path import join

from django.conf import settings
from django.db import models
from django.dispatch import receiver

from electroshop.store_app.models import Item


@receiver(models.signals.post_delete, sender=Item)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Item` object is deleted.
    """
    if instance.image:

        image_path = join(settings.MEDIA_ROOT, str(instance.image))
        if os.path.isfile(image_path):
            os.remove(image_path)


@receiver(models.signals.pre_save, sender=Item)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Item` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Item.objects.get(pk=instance.pk).image
        old_file_path = join(settings.MEDIA_ROOT, str(old_file))
    except Item.DoesNotExist:
        return False

    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file_path):
            os.remove(old_file_path)
