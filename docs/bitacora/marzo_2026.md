# Bitácora de Cambios - Marzo 2026

## 24 de Marzo de 2026 - Actualización de Portafolio e Identidad Visual
- **docs**: Rediseño completo del `README.md` estructurándolo profesionalmente para uso como portafolio en GitHub (Arquitectura, Features, Instalación).
- **docs**: Creación y formateo del Manual de Identidad Visual y UX (`ui_graphics.md`), definiendo la estética Neo-Cyberpunk, componentes clave y reglas de UX.
- **feat/ui**: Rediseño inmersivo completo de  `dashboard_aprendiz.html` implementando la arquitectura visual descrita en el manual. Se reemplazaron colores fijos oscuros por variables modulares que respetan el contraste en el modo claro. Se añadió la Terminal Interactiva HTMX de asignación de roles y la barra superior de status.

## 20 de Marzo de 2026 - Rediseño del Módulo 1 y Filtro de Entorno
- **feat**: Implementación del Módulo 1 como "Misión de Configuración de Entorno" (VSCode, Python, Antigravity).
- **feat**: Nueva ruta `/tutorial/1` con guía visual premium para la preparación de la estación de trabajo.
- **feat**: Renovación total del banco de preguntas del Módulo 1 en `preguntas.csv` con enfoque técnico/entorno.
- **fix**: Resolución global de errores `DetachedInstanceError` mediante la reestructuración del ciclo de vida de las sesiones en las rutas de evaluación y módulos.
- **fix**: Resolución de `NameError: status is not defined` en la ruta `/entrenamiento_detalle/` causado por un error de edición en la gestión de sesiones.
- **refactor**: Optimización del botón "Test Diagnóstico" para direccionamiento inteligente hacia la prueba de programación.



## 19 de Marzo de 2026 - Restauración de Habilidades y Acceso Directo a Test
- **feat**: Restauración de la Matriz de Habilidades completa en `dashboard_aprendiz.html` (6 habilidades: Backend, Frontend, PM, Git, IA, SQL).
- **feat**: Mejora de interactividad en el dashboard permitiendo abrir modales de información al hacer clic en las barras de habilidades.
- **fix**: Deshabilitado el bloqueo de 24 horas (`last_exam_attempt`) en `app.py` para permitir el acceso inmediato e ininterrumpido al Test Diagnóstico/Inflexión.
- **docs**: Actualización de la bitácora de marzo y validación visual de los cambios mediante pruebas en navegador.

## 18 de Marzo de 2026 - Integración de Entrenamiento y Energía Infinita
- **feat**: Rediseño del Dashboard de Aprendiz para integrar el **Centro de Entrenamiento** en el cuerpo superior de la página (ancho completo), mejorando la accesibilidad y el flujo de navegación.
- **fix**: Resolución del bloqueo de 24 horas (`last_exam_attempt`) y depleción de energía para el usuario **Kerwin Quintero**, garantizando acceso inmediato e ininterrumpido al Test Diagnóstico.
- **refactor**: Limpieza de código redundante en `dashboard_aprendiz.html` y remapeo de botones en la barra lateral.

## 17 de Marzo de 2026 - Limpieza y Estabilización de Evaluación
- **feat/refactor**: Consolidación de archivos CSV de preguntas (preguntas_modulo_1.csv, preguntas_python.csv) en un único archivo maestro llamado preguntas.csv.
- **fix**: Resolución de bucle infinito en avance de cola de preguntas al acertar en la evaluación.
- **fix**: Corrección del cálculo y propagación del error 'Undefined XP' para dar soporte robusto al cliente IDE (Terminal) cuando el stock llega a 0.
- **refactor**: Limpieza de entorno eliminando temporales .pyc / __pycache__ y archivos scripts obsoletos (seed_modules.py, init_module1.py).

## [12-03-2026 19:30:00] - Despliegue Oficial del Sistema de Onboarding
- **Recursos Oficiales**: Integración de videos de entrenamiento de VS Code (Official), Microsoft Developer, HolaMundo y Midudev.
- **UI de Misión**: Rediseño de la vista de módulo con iframes estilizados mediante Glassmorphism y sombras neón.
- **Seguridad y Reglas**: 
    - Implementación de la **Regla #13** en `.agent/rules.md` para control de despliegue manual.
    - Añadidos enlaces externos seguros con `target="_blank"` y `rel="noopener noreferrer"`.
- **Backend Reforzado**: Corrección de dependencias (`requests`) y optimización de la lógica de validación técnica local.

