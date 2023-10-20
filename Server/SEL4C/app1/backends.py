from typing import Any
from django.contrib.auth.backends import ModelBackend
from .models import Usuario, Administrador

class JSONAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            admin = Administrador.objects.get(correo=email)

            if admin.password == password:
                return admin

        except Administrador.DoesNotExist:
            return None

class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Usuario.objects.get(username=username)

            if user.password == password:
                return user
        except Usuario.DoesNotExist:
            return None