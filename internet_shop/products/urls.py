from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryView.as_view(), name="category"),
    path("<str:category_name>/items/", views.CatalogItemsView.as_view(), name="category_items"),
    path("<str:category_name>/item/<str:product_name>/", views.ProductItem.as_view(), name="product"),
    path("<str:category_name>/", views.CategoryView.as_view(), name="sub_category"),
]
