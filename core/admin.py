from django.contrib import admin
from .models import Product, Order, OrderProduct, BotSettings
from .forms import ProductAdminForm


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['name', 'price']

# Регистрация моделей с классами администратора
admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(BotSettings)
