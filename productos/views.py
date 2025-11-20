from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse


# Simulación básica de carrito en sesión
@login_required
def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', [])
    if producto_id not in carrito:
        carrito.append(producto_id)
        request.session['carrito'] = carrito
    return redirect(request.META.get('HTTP_REFERER', 'productos'))

@login_required
def ver_carrito(request):
    carrito_ids = request.session.get('carrito', [])
    productos = Producto.objects.filter(id__in=carrito_ids)
    return render(request, 'productos/carrito.html', {'productos': productos})

def home(request):
    return render(request, 'home.html')

def productos_view(request):
    productos = Producto.objects.all()
    carrito_ids = request.session.get('carrito', [])
    carrito_productos = Producto.objects.filter(id__in=carrito_ids)
    return render(request, 'productos/productos.html', {
        'productos': productos,
        'carrito_productos': carrito_productos,
    })


    # Filtros GET
    nombre = request.GET.get('nombre')
    categoria = request.GET.get('categoria')
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    orden = request.GET.get('orden')
    talle = request.GET.get('talle')
    color = request.GET.get('color')

    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if categoria:
        productos = productos.filter(categoria__iexact=categoria)
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    if talle:
        productos = productos.filter(talle__iexact=talle)
    if color:
        productos = productos.filter(color__icontains=color)
    if orden == 'asc':
        productos = productos.order_by('precio')
    elif orden == 'desc':
        productos = productos.order_by('-precio')

    return render(request, 'productos/productos.html', {'productos': productos})


def publicar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.vendedor = request.user
            producto.save()
            return redirect('productos')
    else:
        form = ProductoForm()
    return render(request, 'productos/publicar_producto.html', {'form': form})

