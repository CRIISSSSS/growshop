from django import forms
from .models import Producto, Pedido, Seguimiento
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'stock', 'imagen', 'categoria']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion']

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ['estado', 'descripcion']

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SeguimientoForm(forms.ModelForm):
    class Meta:
        model = Seguimiento
        fields = ['estado', 'descripcion']
        widgets = {
            'estado': forms.Select(choices=Seguimiento.estado),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

