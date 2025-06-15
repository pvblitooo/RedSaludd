
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoxViewSet, ProfesionalViewSet, AsignacionViewSet 

router = DefaultRouter()
router.register(r'profesionales', ProfesionalViewSet, basename='profesional')
router.register(r'asignaciones', AsignacionViewSet, basename='asignacion')
router.register(r'boxes', BoxViewSet, basename='box')

urlpatterns = [
    path('', include(router.urls)),
]