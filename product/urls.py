from django.urls import path
from .views import (
    ListviewProduct,
    ProductCreate,
    ProductUpdate,
    ProductDelete,
    )

urlpatterns = [
    path(
        'product/information/',
        ListviewProduct.as_view(),
        name="product_list"
    ),

    path(
        'product/create-new-product/',
        ProductCreate.as_view(),
        name="product_create"
    ),

    path(
        'product/update-product/<int:pk>/',
        ProductUpdate.as_view(),
        name="product_update"
    ),

    path(
        'product/delete-product/<int:pk>/',
        ProductDelete.as_view(),
        name="product_delete"
    ),
]
