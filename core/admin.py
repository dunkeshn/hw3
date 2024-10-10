from django.contrib import admin

from core.models import Product, Cafe, Cart, Courier, Delivery, Order, DeliveryDescription


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )

@admin.register(Cafe)
class CafeAdmin(admin.ModelAdmin):
    list_display = ('id', 'address', 'barista_number', )

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'sum', )

@admin.register(Courier)
class CourierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', )

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'sum', 'delivery_status', )

@admin.register(DeliveryDescription)
class DeliveryDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', )
