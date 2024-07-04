from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoItem, Pedido, PedidoItem, Seguimiento, Categoria
from .forms import ProductoForm, PedidoForm, RegistroForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect

def listar_productos(request):
    categorias = Categoria.objects.all()
    categoria_nombre = request.GET.get('categoria_nombre')
    
    if categoria_nombre:
        categoria = get_object_or_404(Categoria, nombre=categoria_nombre)
        productos = Producto.objects.filter(categoria=categoria)
    else:
        productos = Producto.objects.all()
    
    mensaje = request.GET.get('mensaje', None)
    return render(request, 'aplicacion/productos/listar_productos.html', {'productos': productos, 'categorias': categorias, 'mensaje': mensaje})


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito_id = request.session.get('carrito_id')
    if not carrito_id:
        carrito = Carrito.objects.create()
        request.session['carrito_id'] = carrito.id
    else:
        carrito = get_object_or_404(Carrito, id=carrito_id)

    carrito_item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()
    referer = request.headers.get('Referer', '/')
    return redirect(f'{referer}?mensaje=Producto+añadido+al+carrito')

@login_required
def realizar_pedido(request):
    carrito_id = request.session.get('carrito_id')
    if not carrito_id:
        return redirect('listar_productos')

    carrito = get_object_or_404(Carrito, id=carrito_id)
    items = CarritoItem.objects.filter(carrito=carrito)

    if request.method == 'POST':
        direccion = request.POST.get('direccion')
        errores= []
        
        for item in items:
            cantidad_solicitada = int(request.POST.get(f'cantidad_{item.producto.id}',1))
            if cantidad_solicitada > item.producto.stock:
                errores.append(f'No hay suficiente stock para el producto {item.producto.nombre}')
            else:
                item.cantidad = cantidad_solicitada
                item.save()
            
        if errores:
            return render(request, 'aplicacion/pedidos/realizar_pedido.html', {'items': items, 'errores': errores})
        
        pedido = Pedido.objects.create(
            usuario=request.user,
            total=sum(item.subtotal() for item in items),
            direccion=direccion,

        
        )
        for item in items:
            PedidoItem.objects.create(
                pedido=pedido,
                producto=item.producto,
                cantidad=item.cantidad,
                precio=item.producto.precio,
            )
            item.producto.stock -= item.cantidad
            item.producto.save()
        carrito.delete()
        del request.session['carrito_id']
        return redirect('ver_seguimiento', pedido_id=pedido.id)

    return render(request, 'aplicacion/pedidos/realizar_pedido.html', {'items': items})


def ver_carrito(request):
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        carrito = get_object_or_404(Carrito, id=carrito_id)
        items = CarritoItem.objects.filter(carrito=carrito)
    else:
        carrito = None
        items = []

    return render(request, 'aplicacion/carrito/ver_carrito.html', {'carrito': carrito, 'items': items})

@login_required
def ver_seguimiento(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    seguimientos = Seguimiento.objects.filter(pedido=pedido)
    return render(request, 'aplicacion/pedidos/ver_seguimiento.html', {'pedido': pedido, 'seguimientos': seguimientos})

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('listar_productos')
    else:
        form = RegistroForm()
    return render(request, 'aplicacion/usuarios/registro.html', {'form': form}) 

def login_usuario(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('listar_productos')
    else:
        form = AuthenticationForm()
    return render(request, 'aplicacion/usuarios/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('listar_productos')



def moledores(request):
    productos = Producto.objects.filter(categoria='Moledores')
    return render(request, 'aplicacion/moledores.html', {'productos': productos})

def listar_bongs(request):
    categoria_bongs = Categoria.objects.get(nombre="Bongs")
    productos = Producto.objects.filter(categoria=categoria_bongs)
    return render(request, 'aplicacion/bongs.html', {'productos': productos})

def mochilas(request):
    productos = Producto.objects.filter(categoria='Mochilas')
    return render(request, 'aplicacion/mochilas.html', {'productos': productos})

def papeleria(request):
    productos = Producto.objects.filter(categoria='Papelería')
    return render(request, 'aplicacion/papeleria.html', {'productos': productos})

def estado_producto(request):
    return render(request, 'aplicacion/estado_producto.html')