from django.urls import path
from . import views
from .views import moledores, mochilas, papeleria, estado_producto
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.conf import settings


urlpatterns = [
    path('', views.listar_productos, name='listar_productos'),
    path('agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('realizar_pedido/', login_required(views.realizar_pedido), name='realizar_pedido'),
    path('registro/', views.registro_usuario, name='registro'),
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('realizar_pedido', views.realizar_pedido, name='realizar_pedido'),
    path('seguimiento/<int:pedido_id>/', views.ver_seguimiento, name='ver_seguimiento'),
    path('moledores/', moledores, name='moledores'),
    path('bongs/', views.listar_bongs, name='bongs'),
    path('mochilas/', mochilas, name='mochilas'),
    path('papeleria/', papeleria, name='papeleria'),
    path('estado_producto/', estado_producto, name='estado_producto'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)