from django.shortcuts import render
from .models import Category, User, Product, Review, Order, LineItem
from django.contrib.auth import login, authenticate, logout
from .forms import UserForm
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from django.db.models import Count, Case, When, Value, CharField, IntegerField, F
from .serializers import CategorySerializer, ProductSerializer, UserSerializer,\
    ReviewSerializer, OrderSerializer, LineItemSerializer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
# Create your views here.

@csrf_exempt
def index(request):
    return render(request, 'index.html')


@csrf_exempt
def index2(request, pk):
    reviews = Review.objects.filter(id=pk).all()
    return render(request, 'index.html')


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
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


@csrf_exempt
# @api_view(['POST'])
def review_product(request, format=None):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body)
        title = data['title']
        content = data['content']
        rating = int(data['rating'])
        userId = int(data['userId'])
        productId = int(data['productId'])
        select_user = User.objects.filter(id=userId).first()
        select_product = Product.objects.filter(id=productId).first()
        Review.objects.create(title=title, content=content, rating=rating, user=select_user, product=select_product)
        return HttpResponse(status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT', 'DELETE'])
@csrf_exempt
def review_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Review.objects.annotate(productId=F('product')).annotate(userId=F('user')).filter(product__pk=pk)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        print("reviews:", request.user.is_authenticated)
        # print(request.user.email)
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


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def cart_detail(request, pks, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        pk_list = pks
        array_of_pk = pk_list.split(",")
        array_of_pk_filtered = []
        for i in array_of_pk:
            array_of_pk_filtered.append(int(i))
        snippet = Product.objects.annotate(categoryId=F('category')).filter(id__in=array_of_pk_filtered).all()
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


@csrf_exempt
@api_view(['GET'])
def order_list(request, pk, format=None):
    if request.method == "GET":
        snippet = Order.objects.annotate(userId=F('user')).annotate(firstName=F('firstname')).annotate(lastName=F('lastname')).annotate(zip=F('zip_code')).filter(user__id=pk)
        serializer = OrderSerializer(snippet, many=True)
        return Response(serializer.data)



        

# @api_view(['GET', 'POST'])
# def payment_process(request, format=None):
#     if request.method == 'POST':
#         print("********process*******")
#         print(request.data)
#         client = razorpay.Client(auth=("rzp_test_BXuuvSnv4i88g9","UwnwdougBKgb4Z5Vl0zMiJq6"))
#         order_amount = float(request.data['amount']) #request.data['amount']
#         order_currency = request.data['currency']
#         order_receipt = request.data['receipt']
#         response = client.order.create(dict(amount=int(order_amount),
#                             currency=order_currency,
#                             receipt = order_receipt))
#         # print(response)
#         return Response(response)

# @api_view(['GET','POST'])
# def payment_complete(request, format=None):
#     if request.method == 'POST':
#         print("********complete*******")
#         print(request.data)
#     return Response(status=status.HTTP_201_CREATED)



# @api_view(['POST'])
@csrf_exempt
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
        
        return HttpResponse(status=status.HTTP_201_CREATED)
        

# @api_view(['GET', 'POST'])
@csrf_exempt
def payment_process(request, format=None):
    if request.method == 'POST':
        print("********process*******")
        print(request.body)
        data = json.loads(request.body)
        client = razorpay.Client(auth=("rzp_test_BXuuvSnv4i88g9","UwnwdougBKgb4Z5Vl0zMiJq6"))
        order_amount = float(data['amount']) #data['amount']
        order_currency = data['currency']
        order_receipt = data['receipt']
        response = client.order.create(dict(amount=int(order_amount)*100,
                            currency=order_currency,
                            receipt = order_receipt))
        # print(response)
        return JsonResponse(response)


# @csrf_exempt
# @api_view(['POST'])
# def order_detail(request, format=None):
#     if request.method == 'POST':
#         print(request.data)
#         checkout = request.data['checkout']
#         cart = request.data['cart']
#         user = request.data['user']
#         token = request.data['token']
#         total = int(float(cart['total']))
#         userObj=User.objects.filter(id=user['id']).first()
#         token = request.data['token']
#         print("***********###################********")
#         orderObj = Order.objects.create(
#             firstname=checkout['firstName'],
#             lastname=checkout['lastName'],
#             email=checkout['email'],
#             phone=checkout['phone'],
#             street=checkout['street'],
#             street2=checkout['street2'],
#             state=checkout['state'],
#             zip_code=checkout['zip'],
#             user=userObj,
#             token=token,
#             total=total
#             )
        
#         for i in cart['myCart']:
#             product = Product.objects.filter(id=i['id']).first()
#             LineItem.objects.create(quantity=i['quantity'],product=product, order=orderObj)
        
#         return Response(status=status.HTTP_201_CREATED)


# @api_view(['GET','POST'])
@csrf_exempt
def payment_complete(request, format=None):
    print(request.user.id)
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        checkout = data['checkout']
        cart = data['cart']
        user_id = request.user.id
        total = data["amount"]
        order_obj = Order.objects.create(
            firstname=checkout["firstName"],
            lastname=checkout["lastName"],
            email=checkout["email"],
            phone=checkout['phone'],
            street=checkout['street'],
            street2=checkout['street2'],
            state=checkout['state'],
            zip_code=checkout['zip'],
            user=User.objects.filter(id=user_id).first(),
            payment_id = data['payment_id'],
            order_id = data['order_id'],
            signature = data['signature'],
            total=data['amount']
        )
        order_obj.save()
        # Order.objects.create(
        #     firstname="akshay",
        #     lastname="deshmukh",
        #     email="a@g.com",
        #     phone="9033282535",
        #     street="abc",
        #     street2="abc",
        #     state="Delhi",
        #     zip_code="144111",
        #     user=User.objects.filter(id=1).first(),
        #     payment_id = data['payment_id'],
        #     order_id = data['order_id'],
        #     signature = data['signature'],
        #     total=data['amount']
        #     )
        for i in cart:
            product = Product.objects.filter(id=i['id']).first()
            LineItem.objects.create(quantity=i['quantity'],product=product, order=order_obj)
        
    return HttpResponse(status=status.HTTP_201_CREATED)



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
# def get_auth(request):
#     if request.method == 'GET':
#         print("*********",request.user)
#         # print(request.data.user.id)
#         print("12345678*********")
#         snippet = User.objects.filter(id=request.user.email).first()
#         print(snippet.email)
#         serializer = UserSerializer(snippet)
#         # return HttpResponse(serializer.data) 
         
#     return JsonResponse(serializer.data)


@api_view(['GET'])
def get_auth(request):
    if request.method == 'GET':
        print(request.data)
        if request.user.is_authenticated:
            print("*********",request.user)
            print("12345678*********")
            snippet = User.objects.filter(id=request.user.id).first()
            print(snippet.email)
            serializer = UserSerializer(snippet)
            return Response(serializer.data)
        else:
            return Response({"error":"No User"}, status=403)
         
    # return Response(serializer.data)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = request.body.decode("UTF-8")
        user_data = json.loads(data)
        print(user_data)
        email = user_data['email']
        password = user_data['password']
        user = authenticate(request, email=email, password=password)
        if user:
            print(request.user)
            if user.is_active:
                login(request, user)
                snippet = User.objects.filter(id=user.id).first()
                serializer = UserSerializer(snippet)
                return JsonResponse(serializer.data)
        else:
            return HttpResponse({"error":"No User"}, status=403)



# @api_view(['POST'])
@csrf_exempt
@login_required
def logout_view(request):
    if request.method == 'POST':
        print("auhfulahfluhfuahfhufpauhf;ahufauhfahuf;iah;a;ifhuifhlzhfzuifh")
        logout(request)
    return HttpResponse(status=status.HTTP_201_CREATED)