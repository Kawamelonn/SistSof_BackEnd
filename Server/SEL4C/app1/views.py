from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from SEL4C.app1.serializers import UserSerializer, GroupSerializer
from .models import Usuario
from .serializers import *

def home(request):
    return render(request, "app1/homepage.html")

def register(request):
    return render(request, "app1/register.html")

def login(request):
    return render(request, "app1/login.html")

def dashboard(request):
    return render(request, "app1/index.html")



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset  = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdministradorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [permissions.IsAuthenticated]

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProgresoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Progreso.objects.all()
    serializer_class = ProgresoSerializer
    permission_classes = [permissions.IsAuthenticated]

class ActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Actividad.objects.all()
    serializer_class = ActividadSerializer
    permission_classes = [permissions.IsAuthenticated]

class EntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that MyModel to be viewed or edited.
    """
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    permission_classes = [permissions.IsAuthenticated]
    
