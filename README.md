# 🚀 RoleCraft

<div align="center">
  <p><strong>Desbloquea tu carrera en Python a través de una experiencia gamificada.</strong></p>
</div>

RoleCraft es una plataforma de aprendizaje interactivo que transforma la educación tradicional de programación en una experiencia similar a un juego de rol (RPG). Únete a *squads* de cinco personas, resuelve retos semanales y escala niveles mediante un sistema de meritocracia real. Aquí no solo programas: lideras, colaboras y evolucionas. 

En RoleCraft, **tu rol no se asigna, se demuestra en el código.**

---

## ✨ Características Principales

- **🎮 Aprendizaje Gamificado:** Sistema de experiencia (XP), niveles y una economía virtual (Monedas) que recompensan el progreso continuo.
- **⚡ Gestión de Energía (Stamina):** Cada intento en una prueba consume energía (`question_stock`). Incluye un sistema de recarga automática de 20 puntos tras 1 hora de inactividad.
- **🧠 Evaluaciones Dinámicas:** Sistema de exámenes con dificultad progresiva adaptativa. Implementa bloqueos temporales (24h) tras fallos repetidos para incentivar el estudio activo y evitar la fuerza bruta.
- **🛡️ Módulos Estructurados:** El aprendizaje inicia con filtros de configuración técnica (VSCode, Python, Antigravity) antes de permitir el avance a desarrollos de código real en Módulos posteriores.
- **📊 Dashboards Personalizados:** Vistas dedicadas tanto para **Aprendices** como para **Expertos** (Mentores), con seguimiento de progreso, inventario y estadísticas de rendimiento en tiempo real.
- **🔐 Seguridad Robusta:** Autenticación de usuarios validada, encriptación de contraseñas (Bcrypt) y gestión de sesiones segura con PyJWT.

## 🏛️ Arquitectura del Sistema

RoleCraft sigue una arquitectura basada en componentes del lado del servidor, optimizada para un alto rendimiento y bajo consumo de recursos.

- **Backend:** Desarrollado en **Python** utilizando el micro-framework **Flask**.
- **Base de Datos:** **SQLite** integrado con **SQLAlchemy** (ORM) para la gestión relacional de usuarios, misiones, progreso e inventario.
- **Frontend:** **HTML5** y **CSS3** puro para diseños ligeros y adaptables, con **Jinja2** como motor de plantillas dinámicas para el renderizado de vistas.
- **Gestión de Contenido:** El sistema de pruebas y retos consume los datos de forma ágil y centralizada a través de archivos tabulares estructurados (`preguntas.csv`).

## 📂 Estructura del Proyecto

```text
RoleCraft/
├── app.py                 # Punto de entrada de la aplicación Flask y enrutador principal
├── backend/               # Modelos de BDD SQLAlchemy, lógica de validación y controladores
├── templates/             # Vistas de interfaz de usuario (HTML con Jinja2)
│   ├── base.html          # Plantilla maestra de la aplicación
│   ├── dashboard_aprendiz.html # Panel principal del estudiante
│   ├── evaluacion.html    # Motor de renderizado de pruebas dinámico
│   ├── diagnostico.html   # Fase inicial de setup técnico
│   └── ...
├── static/                # Archivos estáticos (Hoja de estilos CSS, imágenes, scripts)
├── docs/                  # Documentación del sistema
├── preguntas.csv          # Repositorio central de datos de los retos
├── rolecraft.sqlite3      # Base de datos relacional
└── requirements.txt       # Dependencias del entorno
```

## 🛠️ Requisitos Previos

Para ejecutar la aplicación en un entorno de desarrollo local, asegúrate de tener instalados:
- **Python 3.8** o superior
- **pip** (Gestor de paquetes de Python)

## 🚀 Instalación y Despliegue Local

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/RoleCraft.git
   cd RoleCraft
   ```

2. **Crea y activa un entorno virtual (Recomendado):**
   ```bash
   # En Windows (PowerShell/CMD)
   python -m venv env
   env\Scripts\activate
   ```

3. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepara la base de datos:**
   (Ejecuta el script de migraciones inicial para estructurar las tablas y datos semilla).
   ```bash
   python migrate_db.py
   ```

5. **Inicia el servidor de desarrollo:**
   ```bash
   python app.py
   # El servidor estará expuesto típicamente en http://127.0.0.1:8000
   ```

## 🤝 Contribuir al Proyecto

¡El desarrollo colaborativo hace a RoleCraft más fuerte! Para contribuir:
1. Haz un **Fork** de este repositorio.
2. Crea una rama para tu característica o corrección: `git checkout -b feature/NuevaCaracteristica`.
3. Haz **Commit** de tus cambios de código: `git commit -m 'Implementa NuevaCaracteristica'`.
4. Sube la rama a tu fork: `git push origin feature/NuevaCaracteristica`.
5. Abre un **Pull Request** para revisión y futura integración.

## 📄 Licencia

Este proyecto se distribuye bajo los términos dictados en el archivo `LICENSE`. Consulta dicho archivo para conocer los derechos de uso y limitaciones.

---
*Construido con ❤️ para hacer de la programación una aventura.*
