from django.urls import path
from base.views.order_views import (
    add_order_items,
    paypal_return,
    paypal_cancel,
    get_orders,
    get_my_orders
)

urlpatterns = [
    path('', get_orders, name='get-order'),
    path('add/', add_order_items, name='add-order'),
    path('my_orders/', get_my_orders, name='get-my-order'),
    path('paypal_return/', paypal_return, name='paypal-return'),
    path('paypal_cancel/', paypal_cancel, name='paypal-cancel'),
]