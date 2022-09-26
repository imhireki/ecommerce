from django.db import models


PRICE_OPTIONS = {"max_digits": 6, "decimal_places": 2}


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    slug = models.SlugField(max_length=255, unique=True, blank=True)
    thumbnail = models.ImageField(upload_to='product/thumbnails/%Y/%m/',
                                  blank=True)

    marketing_price = models.DecimalField(**PRICE_OPTIONS)
    promotional_marketing_price = models.DecimalField(**PRICE_OPTIONS)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class ProductVariation(models.Model):
    name = models.CharField(max_length=100, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(**PRICE_OPTIONS, blank=True, null=True)
    promotional_price = models.DecimalField(**PRICE_OPTIONS,
                                            blank=True, null=True)

    class Meta:
        ordering = ['-product']


class ProductImage(models.Model):
    image = models.ImageField(upload_to='product/images/%Y/%m/')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-product']

