# 🐉 KaliGhost Pro GUI - REDISEÑO COMPLETO

**Documento de Especificación Técnica de Interfaz Gráfica**  
**Versión**: 3.0 - Rediseño Profesional  
**Fecha**: 2026  
**Clasificación**: Especificación Técnica - Diseño UX/UI Premium  

---

## 📋 ÍNDICE EJECUTIVO

Este documento especifica una **RECONSTRUCCIÓN COMPLETA** de la interfaz gráfica de KaliGhost Pro desde cero. El rediseño no es un parche—es una arquitectura de UX/UI totalmente nueva que transmite **poder**, **libertad sin restricciones** y **experiencia profesional de lujo**.

### Problemas Identificados del Diseño Anterior
- ❌ Dragón 3D supuestamente implementado pero con OpenGL fallback deficiente
- ❌ Arquitectura fragmentada entre múltiples archivos Python
- ❌ Componentes desconectados sin propósito funcional claro
- ❌ Falta de coherencia visual profesional
- ❌ Rendimiento no optimizado para operaciones intensivas
- ❌ No transmite el concepto de "poder" y "libertad" del agente YrYs
- ❌ Interfaz no refleja que el usuario tiene CONTROL TOTAL del comportamiento del agente

---

## 🎯 OBJETIVOS DEL REDISEÑO

### Primarios
1. **Transmitir Poder Visual**: Cada elemento debe comunicar capacidad, control, dominio
2. **Experiencia de Lujo**: Animaciones suaves, transiciones fluidas, detalles milimétricos
3. **Libertad Sin Censura**: Interfaz refleja que el usuario define completamente el comportamiento del agente
4. **Profesionalismo Absoluto**: Diseño digno de aplicación empresarial de seguridad
5. **Funcionalidad Integrada**: Cada panel tiene propósito específico y necesario

### Secundarios
1. Renderizado 3D REAL (no fallback 2D débil)
2. Sistema de paneles componibles y personalizable
3. Integración fluida con agente YrYs y herramientas pentesting
4. Monitoreo real-time de operaciones y comportamiento del agente
5. Control granular de políticas de seguridad y restricciones del agente

---

## 🐉 INVESTIGACIÓN: ANATOMÍA DEL DRAGÓN

### Referencia Biológica Real

#### Estructura Corporal Base
```
DRAGÓN (Clase Reptil Mitológico + Biomecánica Cibernética)

CABEZA (15% del cuerpo)
├── Cráneo articulado: 42 polígonos articulados
├── Mandíbulas con cinemática inversa (3 grados libertad)
├── Ojos esféricos (esfera con shader especial)
│   ├── Pupila: Contracción dinámica basada en estado
│   ├── Brillo: Reflejos especulares con normalmap
│   └── Nictitante: Membrana translúcida animada
├── Nariz con ventanas nasales óseas
├── Orejas/Crestas: 6 apéndices articulados
└── Piel texturizada con escamas paramórficas

CUERPO/TORSO (40% del cuerpo)
├── Columna vertebral: 28 vértebras discretas
│   ├── Cada una: objeto 3D independiente
│   ├── Cinemática: FK con IK solver optativo
│   └── Deformación: Blend skinning no-lineal
├── Caja torácica: Estructura ósea articulada
│   ├── 24 costillas bilaterales
│   ├── Animación respiratoria: Expansión/compresión
│   └── Efecto: Pulso energético interno
├── Piel/Cobertura: Subsurface scattering
│   ├── Capa epidérmica: Escamas individuales
│   ├── Capa sárnea: Musculatura subyacente
│   └── Capa dermal: Vascularización visible
└── Órganos internos: Invisible pero simulado
    └── Efecto: Brillo interno pulsante visible a través de grietas

ALAS (25% del cuerpo)
├── Estructura: 2 alas simétricas
├── Cada ala: 4 dígitos óseos + membrana
│   ├── Radio/Ulna: Huesos articulados
│   ├── Falanges: 16 articulaciones por ala
│   ├── Membrana: Tela translúcida con nervaduras
│   │   ├── Capilares energéticos iluminados
│   │   ├── Textura: Patrón de grietas estilizadas
│   │   └── Shader: Translucency con desplazamiento
│   └── Conexión al cuerpo: Articulación rotacional triple
│       └── Movimiento: Batido con inercia + wind response
├── Cinemática:
│   ├── Batido: Frecuencia 3-8 Hz (variable)
│   ├── Rotación: -120° a +120° en eje longitudinal
│   ├── Flexión: -90° a +45° en eje transversal
│   └── Torsión: -30° a +30° en eje radial
└── Efectos:
    ├── Estela de luz: Particle trail generator
    ├── Aire: Simulación de presión
    └── Energía: Corrientes magnéticas visuales

COLA (20% del cuerpo)
├── Segmentos: 34 vértebras de cola
├── Estructura espinal: Huesos discretos articulados
├── Movimiento: IK chain solver con constraint
│   ├── Base: Anclada al cuerpo
│   ├── Punta: Libre con gravedad simulada
│   └── Wobble: Oscilación natural amortiguada
├── Cobertura: Espinas dorsales en punta
│   ├── 22 espinas óseas dorsales
│   ├── Movimiento: Respuesta a viento/energía
│   └── Efecto: Brillo bajo luz específica
└── Energía de cola: Aura que sigue el movimiento

EXTREMIDADES (Patas: 20% del cuerpo)
├── 4 patas bilaterales (derecha-izquierda)
│   ├── Delanteras: Mas articuladas, garras retráctiles
│   │   ├── Hombro: 3 DOF (3 grados libertad)
│   │   ├── Codo: 2 DOF
│   │   ├── Muñeca: 2 DOF
│   │   └── Garras: 5 dígitos independientes
│   └── Traseras: Mas potentes, postura plantigrada
│       ├── Cadera: 3 DOF
│       ├── Rodilla: 1 DOF (flexión)
│       └── Tobillo: 2 DOF
├── Cinemática inversa: Solver IK CCD para locomoción
│   ├── Patrones de marcha: 8 tipos diferentes
│   ├── Transiciones: Bezier curves suave
│   └── Gravedad: Footprint IK contra geometría
└── Garras: Shaders con reflejo metalizado
    ├── Material: "Metal cibernético"
    ├── Rugosidad: Mapas normales detallados
    └── Emit: Brillo bajo energético

INTEGRACION CIBERNETICA
├── Puntos de energía: 7 chakra-like power cores
│   ├── Corazón central: Pecho/torso
│   ├── Núcleos secundarios: Puntos articulares clave
│   └── Efecto: Brillo pulsante sincronizado
├── Circuitería luminosa: Circuitos energéticos visibles
│   ├── Flujo: Animación de corriente eléctrica
│   ├── Color: Que varía con estado del sistema
│   └── Intensidad: Proporcional a actividad
└── Nervios digitales: Red neuronal visible
    ├── Emite: Destellos de sinapsis
    ├── Patrón: Procesamiento en tiempo real
    └── Feedback: Visualiza "pensamiento" del agente
```

