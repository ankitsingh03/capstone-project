from rest_framework import serializers
from .models import Category, User, Product, Review, Order, LineItem


class CategorySerializer(serializers.Serializer):
    """
    It will create serializers data for Category Model
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


class ProductSerializer(serializers.ModelSerializer):
    categoryId = serializers.IntegerField(source='category.id')
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'photo', 'rating', 'price', 'categoryId']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','password', 'role', 'salt', 'googleId', 'facebookId']


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
        fields = ['id', 'status', 'firstName', 'lastName', 'street', 'street2', 'state', 'zip', 'phone', 'email', 'userId', 'lineItems']


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


# class LineItemSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     quantity = serializers.CharField()
#     productId = serializers.IntegerField()
#     orderId = serializers.IntegerField()
#     product = ProductSerializer(many=True, read_only=True)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return CompanyTable.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.quantity = validated_data.get('quantity',instance.quantity)
#         instance.productId = validated_data.get('productId', instance.productId)
#         instance.orderId = validated_data.get('orderId', instance.orderId)
#         instance.product = validated_data.get('product', instance.product)


# class OrderSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     status = serializers.CharField()
#     firstName = serializers.CharField()
#     lastName = serializers.CharField()
#     street = serializers.CharField()
#     street2 = serializers.CharField()
#     state = serializers.CharField()
#     zip = serializers.CharField()
#     phone = serializers.IntegerField()
#     email = serializers.CharField()
#     userId = serializers.IntegerField()
#     lineItems = LineItemSerializer(many=True, read_only=True)

#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return CompanyTable.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         instance.status = validated_data.get('status',instance.status)
#         instance.firstName = validated_data.get('firstName', instance.firstName)
#         instance.lastName = validated_data.get('lastName', instance.lastName)
#         instance.street = validated_data.get('street', instance.street)
#         instance.street2 = validated_data.get('street2', instance.street2)
#         instance.state = validated_data.get('state', instance.state)
#         instance.zip = validated_data.get('zip', instance.zip)
#         instance.phone = validated_data.get('phone', instance.phone)
#         instance.email = validated_data.get('email', instance.email)
#         instance.userId = validated_data.get('userId', instance.userId)
#         instance.lineItems = validated_data.get('lineItems', instance.lineItems)
#         instance.save()
#         return instance
