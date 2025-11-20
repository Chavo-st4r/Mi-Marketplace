from django.urls import path
from . import views  # importamos las vistas de la app productos

urlpatterns = [
    path('', views.home, name='home'),  # ruta raíz de la app productos
    path('lista/', views.productos_view, name='productos'),  # página de productos con filtros
    path('publicar/', views.publicar_producto, name='publicar_producto'),  # publicar prenda
    path('carrito/', views.ver_carrito, name='ver_carrito'),  # ver carrito
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),  # agregar producto al carrito
]
