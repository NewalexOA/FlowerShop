from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .bot import send_order_notification
from .forms import UserRegisterForm
from .models import Order, OrderProduct, Product, Cart, CartProduct


@login_required
def checkout(request):
    if request.method == 'POST':
        user = request.user
        delivery_address = request.POST.get('address')
        comment = request.POST.get('comment')

        # Создание заказа
        order = Order.objects.create(user=user, delivery_address=delivery_address, comment=comment)

        # Получение корзины пользователя
        cart, created = Cart.objects.get_or_create(user=user)
        cart_products = CartProduct.objects.filter(cart=cart)

        # Перенос товаров из корзины в заказ
        for cart_product in cart_products:
            OrderProduct.objects.create(
                order=order,
                product=cart_product.product,
                quantity=cart_product.quantity
            )

        # Очистка корзины
        cart_products.delete()

        # Отправка уведомления в Telegram
        send_order_notification(order.id)

        return redirect('order_complete')
    else:
        return render(request, 'core/checkout.html')


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


@login_required
def add_to_cart(request, product_id):
    user = request.user
    product = get_object_or_404(Product, id=product_id)
    
    # Получение или создание корзины для пользователя
    cart, created = Cart.objects.get_or_create(user=user)
    
    # Добавление продукта в корзину
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    
    return redirect('product_list')


@login_required
def cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_products = CartProduct.objects.filter(cart=cart)
    total_price = sum([cp.product.price * cp.quantity for cp in cart_products])
    return render(request, 'core/cart.html', {'products': cart_products, 'total_price': total_price})


def order_complete(request):
    return render(request, 'core/order_complete.html')