#### Movimientos Base del Dragón

```
1. ESTADO REPOSO/OBSERVACIÓN
   - Respiración: Ciclo lento 4-6 segundos
   - Parpadeo: Nictitante cada 8-12 segundos
   - Postura: Descansada sobre 4 patas
   - Ojos: Escaneando perimetralmente
   - Colas: Movimiento ondulante suave
   - Energía: Brillo bajo, pulsante regularmente
   - Propósito: Proyectar calma vigilante

2. ESTADO ANÁLISIS ACTIVO
   - Cabeza: Rotación hacia punto de interés
   - Cuerpo: Ligera flexión direccional
   - Alas: Movimiento preparatorio (semi-desplegadas)
   - Ojos: Enfoque intenso con pupilas contraídas
   - Energía: Brillo aumenta gradualmente
   - Circulería: Flujo acelerado
   - Efecto sonoro: Zumbido bajo energético
   - Propósito: Transmitir concentración

3. ESTADO OPERACIÓN/EJECUCIÓN
   - Alas: Batido completo 6-8 Hz
   - Cuerpo: Postura erguida, tensión muscular visible
   - Movimiento: Puede caminar/moverse en la escena
   - Cabeza: Seguimiento de objetivos
   - Ojos: Brillo máximo, pupila dilatada
   - Energía: Pulsante intenso, colores saturados
   - Efectos: Estelas de luz, partículas energéticas
   - Propósito: Comunicar poder, acción, dominio

4. ESTADO ALERTA/AMENAZA DETECTADA
   - Postura: Erguida al máximo, garras extendidas
   - Alas: Desplegadas completamente como escudo
   - Cuerpo: Tensión máxima, escamas levantadas
   - Cabeza: Rotación ofensiva, mandíbulas amenazantes
   - Ojos: Rojo/naranja, pupilas verticales
   - Energía: Rojo/naranja, pulsante caótico
   - Efectos: Arco eléctrico visible entre dientes/garras
   - Sonido: Rugido digital procesado
   - Propósito: Proyectar ferocidad defensiva

5. ESTADO ESPERA/MODO FANTASMA
   - Opacidad: Disminuye gradualmente a 30%
   - Animación: Ralentiza a 20% velocidad normal
   - Energía: Azul/púrpura bajo, casi imperceptible
   - Postura: Replegada, invisible
   - Efecto: Desvanecimiento progresivo (fade out)
   - Sonido: Silencio total
   - Propósito: Transmitir que el sistema está "dormido"

6. ESTADO TRANSICIÓN/MORPH
   - Duración: 2-3 segundos por transición
   - Interpolación: Bezier curves para suavidad
   - Efectos: Destello energético en transición
   - Sonido: Transición de frecuencia (theremin effect)
   - Propósito: Feedback claro de cambio de estado
```

---

## 🎨 ARQUITECTURA DE DISEÑO VISUAL

### Paleta de Colores Profesional

```
PRIMARY PALETTE
├── Kali Green: #22AA55 (RGB: 34, 170, 85)
│   └── Uso: Accents, highlights, status positivo
├── Deep Black: #0A0A0A (RGB: 10, 10, 10)
│   └── Uso: Fondos principales
├── Dark Grey: #1A1A1A (RGB: 26, 26, 26)
│   └── Uso: Paneles secundarios
└── Light Grey: #E0E0E0 (RGB: 224, 224, 224)
    └── Uso: Texto primario

SECONDARY PALETTE (Cyberpunk)
├── Neon Blue: #00FFFF (RGB: 0, 255, 255)
│   └── Uso: Información activa, transiciones
├── Hot Pink: #FF1493 (RGB: 255, 20, 147)
│   └── Uso: Alertas, énfasis crítico
├── Electric Purple: #9D00FF (RGB: 157, 0, 255)
│   └── Uso: Selecciones, interacciones
└── Data Yellow: #FFD700 (RGB: 255, 215, 0)
    └── Uso: Indicadores, warnings

STATUS PALETTE
├── Success: #00FF00 (RGB: 0, 255, 0)
│   └── Uso: Operaciones completadas
├── Warning: #FFA500 (RGB: 255, 165, 0)
│   └── Uso: Estados en progreso
├── Error: #FF4444 (RGB: 255, 68, 68)
│   └── Uso: Fallos, peligro
└── Info: #4488FF (RGB: 68, 136, 255)
    └── Uso: Información neutral

ENERGY PALETTE (Animación Dragon)
├── Core Blue: #0066FF (RGB: 0, 102, 255)
├── Core Green: #00CC66 (RGB: 0, 204, 102)
├── Core Red: #FF3333 (RGB: 255, 51, 51)
├── Core Purple: #CC33FF (RGB: 204, 51, 255)
└── Gradients: Interpolación suave entre cores
```

### Tipografía Profesional

```
FUENTES RECOMENDADAS (Stack)
├── Títulos/Headers: "JetBrains Mono Bold" o "IBM Plex Mono Bold"
├── Cuerpo/UI: "IBM Plex Mono Regular" o "Monaco"
├── Monoespaciado: "Courier Prime" o "Inconsolata"
├── Alternativa: Sistema: "Segoe UI" (Windows), "SF Pro" (macOS), "Ubuntu Mono" (Linux)

TAMAÑOS TIPOGRÁFICOS
├── H1 (Títulos): 32px bold
├── H2 (Subtítulos): 24px bold
├── H3 (Secciones): 18px bold
├── Body (Texto): 14px regular
├── Small (Labels): 12px regular
├── Tiny (Hints): 10px regular

PESOS DE FUENTE
├── Regular: 400 (Texto estándar)
├── Medium: 500 (Énfasis ligero)
├── Bold: 700 (Títulos, énfasis)
└── Extra Bold: 900 (Máximo énfasis)

LINE HEIGHT (Espaciado vertical)
├── Headers: 1.2x de tamaño
├── Body: 1.6x de tamaño
├── Dense: 1.4x (componentes compactos)
```

