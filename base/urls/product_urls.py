from django.urls import path
from base.views.product_views import (
    get_products,
    get_product_details,
)

urlpatterns = [
    path('', get_products, name='products'),
    path('<uuid:uuid>/', get_product_details, name='product-details'),
]