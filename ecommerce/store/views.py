from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
import datetime
from django.contrib.auth.decorators import login_required
from .models import Product, Wishlist, Customer, Order, OrderItem, ShippingAddress
from .utils import cartData, guestOrder
from django.contrib.auth.models import User


def store(request):
    data = cartData(request)

    cartItems = data['cartItems']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

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


def about_view(request):
    return render(request, 'store/about.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        Customer.objects.create(user=user, name=username, email=email)
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('store')

    return render(request, 'store/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'store')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login_view')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('store')


@login_required(login_url='login_view')  # Redirect to login if not authenticated
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist_items': wishlist_items})


def toggle_wishlist(request, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    product = get_object_or_404(Product, id=product_id)
    wishlist_entry, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        wishlist_entry.delete()
        status = 'removed'
    else:
        status = 'added'

    return JsonResponse({'status': status})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_in_wishlist = False  # Default to not wishlisted for unauthenticated users

    if request.user.is_authenticated:
        is_in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists()

    return render(request, 'store/product_detail.html', {
        'product': product,
        'is_in_wishlist': is_in_wishlist,
    })





















