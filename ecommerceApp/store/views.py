from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login

from django.views import View
from .models import *
# Create your views here.

def store(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created =Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}  
        cartItems = order['get_cart_items']
    
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems }
    return render(request,'store/store.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created =Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order , 'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created =Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0 ,'shipping': False}
        cartItems = order['get_cart_items'] 
    
    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print("Action: ", action)
    print("productId: ", productId)
    
    customer = request.user.customer
    product = Product.objects.get(id =productId)
    order,created =Order.objects.get_or_create(customer=customer,complete=False)
    
    orderItem,created =OrderItem.objects.get_or_create(order=order,product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
        
    return JsonResponse('Eklendi', safe=False)

def login_view(request):
    if request.method == 'POST':
        # Login formu burada işlenecek
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Kullanıcı başarıyla giriş yaparsa yönlendirilecek sayfa
        else:
            # Hatalı giriş durumu
            return render(request, 'store/login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'store/login.html')

def register_view(request):
    if request.method == 'POST':
        # Kayıt formu burada işlenecek
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Kullanıcı başarıyla kayıt olursa yönlendirilecek sayfa
    else:
        form = UserCreationForm()

    return render(request, 'store/register.html', {'form': form})