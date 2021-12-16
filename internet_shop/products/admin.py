from django.contrib import admin
from .models import Currency, Characteristic, Image, Category, Product, ProductImage, ProductCharacteristic

# Register your models here.
admin.site.register(Currency)
admin.site.register(Characteristic)
admin.site.register(Image)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ProductCharacteristic)