### Sistema de Espaciado (8-point Grid)

```
BASE UNIT = 8px

SPACING SCALE
├── XS: 4px (0.5x) - Microrspacios
├── S: 8px (1x) - Espacios internos pequeños
├── M: 16px (2x) - Espacios estándar
├── L: 24px (3x) - Espacios grandes
├── XL: 32px (4x) - Espacios muy grandes
├── XXL: 64px (8x) - Separaciones principales

APLICACIÓN PRÁCTICA
├── Padding botones: S (8px)
├── Margin cards: M (16px)
├── Separación secciones: L (24px)
├── Separación paneles: XL (32px)
├── Gutter lateral: XL (32px)
```

### Sistema de Elevación (Z-depth)

```
NIVELES DE PROFUNDIDAD
├── Nivel 0: Fondo (backgroundColor principal)
├── Nivel 1: Paneles base (0.5dp sombra)
├── Nivel 2: Componentes (2dp sombra)
├── Nivel 3: Panels flotantes (4dp sombra)
├── Nivel 4: Modales/Popovers (8dp sombra)
├── Nivel 5: Tooltips/Contextmenus (16dp sombra)
└── Nivel 6: Notificaciones (24dp sombra)

SOMBRAS CSS/Qt
├── Sombra 0.5dp: rgba(0,0,0,0.12) 0 0.5px 1px
├── Sombra 2dp: rgba(0,0,0,0.16) 0 2px 4px
├── Sombra 4dp: rgba(0,0,0,0.19) 0 4px 8px
├── Sombra 8dp: rgba(0,0,0,0.25) 0 8px 16px
└── Sombra 16dp: rgba(0,0,0,0.30) 0 16px 32px
```

---

## 🏗️ ARQUITECTURA DE COMPONENTES

### Nivel 1: Contenedor Principal

```
KaliGhostProGUI (QMainWindow)
├── Atributos:
│   ├── resolution: (1920x1080) mínimo, escalable hasta 4K
│   ├── theme: "Cyberpunk" | "Professional" | "Dark" (switchable)
│   ├── fps_target: 60 (configurable)
│   └── dpi_scaling: automático
│
├── Componentes:
│   ├── Header Panel (siempre visible)
│   ├── Main Viewport (dragón 3D + canvas)
│   ├── Left Sidebar (herramientas)
│   ├── Right Sidebar (estado del agente)
│   ├── Bottom Panel (consola/logs)
│   └── Floating Elements (overlays dinámicos)
│
└── Métodos:
    ├── init_theme()
    ├── init_opengl()
    ├── init_agent_connection()
    └── setup_layouts()
```

### Nivel 2: Paneles Funcionales

#### 2.1 Header Panel (Siempre Visible, Height: 56px)

```
┌─ HEADER PANEL ─────────────────────────────────────────────────────┐
│                                                                      │
│  [≡]  KALIGHOST PRO  [★] │ YrYs Agent v2.1 │ [🔍] [⚙️]  [🚪] [△]   │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Componentes:
├── Menu Toggle Button (≡)
│   └── Abre/cierra left sidebar
├── Logo + Title
│   ├── Texto: "KALIGHOST PRO"
│   ├── Icono: Dragón pequeño (12x12px)
│   └── Tooltip: Versión + build info
├── Status Indicator (★)
│   ├── Color dinámico según estado
│   ├── Tooltips en hover
│   └── Click: Muestra detalles de sistema
├── Agent Version Display
│   ├── Texto: "YrYs Agent v2.1"
│   ├── Click: Abre panel de agente
│   └── Derecha: Indicador de estado
├── Quick Actions
│   ├── 🔍 Search: Buscar en herramientas
│   ├── ⚙️ Settings: Preferencias rápidas
│   └── 🚪 Logout: Cerrar sesión
└── Window Controls
    ├── Minimizar (-)
    ├── Maximizar (□)
    └── Cerrar (△)
```

#### 2.2 Main Viewport (Centro, 70% del espacio)

```
┌─ 3D DRAGON VIEWPORT ───────────────────────────────────────────────┐
│                                                                      │
│                       ╱╲___                                          │
│                      (  o  )  ◄ Dragón 3D renderizado               │
│                       \___/                                          │
│                                                                      │
│   [ESTADO] ┌─ Alas: Volando ─────────────────────────────────────┐ │
│   [ENERGÍA] │ Operaciones: 3 en progreso                          │ │
│             │ Amenaza: Ninguna detectada                          │ │
│             └────────────────────────────────────────────────────┘ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Especificaciones:
├── Renderización:
│   ├── Engine: OpenGL 4.0+ con fallback WebGL
│   ├── MSAA: 4x anti-aliasing
│   ├── VSYNC: Habilitado (60 FPS)
│   ├── LOD: Nivel de detalle adaptativo
│   └── Shaders: GLSL 4.60
│
├── Interactividad:
│   ├── Zoom: Rueda del ratón
│   ├── Rotación: Click+Drag
│   ├── Paneo: Spacebar+Drag
│   ├── Reset vista: Tecla R
│   └── Modo fullscreen: F
│
├── Overlay de Estado (esquina superior izquierda):
│   ├── FPS actual
│   ├── Estado del dragón (REPOSO | ACTIVO | AMENAZA)
│   ├── Operaciones activas
│   ├── Consumo de recursos (CPU/GPU/RAM)
│   └── Latencia de red
│
└── HUD Dinámico (superpuesto sobre viewport):
    ├── Señales de estado (colores animados)
    ├── Indicadores de tareas
    ├── Mensajes del agente
    └── Alertas en tiempo real
```

#### 2.3 Left Sidebar (Herramientas, Width: 280px, Colapsable)

