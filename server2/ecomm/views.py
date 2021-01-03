from django.shortcuts import render
from .models import Category, User, Product, Review, Order, LineItem
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Case, When, Value, CharField, IntegerField, F
from .serializers import CategorySerializer, ProductSerializer, UserSerializer,\
    ReviewSerializer, OrderSerializer, LineItemSerializer

# Create your views here.


@api_view(['GET', 'POST'])
def category_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Category.objects.all()
        serializer = CategorySerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Product.objects.annotate(categoryId=Case(
            When(category__pk=pk, then=Value(pk)),
            # default=Value('categoryId'),
            output_field=IntegerField(),
        )).filter(category__pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(snippet, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def product_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Product.objects.annotate(categoryId=F('category')).all()
        serializer = ProductSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def review_product(request, format=None):
    if request.method == 'POST':
        print(request.data)
        title = request.data['title']
        content = request.data['content']
        rating = int(request.data['rating'])
        userId = int(request.data['userId'])
        productId = int(request.data['productId'])
        a = User.objects.filter(id=userId).first()
        b = Product.objects.filter(id=productId).first()
        Review.objects.create(title=title, content=content, rating=rating, user=a, product=b)
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Review.objects.annotate(productId=F('product')).annotate(userId=F('user')).filter(product__pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReviewSerializer(snippet, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ReviewSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)