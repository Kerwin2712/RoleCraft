# Reglas del Proyecto RoleCraft
1. **Idioma**: Responde siempre en español.
2. **Comentarios**: Limita los comentarios en el código a frases cortas en español. El código debe ser fácil de leer e interpretar.
3. **Consola**: Operas en Windows 10. Prefiere comandos de PowerShell o CMD. No asumas entornos Linux.
4. **Manejo de Errores**: No asumas datos ni contextos. Si falta validación, detente y pregunta, o implementa un bloque de manejo de errores robusto.
5. **Estilo y Convenciones**: Sigue estrictamente la norma PEP 8 para Python.
6. **Tipado**: No se acepta código sin sus correspondientes Type Hints.
7. **Simplicidad Funcional**: Si una función supera las 15 líneas de código, analízala y refactorízala creando funciones auxiliares para mantener la simplicidad.
8. **Entorno Virtual**: Antes de ejecutar cualquier prueba o script, verifica y activa siempre el entorno virtual (`venv`). Prohibido usar el intérprete global.
9. **Archivos Temporales**: Prohibido subir archivos de prueba temporales, logs o bases de datos locales (`.sqlite3`, `test_*.py` temporales, etc.). Deben borrarse o ignorarse siempre.
