from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    photo = models.CharField(max_length=200)


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class DEF(models.TextChoices):
        user = 'user'
        admin = 'admin'
    username = models.CharField(_('username'), max_length=30, blank=True)
    email = models.EmailField(unique=True, max_length=255, blank=False)
    password = models.CharField(max_length=200)
    role = models.CharField(
        max_length=20,
        choices=DEF.choices,
        default=DEF.user
        )
    salt = models.CharField(max_length=150, null=True)
    googleId = models.CharField(max_length=150, null=True)
    facebookId = models.CharField(max_length=150, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )

    # Add additional fields here if needed

    objects = UserManager()

    USERNAME_FIELD = 'email'


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
        Delhi = 'Delhi'
        Mumbai = 'Mumbai'
        Bangalore = 'Bangalore'
        Kolkata = 'Kolkata'
        Chennai = 'Chennai'
    status = models.CharField(
        max_length=50, choices=ABC.choices, default=ABC.pending
        )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    street2 = models.CharField(max_length=100)
    state = models.CharField(max_length=100, choices=XYZ.choices)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=150)
    total = models.BigIntegerField(null=True)
    order_id = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    signature = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class LineItem(models.Model):
    quantity = models.BigIntegerField()
    product = models.ForeignKey(
        Product, related_name='product_det', on_delete=models.CASCADE
        )
    order = models.ForeignKey(
        Order, related_name='lineItems', on_delete=models.CASCADE
        )
