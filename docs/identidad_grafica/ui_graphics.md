# 🔮 Rolecraft: Manual de Identidad Visual y UX (v1.0)

> Este documento define la estética, el comportamiento y la estructura del proyecto **Rolecraft**. El objetivo es que cualquier propuesta de diseño sea coherente con el **stack tecnológico** (Flask + HTMX + Tailwind) y la narrativa inmersiva de *"Misión Técnica"*.

---

## 1. Concepto Central: "The Dev's Odyssey"

Rolecraft **no es un dashboard administrativo convencional**; es una *Estación de Trabajo de Supervivencia*. Combina la estética Neo-Cyberpunk con la fluidez y funcionalidad de un IDE moderno.

- **Narrativa:** El usuario es un "Aprendiz" que ha sido reclutado para una "Misión de Configuración".
- **Habilidades (Skills Matrix):** Se dividen jerárquicamente en:
  - **Verticales:** Especialidad principal del usuario (Backend, Frontend, PM).
  - **Horizontales:** Competencias de Supervivencia y Multiplicadores (Git, IA, SQL).
- **Gamificación:** El progreso se mide en puntos de experiencia (XP), niveles de usuario y multiplicadores globales estratégicos.

---

## 2. Lenguaje Visual: Neo-Cyberpunk Glassmorphism

### Estética de Superficies
La interfaz debe sentirse profunda, inmersiva y tecnológica.

- **Fondo Base:** Oscuro profundo con destellos radiales sutiles (`radial-gradient`).
- **Efecto Cristal (Glassmorphism):** Los paneles deben implementar desenfoque de fondo (`backdrop-blur`), bordes finos semi-transparentes (`border-white/10`) y sombras de neón dinámicas.
- **Temas Dinámicos:** El sistema soporta 4 estados de tema gestionados mediante variables CSS nativas (*Futuristic, Light, Warm, Cold*).

**Variables CSS Principales:**
```css
--bg-color: /* El lienzo principal o fondo */
--accent-color: /* Acento para botones de acción y estados activos */
--text-header: /* Contraste máximo para títulos (Negro pizarra en Light, Blanco/Neón en Dark) */
--text-muted: /* Texto secundario para descripciones y metadatos */
```

### Componentes Clave
- **Barras de Habilidades:** Elementos interactivos con efectos de brillo (`glow`/`shadow-neon`) en estado `:hover` y apertura de modales informativos para detalles técnicos.
- **Centro de Entrenamiento:** Layout diseñado a ancho completo (*Full Width*) y ubicado en la parte superior del Dashboard para prioridad de atención.
- **Cards de Misión:** Identificadas por bordes de neón delgados, iconos de información táctica y *badges* representativos de multiplicadores (Ej. Icono de Rayo ⚡).
- **Iframes Estilizados:** Los videos y recursos de aprendizaje externos deben integrarse fluidamente y estar contenidos en marcos con bordes unificados y sombras adaptativas.

---

## 3. Arquitectura de Información y UX

### Layout del Dashboard
El panel de información principal se divide y organiza para reducir la carga cognitiva:
1. **Header / Status Bar:** Nivel actual de XP, multiplicadores activos globales y el selector del tema visual actual.
2. **Centro de Entrenamiento (Cuerpo Superior):** Botones y tarjetas de acceso directo a módulos y tutoriales activos.
3. **Núcleo Técnico:** Matriz visual conformada por 6 Habilidades Principales (Backend, Frontend, PM, Git, IA, SQL).
4. **Floating Action Button (FAB):** Menú radial inferior fijo para el cambio rápido de temas visuales y acceso ágil a ajustes técnicos.

### Flujos de Usuario (UX Rules)
- 🚀 **Cero Bloqueos Iniciales:** El acceso al **Test Diagnóstico** debe ser inmediato y sin restricciones (eliminar bloqueos temporales de 24h para el primer paso).
- ⚡ **Feedback Inmediato:** Uso prioritario de **HTMX** para realizar validaciones en tiempo real (P. ej., el botón "Unirse" valida los *skills* del aprendiz sin necesidad de recargar la página entera).
- 🏷️ **Jerarquía de Texto Clara:** Los títulos deben ser grandes y contundentes usando `--text-header`; en contraposición, todas las descripciones secundarias y notas deben usar `--text-muted` para mitigar la fatiga visual de la lectura larga.
- 👁️ **Accesibilidad Universal y Light Mode (Contraste Invertido):** 
  - Cumplimiento de contraste mínimo WCAG de **4.5:1** en tipografías, aplicable rigurosamente incluso en los temas visuales claros ("*Light*").
  - **Prohibido el uso de colores estáticos (Ej: `bg-black/40`, `text-white`, `border-white/10`) en contenedores base.** En lugar de eso, todo debe usar el sistema de variables CSS dinámicas: `bg-[var(--card-bg)]`, `text-[var(--text-main)]`, y `border-[var(--border-color)]` para asegurar legibilidad instantánea sin importar si el fondo muta a claro u oscuro.

---

## 4. Guía para Antigravity (Integración Técnica)

Al diseñar o solicitar vistas para Rolecraft, el Agente debe tener en mente las siguientes **restricciones de comportamiento** para asegurar compatibilidad total con la base técnica:

1. **Tailwind CSS Puro:** Exigencia de no inventar clases CSS externas si no es un componente extremadamente específico. Para el sistema de subtonos, aprovechar rutinas como `color-mix()` en CSS para generar variantes desde la variable principal de acento.
2. **Componentes Atómicos:** Escribir el HTML estructurado pensando su transposición y modulación en el entorno `templates/` de Jinja2.
3. **Persistencia Front-End:** Todos los cambios en la UI configurada por el usuario (como el cambio de tema) deben guardarse y recuperarse desde `localStorage`.

### Enrutamiento Mínimo Base (Endpoints previstos)
- `/tutorial/1`: Vista de Configuración de Entorno de Desarrollo.
- `/entrenamiento_detalle/<id>`: Vista de lectura técnica y detalles de misión individual.
- `/dashboard_aprendiz`: Vista principal unificada post-login.

---

## 5. Glosario de Estilos Base (Tokens)

Este es el catálogo atómico para asegurar un *feel* consistente a lo largo de las páginas de la aplicación:
- **Radios de Borde (Border Radius):** Usa clases estándar `rounded-xl` o `rounded-2xl` para los paneles y *cards*.
- **Transiciones y Animaciones (Transitions):** Aplica la clase `duration-500` (0.5s) u homogéneas para cambios de estado pesados, como el cambio de tema entre *Dark* y *Light*.
- **Sombras (Shadows):** Usar la sombra custom `shadow-neon` definida en configuraciones (vinculada al color del acento actual).
- **Iconografía:** Consistencia absoluta empleando bibliotecas como **Lucide** o **Phosphor Icons**. La versión elegida debe priorizar un estilo lineal o de neón fino.

---

> ⚠️ **Nota final para el Arquitecto de UX/UI:**
> *Siempre que propongas una mejora a la interfaz, asegúrate de respetar la ley inmutable del "Ancho Completo" del Centro de Entrenamiento superior, y de que la Matriz de Habilidades se mantenga inamovible como el eje visual central de la progresión de cada usuario.*