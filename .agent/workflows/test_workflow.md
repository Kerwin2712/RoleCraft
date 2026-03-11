---
description: Flujo de trabajo para pruebas (Activar venv -> Test -> Limpiar -> Informar)
---
1. Activar el entorno virtual de Python. Verifica previamente que `venv` existe. Usa `venv\Scripts\Activate.ps1`.
// turbo
2. Ejecuta las pruebas automatizadas de la plataforma (por ejemplo, con `pytest`).
// turbo
3. Elimina inmediatamente los archivos temporales y la caché generada (ej. archivos `__pycache__`, `.pytest_cache`, logs de prueba).
   Puedes usar: `Remove-Item -Path ".\.pytest_cache", ".\__pycache__", ".\test_*.sqlite3" -Recurse -Force -ErrorAction SilentlyContinue`
4. Analiza e informa los resultados de las pruebas de forma clara y concisa al usuario.
