# views.py

from datetime import datetime

from django.conf import settings
import paypalrestsdk
from paypalrestsdk import Payment

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import OrderSerializer

paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # sandbox or live
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_CLIENT_SECRET
})


@api_view('GET')
@permission_classes([IsAdminUser])
def get_orders(request):
    orders = Order.objects.all().order_by('-created_time')
    serializer = OrderSerializer(orders, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order_items(request):
    user = request.user
    data = request.data
    
    orderItems = data['orderItems']
    
    if not orderItems or len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 1. Create order
    order = Order.objects.create(
        user=user,
        payment_method=data['paymentMethod'],
        tax_price=data['taxPrice'],
        shipping_price=data['shippingPrice'],
        total_price=data['totalPrice'],
    )
    
    # 2. Create shipping address
    shipping = ShippingAddress.objects.create(
        order=order,
        state=data['shippingAddress']['state'],
        city=data['shippingAddress']['city'],
        address=data['shippingAddress']['address'],
        address_note=data['shippingAddress']['address_note'],
        latitude=data['shippingAddress']['latitude'],
        longitude=data['shippingAddress']['longitude']
    )
    
    # 3. Create order items and set order to orderItem relationship
    for item_data in orderItems:
        product = Product.objects.get(uuid=item_data['product'])

        item = OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=item_data['qty'],
            price=item_data['price'],
            image=product.image.url
        )

        # 4. Update stock
        product.count_in_stock -= item.qty
        product.save()
    
    # 5. Create PayPal payment if the payment method is PayPal
    if data['paymentMethod'] == 'PayPal':
        payment = Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://localhost:8000/api/orders/paypal_return",  # Update this with your return URL
                "cancel_url": "http://localhost:8000/api/orders/paypal-cancel"   # Update this with your cancel URL
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": "Order {}".format(order.uuid),
                        "sku": str(order.uuid),
                        "price": str(order.total_price),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(order.total_price),
                    "currency": "USD"
                },
                "description": "Payment for order {}".format(order.uuid)
            }]
        })

        if payment.create():
            for link in payment['links']:
                if link['rel'] == 'approval_url':
                    approval_url = str(link['href'])
                    serializer = OrderSerializer(order, many=False)
                    return Response({'order': serializer.data, 'approval_url': approval_url}, status=status.HTTP_201_CREATED)
        else:
            order.delete()  # Clean up the created order if PayPal payment fails
            return Response(payment.error, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paypal_return(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        order_uuid = payment.transactions[0].item_list.items[0].sku
        order = Order.objects.get(uuid=order_uuid)
        order.is_paid = True
        order.payment_time = datetime.now()
        order.paypal_payment_id = payment_id
        order.save()

        return Response({'status': 'Payment successful!', 'order_id': order.uuid}, status=status.HTTP_200_OK)
    else:
        return Response({'status': 'Payment failed!', 'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def paypal_cancel(request):
    return Response({'status': 'Payment cancelled!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    
    return Response(serializer.data)