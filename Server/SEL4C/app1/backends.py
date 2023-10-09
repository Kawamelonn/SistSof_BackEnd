from typing import Any
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
import requests

class JSONAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        User = get_user_model()

        json_url = 'http://localhost:8000/Administradores'

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
        return None

class CustomUserBackend(ModelBackend):
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
        return None