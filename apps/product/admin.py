from django.contrib import admin

from . import models


admin.site.register(models.Product)
admin.site.register(models.ProductImage)
admin.site.register(models.ProductVariation)

