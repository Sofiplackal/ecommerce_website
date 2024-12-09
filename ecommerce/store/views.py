from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder

# Store view
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

# Cart view
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

# Checkout view
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

# Update item view
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

# Process order view
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)


# Wishlist-related views
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.user.is_authenticated and request.user.is_staff:
        # Admin user logged in
        Wishlist.objects.get_or_create(user=request.user, product=product)
    else:
        # Guest user
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        Wishlist.objects.get_or_create(session_key=session_key, product=product)
    
    return redirect('wishlist_view')

def wishlist_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Show admin's wishlist
        wishlist_items = Wishlist.objects.filter(user=request.user)
    else:
        # Show guest's wishlist
        session_key = request.session.session_key
        wishlist_items = Wishlist.objects.filter(session_key=session_key)
    
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})

def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id)
    wishlist_item.delete()
    return redirect('wishlist_view')


# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})





