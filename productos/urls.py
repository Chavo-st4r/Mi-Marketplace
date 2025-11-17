from django.contrib import admin
from django.urls import path
from productos import views  # importamos la vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # ruta raíz
]

from django.contrib import admin
from django.urls import path
from productos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # esta es la ruta raíz
]
