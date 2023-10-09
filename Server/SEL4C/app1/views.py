from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
import csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.views import View
from django.db.models import Count, Q
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from SEL4C.app1.serializers import UserSerializer, GroupSerializer
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
import hashlib as h
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.response import Response
from django.conf import settings
import json
from django.db.models import Sum
import requests

def home(request):
    return render(request, "app1/homepage.html")

@csrf_exempt
def user_login_view(request):
    original_auth_backends = settings.AUTHENTICATION_BACKENDS
    settings.AUTHENTICATION_BACKENDS = ['SEL4C.app1.backends.CustomUserBackend']

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username','').strip()
        password = data.get('password','').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            api_url = f'http://localhost:8000/Usuarios/{user.id}/'
            print(api_url)
            response = requests.get(api_url)

            if response.status_code == 200:
                api_data = response.json()
                api_id = api_data.get('id', None)

                if api_id:
                    return JsonResponse({'message':'Usuario logueado exitosamente', 'id':api_id})
                else:
                    return JsonResponse({'message':'No iD'})
            else:
                return JsonResponse({'message':'No error 200'})
        else:
            return JsonResponse({'message':'Usuario o contraseña inválidos'})
        
    settings.AUTHENTICATION_BACKENDS = original_auth_backends

    return JsonResponse({'message':'El login requiere una POST request'})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('correo','').strip()
        password = request.POST.get('password','').strip()
        h_password = h.sha256(password.encode()).hexdigest()

        user = authenticate(request, email=email, password=h_password)

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
    usuario = Usuario.objects.get(id=pk)
    questions = list(Pregunta.objects.all())
    autodiagnosticos = Autodiagnostico.objects.filter(usuario=usuario)
    progreso = Progreso.objects.filter(usuario=usuario)
    # AUTODIAGNOSTICO INICIAL
    autoIniAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Autocontrol')
    autoIniLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Liderazgo')
    autoIniCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Conciencia y valor social')
    autoIniInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=1, competencia='Innovación social y sostenibilidad financiera')
    # Suma las respuestas de la competencia "Autocontrol" para el usuario
    suma_autocontrolini = autoIniAuto.aggregate(total_autocontrolini=Sum('respuesta__respuesta'))['total_autocontrolini'] or 0
    suma_liderazgoini = autoIniLider.aggregate(total_liderazgoini=Sum('respuesta__respuesta'))['total_liderazgoini'] or 0
    suma_concienciaini = autoIniCon.aggregate(total_concienciaini=Sum('respuesta__respuesta'))['total_concienciaini'] or 0
    suma_innovacionini = autoIniInn.aggregate(total_innovacionini=Sum('respuesta__respuesta'))['total_innovacionini'] or 0
    # AUTODIAGNOSTICO FINAL
    autoFinAuto = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Autocontrol')
    autoFinLider = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Liderazgo')
    autoFinCon = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Conciencia y valor social')
    autoFinInn = Autodiagnostico.objects.filter(usuario=usuario, num_auto=2, competencia='Innovación social y sostenibilidad financiera')
    # Suma las respuestas de la competencia "Autocontrol" para el usuario
    suma_autocontrolfin = autoFinAuto.aggregate(total_autocontrolfin=Sum('respuesta__respuesta'))['total_autocontrolfin'] or 0
    suma_liderazgofin = autoFinLider.aggregate(total_liderazgofin=Sum('respuesta__respuesta'))['total_liderazgofin'] or 0
    suma_concienciafin = autoFinCon.aggregate(total_concienciafin=Sum('respuesta__respuesta'))['total_concienciafin'] or 0
    suma_innovacionfin = autoFinInn.aggregate(total_innovacionfin=Sum('respuesta__respuesta'))['total_innovacionfin'] or 0
    
    ctx = {
        'usuario': usuario,
        'questions': questions,
        'autodiagnosticos': autodiagnosticos,
        'suma_autocontrolini': suma_autocontrolini,
        'suma_liderazgoini': suma_liderazgoini,
        'suma_concienciaini': suma_concienciaini,
        'suma_innovacionini': suma_innovacionini,
        'suma_autocontrolfin': suma_autocontrolfin,
        'suma_liderazgofin': suma_liderazgofin,
        'suma_concienciafin': suma_concienciafin,
        'suma_innovacionfin': suma_innovacionfin,
        'progreso': progreso,
    }
    
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

