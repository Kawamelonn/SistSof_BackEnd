from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views import View
from .models import *
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from django.db.models import Max
import json
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.utils import timezone


# Create your views here.
class GroupView(View):

    def get(self, request):
        groups = list(Grupo.objects.values())
        if len(groups) > 0:
            datos = {
                "message": "Success", 
                "groups": groups
            }
        else:
            datos = {
                "mesage": "No groups found"
            }
        return JsonResponse(datos)
    
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class PlayerView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        players_values = list(Player.objects.values('id', 'no_lista', 'grupo__grupo_id'))
        players_list = []
        for player_values in players_values:
            grupo_id = player_values.pop('grupo__grupo_id')
            player = {
                'id': player_values['id'],
                'no_lista': player_values['no_lista'],
                'grupo_id': grupo_id,
                'history': list(Session.objects.filter(player=player_values['id']).values())
            }
            players_list.append(player)
        if len(players_list) > 0:
            datos = {
            "player": players_list
        }
        else:
            datos = {
                "message": "No players found"
            }
        return JsonResponse(datos)
    
    def post(self, request):
        form = MyForm(request.POST)
        if form.is_valid():
            no_lista = form.cleaned_data['no_lista']
            grupo = form.cleaned_data['grupo']
            group = Grupo.objects.get(grupo_id=grupo)
            players_values = list(Player.objects.filter(no_lista=no_lista, grupo=group).values('id', 'no_lista', 'grupo__grupo_id'))
            players_list = []
            for player_values in players_values:
                grupo_id = player_values.pop('grupo__grupo_id')
                player = {
                    'id': player_values['id'],
                    'no_lista': player_values['no_lista'],
                    'grupo_id': grupo_id,
                    'history': list(Session.objects.filter(player=player_values['id']).values())
                }
                players_list.append(player)
                if len(players_list) > 0:
                    datos = {
                        "player": players_list
                    }
                else:
                    datos = {
                        "message": "No players found"
                    }
                return JsonResponse(datos)
        else:
            return JsonResponse({'error': 'Formulario no válido'})


    def put(self, request):
        pass

    def delete(self, request):
        pass

class PlayerListView(ListView):
    model = Player
    template_name = 'api/players.html'
    context_object_name = 'players'

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'api/player.html'
    context_object_name = 'player'

class PlayerCreateView(CreateView):
    model = Player
    template_name = 'api/create_edit.html'
    fields = ['no_lista', 'grupo']
    success_url = '/players_list'

class PlayerUpdateView(UpdateView):
    model = Player
    template_name = 'api/create_edit.html'
    fields = ['no_lista', 'grupo']
    success_url = '/players_list'

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'api/confirm.html'
    success_url = '/players_list'

class GrupoListView(ListView):
    model = Grupo
    template_name = 'api/groups.html'
    context_object_name = 'groups'

class GrupoDetailView(DetailView):
    model = Grupo
    template_name = 'api/group.html'
    context_object_name = 'group'

class GrupoCreateView(CreateView):
    model = Grupo
    template_name = 'api/create_editG.html'
    fields = ['grupo_id', 'teacher']
    success_url = '/groups_list'

class GrupoUpdateView(UpdateView):
    model = Grupo
    template_name = 'api/create_editG.html'
    fields = ['grupo_id', 'teacher']
    success_url = '/groups_list'

class GrupoDeleteView(DeleteView):
    model = Grupo
    template_name = 'api/confirmG.html'
    success_url = '/groups_list'

def home(request):
    return render(request, "api/home.html")
        
