from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


from base.models import Product, Review
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
    
    