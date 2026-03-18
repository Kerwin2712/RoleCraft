# Bit谩cora de Cambios - Marzo 2026

## [11-03-2026 13:48:33] - Configuraci贸n Inicial del Entorno y Reglas
- Se crearon los archivos base para los flujos de trabajo del agente (`test_workflow.md`, `database_workflow.md`).
- Se estableci贸 el perfil de `Clean Code Architect`.
- Se a帽adieron directrices para evitar subida de artefactos temporales en `.gitignore`.
- Se configur贸 la estructura de documentaci贸n y bit谩coras para registrar las versiones subidas.

## [11-03-2026 14:08:04] - N煤cleo Funcional (Backend FastAPI + Frontend Flet)
- Creado esquema Pydantic para `User` y modelos `SQLAlchemy`.
- Configurado servidor FastAPI as铆ncrono con base de datos SQLite as铆ncrona (`aiosqlite`).
- Creados endpoints `/login` y `/register`, modularizados en funciones reducidas para cumplir PEP 8.
- Configure seguridad modular con encriptaci贸n bcrypt en `security.py`.
- Generado archivo de dependencias `requirements.txt`.
- Creado cliente `ui.py` en Flet para autenticaci贸n con `httpx` apuntando a la API local.

## [11-03-2026 14:58:20] - Refactorizaci贸n de Interfaz y Roles de Usuario
- Refactorizaci贸n a Single Page Application (SPA) en Flet para evitar contracci贸n de vistas en modo `WEB_BROWSER`.
- Cambio de clases Flet desaprobadas (`ft.View` y `ft.alignment.center`) por contenedores puros (`ft.Container`, `ft.Column`).
- Creada e integrada vista `RegisterView` con endpoint POST `/register` para inscripci贸n de Aprendices.
- Simplificaci贸n del c贸digo de Flet, delegando estructura de layout nativa a los ejes `MainAxisAlignment` y `CrossAxisAlignment`.

## [11-03-2026 15:52:00] - Refactorizaci贸n Estructural a Single Page App "H铆brida" (Flask + HTMX + Tailwind)
- **Migraci贸n a Flask**: Eliminado todo el stack as铆ncrono (FastAPI y Flet local). Establecido `app.py` central conteniendo las reglas de direccionamiento, adaptando una arquitectura _Monolito Flexible_.
- **Sincronizaci贸n de Base de Datos**: Cambiada la conexi贸n SQLite de `aiosqlite` gen茅rico hacia el motor predeterminado y s铆ncrono de _SQLAlchemy_, resolviendo bloqueos de hilos a trav茅s de context-managers (`with SessionLocal() as db`).
- **Web Security**: Descartado formato Bearer expl铆citamente y transici贸n a Tokens _JWT_ entregados y protegidos bajo _Cookies Seguras HTTP-Only_.
- **Aesthetic Glassmorphism (UI)**: Renovaci贸n total a web tradicional mediante plantillas Jinja `/templates` potenciadas por **Tailwind CSS** para un aspecto oscuro _Neo-cyberpunk_ y destellos radiales/degradados. Funciones visuales est茅ticas program谩ticas en el nivel de XP en Barras.
- **Micro-interactividad (HTMX)**: Recreada la funcionalidad de "Unirse" de la tarjeta de aprendiz hacia m贸dulos empleando directrices como `<hx-post>` en el front validando los Skills del Aprendiz en tiempo real.

## [12-03-2026 13:58:00] - Enriquecimiento del Dashboard y L贸gica de Multiplicadores XP
- **Sistema de Informaci贸n Did谩ctica**: Integrados iconos de informaci贸n ne贸n y modales con efecto *glassmorphism* que detallan roles y requisitos.
- **Habilidades de Supervivencia (Multiplicadores)**: Reestructurada la Matriz de Habilidades para separar habilidades Verticales (Especialidad) de Horizontales (Supervivencia).
- **L贸gica de Multiplicador**: Implementada propiedad `xp_multiplier` en el modelo `User`. Las habilidades horizontales (Git, IA, SQL) ahora act煤an como multiplicadores globales.
- **Mejoras en UI**: Nueva secci贸n "N煤cleo T茅cnico" y badges de "Rayo" en especialidades para indicar bonos activos.
- **Soporte IDE**: Configuraci贸n de `settings.json` para ignorar falsos positivos de validaci贸n en plantillas Jinja2/HTML.

## [12-03-2026 14:15:00] - Motor de Temas Din谩micos y Accesibilidad
- **Arquitectura de Temas**: Migraci贸n total a variables CSS (`--bg-color`, `--accent-color`, `--text-header`, etc.) para personalizaci贸n en tiempo real.
- **Optimizaci贸n de Accesibilidad**: 
    - Implementaci贸n de `color-mix` para generar brillos y fondos transl煤cidos adaptativos.
    - Sistema de Jerarqu铆a de Texto: Introducci贸n de `--text-header` y `--text-muted` para asegurar contraste en temas claros (negro pizarra) y oscuros.
- **Temas Base**: Implementaci贸n de 4 temas (Futuristic, Light, Warm, Cold) con transiciones suaves de 0.5s.
- **Interfaz de Selecci贸n**: Floating Action Button (FAB) con men煤 radial para temas y paleta de colores de acento con persistencia en `localStorage`.

## [12-03-2026 19:30:00] - Despliegue Oficial del Sistema de Onboarding
- **Recursos Oficiales**: Integraci贸n de videos de entrenamiento de VS Code (Official), Microsoft Developer, HolaMundo y Midudev.
- **UI de Misi贸n**: Redise帽o de la vista de m贸dulo con iframes estilizados mediante Glassmorphism y sombras ne贸n.
- **Seguridad y Reglas**: 
    - Implementaci贸n de la **Regla #13** en `.agent/rules.md` para control de despliegue manual.
    - A帽adidos enlaces externos seguros con `target="_blank"` y `rel="noopener noreferrer"`.
- **Backend Reforzado**: Correcci贸n de dependencias (`requests`) y optimizaci贸n de la l贸gica de validaci贸n t茅cnica local.

## 17 de Marzo de 2026 - Limpieza y Estabilizaci髇 de Evaluaci髇
- **feat/refactor**: Consolidaci髇 de archivos CSV de preguntas (preguntas_modulo_1.csv, preguntas_python.csv) en un 鷑ico archivo maestro llamado preguntas.csv.
- **fix**: Resoluci髇 de bucle infinito en avance de cola de preguntas al acertar en la evaluaci髇.
- **fix**: Correcci髇 del c醠culo y propagaci髇 del error 'Undefined XP' para dar soporte robusto al cliente IDE (Terminal) cuando el stock llega a 0.
- **refactor**: Limpieza de entorno eliminando temporales .pyc / __pycache__ y archivos scripts obsoletos (seed_modules.py, init_module1.py).