class TeacherView(View):

    def get(self, request):
        teachers = list(Teacher.objects.values())
        if len(teachers) > 0:
            datos = {
                "message": "Success", 
                "teachers": teachers
            }
        else:
            datos = {
                "mesage": "No teachers found"
            }
        return JsonResponse(datos)
    
    def post(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

class TeacherListView(ListView):
    model = Teacher
    template_name = 'api/teachers.html'
    context_object_name = 'teachers'

class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'api/teacher.html'
    context_object_name = 'teacher'

class TeacherCreateView(CreateView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    model = Teacher
    template_name = 'api/createT.html'
    fields = ['correo_escolar', 'username', 'password']
    success_url = '/teacher/home'

class TeacherUpdateView(UpdateView):
    model = Teacher
    template_name = 'api/editT.html'
    fields = ['correo_escolar', 'username', 'password']
    success_url = '/teachers_list'

class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'api/confirmT.html'
    success_url = '/teachers_list'


class SessionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        sessions = list(Session.objects.values())
        if len(sessions) > 0:
            datos = {
                "message": "Success", 
                "sessions": sessions
            }
        else:
            datos = {
                "message": "No sessions found"
            }
        return JsonResponse(datos)
    
    def post(self, request):
        no_lista = request.POST["no_lista"]
        print(no_lista)
        grupo = request.POST["grupo"]
        print(grupo)
        group = Grupo.objects.get(grupo_id=grupo)
        player = Player.objects.get(no_lista = no_lista, grupo=group)
        num_session = request.POST["num_session"]
        print(num_session)
        try:
            session = Session.objects.get(player=player, num_session=num_session)
            num_level = request.POST["level_enter_id"]
            level_enter = Level.objects.get(num_level=num_level)
            session.level_enter = level_enter
            session.exit_at = timezone.now()
            level1 = Level.objects.get(num_level=1)
            score1 = Score.objects.get(session=session, level=level1)
            score1.points = request.POST["score_1"]
            print(score1.points)
            score1.mistakes = request.POST["incorrectas"]
            print(score1.mistakes)
            score1.time = request.POST["time1"]
            print(score1.time)
            score1.save()
            level2 = Level.objects.get(num_level=2)
            score2 = Score.objects.get(session=session, level=level2)
            score2.points = request.POST["score_2"]
            score2.mistakes = request.POST["incorrectas_lvl2"]
            score2.time = request.POST["time2"]
            score2.save()
            level3 = Level.objects.get(num_level=3)
            score3 = Score.objects.get(session=session, level=level3)
            score3.points = request.POST["score_3"]
            score3.mistakes = request.POST["incorrectas_lvl3"]
            score3.time = request.POST["time3"]
            score3.save()
            session.save()

            datos = {
                "message": "Success"
            }

        except Session.DoesNotExist:
            datos = {
                "message": "Session not found"
            }
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass
    
class ScoreView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        scores_values = list(Score.objects.values('id', 'points', 'mistakes', 'time', 'session__num_session', 'session__player__no_lista', 'session__player__grupo__grupo_id', 'level__num_level'))
        scores_list = []
        for score_values in scores_values:
            num_session = score_values.pop('session__num_session')
            no_lista = score_values.pop('session__player__no_lista')
            grupo_id = score_values.pop('session__player__grupo__grupo_id')
            num_level = score_values.pop('level__num_level')
            score = {
                'id': score_values['id'],
                'grupo_id': grupo_id,
                'no_lista': no_lista,
                'num_session': num_session,
                'num_level': num_level,
                'points': score_values['points'],
                'mistakes': score_values['mistakes'],
                'time': score_values['time']
            }
            scores_list.append(score)
        if len(scores_list) > 0:
            datos = {
                "scores": scores_list
            }
        else:
            datos = {
                "message": "No scores found"
            }
        return JsonResponse(datos)
    
    def post(self, request):
        no_lista = request.POST['no_lista']
        grupo = request.POST['grupo']
        group = Grupo.objects.get(grupo_id=grupo)
        player = Player.objects.get(no_lista=no_lista, grupo=group)
        session = Session.objects.get(player=player)
        scores_list = list(Score.objects.filter(session=session).values())
        if len(scores_list) > 0:
            datos = {
                "id": player.id,
                "no_lista": no_lista,
                "grupo_id": grupo,
                "history": scores_list
            }
        else:
            datos = {
                "message": "No scores found"
            }
        return JsonResponse(datos)

    def put(self, request):
        pass

    def delete(self, request):
        pass
    
# Vistas con relación al DashBoard

def index(request):
    level1 = Level.objects.get(num_level=1)
    max_score1 = level1.max_score
    level2 = Level.objects.get(num_level=2)
    max_score2 = level2.max_score
    level3 = Level.objects.get(num_level=3)
    max_score3 = level3.max_score
    ctx = {'max_score1': max_score1, 'max_score2': max_score2, 'max_score3': max_score3}
    return render(request, "api/index.html", ctx)

def chart(request, pk):
    level1 = Level.objects.get(num_level=1)
    max_score1 = level1.max_score
    level2 = Level.objects.get(num_level=2)
    max_score2 = level2.max_score
    level3 = Level.objects.get(num_level=3)
    max_score3 = level3.max_score
    grupo = Grupo.objects.get(id=pk)
    players = list(Player.objects.filter(grupo=grupo))
    ctx = {'max_score1': max_score1, 'max_score2': max_score2, 'max_score3': max_score3, 'grupo': grupo, 'players': players}
    return render(request, "api/chart.html", ctx)

def player_chart(request, pk):
    player = Player.objects.get(id = pk)
    sesion = Session.objects.get(player=player)
    score1 = Score.objects.get(session=sesion, level=Level.objects.get(num_level=1))
    score2 = Score.objects.get(session=sesion, level=Level.objects.get(num_level=2))
    score3 = Score.objects.get(session=sesion, level=Level.objects.get(num_level=3))
    ctx = {'player': player, 'sesiones':sesion, 'score1':score1.points, 'score2':score2.points, 'score3':score3.points}
    return render(request, 'api/player_chart.html', ctx)


def Gallery(request):
    return render(request, 'api/photoGallery.html')

def adminHome(request):
    return render(request, 'api/admin-home.html')

def adminAfterLogin(request):
    groups = Grupo.objects.all()
    ctx = {"grupos": groups}
    return render(request, 'api/admin-a_login.html', ctx)

def teacherHome(request):
    return render(request, 'api/teacher-home.html')

def teacherAfterLogin(request):
    groups = Grupo.objects.all()
    ctx = {"grupos": groups}
    return render(request, 'api/teacher-a_login.html', ctx)

def playersTView(request):
    return render(request, 'api/players-T_view.html')

def auth(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('administration/logged_in/')
        else:
            messages.error(request, ("Usuario o contraseña incorrectas"))
            return redirect('authentication') 
    return render(request, "api/authentication.html")

def register_user(request):
    if(request.method=="POST"):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, ("Usuario creado exitosamente"))
                return redirect('admin-a_login')
            else:
                messages.error(request, ("Error al crear usuario"))
                return redirect('admin-home')
        else:
            return render(request, 'api/admin-register.html', {"form":form})
    else:
        form = UserCreationForm()
        return render(request, 'api/admin-register.html', {"form":form})

def logout_user(request):
    logout(request)
    messages.success(request, ("Sesión Finalizada Correctamente"))
    return redirect('home')

@method_decorator(csrf_exempt)
def authT(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('teacher/logged_in/')
        else:
            messages.error(request, ("Usuario o contraseña incorrectas"))
            return redirect('authenticationT') 
    return render(request, "api/authenticationT.html")

def logout_teacher(request):
    logout(request)
    messages.success(request, ("-Sesión Finalizada con Éxito-"))
    return redirect('home')

def log(request, pk):
    grupo = Grupo.objects.get(id=pk)
    sesiones = list(Session.objects.filter(player__grupo=grupo).values())
    return JsonResponse(sesiones, safe=False)

def scoresp(request, pk):
    player = Player.objects.get(id=pk)
    sesion = Session.objects.get(player=player, num_session = 0)
    scores = list(Score.objects.filter(session=sesion).order_by('level_id').values())
    return JsonResponse(scores, safe=False)