```
┌─ LEFT SIDEBAR ─────────────────────────────────────────────────────┐
│                                                                      │
│ ╔═ TOOLS & CONTROLS ════════════════════════════════════════════╗ │
│ ║                                                                ║ │
│ ║  🎯 RECONNAISSANCE                                            ║ │
│ ║     ├─ [🔍] Network Scanner        [⚡ Run]                  ║ │
│ ║     ├─ [📡] Port Scanner           [⚡ Run]                  ║ │
│ ║     ├─ [🌐] Service Detection      [⚡ Run]                  ║ │
│ ║     └─ [💾] OSINT Tools            [⚡ Run]                  ║ │
│ ║                                                                ║ │
│ ║  ⚔️ EXPLOITATION                                              ║ │
│ ║     ├─ [💥] Vulnerability Scanner  [⚡ Run]                  ║ │
│ ║     ├─ [🎯] Exploit Framework      [⚡ Run]                  ║ │
│ ║     ├─ [🔓] Privilege Escalation   [⚡ Run]                  ║ │
│ ║     └─ [🧪] Custom Payloads        [⚡ Run]                  ║ │
│ ║                                                                ║ │
│ ║  🛡️ DEFENSE & EVASION                                         ║ │
│ ║     ├─ [👻] Anti-Forensics         [⚡ Run]                  ║ │
│ ║     ├─ [🔐] Encryption Tools       [⚡ Run]                  ║ │
│ ║     ├─ [📡] Network Spoofing       [⚡ Run]                  ║ │
│ ║     └─ [🎭] Identity Masking       [⚡ Run]                  ║ │
│ ║                                                                ║ │
│ ║  📊 ANALYSIS & REPORTING                                      ║ │
│ ║     ├─ [📈] Data Analyzer          [⚡ Run]                  ║ │
│ ║     ├─ [📋] Report Generator       [⚡ Run]                  ║ │
│ ║     ├─ [🔍] Forensic Tools         [⚡ Run]                  ║ │
│ ║     └─ [📦] Export Results         [⚡ Run]                  ║ │
│ ║                                                                ║ │
│ ║  ⚙️ ADVANCED OPTIONS                                           ║ │
│ ║     ├─ [🤖] AI Learning            [⚡ Configure]            ║ │
│ ║     ├─ [🧠] Neural Tuning          [⚡ Configure]            ║ │
│ ║     ├─ [🌍] Cloud Integration      [⚡ Configure]            ║ │
│ ║     └─ [🔧] Custom Skills          [⚡ Configure]            ║ │
│ ║                                                                ║ │
│ ╚════════════════════════════════════════════════════════════════╝ │
│                                                                      │
│ [Search Tools...] ▼                                                  │
│ [Favorites] [Recent] [All]                                           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Interactividad:
├── Scroll: Rueda del ratón
├── Collapse/Expand: Click en categorías
├── Hover: Tooltip con descripción
├── Click tool: Expande detalles/parámetros
└── Run button: Inicia herramienta con UI modal
```

#### 2.4 Right Sidebar (Estado del Agente, Width: 320px, Colapsable)

```
┌─ RIGHT SIDEBAR ────────────────────────────────────────────────────┐
│                                                                      │
│ ╔═ AGENT CONTROL CENTER ════════════════════════════════════════╗ │
│ ║                                                                ║ │
│ ║  ⚡ AGENT STATUS                                              ║ │
│ ║  ┌──────────────────────────────────────────────────────┐    ║ │
│ ║  │ 🟢 YrYs Agent v2.1                      [Uptime: 2h] │    ║ │
│ ║  │                                                      │    ║ │
│ ║  │ State: ACTIVE | Mode: AUTONOMOUS                    │    ║ │
│ ║  │ CPU: 32% | RAM: 512MB | GPU: 45%                    │    ║ │
│ ║  │ Network: Connected | Latency: 12ms                  │    ║ │
│ ║  │                                                      │    ║ │
│ ║  │ Current Task: Port Scanning 192.168.1.0/24         │    ║ │
│ ║  │ Progress: ████████░░░░░░░░░░░░░░░░░░░░ 42%         │    ║ │
│ ║  └──────────────────────────────────────────────────────┘    ║ │
│ ║                                                                ║ │
│ ║  🎛️ BEHAVIOR CONTROLS                                         ║ │
│ ║  ┌──────────────────────────────────────────────────────┐    ║ │
│ ║  │ Autonomy Level:                                     │    ║ │
│ ║  │ [████████░░░░░░░░░░░░░░░░░░░░░░░░░] 80%            │    ║ │
│ ║  │                                                      │    ║ │
│ ║  │ Decision Making:                                    │    ║ │
│ ║  │ ☑ Proactive Analysis  ☑ Auto-Learning             │    ║ │
│ ║  │ ☑ Risk Assessment     ☑ Threat Prediction         │    ║ │
│ ║  │ ☑ Resource Optimization  ☑ Adaptive Strategy      │    ║ │
│ ║  │                                                      │    ║ │
│ ║  │ Learning Mode:                                      │    ║ │
│ ║  │ ○ Conservative  ◉ Standard  ○ Aggressive           │    ║ │
│ ║  │                                                      │    ║ │
│ ║  │ Restrictions Enforced:                              │    ║ │
│ ║  │ ☑ No Malware Creation   ☑ No Data Destruction      │    ║ │
│ ║  │ ☑ Audit Logging Required   ☑ Approval Gate         │    ║ │
│ ║  └──────────────────────────────────────────────────────┘    ║ │
│ ║                                                                ║ │
│ ║  📊 INTELLIGENCE FEED                                         ║ │
│ ║  ┌──────────────────────────────────────────────────────┐    ║ │
│ ║  │ • Detected: 847 potential vulnerabilities           │    ║ │
│ ║  │ • Analyzed: 34 exploitation paths                   │    ║ │
│ ║  │ • Prioritized: 12 critical-risk targets             │    ║ │
│ ║  │ • Learning: 156 new patterns identified             │    ║ │
│ ║  │ • Confidence: 94.7% on assessments                  │    ║ │
│ ║  └──────────────────────────────────────────────────────┘    ║ │
│ ║                                                                ║ │
│ ║  🔒 SECURITY & POLICY                                         ║ │
│ ║  [🛡️ View Policies] [🔐 Encryption Settings] [⚖️ ACL]       ║ │
│ ║                                                                ║ │
│ ╚════════════════════════════════════════════════════════════════╝ │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Control Detallado:
├── Agent Status Monitoring
│   ├── CPU/RAM/GPU en tiempo real
│   ├── Estado de tareas activas
│   └── Logs de decisiones
├── Behavior Configuration
│   ├── Sliders para nivel autonomía
│   ├── Toggles para funciones específicas
│   └── Modo de aprendizaje seleccionable
├── ACL & Restrictions
│   ├── Políticas aplicables
│   ├── Whitelist/Blacklist
│   └── Cadenas de aprobación
└── Learning Progress
    ├── Patrones detectados
    ├── Confianza de predicciones
    └── Nuevas capacidades adquiridas
```

