from django.db import models

# Create your models here.

class Order(models.Model):
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)
    delivery_address = models.CharField(max_length=100)
    delivery_method = models.ForeignKey('DeliveryMethod', on_delete=models.PROTECT())
    payment_type = models.CharField(max_length=100)


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=30)
    availability = models.BooleanField()


class OrderItem(models.Model):
    order_id = models.ForeignKey('Order', on_delete=models.CASCADE)
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()