from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import requests
from .models import Usuario, Administrador

""" class JSONAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        json_url = 'http://localhost:8000/Administradores/'

        try:
            response = requests.get(json_url)
            response.raise_for_status()
            json_data = response.json()
        except Exception as e:
            return None
        
        results = json_data.get('results', [])

        for user_data in results:
            if user_data.get('correo') == email and user_data.get('password') == password:
                user, created = User.objects.get_or_create(email=email)
                return user
        return None """

class JSONAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            admin = Administrador.objects.get(correo=email)

            if admin.password == password:
                return admin

        except Administrador.DoesNotExist:
            return None

""" class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        User = get_user_model()

        json_url = 'http://localhost:8000/Usuarios'

        try:
            response = requests.get(json_url)
            response.raise_for_status()
            json_data = response.json()
        except Exception as e:
            return None
        
        results = json_data.get('results', [])

        for user_data in results:
            if user_data.get('username') == username and user_data.get('password') == password:
                user, created = User.objects.get_or_create(username=username)
                return user
        return None """

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(username=username)

            if user.password == password:
                return user
        except Usuario.DoesNotExist:
            return None