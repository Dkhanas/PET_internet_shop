from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Catalog(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=19, decimal_places=10)

    def __str__(self):
        return self.name


class Characteristic(models.Model):
    name = models.CharField(max_length=70, unique=True)
    value = models.CharField(max_length=150)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=19, decimal_places=10)
    image = models.TextField()
    quantity = models.IntegerField()
    currency = models.ForeignKey(Currency, related_name='currency', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Products_Characteristics(models.Model):
    product_id = models.ForeignKey(Product, related_name='product_id', on_delete=models.CASCADE)
    characteristic_id = models.ForeignKey(Characteristic, related_name='characteristic_id', on_delete=models.CASCADE)

