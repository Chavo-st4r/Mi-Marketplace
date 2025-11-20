from .models import Producto

def carrito_context(request):
    carrito_ids = request.session.get('carrito', [])
    productos = Producto.objects.all()
    carrito_productos = Producto.objects.filter(id__in=carrito_ids)
    return {
        'productos': productos,
        'carrito_productos': carrito_productos,
    }
