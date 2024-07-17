from rest_framework import serializers

from .models import (
    Category,
    Tag,
    Brand,
    Product,
    Order,
    OrderItem,
    ShippingAddress,
)

from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['name']

class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['name']

class BrandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Brand
        fields = ['name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'uuid', 'name', 'image_a', 'image_b', 'image_c', 'image_d', 'description', 'price', 'discount_price', 'rating', 'num_of_reviews', 'count_in_stock', 'category', 'brand', 'tags', 'related_products'
        ]
        

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)

        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False

        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)

        return serializer.data