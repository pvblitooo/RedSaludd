from rest_framework import viewsets, permissions
from django.contrib.auth.decorators import login_required
from .models import Profesional, Asignacion, Box
from django.shortcuts import render
from .serializers import (
    ProfesionalSerializer, 
    AsignacionReadSerializer, 
    AsignacionWriteSerializer,
    BoxSerializer 
)

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated]

def professionals_page(request):
    return render(request, 'professionals.html')

def gestion_box_page(request):
    # Por ahora solo renderiza el template. Podríamos pasarle datos en el futuro.
    return render(request, 'gestion-box.html')

# Esta vista manejará automáticamente las acciones GET, POST, PUT, DELETE
class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all()
    serializer_class = ProfesionalSerializer
    permission_classes = [permissions.IsAuthenticated]

class AsignacionViewSet(viewsets.ModelViewSet):
    # Ya no definimos un serializer_class aquí...

    def get_serializer_class(self):
        # Si la acción es 'create', 'update' o 'partial_update', usa el serializer de escritura.
        if self.action in ['create', 'update', 'partial_update']:
            return AsignacionWriteSerializer
        # Para cualquier otra acción ('list', 'retrieve'), usa el de lectura.
        return AsignacionReadSerializer

    # ... (tu función get_queryset no cambia) ...
    def get_queryset(self):
        """
        Esta vista filtra las asignaciones por los parámetros 'piso' y 'fecha'
        enviados en la URL.
        """
        # Empezamos con todas las asignaciones
        queryset = Asignacion.objects.all().order_by('hora_inicio')
        
        # Obtenemos los parámetros de la URL (ej: /api/asignaciones/?piso=4)
        piso = self.request.query_params.get('piso')
        fecha = self.request.query_params.get('fecha')
        
        # Si el parámetro 'piso' existe, filtramos el queryset
        if piso: 
            queryset = queryset.filter(box__piso=piso)
    
        if fecha:
            queryset = queryset.filter(fecha=fecha)
        return queryset
    
@login_required # <-- Añade este decorador
def professionals_page(request):
    return render(request, 'professionals.html')

@login_required # <-- Añade este decorador
def gestion_box_page(request):
    return render(request, 'gestion-box.html')