from django.db import models
import uuid
from mptt.models import MPTTModel, TreeForeignKey


class Base(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        if hasattr(self, 'name'):
            return self.name


class Catalog(MPTTModel, Base):
    name = models.CharField(max_length=50)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']


class Currency(Base):
    name = models.CharField(max_length=50, unique=True)
    exchange_rate = models.DecimalField(max_digits=9, decimal_places=2)


class Characteristic(Base):
    name = models.CharField(max_length=70, unique=True)
    value = models.CharField(max_length=150)


class Product(Base):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.TextField()
    quantity = models.IntegerField()


class Product_Characteristic(Base):
    product_id = models.ForeignKey(Product, related_name='product_characteristics', on_delete=models.CASCADE)
    characteristic_id = models.ForeignKey(Characteristic, related_name='product_characteristics', on_delete=models.CASCADE)
