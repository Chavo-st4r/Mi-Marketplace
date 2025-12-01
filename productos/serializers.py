from rest_framework import serializers
from .models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    vendedor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Producto
        fields = '__all__'
