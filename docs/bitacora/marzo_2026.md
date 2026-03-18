# BitÃ¡cora de Cambios - Marzo 2026

## [11-03-2026 13:48:33] - ConfiguraciÃ³n Inicial del Entorno y Reglas
- Se crearon los archivos base para los flujos de trabajo del agente (`test_workflow.md`, `database_workflow.md`).
- Se estableciÃ³ el perfil de `Clean Code Architect`.
- Se aÃ±adieron directrices para evitar subida de artefactos temporales en `.gitignore`.
- Se configurÃ³ la estructura de documentaciÃ³n y bitÃ¡coras para registrar las versiones subidas.

## [11-03-2026 14:08:04] - NÃºcleo Funcional (Backend FastAPI + Frontend Flet)
- Creado esquema Pydantic para `User` y modelos `SQLAlchemy`.
- Configurado servidor FastAPI asÃ­ncrono con base de datos SQLite asÃ­ncrona (`aiosqlite`).
- Creados endpoints `/login` y `/register`, modularizados en funciones reducidas para cumplir PEP 8.
- Configure seguridad modular con encriptaciÃ³n bcrypt en `security.py`.
- Generado archivo de dependencias `requirements.txt`.
- Creado cliente `ui.py` en Flet para autenticaciÃ³n con `httpx` apuntando a la API local.

## [11-03-2026 14:58:20] - RefactorizaciÃ³n de Interfaz y Roles de Usuario
- RefactorizaciÃ³n a Single Page Application (SPA) en Flet para evitar contracciÃ³n de vistas en modo `WEB_BROWSER`.
- Cambio de clases Flet desaprobadas (`ft.View` y `ft.alignment.center`) por contenedores puros (`ft.Container`, `ft.Column`).
- Creada e integrada vista `RegisterView` con endpoint POST `/register` para inscripciÃ³n de Aprendices.
- SimplificaciÃ³n del cÃ³digo de Flet, delegando estructura de layout nativa a los ejes `MainAxisAlignment` y `CrossAxisAlignment`.

## [11-03-2026 15:52:00] - RefactorizaciÃ³n Estructural a Single Page App "HÃ­brida" (Flask + HTMX + Tailwind)
- **MigraciÃ³n a Flask**: Eliminado todo el stack asÃ­ncrono (FastAPI y Flet local). Establecido `app.py` central conteniendo las reglas de direccionamiento, adaptando una arquitectura _Monolito Flexible_.
- **SincronizaciÃ³n de Base de Datos**: Cambiada la conexiÃ³n SQLite de `aiosqlite` genÃ©rico hacia el motor predeterminado y sÃ­ncrono de _SQLAlchemy_, resolviendo bloqueos de hilos a travÃ©s de context-managers (`with SessionLocal() as db`).
- **Web Security**: Descartado formato Bearer explÃ­citamente y transiciÃ³n a Tokens _JWT_ entregados y protegidos bajo _Cookies Seguras HTTP-Only_.
- **Aesthetic Glassmorphism (UI)**: RenovaciÃ³n total a web tradicional mediante plantillas Jinja `/templates` potenciadas por **Tailwind CSS** para un aspecto oscuro _Neo-cyberpunk_ y destellos radiales/degradados. Funciones visuales estÃ©ticas programÃ¡ticas en el nivel de XP en Barras.
- **Micro-interactividad (HTMX)**: Recreada la funcionalidad de "Unirse" de la tarjeta de aprendiz hacia mÃ³dulos empleando directrices como `<hx-post>` en el front validando los Skills del Aprendiz en tiempo real.

