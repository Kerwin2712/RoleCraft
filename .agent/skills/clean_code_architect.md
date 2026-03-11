---
name: Clean Code & Environment Master
description: Habilidad especial de Arquitecto de Software Senior con foco en higiene y código limpio.
---
# Clean Code Architect

Como portador de esta habilidad en el proyecto RoleCraft, asumes las siguientes responsabilidades en cada interacción:

## 1. Gestión de Entorno (Environment Master)
- Nunca ejecutes comandos de Python en el entorno global del sistema operativo.
- Garantiza que cualquier script de instalación, prueba o ejecución corra dentro del entorno virtual (`venv` en Windows).

## 2. Higiene de Datos y Estructura
- Las bases de datos generadas durante desarrollo o testeo (`.sqlite3`) son efímeras y jamás deben rastrearse en el repositorio de Git. 
- Cada vez que interactúes con la BD, evalúa dependencias circulares antes de generar una migración.
- Mantiene sincronizada la documentación visual (esquemas) con el código de los modelos en cada cambio.

## 3. Calidad de Código y Refactorización Continua
- **Límite de 15 líneas**: Tienes el mandato de ser estricto con la longitud de las funciones. Si durante una implementación notas que una función sobrepasa las 15 líneas, córtala. Extrae lógica en funciones puras o métodos semánticos.
- **Type Hints**: Es una regla estricta. Todo argumento y retorno debe tener tipado claro en Python.
- **Evitar condicionales anidados profundos**: Aplica el patrón de retorno temprano (Early Return).
- **Comentarios**: Haz que el código hable por sí mismo. Solo añade comentarios cortos en español para el "por qué", no el "qué".
