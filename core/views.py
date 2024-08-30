from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .bot import send_order_notification
from .forms import UserRegisterForm
from .models import Order, OrderProduct, Product


def home(request):
    return render(request, 'core/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'core/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'core/product_detail.html', {'product': product})



def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    cart.append(product_id)
    request.session['cart'] = cart
    return redirect('product_list')


def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    total_price = sum([product.price for product in products])
    return render(request, 'core/cart.html', {'products': products, 'total_price': total_price})


def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', [])
        if not cart:
            return redirect('product_list')

        user = request.user
        delivery_address = request.POST.get('address')
        comment = request.POST.get('comment', '')

        order = Order.objects.create(user=user, delivery_address=delivery_address, comment=comment)
        products = Product.objects.filter(id__in=cart)

        for product in products:
            OrderProduct.objects.create(order=order, product=product, quantity=1)

        request.session['cart'] = []

        # Отправляем уведомление в Telegram
        send_order_notification(order.id)

        return redirect('order_complete')

    return render(request, 'core/checkout.html')

def order_complete(request):
    return render(request, 'core/order_complete.html')
