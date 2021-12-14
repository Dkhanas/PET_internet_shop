from django.shortcuts import render, redirect
from django.http import Http404
from django.views import View
from .models import Category, Product
from .forms import OrderItems


class CategoryView(View):
    def get(self, request, category_slug=""):
        if category_slug:
            category_obj = Category.objects.filter(slug=category_slug).first()
            if not category_obj:
                return Http404("Category does not exist")
            children_objects = category_obj.get_children()
            if not children_objects:
                return redirect("category_items", category_slug=category_slug)
            context = {"categories": children_objects, "is_children": True}
        else:
            category_objects = Category.objects.root_nodes()
            context = {"categories": category_objects}
        return render(request, "catalog/index.html", context=context)


class CatalogItemsView(View):
    def get(self, request, category_slug):
        catalog_obj = Category.objects.get(slug=category_slug)
        if not catalog_obj:
            return Http404("Category does not exist")
        products = Product.objects.filter(category=catalog_obj)
        form = OrderItems(request.GET)
        if form.is_valid():
            products = products.order_by(form.cleaned_data["order_type"])
        else:
            form = OrderItems()
        context = {"products": products, "category_slug": category_slug, "form": form}
        return render(request, "product_list/index.html", context=context)


class ProductItem(View):
    def get(self, request, category_slug, product_slug):
        product = Product.objects.get(slug=product_slug)
        if not product:
            return Http404("Product does not exist")
        context = {"product": product}
        return render(request, "product_item/index.html", context=context)
