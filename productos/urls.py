from django.urls import path
from . import views  # importamos las vistas de la app productos

urlpatterns = [
    path('', views.home, name='home'),  # ruta raíz de la app productos
    path('lista/', views.productos_view, name='productos'),  # página de productos con filtros
    path('publicar/', views.publicar_producto, name='publicar_producto'),  # publicar prenda
    path('carrito/', views.ver_carrito, name='ver_carrito'),  # ver carrito
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # agregar producto al carrito
    path('confirmar-compra/', views.confirmar_compra, name='confirmar_compra'),  # confirmar compra y emitir ticket
    path('carrito/ticket/', views.descargar_ticket, name='descargar_ticket'),
    path('historial/', views.historial_publicaciones, name='historial_publicaciones'),

    # Rutas de Mercado Pago
    path('pago/exitoso/', views.pago_exitoso, name='pago_exitoso'),
    path('pago/fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago/pendiente/', views.pago_pendiente, name='pago_pendiente'),
]
