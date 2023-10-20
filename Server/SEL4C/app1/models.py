from django.db import models
from django.utils import timezone
# Create your models here.

class Actividad(models.Model):
    titulo = models.CharField(default="",max_length=50)

    def __str__ (self):
        return "{}".format(self.titulo)

class Institucion(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='Institución')

    def __str__ (self):
        return "{}".format(self.nombre)
    
class Pais(models.Model):
    nombre = models.CharField(max_length=100, null=True, blank=True, unique=True, verbose_name='País')

    def __str__ (self):
        return "{}".format(self.nombre)

class Usuario(models.Model):
    OPCIONES_GENERO = [
        ('Sin_especificar', 'Prefiero no decir'),
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('No_binario', 'No binario'),
    ]
    OPCIONES_GRADO = [
        ('Pregrado', 'Pregrado(licenciatura, profesional, universidad, grado)'),
        ('Posgrado', 'Posgrado(maestría, doctorado)'),
        ('Educación continua', 'Educación continua'),
    ]
    OPCIONES_DISCIPLINA = [
        ('Ingeniería y Ciencias', 'Ingeniería y Ciencias'),
        ('Humanidades y Educación', 'Humanidades y Educación'),
        ('Ciencias Sociales', 'Ciencias Sociales'),
        ('Ciencias de la Salud', 'Ciencias de la Salud'),
        ('Arquitectura, Arte y Diseño', 'Arquitectura, Arte y Diseño'),
        ('Negocios', 'Negocios'),
    ]
    nombre = models.CharField(max_length=50, null=True, blank=True, unique=True, verbose_name='Nombre Completo')
    genero = models.CharField(max_length=50,choices=OPCIONES_GENERO,default='Sin_especificar', verbose_name='Género')
    grado = models.CharField(max_length=60,choices=OPCIONES_GRADO,default='Pregrado', verbose_name='Grado de Estudiso')
    disciplina = models.CharField(max_length=60,choices=OPCIONES_DISCIPLINA,default='Ingeniería y Ciencias', verbose_name='Disciplina de Interés')
    pais = models.ForeignKey(Pais, null=True, blank=True, on_delete=models.CASCADE)
    institucion = models.ForeignKey(Institucion, null=True, blank=True, on_delete=models.CASCADE)
    correo = models.CharField(max_length=50, null=True, unique=True, blank=True, verbose_name='Correo')
    username = models.CharField(max_length=50, null=True, unique=True, blank=True, verbose_name='Nombre de Usuario')
    password = models.CharField(max_length=50, null=True, blank=True, verbose_name='Contraseña')

    def __str__ (self):
        return "{}".format(self.nombre)

class Pregunta(models.Model):
    tipo_pregunta = models.CharField(max_length=300, null=True, blank=True, verbose_name='Tipo Pregunta')
    pregunta = models.CharField(max_length=300, null=True, blank=True, unique=True, verbose_name='Pregunta')

    def __str__ (self):
        return "{}".format(self.pregunta)
    
class Respuesta(models.Model):
    respuesta = models.PositiveIntegerField(default=1, verbose_name='Respuesta')

    def __str__(self) -> str:
        return "{}".format(self.respuesta)
    
class Autodiagnostico(models.Model):
    OPCIONES_COMPETENCIA = [
        ('Autocontrol', 'Autocontrol'),
        ('Liderazgo', 'Liderazgo'),
        ('Conciencia y valor social', 'Conciencia y valor social'),
        ('Innovación social y sostenibilidad financiera', 'Innovación social y sostenibilidad financiera'),
    ]
    num_auto = models.PositiveIntegerField(default=0, verbose_name='Número de Autodiagnóstico')
    usuario = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, null=True, blank=True, on_delete=models.CASCADE)
    respuesta = models.ForeignKey(Respuesta, null=True, blank=True, on_delete=models.CASCADE)
    competencia = models.CharField(max_length=60,choices=OPCIONES_COMPETENCIA, default='Autocontrol', verbose_name='Competencia que evalúa')
    completada = models.BooleanField(default=False)

class Progreso(models.Model):

    usuario = models.ForeignKey(Usuario, null=True, unique = False, blank=True, on_delete=models.CASCADE)
    actividad = models.ForeignKey(Actividad, null=True, unique = False, blank=True, on_delete=models.CASCADE)
    filename = models.CharField(max_length=50, null=True, blank=True, verbose_name='Título')
    file = models.FileField(default='', upload_to='archivos/')
    completado = models.BooleanField(default=False, verbose_name='¿Completado?')

    def __str__ (self):
        return "{}".format(self.usuario)

class Administrador(models.Model):
    username = models.CharField(max_length=50, null=True, unique=True, blank=True, verbose_name='Nombre de Usuario')
    correo = models.EmailField(default="admin@example.com", unique = True, max_length=50, verbose_name="Correo")
    password = models.CharField(max_length=50, unique = True, verbose_name='Contraseña')
    last_login = models.DateTimeField(default=timezone.now, verbose_name='Last Login')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.username = str(Administrador.objects.count() + 1)
        super().save(*args, **kwargs)

    def __str__ (self):
        return "{}".format(self.correo)

