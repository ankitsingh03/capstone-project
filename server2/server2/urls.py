"""server2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ecomm.views import category_list, category_detail, product_list,\
    review_product, review_detail, cart_detail,\
    order_list, payment_process, payment_complete,\
    user_login, register, get_auth, logout_view, index

urlpatterns = [
    path('', index),
    path('login/', index),
    path('signup/', index),
    path('home/', index),
    path('checkout/', index),
    path('cart/', index),
    path('products/<int:pk>', index),
    path('admin/', admin.site.urls),
    path('api/categories', category_list),
    path('api/categories/<int:pk>/', category_detail),
    path('api/products', product_list),
    path('api/reviews', review_product),
    path('api/reviews/<int:pk>/', review_detail),
    path('api/cart/<str:pks>', cart_detail),
    path('api/orders/<int:pk>/', order_list),
    path('api/payment/', payment_process),
    path('api/payment_success', payment_complete),
    path('auth/login', user_login),
    path('auth/signup', register),
    path('auth/me/', get_auth),
    path('auth/logout', logout_view),
    path('accounts/', include('allauth.urls')),
]
