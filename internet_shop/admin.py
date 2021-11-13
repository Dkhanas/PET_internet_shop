from django.contrib import admin

# Register your models here.

from .models import Order, DeliveryMethod, OrderItem

admin.site.register(Order)
admin.site.register(DeliveryMethod)
admin.site.register(OrderItem)