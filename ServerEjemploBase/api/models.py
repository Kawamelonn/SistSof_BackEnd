from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User


class Teacher(models.Model):
    correo_escolar = models.EmailField(default="profesor@example.com", unique = True, max_length=50, verbose_name='Correo Escolar')
    username = models.CharField(max_length=50, unique = True, verbose_name='Usuario')
    password = models.CharField(max_length=50, unique = True, verbose_name='Contraseña')

    def __str__ (self):
        return "{}".format(self.username)
    
def create_user(sender, instance, created, **kwargs):
        if created:
            User.objects.create_user(
                username=instance.username,
                email=instance.correo_escolar,
                password=instance.password,
            )

def delete_user(sender, instance, **kwargs):
        try:
            user = User.objects.get(username=instance.username)
            user.delete()
        except User.DoesNotExist:
            pass
    
post_save.connect(create_user, sender=Teacher)
post_delete.connect(delete_user, sender=Teacher)

class Grupo(models.Model):
    grupo_id = models.CharField(max_length=50, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, null=True, unique = True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey

    def __str__ (self):
        return "{}".format(self.grupo_id)

class Player(models.Model):
    no_lista = models.PositiveIntegerField(null=True, blank=True, verbose_name='Número de lista')
    grupo = models.ForeignKey(Grupo, null=True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey
    
    def __str__ (self):
        return "No. lista: {} - {}".format(self.no_lista, self.grupo)

class Level(models.Model):
    num_level = models.PositiveIntegerField(null=True, blank=True, unique = True, verbose_name='Level')
    max_score = models.PositiveIntegerField(null=True, blank=True, verbose_name='MAX Score')

    def __str__ (self):
        return "Level: {}".format(self.num_level)

class Session(models.Model):
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey
    num_session = models.PositiveIntegerField(default=0)
    enter_at = models.DateTimeField(default=timezone.now, null=True, blank=True, verbose_name='Ingreso')
    exit_at = models.DateTimeField(null=True, blank=True, verbose_name='Fin')
    level_enter = models.ForeignKey(Level, null=True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey

    def __str__ (self):
        return "Sesión: {}, {}".format(self.num_session, self.player)

@receiver(post_save, sender=Player)
def create_default_session(sender, instance, created, **kwargs):
    if created:
        level = Level.objects.first()
        session = Session.objects.create(player=instance, num_session=0, level_enter=level)


class Score(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey
    level = models.ForeignKey(Level, null=True, blank=True, on_delete=models.CASCADE) # Agregar ForeignKey
    points = models.PositiveIntegerField(default=0)
    mistakes = models.IntegerField(null=True, blank=True, default=0)
    time = models.IntegerField(default=0)

    def __str__ (self):
        return "{}, {} - Points: {}".format(self.session, self.level, self.points)

@receiver(post_save, sender=Session)
def create_default_scores(sender, instance, created, **kwargs):
    if created:
        levels = Level.objects.all()
        for level in levels:
            score = Score.objects.create(session=instance, level=level, points=0, mistakes=0, time=0)


