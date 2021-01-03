from rest_framework import serializers
from .models import Category, User, Product, Review, Order, LineItem


class CategorySerializer(serializers.Serializer):
    """
    It will create serialized data for Category Model
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    photo = serializers.CharField()

    def create(self, validated_data):
        """
        Create and return a new Category instance, given the validated data.
        """
        return CompanyTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance


class ProductSerializer(serializers.Serializer):
    """
    It will create serialized data for the problem 2
    """
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField()
    photo = serializers.CharField()
    rating = serializers.CharField()
    price = serializers.CharField()
    categoryId = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return CompanyTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.price = validated_data.get('price', instance.price)
        instance.categoryId = validated_data.get('categoryId', instance.categoryId)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','password', 'role', 'salt', 'googleId', 'facebookId']


class ReviewSerializer(serializers.Serializer):
    """
    It will create serialized data for the problem 2
    """
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    content = serializers.CharField()
    rating = serializers.IntegerField()
    productId = serializers.IntegerField()
    userId = serializers.IntegerField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return CompanyTable.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title',instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.productId = validated_data.get('productId', instance.productId)
        instance.userId = validated_data.get('userId', instance.userId)
        instance.save()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'status', 'firstname', 'lastname', 'street', 'street2',
            'state', 'zip_code', 'phone', 'email', 'user'
            ]


class LineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = LineItem
        fields = ['quantity', 'product']