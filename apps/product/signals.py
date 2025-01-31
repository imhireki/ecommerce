from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from . import utils


PRODUCT_THUMBNAIL_SIZE = (640, 360)


@receiver(pre_save, sender="product.Product")
def pre_save_product(instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

    # Updating my product without updating my thumbnail
    if instance.thumbnail._committed:
        return
    # Adding/Updating thumbnail
    instance.thumbnail = utils.resize_image(instance.thumbnail, PRODUCT_THUMBNAIL_SIZE)
