# Reglas del Proyecto RoleCraft
1. **Idioma**: Responde siempre en español.
2. **Comentarios**: Limita los comentarios en el código a frases cortas en español. El código debe ser fácil de leer e interpretar.
3. **Consola**: Operas en Windows 10. Prefiere comandos de PowerShell o CMD. No asumas entornos Linux.
4. **Manejo de Errores**: No asumas datos ni contextos. Si falta validación, detente y pregunta, o implementa un bloque de manejo de errores robusto.
5. **Estilo y Convenciones**: Sigue estrictamente la norma PEP 8 para Python.
6. **Stack Tecnológico Core**: El backend utiliza Flask y base de datos SQLite síncrona (vía SQLAlchemy `create_engine` tradicional sin async). El frontend utiliza templates Jinja2 interactivos con HTMX y utilidades CSS a través de Tailwind (CDN).
7. **Diseño Visual**: Preferimos "Glassmorphism" (fondos semitransparentes oscuros con blur), bordes con degradados estilo neón (`#00f3ff`, `#bc13fe`) y texturas dark mode.
8. **Manejo de Base de Datos en Flask**: Para inyectar la sesión global de Base de Datos en endpoints, instancia SIEMPRE el decorador context-manager (`with SessionLocal() as db:`) en lugar de variables globales inyectables o generadores `next()` infinitos para evitar bloqueos del hilo servidor.
9. **Falsos Positivos de IDE**: Si el IDE alerta con "property value expected" o "at-rule expected" en archivos `.html` específicamente al inyectar código variable Jinja en el atributo `style="..."`, ignóralos; el framework Flask los renderizará correctamente en runtime.
10. **Entorno Virtual**: Antes de ejecutar cualquier prueba o script, verifica y activa siempre el entorno virtual (`.\env\Scripts\Activate.ps1`).
11. **Archivos Temporales**: Prohibido subir archivos de prueba temporales, logs o bases de datos locales (`.sqlite3`, `test_*.py` temporales, etc.). Deben borrarse o ignorarse siempre en el repo.
12. **Bitácora de Cambios**: Antes de subir cambios al repositorio con git, documenta el cambio en la carpeta `docs/bitacora/`, en un archivo nombrado según el mes y año, incluyendo fecha, hora y detalle de la modificación.
13. **PROHIBICIÓN DE SUBIDA SIN PERMISO**: Queda terminantemente PROHIBIDO ejecutar `git push` o subir cambios al repositorio remoto sin una solicitud verbal EXPLÍCITA Y DIRECTA del usuario para esa acción específica.
