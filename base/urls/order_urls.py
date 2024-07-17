from django.urls import path
from base.views.order_views import (
    add_order_items,
    paypal_return,
    paypal_cancel
)

urlpatterns = [
    path('add/', add_order_items, name='add-order'),
    path('paypal-return/', paypal_return, name='paypal_return'),
    path('paypal-cancel/', paypal_cancel, name='paypal_cancel'),
]