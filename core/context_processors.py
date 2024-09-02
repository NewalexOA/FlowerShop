from .models import Cart, CartProduct

def cart_item_count(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        item_count = CartProduct.objects.filter(cart=cart).count()
        return {'cart_item_count': item_count}
    return {'cart_item_count': 0}
