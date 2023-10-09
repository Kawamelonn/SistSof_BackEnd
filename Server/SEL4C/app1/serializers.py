from django.contrib.auth.models import User, Group
from django.contrib.auth.models import make_password
from rest_framework import serializers
from .models import *
import hashlib as h

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class AdministradorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Administrador
        fields = ['correo', 'password']
    
    def create(self, validated_data):
        password = h.sha256(validated_data['password'].encode()).hexdigest()
        adminstrador_instance = Administrador.objects.create(
            correo=validated_data['correo'],
            password = password,
        )
        return adminstrador_instance

class InstitucionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Institucion
        fields = ['id', 'nombre']

class PaisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pais
        fields = ['id', 'nombre']

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre', 'grado', 'disciplina', 'pais', 'institucion', 'genero', 'correo', 'username', 'password']

class ProgresoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Progreso
        fields = ['usuario', 'actividad', 'entrega', 'completado']

class ActividadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actividad
        fields = ['titulo']

class EntregaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entrega
        fields = ['filename', 'file']

class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pregunta
        fields = ['id', 'tipo_pregunta', 'pregunta']

class RespuestaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['respuesta']

class AutodiagnosticoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Autodiagnostico
        fields = ['num_auto', 'usuario', 'pregunta', 'respuesta', 'completada']

