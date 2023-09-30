from django.db import models
# Create your models here.

class Entrega(models.Model):
    filename = models.CharField(max_length=50, null=True, blank=True, verbose_name='Título')
    file = models.CharField(max_length=50, null=True, blank=True, verbose_name='Archivo')

    def __str__ (self):
        return "{}".format(self.filename)

class Actividad(models.Model):
    titulo = models.CharField(default="",max_length=50)
    entrega = models.ForeignKey(Entrega, null=True, unique = True, blank=True, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.titulo)

class Usuario(models.Model):
    OPCIONES_GENERO = [
        ('Sin_especificar', 'Prefiero no decir'),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('No_binario', 'No binario'),
    ]
    nombre = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='Nombre Completo')
    genero = models.CharField(max_length=25,choices=OPCIONES_GENERO,default='Sin_especificar', verbose_name='Género')
    correo = models.CharField(max_length=50, null=True, blank=True, verbose_name='Correo')
    username = models.CharField(max_length=50, null=True, blank=True, verbose_name='Nombre de Usuario')
    password = models.CharField(max_length=50, null=True, blank=True, unique = True, verbose_name='Contraseña')

    def __str__ (self):
        return "{}".format(self.nombre)

class Pregunta(models.Model):
    tipo_pregunta = models.CharField(max_length=300, null=True, blank=True, unique=True, verbose_name='TipoPregunta')
    pregunta = models.CharField(max_length=300, null=True, blank=True, unique=True, verbose_name='Pregunta')

    def __str__ (self):
        return "{}".format(self.pregunta)
    
class Respuesta(models.Model):
    respuesta = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return "{}".format(self.respuesta)
    
    
class Autodiagnostico(models.Model):
    num_auto = models.PositiveIntegerField(default=0, verbose_name='Número de Autodiagnóstico')
    usuario = models.ForeignKey(Usuario, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, null=True, unique = True, blank=True, on_delete=models.CASCADE )


class Progreso(models.Model):
    usuario = models.ForeignKey(Usuario, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    autodiagnostico = models.ForeignKey(Autodiagnostico, null=True, unique = True, blank=True, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, null=True, unique = True, blank=True, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.usuario)

class Administrador(models.Model):
    correo = models.EmailField(default="admin@example.com", unique = True, max_length=50, verbose_name="Correo")
    password = models.CharField(max_length=50, unique = True, verbose_name='Contraseña')
    progreso = models.ForeignKey(Progreso, null=True, unique = True, blank=True, on_delete=models.CASCADE)

    def __str__ (self):
        return "{}".format(self.correo)