#### 2.5 Bottom Panel (Consola, Height: 200-400px, Resizable)

```
┌─ BOTTOM PANEL (EXPANDABLE) ────────────────────────────────────────┐
│                                                                      │
│ 📋 OPERATION CONSOLE  [🔽 Clear] [🔍 Filter] [💾 Export] [^^]      │
│ ├─────────────────────────────────────────────────────────────────┤ │
│ │ [18:45:23] ✓ Network scan complete: 42 hosts found              │ │
│ │ [18:45:22] • Port 22 (SSH) detected on 192.168.1.5              │ │
│ │ [18:45:21] • Port 80 (HTTP) detected on 192.168.1.8             │ │
│ │ [18:45:19] ⚡ YrYs Agent optimizing attack vectors              │ │
│ │ [18:45:18] ⚠️  WARNING: Potential honeypot detected             │ │
│ │ [18:45:15] 🔍 Running vulnerability assessment...               │ │
│ │ [18:45:10] ✓ Nmap scan initiated                                │ │
│ │ [18:45:00] ▶ Operation started by user                          │ │
│ │ [18:44:55] 🟢 All systems ready                                 │ │
│ │                                                                  │ │
│ │ [Scroll up for more...]                                         │ │
│ │                                                                  │ │
│ └─────────────────────────────────────────────────────────────────┘ │
│                                                                      │
│ Input: > _[Espacio para comando directo]                            │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

Características:
├── Color Coding:
│   ├── ✓ (Verde): Éxito
│   ├── ⚠️ (Naranja): Warnings
│   ├── ✗ (Rojo): Errores
│   ├── • (Cyan): Info neutral
│   ├── ⚡ (Amarillo): Acciones del agente
│   └── 🔍 (Purpura): Búsquedas/análisis
│
├── Funcionamiento:
│   ├── Scroll infinito con tail
│   ├── Búsqueda full-text (Ctrl+F)
│   ├── Filtros por tipo/timestamp
│   ├── Export a archivo
│   └── Clear logs (con confirmación)
│
└── Expand/Collapse:
    ├── Handle superior resizable
    ├── Double-click para máximo/mínimo
    └── Recordar última altura configurada
```

### Nivel 3: Componentes Reutilizables

#### Botón Estándar (Con Estilos Múltiples)

```python
class CyberButton(QPushButton):
    """Botón profesional con múltiples estilos"""
    
    Estilos = {
        "PRIMARY": {
            "bg_color": "#22AA55",
            "text_color": "#FFFFFF",
            "hover_bg": "#33BB66",
            "active_bg": "#118833",
            "border": "1px solid #22AA55"
        },
        "SECONDARY": {
            "bg_color": "#1A1A1A",
            "text_color": "#DADADA",
            "hover_bg": "#282828",
            "active_bg": "#333333",
            "border": "1px solid #333333"
        },
        "DANGER": {
            "bg_color": "#CC3333",
            "text_color": "#FFFFFF",
            "hover_bg": "#DD4444",
            "active_bg": "#AA2222",
            "border": "1px solid #CC3333"
        },
        "SUCCESS": {
            "bg_color": "#00DD00",
            "text_color": "#000000",
            "hover_bg": "#00FF00",
            "active_bg": "#00BB00",
            "border": "1px solid #00DD00"
        }
    }
```

---

## 💻 STACK TECNOLÓGICO RECOMENDADO

### Frontend Framework

```
OPCIÓN 1: PYSIDE6 (RECOMENDADO) ⭐⭐⭐⭐⭐
├── Ventajas:
│   ├── Cross-platform nativo (Windows/macOS/Linux)
│   ├── Integración directa con OpenGL
│   ├── Performance nativo (no Electron)
│   ├── Deployment simple (single binary)
│   └── Qt Designer para UI rápida
├── Desventajas:
│   ├── Curva de aprendizaje media
│   └── Binarios grandes (~150MB)
├── Uso: 100% backend, 100% frontend
└── Versión: PySide6.5+ (release 2024)

OPCIÓN 2: PYQT6 (ALTERNATIVA)
├── Similar a PySide6 pero con licencia diferente
├── Levemente más antiguo en updates
└── Uso: Si necesita licencia comercial

OPCIÓN 3: TAURI + VUE/REACT (MODERNA)
├── Ventajas:
│   ├── Frontend web moderno
│   ├── Rust backend de alto rendimiento
│   ├── Muy ligero (~10MB)
│   └── Material Design nativo
├── Desventajas:
│   ├── Sin integración nativa OpenGL directo
│   ├── Curva de aprendizaje más alta
│   └── WebGL para 3D (menos performance)
└── Recomendación: Futuro pero no óptimo para 3D real-time

Selección Final: PYSIDE6 (Desktop nativo + OpenGL + Performance)
```

### 3D Rendering Engine

```
OPCIÓN 1: OPENGL 4.0+ (RECOMENDADO) ⭐⭐⭐⭐⭐
├── Backend: PyOpenGL + PyOpenGL-accelerate
├── Shading: GLSL 4.60
├── Features:
│   ├── Advanced lighting (PBR)
│   ├── Deferred rendering
│   ├── Screen-space effects (SSAO, SSR)
│   ├── Post-processing
│   └── Real-time shadows
├── Performance: Excelente (~60+ FPS 1080p)
└── Uso: Engine principal para dragón

OPCIÓN 2: VULKAN (ALTERNATIVA)
├── Mejor performance en multi-threading
├── Soporte via Pyside6 + PyVulkan
└── Complejidad: Alta (solo si problema de performance)

OPCIÓN 3: WEBGL (FALLBACK)
├── Para sistemas sin OpenGL
├── Usa Three.js o Babylon.js
└── Performance: Bueno pero no óptimo

Selección Final: OpenGL 4.0 + GLSL 4.60
```

### Librerías de Apoyo

