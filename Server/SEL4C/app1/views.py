from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from SEL4C.app1.serializers import UserSerializer, GroupSerializer
from .models import Usuario
from .serializers import *
import requests
from django.contrib import messages
from django.urls import reverse
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import hashlib as h
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "app1/homepage.html")

def register(request):
    return render(request, "app1/register.html")

def login_view(request):
    if request.method == 'POST':
        print("entre al if")
        email = request.POST.get('correo','').strip()
        password = request.POST.get('password','').strip()
        h_password = h.sha256(password.encode()).hexdigest()
        print(email)
        print(h_password)

        user = authenticate(request, email=email, password=h_password)
        print("Aqui estoy", user)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Correo o contraseña inválidos')
    
    return render(request, "app1/login.html")

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('http://localhost:8000/SEL4C/')

@login_required(login_url='login')
def dashboard(request):
    return render(request, "app1/index.html")

@login_required(login_url='login')
def usersList(request):
    users = list(Usuario.objects.all())
    ctx = {'users': users}
    return render(request, "app1/users-list.html", ctx)

@login_required(login_url='login')
def userDetails(request, pk):
    usuario = Usuario.objects.get(id = pk)
    questions = list(Pregunta.objects.all())
    autodiagnosticos = list(Autodiagnostico.objects.filter(usuario=usuario))
    ctx = {'usuario':usuario, 'questions':questions, 'autodiagnosticos':autodiagnosticos}
    return render(request, "app1/user-details.html", ctx)

@login_required(login_url='login')
def buttons(request):
    return render(request, "app1/ui-buttons.html")

@login_required(login_url='login')
def cards(request):
    return render(request, "app1/ui-card.html")

# Función de prueba POST para crear usuarios desde la app con país e institución 
@csrf_exempt
def crearUsuarioApp(request):
    if request.method == 'POST':
        # Obtener los datos JSON del cuerpo de la solicitud
        data = json.loads(request.body)
        
        pais_id = data.get('pais')
        institucion_id = data.get('institucion')
        
        try:
            pais = Pais.objects.get(id=pais_id)
            institucion = Institucion.objects.get(id=institucion_id)
            
            # Crear un nuevo usuario con la institución relacionada
            usuario = Usuario(
                nombre=data.get('nombre'),
                genero=data.get('genero'),
                grado=data.get('grado'),
                disciplina=data.get('disciplina'),
                pais=pais,
                institucion=institucion,
                correo=data.get('correo'),
                username=data.get('username'),
                password=data.get('password')
            )
            
            usuario.save()
            
            return JsonResponse({'mensaje': 'Usuario creado exitosamente'})
        except Institucion.DoesNotExist:
            return JsonResponse({'error': 'La institución con el ID proporcionado no existe'}, status=400)
    else:
        return JsonResponse({'error': 'Solicitud no permitida'}, status=405)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset  = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer

class PaisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Pais.objects.all()
    serializer_class = PaisSerializer

class InstitucionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Institucion.objects.all()
    serializer_class = InstitucionSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ProgresoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Progreso.objects.all()
    serializer_class = ProgresoSerializer

class ActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer

class EntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer

class PreguntaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer


class AutodiagnosticoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Autodiagnostico.objects.all()
    serializer_class = AutodiagnosticoSerializer

class RespuestaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