## [12-03-2026 14:15:00] - Motor de Temas Dinámicos y Accesibilidad
- **Arquitectura de Temas**: Migración total a variables CSS (`--bg-color`, `--accent-color`, `--text-header`, etc.) para personalización en tiempo real.
- **Optimización de Accesibilidad**: 
    - Implementación de `color-mix` para generar brillos y fondos translúcidos adaptativos.
    - Sistema de Jerarquía de Texto: Introducción de `--text-header` y `--text-muted` para asegurar contraste en temas claros (negro pizarra) y oscuros.
- **Temas Base**: Implementación de 4 temas (Futuristic, Light, Warm, Cold) con transiciones suaves de 0.5s.
- **Interfaz de Selección**: Floating Action Button (FAB) con menú radial para temas y paleta de colores de acento con persistencia en `localStorage`.

## [12-03-2026 13:58:00] - Enriquecimiento del Dashboard y Lógica de Multiplicadores XP
- **Sistema de Información Didáctica**: Integrados iconos de información neón y modales con efecto *glassmorphism* que detallan roles y requisitos.
- **Habilidades de Supervivencia (Multiplicadores)**: Reestructurada la Matriz de Habilidades para separar habilidades Verticales (Especialidad) de Horizontales (Supervivencia).
- **Lógica de Multiplicador**: Implementada propiedad `xp_multiplier` en el modelo `User`. Las habilidades horizontales (Git, IA, SQL) ahora actúan como multiplicadores globales.
- **Mejoras en UI**: Nueva sección "Núcleo Técnico" y badges de "Rayo" en especialidades para indicar bonos activos.
- **Soporte IDE**: Configuración de `settings.json` para ignorar falsos positivos de validación en plantillas Jinja2/HTML.

## [11-03-2026 15:52:00] - Refactorización Estructural a Single Page App "Híbrida" (Flask + HTMX + Tailwind)
- **Migración a Flask**: Eliminado todo el stack asíncrono (FastAPI y Flet local). Establecido `app.py` central conteniendo las reglas de direccionamiento, adaptando una arquitectura _Monolito Flexible_.
- **Sincronización de Base de Datos**: Cambiada la conexión SQLite de `aiosqlite` genérico hacia el motor predeterminado y síncrono de _SQLAlchemy_, resolviendo bloqueos de hilos a través de context-managers (`with SessionLocal() as db`).
- **Web Security**: Descartado formato Bearer explícitamente y transición a Tokens _JWT_ entregados y protegidos bajo _Cookies Seguras HTTP-Only_.
- **Aesthetic Glassmorphism (UI)**: Renovación total a web tradicional mediante plantillas Jinja `/templates` potenciadas por **Tailwind CSS** para un aspecto oscuro _Neo-cyberpunk_ y destellos radiales/degradados. Funciones visuales estéticas programáticas en el nivel de XP en Barras.
- **Micro-interactividad (HTMX)**: Recreada la funcionalidad de "Unirse" de la tarjeta de aprendiz hacia módulos empleando directrices como `<hx-post>` en el front validando los Skills del Aprendiz en tiempo real.

## [11-03-2026 14:58:20] - Refactorización de Interfaz y Roles de Usuario
- **Refactorización a Single Page Application (SPA) en Flet para evitar contracción de vistas en modo `WEB_BROWSER`.**
- **Cambio de clases Flet desaprobadas (`ft.View` y `ft.alignment.center`) por contenedores puros (`ft.Container`, `ft.Column`).**
- **Creada e integrada vista `RegisterView` con endpoint POST `/register` para inscripción de Aprendices.**
- **Simplificación del código de Flet, delegando estructura de layout nativa a los ejes `MainAxisAlignment` y `CrossAxisAlignment`.**

## [11-03-2026 14:08:04] - Núcleo Funcional (Backend FastAPI + Frontend Flet)
- **Creado esquema Pydantic para `User` y modelos `SQLAlchemy`.**
- **Configurado servidor FastAPI asíncrono con base de datos SQLite asíncrona (`aiosqlite`).**
- **Creados endpoints `/login` y `/register`, modularizados en funciones reducidas para cumplir PEP 8.**
- **Configure seguridad modular con encriptación bcrypt en `security.py`.**
- **Generado archivo de dependencias `requirements.txt`.**
- **Creado cliente `ui.py` en Flet para autenticación con `httpx` apuntando a la API local.**

## [11-03-2026 13:48:33] - Configuración Inicial del Entorno y Reglas
- **Se crearon los archivos base para los flujos de trabajo del agente (`test_workflow.md`, `database_workflow.md`).**
- **Se estableció el perfil de `Clean Code Architect`.**
- **Se añadieron directrices para evitar subida de artefactos temporales en `.gitignore`.**
- **Se configuró la estructura de documentación y bitácoras para registrar las versiones subidas.**
