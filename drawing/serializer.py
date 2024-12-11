from rest_framework import serializers
from .models import Dibujo, Estrella, Comentario, Categoria, Reporte

# Los serializers son objetos que se utilizan para serializar y deserializar datos entre el lado del cliente y el servidor
# sirven para poder devolver la informacion en diferentes formatos, como JSON, XML, etc.

class DibujoSerializer(serializers.ModelSerializer):
    total_estrellas = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dibujo
        fields = '__all__'

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class DrawingCountSerializer(serializers.Serializer):
    total_drawings = serializers.IntegerField()