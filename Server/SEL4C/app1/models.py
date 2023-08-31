from django.db import models

# Create your models here.

class Administrador(models.Model):
    correo = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    # userdata_id

class Usuario(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    progress_id = models.CharField(max_length=10)

class Progreso(models.Model):
    actividad_id = models.IntegerField()

class Actividad(models.Model):
    descripcion = models.CharField(max_length=50)
    entrega_id = models.IntegerField()

class Entrega(models.Model):
    file = models.CharField(max_length=50)
    tokens_assigned = models.IntegerChoices()

    


