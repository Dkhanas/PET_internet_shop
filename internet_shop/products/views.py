from django.shortcuts import render
from django.views import View
from .models import Catalog, Product
# Create your views here.


class CatalogView(View):
    def get(self, request, sub_category_name=''):
        category_obj = Catalog.objects.all()
        if sub_category_name:
            sub_category_name = sub_category_name.replace('-', ' ')
            sub_category_obj = ''
            for obj in category_obj:
                if obj.name == sub_category_name:
                    sub_category_obj = obj
                    break
            sub_category_objects = [obj for obj in category_obj if obj.parent == sub_category_obj]
            for category in sub_category_objects:
                temp_name =category.name.replace(' ', '-')
                category.url = temp_name + '/items'
            context = {"categories": sub_category_objects}
        else:
            has_parent = [category.parent for category in list(category_obj) if category.parent]
            parents = [category for category in list(category_obj) if not category.parent]
            for parent in parents:
                temp_name = parent.name.replace(' ', '-')
                if parent in has_parent:

                    parent.url = temp_name
                else:
                    parent.url = temp_name + '/items'
            context = {"categories": parents}
        return render(request, 'catalog/index.html', context=context)


class CatalogItemsView(View):
    def get(self, request, category_name):
        category_name = category_name.replace('-', ' ')
        catalog_obj = Catalog.objects.get(name=category_name)
        products = Product.objects.filter(category=catalog_obj)
        context = {"products": products}
        return render(request, 'product_list/index.html', context=context)


class ProductItem(View):
    def get(self, request, product_id):
        product = Product.objects.get(id=product_id)

        context = {'product': product}
        return render(request, 'product_item/index.html', context=context)
