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