@login_required(login_url='login')
def institute_view(request):
    institutes = list(Institucion.objects.all())
    ctx = {'Instituciones': institutes}
    return render(request, "app1/institutions.html", ctx)

@login_required(login_url='login')
def register_institution(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']

        try:
            institution = Institucion.objects.create(nombre=nombre)
            messages.success(request, 'Institución registrada con éxito')
        except Exception as e:
            messages.error(request, 'No fue posible registrar la institución' + str(e))
        
        return redirect('institutions')

    return render(request, "app1/register-institutions.html")

@login_required(login_url='login')
def delete_institution(request, id):
    institution = get_object_or_404(Institucion, pk=id)
    print(institution)

    if request.method == 'POST':
        try:
            institution.delete()
            messages.success(request, 'Institucion borrada con éxito')
        except Exception as e:
            messages.error(request, 'No fue posible borrar la institución' + str(e))
    
    return redirect('institutions')

# Esta  es la funcion para que lea el archivo 
@method_decorator(csrf_exempt, name='dispatch')
class ImportarDatosCSV(View):
    def post(self, request):
        ruta_archivo_csv = request.POST.get('ruta_archivo_csv', '')
        if not ruta_archivo_csv:
            return JsonResponse({'error': 'Ruta del archivo CSV no proporcionada'}, status=400)
        try:
            with open(ruta_archivo_csv, 'r', encoding='latin-1') as archivo_csv:
                csv_reader = csv.DictReader(archivo_csv)
                for row in csv_reader:
                    nombre_pais = row['nombre']
                    Pais.objects.get_or_create(nombre=nombre_pais)
            return JsonResponse({'message': 'Importación exitosa'})
        except FileNotFoundError:
            return JsonResponse({'error': 'El archivo CSV no fue encontrado'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
class SubcompetenciasAPI(APIView):
    def get(self, request, format=None):
        # Calcular el conteo de respuestas para cada subcompetencia
        autocontrol_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(1, 4)) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=2).count()

        liderazgo_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(5, 10)) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        conciencia_valor_social_count = Autodiagnostico.objects.filter(
            (Q(pregunta__id__range=(11, 17)) | Q(pregunta__id__range=(18, 24))) & Q(respuesta__id__in=[4, 5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        innovacion_social_count = Autodiagnostico.objects.filter(
            Q(pregunta__id__range=(18,24)) & Q(respuesta__id__in=[4,5])
        ).values('usuario__id').annotate(conteo=Count('usuario__id')).filter(conteo__gte=4).count()

        # Construir la respuesta con los conteos de cada subcompetencia
        response_data = {
            'autocontrol': autocontrol_count,
            'liderazgo': liderazgo_count,
            'conciencia_valor_social': conciencia_valor_social_count,
            'innovacion_social': innovacion_social_count
        }

        return Response(response_data, status=status.HTTP_200_OK)
    

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

class ComprobarActividadCompletada(viewsets.ModelViewSet):
    def get(self, request, usuario_id):
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            #actividad = Actividad.objects.get(id=actividad_id)
            actividades = Actividad.objects.all()
            completado = Progreso.objects.filter(usuario=usuario).exists()
            data = {'id_actividad': actividades,
                'completado': completado,}
            
            completado_por_actividad = []
            
            for actividad in actividades:
                completado = Progreso.objects.filter(usuario=usuario, actividad=actividad).exists()
                actividad_json = {
                    "id": actividad.id,
                    "completado": completado
                }
                completado_por_actividad.append(actividad_json)

            return JsonResponse(completado_por_actividad, safe=False)
        
        except Usuario.DoesNotExist or Actividad.DoesNotExist:
            return Response({'error': 'Usuario o actividad no encontrados'}, status=400)

