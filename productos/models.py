from django.db import models
from django.contrib.auth.models import User

class Producto(models.Model):
    CATEGORIAS = [
        ('remera', 'Remera'),
        ('pantalon', 'Pantalón'),
        ('zapatilla', 'Zapatilla'),
        ('campera', 'Campera'),
    ]

    TALLES = [
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='productos')
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)
    talle = models.CharField(max_length=5, choices=TALLES)
    color = models.CharField(max_length=30)
    stock = models.PositiveIntegerField(default=1)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} ({self.vendedor.username})"
