---
description: Flujo de trabajo para migraciones de Base de Datos
---
1. Validar Modelos: Revisa el código de los modelos modificados y asegúrate de que no haya dependencias circulares (revisa los imports).
2. Generar Migración: Usa la herramienta correspondiente (ej. Alembic) para generar el archivo de migración reflejando los cambios.
// turbo
3. Actualizar Esquema/Documentación: Actualiza el archivo de documentación de base de datos (`docs/schema.md` o diagramas) añadiendo los nuevos cambios o tablas.
// turbo
4. Aplicar Migración: Ejecuta el comando para aplicar la migración a la base de datos de desarrollo de manera segura.
