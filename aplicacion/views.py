from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Carrito, CarritoItem, Pedido, PedidoItem, Seguimiento, Categoria
from .forms import ProductoForm, PedidoForm, RegistroForm, SeguimientoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test


def is_admin(user):
    return user.is_staff

def listar_productos(request):
    categorias = Categoria.objects.all()
    mensaje = request.GET.get('mensaje', None)  

    context = {
        'categorias': categorias,
        'mensaje': mensaje,
    }

    return render(request, 'aplicacion/productos/listar_productos.html', context)


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
    usuario = request.user

    if usuario.baneado:
        return render(request, 'aplicacion/usuarios/baneado.html')

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

        seguimiento= Seguimiento.objects.create(
            pedido=pedido,
            estado='pendiente',
            descripcion='Pedido recibido y en proceso de la despachación.'
        )
        carrito.delete()

        print(usuario.baneado)
        del request.session['carrito_id']
        return redirect('ver_seguimiento', pedido_id=pedido.id)

    return render(request, 'aplicacion/pedidos/realizar_pedido.html', {'items': items, 'usuario': usuario})


def ver_carrito(request):
    carrito_id = request.session.get('carrito_id')
    if carrito_id:
        carrito = get_object_or_404(Carrito, id=carrito_id)
        items = CarritoItem.objects.filter(carrito=carrito)
        total = sum(item.subtotal() for item in items)
    else:
        carrito = None
        items = []
        total = 0

    return render(request, 'aplicacion/carrito/ver_carrito.html', {'carrito': carrito, 'items': items, 'total': total})



def actualizar_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        if cantidad > 0:
            item.cantidad = cantidad
            item.save()
    return redirect('ver_carrito')


def eliminar_del_carrito(request, item_id):
    item = get_object_or_404(CarritoItem, id=item_id)
    if request.method == 'POST':
        item.delete()
    return redirect('ver_carrito')

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

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by('-creado')
    return render(request, 'aplicacion/pedidos/mis_pedidos.html', {'pedidos': pedidos})

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
    categoria_moledores = Categoria.objects.get(nombre="Moledores")
    productos = Producto.objects.filter(categoria=categoria_moledores)
    return render(request, 'aplicacion/moledores.html', {'productos': productos})

def listar_bongs(request):
    categoria_bongs = Categoria.objects.get(nombre="Bongs")
    productos = Producto.objects.filter(categoria=categoria_bongs)
    return render(request, 'aplicacion/bongs.html', {'productos': productos})

def mochilas(request):
    categoria_mochilas = Categoria.objects.get(nombre="Mochilas")
    productos = Producto.objects.filter(categoria=categoria_mochilas)
    return render(request, 'aplicacion/mochilas.html', {'productos': productos})

def papeleria(request):
    categoria_papeleria = Categoria.objects.get(nombre="Papeleria")
    productos = Producto.objects.filter(categoria=categoria_papeleria)
    return render(request, 'aplicacion/papeleria.html', {'productos': productos})

def estado_producto(request):
    return render(request, 'aplicacion/estado_producto.html')

@user_passes_test(is_admin)
def admin_listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'aplicacion/admin/listar_usuarios.html', {'usuarios': usuarios})

@user_passes_test(is_admin)
def admin_agregar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_listar_usuarios')
    else:
        form = UserCreationForm()
    return render(request, 'aplicacion/admin/agregar_usuario.html', {'form': form})

@user_passes_test(is_admin)
def admin_editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_listar_usuarios')
    else:
        form = UserChangeForm(instance=usuario)
    return render(request, 'aplicacion/admin/editar_usuario.html', {'form': form})

@user_passes_test(is_admin)
def admin_eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    tiene_pedidos = Pedido.objects.filter(usuario=usuario).exists()
    if request.method == 'POST':
        if tiene_pedidos:
            usuario.baneado = True
            usuario.save()
        else:
            usuario.delete()
        return redirect('admin_listar_usuarios')
    return render(request, 'aplicacion/admin/eliminar_usuario.html', {'usuario': usuario, 'tiene_pedidos': tiene_pedidos})

@user_passes_test(is_admin)
def admin_listar_seguimientos(request):
    seguimientos = Seguimiento.objects.all()
    return render(request, 'aplicacion/admin/listar_seguimientos.html', {'seguimientos': seguimientos})

@user_passes_test(is_admin)
def admin_editar_seguimiento(request, seguimiento_id):
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    if request.method == 'POST':
        form = SeguimientoForm(request.POST, instance=seguimiento)
        if form.is_valid():
            form.save()
            return redirect('admin_listar_seguimientos')
    else:
        form = SeguimientoForm(instance=seguimiento)
    return render(request, 'aplicacion/admin/editar_seguimiento.html', {'form': form})

@user_passes_test(is_admin)
def admin_eliminar_seguimiento(request, seguimiento_id):
    seguimiento = get_object_or_404(Seguimiento, id=seguimiento_id)
    if request.method == 'POST':
        seguimiento.delete()
        return redirect('admin_listar_seguimientos')
    return render(request, 'aplicacion/admin/eliminar_seguimiento.html', {'seguimiento': seguimiento})

@user_passes_test(is_admin)
def admin_listar_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'aplicacion/admin/listar_pedidos.html', {'pedidos': pedidos})

@user_passes_test(is_admin)
def admin_ver_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    seguimientos = Seguimiento.objects.filter(pedido=pedido)
    items = pedido.pedidoitem_set.all()

    for item in items:
        item.total = item.cantidad * item.precio

    if request.method == 'POST':
        estado = request.POST.get('estado')
        descripcion = request.POST.get('descripcion')

        Seguimiento.objects.create(
            pedido=pedido,
            estado=estado,
            descripcion=descripcion
        )
        pedido.estado = estado  
        pedido.save(update_fields=['estado', 'actualizado'])  
        return redirect('admin_ver_pedido', pedido_id=pedido.id)

    return render(request, 'aplicacion/admin/ver_pedido.html', {
        'pedido': pedido,
        'seguimientos': seguimientos,
        'items': items,
    })

@user_passes_test(is_admin)
def admin_inicio(request):

    return render(request, 'aplicacion/admin/adminpanel.html')
    

@user_passes_test(is_admin)
def admin_listar_productos(request):
    categoria_id = request.GET.get('categoria_id')
    if categoria_id:
        productos = Producto.objects.filter(categoria_id=categoria_id)
    else:
        productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'aplicacion/admin/listar_productos.html', {'productos': productos, 'categorias': categorias})


@user_passes_test(is_admin)
def admin_agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'aplicacion/admin/agregar_producto.html', {'form': form})

@user_passes_test(is_admin)
def admin_editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin_listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'aplicacion/admin/editar_producto.html', {'form': form})

@user_passes_test(is_admin)
def admin_eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    tiene_pedidos = PedidoItem.objects.filter(producto=producto).exists()
    if request.method == 'POST':
        if tiene_pedidos:
            producto.oculto = True
            producto.save()
        else:
            producto.delete()
        return redirect('admin_listar_productos')
    return render(request, 'aplicacion/admin/eliminar_producto.html', {'producto': producto, 'tiene_pedidos': tiene_pedidos})


def admin_ver_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    pedidos = Pedido.objects.filter(usuario=usuario).prefetch_related('pedidoitem_set__producto')

    return render(request, 'aplicacion/admin/usuario_adminpanel.html', {'usuario': usuario, 'pedidos': pedidos})