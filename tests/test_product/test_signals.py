from django.db.models.signals import pre_save
from model_bakery import baker
import pytest

from apps.product.signals import PRODUCT_THUMBNAIL_SIZE
from apps.product.models import Product


pytestmark = [pytest.mark.django_db, pytest.mark.unit]


@pytest.mark.parametrize("slug", ["my-slug", ""])
def test_slug_pre_save_product(mocker, slug):
    slugify = mocker.patch("apps.product.signals.slugify")

    p = baker.prepare("product.Product", slug=slug)
    pre_save.send(Product, instance=p, created=True)

    if slug:
        slugify.assert_not_called()
    else:
        slugify.assert_called_with(p.name)


@pytest.mark.parametrize("saved_thumbnail", [True, False])
def test_thumbnail_pre_save_product(mocker, saved_thumbnail):
    mocker.patch("apps.product.signals.slugify")

    make_thumbnail = mocker.patch("apps.product.utils.make_thumbnail")

    original_image = mocker.Mock()
    original_image._committed = saved_thumbnail

    p = baker.prepare("product.Product", thumbnail=original_image)

    if saved_thumbnail:
        make_thumbnail.assert_not_called()
    else:
        # Creating
        pre_save.send(Product, instance=p, created=True)
        make_thumbnail.assert_called_with(original_image, PRODUCT_THUMBNAIL_SIZE)

        # Updating (wo updating thumbnail)
        # Last call should be when creating
        pre_save.send(Product, instance=p, created=False)
        make_thumbnail.assert_called_with(original_image, PRODUCT_THUMBNAIL_SIZE)
