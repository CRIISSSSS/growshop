from django.contrib import admin
from .models import Producto, Carrito, CarritoItem, Pedido, PedidoItem, Seguimiento, Categoria
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre', 'descripcion')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock')
    search_fields = ('nombre', 'descripcion')

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'session_key', 'creado', 'actualizado')
    search_fields = ('usuario__username', 'session_key')

@admin.register(CarritoItem)
class CarritoItemAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad', 'creado', 'actualizado')
    search_fields = ('carrito__usuario__username', 'producto__nombre')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'total', 'creado', 'estado')
    search_fields = ('usuario__username',)
    list_filter = ('estado',)

@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio', 'creado', 'actualizado')
    search_fields = ('pedido__usuario__username', 'producto__nombre')

@admin.register(Seguimiento)
class SeguimientoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'estado', 'creado', 'actualizado')
    search_fields = ('pedido__usuario__username', 'descripcion')
    list_filter = ('estado',)