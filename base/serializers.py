from rest_framework import serializers

from .models import (
    Category,
    Tag,
    Brand,
    Product
)


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