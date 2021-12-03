from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path("<str:category_name>/items/", views.CatalogItemsView.as_view(), name="category_items"),
    url(
        r"",
        include(
            [
                url(r"^$", views.CatalogView.as_view(), name="product"),
                url(
                    r"^(?!item/)(?P<sub_category_name>\S+)(?<!/items)$",
                    views.CatalogView.as_view(),
                    name="project_detail",
                ),
            ]
        ),
    ),
    path("item/<uuid:product_id>/", views.ProductItem.as_view(), name="item"),
]
