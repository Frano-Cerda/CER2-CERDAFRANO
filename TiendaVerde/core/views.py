from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Producto, Carrito, CarritoProducto, Pedido, PedidoProducto
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, '¡Tu cuenta ha sido creada exitosamente! Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/registro.html', {'form': form})

def index(request):
    return render(request, 'core/index.html')

def catalogo(request):
    productos = Producto.objects.all()
    return render(request, 'core/catalogo.html', {'productos': productos})

# Ver Carrito
@login_required
def ver_carrito(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    productos = carrito.productos.all()
    total = carrito.calcular_total()
    return render(request, 'core/carrito.html', {'productos_en_carrito': productos, 'total_carrito': total})

# Agregar producto
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, productoID=producto_id)
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    carrito_producto, created = CarritoProducto.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        carrito_producto.cantidad += 1
    carrito_producto.save()
    return redirect('ver_carrito')

# Eliminar producto
@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = Carrito.objects.get(usuario=request.user)
    producto_en_carrito = get_object_or_404(CarritoProducto, carrito=carrito, producto__productoID=producto_id)
    producto_en_carrito.delete()
    
    return redirect('ver_carrito')

# Confirmar carrito y crear pedido
@login_required
def confirmar_pedido(request):
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    productos_en_carrito = carrito.productos.all()
    
    if productos_en_carrito.exists():
        total_pedido = sum(item.subtotal() for item in productos_en_carrito)
        pedido = Pedido.objects.create(
            usuario=request.user,
            estado='pendiente',
            fecha=timezone.now(),
            total=total_pedido
        )
        
        # Pasa productos del carrito al pedido
        for item in productos_en_carrito:
            PedidoProducto.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad
            )
        CarritoProducto.objects.filter(carrito=carrito).delete()
        
        messages.success(request, "¡Tu pedido ha sido confirmado!")
    else:
        messages.warning(request, "Tu carrito está vacío. No puedes confirmar un pedido sin productos.")
    
    return redirect('ver_carrito')