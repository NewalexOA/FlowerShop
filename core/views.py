from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .bot import send_order_notification
from .forms import UserRegisterForm, CheckoutForm
from .models import Order, OrderProduct, Product, Cart, CartProduct

@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_products = CartProduct.objects.filter(cart=cart)
    
    if not cart_products.exists():
        messages.warning(request, "У вас нет товаров в корзине")
        return redirect('cart_view')
    
    if request.method == 'POST':
        delivery_address = request.POST.get('address')
        comment = request.POST.get('comment')

        # Создание заказа
        order = Order.objects.create(user=user, delivery_address=delivery_address, comment=comment)

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
        total_price = sum([cp.product.price * cp.quantity for cp in cart_products])
        return render(request, 'core/checkout.html', {'cart_products': cart_products, 'total_price': total_price})

def home(request):
    products = Product.objects.all()
    return render(request, 'core/home.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/login/'})
            return redirect('login')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                errors = {}
                for field, error_list in form.errors.items():
                    errors[field] = [str(error) for error in error_list]
                return JsonResponse({'success': False, 'errors': errors})
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
    
    return redirect('home')

@login_required
def cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user)
    cart_products = CartProduct.objects.filter(cart=cart)
    total_price = sum([cp.product.price * cp.quantity for cp in cart_products])
    
    # Получаем сообщения из сессии
    storage = messages.get_messages(request)
    # Преобразуем сообщения в список, чтобы их можно было использовать в шаблоне
    message_list = list(storage)
    
    return render(request, 'core/cart.html', {
        'products': cart_products, 
        'total_price': total_price,
        'messages': message_list
    })

def order_complete(request):
    return render(request, 'core/order_complete.html')
