from django.db import models

class Especialidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.nombre

class Profesional(models.Model):
    nombre = models.CharField(max_length=200)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True, blank=True)
    agenda_activa = models.BooleanField(default=True)
    def __str__(self): return self.nombre

class Box(models.Model):
    numero = models.CharField(max_length=10)
    piso = models.IntegerField()
    def __str__(self): return f"Box {self.numero} - Piso {self.piso}"

class Asignacion(models.Model):
    profesional = models.ForeignKey(Profesional, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    def __str__(self): return f"{self.profesional.nombre} en {self.box} a las {self.hora_inicio}"
