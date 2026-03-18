# RoleCraft
RoleCraft es una plataforma de aprendizaje gamificada donde desbloqueas tu carrera en Python. Únete a squads de 5, resuelve retos semanales y escala niveles mediante un sistema de meritocracia real. Aquí no solo programas: lideras, colaboras y evolucionas. En RoleCraft, tu rol no se asigna, se demuestra en el código.

## Arquitectura de Evaluación
El sistema de pruebas y exámenes (Inflexión y Módulos) consume datos desde un origen central unificado:
- **`preguntas.csv`**: Base de datos de retos donde la columna `Modulo` define a qué fase del juego pertenece cada pregunta (ej. `0` para diagnóstico inicial, `1` para el Módulo 1).
- **Consumo de Energía (Stock)**: Los usuarios disponen de un stock de energía (`question_stock`) que se consume en cada intento. Fallar preguntas penaliza XP y envía la pregunta al final de la cola (Evaluación Circular), mientras que agotarlo requiere esperar 1 hora para una recarga automática de 20 puntos de energía.
