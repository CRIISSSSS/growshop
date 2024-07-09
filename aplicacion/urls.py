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
    path('carrito/actualizar/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar_pedido', views.realizar_pedido, name='realizar_pedido'),
    path('seguimiento/<int:pedido_id>/', views.ver_seguimiento, name='ver_seguimiento'),
    path('moledores/', views.moledores, name='moledores'),
    path('bongs/', views.listar_bongs, name='bongs'),
    path('mochilas/', views.mochilas, name='mochilas'),
    path('papeleria/', views.papeleria, name='papeleria'),
    path('estado_producto/', estado_producto, name='estado_producto'),
    path('mis_pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path('adm/usuarios/', views.admin_listar_usuarios, name='admin_listar_usuarios'),
    path('adm/usuarios/agregar/', views.admin_agregar_usuario, name='admin_agregar_usuario'),
    path('adm/usuarios/editar/<int:user_id>/', views.admin_editar_usuario, name='admin_editar_usuario'),
    path('adm/usuarios/eliminar/<int:user_id>/', views.admin_eliminar_usuario, name='admin_eliminar_usuario'),
    path('adm/seguimientos/', views.admin_listar_seguimientos, name='admin_listar_seguimientos'),
    path('adm/seguimientos/editar/<int:seguimiento_id>/', views.admin_editar_seguimiento, name='admin_editar_seguimiento'),
    path('adm/seguimientos/eliminar/<int:seguimiento_id>/', views.admin_eliminar_seguimiento, name='admin_eliminar_seguimiento'),
    path('adm/pedidos/', views.admin_listar_pedidos, name='admin_listar_pedidos'),
    path('adm/pedidos/<int:pedido_id>/', views.admin_ver_pedido, name='admin_ver_pedido'),
    path('adm/adminpenel', views.admin_inicio, name='admin_inicio'),
    path('adm/productos/', views.admin_listar_productos, name='admin_listar_productos'),
    path('adm/productos/agregar/', views.admin_agregar_producto, name='admin_agregar_producto'),
    path('adm/productos/editar/<int:producto_id>/', views.admin_editar_producto, name='admin_editar_producto'),
    path('adm/productos/eliminar/<int:producto_id>/', views.admin_eliminar_producto, name='admin_eliminar_producto'),
    path('adm/usuarios/ver/<int:user_id>/', views.admin_ver_usuario, name='admin_ver_usuario'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)