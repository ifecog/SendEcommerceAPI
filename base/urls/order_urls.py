from django.urls import path
from base.views.order_views import (
    add_order_items,
    paypal_return,
    paypal_cancel,
    get_orders,
    get_my_orders,
    get_order_by_id,
    update_order_to_delivered,
    create_paypal_payment,
)

urlpatterns = [
    path('', get_orders, name='get-order'),
    path('add/', add_order_items, name='add-order'),
    path('paypal/<uuid:uuid>/', create_paypal_payment, name='paypal-payment'),
    path('<uuid:uuid>/', get_order_by_id, name='user-order'),
    path('my_orders/', get_my_orders, name='get-my-order'),
    path('paypal_return/', paypal_return, name='paypal-return'),
    path('paypal_cancel/', paypal_cancel, name='paypal-cancel'),
    path('<uuid:uuid>/deliver/', update_order_to_delivered, name='update-delivery'),
]