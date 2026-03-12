# Bitácora de Cambios - Marzo 2026

## [11-03-2026 13:48:33] - Configuración Inicial del Entorno y Reglas
- Se crearon los archivos base para los flujos de trabajo del agente (`test_workflow.md`, `database_workflow.md`).
- Se estableció el perfil de `Clean Code Architect`.
- Se añadieron directrices para evitar subida de artefactos temporales en `.gitignore`.
- Se configuró la estructura de documentación y bitácoras para registrar las versiones subidas.

## [11-03-2026 14:08:04] - Núcleo Funcional (Backend FastAPI + Frontend Flet)
- Creado esquema Pydantic para `User` y modelos `SQLAlchemy`.
- Configurado servidor FastAPI asíncrono con base de datos SQLite asíncrona (`aiosqlite`).
- Creados endpoints `/login` y `/register`, modularizados en funciones reducidas para cumplir PEP 8.
- Configure seguridad modular con encriptación bcrypt en `security.py`.
- Generado archivo de dependencias `requirements.txt`.
- Creado cliente `ui.py` en Flet para autenticación con `httpx` apuntando a la API local.

## [11-03-2026 14:58:20] - Refactorización de Interfaz y Roles de Usuario
- Refactorización a Single Page Application (SPA) en Flet para evitar contracción de vistas en modo `WEB_BROWSER`.
- Cambio de clases Flet desaprobadas (`ft.View` y `ft.alignment.center`) por contenedores puros (`ft.Container`, `ft.Column`).
- Creada e integrada vista `RegisterView` con endpoint POST `/register` para inscripción de Aprendices.
- Simplificación del código de Flet, delegando estructura de layout nativa a los ejes `MainAxisAlignment` y `CrossAxisAlignment`.

## [11-03-2026 15:52:00] - Refactorización Estructural a Single Page App "Híbrida" (Flask + HTMX + Tailwind)
- **Migración a Flask**: Eliminado todo el stack asíncrono (FastAPI y Flet local). Establecido `app.py` central conteniendo las reglas de direccionamiento, adaptando una arquitectura _Monolito Flexible_.
- **Sincronización de Base de Datos**: Cambiada la conexión SQLite de `aiosqlite` genérico hacia el motor predeterminado y síncrono de _SQLAlchemy_, resolviendo bloqueos de hilos a través de context-managers (`with SessionLocal() as db`).
- **Web Security**: Descartado formato Bearer explícitamente y transición a Tokens _JWT_ entregados y protegidos bajo _Cookies Seguras HTTP-Only_.
- **Aesthetic Glassmorphism (UI)**: Renovación total a web tradicional mediante plantillas Jinja `/templates` potenciadas por **Tailwind CSS** para un aspecto oscuro _Neo-cyberpunk_ y destellos radiales/degradados. Funciones visuales estéticas programáticas en el nivel de XP en Barras.
- **Micro-interactividad (HTMX)**: Recreada la funcionalidad de "Unirse" de la tarjeta de aprendiz hacia módulos empleando directrices como `<hx-post>` en el front validando los Skills del Aprendiz en tiempo real.

## [12-03-2026 13:58:00] - Enriquecimiento del Dashboard y Lógica de Multiplicadores XP
- **Sistema de Información Didáctica**: Integrados iconos de información neón y modales con efecto *glassmorphism* que detallan roles y requisitos.
- **Habilidades de Supervivencia (Multiplicadores)**: Reestructurada la Matriz de Habilidades para separar habilidades Verticales (Especialidad) de Horizontales (Supervivencia).
- **Lógica de Multiplicador**: Implementada propiedad `xp_multiplier` en el modelo `User`. Las habilidades horizontales (Git, IA, SQL) ahora actúan como multiplicadores globales.
- **Mejoras en UI**: Nueva sección "Núcleo Técnico" y badges de "Rayo" en especialidades para indicar bonos activos.
- **Soporte IDE**: Configuración de `settings.json` para ignorar falsos positivos de validación en plantillas Jinja2/HTML.

## [12-03-2026 14:15:00] - Motor de Temas Dinámicos y Variables CSS
- **Arquitectura de Temas**: Migración total a variables CSS (`--bg-color`, `--accent-color`, etc.) en `base.html` para permitir personalización en tiempo real.
- **Temas Base**: Implementación de 4 temas predefinidos: Futuristic (Dark), Light (Clean), Warm (Desert) y Cold (Polar).
- **Interfaz de Selección**: Creado un Floating Action Button (FAB) con menú radial para cambiar temas y una paleta de micro-selección para el color de acento.
- **Persistencia con LocalStorage**: La preferencia del usuario se guarda localmente, manteniendo el tema elegido tras el inicio de sesión o recarga de página.
- **Micro-interactividad**: Añadida transición suave de 0.5s en cambios de tema y efectos de brillo dinámicos basados en el color de acento seleccionado.
