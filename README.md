# RoleCraft
RoleCraft es una plataforma de aprendizaje gamificada donde desbloqueas tu carrera en Python. Únete a squads de 5, resuelve retos semanales y escala niveles mediante un sistema de meritocracia real. Aquí no solo programas: lideras, colaboras y evolucionas. En RoleCraft, tu rol no se asigna, se demuestra en el código.

## Arquitectura de Evaluación
El sistema de pruebas y exámenes consume datos desde un origen central unificado:
- **`preguntas.csv`**: Base de datos de retos. El **Módulo 1** actúa ahora como un filtro de configuración técnica (VSCode/Python/Antigravity) antes de permitir el avance a retos de código.
- **Consumo de Energía (Stock)**: Los usuarios disponen de un stock de energía (`question_stock`) que se consume en cada intento.
- **Recarga Automática**: Implementada lógica de recarga de 20 puntos tras 1 hora de inactividad por agotamiento de energía.

