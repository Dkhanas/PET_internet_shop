from django.urls import path
from . import views

urlpatterns = [
    path("", views.CategoryView.as_view(), name="category"),
    path("<str:category_slug>/items/", views.CatalogItemsView.as_view(), name="category_items"),
    path("<str:category_slug>/item/<str:product_slug>/", views.ProductItem.as_view(), name="product"),
    path("<str:category_slug>/", views.CategoryView.as_view(), name="sub_category"),
]
