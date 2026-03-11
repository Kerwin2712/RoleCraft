---
description: Flujo de trabajo para subir cambios al repositorio remoto (Git Workflow)
---
1. Analizar los archivos modificados (`git status`, `git diff`).
2. Actualizar la Bitácora de Cambios:
   - Abre/crea el archivo correspondiente en `docs/bitacora/<mes_año>.md` (ejemplo: `marzo_2026.md`).
   - Añade una nueva entrada con la fecha y hora exacta del commit.
   - Describe de forma clara y concisa los cambios realizados (qué se hizo, por qué y si fue una refactorización/fix/feature).
3. Añadir todos los cambios al área de preparación local (`git add .`, validando no incluir archivos prohibidos en `rules.md`).
4. Crear el commit con un mensaje descriptivo y claro (`git commit -m "feat/fix/docs: descripción del cambio"`).
5. Subir los cambios al repositorio remoto (`git push`).
