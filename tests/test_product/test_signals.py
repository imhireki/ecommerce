from django.db.models.signals import pre_save
from model_bakery import baker
import pytest

from apps.product.models import Product


@pytest.mark.django_db
@pytest.mark.unit
def test_pre_save_product(mocker):
    resize_image = mocker.patch("apps.product.utils.resize_image")
    slugify = mocker.patch("apps.product.signals.slugify")
    product = baker.prepare("product.Product")

    pre_save.send(Product, instance=product, created=True)

    resize_image.assert_called()
    slugify.assert_called()
