from django.contrib import admin
from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'stock', 'talle', 'color', 'categoria', 'vendedor', 'fecha_publicacion')
    search_fields = ('nombre', 'descripcion', 'color', 'categoria')
    list_filter = ('categoria', 'talle', 'color', 'fecha_publicacion')
    ordering = ('-fecha_publicacion',)
