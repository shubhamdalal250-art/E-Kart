from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models.product import Product
from  .models.category import Category
from  .models.customer import Customer
from django.contrib import messages
from django.contrib.auth import authenticate, login
from  .models.cart import Cart
from django.db.models import Q
from django.http import JsonResponse
from .models.order import OrderDetails   




def home(request):
    products = None
    totalitem = 0

    if request.session.has_key('phone'):
        phone = request.session['phone']
        category = Category.get_all_categories()
        totalitem = Cart.objects.filter(phone=phone).count()

        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name

            #  SEARCH QUERY
            query = request.GET.get('query')

            #  CATEGORY FILTER
            category_id = request.GET.get('category')

            products = Product.get_all_product()

            if category_id:
                products = products.filter(category_id=category_id)

            if query:
                products = products.filter(
                    Q(name__icontains=query) |
                    Q(description__icontains=query)
                )

            data = {
                'name': name,
                'products': products,
                'category': category,
                'totalitem': totalitem
            }

            print('You are : ', phone)
            return render(request, 'home.html', data)
    else:
        return redirect('login')


def signup(request):
    if request.method == 'GET':
         return render(request, 'signup.html')
    else :
        postDATA = request.POST
        username = postDATA.get('username')
        phone = postDATA.get('phone')
        error_message = None
        value = {
            'phone' : phone,
            'username' : username
        }

        customer = Customer(name=username, phone=phone)

        if len(phone) < 10:
            error_message = "Phone number must be at least 10 digits long."
        elif len(phone) > 10:
            error_message = "Phone number must not exceed 10 digits."
        elif Customer.isExists(phone):
            error_message = "Phone number already registered."
        if not error_message:
            messages.success(request, "Registration successful.")
            customer.register()
            return redirect('signup')
        else:
            data = {
                'error' : error_message,
                'values' : value
            }   
            return render(request, 'signup.html' , data)
        
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        phone = request.POST.get('phone')
        value = {
            'phone' : phone
        }
        error_message = None

        customer = Customer.objects.filter(phone=request.POST["phone"]) 
        if customer:
            request.session['phone'] = phone
            return redirect('home')
        else:
            error_message = "Invalid phone number. Please try again."

        data = {
            'error' : error_message,
            'values' : value
        }   
        return render(request, 'login.html' , data)
    
def productdetail(request , pk):
    product = Product.objects.get(pk=pk)
    totalitem = 0
    item_in_cart = False
    if request.session.has_key('phone'):
        phone = request.session['phone']
        totalitem = len(Cart.objects.filter(phone=phone))
        item_in_cart = Cart.objects.filter(Q(phone=phone), Q(product=product.id)).exists()
        customer = Customer.objects.filter(phone=phone)
        for c in customer:
            name = c.name
        data = {
            'item_in_cart': item_in_cart,
            'product': product,
            'name': name,
            'totalitem': totalitem
            }
        return render(request, 'productdetail.html', data)

def logout(request):
    if request.session.has_key('phone'):
        del request.session['phone']
        return redirect('login')
    else:
        return redirect('login')
    
def add_to_cart(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    if request.method == 'POST':
        phone = request.session['phone']
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # convert to int

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist.")
            return redirect('home')

        # 🔑 CHECK if product already exists in cart
        cart_item = Cart.objects.filter(phone=phone, product=product).first()

        if cart_item:
            # Product already in cart → increase quantity
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Product not in cart → create new row
            Cart.objects.create(
                phone=phone,
                product=product,
                image=product.image,
                price=product.price,
                quantity=quantity
            )

        messages.success(request, f"{product.name} added to cart")
        return redirect(f'/productdetail/{product_id}')

    
def show_cart(request):
    if not request.session.has_key('phone'):
        return redirect('login')

    phone = request.session['phone']

    cart = Cart.objects.filter(phone=phone)

    # If cart is empty
    if not cart.exists():
        return render(request, "empty_cart.html")

    # Calculate total amount
    total = 0
    for item in cart:
        total += item.price * item.quantity

    totalitem = cart.count()

    customer = Customer.objects.get(phone=phone)

    data = {
        'cart': cart,
        'name': customer.name,
        'totalitem': totalitem,
        'total': total
    }

    return render(request, "show_cart.html", data)

  
def plus_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'error': 'Not logged in'}, status=403)

    phone = request.session['phone']
    product_id = request.GET.get('prod_id')

    cart = Cart.objects.get(phone=phone, product_id=product_id)
    cart.quantity += 1
    cart.save()

    return JsonResponse({'quantity': cart.quantity})


def minus_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'error': 'Not logged in'}, status=403)

    phone = request.session['phone']
    product_id = request.GET.get('prod_id')

    cart = Cart.objects.get(phone=phone, product_id=product_id)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()

    return JsonResponse({'quantity': cart.quantity})




def remove_cart(request):
    if not request.session.has_key('phone'):
        return JsonResponse({'error': 'Not logged in'}, status=403)

    phone = request.session['phone']
    product_id = request.GET.get('prod_id')

    try:
        cart = Cart.objects.get(phone=phone, product_id=product_id)
        cart.delete()
    except Cart.DoesNotExist:
        return JsonResponse({'error': 'Item not found'}, status=404)

    return JsonResponse({'success': True})






def checkout(request):
    phone = request.session.get('phone')
    if not phone:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')        # from modal
        address = request.POST.get('address')  # from modal

        cart_products = Cart.objects.filter(phone=phone)

        if not cart_products.exists():
            return redirect('show_cart')

        total = 0

        for cp in cart_products:
            total += cp.price * cp.quantity

            OrderDetails.objects.create(
                phone=phone,
                product=cp.product,
                price=cp.price,
                quantity=cp.quantity,
                image=cp.image,
                status="Pending"
            )

        # Clear cart after checkout
        cart_products.delete()

        return render(request, 'order_success.html', {
            'name': name,
            'total': total
        })

    return redirect('show_cart')




def my_orders(request):
    phone = request.session.get('phone')
    if not phone:
        return redirect('login')

    orders = OrderDetails.objects.filter(phone=phone).order_by('-ordered_date')

    customer = Customer.objects.get(phone=phone)

    data = {
        'orders': orders,
        'name': customer.name
    }

    return render(request, 'my_orders.html', data)





 

   
    
             




   


    
        
