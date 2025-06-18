
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProfesionalViewSet, 
    AsignacionViewSet, 
    BoxViewSet,
    agenda_semanal_view, 
    dashboard_stats_view,
    EspecialidadViewSet 
)

router = DefaultRouter()
router.register(r'profesionales', ProfesionalViewSet, basename='profesional')
router.register(r'asignaciones', AsignacionViewSet, basename='asignacion')
router.register(r'boxes', BoxViewSet, basename='box')
router.register(r'especialidades', EspecialidadViewSet, basename='especialidad')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard-stats/', dashboard_stats_view, name='dashboard-stats'),
    path('agenda-semanal/', agenda_semanal_view, name='agenda-semanal-api'),
]