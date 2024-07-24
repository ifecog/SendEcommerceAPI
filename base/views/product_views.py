from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from base.models import Product, Review, Category, Brand, Tag
from base.serializers import ProductSerializer
# Create your views here.

@api_view(['GET'])
def get_products(request):
    query = request.query_params.get('keyword')
    if not query:
        query = ''
    
    products = Product.objects.filter(name__icontains=query).order_by('-created_time')
    
    page = request.query_params.get('page')
    paginator = Paginator(products, 8)
    
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = Paginator.page(paginator.num_pages)
        
    if not page:
        page = 1
        
    page = int(page)
    
    serializer = ProductSerializer(products, many=True)
    
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})


@api_view(['GET'])
def get_product_details(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_product_review(request, uuid):
    user = request.user
    product = get_object_or_404(Product, uuid=uuid)
    data = request.data
    
    # 1. Review already exist bu user
    already_exists = product.review_set.filter(user=user).exists()
    if already_exists:
        return Response({'detail': 'Product already reviewed by user!'}, status=status.HTTP_403_FORBIDDEN)
    
    # 2. No rating or 0 rating
    elif data['rating'] == 0:
        return Response({'detail': 'Kindly select a rating'}, status=status.HTTP_400_BAD_REQUEST)
    
    # 3. Create review
    else:
        review = Review.objects.create(
            user=user,
            product=product,
            name=user.first_name,
            rating=data['rating'],
            comment=data['comment']
        )
        
        reviews = product.review_set.all()
        product.num_of_reviews = len(reviews)
        
        total = 0
        for i in reviews:
            total += i.rating
            
        product.rating = total / len(reviews)
        product.save()
        
        return Response('Review added!')
    
    
@api_view(['POST'])
def upload_image(request):
    data = request.data
    
    product_id = data['product_id']
    product = Product.objects.get(uuid=product_id)
    
    if 'image_a' in request.FILES:
        product.image_a = request.FILES.get('image_a')
    if 'image_b' in request.FILES:
        product.image_b = request.FILES.get('image_b')
    if 'image_c' in request.FILES:
        product.image_c = request.FILES.get('image_c')
    if 'image_d' in request.FILES:
        product.image_d = request.FILES.get('image_d')
    
    product.save()
    
    return Response('Images were successfully uploaded!')


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_product(request):
    user = request.user
    data = request.data

    # Fetch related fields
    category = get_object_or_404(Category, uuid=data['category']) if 'category' in data else None
    brand = get_object_or_404(Brand, uuid=data['brand']) if 'brand' in data else None

    product = Product.objects.create(
        user=user,
        name=data.get('name', 'Sample Name'),
        price=data.get('price', 0),
        count_in_stock=data.get('count_in_stock', 0),
        description=data.get('description', ''),
        category=category,
        brand=brand,
    )

    # Handle Many-to-Many relationship for tags
    if 'tags' in data:
        tags = data['tags']
        for tag_uuid in tags:
            tag = get_object_or_404(Tag, uuid=tag_uuid)
            product.tags.add(tag)

    serializer = ProductSerializer(product, many=False)
    
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def update_product(request, uuid):
    try:
        product = Product.objects.get(uuid=uuid)
    except Product.DoesNotExist:
        return Response({'detail': 'Product not found'}, status=404)

    data = request.data

    # Update fields
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.discount_price = data.get('discount_price', product.discount_price)
    product.count_in_stock = data.get('count_in_stock', product.count_in_stock)
    product.rating = data.get('rating', product.rating)
    product.num_of_reviews = data.get('num_of_reviews', product.num_of_reviews)

    # Foreign key fields
    if 'category' in data:
        try:
            category = Category.objects.get(name=data['category'])
            product.category = category
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found'}, status=400)

    if 'brand' in data:
        try:
            brand = Brand.objects.get(name=data['brand'])
            product.brand = brand
        except Brand.DoesNotExist:
            return Response({'detail': 'Brand not found'}, status=400)

    # Many-to-many field
    if 'tags' in data:
        try:
            tags = Tag.objects.filter(name__in=[tag.strip() for tag in data['tags']])
            product.tags.set(tags)
        except Tag.DoesNotExist:
            return Response({'detail': 'Some tags not found'}, status=400)

    product.save()

    serializer = ProductSerializer(product)
    return Response(serializer.data)
    

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_product(request, uuid):
    product = get_object_or_404(Product, uuid=uuid)
    product.delete()
    
    return Response('Product was successfully deleted')