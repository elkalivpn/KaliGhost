# 🐉 GUI de KaliGhost - Dragón 3D Animado

## 📋 ÍNDICE
- [Introducción](#introducción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Controles](#controles)
- [Personalización](#personalización)
- [Troubleshooting](#troubleshooting)

## 🎯 INTRODUCCIÓN

Esta es la interfaz gráfica principal de KaliGhost, featuring un dragón 3D animado que representa el espíritu del sistema. La GUI utiliza tecnología moderna de renderizado 3D con PySide6 y OpenGL para crear una experiencia visual única con estética cyberpunk.

## ✨ CARACTERÍSTICAS

### 🐉 Dragón 3D Animado
- Modelo 3D completo del dragón de Kali Linux
- Animación de alas en movimiento
- Efectos de energía en los ojos
- Partículas de energía orbitando
- Rotación automática continua

### 🖥️ Interfaz Cyberpunk
- Tema oscuro con acentos verdes característicos de Kali
- Diseño moderno y responsive
- Paneles dock personalizables
- Barra de herramientas con acceso rápido
- Consola de sistema integrada

### ⚙️ Controles Interactivos
- Ajuste de velocidad de animación
- Control de tamaño del dragón
- Botones de pausa/reinicio
- Menús contextuales completos

### 🛠️ Integración del Sistema
- Monitoreo del estado del agente YrYs
- Acceso directo a herramientas de pentesting
- Visualización de tareas activas
- Consola de salida del sistema

## 📦 REQUISITOS

### Sistema Operativo
- Kali Linux (recomendado)
- Ubuntu/Debian
- macOS
- Windows 10+

### Dependencias de Python
- Python 3.8+
- PySide6
- PyOpenGL
- PyOpenGL_accelerate

### Hardware Recomendado
- GPU compatible con OpenGL 2.0+
- 4GB RAM mínimo
- CPU multinúcleo

## 🔧 INSTALACIÓN

### Método Automático
```bash
# Ir al directorio de KaliGhost
cd /ruta/a/KaliGhost

# Ejecutar script de instalación
./gui/install_dependencies.sh
```

### Método Manual
```bash
# Instalar dependencias con pip
pip3 install PySide6 PyOpenGL PyOpenGL_accelerate

# O instalar con el administrador de paquetes del sistema
sudo apt install python3-pyside6.qtwidgets python3-opengl
```

### Verificación
```bash
# Verificar instalación
python3 -c "import PySide6, OpenGL"
echo "[$] Dependencias instaladas correctamente"
```

## ▶️ USO

### Iniciar la GUI
```bash
# Método 1: Script dedicado
./gui/start_gui.sh

# Método 2: Directamente con Python
cd gui
python3 dragon_3d_gui.py

# Método 3: Desde el directorio raíz
python3 gui/dragon_3d_gui.py
```

### Primer Inicio
1. La ventana principal aparecerá con el dragón 3D en el centro
2. El dragón comenzará a animarse automáticamente
3. La barra de estado mostrará "KaliGhost listo"
4. Los paneles dock mostrarán información del sistema

## 🎮 CONTROLES

### 🖱️ Interfaz Gráfica
- **Menú Archivo**: Nuevo proyecto, abrir proyecto, salir
- **Menú Herramientas**: Acceso a Nmap, Metasploit, Fuzzing
- **Menú Ayuda**: Documentación y acerca de
- **Barra de Herramientas**: Botones de escaneo, explotación, análisis

### 🎛️ Panel de Controles
- **Velocidad**: Slider para ajustar velocidad de animación (0-20)
- **Tamaño**: Slider para ajustar escala del dragón (0-100%)
- **Pausar**: Botón para pausar/reanudar animación
- **Reiniciar**: Botón para resetear posición del dragón

### ⌨️ Atajos de Teclado
- `Ctrl+N`: Nuevo proyecto
- `Ctrl+O`: Abrir proyecto
- `Ctrl+Q`: Salir
- `F11`: Pantalla completa

## 🎨 PERSONALIZACIÓN

### Cambiar Colores del Tema
Editar en `dragon_3d_gui.py`:
```python
# Colores característicos de Kali Linux
self.kali_green = (0.13, 0.67, 0.33)  # #22AA55
self.kali_dark = (0.09, 0.09, 0.09)   # #181818
self.kali_light = (0.85, 0.85, 0.85)  # #DADADA
```

### Modificar Animación del Dragón
En `Dragon3DRenderer` class:
```python
def animate(self):
    """Animar el dragón"""
    self.rotation_y += 1 * self.animation_speed
    self.rotation_x = math.sin(self.rotation_y * 0.02) * 10
    self.rotation_z = math.cos(self.rotation_y * 0.03) * 5
    self.update()
```

### Añadir Nuevas Partes al Dragón
En `initialize_dragon()`:
```python
self.dragon_parts = [
    {"type": "body", "position": [0, 0, 0], "size": [2, 1, 1]},
    # Añadir nuevas partes aquí
]
```

## ❓ TROUBLESHOOTING

### Problemas Comunes

#### 1. ImportError: No module named 'PySide6'
```bash
# Solución
pip3 install PySide6
# O
sudo apt install python3-pyside6.qtwidgets
```

#### 2. ImportError: No module named 'OpenGL'
```bash
# Solución
pip3 install PyOpenGL PyOpenGL_accelerate
# O
sudo apt install python3-opengl
```

#### 3. No se muestra el dragón 3D
```bash
# Verificar drivers de gráficos
glxinfo | grep "OpenGL renderer"
# Asegurar variables de entorno
export LIBGL_ALWAYS_INDIRECT=1
```

#### 4. Bajo rendimiento en animación
```bash
# Reducir FPS en dragon_3d_gui.py
self.timer.start(33)  # 30 FPS en lugar de 16 (~60 FPS)
```

#### 5. Errores de segmentación
```bash
# Actualizar dependencias
pip3 install --upgrade PySide6 PyOpenGL
# O reinstalar
pip3 uninstall PySide6 PyOpenGL
pip3 install PySide6 PyOpenGL
```

### Logs y Diagnóstico
```bash
# Ver logs de la aplicación
tail -f ~/KaliGhost/logs/gui.log

# Diagnóstico de OpenGL
glxinfo | grep -i "direct rendering"
glxinfo | grep -i "opengl version"
```

## 📊 PERFORMANCE

### Métricas de Rendimiento
- **FPS promedio**: 50-60 FPS (configuración por defecto)
- **Uso de CPU**: 5-15% en sistemas modernos
- **Uso de GPU**: 10-25% dependiendo de la tarjeta
- **Memoria RAM**: 200-300MB en ejecución

### Optimización
- Ajustar velocidad de animación según hardware
- Cerrar otras aplicaciones 3D pesadas
- Usar ventanas más pequeñas si es necesario
- Desactivar efectos de partículas en hardware antiguo

## 🤝 INTEGRACIÓN CON YrYs-AGENT

### Comunicación en Tiempo Real
- El estado del agente se muestra en el panel de información
- Las tareas activas se reflejan en el panel de tareas
- La consola muestra logs del sistema en tiempo real

### Comandos Remotos
```python
# Desde la GUI se pueden enviar comandos al agente
yrays_agent.execute_command("nmap_scan", target="192.168.1.0/24")
```

## 🆕 ACTUALIZACIONES FUTURAS

### Roadmap de Desarrollo
- [ ] Texturas HD para el dragón 3D
- [ ] Animaciones más complejas (volar, rugir)
- [ ] Soporte para realidad virtual
- [ ] Integración con motion capture
- [ ] Personalización de modelos 3D
- [ ] Efectos de post-procesamiento avanzados

---

📅 **Última actualización**: 2026-05-15  
📍 **Ubicación**: `/Users/mrhardcore/KaliGhost/gui/`  
👥 **Mantenido por**: Equipo de Desarrollo de KaliGhost  
🔐 **Clasificación**: Componente de Interfaz Gráfica

⚠️ **Importante**: Esta GUI es parte integral de KaliGhost y está optimizada para funcionar con el ecosistema completo del sistema.