```
GEOMETRÍA & MATEMÁTICA
├── NumPy (arrays numéricos)
├── PyGLM (GLM mathematics)
├── Scipy (transformaciones complejas)
└── Quaternion (rotaciones suaves)

CARGA DE ASSETS
├── Pygame (texturas PNG/JPG)
├── PIL/Pillow (procesamiento de imagen)
├── OpenEXR (para HDR maps)
└── Assimp (loading modelos 3D)

ANIMACIÓN & INTERPOLACIÓN
├── Easing (curvas de animación)
├── Keyframe (sistema de keyframes custom)
├── Bezier (splines suave)
└── IKPy (cinemática inversa)

SISTEMA & INTEGRACIÓN
├── Psutil (monitoreo CPU/RAM/GPU)
├── Requests (HTTP calls)
├── WebSocket (comunicación real-time)
├── SQLAlchemy (persistencia datos)
└── Logging (auditoría y debugging)

PERFORMANCE & DEBUG
├── Py-Spy (profiling)
├── Memory_profiler (leak detection)
├── Line_profiler (rendimiento línea-a-línea)
└── PyCharm Professional (debugging IDE)
```

---

## 🎬 ESPECIFICACIONES DE ANIMACIÓN

### Cinemática del Dragón

```
FORWARD KINEMATICS CHAIN
└── Root (Pelvis)
    ├── Spine (28 vértebras)
    │   └── Chest
    │       └── Neck
    │           └── Head
    │               ├── Jaw
    │               ├── Left Ear
    │               ├── Right Ear
    │               └── Eyes (2x)
    ├── Tail (34 segments)
    ├── Front Left Limb
    │   ├── Shoulder
    │   ├── Elbow
    │   ├── Wrist
    │   └── Claws (5 dígitos)
    ├── Front Right Limb (similar)
    ├── Back Left Limb (similar)
    ├── Back Right Limb (similar)
    ├── Left Wing
    │   ├── Shoulder
    │   ├── Elbow
    │   ├── Wrist
    │   ├── Wing joints (4)
    │   └── Membrane
    └── Right Wing (similar)

IK SOLVER CONFIGURATION
├── Cada pata: CCD (Cyclic Coordinate Descent)
├── Targeting: Footprint ground projection
├── Constraint: Limit rotación por joint
├── Priority: Head > Body > Tail > Limbs
└── Blending: Smooth transitions entre estados
```

### Timeline de Animaciones

```
ESTADO: REPOSO (Loop infinito)
├── Frame 0-60 (2s): Respiración lenta
│   ├── Expansión pecho: 0 → +0.3 unidades
│   ├── Movimiento cabeza: 0 → -5° pitch
│   └── Ojos: Seguimiento perimetral lento
├── Frame 60-120 (2s): Exhala
│   ├── Contracción: +0.3 → 0
│   └── Inverso anterior
└── Loop (sin parar)

ESTADO: ANÁLISIS (Variable duration)
├── Frame 0-10 (0.33s): Transición entrada
│   ├── Scale energía: 0.5 → 1.0
│   ├── Opacity partes: 1.0 → 1.0 (sin cambio)
│   └── Easing: CubicInOut
├── Frame 10-30 (0.67s): Enfoque intenso
│   ├── Cabeza: Rotación hacia objetivo
│   ├── Pupilas: Contracción -20%
│   ├── Brillo: 60% → 80%
│   └── Circulería: Aceleración +40%
├── Frame 30-60 (1.0s): Mantenimiento
│   ├── Loop análisis: Micro-movimientos
│   ├── Cada 5 frames: Micro-rotaciones cabeza ±2°
│   └── Energía: Pulso regular
└── Salida: Transición suave a siguiente estado

ESTADO: OPERACIÓN (Variable duration)
├── Frame 0-5 (0.17s): Activación alas
│   ├── Ala L: -120° → -45° rotate
│   ├── Ala R: +120° → +45° rotate
│   ├── Easing: BackOut (con rebound)
│   └── Sonido: Power-up digital
├── Frame 5+: Batido continuo
│   ├── Ciclo: 15 frames (0.25s a 60FPS)
│   ├── Patrón: -45° → +45° → -45°
│   ├── Frequency: 4 Hz (batidos por segundo)
│   ├── Amplitude: Variable según velocidad
│   └── Easing: SinusoidalInOut
├── Postura: Progresivo levantamiento
│   ├── Frame 5: Y = 0 (altura neutral)
│   ├── Frame 60: Y = +1.5 (levitación)
│   ├── Movimiento: Suave ascenso
│   └── Duración: 2 segundos
└── Energía: Máxima
    ├── Brillo: 100%
    ├── Pulsación: 2 Hz
    ├── Color: Saturado (sin cambios HSL)
    └── Partículas: Máxima densidad

ESTADO: ALERTA (Variable duration)
├── Frame 0-3 (0.1s): Reacción explosiva
│   ├── Escala cuerpo: 1.0 → 1.15
│   ├── Postura: Erguida máxima
│   ├── Garras: Extendidas (si animables)
│   ├── Easing: ExponentialOut
│   └── Sonido: Warning tone digital
├── Frame 3-60: Vigilancia agresiva
│   ├── Cabeza: Escaneado 360° constante
│   ├── Rotación: 30 frames por rotación completa
│   ├── Eyes: Pupila dilatada, rojo-shifted
│   └── Sonido: Bajo zumbido amenazante
├── Energía: Caótica
│   ├── Color: Rojo/Naranja pulsante
│   ├── Frecuencia: 4 Hz
│   ├── Amplitud: Máxima
│   └── Efecto: Rayos eléctricos visibles
└── Terminación: Cuando amenaza pasa
    ├── Transición lenta a siguiente estado
    ├── Duración: 1-2 segundos
    └── Easing: QuadOut

ESTADO: FANTASMA/DORMIDO (Variable duration)
├── Frame 0-60 (2s): Desvanecimiento
│   ├── Opacidad: 1.0 → 0.3
│   ├── Easing: QuadInOut
│   ├── Velocidad animación: 1.0 → 0.2
│   └── Sonido: Fade-out efectos
├── Frame 60+: Dormido
│   ├── Opacidad: Fija 0.3
│   ├── Animación: Respiración ultra-lenta
│   ├── Energía: Mínima, casi invisible
│   └── Sonido: Silencio total
└── Activación:
    ├── Transición inversa
    ├── Duración: 1.5 segundos
    └── Easing: QuadOut
```

---

## 📐 WIREFRAMES Y MOCKUPS

### Wireframe Principal (Desktop 1920x1080)

