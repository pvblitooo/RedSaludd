# Sistema de Gestión de Boxes - RedSalud

Este proyecto es una aplicación web interna desarrollada para RedSalud, diseñada para facilitar la gestión y visualización de la asignación de boxes médicos, los horarios de los profesionales y la agenda diaria de la clínica.

La aplicación permite a los administradores tener una visión clara y en tiempo real de la ocupación, agendar citas de forma interactiva y consultar la información de los profesionales registrados.

## ✨ Características Principales

* **Autenticación de Usuarios:** Sistema de inicio y cierre de sesión para proteger el acceso a la plataforma.
* **Dashboard de Inicio:** Una página principal que muestra un resumen de la actividad del día, incluyendo el número total de citas y profesionales activos, así como una tabla con la agenda completa del día ordenada por box.
* **Gestión de Box por Piso:** Una grilla visual e interactiva que muestra la disponibilidad horaria de todos los boxes, filtrada por piso y por fecha.
* **Creación, Edición y Eliminación de Citas:** Interfaz de modal para agendar nuevas citas en los horarios disponibles, y para modificar o eliminar citas existentes directamente desde la grilla.
* **Agenda Semanal por Profesional:** Una vista de calendario semanal que muestra todos los compromisos de un profesional específico, seleccionable desde un menú desplegable.
* **Lista de Profesionales:** Un listado completo de todos los profesionales, con filtros dinámicos por nombre y especialidad.
* **Detalles de Profesional:** Una ventana emergente (modal) para ver la información detallada de cada profesional sin salir de la página de la lista.

## 🛠️ Tecnologías Utilizadas

### Backend
* **Python 3**
* **Django** (Framework principal)
* **Django REST Framework** (Para la creación de la API)
* **django-filter** (Para facilitar los filtros en la API)

### Frontend
* **HTML5**
* **CSS3** (Estilos personalizados, Flexbox, CSS Grid)
* **JavaScript (ES6+)** (Vanilla JS para la interactividad, `fetch` para el consumo de la API)

### Base de Datos
* **SQLite** (Para desarrollo)
* (Recomendado migrar a **PostgreSQL** para producción)

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para poner en funcionamiento el proyecto en un entorno de desarrollo local.

**1. Instalar Requerimientos**
```bash
pip install django djangorestframework
pip install django-filter
```
**2. Clonar el Repositorio**
```bash
git clone https://github.com/pvblitooo/RedSaludd.git
cd RedSaludd
```
**3. Ejecutar App**
```bash
python manage.py runserver
```
