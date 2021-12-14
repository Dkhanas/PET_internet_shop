from django.shortcuts import render, redirect
from django.views import View
from .models import Category, Product
from .forms import OrderItems


class CategoryView(View):
    def get(self, request, category_name=""):
        if category_name:
            category_obj = Category.objects.filter(slug=category_name)
            children_objects = category_obj[0].get_children()
            if not children_objects:
                return redirect("category_items", category_name=category_name)
            context = {"categories": children_objects, "is_children": True}
        else:
            category_objects = Category.objects.filter(parent=None)
            context = {"categories": category_objects}
        return render(request, "catalog/index.html", context=context)


class CatalogItemsView(View):
    def get(self, request, category_name):
        catalog_obj = Category.objects.get(slug=category_name)
        products = Product.objects.filter(category=catalog_obj).order_by("created_at")
        form = OrderItems(request.GET)
        if form.is_valid():
            products = products.order_by(form.cleaned_data["order_type"])
        else:
            form = OrderItems()
        context = {"products": products, "category_name": category_name, "form": form}
        return render(request, "product_list/index.html", context=context)


class ProductItem(View):
    def get(self, request, category_name, product_name):
        product = Product.objects.get(slug=product_name)
        context = {"product": product}
        return render(request, "product_item/index.html", context=context)
