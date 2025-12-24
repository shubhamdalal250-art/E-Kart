from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
from .models.cart import Cart
from .models.order import OrderDetails   




class AdminProduct(admin.ModelAdmin):
    list_display = ['id','name', 'price', 'category', 'description']

class AdminCustomer(admin.ModelAdmin):
    list_display = ['id','name', 'phone']

class AdminCart(admin.ModelAdmin):
    list_display = ['id','phone', 'product', 'image', 'price', 'quantity']

class AdminOrderDetails(admin.ModelAdmin):
    list_display = ['id', 'phone', 'product', 'price','image', 'quantity', 'status', 'ordered_date']
    list_filter = ['status', 'ordered_date']
    search_fields = ['phone', 'product__name']



admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Cart,AdminCart)
admin.site.register(OrderDetails,AdminOrderDetails) 
