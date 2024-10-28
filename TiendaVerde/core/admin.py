from django.contrib import admin
from .models import Producto, Pedido, Carrito, CarritoProducto, PedidoProducto
# Register your models here.

admin.site.register(Producto)
admin.site.register(Pedido)
admin.site.register(Carrito)
admin.site.register(CarritoProducto)
admin.site.register(PedidoProducto)