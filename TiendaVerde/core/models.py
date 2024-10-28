from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Producto(models.Model):
    productoID = models.CharField(max_length=50, primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.IntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='PedidoProducto', related_name='pedidos')
    estado = models.CharField(max_length=50, default='pendiente')
    total = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    def __str__(self):
        return f'Pedido {self.id} - {self.usuario.username} - {self.estado}'

    def calcular_total(self):
        self.total = sum(producto.precio for producto in self.productos.all())
        self.save()

class Carrito(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name="carrito")
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    def calcular_total(self):
        return sum(item.subtotal() for item in self.productos.all())
    
class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name="productos")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en el carrito de {self.carrito.usuario.username}"

    def subtotal(self):
        return self.cantidad * self.producto.precio
    
class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio