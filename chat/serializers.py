from rest_framework import serializers
from .models import Blog, Evento, Task, Estudio, Trabajo, Entretenimiento, Noticia, Cancion

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['usuario']

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'
        read_only_fields = ['usuario']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['usuario']

class EstudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudio
        fields = '__all__'
        read_only_fields = ['usuario']

class TrabajoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trabajo
        fields = '__all__'
        read_only_fields = ['usuario']

class EntretenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entretenimiento
        fields = '__all__'
        read_only_fields = ['usuario']

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'
        read_only_fields = ['usuario']

class CancionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancion
        fields = '__all__'
        read_only_fields = ['usuario']