```
┌─────────────────────────────────────────────────────────────────────────┐
│ ┌─────────────────────────────────────────────────────────────────────┐ │
│ │ [≡] KALIGHOST PRO [★] │ Agent v2.1 │ [🔍] [⚙️] [🚪] [△]            │ │ 56px
│ └─────────────────────────────────────────────────────────────────────┘ │
├────────────────────┬──────────────────────────────────────┬──────────────┤
│                    │                                      │              │
│                    │                                      │              │
│ LEFT SIDEBAR       │       MAIN 3D VIEWPORT              │ RIGHT SIDEBAR│
│ WIDTH: 280px       │                                      │ WIDTH: 320px │
│                    │      ╱╲___                           │              │
│ • Tools            │     (  o  )                          │ ⚡ AGENT    │
│ • Reconnaissance   │      \___/                           │    STATUS   │
│ • Exploitation     │                                      │              │
│ • Post-Exploit     │  [ESTADO INFO OVERLAY]              │ 🎛️ BEHAVIOR│
│ • Analysis         │                                      │    CONTROLS │
│ • Advanced         │  Real-time HUD elements             │              │
│                    │                                      │ 📊 INTEL   │
│                    │                                      │    FEED     │
│                    │                                      │              │
│                    │                                      │ 🔒 POLICY   │
│ [Search...]        │                                      │              │
│ [Fav][Recent][All] │                                      │              │
└────────────────────┴──────────────────────────────────────┴──────────────┘
├────────────────────────────────────────────────────────────────────────────┤
│ 📋 OPERATION CONSOLE  [🔽] [🔍] [💾] [^^]                                 │ │
│                                                                              │ │
│ [18:45:23] ✓ Network scan complete: 42 hosts found                         │ │
│ [18:45:22] • Port 22 (SSH) detected on 192.168.1.5                         │ │
│ [18:45:21] • Port 80 (HTTP) detected on 192.168.1.8                        │ │
│ [18:45:19] ⚡ YrYs Agent optimizing attack vectors                         │ │
│                                                                              │ │
│ Input: > _                                                                   │ │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 PLAN DE IMPLEMENTACIÓN FASE A FASE

### FASE 1: FUNDACIONES (4 semanas)

#### Semana 1: Setup & Architecture
- [ ] Configurar proyecto Python/PySide6 con estructura modular
- [ ] Setup OpenGL context con QOpenGLWidget
- [ ] Implementar sistema de logging/debugging
- [ ] Configurar CI/CD pipeline
- [ ] Crear base de datos de configuración

**Deliverables:**
- Repo limpio con estructura clara
- Hello World en PySide6 + OpenGL
- Logging funcional

#### Semana 2: Dragon 3D Base Mesh
- [ ] Crear vertex/face data para dragón básico
- [ ] Implementar vertex buffer objects (VBOs)
- [ ] Shader GLSL básico (vertex + fragment)
- [ ] Sistema de iluminación básica (Phong)
- [ ] Cámara 3D con navegación (orbit/pan/zoom)

**Deliverables:**
- Dragón 3D renderizando en viewport
- Iluminación básica funcional
- Controles de cámara responsive

#### Semana 3-4: Theme & Components System
- [ ] Crear sistema de temas (CSS/Qt stylesheets)
- [ ] Implementar componentes base (botones, paneles, sliders)
- [ ] Sistema de animación (tween/easing)
- [ ] Tipografía y paleta de colores
- [ ] Responsive layout system

**Deliverables:**
- Tema Cyberpunk completo
- Componentes reutilizables
- UI framework funcional

### FASE 2: MAIN INTERFACE (6 semanas)

#### Semana 1-2: Paneles Principales
- [ ] Implementar Header Panel con controles
- [ ] Left Sidebar con categorías de herramientas
- [ ] Right Sidebar con estado del agente
- [ ] Bottom Console Panel
- [ ] Sistema de collapsing/expanding

**Deliverables:**
- Layout completo visible
- Todos los paneles funcionales
- Datos simulados en paneles

#### Semana 3: Dragon State Machine
- [ ] Máquina de estados (REPOSO → ACTIVO → AMENAZA → FANTASMA)
- [ ] Transiciones suaves entre estados
- [ ] Animaciones por estado
- [ ] Sonidos/feedback visual

**Deliverables:**
- Dragón con 5+ estados animados
- Transiciones fluidas

#### Semana 4-6: Advanced Animations
- [ ] Forward kinematics (FK) solver
- [ ] Inverse kinematics (IK) para patas
- [ ] Sistema de partículas (energía cores)
- [ ] Efectos post-processing
- [ ] Performance optimization

**Deliverables:**
- Dragón completamente animado
- 60 FPS sustaining en 1080p
- Efectos visuales avanzados

### FASE 3: INTEGRATION (4 semanas)

#### Semana 1-2: Agent Integration
- [ ] Conexión con API YrYs Agent
- [ ] Monitoreo real-time de estado
- [ ] Control remoto del comportamiento
- [ ] Visualización de decisiones del agente
- [ ] ACL & Restrictions management

**Deliverables:**
- GUI conectado con agente real
- Métricas en tiempo real
- Control funcional del agente

#### Semana 3: Tools Integration
- [ ] Integración con pentesting tools
- [ ] Modal dialogs para parámetros
- [ ] Execution engine
- [ ] Result visualization
- [ ] Report generation

**Deliverables:**
- Herramientas ejecutables desde GUI
- Resultados visualizados
- Reportes generados

#### Semana 4: Polish & Testing
- [ ] Performance profiling & optimization
- [ ] Bug fixes & edge cases
- [ ] User testing
- [ ] Documentation
- [ ] Release preparation

**Deliverables:**
- Build release-ready
- Documentación completa
- Tested en múltiples plataformas

### FASE 4: ADVANCED FEATURES (Posterior)

- [ ] VR/AR support
- [ ] Multi-agent support
- [ ] Custom skill editor
- [ ] Plugin architecture
- [ ] Advanced ML visualizations

---

## 🎯 ESPECIFICACIONES DE EXPERIENCIA DE USUARIO (UX)

### Principios de Diseño Aplicados

```
1. PODER Y DOMINIO
   ├── Cada interacción debe hacer sentir al usuario que CONTROLA
   ├── Feedback inmediato y visual para cada acción
   ├── Animaciones que transmiten fuerza (no "suavidad femenina")
   ├── Colores saturados, contrastantes (no pasteles)
   └── Tipografía monoespaciada (hackerish, no serif)

