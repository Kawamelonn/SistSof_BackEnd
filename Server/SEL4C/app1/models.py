from django.db import models


# Create your models here.

class Entrega(models.Model):
    #entreda_id = models.CharField(max_length=50, null=True, blank=True)
    file_name = models.CharField(max_length=50)

    def __str__ (self):
        return "{}".format(self.file_name)

class Actividad(models.Model):
    titulo = models.CharField(default="",max_length=50)
    descripcion = models.CharField(default="", max_length=350)
    entrega = models.ForeignKey(Entrega, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    tokens = models.IntegerField(default=-1)

    def __str__ (self):
        return "{} - Tokens: {}".format(self.titulo, self.tokens)

class Usuario(models.Model):
    username = models.CharField(max_length=50, unique = True, verbose_name='Usuario')
    password = models.CharField(max_length=50, unique = True, verbose_name='Contraseña')

    def __str__ (self):
        return "{}".format(self.username)

class Progreso(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, null=True, unique = True, blank=True, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.usuario)

class Administrador(models.Model):
    correo = models.EmailField(default="admin@example.com", unique = True, max_length=50, verbose_name="Correo Admin")
    password = models.CharField(max_length=50, unique = True, verbose_name='Contraseña')
    progreso = models.ForeignKey(Progreso, null=True, unique = True, blank=True, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.correo)
