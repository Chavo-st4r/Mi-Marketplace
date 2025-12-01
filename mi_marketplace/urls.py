from django.contrib import admin
from django.urls import path, include
from productos import views  # solo si tenés la vista home en productos/views.py
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from productos.views_api import ProductoViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # ruta raíz
    path('usuarios/', include('usuarios.urls')),  # app usuarios
    path('productos/', include('productos.urls')),  # app productos
    path('accounts/', include('allauth.urls')),  # login social con allauth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),  # rutas de la API
]

# Configuración para servir archivos estáticos y media en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    if hasattr(settings, 'STATIC_ROOT') and settings.STATIC_ROOT:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
