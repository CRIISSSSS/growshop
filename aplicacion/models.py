from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Categoria(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to='productos', null=True, blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)

    

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    session_key= models.CharField(max_length=50, null=True, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Carrito de {self.usuario.username} ' if self.usuario else f'Carrito Anónimo'
    
class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre}'

    def subtotal(self):
        return self.producto.precio * self.cantidad

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    direccion = models.TextField()
    estado = models.CharField(max_length=50, default='Pendiente', choices={
        ('pendiente', 'Pendiente'),
        ('en proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado')})
    
class PedidoItem(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre} en Pedido {self.pedido.id}'
    
class Seguimiento(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    estado = models.CharField(max_length=50, default='Pendiente', choices={
        ('pendiente', 'Pendiente'),
        ('en proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado')})
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    descripcion = models.TextField()
    
    def __str__(self):
        return f'Seguimiento de Pedido {self.pedido.id}'