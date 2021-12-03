from django.db import models
from utils.constants import NAME_CHARFIELD_LENGTH, CODE_CHARFIELD_LENGTH, HUGE_CHARFIELD_LENGTH, \
    PRICE_DECIMALFIELD_DIGITS_LENGTH, PRICE_DECIMALFIELD_DECIMAL_LENGTH
from mptt.models import MPTTModel, TreeForeignKey

from utils.base_models import BaseModel


class Currency(BaseModel):
    name = models.CharField(max_length=NAME_CHARFIELD_LENGTH, unique=True)
    exchange_rate = models.DecimalField(max_digits=PRICE_DECIMALFIELD_DIGITS_LENGTH,
                                        decimal_places=PRICE_DECIMALFIELD_DECIMAL_LENGTH)

    class Meta:
        verbose_name_plural = "Currencies"


class Characteristic(BaseModel):
    name = models.CharField(max_length=NAME_CHARFIELD_LENGTH, unique=True)
    value = models.CharField(max_length=HUGE_CHARFIELD_LENGTH)


class Image(BaseModel):
    image_url = models.TextField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # TODO: add s3 bucket support
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.image_url


class Catalog(MPTTModel, BaseModel):
    name = models.CharField(max_length=NAME_CHARFIELD_LENGTH)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    image = models.ForeignKey(Image, related_name='catalog', on_delete=models.SET_NULL, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']


class Product(BaseModel):
    name = models.CharField(max_length=NAME_CHARFIELD_LENGTH)
    code = models.CharField(max_length=CODE_CHARFIELD_LENGTH)
    description = models.CharField(max_length=HUGE_CHARFIELD_LENGTH)
    price = models.DecimalField(max_digits=PRICE_DECIMALFIELD_DIGITS_LENGTH,
                                decimal_places=PRICE_DECIMALFIELD_DECIMAL_LENGTH)
    old_price = models.DecimalField(max_digits=PRICE_DECIMALFIELD_DIGITS_LENGTH,
                                    decimal_places=PRICE_DECIMALFIELD_DECIMAL_LENGTH)
    quantity = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Catalog, related_name='products', on_delete=models.SET_NULL, null=True)


class ProductImage(BaseModel):
    image = models.ForeignKey(Image, related_name='product_images', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE)


class ProductCharacteristic(BaseModel):
    product = models.ForeignKey(Product, related_name='product_characteristics', on_delete=models.CASCADE)
    characteristic = models.ForeignKey(Characteristic, related_name='product_characteristics',
                                       on_delete=models.CASCADE)
