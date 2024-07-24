from django.urls import path
from base.views.product_views import (
    get_products,
    get_product_details,
    create_product_review,
    upload_image,
    create_product,
    update_product,
    delete_product
)

urlpatterns = [
    path('', get_products, name='products'),
    path('create/', create_product, name='create-product'),
    path('<uuid:uuid>/', get_product_details, name='product-details'),
    path('<uuid:uuid>/reviews/', create_product_review, name='product-reviews'),
    path('image-upload/', upload_image, name='image-upload'),
    path('update/<uuid:uuid>/', update_product, name='update-product'),
    path('delete/<uuid:uuid>/', delete_product, name='delete-product'),
]