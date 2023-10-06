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
        fields = ['correo', 'password', 'progreso']
    
    def create(self, validated_data):
        password = h.sha256(validated_data['password'].encode()).hexdigest()
        adminstrador_instance = Administrador.objects.create(
            correo=validated_data['correo'],
            password = password,
            progreso=validated_data['progreso'],
        )
        return adminstrador_instance

class UsuarioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Usuario
        fields = ['nombre', 'genero', 'correo', 'username', 'password']

class ProgresoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Progreso
        fields = ['usuario', 'autodiagnostico', 'actividad']

class ActividadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Actividad
        fields = ['titulo', 'entrega']

class EntregaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Entrega
        fields = ['filename', 'file']

class PreguntaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pregunta
        fields = ['pregunta']


class AutodiagnosticoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Autodiagnostico
        fields = ['num_auto', 'usuario', 'pregunta', 'index']

class RespuestaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Respuesta
        fiels = ['respuesta']