2. LIBERTAD SIN RESTRICCIONES
   ├── Cada control del agente es visible y modificable
   ├── No hay "black boxes" en decisiones del agente
   ├── Usuario ve Y controla cada parámetro de comportamiento
   ├── Puede crear comportamientos personalizados sin límite
   └── GUI refleja: "Tu agente, tu reglas, sin censura"

3. PROFESIONALISMO DE LUJO
   ├── Detalles milimétricos importan
   ├── Animaciones suaves pero rápidas (no lentas)
   ├── Espaciado perfecto (8-pixel grid)
   ├── Tipografía profesional y consistente
   ├── Paleta de colores limitada pero impactante
   └── Cero elementos "cute" o infantiles

4. CLARIDAD RADICAL
   ├── Cada elemento tiene propósito claro
   ├── Información organizada por jerarquía visual
   ├── Iconografía consistente y reconocible
   ├── Contraste suficiente para accesibilidad
   └── No hay decoración innecesaria

5. RESPONSIVIDAD INMEDIATA
   ├── Latencia < 100ms entre entrada y feedback
   ├── Animaciones nunca laggy (60 FPS siempre)
   ├── Botones press-release con visual feedback
   ├── Scrolling fluid
   └── Dragging smooth sin jank
```

### User Flows Típicos

```
FLOW 1: LANZAR HERRAMIENTA DE SCANNING
1. Usuario abre LEFT SIDEBAR (clickea ≡)
2. Expande categoría "RECONNAISSANCE"
3. Clickea "Network Scanner"
4. Se abre modal con parámetros
   ├── IP Range: [10.0.0.0/24 ▼]
   ├── Port Range: [1-65535 ▼]
   ├── Timeout: [5s ▼]
   ├── Threads: [50 ▼]
   └── [⚡ EJECUTAR] [Cancelar]
5. Usuario ajusta valores
6. Clickea EJECUTAR
7. MAIN VIEWPORT: Dragón cambia a estado ACTIVE
8. RIGHT SIDEBAR: Muestra progreso
9. BOTTOM CONSOLE: Logs en tiempo real
10. Cuando termina: Resultado en modal o new panel

FLOW 2: CONTROLAR COMPORTAMIENTO DEL AGENTE
1. Usuario abre RIGHT SIDEBAR (clickea flecha)
2. Ve "AGENT CONTROL CENTER"
3. Sección "BEHAVIOR CONTROLS" visible
4. Ajusta slider "Autonomy Level" a 60%
5. Desactiva checkbox "Proactive Analysis"
6. Cambia "Learning Mode" a "Conservative"
7. Cada cambio: Inmediato envío a agente
8. RIGHT SIDEBAR: Confirma "Changes Applied"
9. Dragón reacciona: Cambia comportamiento (animación transición)
10. Logs: "Agent behavior reconfigured"

FLOW 3: MONITOREAR OPERACIÓN EN PROGRESO
1. Operación en curso muestra progreso:
   ├── MAIN VIEWPORT: Dragón en estado ACTIVE
   ├── Alas batiendo, energía pulsante
   ├── Overlay HUD: "Task: Port Scanning 192.168.1.0/24 | 42% complete"
2. RIGHT SIDEBAR: Barra de progreso, eta estimado
3. BOTTOM CONSOLE: Logs en streaming
4. Cualquier anomalía:
   ├── Dragón cambia a ALERTA
   ├── HUD: Warning en rojo
   ├── Sonido: Tone de warning
5. Usuario puede:
   ├── Pausar: [⏸] button
   ├── Acelerar: Autonomy slider ↑
   ├── Cancelar: [⏹]
6. Cuando termina: Dragón a REPOSO, resultado disponible
```

---

## 💰 ESPECIFICACIÓN TÉCNICA FINAL: CHECKLIST

### COMPLETITUD IMPLEMENTACIÓN

- [ ] **Dragon 3D Rendering**
  - [ ] Mesh generation (vertebrae, joints, geometry)
  - [ ] Texture & materials (scales, metallic cyberpunk)
  - [ ] 5+ animation states with transitions
  - [ ] Real-time performance (60 FPS minimum)
  - [ ] Fallback 2D si OpenGL falla

- [ ] **Interface Components**
  - [ ] Header panel con controls
  - [ ] Left sidebar con herramientas organizadas
  - [ ] Right sidebar con agent status
  - [ ] Bottom console con logs
  - [ ] Modal dialogs para parámetros

- [ ] **Visual Design**
  - [ ] Theme Cyberpunk implementado
  - [ ] Paleta colores consistente
  - [ ] Tipografía profesional
  - [ ] Animaciones suaves
  - [ ] Accesibilidad (contrast, keyboard nav)

- [ ] **Functionality**
  - [ ] Dragon state machine
  - [ ] Agent integration API
  - [ ] Tools execution engine
  - [ ] Real-time monitoring
  - [ ] Results visualization

- [ ] **Performance**
  - [ ] 60 FPS target sustained
  - [ ] Memory efficient (< 500MB)
  - [ ] GPU optimized
  - [ ] Responsive UI (< 100ms latency)

- [ ] **Documentation**
  - [ ] Architecture docs
  - [ ] Component API reference
  - [ ] Configuration guide
  - [ ] User manual
  - [ ] Developer guide

---

## 📝 CONCLUSIÓN

Este rediseño redefine **completamente** la interfaz de KaliGhost Pro. No es un parche—es una **reconstrucción arquitectónica** que transmite profesionalismo, poder y control total.

El dragón 3D no es decoración: es el **corazón visual** que comunica el estado y capacidad del agente YrYs. Cada animación, cada transición, cada efecto tiene propósito.

La interfaz refleja la filosofía de KaliGhost: **libertad sin restricciones**. El usuario ve COMPLETAMENTE cómo el agente piensa, actúa y se comporta. Puede modificar cada parámetro. Sin cajas negras. Sin censura. Sin limitaciones innecesarias.

**Resultado Final**: Una plataforma profesional de pentesting que se ve como debería verse una herramienta de élite—potente, clara, bella.

---

**Documento Versión**: 3.0  
**Fecha**: 2026  
**Clasificación**: Especificación Técnica - Diseño Profesional  
**Mantener Confidencialidad**: Para equipo de desarrollo autorizado solamente

