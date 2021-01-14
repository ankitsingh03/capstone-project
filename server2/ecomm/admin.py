from django.contrib import admin
from .models import Category, User, Product, Review, Order, LineItem

# Register your models here.
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(LineItem)
