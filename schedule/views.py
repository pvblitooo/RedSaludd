from rest_framework import viewsets, permissions
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes 
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from .models import Profesional, Asignacion, Box, Especialidad
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.middleware.csrf import get_token
import datetime
from .serializers import (
    ProfesionalSerializer, 
    AsignacionReadSerializer, 
    AsignacionWriteSerializer,
    BoxSerializer,
    EspecialidadSerializer 
)

class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all().order_by('nombre')
    serializer_class = EspecialidadSerializer
    permission_classes = [permissions.IsAuthenticated]

class BoxViewSet(viewsets.ModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [permissions.IsAuthenticated]

@login_required
def professionals_page(request):
    # Generamos el token CSRF para pasárselo al template
    csrf_token = get_token(request)
    context = {
        'csrf_token_value': csrf_token
    }
    return render(request, 'schedule/professionals.html', context)

def gestion_box_page(request):
    # Por ahora solo renderiza el template. Podríamos pasarle datos en el futuro.
    return render(request, 'gestion-box.html')

# Esta vista manejará automáticamente las acciones GET, POST, PUT, DELETE
class ProfesionalViewSet(viewsets.ModelViewSet):
    queryset = Profesional.objects.all().order_by('nombre') # Añadimos un orden por defecto
    serializer_class = ProfesionalSerializer
    permission_classes = [permissions.IsAuthenticated]

    # --- ASEGÚRATE DE QUE ESTA SECCIÓN ESTÉ ASÍ ---
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # Solo filtramos por 'especialidad'. 'piso' ha sido eliminado.
    filterset_fields = ['especialidad'] 
    
    # Solo buscamos por 'nombre'.
    search_fields = ['nombre']
    # ---------------------------------------------
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

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats_view(request):
    """
    Calcula estadísticas y devuelve las próximas citas dentro de un rango
    de los próximos 2 días.
    """
    now = timezone.localtime()
    today = now.date()
    current_time = now.time()

    # Calculamos la fecha límite (hoy + 2 días)
    fecha_limite = today + datetime.timedelta(days=2)

    # --- INICIO DE LA NUEVA LÓGICA DE CONSULTA ---
    
    # 1. Total de citas para hoy (esto no cambia)
    citas_hoy_count = Asignacion.objects.filter(fecha=today).count()

    # 2. Total de profesionales únicos con citas hoy (esto no cambia)
    profesionales_activos_count = Asignacion.objects.filter(fecha=today).values('profesional').distinct().count()

    # 3. Próximas citas dentro de los próximos 2 días
    proximas_citas_qs = Asignacion.objects.filter(
        # CONDICIÓN A: Citas para HOY, pero solo desde la hora actual en adelante
        Q(fecha=today, hora_inicio__gte=current_time) |
        
        # O... CONDICIÓN B: Citas para los próximos 2 días (mañana y pasado mañana)
        Q(fecha__gt=today, fecha__lte=fecha_limite)
    ).order_by('fecha', 'hora_inicio')[:5] # Ordenamos y tomamos las 5 primeras

    proximas_citas_serializer = AsignacionReadSerializer(proximas_citas_qs, many=True)

    data = {
        'citas_hoy': citas_hoy_count,
        'profesionales_activos_hoy': profesionales_activos_count,
        'proximas_citas': proximas_citas_serializer.data
    }
    
    return Response(data)

@login_required
def homepage_view(request):
    return render(request, 'index.html')

@login_required
def professional_detail_page(request, pk):
    try:
        profesional = Profesional.objects.get(pk=pk)
        # Aquí podríamos añadir más contexto, como las próximas citas de este profesional
        context = {
            'profesional': profesional
        }
        return render(request, 'schedule/professional_detail.html', context)
    except Profesional.DoesNotExist:
        # Manejar el caso de que no se encuentre el profesional
        from django.http import Http404
        raise Http404("Profesional no encontrado")

@login_required
def professionals_page(request):
    # Ahora renderiza desde la sub-carpeta para ser consistentes
    return render(request, 'schedule/professionals.html') 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def agenda_semanal_view(request):
    """
    Devuelve todas las asignaciones de un profesional para la semana actual.
    Espera un parámetro 'profesional_id' en la URL.
    """
    profesional_id = request.query_params.get('profesional_id')
    if not profesional_id:
        from rest_framework import status
        return Response({'error': 'profesional_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)

    # Calculamos el inicio y fin de la semana actual (Lunes a Domingo)
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)

    # Filtramos las asignaciones
    queryset = Asignacion.objects.filter(
        profesional_id=profesional_id,
        fecha__range=[start_of_week, end_of_week]
    ).order_by('fecha', 'hora_inicio')

    serializer = AsignacionReadSerializer(queryset, many=True)
    return Response(serializer.data)

@login_required
def agenda_semanal_page(request):
    return render(request, 'schedule/agenda_semanal.html')