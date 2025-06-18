from rest_framework import serializers
from .models import Profesional, Especialidad, Box, Asignacion

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']

class ProfesionalSerializer(serializers.ModelSerializer):
    # Para mostrar el nombre de la especialidad en lugar de solo su ID
    especialidad = EspecialidadSerializer(read_only=True)

    class Meta:
        model = Profesional
        fields = ['id', 'nombre', 'rut', 'correo', 'telefono', 'piso', 'agenda_activa', 'especialidad']

class AsignacionReadSerializer(serializers.ModelSerializer):
    profesional = ProfesionalSerializer(read_only=True)
    box = serializers.StringRelatedField(read_only=True) # Muestra "Box 401 - Piso 4"

    class Meta:
        model = Asignacion
        fields = '__all__'

# Serializer para ESCRIBIR datos (acepta IDs para crear/actualizar)
class AsignacionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asignacion
        fields = ['profesional', 'box', 'fecha', 'hora_inicio', 'hora_fin']

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['id', 'numero', 'piso']

class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = ['id', 'nombre']