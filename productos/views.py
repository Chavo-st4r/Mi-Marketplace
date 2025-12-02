from django.shortcuts import render, redirect
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from reportlab.pdfgen import canvas
from io import BytesIO

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
    numero_compra = request.session.pop('compra_exitosa', None)

    return render(request, 'productos/carrito.html', {
        'productos': productos,
        'numero_compra': numero_compra
    })

@login_required
def confirmar_compra(request):
    carrito_ids = request.session.get('carrito', [])
    productos = Producto.objects.filter(id__in=carrito_ids)

    if request.method == 'POST':
        numero_compra = get_random_string(length=8).upper()
        direccion = request.POST.get('direccion')
        metodo_pago = request.POST.get('metodo_pago')

        # Limpiar carrito
        request.session['carrito'] = []

        # Generar PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica", 12)
        p.drawString(100, 800, f"Ticket de compra - Nº {numero_compra}")
        p.drawString(100, 780, f"Dirección: {direccion}")
        p.drawString(100, 760, f"Método de pago: {metodo_pago}")
        y = 740
        for producto in productos:
            p.drawString(100, y, f"{producto.nombre} - ${producto.precio}")
            y -= 20
        p.drawString(100, y - 20, "Gracias por tu compra en Mi Marketplace.")
        p.showPage()
        p.save()
        buffer.seek(0)

        # Guardar PDF en sesión como hex para descarga
        request.session['ticket_pdf'] = buffer.getvalue().hex()
        request.session['compra_exitosa'] = numero_compra

        return redirect('ver_carrito')

    return redirect('ver_carrito')

@login_required
def descargar_ticket(request):
    hex_data = request.session.get('ticket_pdf')
    if not hex_data:
        return redirect('productos')

    buffer = BytesIO(bytes.fromhex(hex_data))
    numero = request.session.get('compra_exitosa', 'compra')
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=ticket_{numero}.pdf'
    return response

def home(request):
    return render(request, 'home.html')

def productos_view(request):
    productos = Producto.objects.all()
    carrito_ids = request.session.get('carrito', [])
    carrito_productos = Producto.objects.filter(id__in=carrito_ids)

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
        try:
            productos = productos.filter(precio__gte=float(precio_min))
        except ValueError:
            pass
    if precio_max:
        try:
            productos = productos.filter(precio__lte=float(precio_max))
        except ValueError:
            pass
    if talle:
        productos = productos.filter(talle__iexact=talle)
    if color:
        productos = productos.filter(color__icontains=color)
    if orden == 'asc':
        productos = productos.order_by('precio')
    elif orden == 'desc':
        productos = productos.order_by('-precio')

    return render(request, 'productos/productos.html', {
        'productos': productos,
        'carrito_productos': carrito_productos,
    })

@login_required
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

@login_required
def historial_publicaciones(request):
    publicaciones = Producto.objects.filter(vendedor=request.user).order_by('-id')
    return render(request, 'productos/historial.html', {
        'publicaciones': publicaciones
    })
