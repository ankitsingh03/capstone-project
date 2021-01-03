from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    photo = models.CharField(max_length=200)


class User(models.Model):

    class DEF(models.TextChoices):
        user = 'user'
        admin ='admin'
    email = models.EmailField()
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=DEF.choices, default=DEF.user)
    salt = models.CharField(max_length=150)
    googleId = models.CharField(max_length=150, null=True)
    facebookId = models.CharField(max_length=150, null=True)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.CharField(max_length=250)
    rating = models.BigIntegerField()
    price = models.BigIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Review(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    rating = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Order(models.Model):
    class ABC(models.TextChoices):
        pending = 'pending'
        shipped = 'shipped'
        delivered = 'delivered'
    class XYZ(models.TextChoices):
        ap = 'Andhra Pradesh'
        an = 'Arunachal Pradesh'
        Assam = 'Assam'
        Bihar = 'Bihar'
        Chhattisgarh = 'Chhattisgarh'
    status = models.CharField(max_length=50, choices=ABC.choices, default=ABC.pending)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=XYZ.choices)
    zip_code = models.CharField(max_length=10)
    phone = models.BigIntegerField()
    email = models.EmailField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LineItem(models.Model):
    quantity = models.BigIntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
