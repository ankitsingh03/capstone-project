from django.shortcuts import render
from .models import Category, User, Product, Review, Order, LineItem
from django.contrib.auth import login, authenticate, logout
from .forms import UserForm
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Case, When, Value, CharField, IntegerField, F
from .serializers import CategorySerializer, ProductSerializer, UserSerializer,\
    ReviewSerializer, OrderSerializer, LineItemSerializer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.views.decorators.http import require_POST
from django.middleware.csrf import get_token
import json
import ast
import razorpay
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


@api_view(['GET', 'PUT', 'DELETE'])
def cart_detail(request, pks, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        abc = pks
        arrayOfpk = abc.split(",")
        arr2 = []
        for i in arrayOfpk:
            arr2.append(int(i))
        snippet = Product.objects.annotate(categoryId=F('category')).filter(id__in=arr2).all()
        print(snippet)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print(request.data)
        print("****************")
        print(pks)
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


@api_view(['GET'])
def order_list(request, pk, format=None):
    if request.method == "GET":
        snippet = Order.objects.annotate(userId=F('user')).annotate(firstName=F('firstname')).annotate(lastName=F('lastname')).annotate(zip=F('zip_code')).filter(user__id=pk)
        serializer = OrderSerializer(snippet, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def order_detail(request, format=None):
    if request.method == 'POST':
        print(request.data)
        checkout = request.data['checkout']
        cart = request.data['cart']
        user = request.data['user']
        token = request.data['token']
        total = int(float(cart['total']))
        userObj=User.objects.filter(id=user['id']).first()
        token = request.data['token']
        print("***********###################********")
        orderObj = Order.objects.create(
            firstname=checkout['firstName'],
            lastname=checkout['lastName'],
            email=checkout['email'],
            phone=checkout['phone'],
            street=checkout['street'],
            street2=checkout['street2'],
            state=checkout['state'],
            zip_code=checkout['zip'],
            user=userObj,
            token=token,
            total=total
            )
        
        for i in cart['myCart']:
            product = Product.objects.filter(id=i['id']).first()
            LineItem.objects.create(quantity=i['quantity'],product=product, order=orderObj)
        
        return Response(status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'POST'])
def payment_process(request, format=None):
    if request.method == 'POST':
        print("********process*******")
        print(request.data)
        client = razorpay.Client(auth=("rzp_test_BXuuvSnv4i88g9","UwnwdougBKgb4Z5Vl0zMiJq6"))
        order_amount = float(request.data['amount']) #request.data['amount']
        order_currency = request.data['currency']
        order_receipt = request.data['receipt']
        response = client.order.create(dict(amount=int(order_amount),
                            currency=order_currency,
                            receipt = order_receipt))
        # print(response)
        return Response(response)

@api_view(['GET','POST'])
def payment_complete(request, format=None):
    if request.method == 'POST':
        print("********complete*******")
        print(request.data)
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def register(request, format=None):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.data)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
        registered = True
    return Response(status=status.HTTP_201_CREATED)

# @api_view(['GET'])
def get_auth(request):
    if request.method == 'GET':
        print("*********",request.user)
        # print(request.data.user.id)
        print("12345678*********")
        snippet = User.objects.filter(id=request.user.email).first()
        print(snippet.email)
        serializer = UserSerializer(snippet)
        # return HttpResponse(serializer.data) 
         
    return JsonResponse(serializer.data)

# @api_view(['POST'])
@csrf_exempt
def user_login(request, format=None):
    if request.method == 'POST':
        data = request.body.decode("UTF-8")
        abc = ast.literal_eval(data)
        print(type(abc))
        email = abc['email']
        password = abc['password']
        user = authenticate(email=email, password=password)
        if user:
            print("******acive*****")
            if user.is_active:
                login(request, user)

                print(user.is_authenticated)
                print(user.id)
                snippet = User.objects.filter(id=user.id).first()
                serializer = UserSerializer(snippet)
        else:
            print("afhao;ffoiaf;fa;eihaafhlaiufhiaufhkagfk")
    return JsonResponse(serializer.data)


@api_view(['POST'])
# @login_required
def logout_view(request):
    if request.method == 'POST':
        print("auhfulahfluhfuahfhufpauhf;ahufauhfahuf;iah;a;ifhuifhlzhfzuifh")
        logout(request)
    return Response(status=status.HTTP_201_CREATED)