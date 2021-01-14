from rest_framework import serializers
from .models import User, Product, Order, LineItem


class CategorySerializer(serializers.Serializer):
    """
    It will create serializers data for Category Model
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    photo = serializers.CharField()


class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(source='category.id')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'photo',
            'rating', 'price', 'categoryId'
            ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'password',
            'role', 'salt', 'googleId', 'facebookId'
            ]


class LineItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    productId = serializers.IntegerField(source='product.id')
    orderId = serializers.IntegerField(source='order.id')

    class Meta:
        model = LineItem
        fields = ['id', 'quantity', 'productId', 'orderId', 'product']


class OrderSerializer(serializers.ModelSerializer):
    lineItems = LineItemSerializer(many=True, read_only=True)
    firstName = serializers.CharField(source='firstname')
    lastName = serializers.CharField(source='lastname')
    userId = serializers.IntegerField(source='user.id')
    zip = serializers.CharField(source='zip_code')

    class Meta:
        model = Order
        fields = [
            'id', 'status', 'firstName', 'lastName', 'street',
            'street2', 'state', 'zip', 'phone', 'email', 'userId', 'lineItems'
            ]


class ReviewSerializer(serializers.Serializer):
    """
    It will create serializers data for the problem 2
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    rating = serializers.IntegerField()
    productId = serializers.IntegerField()
    userId = serializers.IntegerField()
