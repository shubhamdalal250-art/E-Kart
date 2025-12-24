from django.contrib import admin
from django.urls import path
from .views import home, signup, login , productdetail
from store import views 

urlpatterns = [
  path('', home , name='home'),
  path('signup', signup , name='signup'),
  path('login', login , name='login'),
  path('productdetail/<int:pk>', productdetail , name='productdetail'),
  path('logout', views.logout , name='logout'),
  path('add_to_cart', views.add_to_cart , name='add_to_cart'),
  path('show_cart', views.show_cart , name='show_cart'),
  path('plus_cart', views.plus_cart , name='plus_cart'),
  path('minus_cart', views.minus_cart, name='minus_cart'),
  path('remove_cart', views.remove_cart, name='remove_cart'),
  path('checkout', views.checkout, name='checkout'),
  path('my-orders', views.my_orders, name='my_orders'),


]