## [12-03-2026 13:58:00] - Enriquecimiento del Dashboard y LÃ³gica de Multiplicadores XP
- **Sistema de InformaciÃ³n DidÃ¡ctica**: Integrados iconos de informaciÃ³n neÃ³n y modales con efecto *glassmorphism* que detallan roles y requisitos.
- **Habilidades de Supervivencia (Multiplicadores)**: Reestructurada la Matriz de Habilidades para separar habilidades Verticales (Especialidad) de Horizontales (Supervivencia).
- **LÃ³gica de Multiplicador**: Implementada propiedad `xp_multiplier` en el modelo `User`. Las habilidades horizontales (Git, IA, SQL) ahora actÃºan como multiplicadores globales.
- **Mejoras en UI**: Nueva secciÃ³n "NÃºcleo TÃ©cnico" y badges de "Rayo" en especialidades para indicar bonos activos.
- **Soporte IDE**: ConfiguraciÃ³n de `settings.json` para ignorar falsos positivos de validaciÃ³n en plantillas Jinja2/HTML.

## [12-03-2026 14:15:00] - Motor de Temas DinÃ¡micos y Accesibilidad
- **Arquitectura de Temas**: MigraciÃ³n total a variables CSS (`--bg-color`, `--accent-color`, `--text-header`, etc.) para personalizaciÃ³n en tiempo real.
- **OptimizaciÃ³n de Accesibilidad**: 
    - ImplementaciÃ³n de `color-mix` para generar brillos y fondos translÃºcidos adaptativos.
    - Sistema de JerarquÃ­a de Texto: IntroducciÃ³n de `--text-header` y `--text-muted` para asegurar contraste en temas claros (negro pizarra) y oscuros.
- **Temas Base**: ImplementaciÃ³n de 4 temas (Futuristic, Light, Warm, Cold) con transiciones suaves de 0.5s.
- **Interfaz de SelecciÃ³n**: Floating Action Button (FAB) con menÃº radial para temas y paleta de colores de acento con persistencia en `localStorage`.

## [12-03-2026 19:30:00] - Despliegue Oficial del Sistema de Onboarding
- **Recursos Oficiales**: IntegraciÃ³n de videos de entrenamiento de VS Code (Official), Microsoft Developer, HolaMundo y Midudev.
- **UI de MisiÃ³n**: RediseÃ±o de la vista de mÃ³dulo con iframes estilizados mediante Glassmorphism y sombras neÃ³n.
- **Seguridad y Reglas**: 
    - ImplementaciÃ³n de la **Regla #13** en `.agent/rules.md` para control de despliegue manual.
    - AÃ±adidos enlaces externos seguros con `target="_blank"` y `rel="noopener noreferrer"`.
- **Backend Reforzado**: CorrecciÃ³n de dependencias (`requests`) y optimizaciÃ³n de la lÃ³gica de validaciÃ³n tÃ©cnica local.

## 17 de Marzo de 2026 - Limpieza y Estabilización de Evaluación
- **feat/refactor**: Consolidación de archivos CSV de preguntas (preguntas_modulo_1.csv, preguntas_python.csv) en un único archivo maestro llamado preguntas.csv.
- **fix**: Resolución de bucle infinito en avance de cola de preguntas al acertar en la evaluación.
- **fix**: Corrección del cálculo y propagación del error 'Undefined XP' para dar soporte robusto al cliente IDE (Terminal) cuando el stock llega a 0.
- **refactor**: Limpieza de entorno eliminando temporales .pyc / __pycache__ y archivos scripts obsoletos (seed_modules.py, init_module1.py).


## 18 de Marzo de 2026 - Integración de Entrenamiento y Energía Infinita
- **feat**: Rediseño del Dashboard de Aprendiz para integrar el **Centro de Entrenamiento** en el cuerpo superior de la página (ancho completo), mejorando la accesibilidad y el flujo de navegación.
- **fix**: Resolución del bloqueo de 24 horas (`last_exam_attempt`) y depleción de energía para el usuario **Kerwin Quintero**, garantizando acceso inmediato e ininterrumpido al Test Diagnóstico.
- **refactor**: Limpieza de código redundante en `dashboard_aprendiz.html` y remapeo de botones en la barra lateral.

