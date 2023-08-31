from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
from django import forms
from api.models import Teacher

class MyForm(forms.Form):
    no_lista = forms.CharField(max_length=2)
    grupo = forms.CharField(max_length=2)

class SessionForm(forms.Form):
    session_id = forms.CharField(max_length=50)
    max_level1 = forms.IntegerField()
    max_level2 = forms.IntegerField()
    max_level3 = forms.IntegerField()
    level_enter = forms.IntegerField()
    #exit_at = forms.DateTimeField()

class TeacherForm(UserCreationForm):
    correo_escolar = forms.EmailField(required=True, label='Correo Escolar')


